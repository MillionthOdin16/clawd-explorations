#!/usr/bin/env python3
"""
Test Suite for Ralph Wiggum Loop Framework

Tests the core components:
1. Stop Hook
2. Feedback Formatter
3. Verification Runner
4. Infinite Loop Detector
5. Full Ralph Loop execution
"""

import asyncio
import pytest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ralph import (
    RalphConfig,
    RalphLoop,
    StopHook,
    FeedbackFormatter,
    VerificationRunner,
    InfiniteLoopDetector,
    RalphResult,
    FeedbackType
)


class TestStopHook:
    """Test the Stop Hook component"""
    
    def test_no_promise_blocks_exit(self):
        """Output without promise should block exit"""
        config = RalphConfig(task="Test task", promise="Tests pass")
        hook = StopHook(config)
        
        output = "I worked on the task but didn't finish"
        context = {}
        
        should_exit, reason = hook.check(output, context)
        
        assert should_exit == False
        assert "No completion promise" in reason
    
    def test_promise_without_verification_blocks_exit(self):
        """Promise present but verification failed should block exit"""
        config = RalphConfig(task="Test task", promise="Tests pass")
        hook = StopHook(config)
        
        output = "I tried to complete the task <promise>Tests pass</promise>"
        context = {"verification": {"passed": False, "failures": ["Test X failed"]}}
        
        should_exit, reason = hook.check(output, context)
        
        assert should_exit == False
        assert "Promise not fulfilled" in reason
    
    def test_promise_with_verification_allows_exit(self):
        """Promise with successful verification allows exit"""
        config = RalphConfig(task="Test task", promise="Tests pass")
        hook = StopHook(config)
        
        output = "Task completed <promise>Tests pass</promise>"
        context = {"verification": {"passed": True, "failures": []}}
        
        should_exit, reason = hook.check(output, context)
        
        assert should_exit == True
        assert "fulfilled" in reason
    
    def test_custom_promise_matching(self):
        """Custom promise should be matched correctly"""
        config = RalphConfig(task="Test task", promise="Build succeeds")
        hook = StopHook(config)
        
        # Should match the exact promise
        output = "Done! <promise>Build succeeds</promise>"
        context = {"verification": {"passed": True}}
        
        should_exit, _ = hook.check(output, context)
        
        assert should_exit == True


class TestFeedbackFormatter:
    """Test the Feedback Formatter component"""
    
    def test_format_iteration(self):
        """Test iteration feedback formatting"""
        config = RalphConfig(
            task="Fix the bug",
            promise="All tests pass",
            feedback=FeedbackType.ERRORS
        )
        formatter = FeedbackFormatter(config)
        
        feedback = formatter.format(
            iteration=0,
            output="Some code with errors\nError: TypeError in line 5",
            verification={"passed": False, "failures": ["TypeError in line 5"]},
            hint="Check the type of variable"
        )
        
        assert "ITERATION 1" in feedback
        assert "PREVIOUS OUTPUT" in feedback
        assert "VERIFICATION RESULT" in feedback
        assert "Fix the bug" in feedback  # Task name (case sensitive from input)
        assert "All tests pass" in feedback  # Promise
    
    def test_extract_errors(self):
        """Test error extraction from output"""
        config = RalphConfig(task="Test", feedback=FeedbackType.ERRORS)
        formatter = FeedbackFormatter(config)
        
        output = """
        Here's my code:
        Error: TypeError: undefined is not a function
        Another error: ValueError: invalid value
        """
        
        errors = formatter._extract_errors(output)
        
        assert "TypeError" in errors
        assert "ValueError" in errors


class TestInfiniteLoopDetector:
    """Test the Infinite Loop Detector component"""
    
    def test_no_loop_detected(self):
        """Different outputs should not trigger loop detection"""
        detector = InfiniteLoopDetector(history_threshold=3)
        
        for i in range(3):
            is_stuck, _ = detector.check(f"Different output {i}")
            assert is_stuck == False
    
    def test_identical_outputs_detected(self):
        """Identical outputs should trigger loop detection"""
        detector = InfiniteLoopDetector(history_threshold=3)
        
        # Same output multiple times
        for i in range(3):
            detector.check("Identical output")
        
        is_stuck, reason = detector.check("Identical output")
        
        assert is_stuck == True
        assert "Identical output" in reason


class TestVerificationRunner:
    """Test the Verification Runner component"""
    
    @pytest.mark.asyncio
    async def test_has_errors_detection(self):
        """Test that errors are detected in output"""
        config = RalphConfig(task="Test")
        runner = VerificationRunner(config)
        
        output_with_errors = "Error: Something failed\nTypeError: bad things"
        
        has_errors = runner._has_errors(output_with_errors)
        
        assert has_errors == True
    
    @pytest.mark.asyncio
    async def test_clean_output_no_errors(self):
        """Test that clean output has no errors"""
        config = RalphConfig(task="Test")
        runner = VerificationRunner(config)
        
        clean_output = "All tests passed successfully! Great job!"
        
        has_errors = runner._has_errors(clean_output)
        
        assert has_errors == False


class TestRalphConfig:
    """Test configuration options"""
    
    def test_default_values(self):
        """Test default configuration values"""
        config = RalphConfig(task="Test task")
        
        assert config.promise == "All tests pass"
        assert config.max_iterations == 10
        assert config.verbose == False
        assert config.feedback == FeedbackType.ERRORS
        assert config.max_cost == 100.0
    
    def test_custom_values(self):
        """Test custom configuration values"""
        config = RalphConfig(
            task="Custom task",
            promise="Build succeeds",
            max_iterations=20,
            verbose=True,
            timeout=600
        )
        
        assert config.task == "Custom task"
        assert config.promise == "Build succeeds"
        assert config.max_iterations == 20
        assert config.verbose == True
        assert config.timeout == 600


class TestRalphResult:
    """Test result dataclass"""
    
    def test_success_result(self):
        """Test successful result creation"""
        result = RalphResult(
            success=True,
            iterations=5,
            total_time=120.5,
            cost=15.75,
            final_output="Task completed"
        )
        
        assert result.success == True
        assert result.iterations == 5
        assert result.total_time == 120.5
        assert result.cost == 15.75
        
        # Test to_dict
        result_dict = result.to_dict()
        assert result_dict["success"] == True
        assert result_dict["iterations"] == 5
    
    def test_failure_result(self):
        """Test failure result creation"""
        result = RalphResult(
            success=False,
            iterations=10,
            total_time=300.0,
            cost=50.0,
            final_output="",
            error="Max iterations reached"
        )
        
        assert result.success == False
        assert result.error == "Max iterations reached"


class TestFeedbackTypes:
    """Test different feedback type behaviors"""
    
    def test_errors_feedback(self):
        """Test errors feedback type"""
        config = RalphConfig(task="Test", feedback=FeedbackType.ERRORS)
        
        assert config.feedback == FeedbackType.ERRORS
    
    def test_diff_feedback(self):
        """Test diff feedback type"""
        config = RalphConfig(task="Test", feedback=FeedbackType.DIFF)
        
        assert config.feedback == FeedbackType.DIFF
    
    def test_full_feedback(self):
        """Test full feedback type"""
        config = RalphConfig(task="Test", feedback=FeedbackType.FULL)
        
        assert config.feedback == FeedbackType.FULL


# Integration tests
class TestIntegration:
    """Integration tests for the full loop"""
    
    @pytest.mark.asyncio
    async def test_loop_max_iterations(self):
        """Test that loop respects max iterations"""
        config = RalphConfig(
            task="Impossible task",
            max_iterations=3,
            promise="Tests pass"
        )
        
        loop = RalphLoop(config)
        result = await loop.run()
        
        assert result.success == False
        assert result.iterations <= 3
        assert "Max iterations" in result.error


def run_tests():
    """Run all tests"""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_tests()
