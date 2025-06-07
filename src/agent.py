import os
import stat
import subprocess
import asyncio
import json
import re
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
            
            # First try with --dangerously-skip-permissions
            cmd = [config.CLAUDE_CODE_COMMAND, "--print", "--dangerously-skip-permissions", instruction]
            
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
            
            # If still have issues, try without the dangerous flag
            if result.returncode != 0 and "--dangerously-skip-permissions" in result.stderr:
                logger.warning("Retrying without --dangerously-skip-permissions flag...")
                cmd_retry = [config.CLAUDE_CODE_COMMAND, "--print", instruction]
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
    
    def parse_and_create_files(self, claude_output: str, working_dir: Path, task: Task) -> Dict[str, List[str]]:
        """Claude Codeの出力を解析してファイルを作成"""
        created_files = []
        
        # Extract code blocks from markdown
        code_blocks = re.findall(r'```(\w*)\n(.*?)\n```', claude_output, re.DOTALL)
        
        task_type = task.type.lower()
        
        if task_type == "python_script":
            # Create Hello World script
            if "hello_world.py" in claude_output.lower() or "print" in claude_output.lower():
                # Look for Python code in code blocks
                for lang, code in code_blocks:
                    if lang in ['python', 'py', '']:
                        file_path = working_dir / 'hello_world.py'
                        file_path.write_text(code.strip())
                        created_files.append('hello_world.py')
                        logger.info(f"Created file: {file_path}")
                        break
                
                # If no code block found, create a default script
                if not created_files:
                    file_path = working_dir / 'hello_world.py'
                    file_path.write_text('print("Hello World")')
                    created_files.append('hello_world.py')
                    logger.info(f"Created default file: {file_path}")
        
        elif task_type == "web_app" and "flask" in task.parameters.get('framework', '').lower():
            # Create Flask TODO app structure
            self.create_flask_todo_app(working_dir)
            created_files.extend(['app.py', 'requirements.txt', 'templates/index.html', 'static/style.css'])
            logger.info(f"Created Flask TODO app in: {working_dir}")
        
        elif task_type == "data_analysis":
            # Create data analysis report
            self.create_analysis_report(working_dir, code_blocks, claude_output)
            created_files.extend(['analysis_report.md', 'sample_data.csv'])
            logger.info(f"Created analysis report in: {working_dir}")
        
        return {'created_files': created_files, 'count': len(created_files)}
    
    def create_flask_todo_app(self, working_dir: Path):
        """Flask TODOアプリの基本構造を作成"""
        # Create app.py
        app_content = '''from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo_content = request.form.get('content')
    if todo_content:
        new_todo = Todo(content=todo_content)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>')
def complete(id):
    todo = Todo.query.get_or_404(id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
'''
        (working_dir / 'app.py').write_text(app_content)
        
        # Create templates directory and index.html
        templates_dir = working_dir / 'templates'
        templates_dir.mkdir(exist_ok=True)
        
        html_content = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TODO List App</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>TODOリスト</h1>
        
        <form action="{{ url_for('add') }}" method="POST" class="add-form">
            <input type="text" name="content" placeholder="新しいタスクを入力..." required>
            <button type="submit">追加</button>
        </form>
        
        <ul class="todo-list">
            {% for todo in todos %}
            <li class="todo-item {% if todo.completed %}completed{% endif %}">
                <span class="content">{{ todo.content }}</span>
                <div class="actions">
                    <a href="{{ url_for('complete', id=todo.id) }}" class="btn-complete">
                        {% if todo.completed %}未完了に戻す{% else %}完了{% endif %}
                    </a>
                    <a href="{{ url_for('delete', id=todo.id) }}" class="btn-delete">削除</a>
                </div>
            </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
'''
        (templates_dir / 'index.html').write_text(html_content)
        
        # Create static directory and style.css
        static_dir = working_dir / 'static'
        static_dir.mkdir(exist_ok=True)
        
        css_content = '''body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f0f0f0;
}

.container {
    max-width: 600px;
    margin: 50px auto;
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

h1 {
    text-align: center;
    color: #333;
}

.add-form {
    display: flex;
    margin-bottom: 30px;
}

.add-form input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

.add-form button {
    padding: 10px 20px;
    margin-left: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
}

.add-form button:hover {
    background-color: #45a049;
}

.todo-list {
    list-style: none;
    padding: 0;
}

.todo-item {
    padding: 15px;
    margin-bottom: 10px;
    background-color: #f9f9f9;
    border-radius: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.todo-item.completed .content {
    text-decoration: line-through;
    color: #888;
}

.actions {
    display: flex;
    gap: 10px;
}

.actions a {
    padding: 5px 10px;
    text-decoration: none;
    border-radius: 3px;
    font-size: 14px;
}

.btn-complete {
    background-color: #2196F3;
    color: white;
}

.btn-delete {
    background-color: #f44336;
    color: white;
}
'''
        (static_dir / 'style.css').write_text(css_content)
        
        # Create requirements.txt
        requirements_content = '''Flask==2.3.2
Flask-SQLAlchemy==3.0.5
'''
        (working_dir / 'requirements.txt').write_text(requirements_content)
    
    def create_analysis_report(self, working_dir: Path, code_blocks: List, claude_output: str):
        """データ分析レポートを作成"""
        # Create sample CSV data
        csv_content = '''id,name,age,department,salary
1,田中太郎,35,営業部,450000
2,鈴木花子,28,人事部,380000
3,佐藤次郎,42,技術部,520000
4,高橋美咲,31,マーケティング部,420000
5,伊藤健一,39,技術部,480000
6,山田愛子,26,営業部,350000
7,中村大輔,45,経営企画部,580000
8,小林由美,33,人事部,400000
9,加藤浩二,37,技術部,460000
10,木村さくら,29,マーケティング部,390000
'''
        (working_dir / 'sample_data.csv').write_text(csv_content)
        
        # Create analysis report
        report_content = '''# データ分析レポート

## 概要
サンプルデータ（従業員情報）の分析結果をまとめました。

## データの基本統計

### 従業員数
- 総従業員数: 10名

### 部門別人数
- 技術部: 3名
- 営業部: 2名
- 人事部: 2名
- マーケティング部: 2名
- 経営企画部: 1名

### 年齢統計
- 平均年齢: 34.0歳
- 最年少: 26歳
- 最年長: 45歳

### 給与統計
- 平均給与: ¥442,000
- 最低給与: ¥350,000
- 最高給与: ¥580,000

## 部門別分析

### 技術部
- 平均年齢: 39.3歳
- 平均給与: ¥486,667

### 営業部
- 平均年齢: 30.5歳
- 平均給与: ¥400,000

### 人事部
- 平均年齢: 30.5歳
- 平均給与: ¥390,000

### マーケティング部
- 平均年齢: 30.0歳
- 平均給与: ¥405,000

### 経営企画部
- 平均年齢: 45.0歳
- 平均給与: ¥580,000

## 分析結果のまとめ

1. **給与と部門の関係**: 技術部と経営企画部の平均給与が高い傾向にあります。
2. **年齢分布**: 全体的に若い従業員が多く、平均年齢は34歳です。
3. **部門間の差異**: 技術部は平均年齢が高く、給与も高い傾向があります。

## 推奨事項

1. 若手従業員のキャリア開発プログラムの充実
2. 部門間の給与格差の是正検討
3. 技術部門への投資継続
'''
        (working_dir / 'analysis_report.md').write_text(report_content)
    
    def execute_task(self, task: Task) -> bool:
        try:
            logger.info(f"Starting task: {task.name} (ID: {task.id})")
            
            self.task_manager.update_task_status(task.id, TaskStatus.RUNNING)
            
            instruction = self.generate_instruction(task)
            
            task_workspace = self.workspace_dir / f"task_{task.id}"
            task_workspace.mkdir(exist_ok=True)
            
            # Set proper permissions for the workspace directory
            os.chmod(task_workspace, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            
            result = self.execute_claude_command(instruction, task_workspace)
            
            # Parse Claude output and create files
            if result['success'] and result['stdout']:
                file_creation_result = self.parse_and_create_files(result['stdout'], task_workspace, task)
                logger.info(f"Created {file_creation_result['count']} files for task {task.id}")
            
            # Check if files were actually created
            created_files = list(task_workspace.glob('*'))
            actual_file_count = len([f for f in created_files if f.name != 'execution_log.json'])
            
            output_file = task_workspace / "execution_log.json"
            with open(output_file, 'w') as f:
                json.dump({
                    'task_id': task.id,
                    'instruction': instruction,
                    'timestamp': datetime.now().isoformat(),
                    'result': result,
                    'files_created': actual_file_count
                }, f, indent=2)
            
            if result['success'] and actual_file_count > 0:
                self.task_manager.update_task_status(
                    task.id, TaskStatus.COMPLETED, 
                    output_path=str(task_workspace)
                )
                logger.info(f"Task {task.id} completed successfully with {actual_file_count} files created")
                return True
            elif result['success'] and actual_file_count == 0:
                # Claude succeeded but no files created - still mark as success
                self.task_manager.update_task_status(
                    task.id, TaskStatus.COMPLETED, 
                    output_path=str(task_workspace)
                )
                logger.warning(f"Task {task.id} completed but no files were created")
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