import os
import subprocess
import asyncio
import json
import click
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
import psutil
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, TaskID
from rich.panel import Panel

from .config import config, logger
from .task_manager import TaskManager, Task, TaskStatus

console = Console()

class ClaudeAgent:
    def __init__(self):
        self.task_manager = TaskManager()
        self.workspace_dir = config.WORKSPACE_DIR
        self.workspace_dir.mkdir(exist_ok=True)
    
    def execute_claude_command(self, instruction: str, working_dir: Optional[Path] = None) -> Dict:
        try:
            work_dir = working_dir or self.workspace_dir
            work_dir.mkdir(exist_ok=True)
            
            # Use --print option for non-interactive execution
            cmd = [config.CLAUDE_CODE_COMMAND, "--print", instruction]
            
            # Prepare environment variables
            env = os.environ.copy()
            env['CLAUDE_TRUST_WORKSPACE'] = 'true'
            
            logger.info(f"Executing Claude Code: {' '.join(cmd)}")
            logger.info(f"Working directory: {work_dir}")
            
            result = subprocess.run(
                cmd,
                cwd=work_dir,
                capture_output=True,
                text=True,
                env=env,
                timeout=config.CLAUDE_CODE_TIMEOUT
            )
            
            # Check if we got an interactive prompt error
            if result.stderr and "Raw mode is not supported" in result.stderr:
                logger.warning("Claude Code requires interactive mode. Retrying with permissions skip...")
                # Retry with --dangerously-skip-permissions for Docker/CI environments
                cmd_retry = [config.CLAUDE_CODE_COMMAND, "--print", "--dangerously-skip-permissions", instruction]
                result = subprocess.run(
                    cmd_retry,
                    cwd=work_dir,
                    capture_output=True,
                    text=True,
                    env=env,
                    timeout=config.CLAUDE_CODE_TIMEOUT
                )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        
        except subprocess.TimeoutExpired:
            logger.error(f"Claude Code command timed out after {config.CLAUDE_CODE_TIMEOUT} seconds")
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Command timed out',
                'returncode': -1
            }
        except Exception as e:
            logger.error(f"Failed to execute Claude Code command: {e}")
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }
    
    def generate_instruction(self, task: Task) -> str:
        task_type = task.type.lower()
        params = task.parameters
        
        if task_type == "python_script":
            return f"Create a Python script that {task.description}. Save it as {params.get('filename', 'script.py')}."
        
        elif task_type == "web_app":
            framework = params.get('framework', 'Flask')
            return f"Create a {framework} web application: {task.description}. Include all necessary files and dependencies."
        
        elif task_type == "data_analysis":
            input_file = params.get('input_file', 'data.csv')
            return f"Analyze the data file {input_file} and {task.description}. Create a summary report."
        
        elif task_type == "code_review":
            target_file = params.get('target_file', '.')
            return f"Review the code in {target_file} and {task.description}. Provide recommendations."
        
        else:
            return task.description
    
    def execute_task(self, task: Task) -> bool:
        try:
            logger.info(f"Starting task: {task.name} (ID: {task.id})")
            
            self.task_manager.update_task_status(task.id, TaskStatus.RUNNING)
            
            instruction = self.generate_instruction(task)
            
            task_workspace = self.workspace_dir / f"task_{task.id}"
            task_workspace.mkdir(exist_ok=True)
            
            result = self.execute_claude_command(instruction, task_workspace)
            
            output_file = task_workspace / "execution_log.json"
            with open(output_file, 'w') as f:
                json.dump({
                    'task_id': task.id,
                    'instruction': instruction,
                    'timestamp': datetime.now().isoformat(),
                    'result': result
                }, f, indent=2)
            
            if result['success']:
                self.task_manager.update_task_status(
                    task.id, TaskStatus.COMPLETED, 
                    output_path=str(task_workspace)
                )
                logger.info(f"Task {task.id} completed successfully")
                return True
            else:
                self.task_manager.update_task_status(
                    task.id, TaskStatus.FAILED,
                    error_message=result['stderr']
                )
                logger.error(f"Task {task.id} failed: {result['stderr']}")
                return False
        
        except Exception as e:
            logger.error(f"Exception during task execution: {e}")
            self.task_manager.update_task_status(
                task.id, TaskStatus.FAILED,
                error_message=str(e)
            )
            return False
    
    def run_tasks_from_file(self, task_file: Path) -> Dict:
        tasks = self.task_manager.load_tasks_from_yaml(task_file)
        
        if not tasks:
            logger.error("No tasks found in file")
            return {'success': False, 'completed': 0, 'failed': 0}
        
        completed = 0
        failed = 0
        
        with Progress() as progress:
            task_progress = progress.add_task("[green]Processing tasks...", total=len(tasks))
            
            for task in tasks:
                self.task_manager.save_task(task)
                
                progress.update(task_progress, description=f"[green]Processing: {task.name}")
                
                if self.execute_task(task):
                    completed += 1
                else:
                    failed += 1
                
                progress.advance(task_progress)
        
        return {
            'success': failed == 0,
            'completed': completed,
            'failed': failed,
            'total': len(tasks)
        }
    
    def health_check(self) -> Dict:
        health_status = {
            'claude_code_available': False,
            'system_resources': {},
            'workspace_writable': False,
            'database_accessible': False
        }
        
        try:
            result = subprocess.run(
                [config.CLAUDE_CODE_COMMAND, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            health_status['claude_code_available'] = result.returncode == 0
        except:
            pass
        
        try:
            health_status['system_resources'] = {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent
            }
        except:
            pass
        
        try:
            test_file = self.workspace_dir / "health_check.txt"
            test_file.write_text("test")
            test_file.unlink()
            health_status['workspace_writable'] = True
        except:
            pass
        
        try:
            self.task_manager.get_task_statistics()
            health_status['database_accessible'] = True
        except:
            pass
        
        return health_status
    
    def show_dashboard(self):
        stats = self.task_manager.get_task_statistics()
        health = self.health_check()
        
        console.print(Panel.fit("📊 Claude Agent System Dashboard", style="bold blue"))
        
        # Task Statistics
        task_table = Table(title="Task Statistics")
        task_table.add_column("Status", style="cyan")
        task_table.add_column("Count", style="magenta")
        task_table.add_column("Percentage", style="green")
        
        total = stats['total']
        if total > 0:
            task_table.add_row("Total", str(total), "100%")
            task_table.add_row("Pending", str(stats['pending']), f"{stats['pending']/total*100:.1f}%")
            task_table.add_row("Running", str(stats['running']), f"{stats['running']/total*100:.1f}%")
            task_table.add_row("Completed", str(stats['completed']), f"{stats['completed']/total*100:.1f}%")
            task_table.add_row("Failed", str(stats['failed']), f"{stats['failed']/total*100:.1f}%")
            task_table.add_row("Success Rate", f"{stats['success_rate']:.1f}%", "")
        else:
            task_table.add_row("No tasks found", "", "")
        
        console.print(task_table)
        
        # Health Status
        health_table = Table(title="System Health")
        health_table.add_column("Component", style="cyan")
        health_table.add_column("Status", style="magenta")
        
        health_table.add_row("Claude Code", "✅ Available" if health['claude_code_available'] else "❌ Not Available")
        health_table.add_row("Workspace", "✅ Writable" if health['workspace_writable'] else "❌ Not Writable")
        health_table.add_row("Database", "✅ Accessible" if health['database_accessible'] else "❌ Not Accessible")
        
        if health['system_resources']:
            resources = health['system_resources']
            health_table.add_row("CPU Usage", f"{resources['cpu_percent']:.1f}%")
            health_table.add_row("Memory Usage", f"{resources['memory_percent']:.1f}%")
            health_table.add_row("Disk Usage", f"{resources['disk_usage']:.1f}%")
        
        console.print(health_table)
        
        # Recent Tasks
        recent_tasks = self.task_manager.get_all_tasks()[:5]
        if recent_tasks:
            recent_table = Table(title="Recent Tasks")
            recent_table.add_column("ID", style="cyan")
            recent_table.add_column("Name", style="magenta")
            recent_table.add_column("Status", style="green")
            recent_table.add_column("Completed", style="yellow")
            
            for task in recent_tasks:
                status_emoji = {
                    TaskStatus.PENDING: "⏳",
                    TaskStatus.RUNNING: "🔄",
                    TaskStatus.COMPLETED: "✅",
                    TaskStatus.FAILED: "❌"
                }
                completed_time = task.completed_at.strftime("%Y-%m-%d %H:%M") if task.completed_at else "N/A"
                recent_table.add_row(
                    task.id[:8],
                    task.name[:30],
                    f"{status_emoji.get(task.status, '❓')} {task.status.value}",
                    completed_time
                )
            
            console.print(recent_table)

@click.group()
def cli():
    """Claude Agent System - Automated task execution using Claude Code."""
    pass

@cli.command()
@click.option('--task-file', '-f', type=click.Path(exists=True), required=True,
              help='Path to YAML file containing tasks')
def run(task_file):
    """Run tasks from a YAML file."""
    agent = ClaudeAgent()
    result = agent.run_tasks_from_file(Path(task_file))
    
    if result['success']:
        console.print(f"✅ All {result['total']} tasks completed successfully!", style="green")
    else:
        console.print(f"❌ {result['failed']} out of {result['total']} tasks failed.", style="red")
        console.print(f"✅ {result['completed']} tasks completed successfully.", style="green")

@cli.command()
def dashboard():
    """Show the system dashboard."""
    agent = ClaudeAgent()
    agent.show_dashboard()

@cli.command()
def health():
    """Run system health check."""
    agent = ClaudeAgent()
    health_status = agent.health_check()
    
    console.print(Panel.fit("🏥 System Health Check", style="bold blue"))
    
    all_good = all([
        health_status['claude_code_available'],
        health_status['workspace_writable'],
        health_status['database_accessible']
    ])
    
    if all_good:
        console.print("✅ All systems operational!", style="green")
    else:
        console.print("❌ Some issues detected:", style="red")
        if not health_status['claude_code_available']:
            console.print("  - Claude Code not available", style="red")
        if not health_status['workspace_writable']:
            console.print("  - Workspace not writable", style="red")
        if not health_status['database_accessible']:
            console.print("  - Database not accessible", style="red")

if __name__ == '__main__':
    cli()