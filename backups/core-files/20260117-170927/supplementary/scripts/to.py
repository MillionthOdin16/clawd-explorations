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

# Import functions directly (task-orchestrator uses function-based interface)
status_func = task_orchestrator.status
spawn_func = task_orchestrator.spawn
queue_add_func = task_orchestrator.queue_add
queue_list_func = task_orchestrator.queue_list
queue_run_func = task_orchestrator.queue_run
history_func = task_orchestrator.history
cleanup_func = task_orchestrator.cleanup

def main():
    if len(sys.argv) < 2:
        os.system('python ' + os.path.abspath(__file__).replace('-orchestrator', '') + ' status')
        return
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    # No orchestrator instance needed - use functions directly
    
    if cmd == 'status':
        status_func()
    
    elif cmd == 'add':
        if not args:
            print("Usage: to add \"<command>\" [--priority N] [--desc \"<description>\"]")
            return
        task_cmd = args[0]
        priority = 0
        description = None
        
        i = 1
        while i < len(args):
            if args[i] == '--priority' and i + 1 < len(args):
                priority = int(args[i+1])
                i += 2
            elif args[i] == '--desc' and i + 1 < len(args):
                description = args[i+1]
                i += 2
            else:
                i += 1
        
        queue_add_func(task_cmd, priority)
    
    elif cmd == 'list':
        queue_list_func()
    
    elif cmd == 'run':
        print("🚀 Processing queue...")
        queue_run_func(max_concurrent=4)
        status_func()
    
    elif cmd == 'spawn':
        if not args:
            print("Usage: to spawn \"<task>\" [--label \"<name>\"]")
            return
        task = args[0]
        label = None
        agent = "worker"
        
        i = 1
        while i < len(args):
            if args[i] == '--label' and i + 1 < len(args):
                label = args[i+1]
                i += 2
            elif args[i] == '--agent' and i + 1 < len(args):
                agent = args[i+1]
                i += 2
            else:
                i += 1
        
        task_id = spawn_func(task, label=label, agent=agent)
        print(f"✅ Spawned: {task_id}")
    
    elif cmd == 'history':
        if not args:
            print("Usage: to history <session-key>")
            return
        history_func(args[0])
    
    elif cmd == 'cleanup':
        cleaned = cleanup_func()
        print(f"🧹 Cleaned {cleaned} stale tasks")
    
    elif cmd in ['-h', '--help', 'help']:
        print(__doc__)
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == '__main__':
    main()
