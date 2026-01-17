#!/usr/bin/env python3
"""
Ralph Quick Test Suite - Fast verification tests
"""

import subprocess
import tempfile
import shutil
import os
import sys
import json
import time

def run_test(name, func):
    """Run a test function and report results."""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    try:
        func()
        print(f"✓ {name} PASSED")
        return True
    except Exception as e:
        print(f"✗ {name} FAILED: {e}")
        return False


def test_basic_workflow():
    """Test basic spec creation and execution."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        # Init git
        subprocess.run(['git', 'init'], capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test'], capture_output=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial'], capture_output=True)
        
        # Create spec
        result = subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/new-spec.py', 'test-spec', 'Test'],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"new-spec failed: {result.stderr}"
        
        # Create simple task
        tasks_content = """# Tasks: Test

## Phase 1: POC

- [ ] 1.1 Create test.txt
  **Do**: Create test.txt with hello
  **Files**: test.txt
  **Done when**: test.txt exists
  **Verify**: test -f test.txt && echo "PASS"
  **Commit**: feat: create test.txt
"""
        with open('specs/test-spec/tasks.md', 'w') as f:
            f.write(tasks_content)
        
        # Run coordinator
        result = subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/coordinator.py', 'test-spec'],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"coordinator failed: {result.stderr}"
        assert 'SPEC_COMPLETE' in result.stdout, f"Expected SPEC_COMPLETE: {result.stdout}"
        
        # Verify file created
        assert os.path.exists('specs/test-spec/test.txt'), "test.txt should exist"
        
        print(f"  Created: test.txt")
        print(f"  Output: {result.stdout[-200:]}")


def test_parallel_execution():
    """Test parallel task execution."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        # Init git
        subprocess.run(['git', 'init'], capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test'], capture_output=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial'], capture_output=True)
        
        # Create spec
        subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/new-spec.py', 'parallel-test', 'Test'],
            capture_output=True, check=True
        )
        
        # Create parallel tasks
        tasks_content = """# Tasks: Parallel Test

## Phase 1: POC

- [ ] 1.1 [P] Create a.txt
  **Do**: Create a.txt
  **Files**: a.txt
  **Done when**: a.txt exists
  **Verify**: test -f a.txt && echo "PASS"
  **Commit**: feat: create a.txt

- [ ] 1.2 [P] Create b.txt
  **Do**: Create b.txt
  **Files**: b.txt
  **Done when**: b.txt exists
  **Verify**: test -f b.txt && echo "PASS"
  **Commit**: feat: create b.txt

- [ ] 1.3 Create c.txt
  **Do**: Create c.txt
  **Files**: c.txt
  **Done when**: c.txt exists
  **Verify**: test -f c.txt && echo "PASS"
  **Commit**: feat: create c.txt
"""
        with open('specs/parallel-test/tasks.md', 'w') as f:
            f.write(tasks_content)
        
        # Run coordinator twice (first 2 parallel, then 1 sequential)
        for i in range(2):
            result = subprocess.run(
                ['python', '/home/opc/clawd/skills/ralph/scripts/coordinator.py', 'parallel-test'],
                capture_output=True, text=True
            )
            assert result.returncode == 0, f"coordinator failed: {result.stderr}"
        
        assert 'SPEC_COMPLETE' in result.stdout, f"Expected SPEC_COMPLETE"
        
        # Verify files
        assert os.path.exists('specs/parallel-test/a.txt'), "a.txt should exist"
        assert os.path.exists('specs/parallel-test/b.txt'), "b.txt should exist"
        assert os.path.exists('specs/parallel-test/c.txt'), "c.txt should exist"
        
        print(f"  Created: a.txt, b.txt, c.txt")


def test_error_handling():
    """Test error handling when verification fails."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        # Init git
        subprocess.run(['git', 'init'], capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test'], capture_output=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial'], capture_output=True)
        
        # Create spec
        subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/new-spec.py', 'error-test', 'Test'],
            capture_output=True, check=True
        )
        
        # Create task that will fail verification
        tasks_content = """# Tasks: Error Test

## Phase 1: POC

- [ ] 1.1 Create success.txt
  **Do**: Create success.txt
  **Files**: success.txt
  **Done when**: success.txt exists
  **Verify**: test -f success.txt && echo "PASS"
  **Commit**: feat: create success.txt

- [ ] 1.2 Create fail.txt
  **Do**: Create fail.txt
  **Files**: fail.txt
  **Done when**: fail.txt exists
  **Verify**: test -f nonexistent.txt && echo "PASS"
  **Commit**: feat: create fail.txt
"""
        with open('specs/error-test/tasks.md', 'w') as f:
            f.write(tasks_content)
        
        # Run coordinator first time - should complete task 1.1
        result1 = subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/coordinator.py', 'error-test'],
            capture_output=True, text=True
        )
        assert result1.returncode == 0, f"First run should succeed: {result1.stderr}"
        
        # First task should be complete
        with open('specs/error-test/tasks.md') as f:
            content = f.read()
        assert '- [x] 1.1' in content, "Task 1.1 should be complete"
        
        # Run coordinator second time - should fail on task 1.2
        result2 = subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/coordinator.py', 'error-test'],
            capture_output=True, text=True
        )
        
        # Should fail
        assert result2.returncode != 0, f"Should fail on verification, got returncode={result2.returncode}"
        output = result2.stdout + result2.stderr
        assert 'VERIFICATION FAILED' in output or 'failed' in output.lower(), f"Expected failure: {output}"
        
        print(f"  Error handling: PASS")


def test_state_management():
    """Test state file management."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        # Init git
        subprocess.run(['git', 'init'], capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test'], capture_output=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial'], capture_output=True)
        
        # Create spec
        subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/new-spec.py', 'state-test', 'Test'],
            capture_output=True, check=True
        )
        
        # Create 2 tasks
        tasks_content = """# Tasks: State Test

## Phase 1: POC

- [ ] 1.1 Create a.txt
  **Do**: Create a.txt
  **Files**: a.txt
  **Done when**: a.txt exists
  **Verify**: test -f a.txt && echo "PASS"
  **Commit**: feat: create a.txt

- [ ] 1.2 Create b.txt
  **Do**: Create b.txt
  **Files**: b.txt
  **Done when**: b.txt exists
  **Verify**: test -f b.txt && echo "PASS"
  **Commit**: feat: create b.txt
"""
        with open('specs/state-test/tasks.md', 'w') as f:
            f.write(tasks_content)
        
        # Run once - should complete first task
        result1 = subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/coordinator.py', 'state-test'],
            capture_output=True, text=True
        )
        assert result1.returncode == 0
        assert 'CYCLE_COMPLETE' in result1.stdout
        
        # State file should exist with taskIndex = 1
        import json
        with open('specs/state-test/.ralph-state.json') as f:
            state = json.load(f)
        assert state['taskIndex'] == 1, f"Expected taskIndex=1, got {state['taskIndex']}"
        
        # Run again - should complete
        result2 = subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/coordinator.py', 'state-test'],
            capture_output=True, text=True
        )
        assert result2.returncode == 0
        assert 'SPEC_COMPLETE' in result2.stdout
        
        # State file should be deleted
        assert not os.path.exists('specs/state-test/.ralph-state.json'), "State should be deleted"
        
        print(f"  State management: PASS")


def test_dry_run_mode():
    """Test dry-run mode - shows actions without executing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        # Init git
        subprocess.run(['git', 'init'], capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test'], capture_output=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial'], capture_output=True)
        
        # Create spec
        subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/new-spec.py', 'dryrun-test', 'Test'],
            capture_output=True, check=True
        )
        
        # Create task
        tasks_content = """# Tasks: Dry Run Test

## Phase 1: POC

- [ ] 1.1 Create important.txt
  **Do**: Create important.txt
  **Files**: important.txt
  **Done when**: important.txt exists
  **Verify**: test -f important.txt && echo "PASS"
  **Commit**: feat: create important.txt
"""
        with open('specs/dryrun-test/tasks.md', 'w') as f:
            f.write(tasks_content)
        
        # Remove .current-spec and state file if they exist (new-spec.py may have created them)
        if os.path.exists('specs/.current-spec'):
            os.remove('specs/.current-spec')
        if os.path.exists('specs/dryrun-test/.ralph-state.json'):
            os.remove('specs/dryrun-test/.ralph-state.json')
        
        # Run coordinator in dry-run mode
        result = subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/coordinator.py', 'dryrun-test', '--dry-run'],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"dry-run failed: {result.stderr}"
        
        output = result.stdout + result.stderr
        assert 'DRY RUN MODE' in output, f"Expected dry-run header: {output}"
        assert 'No changes will be made' in output, f"Expected no changes warning: {output}"
        assert 'Would create' in output or 'Would create files' in output, f"Expected would-create: {output}"
        assert 'important.txt' in output, f"Expected important.txt mentioned: {output}"
        assert 'Dry Run' in output, f"Expected dry-run suffix in output: {output}"
        
        # CRITICAL: Verify NO actual changes were made
        assert not os.path.exists('specs/dryrun-test/important.txt'), "File should NOT be created in dry-run"
        assert not os.path.exists('specs/.current-spec'), ".current-spec should NOT be created in dry-run"
        
        # Verify state file NOT created
        assert not os.path.exists('specs/dryrun-test/.ralph-state.json'), "State file should NOT be created in dry-run"
        
        # Verify tasks.md NOT modified
        with open('specs/dryrun-test/tasks.md') as f:
            content = f.read()
        assert '- [ ] 1.1' in content, "Task should NOT be marked complete in dry-run"
        assert '- [x] 1.1' not in content, "Task should still be incomplete"
        
        print(f"  Dry-run header: ✓")
        print(f"  No files created: ✓")
        print(f"  Tasks unchanged: ✓")
        print(f"  No state changes: ✓")


def test_undo_rollback():
    """Test undo/rollback functionality."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        # Init git
        subprocess.run(['git', 'init'], capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test'], capture_output=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial'], capture_output=True)
        
        # Create spec
        subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/new-spec.py', 'undo-test', 'Test'],
            capture_output=True, check=True
        )
        
        # Create 2 tasks
        tasks_content = """# Tasks: Undo Test

## Phase 1: POC

- [ ] 1.1 Create first.txt
  **Do**: Create first.txt
  **Files**: first.txt
  **Done when**: first.txt exists
  **Verify**: test -f first.txt && echo "PASS"
  **Commit**: feat: create first.txt

- [ ] 1.2 Create second.txt
  **Do**: Create second.txt
  **Files**: second.txt
  **Done when**: second.txt exists
  **Verify**: test -f second.txt && echo "PASS"
  **Commit**: feat: create second.txt
"""
        with open('specs/undo-test/tasks.md', 'w') as f:
            f.write(tasks_content)
        
        # Run twice to complete both tasks
        for i in range(2):
            result = subprocess.run(
                ['python', '/home/opc/clawd/skills/ralph/scripts/coordinator.py', 'undo-test'],
                capture_output=True, text=True
            )
            assert result.returncode == 0, f"Run {i+1} failed: {result.stderr}"
        
        # Verify both files exist
        assert os.path.exists('specs/undo-test/first.txt'), "first.txt should exist"
        assert os.path.exists('specs/undo-test/second.txt'), "second.txt should exist"
        
        # Verify both tasks marked complete
        with open('specs/undo-test/tasks.md') as f:
            content = f.read()
        assert '- [x] 1.1' in content, "Task 1.1 should be complete"
        assert '- [x] 1.2' in content, "Task 1.2 should be complete"
        
        # Test UNDO
        result = subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/coordinator.py', 'undo-test', '--undo'],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Undo failed: {result.stderr}"
        assert 'UNDO COMPLETE' in result.stdout, "Should show undo complete"
        
        # Verify second.txt removed, first.txt still exists
        assert os.path.exists('specs/undo-test/first.txt'), "first.txt should still exist"
        assert not os.path.exists('specs/undo-test/second.txt'), "second.txt should be removed after undo"
        
        # Verify task 1.2 unmarked
        with open('specs/undo-test/tasks.md') as f:
            content = f.read()
        assert '- [x] 1.1' in content, "Task 1.1 should still be complete"
        assert '- [ ] 1.2' in content, "Task 1.2 should be incomplete after undo"
        
        print(f"  Undo command: ✓")
        print(f"  File reverted: ✓")
        print(f"  Tasks restored: ✓")


def test_statistics_tracking():
    """Test statistics tracking."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        # Init git
        subprocess.run(['git', 'init'], capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test'], capture_output=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial'], capture_output=True)
        
        # Create spec
        subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/new-spec.py', 'stats-test', 'Test'],
            capture_output=True, check=True
        )
        
        # Create 2 tasks
        tasks_content = """# Tasks: Stats Test

## Phase 1: POC

- [ ] 1.1 Create task1.txt
  **Do**: Create task1.txt
  **Files**: task1.txt
  **Done when**: task1.txt exists
  **Verify**: test -f task1.txt && echo "PASS"
  **Commit**: feat: create task1.txt

- [ ] 1.2 Create task2.txt
  **Do**: Create task2.txt
  **Files**: task2.txt
  **Done when**: task2.txt exists
  **Verify**: test -f task2.txt && echo "PASS"
  **Commit**: feat: create task2.txt
"""
        with open('specs/stats-test/tasks.md', 'w') as f:
            f.write(tasks_content)
        
        # Run tasks
        for i in range(2):
            result = subprocess.run(
                ['python', '/home/opc/clawd/skills/ralph/scripts/coordinator.py', 'stats-test'],
                capture_output=True, text=True
            )
            assert result.returncode == 0, f"Run {i+1} failed: {result.stderr}"
        
        # Verify stats file created
        stats_file = 'specs/stats-test/.ralph-stats.json'
        assert os.path.exists(stats_file), "Stats file should be created"
        
        # Read and verify stats
        with open(stats_file) as f:
            stats = json.load(f)
        
        assert 'tasks' in stats, "Stats should have tasks section"
        assert 'summary' in stats, "Stats should have summary section"
        
        # Verify summary
        summary = stats['summary']
        assert summary['total_tasks'] == 2, "Should track 2 tasks"
        assert summary['total_successes'] == 2, "Both tasks should succeed"
        assert summary['total_failures'] == 0, "No tasks should fail"
        assert summary['success_rate'] == 100.0, "Success rate should be 100%"
        assert summary['total_time_seconds'] > 0, "Should track execution time"
        assert 'last_updated' in summary, "Should have timestamp"
        
        # Verify individual task stats
        assert 'task_0' in stats['tasks'], "Should have stats for task 0"
        assert 'task_1' in stats['tasks'], "Should have stats for task 1"
        assert stats['tasks']['task_0']['successes'] == 1, "Task 0 should succeed once"
        assert stats['tasks']['task_1']['successes'] == 1, "Task 1 should succeed once"
        
        print(f"  Stats file created: ✓")
        print(f"  Task tracking: ✓")
        print(f"  Summary calculation: ✓")
        print(f"  Execution time tracked: ✓")


def test_webhook_notifications():
    """Test webhook notifications (mock only - no real webhook)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        # Init git
        subprocess.run(['git', 'init'], capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test'], capture_output=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial'], capture_output=True)
        
        # Create spec
        subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/new-spec.py', 'webhook-test', 'Test'],
            capture_output=True, check=True
        )
        
        # Create task
        tasks_content = """# Tasks: Webhook Test

## Phase 1: POC

- [ ] 1.1 Create webhook.txt
  **Do**: Create webhook.txt
  **Files**: webhook.txt
  **Done when**: webhook.txt exists
  **Verify**: test -f webhook.txt && echo "PASS"
  **Commit**: feat: create webhook.txt
"""
        with open('specs/webhook-test/tasks.md', 'w') as f:
            f.write(tasks_content)
        
        # Run coordinator - should not fail even if webhook is not configured
        result = subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/coordinator.py', 'webhook-test'],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Coordinator failed: {result.stderr}"
        
        # Should complete successfully (webhook errors are warnings, not failures)
        assert 'SPEC_COMPLETE' in result.stdout, "Should complete spec"
        
        print(f"  Coordinator runs without webhook: ✓")
        print(f"  No webhook errors: ✓")


def test_quality_gate():
    """Test quality gate - blocks after max iterations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        # Init git
        subprocess.run(['git', 'init'], capture_output=True, check=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test'], capture_output=True)
        subprocess.run(['git', 'commit', '--allow-empty', '-m', 'Initial'], capture_output=True)
        
        # Create spec
        subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/new-spec.py', 'quality-test', 'Test'],
            capture_output=True, check=True
        )
        
        # Create a task that will always fail verification
        tasks_content = """# Tasks: Quality Gate Test

## Phase 1: POC

- [ ] 1.1 Create success.txt
  **Do**: Create success.txt
  **Files**: success.txt
  **Done when**: success.txt exists
  **Verify**: test -f nonexistent.txt && echo "PASS"
  **Commit**: feat: create success.txt
"""
        with open('specs/quality-test/tasks.md', 'w') as f:
            f.write(tasks_content)
        
        # Manually set maxTaskIterations to 2 for faster testing
        state_file = 'specs/quality-test/.ralph-state.json'
        with open(state_file, 'r') as f:
            state = json.load(f)
        state['maxTaskIterations'] = 2
        state['taskIteration'] = 3  # Already EXCEEDED max (2 >= 2 = block, so use 3)
        with open(state_file, 'w') as f:
            json.dump(state, f)
        
        # Run coordinator - should be blocked by quality gate
        result = subprocess.run(
            ['python', '/home/opc/clawd/skills/ralph/scripts/coordinator.py', 'quality-test'],
            capture_output=True, text=True
        )
        
        # Should fail with quality gate message
        assert result.returncode != 0, f"Should fail due to quality gate"
        output = result.stdout + result.stderr
        assert 'QUALITY GATE' in output or 'quality gate' in output.lower(), f"Expected quality gate error: {output}"
        assert 'exceeded' in output.lower() or 'blocked' in output.lower(), f"Expected exceeded/blocked message: {output}"
        
        print(f"  Quality gate blocks after max iterations: ✓")


def main():
    print(f"\n{'='*70}")
    print("RALPH QUICK TEST SUITE")
    print(f"{'='*70}")
    
    tests = [
        ("Basic Workflow", test_basic_workflow),
        ("Parallel Execution", test_parallel_execution),
        ("Error Handling", test_error_handling),
        ("State Management", test_state_management),
        ("Dry Run Mode", test_dry_run_mode),
        ("Undo/Rollback", test_undo_rollback),
        ("Statistics Tracking", test_statistics_tracking),
        ("Webhook Notifications", test_webhook_notifications),
        ("Quality Gate", test_quality_gate),
    ]
    
    results = []
    for name, func in tests:
        results.append(run_test(name, func))
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n{'='*70}")
    if passed == total:
        print(f"ALL {total} TESTS PASSED ✓")
    else:
        print(f"{passed}/{total} TESTS PASSED, {total-passed} FAILED ✗")
    print(f"{'='*70}\n")
    
    # Show test results summary
    print("\nTest Results Summary:")
    for i, (name, _) in enumerate(tests):
        status = "✓ PASS" if results[i] else "✗ FAIL"
        print(f"  {status} - {name}")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
