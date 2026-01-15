# 🦞 Ralph Wiggum Loop - Persistent Agent Framework

**Version:** 1.0.0  
**Created:** 2026-01-15  
**Purpose:** Autonomous agent loop that persists until task completion

---

## Overview

The Ralph Wiggum Loop is a framework for creating persistent, autonomous agents that iterate until a specific completion condition is met. Named after the relentlessly optimistic character from The Simpsons, this technique uses a "contextual pressure cooker" approach where the agent's own failures are fed back as input for the next iteration.

### Core Philosophy

> "If you press the model hard enough against its own failures without a safety net, it will eventually 'dream' a correct solution just to escape the loop."

### Key Components

1. **Completion Promise** - Agent must emit `<promise>COMPLETE</promise>` to exit
2. **Stop Hook** - Intercepts exit attempts and verifies promise
3. **Feedback Injection** - Formats failures as structured data for next iteration
4. **Escape Hatches** - Safety limits to prevent infinite loops
5. **Verification System** - Tests if the promise conditions are actually met

---

## Usage

### Basic Usage

```bash
# Run a Ralph loop with default settings (10 iterations max)
uv run ralph.py "Fix all TypeScript errors in the project"

# Custom iterations
uv run ralph.py "Write unit tests for all functions" --max-iterations 20

# With specific completion promise
uv run ralph.py "Complete the migration" --promise "All tests pass and build succeeds"

# Verbose mode
uv run ralph.py "Refactor the codebase" --verbose --max-iterations 50
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--task` | The task to complete | Required |
| `--promise` | Custom completion promise | "All tests pass" |
| `--max-iterations` | Maximum iterations before giving up | 10 |
| `--verbose` | Show detailed output | False |
| `--dangerously-skip-permissions` | Skip permission checks | False |
| `--sandbox` | Run in sandboxed environment | False |
| `--timeout` | Timeout per iteration (seconds) | 300 |
| `--feedback` | Type of feedback (full, errors, diff) | errors |

---

## The Ralph Loop Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RALPH WIGGUM LOOP                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐                                           │
│  │  Task Input   │                                           │
│  └──────┬───────┘                                           │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────────────────┐                            │
│  │  Claude Code Session        │                            │
│  │  - Receives task            │                            │
│  │  - Receives previous output │                            │
│  │  - Attempts to complete     │                            │
│  └──────────────┬──────────────┘                            │
│                 │                                           │
│                 ▼                                           │
│  ┌─────────────────────────────┐                            │
│  │  Stop Hook Interceptor      │                            │
│  │  - Checks for <promise>     │                            │
│  │  - Verifies completion      │                            │
│  │  - Blocks exit if incomplete│                            │
│  └──────────────┬──────────────┘                            │
│                 │                                           │
│         ┌───────┴───────┐                                   │
│         │               │                                   │
│         ▼               ▼                                   │
│  ┌──────────┐    ┌──────────────┐                          │
│  │ COMPLETE │    │ FEEDBACK     │                          │
│  │          │    │ - Errors     │                          │
│  │ Exit     │    │ - Logs       │                          │
│  │ Loop     │    │ - Diff       │                          │
│  └──────────┘    └──────┬───────┘                          │
│                         │                                   │
│                         └──────────┐                        │
│                                    │                        │
│                                    ▼                        │
│                          ┌─────────────────┐                │
│                          │  Next Iteration │                │
│                          │  (Back to top)  │                │
│                          └─────────────────┘                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Details

### 1. The Stop Hook

The Stop Hook is the core innovation. It intercepts Claude's exit attempt:

```python
def stop_hook(session):
    """
    Intercept exit attempts and verify completion promise.
    
    Returns:
        True: Exit allowed (promise met)
        False: Block exit, continue looping
        Exception: Error during verification
    """
    # 1. Check for completion promise in output
    if not session.output.contains("<promise>COMPLETE</promise>"):
        return False
    
    # 2. Verify promise conditions
    if not verify_promise(session, session.config.promise):
        return False
    
    # 3. All checks passed - allow exit
    return True
```

### 2. Completion Promise Verification

The promise must be verifiable, not just stated:

```python
async def verify_promise(session, promise):
    """
    Verify that the stated completion promise is actually fulfilled.
    
    Args:
        session: Current session with output and context
        promise: The promised completion condition
    
    Returns:
        True if promise is fulfilled
        False if promise is not fulfilled
    """
    # Parse the promise into verifiable conditions
    conditions = parse_promise(promise)
    
    # Check each condition
    for condition in conditions:
        if not await check_condition(session, condition):
            return False
    
    return True
```

### 3. Feedback Formatting

Failures are formatted for maximum learning:

```python
def format_feedback(session):
    """
    Format session output as feedback for next iteration.
    
    Structure:
    ```
    === ITERATION N ===
    
    PREVIOUS OUTPUT:
    [Full output from previous attempt]
    
    ERRORS:
    [Extracted errors and warnings]
    
    VERIFICATION RESULT:
    [Why the previous attempt failed]
    
    HINT:
    [Suggested approach based on errors]
    
    ===
    ```
    """
    feedback = {
        "iteration": session.iteration,
        "output": session.last_output,
        "errors": extract_errors(session.last_output),
        "verification": session.verification_result,
        "hint": generate_hint(session.verification_result)
    }
    return format_feedback_text(feedback)
```

### 4. Safety Mechanisms

Multiple layers of safety:

```python
class SafetyMechanisms:
    """Safety mechanisms for Ralph Loop"""
    
    def __init__(self, config):
        self.max_iterations = config.max_iterations
        self.max_cost = config.max_cost
        self.timeout = config.timeout
        self.sandbox = config.sandbox
        
    def should_continue(self, iteration, cost, session):
        """Determine if loop should continue"""
        
        # Check iteration limit
        if iteration >= self.max_iterations:
            return False, f"Max iterations ({self.max_iterations}) reached"
        
        # Check cost limit
        if cost > self.max_cost:
            return False, f"Max cost (${self.max_cost}) exceeded"
        
        # Check for infinite loop patterns
        if self.detect_infinite_loop(session):
            return False, "Infinite loop pattern detected"
        
        # Check timeout
        if session.elapsed_time > self.timeout:
            return False, f"Timeout ({self.timeout}s) exceeded"
        
        return True, "Continue"
    
    def detect_infinite_loop(self, session):
        """Detect if we're stuck in a loop"""
        if len(session.history) < 3:
            return False
        
        # Check if last 3 outputs are identical
        recent = session.history[-3:]
        if len(set(recent)) == 1:
            return True
        
        # Check if we're making no progress
        if session.error_count_stagnant > 5:
            return True
        
        return False
```

### 5. Escape Hatches

Users should always have escape options:

```bash
# Kill the loop from another terminal
echo "RALPH_EXIT" > /tmp/ralph-exit-$PID

# Or use the built-in escape
Ctrl+C (confirms before killing)

# Or use the API
curl -X POST http://localhost:18789/ralph/exit
```

---

## Completion Promise Patterns

### TypeScript/JavaScript Projects

```
<promise>TypeScript compiles without errors, ESLint passes, and all tests pass</promise>
```

### Python Projects

```
<promise>All tests pass (pytest), no linting errors, and type checking passes</promise>
```

### Database Migrations

```
<promise>All migration scripts run successfully, schema matches target, and tests pass</promise>
```

### Infrastructure/DevOps

```
<promise>Terraform plan shows only expected changes, apply succeeds, and health checks pass</promise>
```

### General Tasks

```
<promise>TASK_DESCRIPTION and verification steps pass</promise>
```

---

## Best Practices

### 1. Use Strong Verification
- Prefer automated tests over manual checking
- Use type systems (TypeScript, Rust, etc.)
- Include linting in the verification
- Set up CI/CD that Ralph can trigger

### 2. Set Appropriate Limits
- Start with `--max-iterations 20` for complex tasks
- Set `--max-cost` based on budget
- Use `--timeout` to prevent stuck sessions

### 3. Sandbox Dangerous Operations
- Always use `--sandbox` for destructive operations
- Run in disposable VMs for risky tasks
- Use `--dangerously-skip-permissions` only when necessary

### 4. Structure Tasks Well
- Break large tasks into smaller sub-tasks
- Use Ralph for tasks with clear completion criteria
- For ambiguous tasks, add more context

### 5. Monitor Progress
- Use `--verbose` for debugging
- Check session logs regularly
- Set up notifications for completion/failure

---

## Examples

### Example 1: Fix TypeScript Errors

```bash
uv run ralph.py "Fix all TypeScript errors in src/" \
  --promise "tsc --noEmit passes with no errors" \
  --max-iterations 15 \
  --verbose
```

### Example 2: Write Unit Tests

```bash
uv run ralph.py "Write unit tests for all functions in lib/" \
  --promise "All functions have >= 80% test coverage and tests pass" \
  --max-iterations 20 \
  --feedback full
```

### Example 3: Database Migration

```bash
uv run ralph.py "Create and run database migration for user table" \
  --promise "Migration runs successfully, tests pass, rollback works" \
  --max-iterations 5 \
  --sandbox
```

### Example 4: Full Refactor

```bash
uv run ralph.py "Refactor authentication module to use JWT" \
  --promise "All auth tests pass, API contracts unchanged, security audit passes" \
  --max-iterations 30 \
  --timeout 600
```

---

## Cost Estimation

| Task Complexity | Avg Iterations | Est. Cost (Claude 4) |
|-----------------|----------------|---------------------|
| Simple fix | 2-5 | $0.50 - $2.00 |
| Medium task | 5-15 | $2.00 - $15.00 |
| Complex refactor | 15-30 | $15.00 - $50.00 |
| Large migration | 30-50 | $50.00 - $150.00 |

*Estimates based on typical Claude 4 pricing. Actual costs vary.*

---

## Comparison: Huntley Ralph vs Official Ralph

| Aspect | Huntley Ralph (OG) | Official Ralph (Plugin) |
|--------|-------------------|------------------------|
| **Philosophy** | Brute force, chaos | "Failures Are Data" |
| **Safety** | None | Stop hooks, limits |
| **Exit** | Manual kill | Promise verification |
| **Feedback** | Raw output | Structured data |
| **Best For** | Creative exploration | Enterprise workflows |

---

## Troubleshooting

### Ralph won't exit even after success
- Check that `<promise>COMPLETE</promise>` is in output
- Verify promise conditions are actually met
- Check that verification script is working

### Ralph is stuck in a loop
- Reduce `--max-iterations`
- Add more specific hints to task description
- Check for infinite loop patterns

### Ralph is too aggressive
- Use `--sandbox` mode
- Set lower `--max-cost`
- Add more verification steps

### Ralph is too cautious
- Increase `--max-iterations`
- Simplify completion promise
- Reduce verification strictness

---

## Integration with Claude Code

### Claude Code CLI

```bash
# Install as plugin (if available)
/plugin ralph

# Or run directly
claude-code --task "Your task" --ralph-loop
```

### Programmatic Usage

```python
from ralph import RalphLoop

loop = RalphLoop(
    task="Fix the bug in auth.py",
    promise="All auth tests pass",
    max_iterations=20,
    verbose=True
)

result = loop.run()
print(f"Completed in {result.iterations} iterations")
print(f"Total cost: ${result.cost:.2f}")
```

---

## Research and Credits

- **Original Concept:** Geoffrey Huntley's 5-line Bash script
- **Official Implementation:** Anthropic's Claude Code Ralph Wiggum Plugin
- **Key Insights:** 
  - "Naive persistence" from unsanitized feedback
  - "Contextual pressure cooker" effect
  - "Dreaming correct solutions" through iteration

---

## Future Enhancements

- [ ] Parallel Ralph loops for independent tasks
- [ ] Learning from previous Ralph sessions
- [ ] Cost optimization suggestions
- [ ] Integration with more verification tools
- [ ] Distributed Ralph for massive tasks
- [ ] Web dashboard for monitoring

---

## Summary

The Ralph Wiggum Loop is a powerful technique for autonomous agent persistence. By creating a feedback loop where the agent confronts its own failures, it can achieve remarkable results through sheer iteration.

**Key takeaways:**
1. Use strong verification (tests, type checks, linters)
2. Set appropriate limits (iterations, cost, timeout)
3. Structure tasks well with clear completion criteria
4. Sandbox dangerous operations
5. Monitor progress and adjust parameters

The Ralph Loop represents a shift from "Waterfall" planning to true "Agile" for AI - grab a ticket, finish it, move to the next.

---

*For updates and issues, see the project repository.*
