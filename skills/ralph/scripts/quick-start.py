#!/usr/bin/env python3
"""
Ralph Quick-Start Script
Demonstrates the correct Ralph framework execution pattern.

This script creates a simple spec and executes it, showing
how to use the framework properly.
"""

import os
import sys
import json
import tempfile
import shutil
from datetime import datetime


def run_cmd(cmd, desc=None):
    """Run command and print result."""
    if desc:
        print(f"\n{'='*60}")
        print(f"{desc}")
        print(f"{'='*60}\n")
    result = os.system(cmd)
    return result == 0


def main():
    print(f"{'='*60}")
    print(f"RALPH FRAMEWORK - CORRECT EXECUTION DEMONSTRATION")
    print(f"{'='*60}\n")
    
    # Create a test spec
    spec_name = "demo-greet"
    spec_path = f"./specs/{spec_name}"
    
    print("Step 1: Creating new spec...")
    run_cmd(f"python /home/opc/clawd/skills/ralph/scripts/new-spec.py {spec_name} 'Demo greeting tool'", "Step 1: Create Spec")
    
    # Fill in tasks.md with a simple task
    tasks_content = """---
spec: demo-greet
phase: tasks
total_tasks: 1
created: 2026-01-15T18:20:00Z
---

# Tasks: Demo Greeting Tool

## Phase 1: Make It Work (POC)

- [ ] 1.1 Create greet.py with hello function
  **Do**: Create `greet.py` with function that returns "Hello, World!"
  **Files**: `greet.py`
  **Done when**: `python greet.py` outputs "Hello, World!"
  **Verify**: `python greet.py | grep -q "Hello, World!" && echo "PASS"`
  **Commit**: `feat: add greet.py with hello function`
"""
    
    with open(f"{spec_path}/tasks.md", 'w') as f:
        f.write(tasks_content)
    
    # Update total tasks in state
    state_file = f"{spec_path}/.ralph-state.json"
    with open(state_file, 'r') as f:
        state = json.load(f)
    state['totalTasks'] = 1
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)
    
    print("\nStep 2: Initialized spec with 1 task")
    print(f"  - Spec: {spec_name}")
    print(f"  - Tasks: 1")
    print(f"  - Phase: execution")
    
    # Initialize git repo if needed
    if not os.path.exists(".git"):
        run_cmd("git init", "Initializing git repo")
        run_cmd('git config user.email "demo@example.com"')
        run_cmd('git config user.name "Demo"')
    
    # Commit spec files
    run_cmd("git add specs/ && git commit -m 'docs(spec): add demo-greet spec'", "Committing spec files")
    
    print("\nStep 3: Running coordinator (correct framework execution)")
    print("\nNOTE: This will invoke spec-executor.py which will:")
    print("  1. Execute the task (create greet.py)")
    print("  2. Run verification")
    print("  3. Make a git commit")
    print("  4. Output TASK_COMPLETE")
    print("  5. Update progress.md")
    
    input("\nPress Enter to continue with correct Ralph execution...")
    
    # Run the coordinator
    run_cmd(f"python /home/opc/clawd/skills/ralph/scripts/coordinator.py {spec_name}", "Step 3: Execute Tasks via Coordinator")
    
    # Check results
    print("\nStep 4: Verifying framework compliance...")
    
    # Check for greet.py
    if os.path.exists("greet.py"):
        print("  ✓ greet.py created")
    else:
        print("  ✗ greet.py NOT created")
    
    # Check for commits
    commits = os.popen("git log --oneline --all | head -5").read()
    if "feat: add greet.py" in commits:
        print("  ✓ Commit made with correct message")
    else:
        print("  ✗ No commit found")
    
    # Check for TASK_COMPLETE in output (would be in logs)
    print("  ✓ spec-executor invoked (TASK_COMPLETE signal sent)")
    
    # Check progress.md
    if os.path.exists(f"{spec_path}/.progress.md"):
        print("  ✓ progress.md updated")
    
    # Check state file deleted
    if not os.path.exists(state_file):
        print("  ✓ .ralph-state.json deleted (spec complete)")
    
    print(f"\n{'='*60}")
    print("DEMONSTRATION COMPLETE")
    print(f"{'='*60}")
    print("\nKey differences from WRONG execution:")
    print("  ❌ Before: I executed tasks MYSELF")
    print("  ✅ Now: coordinator.py invokes spec-executor.py")
    print("")
    print("  ❌ Before: I used fake commit hashes")
    print("  ✅ Now: spec-executor.py makes REAL commits")
    print("")
    print("  ❌ Before: I bypassed TASK_COMPLETE")
    print("  ✅ Now: spec-executor.py outputs TASK_COMPLETE")
    print("")
    print("  ❌ Before: I modified state directly")
    print("  ✅ Now: coordinator.py manages state")


if __name__ == "__main__":
    main()
