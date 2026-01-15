#!/usr/bin/env python3
"""
Simple verification test for Ralph Loop core components
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ralph import RalphConfig, StopHook, FeedbackFormatter, InfiniteLoopDetector

def test_stop_hook():
    """Test Stop Hook functionality"""
    print("Testing Stop Hook...")
    
    # Test 1: No promise blocks exit
    config = RalphConfig(task="Test")
    hook = StopHook(config)
    
    output = "Task completed"
    context = {}
    should_exit, reason = hook.check(output, context)
    
    assert should_exit == False, "Should block exit without promise"
    print("  ✓ No promise blocks exit")
    
    # Test 2: Promise with verification allows exit
    output = "Task completed <promise>All tests pass</promise>"
    context = {"verification": {"passed": True, "failures": []}}
    should_exit, reason = hook.check(output, context)
    
    assert should_exit == True, "Should allow exit with promise and verification"
    print("  ✓ Promise with verification allows exit")
    
    # Test 3: Promise without verification blocks exit
    output = "Task completed <promise>All tests pass</promise>"
    context = {"verification": {"passed": False, "failures": ["Test failed"]}}
    should_exit, reason = hook.check(output, context)
    
    assert should_exit == False, "Should block exit with failed verification"
    print("  ✓ Promise without verification blocks exit")
    
    print("Stop Hook tests: PASSED ✓\n")

def test_feedback_formatter():
    """Test Feedback Formatter functionality"""
    print("Testing Feedback Formatter...")
    
    config = RalphConfig(
        task="Fix the bug",
        promise="All tests pass",
        feedback="errors"
    )
    formatter = FeedbackFormatter(config)
    
    # Test formatting
    feedback = formatter.format(
        iteration=0,
        output="Error: TypeError in line 5",
        verification={"passed": False, "failures": ["TypeError"]},
        hint="Check the type"
    )
    
    assert "ITERATION 1" in feedback
    assert "PREVIOUS OUTPUT" in feedback
    assert "VERIFICATION RESULT" in feedback
    print("  ✓ Iteration formatting works")
    
    # Test error extraction
    output = "Some code\nError: TypeError: undefined is not a function\nDone"
    errors = formatter._extract_errors(output)
    
    assert "TypeError" in errors
    print("  ✓ Error extraction works")
    
    print("Feedback Formatter tests: PASSED ✓\n")

def test_infinite_loop_detector():
    """Test Infinite Loop Detector"""
    print("Testing Infinite Loop Detector...")
    
    detector = InfiniteLoopDetector(history_threshold=3)
    
    # Test 1: Different outputs don't trigger
    for i in range(3):
        is_stuck, _ = detector.check(f"Output {i}")
        assert is_stuck == False
    print("  ✓ Different outputs don't trigger detection")
    
    # Test 2: Identical outputs trigger detection
    for i in range(3):
        detector.check("Same output")
    
    is_stuck, reason = detector.check("Same output")
    assert is_stuck == True
    assert "Identical output" in reason
    print("  ✓ Identical outputs trigger detection")
    
    print("Infinite Loop Detector tests: PASSED ✓\n")

def test_config():
    """Test configuration"""
    print("Testing Configuration...")
    
    # Test defaults
    config = RalphConfig(task="Test")
    assert config.promise == "All tests pass"
    assert config.max_iterations == 10
    assert config.verbose == False
    print("  ✓ Default configuration works")
    
    # Test custom values
    config = RalphConfig(
        task="Custom task",
        promise="Build succeeds",
        max_iterations=20,
        verbose=True
    )
    assert config.task == "Custom task"
    assert config.promise == "Build succeeds"
    assert config.max_iterations == 20
    assert config.verbose == True
    print("  ✓ Custom configuration works")
    
    print("Configuration tests: PASSED ✓\n")

def main():
    """Run all tests"""
    print("=" * 60)
    print("RALPH WIGGUM LOOP - VERIFICATION TESTS")
    print("=" * 60)
    print()
    
    try:
        test_stop_hook()
        test_feedback_formatter()
        test_infinite_loop_detector()
        test_config()
        
        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
