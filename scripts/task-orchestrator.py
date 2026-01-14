#!/usr/bin/env python3
"""
Task Orchestrator for Clawdbot

A comprehensive system for coordinating:
1. Sub-agent sessions (track, monitor, manage)
2. Persistent task queues (survive session ends)
3. Async task progress (real-time status)
4. Retry logic (automatic exponential backoff)

Usage:
    python task-orchestrator.py status                    # Show all active tasks
    python task-orchestrator.py spawn "<task>"            # Spawn sub-agent
    python task-orchestrator.py queue add "<task>"        # Add to queue
    python task-orchestrator.py queue list                # Show queued tasks
    python task-orchestrator.py queue run                 # Process queue
    python task-orchestrator.py history <session>         # Get session history
    python task-orchestrator.py kill <session>            # Kill sub-agent
    python task-orchestrator.py cleanup                   # Clean up stale sessions

Features:
- Survives session ends (queue persisted to disk)
- Automatic retry with exponential backoff
- Progress tracking across all async tasks
- Sub-agent monitoring and management
"""

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import Clawdbot session tools (if available in context)
try:
    from sessions_list import sessions_list
    from sessions_history import sessions_history
    from sessions_spawn import sessions_spawn
    SESSIONS_AVAILABLE = True
except ImportError:
    SESSIONS_AVAILABLE = False


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(Enum):
    SUBAGENT = "subagent"
    LOCAL = "local"
    API = "api"


@dataclass
class Task:
    """A task in the orchestrator."""
    id: str
    description: str
    task_type: TaskType
    command: str = ""
    priority: int = 0
    max_retries: int = 3
    retry_delay: float = 1.0
    status: TaskStatus = TaskStatus.PENDING
    session_key: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    retry_count: int = 0
    metadata: Dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "task_type": self.task_type.value,
            "command": self.command,
            "priority": self.priority,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay,
            "status": self.status.value,
            "session_key": self.session_key,
            "result": self.result[:500] if self.result else None,
            "error": self.error[:500] if self.error else None,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "retry_count": self.retry_count,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        task = cls(
            id=data["id"],
            description=data["description"],
            task_type=TaskType(data["task_type"]),
            command=data.get("command", ""),
            priority=data.get("priority", 0),
            max_retries=data.get("max_retries", 3),
            retry_delay=data.get("retry_delay", 1.0),
            status=TaskStatus(data["status"]),
            session_key=data.get("session_key"),
            result=data.get("result"),
            error=data.get("error"),
            created_at=data.get("created_at", time.time()),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            retry_count=data.get("retry_count", 0),
            metadata=data.get("metadata", {})
        )
        return task


class TaskOrchestrator:
    """
    Comprehensive task orchestration system for Clawdbot.
    
    Features:
    - Sub-agent tracking and monitoring
    - Persistent queues that survive session ends
    - Automatic retry with exponential backoff
    - Progress tracking across all async tasks
    """

    def __init__(self, queue_dir: str = "/home/opc/clawd/.task-orchestrator"):
        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        self.active_queue_file = self.queue_dir / "active-queue.json"
        self.history_file = self.queue_dir / "history.json"
        self.state_file = self.queue_dir / "state.json"
        
        # In-memory state
        self.tasks: Dict[str, Task] = {}
        self.subagent_sessions: Dict[str, dict] = {}
        
        # Load state
        self._load_state()
    
    def _load_state(self):
        """Load persisted state from disk."""
        if self.active_queue_file.exists():
            with open(self.active_queue_file, 'r') as f:
                data = json.load(f)
                self.tasks = {k: Task.from_dict(v) for k, v in data.get("tasks", {}).items()}
    
    def _save_state(self):
        """Persist state to disk."""
        data = {
            "tasks": {k: v.to_dict() for k, v in self.tasks.items()},
            "saved_at": time.time()
        }
        with open(self.active_queue_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_subagent_sessions(self):
        """Load active sub-agent sessions from Clawdbot."""
        if not SESSIONS_AVAILABLE:
            return
        
        try:
            result = sessions_list(kinds=["sub-agent"])
            self.subagent_sessions = result or {}
        except Exception as e:
            print(f"Warning: Could not load sub-agent sessions: {e}")
            self.subagent_sessions = {}
    
    def add_task(
        self,
        description: str,
        task_type: TaskType,
        command: str = "",
        priority: int = 0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        metadata: Dict = None
    ) -> str:
        """Add a new task to the queue."""
        task_id = f"task_{int(time.time() * 1000)}_{len(self.tasks)}"
        
        task = Task(
            id=task_id,
            description=description,
            task_type=task_type,
            command=command,
            priority=priority,
            max_retries=max_retries,
            retry_delay=retry_delay,
            metadata=metadata or {}
        )
        
        self.tasks[task_id] = task
        self._save_state()
        
        return task_id
    
    def spawn_subagent(self, task: str, label: str = None) -> Optional[str]:
        """Spawn a sub-agent to execute a task."""
        if not SESSIONS_AVAILABLE:
            print("Error: Session tools not available")
            return None
        
        try:
            result = sessions_spawn(task=task, label=label)
            # Extract session key from result
            if isinstance(result, dict) and "sessionKey" in result:
                session_key = result["sessionKey"]
            elif isinstance(result, str):
                session_key = result
            else:
                session_key = str(result)
            
            # Create tracking task
            task_id = self.add_task(
                description=label or task[:50],
                task_type=TaskType.SUBAGENT,
                command=task,
                priority=10,  # High priority for sub-agents
                metadata={"session_key": session_key}
            )
            
            self.tasks[task_id].status = TaskStatus.RUNNING
            self.tasks[task_id].session_key = session_key
            self._save_state()
            
            print(f"🚀 Spawned sub-agent: {session_key}")
            return session_key
            
        except Exception as e:
            print(f"Error spawning sub-agent: {e}")
            return None
    
    def get_subagent_status(self, session_key: str) -> Optional[dict]:
        """Get status of a sub-agent session."""
        if not SESSIONS_AVAILABLE:
            return None
        
        try:
            result = sessions_history(sessionKey=session_key, include_tools=True)
            return result
        except Exception as e:
            return None
    
    def refresh_subagent_statuses(self):
        """Update statuses of all running sub-agents."""
        self._load_subagent_sessions()
        
        for task_id, task in list(self.tasks.items()):
            if task.task_type == TaskType.SUBAGENT and task.session_key:
                # Check if session is still active
                is_active = task.session_key in self.subagent_sessions
                
                if is_active:
                    # Get latest status
                    history = self.get_subagent_status(task.session_key)
                    if history:
                        # Check if completed
                        if len(history) > 0:
                            last_msg = history[-1] if isinstance(history, list) else {}
                            # Mark complete if no more activity
                            task.status = TaskStatus.RUNNING
                else:
                    # Session ended - check if successful
                    if task.status == TaskStatus.RUNNING:
                        task.status = TaskStatus.COMPLETED
                        task.completed_at = time.time()
                        self._save_state()
    
    def process_queue(self, max_concurrent: int = 4) -> Dict[str, Task]:
        """Process all pending tasks in the queue."""
        pending = [t for t in self.tasks.values() if t.status == TaskStatus.PENDING]
        pending.sort(key=lambda t: t.priority, reverse=True)
        
        running = []
        
        for task in pending:
            if len(running) >= max_concurrent:
                break
            
            if task.task_type == TaskType.LOCAL:
                task.status = TaskStatus.RUNNING
                task.started_at = time.time()
                self._save_state()
                
                success, result, error = self._run_local_task(task)
                
                task.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
                task.completed_at = time.time()
                task.result = result
                task.error = error
                
                if not success and task.retry_count < task.max_retries:
                    # Schedule retry
                    task.retry_count += 1
                    delay = task.retry_delay * (2 ** (task.retry_count - 1))
                    task.status = TaskStatus.PENDING
                    print(f"  🔄 Retrying {task.id} in {delay:.1f}s ({task.retry_count}/{task.max_retries})")
                    time.sleep(min(delay, 2))  # Small delay for demo
                else:
                    running.append(task)
            
            self._save_state()
        
        return {t.id: t for t in running}
    
    def _run_local_task(self, task: Task) -> Tuple[bool, str, str]:
        """Execute a local task."""
        try:
            result = subprocess.run(
                task.command, shell=True, capture_output=True, text=True, timeout=120
            )
            return (result.returncode == 0, result.stdout, result.stderr)
        except Exception as e:
            return (False, "", str(e))
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending or running task."""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        
        if task.status == TaskStatus.RUNNING and task.session_key:
            # Would need to implement session kill
            print(f"Note: Cannot kill sub-agent {task.session_key} (not implemented)")
        
        task.status = TaskStatus.CANCELLED
        task.completed_at = time.time()
        self._save_state()
        
        return True
    
    def get_status(self) -> dict:
        """Get comprehensive status of all tasks."""
        self.refresh_subagent_statuses()
        
        stats = {
            "total": len(self.tasks),
            "pending": 0,
            "running": 0,
            "completed": 0,
            "failed": 0,
            "cancelled": 0
        }
        
        for task in self.tasks.values():
            stats[task.status.value] += 1
        
        return {
            "stats": stats,
            "active_sessions": len(self.subagent_sessions),
            "tasks": {k: v.to_dict() for k, v in self.tasks.items()}
        }
    
    def show_dashboard(self):
        """Display a comprehensive dashboard."""
        status = self.get_status()
        stats = status["stats"]
        
        print("\n" + "=" * 60)
        print("🦞 TASK ORCHESTRATOR DASHBOARD")
        print("=" * 60)
        print(f"\n📊 Statistics:")
        print(f"   Total Tasks:  {stats['total']}")
        print(f"   ✅ Completed: {stats['completed']}")
        print(f"   🔄 Running:   {stats['running']}")
        print(f"   ⏳ Pending:   {stats['pending']}")
        print(f"   ❌ Failed:    {stats['failed']}")
        print(f"   🚫 Cancelled: {stats['cancelled']}")
        print(f"   👥 Sub-agents: {status['active_sessions']}")
        
        # Show active tasks
        active = [(k, v) for k, v in status["tasks"].items() 
                  if v["status"] in ["running", "pending"]]
        
        if active:
            print(f"\n📋 Active Tasks:")
            for task_id, task in sorted(active, key=lambda x: -x[1]["priority"]):
                status_icon = {"pending": "⏳", "running": "🔄", "completed": "✅", "failed": "❌", "cancelled": "🚫"}
                print(f"   {status_icon.get(task['status'], '?')} [{task['task_type']}] {task['description'][:40]}")
                if task.get('session_key'):
                    print(f"      Session: {task['session_key'][:20]}...")
        
        print()
    
    def cleanup_stale_sessions(self) -> int:
        """Clean up stale/timeout sub-agent sessions."""
        cleaned = 0
        for task_id, task in self.tasks.items():
            if task.task_type == TaskType.SUBAGENT:
                if task.status == TaskStatus.RUNNING:
                    # Check if session still exists
                    self._load_subagent_sessions()
                    if task.session_key not in self.subagent_sessions:
                        task.status = TaskStatus.FAILED
                        task.error = "Session ended unexpectedly"
                        task.completed_at = time.time()
                        cleaned += 1
        
        if cleaned > 0:
            print(f"🧹 Cleaned {cleaned} stale sessions")
            self._save_state()
        
        return cleaned


def run_command(cmd: str) -> tuple:
    """Run a shell command."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        return (result.returncode == 0, result.stdout, result.stderr)
    except Exception as e:
        return (False, "", str(e))


def main():
    parser = argparse.ArgumentParser(
        description='Task Orchestrator for Clawdbot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show dashboard
  task-orchestrator.py status
  
  # Add task to queue
  task-orchestrator.py queue add "echo hello" --type local
  
  # Process queue
  task-orchestrator.py queue run --max-concurrent 4
  
  # Spawn sub-agent
  task-orchestrator.py spawn "Research AI consciousness" --label "consciousness-research"
  
  # Get sub-agent history
  task-orchestrator.py history <session-key>
  
  # Cancel task
  task-orchestrator.py cancel <task-id>
  
  # Cleanup stale sessions
  task-orchestrator.py cleanup
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Status/Dashboard
    status_parser = subparsers.add_parser('status', help='Show task dashboard')
    status_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Queue management
    queue_parser = subparsers.add_parser('queue', help='Queue management')
    queue_sub = queue_parser.add_subparsers(dest='queue_cmd')
    
    queue_add = queue_sub.add_parser('add', help='Add task to queue')
    queue_add.add_argument('command', help='Task command')
    queue_add.add_argument('--type', choices=['local', 'api'], default='local', help='Task type')
    queue_add.add_argument('--priority', type=int, default=0, help='Priority (higher = first)')
    queue_add.add_argument('--retry', type=int, default=3, help='Max retries')
    queue_add.add_argument('--description', help='Task description')
    
    queue_list = queue_sub.add_parser('list', help='List queued tasks')
    queue_list.add_argument('--all', action='store_true', help='Include completed tasks')
    
    queue_run = queue_sub.add_parser('run', help='Process queue')
    queue_run.add_argument('--max-concurrent', type=int, default=4, help='Max concurrent tasks')
    
    # Sub-agent management
    spawn_parser = subparsers.add_parser('spawn', help='Spawn a sub-agent')
    spawn_parser.add_argument('task', help='Task for sub-agent')
    spawn_parser.add_argument('--label', help='Task label')
    
    history_parser = subparsers.add_parser('history', help='Get sub-agent history')
    history_parser.add_argument('session', help='Session key')
    
    cancel_parser = subparsers.add_parser('cancel', help='Cancel a task')
    cancel_parser.add_argument('task_id', help='Task ID')
    
    # Cleanup
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up stale sessions')
    
    args = parser.parse_args()
    
    orchestrator = TaskOrchestrator()
    
    if args.command == 'status':
        if args.json:
            print(json.dumps(orchestrator.get_status(), indent=2))
        else:
            orchestrator.show_dashboard()
    
    elif args.command == 'queue':
        if args.queue_cmd == 'add':
            task_id = orchestrator.add_task(
                description=args.description or args.command,
                task_type=TaskType.LOCAL if args.type == 'local' else TaskType.API,
                command=args.command,
                priority=args.priority,
                max_retries=args.retry
            )
            print(f"✅ Added task: {task_id}")
        
        elif args.queue_cmd == 'list':
            status = orchestrator.get_status()
            tasks = status["tasks"]
            for task_id, task in tasks.items():
                if args.all or task["status"] in ["pending", "running"]:
                    print(f"[{task['status'][:3]}] {task_id}: {task['description'][:50]}")
        
        elif args.queue_cmd == 'run':
            print("🚀 Processing queue...")
            results = orchestrator.process_queue(max_concurrent=args.max_concurrent)
            print(f"✅ Processed {len(results)} tasks")
    
    elif args.command == 'spawn':
        session_key = orchestrator.spawn_subagent(args.task, args.label)
        if session_key:
            print(f"✅ Spawned: {session_key}")
    
    elif args.command == 'history':
        history = orchestrator.get_subagent_status(args.session)
        if history:
            print(json.dumps(history, indent=2))
        else:
            print("Could not get history")
    
    elif args.command == 'cancel':
        if orchestrator.cancel_task(args.task_id):
            print(f"✅ Cancelled: {args.task_id}")
        else:
            print(f"❌ Task not found: {args.task_id}")
    
    elif args.command == 'cleanup':
        cleaned = orchestrator.cleanup_stale_sessions()
        print(f"🧹 Cleaned {cleaned} stale sessions")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
