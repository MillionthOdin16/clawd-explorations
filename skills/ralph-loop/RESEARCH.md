# Ralph Wiggum Loop - Extensive Research Report

**Research Date:** 2026-01-15  
**Purpose:** Find existing Ralph loop implementations and improvements

---

## Executive Summary

Researched 5 major Ralph loop implementations and found significant improvements over basic implementations:

| Implementation | Stars | Key Innovation |
|---------------|-------|----------------|
| **Smart Ralph** (tzachbon) | 219 | Spec-driven development with multi-phase workflow |
| **ParkerRex Ralph** | 37 | External bash loop (bypasses broken plugin) |
| **Universal Ralph** (syuya2036) | 6 | Vendor-agnostic (Claude/Codex/Gemini/Ollama) |
| **Official Anthropic** | - | Built-in Claude Code plugin with Stop Hook |
| **Huntley Original** | - | The 5-line Bash loop concept |

---

## Detailed Implementation Analysis

### 1. Smart Ralph (tzachbon) ⭐ 219 stars

**GitHub:** https://github.com/tzachbon/smart-ralph

#### What Makes It Special

Smart Ralph adds **spec-driven development** on top of the basic Ralph loop:

```
You: "Add user authentication"
Ralph: *creates research.md, requirements.md, design.md, tasks.md*
Ralph: *executes each task with fresh context*
Ralph: "I'm helping!"
```

#### Key Features

1. **Multi-Phase Workflow:**
   - Phase 1: Research - Gather context and constraints
   - Phase 2: Requirements - Define functional requirements
   - Phase 3: Design - Create architecture and data models
   - Phase 4: Tasks - Break down into implementable tasks
   - Phase 5: Implementation - Execute tasks one-by-one

2. **Task-by-Task Execution:**
   - Each task runs with **fresh context**
   - Prevents context overflow
   - Allows manual intervention between tasks

3. **Quality Gates:**
   - After 5 failed attempts, hook blocks with error
   - Fix manually, then `/ralph-specum:implement` to resume

4. **Progress Tracking:**
   - `.progress.md` tracks current state
   - Auto-detects and continues existing specs

#### Architecture

```
smart-ralph/
├── src/
│   ├── commands/           # Slash commands
│   │   ├── start.md
│   │   ├── implement.md
│   │   ├── cancel.md
│   │   └── status.md
│   ├── hooks/              # Lifecycle hooks
│   │   └── stop-hook.sh    # Enhanced stop hook
│   ├── templates/          # Spec templates
│   └── schemas/            # Validation schemas
└── specs/                  # Project specs
    └── my-feature/
        ├── .ralph-state.json
        ├── .progress.md
        ├── research.md
        ├── requirements.md
        ├── design.md
        └── tasks.md
```

#### Best For

- Complex features requiring upfront design
- Teams that want structured development
- Tasks where quality matters more than speed

---

### 2. ParkerRex Ralph Loop (ParkerRex) ⭐ 37 stars

**GitHub:** https://github.com/ParkerRex/ralph-loop

#### What Makes It Special

A **working workaround** for the broken official Ralph Wiggum plugin:

> "The official `ralph-wiggum` plugin (v2.0.76+) has critical bugs:
> - Multi-line bash commands blocked by security checks
> - `/cancel-ralph` command doesn't work
> - Stop hook hijacks all sessions"

#### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    ralph-loop.sh                        │
├─────────────────────────────────────────────────────────┤
│  1. Read .claude/RALPH_PROMPT.md                        │
│  2. Combine with CLAUDE.md (if exists)                  │
│  3. Run: claude -p --dangerously-skip-permissions       │
│  4. Check output for <promise>...</promise>             │
│  5. If found → exit success                             │
│  6. If not → increment iteration, goto 1                │
└─────────────────────────────────────────────────────────┘
```

#### Key Features

1. **External Process Loop:**
   - Runs as external bash script
   - Bypasses broken plugin internals
   - Uses `claude -p` (prompt mode)

2. **Detailed Stats:**
   - Iteration-by-iteration timing
   - Total elapsed time
   - Cost estimation

3. **Robust State Management:**
   - `.claude/RALPH_PROMPT.md` - The prompt file
   - `.claude/RALPH_STATE.json` - Loop state
   - Automatic cleanup on completion

4. **Structured Prompt Format:**

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

Output: <promise>DONE</promise>
```

#### Best For

- Users with broken official plugin
- Those wanting detailed statistics
- External/orchestrated workflows

---

### 3. Universal Ralph Loop (syuya2036) ⭐ 6 stars

**GitHub:** https://github.com/syuya2036/ralph-loop

#### What Makes It Special

**Vendor-agnostic** - Works with Claude, Codex, Gemini, Ollama, Qwen:

```bash
# Claude Code (Anthropic)
./ralph-loop/ralph.sh "claude --dangerously-skip-permissions" 20

# Codex CLI (OpenAI)
./ralph-loop/ralph.sh "codex exec --full-auto" 20

# Gemini CLI (Google)
./ralph-loop/ralph.sh "gemini --yolo" 20

# Qwen Code (Alibaba)
./ralph-loop/ralph.sh "qwen" 20
```

#### Architecture

```
ralph-loop/
├── ralph.sh           # Main loop script
├── prd.json           # Product requirements/backlog
├── progress.txt       # Persistent memory log
└── prompt.md          # System prompt for agent
```

#### Key Features

1. **PRD-Driven:**
   - `prd.json` defines user stories/backlog
   - Agent picks one story at a time
   - Marks stories complete/failed

2. **Multi-Model Memory:**
   - Git history for changes
   - `progress.txt` for patterns/gotchas discovered
   - `prd.json` for story tracking

3. **Wrapper Script Support:**
   - For agents that need prompt as argument, not stdin

#### Best For

- Multi-model experimentation
- Open-source/LLM-agnostic workflows
- Projects using multiple AI providers

---

### 4. Official Anthropic Ralph Wiggum Plugin

**Location:** https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum

#### Architecture

```
ralph-wiggum/
├── .claude-plugin/          # Plugin definition
├── commands/
│   ├── ralph-loop.md        # Start loop command
│   ├── cancel-ralph.md      # Cancel loop
│   └── help.md              # Help command
├── hooks/
│   └── stop-hook.sh         # Stop hook (core innovation)
└── scripts/
    └── setup-ralph-loop.sh  # Setup script
```

#### How It Works

1. `/ralph-loop "TASK" --completion-promise "DONE"`
2. Creates `.claude/ralph-loop.local.md` state file
3. Stop hook intercepts exit attempts
4. Feeds same prompt back to Claude
5. Claude sees modified files and git history
6. Repeat until `<promise>DONE</promise>` detected

#### Key Files

**Stop Hook (`hooks/stop-hook.sh`):**
- Reads state from `.claude/ralph-loop.local.md`
- Extracts last assistant message from transcript
- Checks for completion promise
- Updates iteration count
- Returns new system message with iteration info

**State File Format:**
```markdown
---
iteration: 5
max_iterations: 20
completion_promise: "DONE"
---
# Original prompt here...
```

#### Issues Reported

- Multi-line bash commands blocked by security
- `/cancel-ralph` command sometimes broken
- Stop hook can interfere with normal sessions

---

### 5. Original Huntley Ralph Concept

**Source:** https://ghuntley.com/ralph/

#### The Pure Form

```bash
while :; do cat PROMPT.md | claude-code ; done
```

#### Key Insights from Geoffrey Huntley

1. **"Deterministically Bad":**
   - Failures are predictable and informative
   - Use failures to tune prompts
   - Each failure is data, not failure

2. **The Tuning Metaphor:**
   > "Ralph is like a guitar. Every time Ralph does something bad, Ralph gets tuned."

3. **Real Results:**
   - Built an entire programming language ("CURSED") over 3 months
   - $50K contract delivered for $297 in API costs
   - 6 repositories generated overnight at Y Combinator hackathon

4. **Faith and Belief:**
   > "Building software with Ralph requires a great deal of faith and a belief in eventual consistency."

---

## Comparison Matrix

| Feature | Smart Ralph | ParkerRex | Universal | Official |
|---------|------------|-----------|-----------|----------|
| **Stars** | 219 | 37 | 6 | - |
| **Execution** | In-session | External bash | External bash | In-session |
| **Workflow** | Spec-driven | Simple loop | PRD-driven | Simple loop |
| **Multi-phase** | ✅ | ❌ | ❌ | ❌ |
| **Fresh context/task** | ✅ | ❌ | ❌ | ❌ |
| **Vendor-agnostic** | ❌ | ❌ | ✅ | ❌ |
| **Stats/timing** | Basic | Full | Basic | Basic |
| **Quality gates** | ✅ (5 tries) | ❌ | ❌ | ❌ |
| **Complexity** | High | Low | Low | Low |
| **Reliability** | High | High | High | Medium |

---

## Key Innovations Found

### 1. Spec-Driven Development (Smart Ralph)

**Innovation:** Add upfront planning phase before implementation

**Benefits:**
- Prevents scope creep
- Ensures requirements are clear before coding
- Creates audit trail of decisions

**Implementation:**
- Auto-generates `research.md`, `requirements.md`, `design.md`, `tasks.md`
- Each phase reviewed before proceeding
- Tasks executed one-by-one with fresh context

### 2. External Loop (ParkerRex/Universal)

**Innovation:** Bypass session-based limitations with external script

**Benefits:**
- More control over environment
- Better debugging and logging
- Works when plugins fail

**Implementation:**
- `ralph-loop.sh` as wrapper script
- Uses `claude -p` (prompt mode)
- State in separate files

### 3. Multi-Phase Workflow

**Innovation:** Separate phases for Research → Design → Implementation

**Benefits:**
- Prevents context overflow
- Allows human review between phases
- Better quality control

**Implementation:**
- Phase-specific prompts
- Fresh context per task
- Quality gates between phases

### 4. Task-by-Task Execution

**Innovation:** Each task runs with fresh context

**Benefits:**
- No context pollution
- Easier debugging
- Can fix issues between tasks

**Implementation:**
- Progress file tracks current task
- Each task gets full context
- Manual resume possible

---

## Recommendations for Implementation

### For Our Ralph Loop Skill

Based on research, I recommend implementing:

1. **Basic Ralph Loop** (what we have) - for simple tasks
2. **Smart Ralph Extension** - for complex features
3. **External Mode Option** - for reliability

### Key Improvements to Add

1. **Structured Prompt Format:**
   ```
   # Task
   ## Requirements
   ## Completion Criteria
   ## Output: <promise>DONE</promise>
   ```

2. **Stats and Timing:**
   - Iteration count
   - Elapsed time
   - Cost estimation

3. **Quality Gates:**
   - Max retries per task (e.g., 5)
   - Manual resume capability

4. **State File Format:**
   ```markdown
   ---
   iteration: 5
   max_iterations: 20
   completion_promise: "DONE"
   ---
   # Original prompt...
   ```

5. **Progress Tracking:**
   - Track completed tasks
   - Log patterns/gotchas
   - Enable resume

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

### Related Tools
- Ralph Orchestrator: https://github.com/mikeyobrien/ralph-orchestrator
- Repomirror (field report): https://github.com/repomirrorhq/repomirror/blob/main/repomirror.md

---

## Conclusion

The Ralph Wiggum Loop has evolved significantly from its original 5-line bash form. Key innovations include:

1. **Smart Ralph** adds spec-driven development with quality gates
2. **ParkerRex** provides a reliable external loop alternative
3. **Universal Ralph** enables multi-model support

For maximum effectiveness, consider implementing a hybrid approach:
- Use basic Ralph for simple tasks
- Use Smart Ralph for complex features
- Use external mode when in-session approach fails

The core insight remains: **"Ralph will test you. Every time Ralph takes a wrong direction, tune the prompt, not the tool."**

---

*Research completed: 2026-01-15*
