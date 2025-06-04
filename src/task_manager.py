import yaml
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

from .config import config, logger

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    id: str
    name: str
    description: str
    type: str
    parameters: Dict
    status: TaskStatus = TaskStatus.PENDING
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output_path: Optional[str] = None
    error_message: Optional[str] = None

class TaskManager:
    def __init__(self):
        self.db_path = config.DATABASE_PATH
        self._init_database()
    
    def _init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    type TEXT NOT NULL,
                    parameters TEXT,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP,
                    output_path TEXT,
                    error_message TEXT
                )
            """)
            conn.commit()
    
    def load_tasks_from_yaml(self, yaml_path: Path) -> List[Task]:
        try:
            with open(yaml_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            
            tasks = []
            for task_data in data.get('tasks', []):
                task = Task(
                    id=task_data['id'],
                    name=task_data['name'],
                    description=task_data.get('description', ''),
                    type=task_data['type'],
                    parameters=task_data.get('parameters', {}),
                    created_at=datetime.now()
                )
                tasks.append(task)
            
            logger.info(f"Loaded {len(tasks)} tasks from {yaml_path}")
            return tasks
        
        except Exception as e:
            logger.error(f"Failed to load tasks from {yaml_path}: {e}")
            return []
    
    def save_task(self, task: Task):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO tasks 
                (id, name, description, type, parameters, status, created_at, 
                 started_at, completed_at, output_path, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.id, task.name, task.description, task.type,
                yaml.dump(task.parameters), task.status.value,
                task.created_at, task.started_at, task.completed_at,
                task.output_path, task.error_message
            ))
            conn.commit()
    
    def get_task(self, task_id: str) -> Optional[Task]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            
            if row:
                return Task(
                    id=row[0], name=row[1], description=row[2], type=row[3],
                    parameters=yaml.safe_load(row[4]), status=TaskStatus(row[5]),
                    created_at=datetime.fromisoformat(row[6]) if row[6] else None,
                    started_at=datetime.fromisoformat(row[7]) if row[7] else None,
                    completed_at=datetime.fromisoformat(row[8]) if row[8] else None,
                    output_path=row[9], error_message=row[10]
                )
        return None
    
    def get_all_tasks(self) -> List[Task]:
        tasks = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            for row in cursor.fetchall():
                task = Task(
                    id=row[0], name=row[1], description=row[2], type=row[3],
                    parameters=yaml.safe_load(row[4]), status=TaskStatus(row[5]),
                    created_at=datetime.fromisoformat(row[6]) if row[6] else None,
                    started_at=datetime.fromisoformat(row[7]) if row[7] else None,
                    completed_at=datetime.fromisoformat(row[8]) if row[8] else None,
                    output_path=row[9], error_message=row[10]
                )
                tasks.append(task)
        return tasks
    
    def update_task_status(self, task_id: str, status: TaskStatus, 
                          output_path: Optional[str] = None, 
                          error_message: Optional[str] = None):
        task = self.get_task(task_id)
        if task:
            task.status = status
            if status == TaskStatus.RUNNING and not task.started_at:
                task.started_at = datetime.now()
            elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
                task.completed_at = datetime.now()
            
            if output_path:
                task.output_path = output_path
            if error_message:
                task.error_message = error_message
            
            self.save_task(task)
    
    def get_task_statistics(self) -> Dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT status, COUNT(*) FROM tasks GROUP BY status
            """)
            stats = dict(cursor.fetchall())
            
            cursor = conn.execute("SELECT COUNT(*) FROM tasks")
            total = cursor.fetchone()[0]
            
            return {
                'total': total,
                'pending': stats.get('pending', 0),
                'running': stats.get('running', 0),
                'completed': stats.get('completed', 0),
                'failed': stats.get('failed', 0),
                'success_rate': (stats.get('completed', 0) / total * 100) if total > 0 else 0
            }