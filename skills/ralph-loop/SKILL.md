# 🦞 Ralph Wiggum Loop - Persistent Agent Framework

**Version:** 2.0.0 - Research-Enhanced  
**Created:** 2026-01-15  
**Research Sources:** Smart Ralph, ParkerRex, Universal Ralph, Official Anthropic Plugin

---

## Overview

The Ralph Wiggum Loop is a framework for creating persistent, autonomous agents that iterate until a specific completion condition is met. Named after the relentlessly optimistic character from The Simpsons, this technique uses a "contextual pressure cooker" approach where the agent's own failures are fed back as input for the next iteration.

### The Core Insight

> "Ralph will test you. Every time Ralph takes a wrong direction, tune the prompt, not the tool."  
> — Geoffrey Huntley

---

## Research Findings

Extensive research found 5 major implementations with significant variations:

| Implementation | Stars | Key Innovation |
|---------------|-------|----------------|
| **Smart Ralph** | 219 | Spec-driven development with multi-phase workflow |
| **ParkerRex Ralph** | 37 | External bash loop (bypasses broken plugin) |
| **Universal Ralph** | 6 | Vendor-agnostic (Claude/Codex/Gemini/Ollama) |
| **Official Anthropic** | - | Built-in Claude Code plugin with Stop Hook |
| **Huntley Original** | - | The 5-line Bash loop concept |

---

## Key Innovations Found

### 1. Smart Ralph - Spec-Driven Development

**GitHub:** https://github.com/tzachbon/smart-ralph

Smart Ralph adds upfront planning before implementation:

```
You: "Add user authentication"
Ralph: *creates research.md, requirements.md, design.md, tasks.md*
Ralph: *executes each task with fresh context*
Ralph: "I'm helping!"
```

**Key Features:**
- **Multi-Phase Workflow:** Research → Requirements → Design → Tasks → Implementation
- **Task-by-Task Execution:** Fresh context per task (prevents overflow)
- **Quality Gates:** After 5 failed attempts, blocks with error
- **Progress Tracking:** `.progress.md` tracks current state

### 2. ParkerRex - External Loop Pattern

**GitHub:** https://github.com/ParkerRex/ralph-loop

A working workaround for broken official plugin:

> "The official `ralph-wiggum` plugin (v2.0.76+) has critical bugs:
> - Multi-line bash commands blocked by security checks
> - `/cancel-ralph` command doesn't work
> - Stop hook hijacks all sessions"

**Architecture:**
```
┌─────────────────────────────────────────────────────────┐
│                    ralph-loop.sh                        │
│  1. Read .claude/RALPH_PROMPT.md                        │
│  2. Run: claude -p --dangerously-skip-permissions       │
│  3. Check output for <promise>...</promise>             │
│  4. If found → exit success                             │
│  5. If not → increment iteration, goto 1                │
└─────────────────────────────────────────────────────────┘
```

### 3. Universal Ralph - Vendor-Agnostic

**GitHub:** https://github.com/syuya2036/ralph-loop

Works with Claude, Codex, Gemini, Ollama, Qwen:

```bash
# Claude Code
./ralph-loop/ralph.sh "claude --dangerously-skip-permissions" 20

# Codex CLI
./ralph-loop/ralph.sh "codex exec --full-auto" 20

# Gemini CLI
./ralph-loop/ralph.sh "gemini --yolo" 20
```

---

## Our Implementation

This implementation combines the best features from research:

### Features

| Feature | Implementation |
|---------|----------------|
| **Structured Prompt Format** | Based on Smart Ralph |
| **Stats and Timing** | Based on ParkerRex |
| **Quality Gates** | Max retries per task |
| **Progress Tracking** | State file management |
| **Dual Mode** | In-session + External |

### Usage

#### Basic Usage

```bash
# External mode (recommended)
uv run ralph-enhanced.py "Fix all TypeScript errors" --max-iterations 20

# With structured prompt
uv run ralph-enhanced.py "Build a REST API" \
  --promise "Tests pass and server runs" \
  --max-iterations 30

# Verbose mode
uv run ralph-enhanced.py "Refactor the codebase" --verbose
```

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `task` | The task to complete | Required |
| `--promise` | Completion promise | "All tests pass" |
| `--max-iterations` | Max iterations | 10 |
| `--max-retries` | Max retries per task (quality gate) | 5 |
| `--mode` | in_session or external | external |
| `--verbose` | Verbose output | False |
| `--timeout` | Timeout per iteration (seconds) | 300 |
| `--claude-command` | Claude CLI command | claude --dangerously-skip-permissions |

### Structured Prompt Format

For best results, use structured prompts:

```markdown
# Task Title

[Clear description of what to build]

## Requirements
- Requirement 1
- Requirement 2

## Completion Criteria
When ALL of the following are true:
- Tests pass (`npm test`)
- Server runs (`npm start`)

Output: <promise>TASK COMPLETE</promise>
```

---

## Ralph Loop Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RALPH WIGGUM LOOP                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    RalphConfig                       │   │
│  │  - task, promise, max_iterations                     │   │
│  │  - mode (in_session/external)                        │   │
│  │  - max_retries_per_task (quality gate)               │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              StructuredPromptBuilder                 │   │
│  │  - Builds prompts with clear requirements           │   │
│  │  - Parses prompt components                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   RalphLoop                          │   │
│  │  - Orchestrates execution                           │   │
│  │  - Tracks stats and progress                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│              ┌────────────┴────────────┐                    │
│              │                         │                    │
│              ▼                         ▼                    │
│  ┌─────────────────────┐   ┌─────────────────────────┐    │
│  │ InSessionRalphLoop  │   │ ExternalRalphLoop       │    │
│  │ - Official plugin   │   │ - ParkerRex pattern     │    │
│  │ - Stop hook based   │   │ - claude -p based       │    │
│  └─────────────────────┘   └─────────────────────────┘    │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   StopHook                           │   │
│  │  - Intercepts exit attempts                         │   │
│  │  - Verifies completion promise                      │   │
│  │  - Blocks until promise met                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## The Stop Hook (Core Innovation)

The Stop Hook is what makes Ralph work:

```python
def stop_hook(output: str) -> Tuple[bool, str]:
    """
    Intercept exit attempts and verify completion promise.
    
    Returns:
        (should_exit, reason)
    """
    # 1. Check for completion promise
    if not has_promise(output):
        return False, "No completion promise found"
    
    # 2. Verify the promise conditions
    if not verify_conditions(output):
        return False, "Promise not fulfilled"
    
    # 3. All checks passed - allow exit
    return True, "Promise fulfilled"
```

---

## Safety Mechanisms

Multiple layers of safety:

| Mechanism | Description | Default |
|-----------|-------------|---------|
| **Max Iterations** | Hard limit on iterations | 10 |
| **Max Retries** | Quality gate per task | 5 |
| **Cost Limit** | Dollar limit | $100 |
| **Timeout** | Per-iteration timeout | 300s |
| **Escape Hatch** | Manual kill option | Ctrl+C |
| **Sandbox Mode** | Isolated environment | Optional |

---

## Completion Promise Patterns

### TypeScript/JavaScript
```
<promise>TypeScript compiles without errors, ESLint passes, and all tests pass</promise>
```

### Python
```
<promise>All tests pass (pytest), no linting errors, and type checking passes</promise>
```

### Database Migrations
```
<promise>All migration scripts run successfully, schema matches target, and tests pass</promise>
```

### General Tasks
```
<promise>TASK_DESCRIPTION and verification steps pass</promise>
```

---

## Cost Estimation

| Task Complexity | Avg Iterations | Est. Cost (Claude 4) |
|-----------------|----------------|---------------------|
| Simple fix | 2-5 | $0.50 - $2.00 |
| Medium task | 5-15 | $2.00 - $15.00 |
| Complex refactor | 15-30 | $15.00 - $50.00 |
| Large migration | 30-50 | $50.00 - $150.00 |

---

## Best Practices

### Do

- ✅ Use structured prompts with clear requirements
- ✅ Set appropriate iteration limits
- ✅ Include automated verification (tests, type checks)
- ✅ Monitor progress in verbose mode
- ✅ Use quality gates (max retries) for complex tasks
- ✅ Consider external mode for reliability

### Don't

- ❌ Use vague completion criteria
- ❌ Forget to mention test/verification commands
- ❌ Skip the "Completion Criteria" section
- ❌ Use without limits on production systems

---

## Real-World Results

From research:
- **$50K contract** completed for $297 in API costs
- **6 repositories** generated overnight at Y Combinator hackathon
- **Entire programming language** ("CURSED") built over 3 months

---

## File Structure

```
skills/ralph-loop/
├── SKILL.md               # This documentation
├── RESEARCH.md            # Extensive research findings
├── IMPLEMENTATION.md      # Original implementation report
└── scripts/
    ├── ralph.py           # Basic implementation (7KB)
    ├── ralph-enhanced.py  # Research-enhanced (21KB)
    ├── verify_ralph.py    # Quick verification tests
    └── test_ralph.py      # Full pytest test suite
```

---

## Resources

### Implementations
- Smart Ralph: https://github.com/tzachbon/smart-ralph
- ParkerRex Ralph: https://github.com/ParkerRex/ralph-loop
- Universal Ralph: https://github.com/syuya2036/ralph-loop
- Official Plugin: https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum

### Original Concept
- Geoffrey Huntley: https://ghuntley.com/ralph/
- VentureBeat Article: https://venturebeat.com/technology/how-ralph-wiggum-went-from-the-simpsons-to-the-biggest-name-in-ai-right-now

---

## Summary

The Ralph Wiggum Loop is a powerful technique for autonomous agent persistence. Research found significant improvements:

1. **Smart Ralph** adds spec-driven development with multi-phase workflow
2. **ParkerRex** provides reliable external loop pattern
3. **Universal Ralph** enables multi-model support

This implementation combines the best features for maximum effectiveness.

**Key takeaways:**
1. Use structured prompts with clear completion criteria
2. Set appropriate limits (iterations, cost, retries)
3. Consider external mode for reliability
4. Quality gates prevent wasted iterations
5. Monitor progress and adjust parameters

---

*Documentation based on research completed 2026-01-15*
