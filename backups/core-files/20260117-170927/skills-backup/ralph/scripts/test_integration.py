#!/usr/bin/env python3
"""
Ralph Integration Tests
Tests the complete Ralph workflow from spec creation to execution.

Test Coverage:
1. Full spec creation and execution workflow
2. Parallel task execution
3. Error handling and recovery
4. State file management

Each test:
- Creates a temporary spec
- Runs the full workflow (new-spec → coordinator)
- Verifies all files are created correctly
- Verifies git commits are made
- Cleans up after itself
"""

import unittest
import sys
import os
import json
import tempfile
import shutil
import subprocess
import re
from pathlib import Path


class RalphIntegrationTest(unittest.TestCase):
    """Integration tests for Ralph skill."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are shared across all tests."""
        cls.test_base_dir = tempfile.mkdtemp(prefix="ralph-integration-")
        cls.original_dir = os.getcwd()
        os.chdir(cls.test_base_dir)
        
        # Initialize git repo
        subprocess.run(['git', 'init'], capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], capture_output=True, check=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial commit'], capture_output=True, check=True)
        
        print(f"\n{'='*60}")
        print(f"Integration test workspace: {cls.test_base_dir}")
        print(f"{'='*60}")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        os.chdir(cls.original_dir)
        # Only remove if tests completed
        if hasattr(cls, '_keep_on_failure') and cls._keep_on_failure:
            print(f"\n{'='*60}")
            print(f"Test workspace preserved for inspection:")
            print(f"  {cls.test_base_dir}")
            print(f"{'='*60}")
        else:
            shutil.rmtree(cls.test_base_dir, ignore_errors=True)
    
    def setUp(self):
        """Set up individual test."""
        self.spec_name = None
    
    def tearDown(self):
        """Clean up after individual test."""
        if self.spec_name:
            spec_path = os.path.join(self.test_base_dir, 'specs', self.spec_name)
            if os.path.exists(spec_path):
                shutil.rmtree(spec_path, ignore_errors=True)
    
    # Helper methods
    
    def run_script(self, script_name, *args, check=True):
        """Run a Ralph script and return result."""
        script_path = f"/home/opc/clawd/skills/ralph/scripts/{script_name}"
        cmd = ['python', script_path] + list(args)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=self.test_base_dir
        )
        if check and result.returncode != 0:
            print(f"\nScript {script_name} failed:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
        return result
    
    def create_simple_tasks_file(self, spec_path):
        """Create a simple tasks file for testing."""
        tasks_content = """# Tasks: Test Feature

## Overview

Total tasks: 5
Simple test tasks for integration testing.

## Phase 1: Make It Work (POC)

- [ ] 1.1 Create calculator.py with add(a, b) function
  **Do**: Create calculator.py with add(a, b) function
  **Files**: calculator.py
  **Done when**: python -c "from calculator import add; assert add(2,3) == 5"
  **Verify**: python -c "from calculator import add; assert add(2,3) == 5" && echo "PASS"
  **Commit**: feat(calculator): add add(a, b) function
  _Requirements: FR-1_

- [ ] 1.2 Create multiplier.py with multiply(a, b) function
  **Do**: Create multiplier.py with multiply(a, b) function
  **Files**: multiplier.py
  **Done when**: python -c "from multiplier import multiply; assert multiply(2,3) == 6"
  **Verify**: python -c "from multiplier import multiply; assert multiply(2,3) == 6" && echo "PASS"
  **Commit**: feat(multiplier): add multiply(a, b) function
  _Requirements: FR-2_

- [ ] 1.3 [VERIFY] Quality Checkpoint
  **Do**: Verify all Python files run without errors
  **Done when**: All files execute successfully
  **Verify**: python -c "from calculator import add; from multiplier import multiply; assert add(2,3) == 5 and multiply(2,3) == 6" && echo "PASS"
  **Commit**: chore: pass quality checkpoint

- [ ] 1.4 Create README.md
  **Do**: Create README.md documenting the calculator and multiplier
  **Files**: README.md
  **Done when**: README.md exists and contains documentation
  **Verify**: test -f README.md && grep -q "Calculator" README.md && echo "PASS"
  **Commit**: docs: add README.md

- [ ] 1.5 POC Checkpoint
  **Do**: Verify feature works end-to-end
  **Done when**: All modules can be imported and used
  **Verify**: python -c "from calculator import add; from multiplier import multiply; print(f'add(2,3)={add(2,3)}, multiply(2,3)={multiply(2,3)}')" && echo "PASS"
  **Commit**: feat: complete POC
"""
        with open(os.path.join(spec_path, 'tasks.md'), 'w') as f:
            f.write(tasks_content)
    
    def create_parallel_tasks_file(self, spec_path):
        """Create a tasks file with parallel tasks for testing."""
        tasks_content = """# Tasks: Parallel Test

## Overview

Total tasks: 7
Test parallel task execution.

## Phase 1: Make It Work (POC)

- [ ] 1.1 [P] Create utils/alpha.py
  **Do**: Create utils/alpha.py with alpha() function
  **Files**: utils/alpha.py
  **Done when**: File exists
  **Verify**: test -f utils/alpha.py && echo "PASS"
  **Commit**: feat(utils): add alpha.py

- [ ] 1.2 [P] Create utils/beta.py
  **Do**: Create utils/beta.py with beta() function
  **Files**: utils/beta.py
  **Done when**: File exists
  **Verify**: test -f utils/beta.py && echo "PASS"
  **Commit**: feat(utils): add beta.py

- [ ] 1.3 [P] Create utils/gamma.py
  **Do**: Create utils/gamma.py with gamma() function
  **Files**: utils/gamma.py
  **Done when**: File exists
  **Verify**: test -f utils/gamma.py && echo "PASS"
  **Commit**: feat(utils): add gamma.py

- [ ] 1.4 [SEQUENTIAL] Create README.md
  **Do**: Create README.md documenting utils
  **Files**: README.md
  **Done when**: README.md exists
  **Verify**: test -f README.md && echo "PASS"
  **Commit**: docs: add README.md

- [ ] 1.5 [P] Create config/app.json
  **Do**: Create config/app.json with configuration
  **Files**: config/app.json
  **Done when**: File exists and is valid JSON
  **Verify**: test -f config/app.json && python -c "import json; json.load(open('config/app.json'))" && echo "PASS"
  **Commit**: config: add app.json

- [ ] 1.6 [P] Create config/settings.py
  **Do**: Create config/settings.py with settings loader
  **Files**: config/settings.py
  **Done when**: File exists
  **Verify**: test -f config/settings.py && echo "PASS"
  **Commit**: config: add settings.py

- [ ] 1.7 [VERIFY] Verify all files created
  **Do**: Verify all files exist and are valid
  **Done when**: All verification passes
  **Verify**: test -f utils/alpha.py && test -f utils/beta.py && test -f utils/gamma.py && test -f README.md && test -f config/app.json && test -f config/settings.py && echo "PASS"
  **Commit**: chore: pass quality checkpoint
"""
        with open(os.path.join(spec_path, 'tasks.md'), 'w') as f:
            f.write(tasks_content)
    
    def create_error_task_file(self, spec_path):
        """Create a tasks file that will fail for testing error handling."""
        tasks_content = """# Tasks: Error Test

## Overview

Total tasks: 3
Test error handling and recovery.

## Phase 1: Make It Work (POC)

- [ ] 1.1 Create success.py
  **Do**: Create success.py with success() function
  **Files**: success.py
  **Done when**: File exists
  **Verify**: python -c "from success import success; print('PASS')" || echo "PASS"
  **Commit**: feat: add success.py

- [ ] 1.2 Create fail.py
  **Do**: Create fail.py with fail() function
  **Files**: fail.py
  **Done when**: File exists
  **Verify**: python -c "this will fail" && echo "PASS"
  **Commit**: feat: add fail.py (should not commit)

- [ ] 1.3 Create recovery.py
  **Do**: Create recovery.py with recovery() function
  **Files**: recovery.py
  **Done when**: File exists
  **Verify**: python -c "from recovery import recovery; print('PASS')" || echo "PASS"
  **Commit**: feat: add recovery.py
"""
        with open(os.path.join(spec_path, 'tasks.md'), 'w') as f:
            f.write(tasks_content)
    
    def read_state(self, spec_path):
        """Read state file."""
        state_file = os.path.join(spec_path, '.ralph-state.json')
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                return json.load(f)
        return None
    
    def read_progress(self, spec_path):
        """Read progress file."""
        progress_file = os.path.join(spec_path, '.progress.md')
        if os.path.exists(progress_file):
            with open(progress_file, 'r') as f:
                return f.read()
        return None
    
    def get_git_commits(self, spec_path):
        """Get list of git commits."""
        result = subprocess.run(
            ['git', 'log', '--oneline'],
            capture_output=True,
            text=True,
            cwd=spec_path
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    # Test cases
    
    def test_01_spec_creation(self):
        """Test 1: Full spec creation workflow."""
        print(f"\n{'='*60}")
        print("TEST 1: Spec Creation Workflow")
        print(f"{'='*60}")
        
        spec_name = "test-spec-creation"
        self.spec_name = spec_name
        
        # Run new-spec
        result = self.run_script('new-spec.py', spec_name, "Test spec for integration testing")
        self.assertEqual(result.returncode, 0, "new-spec.py should succeed")
        
        # Verify directory structure
        spec_path = os.path.join(self.test_base_dir, 'specs', spec_name)
        self.assertTrue(os.path.exists(spec_path), "Spec directory should exist")
        
        expected_files = [
            '.ralph-state.json',
            '.progress.md',
            'research.md',
            'requirements.md',
            'design.md',
            'tasks.md'
        ]
        
        for file in expected_files:
            file_path = os.path.join(spec_path, file)
            self.assertTrue(os.path.exists(file_path), f"{file} should exist")
        
        # Verify .current-spec
        current_spec_path = os.path.join(self.test_base_dir, 'specs', '.current-spec')
        self.assertTrue(os.path.exists(current_spec_path), ".current-spec should exist")
        
        with open(current_spec_path, 'r') as f:
            current_spec = f.read()
        self.assertEqual(current_spec, spec_name, "Current spec should match")
        
        # Verify state file
        state = self.read_state(spec_path)
        self.assertIsNotNone(state, "State file should exist")
        self.assertEqual(state['name'], spec_name, "State name should match")
        self.assertEqual(state['phase'], 'research', "Initial phase should be research")
        self.assertEqual(state['taskIndex'], 0, "Initial task index should be 0")
        
        print("✓ Spec creation workflow test passed")
    
    def test_02_full_execution_workflow(self):
        """Test 2: Full execution workflow from start to finish."""
        print(f"\n{'='*60}")
        print("TEST 2: Full Execution Workflow")
        print(f"{'='*60}")
        
        spec_name = "test-full-execution"
        self.spec_name = spec_name
        
        # Create spec
        result = self.run_script('new-spec.py', spec_name, "Test full execution")
        self.assertEqual(result.returncode, 0, "new-spec.py should succeed")
        
        spec_path = os.path.join(self.test_base_dir, 'specs', spec_name)
        
        # Create tasks
        self.create_simple_tasks_file(spec_path)
        
        # Run coordinator to completion
        max_cycles = 10  # Prevent infinite loops
        cycle = 0
        
        while cycle < max_cycles:
            result = self.run_script('coordinator.py', spec_name, check=False)
            
            # Check if complete
            if 'SPEC_COMPLETE' in result.stdout:
                print(f"✓ Spec completed in {cycle + 1} cycle(s)")
                break
            
            # Check if cycle complete
            if 'CYCLE_COMPLETE' not in result.stdout:
                print(f"✗ Unexpected coordinator output")
                print(f"STDOUT: {result.stdout}")
                self.fail("Coordinator should output CYCLE_COMPLETE or SPEC_COMPLETE")
            
            cycle += 1
        
        self.assertLess(cycle, max_cycles, "Should complete within max cycles")
        
        # Verify all files created
        expected_files = [
            'calculator.py',
            'multiplier.py',
            'README.md'
        ]
        
        for file in expected_files:
            file_path = os.path.join(spec_path, file)
            self.assertTrue(os.path.exists(file_path), f"{file} should be created")
        
        # Verify git commits
        commits = self.get_git_commits(spec_path)
        self.assertGreater(len(commits), 0, "Should have git commits")
        
        # Verify commit messages contain expected keywords
        commit_messages = ' '.join(commits).lower()
        self.assertIn('calculator', commit_messages, "Should commit calculator changes")
        self.assertIn('multiplier', commit_messages, "Should commit multiplier changes")
        self.assertIn('readme', commit_messages, "Should commit README changes")
        
        # Verify state file deleted
        state_file = os.path.join(spec_path, '.ralph-state.json')
        self.assertFalse(os.path.exists(state_file), "State file should be deleted on completion")
        
        # Verify progress file updated
        progress = self.read_progress(spec_path)
        self.assertIsNotNone(progress, "Progress file should exist")
        self.assertIn('Completed Tasks', progress, "Should have completed tasks section")
        
        # Verify tasks.md all checked
        tasks_path = os.path.join(spec_path, 'tasks.md')
        with open(tasks_path, 'r') as f:
            tasks_content = f.read()
        unchecked = re.findall(r'^- \[ \]', tasks_content, re.MULTILINE)
        self.assertEqual(len(unchecked), 0, "All tasks should be checked")
        
        print("✓ Full execution workflow test passed")
    
    def test_03_parallel_task_execution(self):
        """Test 3: Parallel task execution with [P] markers."""
        print(f"\n{'='*60}")
        print("TEST 3: Parallel Task Execution")
        print(f"{'='*60}")
        
        spec_name = "test-parallel-execution"
        self.spec_name = spec_name
        
        # Create spec
        result = self.run_script('new-spec.py', spec_name, "Test parallel execution")
        self.assertEqual(result.returncode, 0, "new-spec.py should succeed")
        
        spec_path = os.path.join(self.test_base_dir, 'specs', spec_name)
        
        # Create parallel tasks
        self.create_parallel_tasks_file(spec_path)
        
        # Run coordinator to completion
        max_cycles = 15
        cycle = 0
        
        while cycle < max_cycles:
            result = self.run_script('coordinator.py', spec_name, check=False)
            
            if 'SPEC_COMPLETE' in result.stdout:
                print(f"✓ Spec completed in {cycle + 1} cycle(s)")
                break
            
            if 'CYCLE_COMPLETE' not in result.stdout:
                print(f"✗ Unexpected coordinator output")
                self.fail("Coordinator should output CYCLE_COMPLETE or SPEC_COMPLETE")
            
            cycle += 1
        
        self.assertLess(cycle, max_cycles, "Should complete within max cycles")
        
        # Verify all files created including in subdirectories
        expected_files = [
            'utils/alpha.py',
            'utils/beta.py',
            'utils/gamma.py',
            'README.md',
            'config/app.json',
            'config/settings.py'
        ]
        
        for file in expected_files:
            file_path = os.path.join(spec_path, file)
            self.assertTrue(os.path.exists(file_path), f"{file} should be created")
        
        # Verify config/app.json is valid JSON
        config_path = os.path.join(spec_path, 'config/app.json')
        with open(config_path, 'r') as f:
            json_content = json.load(f)
        self.assertIsNotNone(json_content, "config/app.json should be valid JSON")
        
        # Verify parallel tasks were committed
        commits = self.get_git_commits(spec_path)
        self.assertGreater(len(commits), 0, "Should have git commits")
        
        # Verify no temp progress files left
        temp_files = [f for f in os.listdir(spec_path) if f.startswith('.progress-task-')]
        self.assertEqual(len(temp_files), 0, "No temp progress files should remain")
        
        print("✓ Parallel task execution test passed")
    
    def test_04_error_handling_and_recovery(self):
        """Test 4: Error handling when verification fails."""
        print(f"\n{'='*60}")
        print("TEST 4: Error Handling and Recovery")
        print(f"{'='*60}")
        
        spec_name = "test-error-handling"
        self.spec_name = spec_name
        
        # Create spec
        result = self.run_script('new-spec.py', spec_name, "Test error handling")
        self.assertEqual(result.returncode, 0, "new-spec.py should succeed")
        
        spec_path = os.path.join(self.test_base_dir, 'specs', spec_name)
        
        # Create tasks that will fail
        self.create_error_task_file(spec_path)
        
        # Run coordinator - should fail at task 1.2
        result = self.run_script('coordinator.py', spec_name, check=False)
        
        # Should fail with verification error
        self.assertEqual(result.returncode, 1, "Coordinator should fail on verification")
        self.assertIn('VERIFICATION FAILED', result.stdout, "Should output verification failure")
        
        # Verify state file shows task 1.2 incomplete
        state = self.read_state(spec_path)
        self.assertIsNotNone(state, "State file should exist")
        
        # Task 1.1 should be complete (index 0), task 1.2 should be incomplete (index 1)
        tasks_path = os.path.join(spec_path, 'tasks.md')
        with open(tasks_path, 'r') as f:
            tasks_content = f.read()
        
        # First task should be checked
        task1_complete = bool(re.search(r'^- \[x\] 1\.1', tasks_content, re.MULTILINE))
        # Second task should be unchecked
        task2_incomplete = bool(re.search(r'^- \[ \] 1\.2', tasks_content, re.MULTILINE))
        
        self.assertTrue(task1_complete, "Task 1.1 should be complete")
        self.assertTrue(task2_incomplete, "Task 1.2 should be incomplete")
        
        # Verify success.py was created but fail.py was not committed
        self.assertTrue(os.path.exists(os.path.join(spec_path, 'success.py')), "success.py should exist")
        
        # Check git log - should not contain fail.py commit
        commits = self.get_git_commits(spec_path)
        commit_messages = ' '.join(commits).lower()
        self.assertIn('success', commit_messages, "Should commit success.py")
        self.assertNotIn('fail', commit_messages, "Should not commit fail.py (verification failed)")
        
        print("✓ Error handling test passed")
    
    def test_05_state_file_management(self):
        """Test 5: State file management throughout execution."""
        print(f"\n{'='*60}")
        print("TEST 5: State File Management")
        print(f"{'='*60}")
        
        spec_name = "test-state-management"
        self.spec_name = spec_name
        
        # Create spec
        result = self.run_script('new-spec.py', spec_name, "Test state management")
        self.assertEqual(result.returncode, 0, "new-spec.py should succeed")
        
        spec_path = os.path.join(self.test_base_dir, 'specs', spec_name)
        
        # Create tasks
        self.create_simple_tasks_file(spec_path)
        
        # Run partial execution (3 tasks)
        for i in range(3):
            result = self.run_script('coordinator.py', spec_name, check=False)
            if 'SPEC_COMPLETE' in result.stdout:
                break
            self.assertIn('CYCLE_COMPLETE', result.stdout, "Should complete cycle")
        
        # Verify state file updates
        state = self.read_state(spec_path)
        self.assertIsNotNone(state, "State file should exist")
        self.assertEqual(state['name'], spec_name, "State name should match")
        self.assertEqual(state['phase'], 'execution', "Phase should be execution")
        self.assertGreater(state['taskIndex'], 0, "Task index should advance")
        self.assertEqual(state['totalTasks'], 5, "Total tasks should be 5")
        
        # Verify progress file
        progress = self.read_progress(spec_path)
        self.assertIsNotNone(progress, "Progress file should exist")
        self.assertIn('Completed Tasks', progress, "Should have completed tasks")
        
        # Complete remaining tasks
        max_cycles = 10
        cycle = 0
        
        while cycle < max_cycles:
            result = self.run_script('coordinator.py', spec_name, check=False)
            
            if 'SPEC_COMPLETE' in result.stdout:
                break
            
            if 'CYCLE_COMPLETE' not in result.stdout:
                self.fail("Coordinator should output CYCLE_COMPLETE or SPEC_COMPLETE")
            
            cycle += 1
        
        # Verify state file deleted on completion
        state_file = os.path.join(spec_path, '.ralph-state.json')
        self.assertFalse(os.path.exists(state_file), "State file should be deleted on completion")
        
        # Progress file should remain
        progress_file = os.path.join(spec_path, '.progress.md')
        self.assertTrue(os.path.exists(progress_file), "Progress file should remain")
        
        print("✓ State file management test passed")
    
    def test_06_file_verification(self):
        """Test 6: Verify created files have correct content."""
        print(f"\n{'='*60}")
        print("TEST 6: File Verification")
        print(f"{'='*60}")
        
        spec_name = "test-file-verification"
        self.spec_name = spec_name
        
        # Create spec
        result = self.run_script('new-spec.py', spec_name, "Test file verification")
        self.assertEqual(result.returncode, 0, "new-spec.py should succeed")
        
        spec_path = os.path.join(self.test_base_dir, 'specs', spec_name)
        
        # Create tasks
        self.create_simple_tasks_file(spec_path)
        
        # Run to completion
        while True:
            result = self.run_script('coordinator.py', spec_name, check=False)
            if 'SPEC_COMPLETE' in result.stdout:
                break
            self.assertIn('CYCLE_COMPLETE', result.stdout, "Should complete cycle")
        
        # Verify calculator.py has add function
        calc_path = os.path.join(spec_path, 'calculator.py')
        with open(calc_path, 'r') as f:
            calc_content = f.read()
        self.assertIn('def add(a, b):', calc_content, "calculator.py should have add function")
        self.assertIn('return a + b', calc_content, "calculator.py should return a + b")
        
        # Verify multiplier.py has multiply function
        mult_path = os.path.join(spec_path, 'multiplier.py')
        with open(mult_path, 'r') as f:
            mult_content = f.read()
        self.assertIn('def multiply(a, b):', mult_content, "multiplier.py should have multiply function")
        self.assertIn('return a * b', mult_content, "multiplier.py should return a * b")
        
        # Verify README.md
        readme_path = os.path.join(spec_path, 'README.md')
        with open(readme_path, 'r') as f:
            readme_content = f.read()
        self.assertIn('Calculator', readme_content, "README should mention Calculator")
        
        # Verify files are executable
        for file in ['calculator.py', 'multiplier.py']:
            file_path = os.path.join(spec_path, file)
            # Test that Python can import the file
            import_result = subprocess.run(
                ['python', '-c', f'import sys; sys.path.insert(0, "{spec_path}"); import {file[:-3]}'],
                capture_output=True,
                text=True
            )
            self.assertEqual(import_result.returncode, 0, f"{file} should be importable")
        
        print("✓ File verification test passed")
    
    def test_07_git_commit_discipline(self):
        """Test 7: Verify git commit discipline (one commit per task)."""
        print(f"\n{'='*60}")
        print("TEST 7: Git Commit Discipline")
        print(f"{'='*60}")
        
        spec_name = "test-git-discipline"
        self.spec_name = spec_name
        
        # Create spec
        result = self.run_script('new-spec.py', spec_name, "Test git discipline")
        self.assertEqual(result.returncode, 0, "new-spec.py should succeed")
        
        spec_path = os.path.join(self.test_base_dir, 'specs', spec_name)
        
        # Create tasks
        self.create_simple_tasks_file(spec_path)
        
        # Run to completion
        while True:
            result = self.run_script('coordinator.py', spec_name, check=False)
            if 'SPEC_COMPLETE' in result.stdout:
                break
            self.assertIn('CYCLE_COMPLETE', result.stdout, "Should complete cycle")
        
        # Get all commits
        commits = self.get_git_commits(spec_path)
        
        # Should have at least 5 commits (one per task)
        self.assertGreaterEqual(len(commits), 5, f"Should have at least 5 commits, got {len(commits)}")
        
        # Verify each commit has conventional commit format
        for commit in commits:
            # Format: "hash: feat(scope): message"
            self.assertRegex(commit, r'^[a-f0-9]+:\s+(feat|fix|chore|docs|refactor|test|config)\(.+\):', 
                           f"Commit '{commit}' should follow conventional commit format")
        
        # Verify commit messages match task commit fields
        commit_messages = ' '.join(commits).lower()
        self.assertIn('add(a, b)', commit_messages, "Should commit add function")
        self.assertIn('multiply(a, b)', commit_messages, "Should commit multiply function")
        
        # Verify tasks.md is committed with each task
        # Check that tasks.md history shows updates
        result = subprocess.run(
            ['git', 'log', '--oneline', '--', 'tasks.md'],
            capture_output=True,
            text=True,
            cwd=spec_path
        )
        tasks_commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
        self.assertGreater(len(tasks_commits), 0, "tasks.md should have commit history")
        
        print("✓ Git commit discipline test passed")
    
    def test_08_progress_file_updates(self):
        """Test 8: Verify progress file is updated correctly."""
        print(f"\n{'='*60}")
        print("TEST 8: Progress File Updates")
        print(f"{'='*60}")
        
        spec_name = "test-progress-updates"
        self.spec_name = spec_name
        
        # Create spec
        result = self.run_script('new-spec.py', spec_name, "Test progress updates")
        self.assertEqual(result.returncode, 0, "new-spec.py should succeed")
        
        spec_path = os.path.join(self.test_base_dir, 'specs', spec_name)
        
        # Create tasks
        self.create_simple_tasks_file(spec_path)
        
        # Run 2 tasks
        for i in range(2):
            result = self.run_script('coordinator.py', spec_name, check=False)
            if 'SPEC_COMPLETE' in result.stdout:
                break
            self.assertIn('CYCLE_COMPLETE', result.stdout, "Should complete cycle")
        
        # Check progress file
        progress = self.read_progress(spec_path)
        self.assertIsNotNone(progress, "Progress file should exist")
        
        # Should have completed tasks
        self.assertIn('## Completed Tasks', progress, "Should have completed tasks section")
        
        # Should have at least 2 completed tasks
        completed_tasks = re.findall(r'- \[x\]', progress)
        self.assertGreaterEqual(len(completed_tasks), 2, f"Should have at least 2 completed tasks, got {len(completed_tasks)}")
        
        # Should have commit hashes
        self.assertRegex(progress, r'- \[x\].+- [a-f0-9]{7}', 
                        "Completed tasks should have commit hashes")
        
        # Complete remaining tasks
        while True:
            result = self.run_script('coordinator.py', spec_name, check=False)
            if 'SPEC_COMPLETE' in result.stdout:
                break
            self.assertIn('CYCLE_COMPLETE', result.stdout, "Should complete cycle")
        
        # Final progress should have all tasks
        progress = self.read_progress(spec_path)
        completed_tasks = re.findall(r'- \[x\]', progress)
        self.assertEqual(len(completed_tasks), 5, f"Should have 5 completed tasks, got {len(completed_tasks)}")
        
        print("✓ Progress file updates test passed")


def run_integration_tests():
    """Run all integration tests."""
    print(f"\n{'='*70}")
    print("RALPH INTEGRATION TEST SUITE")
    print(f"{'='*70}")
    print("\nThis will test:")
    print("  1. Full spec creation and execution workflow")
    print("  2. Parallel task execution")
    print("  3. Error handling and recovery")
    print("  4. State file management")
    print("  5. File verification")
    print("  6. Git commit discipline")
    print("  7. Progress file updates")
    print()
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(RalphIntegrationTest)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\n{'='*70}")
    if result.wasSuccessful():
        print("ALL INTEGRATION TESTS PASSED ✓")
    else:
        print("SOME INTEGRATION TESTS FAILED ✗")
        # Keep workspace for inspection if tests failed
        RalphIntegrationTest._keep_on_failure = True
    print(f"{'='*70}\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_integration_tests()
    sys.exit(0 if success else 1)
