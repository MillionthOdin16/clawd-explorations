#!/usr/bin/env python3
"""
Ralph Wiggum Loop - Persistent Agent Framework

A framework for creating persistent, autonomous agents that iterate until
a specific completion condition is met.

Usage:
    python ralph.py "Your task here" [--options]
    
Options:
    --promise: Completion promise (default: "All tests pass")
    --max-iterations: Maximum iterations (default: 10)
    --verbose: Verbose output
    --dangerously-skip-permissions: Skip permission checks
    --sandbox: Run in sandboxed environment
    --timeout: Timeout per iteration (default: 300)
    --feedback: Feedback type (full, errors, diff)
"""

import asyncio
import argparse
import json
import os
import sys
import time
import hashlib
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

# ANSI colors for output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class FeedbackType(str, Enum):
    ERRORS = "errors"
    DIFF = "diff"
    FULL = "full"


@dataclass
class RalphConfig:
    """Configuration for Ralph Loop"""
    task: str
    promise: str = "All tests pass"
    max_iterations: int = 10
    verbose: bool = False
    skip_permissions: bool = False
    sandbox: bool = False
    timeout: int = 300
    feedback: FeedbackType = FeedbackType.ERRORS
    workdir: str = "."
    
    # Safety limits
    max_cost: float = 100.0  # dollars
    
    # Output
    output_file: Optional[str] = None


@dataclass
class RalphResult:
    """Result of Ralph Loop execution"""
    success: bool
    iterations: int
    total_time: float
    cost: float
    final_output: str
    error: Optional[str] = None
    
    def to_dict(self):
        return {
            "success": self.success,
            "iterations": self.iterations,
            "total_time": self.total_time,
            "cost": self.cost,
            "error": self.error,
            "timestamp": datetime.utcnow().isoformat()
        }


class StopHook:
    """
    The core Stop Hook that intercepts exit attempts.
    
    This is the key innovation of the Ralph Loop - it checks if the
    completion promise is actually met before allowing exit.
    """
    
    def __init__(self, config: RalphConfig):
        self.config = config
        self.exit_blocked_count = 0
        
    def check(self, output: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Check if exit should be blocked.
        
        Args:
            output: The agent's output
            context: Additional context (verification results, etc.)
            
        Returns:
            Tuple of (should_exit, reason)
        """
        # 1. Check for completion promise
        if not self._has_promise(output):
            self.exit_blocked_count += 1
            return False, "No completion promise found in output"
        
        # 2. Verify the promise conditions
        verified, reason = self._verify_promise(output, context)
        if not verified:
            self.exit_blocked_count += 1
            return False, f"Promise not fulfilled: {reason}"
        
        # 3. All checks passed
        return True, "Promise fulfilled"
    
    def _has_promise(self, output: str) -> bool:
        """Check if output contains the completion promise marker"""
        # Look for <promise>COMPLETE</promise> or custom promise
        promise_marker = f"<promise>{self.config.promise}</promise>"
        return promise_marker in output or "<promise>COMPLETE</promise>" in output
    
    def _verify_promise(self, output: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Verify that the promised completion condition is actually met.
        
        This is where we check actual verification results (tests, builds, etc.)
        """
        # Extract verification result from context
        verification_result = context.get("verification", {})
        
        if not verification_result:
            # If no verification, assume we need to run it
            return False, "No verification results available"
        
        # Check if verification passed
        if verification_result.get("passed") is True:
            return True, "Verification passed"
        
        # Get failure reason
        failures = verification_result.get("failures", [])
        if failures:
            return False, f"Verification failed: {'; '.join(failures)}"
        
        return False, "Verification status unknown"


class FeedbackFormatter:
    """Formats feedback from the previous iteration for the next"""
    
    def __init__(self, config: RalphConfig):
        self.config = config
        
    def format(self, iteration: int, output: str, 
               verification: Dict, hint: str) -> str:
        """
        Format feedback for the next iteration.
        
        Structure:
        ```
        === ITERATION N ===
        
        PREVIOUS OUTPUT:
        [Previous output]
        
        ERRORS/FEEDBACK:
        [Extracted errors]
        
        VERIFICATION RESULT:
        [Why the previous attempt failed]
        
        HINT:
        [Suggested approach]
        
        ===
        ```
        """
        lines = []
        lines.append("=" * 60)
        lines.append(f"ITERATION {iteration + 1} (Previous attempt feedback)")
        lines.append("=" * 60)
        lines.append("")
        
        # Previous output section
        lines.append("PREVIOUS OUTPUT:")
        lines.append("-" * 40)
        if self.config.feedback == FeedbackType.FULL:
            lines.append(output)
        elif self.config.feedback == FeedbackType.DIFF:
            lines.append(self._extract_diff(output))
        else:  # errors
            lines.append(self._extract_errors(output))
        lines.append("")
        
        # Verification result
        lines.append("VERIFICATION RESULT:")
        lines.append("-" * 40)
        if verification:
            if verification.get("passed"):
                lines.append("✅ PASSED")
            else:
                lines.append("❌ FAILED")
                for failure in verification.get("failures", []):
                    lines.append(f"  - {failure}")
        else:
            lines.append("No verification available")
        lines.append("")
        
        # Hint
        if hint:
            lines.append("HINT:")
            lines.append("-" * 40)
            lines.append(hint)
            lines.append("")
        
        lines.append("=" * 60)
        lines.append(f"TASK: {self.config.task}")
        lines.append(f"COMPLETION PROMISE: <promise>{self.config.promise}</promise>")
        lines.append("=" * 60)
        lines.append("")
        
        return "\n".join(lines)
    
    def _extract_errors(self, output: str) -> str:
        """Extract error messages from output"""
        errors = []
        
        # Common error patterns
        patterns = [
            r'Error[:\s]+([^\n]+)',
            r'error[:\s]+([^\n]+)',
            r'FAILED[:\s]+([^\n]+)',
            r'failed[:\s]+([^\n]+)',
            r'Traceback[^\n]*\n([^\n]*(?:Error|Exception)[^\n]*)',
            r'AssertionError[:\s]+([^\n]+)',
            r'TypeError[:\s]+([^\n]+)',
            r'ValueError[:\s]+([^\n]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, output, re.IGNORECASE | re.MULTILINE)
            errors.extend(matches)
        
        # Also look for test failure patterns
        test_failures = re.findall(r'FAIL:?\s*([^\n]+)', output)
        errors.extend(test_failures)
        
        if errors:
            return "\n".join(f"  {e.strip()}" for e in errors[:20])
        else:
            return "  No errors extracted (check full output)"
    
    def _extract_diff(self, output: str) -> str:
        """Extract git diff style changes"""
        diff_lines = []
        in_diff = False
        
        for line in output.split('\n'):
            if line.startswith('---') or line.startswith('+++'):
                in_diff = True
            elif in_diff and not line.startswith('@'):
                diff_lines.append(line)
            elif in_diff and line.startswith('@@'):
                diff_lines.append(line)
        
        if diff_lines:
            return "\n".join(diff_lines[:50])
        return self._extract_errors(output)


class VerificationRunner:
    """Runs verification commands to check promise fulfillment"""
    
    def __init__(self, config: RalphConfig):
        self.config = config
        
    async def verify(self, task_output: str) -> Dict[str, Any]:
        """
        Run verification based on the promise type.
        
        Returns:
            Dict with 'passed' (bool), 'failures' (list), and 'output' (str)
        """
        result = {
            "passed": False,
            "failures": [],
            "output": ""
        }
        
        # Determine what to verify based on promise
        promise_lower = self.config.promise.lower()
        
        # TypeScript/JavaScript verification
        if "typescript" in promise_lower or "tsc" in promise_lower:
            result = await self._verify_typescript()
        elif "eslint" in promise_lower or "lint" in promise_lower:
            result = await self._verify_linting()
        elif "test" in promise_lower or "pytest" in promise_lower or "jest" in promise_lower:
            result = await self._verify_tests()
        elif "build" in promise_lower or "compile" in promise_lower:
            result = await self._verify_build()
        elif "type check" in promise_lower:
            result = await self._verify_typescript()
        
        # Generic: check for error indicators in output
        if not result["passed"] and not result["failures"]:
            if self._has_errors(task_output):
                result["failures"].append("Errors found in output")
            else:
                # No errors found, assume success
                result["passed"] = True
                
        return result
    
    async def _verify_typescript(self) -> Dict:
        """Verify TypeScript compilation"""
        result = {"passed": False, "failures": [], "output": ""}
        
        try:
            proc = await asyncio.create_subprocess_exec(
                "npx", "tsc", "--noEmit",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.config.workdir
            )
            stdout, stderr = await proc.communicate()
            output = stdout.decode() + stderr.decode()
            
            result["output"] = output
            
            if proc.returncode == 0:
                result["passed"] = True
            else:
                # Parse TypeScript errors
                errors = re.findall(r'error TS\d+:[^\n]+', output)
                result["failures"].extend(errors[:10])
                
        except Exception as e:
            result["failures"].append(f"TypeScript verification failed: {str(e)}")
            
        return result
    
    async def _verify_tests(self) -> Dict:
        """Verify tests pass"""
        result = {"passed": False, "failures": [], "output": ""}
        
        try:
            # Try pytest first, then jest
            for test_cmd in [["pytest"], ["npx", "jest", "--passWithNoTests"]]:
                proc = await asyncio.create_subprocess_exec(
                    *test_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=self.config.workdir
                )
                stdout, stderr = await proc.communicate()
                output = stdout.decode() + stderr.decode()
                
                result["output"] = output
                
                if proc.returncode == 0:
                    result["passed"] = True
                    # Count tests
                    passed = re.findall(r'\d+ passed', output)
                    if passed:
                        result["message"] = passed[0]
                    break
                else:
                    # Parse test failures
                    failures = re.findall(r'FAILED\s+[^\n]+', output)
                    result["failures"].extend(failures[:10])
                    
        except Exception as e:
            result["failures"].append(f"Test verification failed: {str(e)}")
            
        return result
    
    async def _verify_linting(self) -> Dict:
        """Verify linting passes"""
        result = {"passed": False, "failures": [], "output": ""}
        
        try:
            for linter in [["npx", "eslint", "."], ["flake8"], ["pylint"]]:
                proc = await asyncio.create_subprocess_exec(
                    *linter,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=self.config.workdir
                )
                stdout, stderr = await proc.communicate()
                output = stdout.decode() + stderr.decode()
                
                result["output"] = output
                
                if proc.returncode == 0:
                    result["passed"] = True
                    break
                else:
                    # Parse lint errors
                    errors = re.findall(r'error[:\s]+[^\n]+', output)
                    result["failures"].extend(errors[:10])
                    
        except Exception as e:
            result["failures"].append(f"Lint verification failed: {str(e)}")
            
        return result
    
    async def _verify_build(self) -> Dict:
        """Verify build succeeds"""
        result = {"passed": False, "failures": [], "output": ""}
        
        try:
            for build_cmd in [["npm", "run", "build"], ["yarn", "build"], ["cargo", "build"]]:
                proc = await asyncio.create_subprocess_exec(
                    *build_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=self.config.workdir
                )
                stdout, stderr = await proc.communicate()
                output = stdout.decode() + stderr.decode()
                
                result["output"] = output
                
                if proc.returncode == 0:
                    result["passed"] = True
                    break
                else:
                    errors = re.findall(r'error[:\s]+[^\n]+', output)
                    result["failures"].extend(errors[:10])
                    
        except Exception as e:
            result["failures"].append(f"Build verification failed: {str(e)}")
            
        return result
    
    def _has_errors(self, output: str) -> bool:
        """Check if output contains error indicators"""
        error_patterns = [
            r'error[:\s]+[A-Z]',
            r'Error[:\s]+[A-Z]',
            r'FAILED',
            r'FAILURE',
            r'AssertionError',
            r'Traceback.*Error',
            r'TypeError',
            r'ValueError',
            r'ImportError',
            r'ReferenceError',
        ]
        
        for pattern in error_patterns:
            if re.search(pattern, output):
                return True
                
        return False


class InfiniteLoopDetector:
    """Detects infinite loop patterns"""
    
    def __init__(self, history_threshold: int = 5):
        self.history = []
        self.history_threshold = history_threshold
        
    def check(self, output: str) -> Tuple[bool, str]:
        """
        Check if we're stuck in an infinite loop.
        
        Returns:
            Tuple of (is_stuck, reason)
        """
        # Add output to history
        self.history.append(self._hash_output(output))
        
        # Keep only recent history
        if len(self.history) > self.history_threshold * 2:
            self.history = self.history[-self.history_threshold * 2:]
        
        # Check for identical outputs
        if len(self.history) >= self.history_threshold:
            recent = self.history[-self.history_threshold:]
            if len(set(recent)) == 1:
                return True, f"Identical output for {self.history_threshold} iterations"
        
        return False, ""
    
    def _hash_output(self, output: str) -> str:
        """Create a hash of the output for comparison"""
        # Normalize output by removing timestamps and noise
        normalized = re.sub(r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}[^\n]*', '', output)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return hashlib.md5(normalized.encode()).hexdigest()


class RalphLoop:
    """
    Main Ralph Wiggum Loop implementation.
    
    This class orchestrates the entire loop:
    1. Create agent session
    2. Run task
    3. Intercept exit with Stop Hook
    4. Format feedback
    5. Repeat until completion or limits reached
    """
    
    def __init__(self, config: RalphConfig):
        self.config = config
        self.stop_hook = StopHook(config)
        self.feedback_formatter = FeedbackFormatter(config)
        self.verification = VerificationRunner(config)
        self.loop_detector = InfiniteLoopDetector()
        self.iteration = 0
        self.start_time = 0
        self.history: List[str] = []
        self.total_cost = 0.0
        
    async def run(self) -> RalphResult:
        """
        Execute the Ralph Loop.
        
        Returns:
            RalphResult with success status and metrics
        """
        self.start_time = time.time()
        initial_context = self._create_initial_context()
        
        if self.config.verbose:
            self._print_header("RALPH WIGGUM LOOP STARTED")
            print(f"Task: {self.config.task}")
            print(f"Promise: {self.config.promise}")
            print(f"Max iterations: {self.config.max_iterations}")
            print()
        
        while self.iteration < self.config.max_iterations:
            iteration_start = time.time()
            
            # Check for escape hatch
            if self._check_escape_hatch():
                return RalphResult(
                    success=False,
                    iterations=self.iteration,
                    total_time=time.time() - self.start_time,
                    cost=self.total_cost,
                    final_output="",
                    error="Escape hatch triggered"
                )
            
            # Check for infinite loop
            stuck, reason = self.loop_detector.check("")
            if stuck:
                return RalphResult(
                    success=False,
                    iterations=self.iteration,
                    total_time=time.time() - self.start_time,
                    cost=self.total_cost,
                    final_output="",
                    error=f"Infinite loop detected: {reason}"
                )
            
            if self.config.verbose:
                print(f"{Colors.CYAN}--- Iteration {self.iteration + 1}/{self.config.max_iterations} ---{Colors.ENDC}")
            
            # Format input for this iteration
            if self.iteration == 0:
                input_text = self._format_initial_input()
            else:
                input_text = self._format_iteration_input()
            
            # Execute the task (this would call Claude Code)
            output, cost = await self._execute_task(input_text)
            self.total_cost += cost
            self.history.append(output)
            
            # Run verification
            verification = await self.verification.verify(output)
            
            # Check with Stop Hook
            should_exit, reason = self.stop_hook.check(output, {
                "verification": verification,
                "iteration": self.iteration
            })
            
            if self.config.verbose:
                if should_exit:
                    print(f"{Colors.GREEN}✅ {reason}{Colors.ENDC}")
                else:
                    print(f"{Colors.YELLOW}🔄 {reason}{Colors.ENDC}")
            
            if should_exit:
                # Success!
                if self.config.verbose:
                    self._print_success()
                return RalphResult(
                    success=True,
                    iterations=self.iteration + 1,
                    total_time=time.time() - self.start_time,
                    cost=self.total_cost,
                    final_output=output
                )
            
            # Continue to next iteration
            self.iteration += 1
            
            # Check cost limit
            if self.total_cost > self.config.max_cost:
                return RalphResult(
                    success=False,
                    iterations=self.iteration,
                    total_time=time.time() - self.start_time,
                    cost=self.total_cost,
                    final_output=output,
                    error=f"Cost limit exceeded: ${self.total_cost:.2f} > ${self.config.max_cost:.2f}"
                )
        
        # Max iterations reached
        return RalphResult(
            success=False,
            iterations=self.iteration,
            total_time=time.time() - self.start_time,
            cost=self.total_cost,
            final_output=self.history[-1] if self.history else "",
            error=f"Max iterations ({self.config.max_iterations}) reached without completion"
        )
    
    def _create_initial_context(self) -> Dict[str, Any]:
        """Create the initial context for the task"""
        return {
            "task": self.config.task,
            "promise": self.config.promise,
            "workdir": self.config.workdir,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _format_initial_input(self) -> str:
        """Format the initial task input"""
        lines = []
        lines.append("=" * 60)
        lines.append("RALPH WIGGUM LOOP - TASK EXECUTION")
        lines.append("=" * 60)
        lines.append("")
        lines.append("TASK:")
        lines.append(self.config.task)
        lines.append("")
        lines.append("COMPLETION PROMISE:")
        lines.append(f"<promise>{self.config.promise}</promise>")
        lines.append("")
        lines.append("INSTRUCTIONS:")
        lines.append("1. Work on this task until the completion promise is fulfilled")
        lines.append("2. When done, output <promise>COMPLETE</promise> at the end")
        lines.append("3. The system will verify the promise before allowing exit")
        lines.append("")
        lines.append("=" * 60)
        lines.append("BEGIN TASK")
        lines.append("=" * 60)
        lines.append("")
        return "\n".join(lines)
    
    def _format_iteration_input(self) -> str:
        """Format input for subsequent iterations with feedback"""
        last_output = self.history[-1] if self.history else ""
        
        # Generate hint based on verification failures
        hint = self._generate_hint()
        
        return self.feedback_formatter.format(
            self.iteration,
            last_output,
            {},
            hint
        )
    
    def _generate_hint(self) -> str:
        """Generate a helpful hint based on previous failures"""
        if not self.history:
            return ""
        
        last_output = self.history[-1]
        hints = []
        
        # Look for common issues and suggest fixes
        if "TypeError" in last_output:
            hints.append("- Check for undefined variables or incorrect types")
        if "ImportError" in last_output:
            hints.append("- Verify all imports are correct and packages are installed")
        if "SyntaxError" in last_output:
            hints.append("- Review syntax, especially recent changes")
        if "test" in self.config.promise.lower():
            hints.append("- Run tests locally to see exact failures")
        if "build" in self.config.promise.lower():
            hints.append("- Check build logs for specific error messages")
            
        if hints:
            return "Based on the output:\n" + "\n".join(hints)
        return "Review the errors above and try a different approach."
    
    async def _execute_task(self, input_text: str) -> Tuple[str, float]:
        """
        Execute the task with Claude Code.
        
        In a real implementation, this would call Claude Code CLI.
        For now, we simulate the execution.
        
        Returns:
            Tuple of (output, cost)
        """
        # This is a placeholder - in real implementation, call Claude Code
        # For testing, we'll return a simulated response
        
        if self.config.verbose:
            print(f"{Colors.BLUE}Executing task...{Colors.ENDC}")
        
        # Simulate task execution (replace with actual Claude Code call)
        # Example real implementation:
        # proc = await asyncio.create_subprocess_exec(
        #     "claude-code", "--task", self.config.task,
        #     "--input", input_text,
        #     stdout=asyncio.subprocess.PIPE,
        #     stderr=asyncio.subprocess.PIPE
        # )
        # stdout, stderr = await proc.communicate()
        # return stdout.decode(), self._estimate_cost(stdout)
        
        # Placeholder: Return simulated output
        simulated_output = f"""[Iteration {self.iteration + 1}] Working on task...

Error: Some error occurred during execution
This is simulated output for testing purposes.

<task_result partial>
More work needed to complete the promise.
</task_result>
"""
        
        # Estimate cost (placeholder)
        estimated_cost = 0.10  # $0.10 per iteration (placeholder)
        
        return simulated_output, estimated_cost
    
    def _check_escape_hatch(self) -> bool:
        """Check if escape hatch file exists"""
        escape_file = f"/tmp/ralph-exit-{os.getpid()}"
        return os.path.exists(escape_file)
    
    def _print_header(self, text: str):
        """Print a formatted header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")
    
    def _print_success(self):
        """Print success message"""
        elapsed = time.time() - self.start_time
        print(f"\n{Colors.GREEN}{Colors.BOLD}")
        print("=" * 60)
        print("RALPH WIGGUM LOOP COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"Iterations: {self.iteration + 1}")
        print(f"Total time: {elapsed:.2f}s")
        print(f"Total cost: ${self.total_cost:.2f}")
        print("=" * 60)
        print(f"{Colors.ENDC}")


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Ralph Wiggum Loop - Persistent Agent Framework"
    )
    parser.add_argument("task", help="The task to complete")
    parser.add_argument("--promise", 
                        default="All tests pass",
                        help="Completion promise (default: 'All tests pass')")
    parser.add_argument("--max-iterations", 
                        type=int, 
                        default=10,
                        help="Maximum iterations (default: 10)")
    parser.add_argument("--verbose", 
                        action="store_true",
                        help="Verbose output")
    parser.add_argument("--dangerously-skip-permissions",
                        action="store_true",
                        help="Skip permission checks (dangerous!)")
    parser.add_argument("--sandbox",
                        action="store_true",
                        help="Run in sandboxed environment")
    parser.add_argument("--timeout",
                        type=int,
                        default=300,
                        help="Timeout per iteration in seconds (default: 300)")
    parser.add_argument("--feedback",
                        choices=["errors", "diff", "full"],
                        default="errors",
                        help="Feedback type (default: errors)")
    parser.add_argument("--workdir",
                        default=".",
                        help="Working directory (default: current)")
    
    args = parser.parse_args()
    
    # Create config
    config = RalphConfig(
        task=args.task,
        promise=args.promise,
        max_iterations=args.max_iterations,
        verbose=args.verbose,
        skip_permissions=args.dangerously_skip_permissions,
        sandbox=args.sandbox,
        timeout=args.timeout,
        feedback=FeedbackType(args.feedback),
        workdir=args.workdir
    )
    
    # Run Ralph Loop
    loop = RalphLoop(config)
    result = await loop.run()
    
    # Output result
    if result.success:
        print(f"\n{Colors.GREEN}✅ SUCCESS{Colors.ENDC}")
        print(f"Iterations: {result.iterations}")
        print(f"Time: {result.total_time:.2f}s")
        print(f"Cost: ${result.cost:.2f}")
    else:
        print(f"\n{Colors.RED}❌ FAILED{Colors.ENDC}")
        print(f"Iterations: {result.iterations}")
        print(f"Time: {result.total_time:.2f}s")
        print(f"Cost: ${result.cost:.2f}")
        print(f"Error: {result.error}")
    
    # Save result to file if specified
    if config.output_file:
        with open(config.output_file, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
    
    return 0 if result.success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
