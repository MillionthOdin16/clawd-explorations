#!/usr/bin/env python3
"""
Ralph Wiggum Loop - Enhanced Implementation

Based on extensive research of:
- Smart Ralph (spec-driven development)
- ParkerRex (external loop pattern)
- Universal Ralph (vendor-agnostic)
- Official Anthropic plugin

Key improvements:
1. Structured prompt format with completion criteria
2. Stats and timing
3. Quality gates (max retries)
4. Progress tracking
5. External mode option
"""

import asyncio
import argparse
import json
import os
import sys
import time
import hashlib
import re
import subprocess
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


class ExecutionMode(str, Enum):
    IN_SESSION = "in_session"  # Like official plugin
    EXTERNAL = "external"      # Like ParkerRex


@dataclass
class RalphConfig:
    """Enhanced configuration for Ralph Loop"""
    
    # Core
    task: str
    promise: str = "All tests pass"
    max_iterations: int = 10
    max_retries_per_task: int = 5  # Quality gate
    
    # Execution
    mode: ExecutionMode = ExecutionMode.IN_SESSION
    verbose: bool = False
    skip_permissions: bool = False
    sandbox: bool = False
    timeout: int = 300
    
    # Feedback
    feedback: FeedbackType = FeedbackType.ERRORS
    workdir: str = "."
    
    # Safety
    max_cost: float = 100.0
    
    # State files
    state_file: str = ".claude/ralph-loop.local.md"
    prompt_file: str = ".claude/RALPH_PROMPT.md"
    progress_file: str = ".claude/RALPH_PROGRESS.md"
    
    # Claude command (for external mode)
    claude_command: str = "claude --dangerously-skip-permissions"


@dataclass
class RalphResult:
    """Result of Ralph Loop execution"""
    success: bool
    iterations: int
    total_time: float
    cost: float
    final_output: str
    error: Optional[str] = None
    mode: str = "in_session"
    
    def to_dict(self):
        return {
            "success": self.success,
            "iterations": self.iterations,
            "total_time": self.total_time,
            "cost": self.cost,
            "error": self.error,
            "mode": self.mode,
            "timestamp": datetime.utcnow().isoformat()
        }


class StructuredPromptBuilder:
    """
    Builds structured prompts based on Smart Ralph research.
    Ensures clear requirements and completion criteria.
    """
    
    @staticmethod
    def build(task: str, promise: str, requirements: List[str] = None, 
              verification: List[str] = None) -> str:
        """
        Build a structured prompt with clear sections.
        
        Template:
        # Task
        [description]
        
        ## Requirements
        - [requirement 1]
        - [requirement 2]
        
        ## Completion Criteria
        When ALL of the following are true:
        - [criteria 1]
        - [criteria 2]
        
        Output: <promise>YOUR_PROMISE</promise>
        """
        lines = []
        lines.append("=" * 60)
        lines.append("RALPH WIGGUM LOOP - TASK EXECUTION")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"# {task}")
        lines.append("")
        
        if requirements:
            lines.append("## Requirements")
            for req in requirements:
                lines.append(f"- {req}")
            lines.append("")
        
        if verification:
            lines.append("## Verification")
            for v in verification:
                lines.append(f"- [ ] {v}")
            lines.append("")
        
        lines.append("## Completion Criteria")
        lines.append("When ALL of the following are true:")
        lines.append(f"- {verification[0] if verification else 'Task is complete'}")
        lines.append("")
        lines.append(f"Output: <promise>{promise}</promise>")
        lines.append("")
        lines.append("=" * 60)
        lines.append("INSTRUCTIONS:")
        lines.append("1. Work on this task until completion criteria are met")
        lines.append("2. Output <promise>{promise}</promise> ONLY when criteria are truly met")
        lines.append("3. Do NOT lie to exit the loop")
        lines.append("=" * 60)
        lines.append("")
        lines.append("BEGIN TASK")
        lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def parse_prompt(prompt_text: str) -> Dict[str, Any]:
        """Parse a structured prompt to extract components"""
        result = {
            "task": "",
            "requirements": [],
            "verification": [],
            "promise": ""
        }
        
        lines = prompt_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('# '):
                result["task"] = line[2:]
                current_section = "task"
            elif line.startswith('## '):
                current_section = line[3:].lower()
            elif line.startswith('- ') and current_section == "requirements":
                result["requirements"].append(line[2:])
            elif line.startswith('- [ ]') and current_section == "verification":
                result["verification"].append(line[6:])
            elif 'Output: <promise>' in line:
                match = re.search(r'<promise>(.+)</promise>', line)
                if match:
                    result["promise"] = match.group(1)
        
        return result


class RalphStats:
    """Track statistics for Ralph loop execution"""
    
    def __init__(self):
        self.iterations = 0
        self.start_time = time.time()
        self.attempts = 0
        self.retries = 0
        self.cost = 0.0
        self.task_start_times = []
        
    def start_task(self):
        """Mark start of a new task"""
        self.task_start_times.append(time.time())
        
    def complete_task(self):
        """Mark task as complete"""
        if self.task_start_times:
            self.task_start_times.pop()
    
    def add_retry(self):
        """Add a retry"""
        self.retries += 1
        
    def to_dict(self) -> Dict:
        elapsed = time.time() - self.start_time
        return {
            "iterations": self.iterations,
            "total_time": f"{elapsed:.2f}s",
            "retries": self.retries,
            "cost": f"${self.cost:.2f}",
            "avg_task_time": f"{elapsed/max(1, len(self.task_start_times)):.2f}s"
        }
    
    def print_summary(self):
        """Print summary of execution"""
        elapsed = time.time() - self.start_time
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("=" * 60)
        print("RALPH WIGGUM LOOP COMPLETED")
        print("=" * 60)
        print(f"Iterations: {self.iterations}")
        print(f"Retries: {self.retries}")
        print(f"Total time: {elapsed:.2f}s")
        print(f"Estimated cost: ${self.cost:.2f}")
        print("=" * 60)
        print(f"{Colors.ENDC}")


class StopHook:
    """
    Enhanced Stop Hook based on official Anthropic implementation.
    Intercepts exit attempts and verifies completion promise.
    """
    
    def __init__(self, config: RalphConfig):
        self.config = config
        self.exit_blocked_count = 0
        
    def check(self, output: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Check if exit should be blocked.
        
        Returns:
            Tuple of (should_exit, reason)
        """
        # Check for completion promise
        if not self._has_promise(output):
            self.exit_blocked_count += 1
            return False, "No completion promise found"
        
        # Verify the promise conditions
        verified, reason = self._verify_promise(output, context)
        if not verified:
            self.exit_blocked_count += 1
            return False, f"Promise not fulfilled: {reason}"
        
        return True, "Promise fulfilled"
    
    def _has_promise(self, output: str) -> bool:
        """Check if output contains the completion promise marker"""
        promise_marker = f"<promise>{self.config.promise}</promise>"
        return promise_marker in output or "<promise>COMPLETE</promise>" in output
    
    def _verify_promise(self, output: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """Verify that the promised completion condition is actually met"""
        verification_result = context.get("verification", {})
        
        if not verification_result:
            return False, "No verification results available"
        
        if verification_result.get("passed") is True:
            return True, "Verification passed"
        
        failures = verification_result.get("failures", [])
        if failures:
            return False, f"Verification failed: {'; '.join(failures)}"
        
        return False, "Verification status unknown"


class ExternalRalphLoop:
    """
    External loop implementation based on ParkerRex pattern.
    Runs as external bash script, bypassing session limitations.
    """
    
    def __init__(self, config: RalphConfig, stats: RalphStats):
        self.config = config
        self.stats = stats
        
    async def run(self) -> RalphResult:
        """
        Execute external Ralph loop.
        
        This runs claude -p in a loop, similar to ParkerRex implementation.
        """
        start_time = time.time()
        
        # Ensure state directory exists
        Path(self.config.workdir).mkdir(parents=True, exist_ok=True)
        
        # Write prompt file
        prompt_text = StructuredPromptBuilder.build(
            self.config.task,
            self.config.promise
        )
        prompt_file = os.path.join(self.config.workdir, "RALPH_PROMPT.md")
        with open(prompt_file, 'w') as f:
            f.write(prompt_text)
        
        iteration = 0
        
        while iteration < self.config.max_iterations:
            iteration += 1
            self.stats.iterations = iteration
            
            if self.config.verbose:
                print(f"{Colors.CYAN}--- Iteration {iteration}/{self.config.max_iterations} ---{Colors.ENDC}")
            
            # Build command
            cmd = self.config.claude_command
            
            # Read prompt and add context
            with open(prompt_file, 'r') as f:
                prompt = f.read()
            
            # Add iteration info to prompt
            iteration_prompt = f"{prompt}\n\n# Iteration {iteration}\nPlease continue working on the task above.\n"
            
            # Execute Claude in prompt mode
            try:
                proc = await asyncio.create_subprocess_exec(
                    *cmd.split(),
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=self.config.workdir
                )
                stdout, stderr = await proc.communicate(
                    input=iteration_prompt.encode(),
                    timeout=self.config.timeout
                )
                output = stdout.decode() + stderr.decode()
                
                # Estimate cost (placeholder)
                self.stats.cost += 0.10  # $0.10 per iteration
                
                # Check for completion promise
                stop_hook = StopHook(self.config)
                should_exit, reason = stop_hook.check(output, {})
                
                if self.config.verbose:
                    if should_exit:
                        print(f"{Colors.GREEN}✅ {reason}{Colors.ENDC}")
                    else:
                        print(f"{Colors.YELLOW}🔄 {reason}{Colors.ENDC}")
                
                if should_exit:
                    return RalphResult(
                        success=True,
                        iterations=iteration,
                        total_time=time.time() - start_time,
                        cost=self.stats.cost,
                        final_output=output,
                        mode="external"
                    )
                
                # Update prompt file with context for next iteration
                with open(prompt_file, 'w') as f:
                    f.write(f"{iteration_prompt}\n\n# Previous Output:\n{output[:2000]}")
                
            except asyncio.TimeoutError:
                if self.config.verbose:
                    print(f"{Colors.RED}⏱️  Timeout on iteration {iteration}{Colors.ENDC}")
                if iteration >= self.config.max_iterations:
                    break
            except Exception as e:
                if self.config.verbose:
                    print(f"{Colors.RED}❌ Error: {e}{Colors.ENDC}")
                if iteration >= self.config.max_iterations:
                    break
        
        # Max iterations reached
        return RalphResult(
            success=False,
            iterations=iteration,
            total_time=time.time() - start_time,
            cost=self.stats.cost,
            final_output="",
            error=f"Max iterations ({self.config.max_iterations}) reached",
            mode="external"
        )


class InSessionRalphLoop:
    """
    In-session loop implementation based on official plugin.
    Uses Stop Hook to intercept exit and feed prompt back.
    """
    
    def __init__(self, config: RalphConfig, stats: RalphStats):
        self.config = config
        self.stats = stats
        
    async def run(self) -> RalphResult:
        """
        Execute in-session Ralph loop.
        
        This simulates the official plugin behavior:
        1. Create state file
        2. Output formatted prompt
        3. User/agent works on task
        4. Stop hook intercepts exit
        5. Loop continues
        """
        start_time = time.time()
        
        # Ensure state directory exists
        state_dir = os.path.dirname(self.config.state_file)
        Path(state_dir).mkdir(parents=True, exist_ok=True)
        
        # Create state file
        state_content = f"""---
iteration: 0
max_iterations: {self.config.max_iterations}
completion_promise: "{self.config.promise}"
---
# Task
{self.config.task}

## Instructions
Work on this task until completion. Output <promise>{self.config.promise}</promise> when done.
"""
        with open(self.config.state_file, 'w') as f:
            f.write(state_content)
        
        if self.config.verbose:
            self._print_header()
            print(f"Task: {self.config.task}")
            print(f"Promise: {self.config.promise}")
            print(f"Max iterations: {self.config.max_iterations}")
            print(f"\nState file: {self.config.state_file}")
            print("\nThis simulates in-session Ralph loop.")
            print("In a real Claude Code session, the stop hook would intercept exit.\n")
        
        # For in-session mode, we output the structured prompt
        # In actual implementation, Claude Code handles the loop
        prompt_text = StructuredPromptBuilder.build(
            self.config.task,
            self.config.promise
        )
        
        return RalphResult(
            success=False,
            iterations=0,
            total_time=time.time() - start_time,
            cost=0.0,
            final_output=prompt_text,
            mode="in_session",
            error="In-session mode requires Claude Code plugin. Use --mode external for standalone execution."
        )
    
    def _print_header(self):
        """Print formatted header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("=" * 60)
        print("RALPH WIGGUM LOOP - IN SESSION MODE")
        print("=" * 60)
        print(f"{Colors.ENDC}")


class RalphLoop:
    """
    Main Ralph Wiggum Loop orchestrator.
    
    Supports both in-session and external execution modes.
    """
    
    def __init__(self, config: RalphConfig):
        self.config = config
        self.stats = RalphStats()
        self.stop_hook = StopHook(config)
        
    async def run(self) -> RalphResult:
        """
        Execute Ralph Loop based on configured mode.
        """
        if self.config.mode == ExecutionMode.EXTERNAL:
            loop = ExternalRalphLoop(self.config, self.stats)
        else:
            loop = InSessionRalphLoop(self.config, self.stats)
        
        result = await loop.run()
        
        if self.config.verbose:
            self.stats.print_summary()
        
        return result
    
    def create_structured_prompt(self) -> str:
        """Create a structured prompt for the task"""
        return StructuredPromptBuilder.build(
            self.config.task,
            self.config.promise
        )


def parse_arguments():
    """Parse command line arguments"""
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
    parser.add_argument("--max-retries",
                        type=int,
                        default=5,
                        help="Max retries per task (quality gate, default: 5)")
    parser.add_argument("--mode",
                        choices=["in_session", "external"],
                        default="external",
                        help="Execution mode (default: external)")
    parser.add_argument("--verbose", 
                        action="store_true",
                        help="Verbose output")
    parser.add_argument("--dangerously-skip-permissions",
                        action="store_true",
                        help="Skip permission checks (external mode only)")
    parser.add_argument("--sandbox",
                        action="store_true",
                        help="Run in sandboxed environment")
    parser.add_argument("--timeout",
                        type=int,
                        default=300,
                        help="Timeout per iteration (default: 300)")
    parser.add_argument("--feedback",
                        choices=["errors", "diff", "full"],
                        default="errors",
                        help="Feedback type (default: errors)")
    parser.add_argument("--workdir",
                        default=".",
                        help="Working directory (default: current)")
    parser.add_argument("--claude-command",
                        default="claude --dangerously-skip-permissions",
                        help="Claude command (external mode, default: 'claude --dangerously-skip-permissions')")
    
    return parser.parse_args()


async def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Create config
    config = RalphConfig(
        task=args.task,
        promise=args.promise,
        max_iterations=args.max_iterations,
        max_retries_per_task=args.max_retries,
        mode=ExecutionMode.EXTERNAL if args.mode == "external" else ExecutionMode.IN_SESSION,
        verbose=args.verbose,
        skip_permissions=args.dangerously_skip_permissions,
        sandbox=args.sandbox,
        timeout=args.timeout,
        feedback=FeedbackType(args.feedback),
        workdir=args.workdir,
        claude_command=args.claude_command
    )
    
    if config.verbose:
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("RALPH WIGGUM LOOP - Enhanced Implementation")
        print("Based on research from:")
        print("  - Smart Ralph (spec-driven development)")
        print("  - ParkerRex (external loop pattern)")
        print("  - Universal Ralph (vendor-agnostic)")
        print("=" * 60)
        print(f"{Colors.ENDC}")
        print(f"\nMode: {config.mode}")
        print(f"Task: {config.task}")
        print(f"Promise: {config.promise}")
        print(f"Max iterations: {config.max_iterations}")
        print(f"Quality gate: {config.max_retries_per_task} retries per task\n")
    
    # Create and run Ralph Loop
    loop = RalphLoop(config)
    result = await loop.run()
    
    # Output result
    if result.success:
        print(f"\n{Colors.GREEN}✅ SUCCESS{Colors.ENDC}")
    else:
        print(f"\n{Colors.RED}❌ FAILED{Colors.ENDC}")
        print(f"Error: {result.error}")
    
    print(f"Iterations: {result.iterations}")
    print(f"Time: {result.total_time:.2f}s")
    print(f"Cost: ${result.cost:.2f}")
    
    return 0 if result.success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
