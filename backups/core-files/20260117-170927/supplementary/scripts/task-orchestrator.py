#!/usr/bin/env python3
"""
Task Orchestrator for Clawdbot

Simple, reliable task management for sub-agents and task queues.

Usage:
    python task-orchestrator.py status              # Show all tasks
    python task-orchestrator.py spawn <task>        # Spawn sub-agent
    python task-orchestrator.py queue add <task>    # Add to queue
    python task-orchestrator.py queue list          # Show queue
    python task-orchestrator.py queue run           # Process queue
    python task-orchestrator.py history <session>   # Get session history
    python task-orchestrator.py cleanup             # Clean up stale

Features:
- Simple JSON-based persistence
- Sub-agent status tracking
- Task queue with concurrency control
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Paths
BASE_DIR = Path.home() / ".clawdbot" / "shared"
TASKS_DIR = BASE_DIR / "tasks"
RESULTS_DIR = BASE_DIR / "results"
QUEUE_FILE = BASE_DIR / "queue.json"

# Ensure directories exist
BASE_DIR.mkdir(parents=True, exist_ok=True)
TASKS_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)


def get_timestamp():
    return datetime.utcnow().isoformat() + "Z"


def status():
    """Show dashboard of current tasks."""
    print("📊 Task Dashboard")
    print("=" * 50)
    
    # Check queue
    queue = []
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE) as f:
            queue = json.load(f)
    print(f"📥 Queue: {len(queue)} pending tasks")
    
    # Check running tasks (from results)
    running = list(RESULTS_DIR.glob("running-*.json"))
    print(f"⚡ Running: {len(running)} tasks")
    
    # Check completed
    completed = list(RESULTS_DIR.glob("complete-*.json"))
    print(f"✅ Completed: {len(completed)} tasks")
    
    # Show recent
    print("\n🕐 Recent Results:")
    for f in sorted(RESULTS_DIR.glob("*.json"), reverse=True)[:5]:
        name = f.name
        status_ico = "✅" if "complete" in name else "⚡" if "running" in name else "❌"
        print(f"  {status_ico} {name}")
    
    return {"queue": len(queue), "running": len(running), "completed": len(completed)}


def spawn(task: str, label: str = None, agent: str = "worker"):
    """Spawn a sub-agent for a task."""
    task_id = label or f"task-{int(time.time())}"
    timestamp = get_timestamp()
    
    # Write task definition
    task_file = TASKS_DIR / f"{task_id}.json"
    task_data = {
        "id": task_id,
        "task": task,
        "agent": agent,
        "created": timestamp,
        "status": "pending"
    }
    with open(task_file, 'w') as f:
        json.dump(task_data, f, indent=2)
    
    # Write running marker
    running_file = RESULTS_DIR / f"running-{task_id}.json"
    with open(running_file, 'w') as f:
        json.dump({
            "id": task_id,
            "task": task,
            "agent": agent,
            "started": timestamp,
            "status": "running"
        }, f, indent=2)
    
    print(f"📝 Task created: {task_id}")
    print(f"   Agent: {agent}")
    print(f"   Task: {task[:60]}...")
    
    return task_id


def queue_add(task: str, priority: int = 0):
    """Add task to persistent queue."""
    queue = []
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE) as f:
            queue = json.load(f)
    
    entry = {
        "id": f"q-{int(time.time())}",
        "task": task,
        "priority": priority,
        "added": get_timestamp(),
        "status": "pending"
    }
    queue.append(entry)
    
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)
    
    print(f"📥 Added to queue: {entry['id']}")


def queue_list():
    """List pending queue tasks."""
    if not QUEUE_FILE.exists():
        print("📭 Queue is empty")
        return
    
    with open(QUEUE_FILE) as f:
        queue = json.load(f)
    
    pending = [q for q in queue if q["status"] == "pending"]
    
    print(f"📥 Queue ({len(pending)} pending)")
    print("-" * 50)
    
    for q in sorted(pending, key=lambda x: -x.get("priority", 0)):
        print(f"  [{q.get('priority', 0)}] {q['id']}: {q['task'][:50]}...")
    
    return pending


def queue_run(max_concurrent: int = 3):
    """Process queue with concurrency limit."""
    if not QUEUE_FILE.exists():
        print("📭 Queue is empty")
        return
    
    with open(QUEUE_FILE) as f:
        queue = json.load(f)
    
    pending = [q for q in queue if q["status"] == "pending"]
    
    if not pending:
        print("✅ Queue is empty")
        return
    
    print(f"🚀 Processing {len(pending)} tasks (max {max_concurrent} concurrent)")
    
    processed = 0
    for q in pending:
        if q["status"] == "pending":
            print(f"\n📋 Processing: {q['id']}")
            spawn(q["task"], label=q["id"], agent="worker")
            q["status"] = "running"
            processed += 1
            
            if processed >= max_concurrent:
                print(f"\n⚠️  Reached concurrency limit ({max_concurrent})")
                break
    
    # Update queue file
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)
    
    print(f"\n✅ Started {processed} tasks")
    print("   Use 'status' to monitor progress")


def complete(task_id: str, result: str = None, error: str = None):
    """Mark task as complete."""
    running_file = RESULTS_DIR / f"running-{task_id}.json"
    
    if not running_file.exists():
        print(f"❌ Task not found: {task_id}")
        return False
    
    # Read running data
    with open(running_file) as f:
        data = json.load(f)
    
    # Move to complete or error
    status_ = "complete" if not error else "error"
    data["status"] = status_
    data["finished"] = get_timestamp()
    if result:
        data["result"] = result
    if error:
        data["error"] = error
    
    complete_file = RESULTS_DIR / f"{status_}-{task_id}.json"
    with open(complete_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Remove running marker
    running_file.unlink()
    
    print(f"{'✅' if status_ == 'complete' else '❌'} Task {task_id}: {status_}")
    return True


def history(session_key: str):
    """Get session history (placeholder for sessions_history)."""
    print(f"📜 History for: {session_key}")
    print("   Use sessions_history tool for full transcript")
    print("   This is a simplified placeholder")
    return {"session": session_key, "note": "Use sessions_history tool"}


def cleanup():
    """Clean up stale tasks (>1 hour old)."""
    stale = []
    cutoff = time.time() - 3600
    
    for f in RESULTS_DIR.glob("running-*.json"):
        if f.stat().st_mtime < cutoff:
            stale.append(f)
    
    for f in stale:
        name = f.name
        f.rename(RESULTS_DIR / f"stale-{name}")
        print(f"🧹 Marked stale: {name}")
    
    if not stale:
        print("🧹 No stale tasks found")
    
    return len(stale)


def main():
    parser = argparse.ArgumentParser(
        description="Task orchestrator for Clawdbot sub-agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  task-orchestrator.py status                    # Show dashboard
  task-orchestrator.py spawn "Research topic"    # Create task
  task-orchestrator.py queue add "Task name"     # Add to queue
  task-orchestrator.py queue list                # Show queue
  task-orchestrator.py queue run                 # Process queue
  task-orchestrator.py cleanup                   # Clean stale
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Status
    subparsers.add_parser('status', help='Show task dashboard')
    
    # Spawn
    spawn_parser = subparsers.add_parser('spawn', help='Spawn sub-agent task')
    spawn_parser.add_argument('task', help='Task description')
    spawn_parser.add_argument('--label', help='Task label/ID')
    spawn_parser.add_argument('--agent', default='worker', help='Agent type')
    
    # Queue
    queue_parser = subparsers.add_parser('queue', help='Task queue operations')
    queue_sub = queue_parser.add_subparsers(dest='queue_cmd', help='Queue commands')
    
    queue_add_parser = queue_sub.add_parser('add', help='Add to queue')
    queue_add_parser.add_argument('task', help='Task description')
    queue_add_parser.add_argument('--priority', type=int, default=0, help='Priority')
    
    queue_sub.add_parser('list', help='List pending tasks')
    queue_sub.add_parser('run', help='Process queue')
    queue_run_parser = queue_sub.add_parser('run', help='Process queue')
    queue_run_parser.add_argument('--max', type=int, default=3, help='Max concurrent')
    
    # History
    history_parser = subparsers.add_parser('history', help='Get session history')
    history_parser.add_argument('session', help='Session key')
    
    # Complete
    complete_parser = subparsers.add_parser('complete', help='Mark task complete')
    complete_parser.add_argument('task_id', help='Task ID')
    complete_parser.add_argument('--result', help='Result')
    complete_parser.add_argument('--error', help='Error message')
    
    # Cleanup
    subparsers.add_parser('cleanup', help='Clean up stale tasks')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'status':
            status()
        
        elif args.command == 'spawn':
            spawn(args.task, label=args.label, agent=args.agent)
        
        elif args.command == 'queue':
            if args.queue_cmd == 'add':
                queue_add(args.task, args.priority)
            elif args.queue_cmd == 'list':
                queue_list()
            elif args.queue_cmd == 'run':
                queue_run(args.max if hasattr(args, 'max') else 3)
            else:
                queue_parser.print_help()
        
        elif args.command == 'history':
            history(args.session)
        
        elif args.command == 'complete':
            complete(args.task_id, args.result, args.error)
        
        elif args.command == 'cleanup':
            cleaned = cleanup()
            print(f"🧹 Cleaned {cleaned} stale tasks")
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
