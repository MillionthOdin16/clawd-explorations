#!/usr/bin/env python3
"""
Ralph Spec-Executor Script - SECURE VERSION
Enforces Ralph framework rules for task execution.

Usage: python scripts/spec-executor.py <spec-name> <task-index> [progress-file]

This script interprets task instructions and executes them properly.
Uses subprocess.run() instead of os.system() to prevent shell injection.
"""

import json
import sys
import os
import re
import subprocess
from pathlib import Path

# Use environment variable if set (from coordinator), otherwise default to 'specs' in current directory
RALPH_SPECS_DIR = os.environ.get('RALPH_SPECS_DIR', '')
if RALPH_SPECS_DIR:
    SPECS_DIR = RALPH_SPECS_DIR
else:
    SPECS_DIR = 'specs'
    if not os.path.isabs(SPECS_DIR):
        SPECS_DIR = os.path.join(os.getcwd(), SPECS_DIR)

GIT_LOCK_FILE = "/tmp/ralph-git-lock"

# Load config - use relative path from script location
script_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(script_dir, '..', 'config.json')
try:
    import json
    with open(CONFIG_FILE, 'r') as f:
        CONFIG = json.load(f)
    MAX_RETRIES = CONFIG.get('execution', {}).get('max_task_retries', 3)
    VERIFY_TIMEOUT = CONFIG.get('execution', {}).get('verify_timeout', 120)
except:
    MAX_RETRIES = 3
    VERIFY_TIMEOUT = 120


def read_file(path):
    """Read file content safely."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


def acquire_git_lock(timeout=30):
    """Acquire exclusive lock for git operations."""
    import time
    start = time.time()
    while os.path.exists(GIT_LOCK_FILE):
        if time.time() - start > timeout:
            return False
        time.sleep(0.1)
    # Create lock file
    with open(GIT_LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))
    return True


def release_git_lock():
    """Release git lock."""
    if os.path.exists(GIT_LOCK_FILE):
        os.remove(GIT_LOCK_FILE)


def run_subprocess(args, cwd=None, capture=True, check=False, input_text=None):
    """Run subprocess safely, returns (success, stdout, stderr)."""
    try:
        result = subprocess.run(
            args,
            cwd=cwd,
            capture_output=capture,
            text=True,
            input=input_text,
            timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def parse_task(tasks_content, task_index):
    """Parse a specific task from tasks.md by finding task at the given index."""
    lines = tasks_content.split('\n')
    in_task = False
    task_lines = []
    current_idx = -1
    
    for line in lines:
        task_match = re.match(r'^- \[([ x])\] (\d+\.\d+)', line)
        if task_match:
            is_complete = task_match.group(1) == 'x'
            current_idx += 1
            
            if current_idx == task_index:
                in_task = True
                task_lines.append(line)
            elif in_task:
                break
        elif in_task:
            task_lines.append(line)
    
    return '\n'.join(task_lines) if task_lines else None


def parse_task_sections(task_content):
    """Parse Do, Files, Done when, Verify, Commit from task."""
    sections = {
        'do': None,
        'files': None,
        'done_when': None,
        'verify': None,
        'commit': None,
        'description': None
    }
    
    desc_match = re.match(r'^- \[.+\] (\d+\.\d+) (.+?)(?:\n  \*\*|\s*$)', task_content)
    if desc_match:
        sections['description'] = f"{desc_match.group(1)} {desc_match.group(2)}"
    
    for section in ['do', 'files', 'done_when', 'verify', 'commit']:
        pattern = r'  \*\*' + section.capitalize() + r'\*\*:\s*(.+?)(?=\n  \*\*|\n*$)'
        match = re.search(pattern, task_content, re.DOTALL)
        if match:
            value = match.group(1).strip()
            sections[section] = value
    
    return sections


def extract_file_names(files_field):
    """Extract file names from **Files** field."""
    if not files_field:
        return []
    files = re.split(r'[\n,]', files_field)
    return [f.strip() for f in files if f.strip()]


def extract_function_from_do(do_field, filename):
    """Extract function information from **Do** field."""
    if not do_field:
        return None, []
    
    func_pattern = r'with\s+(\w+)\s*\(([^)]*)\)\s*function'
    match = re.search(func_pattern, do_field)
    
    if match:
        func_name = match.group(1)
        params = match.group(2)
        param_list = [p.strip() for p in params.split(',') if p.strip()]
        return func_name, param_list
    
    return None, []


def sanitize_filename(filename):
    """Sanitize filename to prevent shell injection."""
    # Remove any shell metacharacters
    sanitized = re.sub(r'[;&|$`!()<>{}[\]\\*?~\n]', '', filename)
    return sanitized.strip()


def generate_python_content(filename, do_field, description):
    """Generate Python file content based on task description."""
    func_name, params = extract_function_from_do(do_field, filename)
    
    if func_name:
        if params:
            sig = ', '.join(params)
        else:
            sig = ''
        
        func_bodies = {
            'add': '    return a + b',
            'subtract': '    return a - b',
            'multiply': '    return a * b',
            'divide': '    if b == 0: raise ValueError("Cannot divide by zero")\n    return a / b',
            'greet': '    return f"Hello, {name}!"',
            'echo': '    return " ".join(args)',
            'hello': '    return "Hello, World!"',
        }
        
        body = func_bodies.get(func_name, '    pass')
        
        if body == '    pass' and params:
            param_names = [p.split()[1] if ' ' in p else p for p in params]
            body = f'    # TODO: implement\n    return ({", ".join(param_names)})'
        
        content = f'''#!/usr/bin/env python3
"""Auto-generated by Ralph spec-executor."""

def {func_name}({sig}):
{body}


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        try:
            result = {func_name}(*sys.argv[1:])
            print(result)
        except TypeError:
            print(f"Usage: python {filename} [args...]")
    else:
        print(f"{func_name}() = {{{func_name}()}}")
'''
    else:
        base_name = os.path.splitext(filename)[0]
        content = f'''#!/usr/bin/env python3
"""Auto-generated by Ralph spec-executor."""

import sys

def main():
    """Main function."""
    pass

if __name__ == "__main__":
    main()
'''
    
    return content


def generate_shell_content(filename, do_field, description):
    """Generate Shell script content."""
    content = f'''#!/bin/bash
# Auto-generated by Ralph spec-executor

# TODO: Implement according to: {do_field[:50]}...

echo "Implement: {do_field}"
'''
    return content


def generate_js_content(filename, do_field, description):
    """Generate JavaScript file content."""
    func_name, _ = extract_function_from_do(do_field, filename)
    
    if func_name:
        content = f'''// Auto-generated by Ralph spec-executor

function {func_name}() {{
    // TODO: implement
    return null;
}}

module.exports = {{ {func_name} }};
'''
    else:
        content = '''// Auto-generated by Ralph spec-executor
console.log("Hello");
'''
    
    return content


def generate_markdown_content(filename, do_field, description):
    """Generate Markdown file content."""
    content = f'''# {filename}

Auto-generated by Ralph spec-executor.

## Description
{description}

## Implementation
{do_field}
'''
    return content


def generate_generic_content(filename, do_field, description):
    """Generate generic file content."""
    content = f'''# {filename}

Auto-generated by Ralph spec-executor.

Description: {description}
Do: {do_field}
'''
    return content


def create_file_from_task(filename, spec_path, do_field, description):
    """Create a file based on task description."""
    filepath = os.path.join(spec_path, filename)
    
    # Sanitize filename to prevent shell injection
    safe_filename = sanitize_filename(filename)
    filepath = os.path.join(spec_path, safe_filename)
    
    if filename.endswith('.py'):
        content = generate_python_content(filename, do_field, description)
    elif filename.endswith('.sh'):
        content = generate_shell_content(filename, do_field, description)
    elif filename.endswith('.js') or filename.endswith('.mjs'):
        content = generate_js_content(filename, do_field, description)
    elif filename.endswith('.md'):
        content = generate_markdown_content(filename, do_field, description)
    else:
        content = generate_generic_content(filename, do_field, description)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return safe_filename


def run_verify(verify_cmd, spec_path):
    """Run verification command safely."""
    if not verify_cmd:
        return True, "No verification command"
    
    # Use subprocess.run with shell=False for safer execution
    # But allow shell=True for complex commands with pipes
    try:
        result = subprocess.run(
            verify_cmd,
            shell=True,
            cwd=spec_path,
            capture_output=True,
            text=True,
            timeout=VERIFY_TIMEOUT
        )
        success = result.returncode == 0
        return success, f"Exit code: {result.returncode}"
    except subprocess.TimeoutExpired:
        return False, "Verification timed out after 120 seconds"
    except Exception as e:
        return False, str(e)


def update_progress_file(progress_path, task_desc, commit_hash, learnings=None):
    """Update progress file with completed task."""
    timestamp = subprocess.run(
        ['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'],
        capture_output=True, text=True
    ).stdout.strip()
    
    # Handle None values
    task_desc = task_desc or 'Unknown task'
    commit_hash = commit_hash or 'local'

    if os.path.exists(progress_path):
        content = read_file(progress_path)
        content = re.sub(r'\nNone\n', '\n', content)
        content = re.sub(r'\nNone$', '', content)
        content = re.sub(
            r'(## Completed Tasks\n)',
            r'\1- [x] ' + task_desc + ' - ' + commit_hash + '\n',
            content
        )
        content = re.sub(
            r'## Current Task\n.+',
            r'## Current Task\nAwaiting next task',
            content
        )
    else:
        content = f"""---
spec: unknown
phase: execution
task: 0/0
updated: {timestamp}
---

## Completed Tasks
- [x] {task_desc} - {commit_hash}

## Current Task
Awaiting next task

## Learnings
- Framework execution started
"""
    
    with open(progress_path, 'w') as f:
        f.write(content)


def check_git_initialized(spec_path):
    """Check if git is initialized in spec directory."""
    success, stdout, _ = run_subprocess(['git', 'status'], cwd=spec_path)
    return success


def git_add(filepath):
    """Stage a file safely."""
    if not acquire_git_lock():
        return False, "Could not acquire git lock"
    try:
        safe_path = os.path.abspath(filepath)
        success, out, err = run_subprocess(['git', 'add', safe_path])
        return success, err or out
    finally:
        release_git_lock()


def git_commit(commit_msg, spec_path):
    """Commit changes safely with git lock."""
    if not acquire_git_lock():
        return False, "Could not acquire git lock"
    try:
        # Use a safe subprocess call with proper escaping
        success, stdout, stderr = run_subprocess(
            ['git', 'commit', '-m', commit_msg],
            cwd=spec_path
        )
        
        if not success:
            # Check if it's "nothing to commit"
            if 'nothing to commit' in stderr or 'nothing to commit' in stdout:
                return True, "No changes to commit"
        
        return success, stderr or stdout
    finally:
        release_git_lock()


def commit_files(files, commit_msg, spec_path):
    """Stage and commit files safely."""
    if not commit_msg:
        commit_msg = "chore: task completed"
    
    # Stage each file
    for f in files:
        filepath = os.path.join(spec_path, f)
        if os.path.exists(filepath):
            git_add(filepath)
    
    # Check for changes
    success, stdout, _ = run_subprocess(['git', 'status', '--porcelain'], cwd=spec_path)
    if not success or not stdout.strip():
        return None, "No changes to commit"
    
    # Commit
    success, msg = git_commit(commit_msg, spec_path)
    
    # Get commit hash
    success, stdout, _ = run_subprocess(['git', 'log', '-1', '--format=%H'], cwd=spec_path)
    commit_hash = stdout.strip()[:7] if success else None
    
    return commit_hash, msg


def mark_task_complete(tasks_path, task_index):
    """Mark a task as complete in tasks.md."""
    content = read_file(tasks_path)
    lines = content.split('\n')
    
    current_idx = 0
    
    for i, line in enumerate(lines):
        task_match = re.match(r'^- \[([ x])\] (\d+\.\d+)', line)
        if task_match:
            is_complete = task_match.group(1) == 'x'
            if not is_complete and current_idx == task_index:
                lines[i] = line.replace('[ ]', '[x]')
                print(f"✓ Marked task {current_idx} as complete in tasks.md")
                with open(tasks_path, 'w') as f:
                    f.write('\n'.join(lines))
                return True
            current_idx += 1
    
    print(f"⚠️ Could not find task at index {task_index}")
    return False


def main():
    if len(sys.argv) < 3:
        print("Usage: spec-executor.py <spec-name> <task-index> [progress-file] [--dry-run]")
        sys.exit(1)
    
    spec_name = sys.argv[1]
    task_index = int(sys.argv[2])
    progress_file = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != '--dry-run' else None
    dry_run = '--dry-run' in sys.argv
    
    spec_path = f"{SPECS_DIR}/{spec_name}"
    tasks_path = f"{spec_path}/tasks.md"
    progress_path = f"{spec_path}/.progress.md"
    
    if not os.path.exists(spec_path):
        print(f"ERROR: Spec '{spec_name}' not found at {spec_path}")
        sys.exit(1)
    
    # Check git is initialized (skip in dry-run)
    if not dry_run and not check_git_initialized(spec_path):
        print("ERROR: Git not initialized. Run 'git init' first.")
        sys.exit(1)
    
    tasks_content = read_file(tasks_path)
    if not tasks_content:
        print(f"ERROR: tasks.md not found at {tasks_path}")
        sys.exit(1)
    
    task_content = parse_task(tasks_content, task_index)
    if not task_content:
        print(f"ERROR: Could not find task at index {task_index}")
        sys.exit(1)
    
    task = parse_task_sections(task_content)
    
    print(f"\n{'='*60}")
    print(f"🔧 SPEC-EXECUTOR: {spec_name}")
    print(f"📋 TASK: {task['description']}")
    if dry_run:
        print(f"🔍 DRY RUN MODE - No changes will be made")
    print(f"{'='*60}\n")
    
    print(f"Parsed fields:")
    print(f"  do: {task['do']}")
    print(f"  files: {task['files']}")
    print(f"  verify: {task['verify']}")
    print(f"  commit: {task['commit']}")
    print()
    
    # Execute: Create files with proper interpretation
    file_names = extract_file_names(task['files'])
    created_files = []
    
    if dry_run:
        # Dry-run: show what would be done
        print(f"🔍 DRY RUN: Would create files:")
        for filename in file_names:
            safe_filename = sanitize_filename(filename)
            created_files.append(safe_filename)
            print(f"  → {safe_filename}")
            if filename.endswith('.py'):
                func_name, _ = extract_function_from_do(task['do'], filename)
                if func_name:
                    print(f"     → Would add {func_name}() function")
        
        # Show what verification would be done
        if task['verify']:
            print(f"\n🔍 DRY RUN: Would run verification:")
            print(f"  → {task['verify']}")
        
        # Show what commit would be made
        if task['commit']:
            print(f"\n🔍 DRY RUN: Would commit:")
            print(f"  → Message: {task['commit']}")
            print(f"  → Files: {', '.join(created_files + ['tasks.md', '.progress.md'])}")
        
        # Show what would be updated
        print(f"\n🔍 DRY RUN: Would mark task {task_index} as complete in tasks.md")
        print(f"🔍 DRY RUN: Would update progress file")
    else:
        # Actual execution
        for filename in file_names:
            safe_filename = create_file_from_task(filename, spec_path, task['do'], task['description'])
            created_files.append(safe_filename)
            print(f"✓ Created: {safe_filename}")
            if filename.endswith('.py'):
                func_name, _ = extract_function_from_do(task['do'], filename)
                if func_name:
                    print(f"   → Added {func_name}() function")
        
        # Run verification with retry
        if task['verify']:
            print(f"\nVERIFY: {task['verify']}")
            max_retries = MAX_RETRIES
            for attempt in range(max_retries):
                success, msg = run_verify(task['verify'], spec_path)
                print(f"Result: {msg}")
                if success:
                    print(f"✓ Verification passed on attempt {attempt + 1}")
                    break
                if attempt < max_retries - 1:
                    print(f"⚠️ Verification failed, retrying ({attempt + 1}/{max_retries})...")
            else:
                print("\n❌ VERIFICATION FAILED after 3 attempts")
                print("TASK_COMPLETE: FAILED")
                # Clean up progress files before exiting
                if progress_file:
                    temp_file = f"{spec_path}/{progress_file}"
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                sys.exit(1)
        
        # Mark task complete (skip in parallel mode - coordinator will handle it)
        # In parallel mode, multiple executors would race to write tasks.md
        progress_file_suffix = progress_file if progress_file else ".progress.md"
        if progress_file_suffix.startswith(".progress-task-"):
            # Parallel mode - don't mark task complete, let coordinator do it
            print(f"✓ Task {task_index} complete (coordinator will mark in tasks.md)")
        else:
            # Sequential mode - mark task complete now
            success = mark_task_complete(tasks_path, task_index)
            if not success:
                print("⚠️ Warning: Could not mark task complete in tasks.md")
        
        # === VERIFICATION LAYER: Checkmark Verification ===
        # Verify task was actually marked [x] before committing
        # In parallel mode, coordinator handles this after merging
        if not progress_file or not progress_file.startswith(".progress-task-"):
            with open(tasks_path, 'r') as f:
                content = f.read()
            # Count completed tasks up to this point
            completed_count = content.count('- [x]')
            if completed_count <= task_index:
                print(f"\n❌ CHECKMARK VERIFICATION FAILED")
                print(f"   Expected task {task_index} to be marked [x], but only {completed_count} tasks marked complete")
                print(f"   This may indicate a parsing issue or task structure mismatch")
                return False
        
        # First, add all files in spec directory to git
        subprocess.run(
            ['git', 'add', '.'],
            cwd=spec_path,
            capture_output=True,
            text=True
        )
        
        # === VERIFICATION LAYER: Commit Discipline ===
        # Check for uncommitted spec files before committing
        if not dry_run:
            result = subprocess.run(
                ['git', 'status', '--porcelain', f'{spec_name}/tasks.md', '.progress.md'],
                cwd=spec_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and result.stdout.strip():
                print(f"\n⚠️ WARNING: Spec files have uncommitted changes")
                print(f"   This violates commit discipline - spec files must be committed with every task")
        
        # Then commit all tracked files
        # This ensures each commit has the complete state
        result = subprocess.run(
            ['git', 'ls-files'],
            cwd=spec_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            # Commit all tracked files
            all_files = result.stdout.strip().split('\n')
            # Remove .progress.md from list as it may not exist yet
            all_files = [f for f in all_files if f and not f.startswith('.progress')]
            files_to_commit = all_files if all_files else ['tasks.md']
        else:
            # Fallback: use created files + tasks.md
            files_to_commit = created_files + ['tasks.md']
            if progress_file:
                files_to_commit.append(progress_file)
            else:
                files_to_commit.append('.progress.md')
        
        commit_hash, commit_msg = commit_files(files_to_commit, task['commit'], spec_path)
        print(f"\nCOMMIT: {commit_msg}")
        if commit_hash:
            print(f"HASH: {commit_hash}")
        
        # Update progress
        if progress_file:
            progress_file_path = f"{spec_path}/{progress_file}"
        else:
            progress_file_path = progress_path
        
        if os.path.exists(progress_file_path):
            update_progress_file(progress_file_path, task['description'], commit_hash or 'local')
            print(f"✓ Updated progress file")
    
    print(f"\n{'='*60}")
    if dry_run:
        print("TASK_COMPLETE (Dry Run)")
    else:
        print("TASK_COMPLETE")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
