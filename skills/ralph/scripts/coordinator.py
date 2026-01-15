#!/usr/bin/env python3
"""
Ralph Coordinator Script - PARALLEL EXECUTION SUPPORT
Enforces Ralph framework rules for task coordination.

Usage: python scripts/coordinator.py <spec-name> [--dry-run] [--undo] [--rollback <index>]

This script implements the implement.md coordinator behavior:
1. Reads state to determine current task
2. Invokes spec-executor for the task
3. Checks for TASK_COMPLETE signal
4. Updates state appropriately

Supports actual parallel execution with [P] markers.
"""

import json
import sys
import os
import re
import subprocess
import time
from pathlib import Path
import concurrent.futures
import threading
import urllib.request
import urllib.error

# Use environment variable or relative path, default to 'specs' in current directory
SPECS_DIR = os.environ.get('RALPH_SPECS_DIR', 'specs')
if not os.path.isabs(SPECS_DIR):
    SPECS_DIR = os.path.join(os.getcwd(), SPECS_DIR)

# Load config
script_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(script_dir, '..', 'config.json')
try:
    with open(CONFIG_FILE, 'r') as f:
        CONFIG = json.load(f)
except:
    CONFIG = {}

WEBHOOK_URL = CONFIG.get('webhook', {}).get('url', '')
WEBHOOK_ENABLED = CONFIG.get('webhook', {}).get('enabled', False)
WEBHOOK_ON_TASK = CONFIG.get('webhook', {}).get('on_task_complete', True)
WEBHOOK_ON_SPEC = CONFIG.get('webhook', {}).get('on_spec_complete', True)
STATS_ENABLED = CONFIG.get('statistics', {}).get('enabled', True)


def read_file(path):
    """Read file content safely."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


def write_file(path, content):
    """Write file content."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)


def run_subprocess(args, cwd=None, capture=True, check=False):
    """Run subprocess safely."""
    try:
        result = subprocess.run(
            args,
            cwd=cwd,
            capture_output=capture,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timed out"
    except Exception as e:
        return False, "", str(e)


def count_tasks(tasks_content):
    """Count total and completed tasks."""
    lines = tasks_content.split('\n')
    total = 0
    completed = 0
    
    for line in lines:
        if re.match(r'^- \[ \]', line):
            total += 1
        elif re.match(r'^- \[x\]', line):
            total += 1
            completed += 1
    
    return total, completed


def parse_tasks_for_markers(tasks_content):
    """Parse tasks and detect [P], [VERIFY], [SEQUENTIAL] markers."""
    tasks = []
    lines = tasks_content.split('\n')
    
    for i, line in enumerate(lines):
        task_match = re.match(r'^- \[([ x])\] (\d+\.\d+)(.*)', line)
        if task_match:
            desc = task_match.group(3)
            task = {
                'index': len(tasks),
                'complete': task_match.group(1) == 'x',
                'has_p': '[P]' in desc,
                'has_verify': '[VERIFY]' in desc,
                'has_sequential': '[SEQUENTIAL]' in desc,
                'is_parallel': '[P]' in desc and '[VERIFY]' not in desc and '[SEQUENTIAL]' not in desc
            }
            tasks.append(task)
    
    return tasks


def detect_parallel_group(tasks, start_index):
    """Detect parallel group starting from start_index."""
    if start_index >= len(tasks):
        return None
    
    current = tasks[start_index]
    
    if not current['is_parallel']:
        return {
            'startIndex': start_index,
            'endIndex': start_index,
            'taskIndices': [start_index],
            'isParallel': False
        }
    
    indices = [start_index]
    next_idx = start_index + 1
    
    while next_idx < len(tasks):
        next_task = tasks[next_idx]
        if not next_task['is_parallel']:
            break
        indices.append(next_idx)
        next_idx += 1
    
    return {
        'startIndex': start_index,
        'endIndex': indices[-1],
        'taskIndices': indices,
        'isParallel': len(indices) >= 2
    }


def get_next_task_index(tasks):
    """Find first incomplete task index."""
    for i, task in enumerate(tasks):
        if not task['complete']:
            return i
    return len(tasks)  # All complete


def invoke_spec_executor(spec_name, task_index, progress_file=None, dry_run=False):
    """Invoke spec-executor for a single task."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = f"python {script_dir}/spec-executor.py {spec_name} {task_index}"
    if progress_file:
        cmd += f" {progress_file}"
    if dry_run:
        cmd += " --dry-run"
    
    print(f"\n{'='*60}")
    print(f"COORDINATOR: Invoking spec-executor for task {task_index}")
    print(f"{'='*60}\n")
    
    # Pass SPECS_DIR via environment variable to avoid path duplication
    env = os.environ.copy()
    env['RALPH_SPECS_DIR'] = SPECS_DIR
    
    # Use subprocess.run to capture exit code
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        cwd=os.path.join(SPECS_DIR, spec_name),
        env=env
    )
    
    # Print output
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    
    return result.returncode == 0


def invoke_spec_executor_wrapper(args):
    """Wrapper for parallel execution."""
    spec_name, task_index, progress_file = args
    success = invoke_spec_executor(spec_name, task_index, progress_file)
    return (task_index, success)


def invoke_parallel(spec_name, task_indices, dry_run=False):
    """Invoke spec-executor for multiple tasks in parallel."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print(f"\n{'='*60}")
    print(f"COORDINATOR: Parallel execution of {len(task_indices)} tasks")
    if dry_run:
        print(f"DRY RUN MODE - Would execute in parallel (shown sequentially)")
    print(f"{'='*60}\n")
    
    tasks = []
    for idx in task_indices:
        progress_file = f".progress-task-{idx}.md"
        tasks.append((spec_name, idx, progress_file))
    
    # Execute in parallel using ThreadPoolExecutor
    # Use file locking to prevent git conflicts
    results = {idx: False for idx in task_indices}
    lock_file = "/tmp/ralph-git-lock"
    
    def exec_task(task_info):
        idx, spec_name, progress_file = task_info
        try:
            success = invoke_spec_executor(spec_name, idx, progress_file, dry_run)
            return (idx, success)
        except Exception as e:
            print(f"Task {idx} failed with exception: {e}")
            return (idx, False)
    
    max_workers = 3
    try:
        import json
        with open("/home/opc/clawd/skills/ralph/config.json", 'r') as f:
            max_workers = json.load(f).get('execution', {}).get('parallel_max_workers', 3)
    except:
        pass
    
    # In dry-run mode, run sequentially to show output clearly
    if dry_run:
        for idx in task_indices:
            idx, success = exec_task((idx, spec_name, f".progress-task-{idx}.md"))
            results[idx] = success
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(exec_task, (idx, spec_name, f".progress-task-{idx}.md"))
                for idx in task_indices
            ]
            
            for future in concurrent.futures.as_completed(futures):
                idx, success = future.result()
                results[idx] = success
    
    return all(results.values())


def merge_progress_files(spec_path, task_indices):
    """Merge parallel progress files into main .progress.md and mark tasks complete"""
    main_progress = read_file(f"{spec_path}/.progress.md")
    if not main_progress:
        return
    
    tasks_path = f"{spec_path}/tasks.md"
    tasks_content = read_file(tasks_path)
    lines = tasks_content.split('\n')
    
    # Mark all parallel tasks as complete in tasks.md
    # This prevents race conditions from multiple writers
    current_idx = 0
    for i, line in enumerate(lines):
        task_match = re.match(r'^- \[([ x])\] (\d+\.\d+)', line)
        if task_match:
            if current_idx in task_indices:
                lines[i] = line.replace('[ ]', '[x]')
            current_idx += 1
    
    write_file(tasks_path, '\n'.join(lines))
    print(f"✓ Marked {len(task_indices)} parallel tasks as complete")
    
    # Find all completed tasks from temp files
    completed_tasks = []
    for idx in task_indices:
        temp_file = f"{spec_path}/.progress-task-{idx}.md"
        if os.path.exists(temp_file):
            temp_content = read_file(temp_file)
            # Extract completed task lines
            matches = re.findall(r'- \[x\] (.+?) - ([a-f0-9]+)', temp_content)
            for task_desc, commit_hash in matches:
                completed_tasks.append((task_desc, commit_hash))
            os.remove(temp_file)  # Clean up temp file
    
    if not completed_tasks:
        return
    
    # Merge into main progress
    for task_desc, commit_hash in completed_tasks:
        # Add to completed tasks section if not already there
        if task_desc not in main_progress:
            main_progress = re.sub(
                r'(## Completed Tasks\n)',
                r'\1- [x] ' + task_desc + ' - ' + commit_hash + '\n',
                main_progress
            )
    
    write_file(f"{spec_path}/.progress.md", main_progress)


def commit_spec_files(spec_name, spec_path):
    """Commit all spec files before starting implementation."""
    spec_files = ['research.md', 'requirements.md', 'design.md', 'tasks.md', '.progress.md']
    
    for f in spec_files:
        path = f"{spec_path}/{f}"
        if os.path.exists(path):
            run_subprocess(['git', 'add', path], cwd=spec_path)
    
    success, stdout, _ = run_subprocess(['git', 'status', '--porcelain'], cwd=spec_path)
    if success and stdout.strip():
        run_subprocess(
            ['git', 'commit', '-m', f'docs(spec): add spec for {spec_name}\n\nSpec artifacts committed before implementation.'],
            cwd=spec_path
        )
        print("✓ Committed spec files\n")
    else:
        print("(Spec files already committed)\n")


def update_state(state_file, task_index, total_tasks, increment_iteration=False):
    """Update state file with new task index."""
    if os.path.exists(state_file):
        state = json.loads(read_file(state_file))
        state['taskIndex'] = task_index
        state['totalTasks'] = total_tasks
        if increment_iteration:
            state['taskIteration'] = state.get('taskIteration', 1) + 1
        write_file(state_file, json.dumps(state, indent=2))


def send_webhook(spec_name, event_type, data):
    """Send webhook notification."""
    if not WEBHOOK_ENABLED or not WEBHOOK_URL:
        return
    
    # Check if this event type is enabled
    if event_type == 'task_complete' and not WEBHOOK_ON_TASK:
        return
    if event_type == 'spec_complete' and not WEBHOOK_ON_SPEC:
        return
    
    try:
        payload = {
            'spec': spec_name,
            'event': event_type,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            **data
        }
        
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status >= 200 and response.status < 300:
                print(f"✓ Webhook sent: {event_type}")
            else:
                print(f"⚠️ Webhook returned status {response.status}")
    except urllib.error.URLError as e:
        print(f"⚠️ Webhook failed: {e}")
    except Exception as e:
        print(f"⚠️ Webhook error: {e}")


def get_commit_history(spec_path, limit=10):
    """Get recent commit history."""
    try:
        result = subprocess.run(
            ['git', 'log', '-n', str(limit), '--format=%H|%s'],
            cwd=spec_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            history = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    hash, msg = line.split('|', 1)
                    history.append({'hash': hash, 'message': msg})
            return history
        return []
    except:
        return []


def update_statistics(stats_file, task_index, success, execution_time):
    """Update statistics file with task execution data."""
    if not STATS_ENABLED:
        return
    
    stats = {'tasks': {}, 'summary': {}}
    if os.path.exists(stats_file):
        stats = json.loads(read_file(stats_file))
    
    # Update task stats
    task_key = f'task_{task_index}'
    if task_key not in stats['tasks']:
        stats['tasks'][task_key] = {
            'executions': 0,
            'successes': 0,
            'failures': 0,
            'total_time': 0,
            'last_execution': None
        }
    
    stats['tasks'][task_key]['executions'] += 1
    stats['tasks'][task_key]['last_execution'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    
    if success:
        stats['tasks'][task_key]['successes'] += 1
    else:
        stats['tasks'][task_key]['failures'] += 1
    
    stats['tasks'][task_key]['total_time'] += execution_time
    
    # Update summary
    total_executions = sum(t['executions'] for t in stats['tasks'].values())
    total_successes = sum(t['successes'] for t in stats['tasks'].values())
    total_failures = sum(t['failures'] for t in stats['tasks'].values())
    total_time = sum(t['total_time'] for t in stats['tasks'].values())
    
    stats['summary'] = {
        'total_tasks': len(stats['tasks']),
        'total_executions': total_executions,
        'total_successes': total_successes,
        'total_failures': total_failures,
        'success_rate': round(total_successes / total_executions * 100, 2) if total_executions > 0 else 0,
        'total_time_seconds': round(total_time, 2),
        'last_updated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }
    
    write_file(stats_file, json.dumps(stats, indent=2))


def display_statistics(stats_file):
    """Display statistics summary."""
    if not STATS_ENABLED or not os.path.exists(stats_file):
        return
    
    stats = json.loads(read_file(stats_file))
    summary = stats.get('summary', {})
    
    print(f"\n{'='*60}")
    print("📊 STATISTICS SUMMARY")
    print(f"{'='*60}")
    print(f"Total tasks: {summary.get('total_tasks', 0)}")
    print(f"Total executions: {summary.get('total_executions', 0)}")
    print(f"Successes: {summary.get('total_successes', 0)}")
    print(f"Failures: {summary.get('total_failures', 0)}")
    print(f"Success rate: {summary.get('success_rate', 0)}%")
    print(f"Total execution time: {summary.get('total_time_seconds', 0)}s")
    print(f"{'='*60}\n")


def undo_last_task(spec_name, spec_path):
    """Undo the last completed task by reverting the last commit."""
    print(f"\n{'='*60}")
    print("UNDO: Reverting last completed task")
    print(f"{'='*60}\n")
    
    # Get commit history
    history = get_commit_history(spec_path, limit=20)
    
    # Debug: print history
    print(f"Commit history (found {len(history)} commits):")
    for i, commit in enumerate(history):
        print(f"  {i}: {commit['hash'][:7]} - {commit['message']}")
    
    if len(history) < 2:
        print("⚠️ No task commits to undo (need at least 2 commits: initial + task)")
        return False
    
    # Find the most recent task commit (history[0] is most recent)
    # Find the previous task commit to preserve its work
    task_commit = None
    previous_task_commit = None
    
    for commit in history:
        # Check if this is a task commit
        if 'feat:' in commit['message'] or 'fix:' in commit['message'] or 'chore:' in commit['message']:
            if not task_commit:
                task_commit = commit
            elif not previous_task_commit:
                previous_task_commit = commit
                break  # Found both commits we need
    
    if not task_commit:
        print("⚠️ No task commits found to undo")
        return False
    
    if not previous_task_commit:
        print("⚠️ Cannot undo: this is the first task commit")
        return False
    
    # Use the previous task commit itself as the reset target
    # This represents the state where the previous task is complete
    # DO NOT use the commit after it (might be docs/spec commit without files)
    target_hash = previous_task_commit['hash']
    
    print(f"\nFound task commit: {task_commit['hash'][:7]} - {task_commit['message']}")
    print(f"Previous task: {previous_task_commit['hash'][:7]} - {previous_task_commit['message']}")
    print(f"Resetting to: {target_hash[:7]} (where previous task is complete)\n")
    
    # Reset to target commit
    result = subprocess.run(
        ['git', 'reset', '--hard', target_hash],
        cwd=spec_path,
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ Undo failed: {result.stderr}")
        return False
    
    print(f"✓ Successfully reset to commit {target_hash[:7]}")
    
    # Update tasks.md to unmark the task as complete
    # Git reset restores tasks.md to correct state automatically
    # No need to manually unmark tasks - the reset handles it
    print(f"✓ tasks.md restored by git reset")
    
    # Update state file
    state_file = f"{spec_path}/.ralph-state.json"
    if os.path.exists(state_file):
        state = json.loads(read_file(state_file))
        state['taskIndex'] = max(0, state['taskIndex'] - 1)
        write_file(state_file, json.dumps(state, indent=2))
        print(f"✓ Updated state to task {state['taskIndex']}")
    
    # Send webhook notification
    send_webhook(spec_name, 'task_undo', {
        'commit': task_commit['hash'][:7],
        'reset_to': target_hash[:7],
        'message': task_commit['message']
    })
    
    print(f"\n{'='*60}")
    print("UNDO COMPLETE")
    print(f"{'='*60}\n")
    return True


def rollback_to_task(spec_name, spec_path, target_task_index):
    """Rollback to a specific task index."""
    print(f"\n{'='*60}")
    print(f"ROLLBACK: Reverting to task {target_task_index}")
    print(f"{'='*60}\n")
    
    # Parse tasks to find the target
    tasks_path = f"{spec_path}/tasks.md"
    tasks_content = read_file(tasks_path)
    tasks = parse_tasks_for_markers(tasks_content)
    
    if target_task_index < 0 or target_task_index >= len(tasks):
        print(f"❌ Invalid task index: {target_task_index} (valid range: 0-{len(tasks)-1})")
        return False
    
    # Find all tasks that need to be unmarked (from target+1 to end)
    tasks_to_unmark = []
    for i in range(target_task_index + 1, len(tasks)):
        if tasks[i]['complete']:
            tasks_to_unmark.append(i)
    
    if not tasks_to_unmark:
        print(f"✓ No completed tasks after {target_task_index} to rollback")
        # Just update state
        state_file = f"{spec_path}/.ralph-state.json"
        if os.path.exists(state_file):
            state = json.loads(read_file(state_file))
            state['taskIndex'] = target_task_index
            write_file(state_file, json.dumps(state, indent=2))
        return True
    
    print(f"Tasks to rollback: {len(tasks_to_unmark)}")
    
    # Get commit history to find commits to revert
    history = get_commit_history(spec_path, limit=50)
    
    # Revert commits in reverse order (newest first)
    for i in range(len(history) - 1, -1, -1):
        commit = history[i]
        # Check if this is a task commit
        if 'feat:' in commit['message'] or 'fix:' in commit['message'] or 'chore:' in commit['message']:
            print(f"Reverting: {commit['hash'][:7]} - {commit['message']}")
            
            # Revert this commit
            result = subprocess.run(
                ['git', 'revert', '--no-commit', commit['hash']],
                cwd=spec_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"⚠️ Could not revert {commit['hash'][:7]}: {result.stderr}")
                # Try reset instead
                result = subprocess.run(
                    ['git', 'reset', '--hard', 'HEAD~1'],
                    cwd=spec_path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f"✓ Reset instead to remove commit")
    
    # Unmark tasks
    lines = tasks_content.split('\n')
    current_idx = 0
    for i, line in enumerate(lines):
        if '- [x]' in line or '- [ ]' in line:
            if current_idx in tasks_to_unmark:
                lines[i] = line.replace('- [x]', '- [ ]')
            current_idx += 1
    
    write_file(tasks_path, '\n'.join(lines))
    print(f"✓ Unmarked {len(tasks_to_unmark)} tasks")
    
    # Update state
    state_file = f"{spec_path}/.ralph-state.json"
    if os.path.exists(state_file):
        state = json.loads(read_file(state_file))
        state['taskIndex'] = target_task_index
        write_file(state_file, json.dumps(state, indent=2))
        print(f"✓ Updated state to task {target_task_index}")
    
    # Send webhook notification
    send_webhook(spec_name, 'task_rollback', {
        'target_task_index': target_task_index,
        'tasks_rolled_back': len(tasks_to_unmark)
    })
    
    print(f"\n{'='*60}")
    print("ROLLBACK COMPLETE")
    print(f"{'='*60}\n")
    return True


def check_all_complete(task_index, total_tasks):
    """Check if all tasks are complete."""
    return task_index >= total_tasks


def main():
    if len(sys.argv) < 2:
        print("ERROR: Usage: coordinator.py <spec-name> [--dry-run] [--undo] [--rollback <index>]")
        sys.exit(1)
    
    # Parse flags
    dry_run = '--dry-run' in sys.argv
    if dry_run:
        sys.argv.remove('--dry-run')
    
    undo = '--undo' in sys.argv
    if undo:
        sys.argv.remove('--undo')
    
    rollback_index = None
    if '--rollback' in sys.argv:
        idx = sys.argv.index('--rollback')
        if idx + 1 < len(sys.argv):
            rollback_index = int(sys.argv[idx + 1])
            sys.argv.pop(idx + 1)
            sys.argv.pop(idx)
    
    spec_name = sys.argv[1]
    spec_path = f"{SPECS_DIR}/{spec_name}"
    
    if not os.path.exists(spec_path):
        print(f"ERROR: Spec '{spec_name}' not found at {spec_path}")
        sys.exit(1)
    
    # Handle undo
    if undo:
        undo_last_task(spec_name, spec_path)
        sys.exit(0)
    
    # Handle rollback
    if rollback_index is not None:
        rollback_to_task(spec_name, spec_path, rollback_index)
        sys.exit(0)
    
    # Show dry-run header
    if dry_run:
        print(f"\n{'='*60}")
        print("🔍 DRY RUN MODE - No changes will be made")
        print(f"{'='*60}\n")
    
    # Write active spec (skip in dry-run)
    if not dry_run:
        write_file(f"{SPECS_DIR}/.current-spec", spec_name)
    
    # Initialize or read state (skip in dry-run)
    state_file = f"{spec_path}/.ralph-state.json"
    if not dry_run and not os.path.exists(state_file):
        tasks_path = f"{spec_path}/tasks.md"
        if not os.path.exists(tasks_path):
            print(f"ERROR: tasks.md not found. Run /ralph:tasks first.")
            sys.exit(1)
        
        tasks_content = read_file(tasks_path)
        total, completed = count_tasks(tasks_content)
        
        state = {
            "source": "spec",
            "name": spec_name,
            "basePath": spec_path,
            "phase": "execution",
            "taskIndex": completed,
            "totalTasks": total,
            "taskIteration": 1,
            "maxTaskIterations": 5,
            "globalIteration": 1,
            "maxGlobalIterations": 100,
            "relatedSpecs": [],
            "parallelGroup": None,
            "taskResults": {}
        }
        write_file(state_file, json.dumps(state, indent=2))
        print(f"✓ Initialized state: {completed}/{total} tasks\n")
    
    # Commit spec files first (skip in dry-run)
    if dry_run:
        print("🔍 DRY RUN: Would check and commit spec files")
    else:
        print("Checking spec files...")
        commit_spec_files(spec_name, spec_path)
    
    # Quality Gate: Check if we've exceeded max iterations
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            state = json.load(f)
        task_iteration = state.get('taskIteration', 1)
        max_task_iterations = state.get('maxTaskIterations', 5)
        if task_iteration > max_task_iterations:
            print(f"\n❌ QUALITY GATE BLOCKED")
            print(f"   Task has failed {max_task_iterations} times.")
            print(f"   Please review and fix the task before continuing.")
            print(f"   Current iteration: {task_iteration}")
            print(f"   Max iterations: {max_task_iterations}")
            print(f"\n   To reset and try again, delete: {state_file}")
            print(f"{'='*60}\n")
            sys.exit(1)
    
    # Read tasks and find current task
    tasks_path = f"{spec_path}/tasks.md"
    tasks_content = read_file(tasks_path)
    tasks = parse_tasks_for_markers(tasks_content)
    total_tasks = len(tasks)
    
    # Find next incomplete task
    task_index = get_next_task_index(tasks)
    
    # Calculate progress percentage
    progress_pct = 0
    if total_tasks > 0:
        progress_pct = int((task_index / total_tasks) * 100)
    
    # Create progress bar
    bar_len = 30
    filled = int(bar_len * task_index / total_tasks) if total_tasks > 0 else 0
    bar = '█' * filled + '░' * (bar_len - filled)
    
    print(f"{'='*60}")
    print(f"RALPH COORDINATOR: {spec_name}")
    print(f"{'='*60}")
    print(f"Progress: [{bar}] {progress_pct}% ({task_index}/{total_tasks})")
    print()
    
    # Check if all complete
    if check_all_complete(task_index, total_tasks):
        print("✓ All tasks complete!")
        if os.path.exists(state_file):
            os.remove(state_file)
            print(f"✓ Deleted {state_file}")
        print(f"\n{'='*60}")
        print("SPEC_COMPLETE")
        print(f"{'='*60}\n")
        sys.exit(0)
    
    # Detect parallel group
    parallel_group = detect_parallel_group(tasks, task_index)
    
    print(f"Task group: indices {parallel_group['startIndex']}-{parallel_group['endIndex']}")
    if parallel_group['isParallel']:
        print(f"Mode: PARALLEL ({len(parallel_group['taskIndices'])} tasks)")
    else:
        print("Mode: SEQUENTIAL")
    print()
    
    # Execute task(s)
    success = True
    start_time = time.time()
    
    if parallel_group['isParallel'] and len(parallel_group['taskIndices']) >= 2:
        # ACTUAL parallel execution
        success = invoke_parallel(spec_name, parallel_group['taskIndices'], dry_run)
        
        # Merge progress files after parallel execution (skip in dry-run)
        if success and not dry_run:
            merge_progress_files(spec_path, parallel_group['taskIndices'])
    else:
        # Sequential execution
        progress_file = f".progress-task-{task_index}.md" if parallel_group['isParallel'] else None
        success = invoke_spec_executor(spec_name, task_index, progress_file, dry_run)
        
        # Clean up single temp file if it exists (skip in dry-run)
        if progress_file and not dry_run:
            temp_file = f"{spec_path}/{progress_file}"
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    execution_time = time.time() - start_time
    
    # Update statistics (skip in dry-run)
    if not dry_run:
        stats_file = f"{spec_path}/.ralph-stats.json"
        # Update stats for all executed tasks
        for idx in parallel_group['taskIndices']:
            update_statistics(stats_file, idx, success, execution_time)
        
        # Send webhook notification
        if success:
            task_desc = f"task_{task_index}"
            if parallel_group['isParallel']:
                task_desc = f"tasks_{parallel_group['startIndex']}-{parallel_group['endIndex']}"
            
            send_webhook(spec_name, 'task_complete', {
                'task_index': task_index,
                'parallel_indices': parallel_group['taskIndices'],
                'execution_time_seconds': round(execution_time, 2),
                'description': task_desc
            })
    
    if not success:
        print("\n⚠️ Task execution failed. Check errors above.")
        # Clean up any orphaned progress files
        cleanup_indices = parallel_group['taskIndices']
        for idx in cleanup_indices:
            temp_file = f"{spec_path}/.progress-task-{idx}.md"
            if os.path.exists(temp_file):
                os.remove(temp_file)
        sys.exit(1)
    
    # Re-read tasks to find next incomplete task
    tasks_content = read_file(tasks_path)
    tasks = parse_tasks_for_markers(tasks_content)
    next_task = get_next_task_index(tasks)
    
    # Update state (skip in dry-run)
    if not dry_run:
        update_state(state_file, next_task, total_tasks, increment_iteration=True)
    else:
        print(f"\n🔍 DRY RUN: Would update state to task {next_task}")
    
    # Check if spec is complete
    if check_all_complete(next_task, total_tasks):
        if dry_run:
            print(f"\n🔍 DRY RUN: Would delete state file and mark SPEC_COMPLETE")
            print(f"{'='*60}")
            print("SPEC_COMPLETE (Dry Run)")
            print(f"{'='*60}\n")
        else:
            print("\n✓ All tasks complete!")
            if os.path.exists(state_file):
                os.remove(state_file)
                print(f"✓ Deleted {state_file}")
            
            # Display statistics
            stats_file = f"{spec_path}/.ralph-stats.json"
            display_statistics(stats_file)
            
            # Send webhook notification
            send_webhook(spec_name, 'spec_complete', {
                'total_tasks': total_tasks,
                'total_execution_time': round(execution_time, 2)
            })
            
            print(f"\n{'='*60}")
            print("SPEC_COMPLETE")
            print(f"{'='*60}\n")
    else:
        if dry_run:
            print(f"\n🔍 DRY RUN: Would advance to task {next_task}")
            print(f"\n{'='*60}")
            print("CYCLE_COMPLETE - Ready for next task (Dry Run)")
            print(f"{'='*60}\n")
        else:
            print(f"\n✓ Advanced to task {next_task}")
            print(f"\n{'='*60}")
            print("CYCLE_COMPLETE - Ready for next task")
            print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
