#!/usr/bin/env python3
"""
Task Orchestrator CLI Wrapper

Simplified interface to the Task Orchestrator.

Usage:
    to status              # Show dashboard
    to add "<task>"        # Add task
    to list                # List tasks
    to run                 # Process queue
    to spawn "<task>"      # Spawn sub-agent
    to history <session>   # Get session history
    to cancel <task_id>    # Cancel task
    to cleanup             # Clean stale sessions
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib.util
spec = importlib.util.spec_from_file_location("task_orchestrator", os.path.join(os.path.dirname(__file__), "task-orchestrator.py"))
task_orchestrator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(task_orchestrator)
TaskOrchestrator = task_orchestrator.TaskOrchestrator
TaskType = task_orchestrator.TaskType
run_command = task_orchestrator.run_command

def main():
    if len(sys.argv) < 2:
        os.system('python ' + os.path.abspath(__file__).replace('-orchestrator', '') + ' status')
        return
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    orchestrator = TaskOrchestrator()
    
    if cmd == 'status':
        orchestrator.show_dashboard()
    
    elif cmd == 'add':
        if not args:
            print("Usage: to add \"<command>\" [--priority N] [--retry N] [--desc \"<description>\"]")
            return
        task_cmd = args[0]
        priority = 0
        retries = 3
        description = None
        
        i = 1
        while i < len(args):
            if args[i] == '--priority' and i + 1 < len(args):
                priority = int(args[i+1])
                i += 2
            elif args[i] == '--retry' and i + 1 < len(args):
                retries = int(args[i+1])
                i += 2
            elif args[i] == '--desc' and i + 1 < len(args):
                description = args[i+1]
                i += 2
            else:
                i += 1
        
        task_id = orchestrator.add_task(
            description=description or task_cmd[:50],
            task_type=TaskType.LOCAL,
            command=task_cmd,
            priority=priority,
            max_retries=retries
        )
        print(f"✅ Added: {task_id}")
    
    elif cmd == 'list':
        status = orchestrator.get_status()
        for task_id, task in status["tasks"].items():
            print(f"[{task['status'][:3]}] {task_id}: {task['description'][:50]}")
    
    elif cmd == 'run':
        print("🚀 Processing queue...")
        results = orchestrator.process_queue(max_concurrent=4)
        print(f"✅ Processed {len(results)} tasks")
        orchestrator.show_dashboard()
    
    elif cmd == 'spawn':
        if not args:
            print("Usage: to spawn \"<task>\" [--label \"<name>\"]")
            return
        task = args[0]
        label = args[2] if len(args) > 2 and args[1] == '--label' else None
        session_key = orchestrator.spawn_subagent(task, label)
        if session_key:
            print(f"✅ Spawned: {session_key}")
    
    elif cmd == 'history':
        if not args:
            print("Usage: to history <session-key>")
            return
        history = orchestrator.get_subagent_status(args[0])
        if history:
            import json
            print(json.dumps(history, indent=2))
    
    elif cmd == 'cancel':
        if not args:
            print("Usage: to cancel <task-id>")
            return
        if orchestrator.cancel_task(args[0]):
            print(f"✅ Cancelled: {args[0]}")
        else:
            print(f"❌ Not found: {args[0]}")
    
    elif cmd == 'cleanup':
        cleaned = orchestrator.cleanup_stale_sessions()
        print(f"🧹 Cleaned {cleaned} stale sessions")
    
    elif cmd in ['-h', '--help', 'help']:
        print(__doc__)
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == '__main__':
    main()
