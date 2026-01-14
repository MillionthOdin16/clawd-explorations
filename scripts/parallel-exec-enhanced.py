#!/usr/bin/env python3
"""
Enhanced Parallel Execution Utilities for Clawdbot

New Features:
- Auto-scaling workers based on task type
- Retry logic with exponential backoff
- Priority queue support
- Task dependencies
- Rate limiting awareness
- Progress dashboard
- Queue persistence (save/load)
- Result aggregation

Usage:
    python parallel-exec-enhanced.py curl <urls_file>
    python parallel-exec-enhanced.py exec <commands_file> --retry 3 --priority
    python parallel-exec-enhanced.py api <endpoints_file> --rate-limit 10
    python parallel-exec-enhanced.py queue-status
    python parallel-exec-enhanced.py queue-persist <name>
    python parallel-exec-enhanced.py queue-load <name>
"""

import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import time
import urllib.request
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple


class Priority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    """A task in the queue."""
    id: str
    command: str
    priority: Priority = Priority.NORMAL
    retries: int = 0
    max_retries: int = 3
    retry_delay: float = 1.0
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    
    def __hash__(self):
        return hash(self.id)


@dataclass
class QueueState:
    """State of a persistent queue."""
    name: str
    tasks: List[Task] = field(default_factory=list)
    results: Dict[str, Tuple[bool, str, str]] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


class RateLimiter:
    """Rate limiter for API calls."""
    def __init__(self, max_per_second: float = 10):
        self.max_per_second = max_per_second
        self.min_interval = 1.0 / max_per_second if max_per_second > 0 else 0
        self.last_call = 0
    
    def acquire(self):
        """Wait if necessary to respect rate limit."""
        if self.min_interval > 0:
            now = time.time()
            elapsed = now - self.last_call
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_call = time.time()


class EnhancedParallelExec:
    """Enhanced parallel execution with advanced features."""
    
    def __init__(self, auto_scale: bool = True, default_workers: int = 4):
        self.auto_scale = auto_scale
        self.default_workers = default_workers
        self.queues: Dict[str, QueueState] = {}
        self.rate_limiter = None
    
    def get_optimal_workers(self, task_type: str = "exec") -> int:
        """Get optimal worker count based on task type."""
        if not self.auto_scale:
            return self.default_workers
        
        import multiprocessing
        cpu_count = multiprocessing.cpu_count()
        
        if task_type == "cpu":
            return max(1, cpu_count // 2)
        elif task_type in ["api", "curl", "download"]:
            return min(cpu_count * 2, 16)  # I/O bound can use more workers
        else:
            return min(cpu_count, 8)
    
    def run_with_retry(
        self,
        command: str,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        rate_limiter: Optional[RateLimiter] = None
    ) -> Tuple[bool, str, str]:
        """Run a command with retry logic and exponential backoff."""
        if rate_limiter:
            rate_limiter.acquire()
        
        last_error = ""
        for attempt in range(max_retries + 1):
            try:
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True, timeout=120
                )
                return (result.returncode == 0, result.stdout, result.stderr)
            except subprocess.TimeoutExpired:
                last_error = "Timeout"
            except Exception as e:
                last_error = str(e)
            
            if attempt < max_retries:
                delay = retry_delay * (2 ** attempt)  # Exponential backoff
                time.sleep(delay)
        
        return (False, "", last_error)
    
    def run_parallel_with_retry(
        self,
        tasks: List[Task],
        worker: Callable,
        max_workers: int = 4,
        rate_limit: Optional[float] = None,
        quiet: bool = False
    ) -> Dict[str, Tuple[bool, str, str]]:
        """Run tasks in parallel with retry logic."""
        results = {}
        start_time = time.time()
        
        # Sort by priority
        sorted_tasks = sorted(tasks, key=lambda t: t.priority.value, reverse=True)
        
        if not quiet:
            print(f"🚀 Starting {len(sorted_tasks)} tasks with {max_workers} workers...")
            if rate_limit:
                print(f"📊 Rate limit: {rate_limit} calls/second")
        
        rate_limiter = RateLimiter(rate_limit) if rate_limit else None
        
        def task_with_retry(task: Task):
            success, output, error = self.run_with_retry(
                task.command,
                task.max_retries,
                task.retry_delay,
                rate_limiter
            )
            return task.id, (success, output, error)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_task = {executor.submit(task_with_retry, task): task for task in sorted_tasks}
            
            completed = 0
            for future in concurrent.futures.as_completed(future_to_task):
                task_id, result = future.result()
                results[task_id] = result
                
                completed += 1
                if not quiet:
                    progress = (completed / len(sorted_tasks)) * 100
                    status = "✅" if result[0] else "❌"
                    print(f"  [{progress:5.1f}%] {status} {completed}/{len(sorted_tasks)}", end="\r")
        
        elapsed = time.time() - start_time
        
        # Summary
        success_count = sum(1 for s, _, _ in results.values() if s)
        failed_count = len(results) - success_count
        
        if not quiet:
            print()  # New line
            print(f"✅ Completed: {success_count} | ❌ Failed: {failed_count} | ⏱️ {elapsed:.2f}s")
        
        return results
    
    def save_queue(self, name: str, tasks: List[Task], results: Dict = None):
        """Persist a queue to disk."""
        state = QueueState(
            name=name,
            tasks=tasks,
            results=results or {}
        )
        self.queues[name] = state
        
        filename = f"/home/opc/clawd/.queues/{name}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        data = {
            "name": name,
            "tasks": [
                {
                    "id": t.id,
                    "command": t.command,
                    "priority": t.priority.name,
                    "max_retries": t.max_retries,
                    "retry_delay": t.retry_delay,
                    "dependencies": t.dependencies,
                    "metadata": t.metadata
                }
                for t in tasks
            ],
            "results": {k: [v[0], v[1][:1000], v[2][:500]] for k, v in results.items()} if results else {},
            "created_at": state.created_at,
            "updated_at": time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Queue '{name}' saved ({len(tasks)} tasks)")
    
    def load_queue(self, name: str) -> Optional[QueueState]:
        """Load a persisted queue from disk."""
        filename = f"/home/opc/clawd/.queues/{name}.json"
        if not os.path.exists(filename):
            print(f"Error: Queue '{name}' not found", file=sys.stderr)
            return None
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        tasks = []
        for t_data in data.get("tasks", []):
            task = Task(
                id=t_data["id"],
                command=t_data["command"],
                priority=Priority[t_data.get("priority", "NORMAL")],
                max_retries=t_data.get("max_retries", 3),
                retry_delay=t_data.get("retry_delay", 1.0),
                dependencies=t_data.get("dependencies", []),
                metadata=t_data.get("metadata", {})
            )
            tasks.append(task)
        
        results = {}
        for k, v in data.get("results", {}).items():
            results[k] = (v[0], v[1], v[2])
        
        state = QueueState(
            name=name,
            tasks=tasks,
            results=results
        )
        self.queues[name] = state
        
        print(f"📂 Queue '{name}' loaded ({len(tasks)} tasks, {len(results)} results)")
        return state
    
    def list_queues(self):
        """List all persisted queues."""
        queue_dir = "/home/opc/clawd/.queues"
        if not os.path.exists(queue_dir):
            print("No queues saved")
            return
        
        files = [f for f in os.listdir(queue_dir) if f.endswith('.json')]
        if not files:
            print("No queues saved")
            return
        
        print("📋 Saved queues:")
        for f in sorted(files):
            name = f.replace('.json', '')
            filepath = os.path.join(queue_dir, f)
            size = os.path.getsize(filepath)
            modified = time.ctime(os.path.getmtime(filepath))
            print(f"  - {name} ({size} bytes, modified: {modified})")
    
    def get_queue_status(self, name: str = None):
        """Show queue status."""
        if name:
            if name not in self.queues:
                print(f"Queue '{name}' not found")
                return
            states = [self.queues[name]]
        else:
            states = list(self.queues.values())
        
        for state in states:
            completed = len(state.results)
            pending = len(state.tasks) - completed
            print(f"\n📊 Queue: {state.name}")
            print(f"  Tasks: {len(state.tasks)} total | {completed} done | {pending} pending")
            print(f"  Created: {time.ctime(state.created_at)}")
            print(f"  Updated: {time.ctime(state.updated_at)}")
    
    def run_with_dependencies(
        self,
        tasks: List[Task],
        worker: Callable,
        max_workers: int = 4,
        quiet: bool = False
    ) -> Dict[str, Tuple[bool, str, str]]:
        """Run tasks respecting dependencies."""
        # Build dependency graph
        task_map = {t.id: t for t in tasks}
        completed = set()
        results = {}
        
        remaining = set(tasks)
        
        while remaining:
            # Find tasks with all dependencies satisfied
            ready = [t for t in remaining if all(d in completed for d in t.dependencies)]
            
            if not ready and remaining:
                # Circular dependency or missing dependency
                print(f"⚠️ Cannot resolve dependencies for {len(remaining)} tasks", file=sys.stderr)
                # Run what we can
                ready = [t for t in remaining if not t.dependencies]
                if not ready:
                    break
            
            # Sort by priority
            ready.sort(key=lambda t: t.priority.value, reverse=True)
            
            if not quiet:
                print(f"🚀 Running {len(ready)} ready tasks (remaining: {len(remaining) - len(ready)})")
            
            def run_task(task):
                success, output, error = worker(task.command)
                return task.id, (success, output, error)
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_task = {executor.submit(run_task, task): task for task in ready}
                
                for future in concurrent.futures.as_completed(future_to_task):
                    task_id, result = future.result()
                    results[task_id] = result
                    completed.add(task_id)
                    remaining = remaining - {future_to_task[future]}
        
        return results


# CLI Functions
def run_command(cmd: str) -> tuple:
    """Run a shell command."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        return (result.returncode == 0, result.stdout, result.stderr)
    except Exception as e:
        return (False, "", str(e))


def curl_url(url: str) -> tuple:
    """Fetch a URL."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Clawdbot/1.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            return (True, response.read().decode('utf-8'), "")
    except Exception as e:
        return (False, "", str(e))


def main():
    parser = argparse.ArgumentParser(
        description='Enhanced parallel execution utilities for Clawdbot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic parallel exec
  parallel-exec-enhanced.py exec commands.txt
  
  # With retry logic (3 retries, exponential backoff)
  parallel-exec-enhanced.py exec commands.txt --retry 3 --retry-delay 1
  
  # Priority queue (high priority first)
  parallel-exec-enhanced.py exec commands.txt --priority
  
  # Rate limited API calls (10 per second)
  parallel-exec-enhanced.py api endpoints.txt --rate-limit 10
  
  # Save queue for later
  parallel-exec-enhanced.py exec tasks.txt --save my-queue
  
  # Load and continue
  parallel-exec-enhanced.py queue-load my-queue --continue
  
  # List saved queues
  parallel-exec-enhanced.py queue-list
  
  # Show queue status
  parallel-exec-enhanced.py queue-status my-queue
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Shared arguments
    def add_common_args(p):
        p.add_argument('-w', '--workers', type=int, default=0, help='Number of workers (0=auto)')
        p.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
        p.add_argument('--retry', type=int, default=0, help='Max retries on failure')
        p.add_argument('--retry-delay', type=float, default=1.0, help='Initial retry delay (seconds)')
    
    # Exec command
    exec_parser = subparsers.add_parser('exec', help='Parallel command execution')
    exec_parser.add_argument('file', help='File with commands (one per line)')
    add_common_args(exec_parser)
    exec_parser.add_argument('--save', help='Save queue with this name')
    exec_parser.add_argument('--priority', action='store_true', help='Run high priority first')
    
    # API command
    api_parser = subparsers.add_parser('api', help='Parallel API calls')
    api_parser.add_argument('file', help='File with endpoints (one per line)')
    add_common_args(api_parser)
    api_parser.add_argument('--rate-limit', type=float, default=0, help='Max calls per second')
    api_parser.add_argument('--save', help='Save queue with this name')
    
    # Curl command
    curl_parser = subparsers.add_parser('curl', help='Parallel curl requests')
    curl_parser.add_argument('file', help='File with URLs (one per line)')
    add_common_args(curl_parser)
    
    # Queue management
    queue_parser = subparsers.add_parser('queue', help='Queue management')
    queue_sub = queue_parser.add_subparsers(dest='queue_cmd')
    
    list_parser = queue_sub.add_parser('list', help='List saved queues')
    status_parser = queue_sub.add_parser('status', help='Show queue status')
    status_parser.add_argument('name', help='Queue name (or all)')
    load_parser = queue_sub.add_parser('load', help='Load a saved queue')
    load_parser.add_argument('name', help='Queue name')
    load_parser.add_argument('--continue', action='store_true', help='Continue from saved results')
    
    args = parser.parse_args()
    
    executor = EnhancedParallelExec()
    
    if args.command == 'queue':
        if args.queue_cmd == 'list':
            executor.list_queues()
        elif args.queue_cmd == 'status':
            executor.get_queue_status(args.name)
        elif args.queue_cmd == 'load':
            state = executor.load_queue(args.name)
            if state and getattr(args, 'continue', False):
                # Continue from saved results
                remaining = [t for t in state.tasks if t.id not in state.results]
                if remaining:
                    print(f"Continuing with {len(remaining)} pending tasks...")
                    results = executor.run_parallel_with_retry(
                        remaining, run_command,
                        args.workers or executor.get_optimal_workers(),
                        quiet=args.quiet
                    )
                    state.results.update(results)
                    executor.save_queue(args.name, state.tasks, state.results)
        else:
            queue_parser.print_help()
        return
    
    if not args.command:
        parser.print_help()
        return
    
    # Read commands from file
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    with open(args.file, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not lines:
        print("Error: No commands found in file", file=sys.stderr)
        sys.exit(1)
    
    # Create tasks
    tasks = []
    for i, cmd in enumerate(lines):
        task = Task(
            id=f"task_{i}",
            command=cmd,
            priority=Priority.HIGH if args.priority else Priority.NORMAL,
            max_retries=args.retry,
            retry_delay=args.retry_delay
        )
        tasks.append(task)
    
    # Run
    workers = args.workers or executor.get_optimal_workers(args.command)
    rate_limit = getattr(args, 'rate_limit', 0) or None
    
    results = executor.run_parallel_with_retry(
        tasks, run_command, workers, rate_limit, args.quiet
    )
    
    # Save if requested
    if args.save:
        executor.save_queue(args.save, tasks, results)
    
    # Exit with error if any failed
    failed = sum(1 for s, _, _ in results.values() if not s)
    if failed > 0:
        print(f"⚠️ {failed} tasks failed", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
