#!/usr/bin/env python3
"""
Ralph Integration Tests
Tests the full spec creation and execution workflow.
"""

import json
import os
import sys
import tempfile
import shutil
import subprocess

SPECS_DIR = "/home/opc/clawd/specs"
RALPH_SCRIPTS = "/home/opc/clawd/skills/ralph/scripts"


def run_cmd(cmd, cwd=None, timeout=60):
    """Run command and return success/failure."""
    try:
        result = subprocess.run(
            cmd, shell=True, cwd=cwd,
            capture_output=True, text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"


def test_new_spec_creation():
    """Test creating a new spec."""
    print("Test 1: Creating new spec...")
    
    # Create temp directory for this test
    test_dir = tempfile.mkdtemp(prefix="ralph_test_")
    original_cwd = os.getcwd()
    os.chdir(test_dir)
    
    try:
        # Initialize git
        subprocess.run("git init", capture_output=True)
        subprocess.run('git config user.email "test@example.com"')
        subprocess.run('git config user.name "Test"')
        
        # Create symlink to actual specs dir
        os.makedirs("specs", exist_ok=True)
        subprocess.run(f"ln -sf {SPECS_DIR} specs/actual", capture_output=True)
        
        # Create spec
        success, out, err = run_cmd(
            f"python {RALPH_SCRIPTS}/new-spec.py test-spec 'Test integration'",
            cwd=test_dir
        )
        
        if not success:
            return False, f"Failed to create spec: {err}"
        
        # Check spec files exist
        spec_path = "specs/actual/test-spec"
        if not os.path.exists(f"{spec_path}/.ralph-state.json"):
            return False, "State file not created"
        if not os.path.exists(f"{spec_path}/research.md"):
            return False, "Research file not created"
        if not os.path.exists(f"{spec_path}/tasks.md"):
            return False, "Tasks file not created"
        
        return True, "Spec created successfully"
    
    finally:
        os.chdir(original_cwd)
        shutil.rmtree(test_dir)


def test_single_task_execution():
    """Test executing a single task."""
    print("Test 2: Single task execution...")
    
    test_dir = tempfile.mkdtemp(prefix="ralph_test_")
    original_cwd = os.getcwd()
    os.chdir(test_dir)
    
    try:
        subprocess.run("git init", capture_output=True)
        subprocess.run('git config user.email "test@example.com"')
        subprocess.run('git config user.name "Test"')
        os.makedirs("specs", exist_ok=True)
        subprocess.run(f"ln -sf {SPECS_DIR} specs/actual", capture_output=True)
        
        # Create spec
        subprocess.run(f"python {RALPH_SCRIPTS}/new-spec.py single-task 'Test'", 
                      capture_output=True, shell=True)
        
        # Create simple task
        tasks_content = """---
spec: single-task
phase: tasks
total_tasks: 1
---

# Tasks

- [ ] 1.1 Create hello.py
  **Do**: Create hello.py with hello() function
  **Files**: hello.py
  **Verify**: python -c "from hello import hello; print(hello())" | grep -q "Hello"
  **Commit**: feat: add hello.py
"""
        with open("specs/actual/single-task/tasks.md", 'w') as f:
            f.write(tasks_content)
        
        with open("specs/actual/single-task/.ralph-state.json", 'r') as f:
            state = json.load(f)
        state['totalTasks'] = 1
        with open("specs/actual/single-task/.ralph-state.json", 'w') as f:
            json.dump(state, f, indent=2)
        
        subprocess.run("git add specs/", capture_output=True)
        subprocess.run('git commit -m "docs: add spec"', capture_output=True)
        
        # Execute task
        success, out, err = run_cmd(
            f"python {RALPH_SCRIPTS}/coordinator.py single-task",
            cwd=test_dir, timeout=120
        )
        
        if not success:
            return False, f"Coordinator failed: {err}"
        
        if "TASK_COMPLETE" not in out:
            return False, "TASK_COMPLETE not found in output"
        
        return True, "Single task executed successfully"
    
    finally:
        os.chdir(original_cwd)
        shutil.rmtree(test_dir)


def test_parallel_tasks():
    """Test parallel task execution."""
    print("Test 3: Parallel task execution...")
    
    test_dir = tempfile.mkdtemp(prefix="ralph_test_")
    original_cwd = os.getcwd()
    os.chdir(test_dir)
    
    try:
        subprocess.run("git init", capture_output=True)
        subprocess.run('git config user.email "test@example.com"')
        subprocess.run('git config user.name "Test"')
        os.makedirs("specs", exist_ok=True)
        subprocess.run(f"ln -sf {SPECS_DIR} specs/actual", capture_output=True)
        
        subprocess.run(f"python {RALPH_SCRIPTS}/new-spec.py parallel-test 'Test'", 
                      capture_output=True, shell=True)
        
        # Create parallel tasks
        tasks_content = """---
spec: parallel-test
phase: tasks
total_tasks: 3
---

# Tasks

- [ ] 1.1 Create file1.py
  **Do**: Create file1.py
  **Files**: file1.py
  **Verify**: python file1.py | grep -q "file1"
  **Commit**: feat: add file1.py

- [ ] 1.2 [P] Create file2.py
  **Do**: Create file2.py
  **Files**: file2.py
  **Verify**: python file2.py | grep -q "file2"
  **Commit**: feat: add file2.py

- [ ] 1.3 [P] Create file3.py
  **Do**: Create file3.py
  **Files**: file3.py
  **Verify**: python file3.py | grep -q "file3"
  **Commit**: feat: add file3.py
"""
        with open("specs/actual/parallel-test/tasks.md", 'w') as f:
            f.write(tasks_content)
        
        with open("specs/actual/parallel-test/.ralph-state.json", 'r') as f:
            state = json.load(f)
        state['totalTasks'] = 3
        with open("specs/actual/parallel-test/.ralph-state.json", 'w') as f:
            json.dump(state, f, indent=2)
        
        subprocess.run("git add specs/", capture_output=True)
        subprocess.run('git commit -m "docs: add spec"', capture_output=True)
        
        # Execute all tasks
        for _ in range(3):
            success, out, err = run_cmd(
                f"python {RALPH_SCRIPTS}/coordinator.py parallel-test",
                cwd=test_dir, timeout=120
            )
            if not success:
                return False, f"Coordinator failed: {err}"
        
        return True, "Parallel tasks executed successfully"
    
    finally:
        os.chdir(original_cwd)
        shutil.rmtree(test_dir)


def run_all_tests():
    """Run all integration tests."""
    tests = [
        ("New Spec Creation", test_new_spec_creation),
        ("Single Task Execution", test_single_task_execution),
        ("Parallel Tasks", test_parallel_tasks),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success, msg = test_func()
            results.append((name, success, msg))
            status = "✓ PASS" if success else "✗ FAIL"
            print(f"  {status}: {name} - {msg}")
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"  ✗ FAIL: {name} - {e}")
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"\n{'='*50}")
    print(f"INTEGRATION TESTS: {passed}/{total} passed")
    print(f"{'='*50}")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
