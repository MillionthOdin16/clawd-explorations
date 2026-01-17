---
name: ralph
description: Spec-driven development with task-by-task execution. Transforms feature ideas into structured specs (research, requirements, design, tasks) then executes them autonomously with fresh context per task. Supports parallel task execution with [P] markers.
---

# Ralph Loop Skill

Spec-driven development for autonomous agent workflows. Transform vague feature ideas into executable specs, then execute task-by-task with fresh context.

## When to Use This Skill

Use when you need to:
- **Build features systematically**: Research → Requirements → Design → Tasks → Implementation
- **Execute complex multi-step tasks**: Task-by-task with progress persistence
- **Handle long-running implementations**: Fresh context per task prevents context overflow
- **Parallelize independent tasks**: Mark tasks with [P] for concurrent execution
- **Maintain quality gates**: [VERIFY] checkpoints and POC-first workflow

## Quick Start

```bash
# Smart entry: resume or create new spec
/ralph:start feature-name Add JWT authentication

# Quick mode: auto-generate all specs and execute
/ralph:start "Add user auth" --quick

# Step-by-step
/ralph:new user-auth Add JWT authentication
/ralph:research
/ralph:requirements
/ralph:design
/ralph:tasks
/ralph:implement
```

## Commands

| Command | Purpose |
|---------|---------|
| `/ralph:start [name] [goal]` | Smart entry: resume existing or create new |
| `/ralph:start [goal] --quick` | Quick mode: auto-generate and execute |
| `/ralph:new <name> [goal]` | Create new spec, start research |
| `/ralph:research` | Run/re-run research phase |
| `/ralph:requirements` | Generate requirements from research |
| `/ralph:design` | Generate technical design |
| `/ralph:tasks` | Break design into executable tasks |
| `/ralph:implement` | Execute tasks one-by-one (or parallel) |
| `/ralph:status` | Show all specs and progress |
| `/ralph:switch <name>` | Change active spec |
| `/ralph:cancel` | Cancel loop, cleanup state |
| `/ralph:help` | Show help |

## The Ralph Loop

```
Feature Request
      |
      v
+-----------------+
|    Research     |  <- Analyzes feasibility, codebase, web search
+-----------------+
      |
      v
+-----------------+
|  Requirements   |  <- User stories, acceptance criteria
+-----------------+
      |
      v
+-----------------+
|     Design      |  <- Architecture, patterns, decisions
+-----------------+
      |
      v
+-----------------+
|     Tasks       |  <- POC-first task breakdown
+-----------------+
      |
      v
+-----------------+
|  Implementation |  <- Task-by-task with fresh context
+-----------------+
      |
      v
   Feature Done
```

## Parallel Task Execution

Mark tasks with `[P]` for parallel execution:

```markdown
- [ ] 1.1 [P] First parallel task
- [ ] 1.2 [P] Second parallel task (runs with 1.1)
- [ ] 1.3 [P] Third parallel task (runs with 1.1, 1.2)
- [ ] 1.4 Sequential task (breaks group, runs alone)
- [ ] 1.5 [VERIFY] Checkpoint (never parallel)
```

### Rules
- Consecutive `[P]` tasks form a parallel group
- Non-[P], [VERIFY], or [SEQUENTIAL] tasks break the group
- [VERIFY] and [SEQUENTIAL] override [P] if on same line
- Max 3 concurrent executors per batch
- Partial failures preserve successful task progress

## Sub-Agents

| Agent | File | Role |
|-------|------|------|
| research-analyst | `agents/research-analyst.md` | Web search, codebase analysis |
| product-manager | `agents/product-manager.md` | User stories, acceptance criteria |
| architect-reviewer | `agents/architect-reviewer.md` | Technical design, architecture |
| task-planner | `agents/task-planner.md` | POC-first task breakdown |
| spec-executor | `agents/spec-executor.md` | Autonomous task implementation |
| qa-engineer | `agents/qa-engineer.md` | Quality verification |
| plan-synthesizer | `agents/plan-synthesizer.md` | Plan synthesis |

## Project Structure

```
skills/ralph/
├── SKILL.md                    <- This file
├── agents/                     <- Sub-agent definitions
│   ├── research-analyst.md
│   ├── product-manager.md
│   ├── architect-reviewer.md
│   ├── task-planner.md
│   ├── spec-executor.md
│   ├── qa-engineer.md
│   └── plan-synthesizer.md
├── commands/                   <- Slash command definitions
│   ├── start.md
│   ├── new.md
│   ├── research.md
│   ├── requirements.md
│   ├── design.md
│   ├── tasks.md
│   ├── implement.md
│   ├── status.md
│   ├── switch.md
│   └── cancel.md
├── templates/                  <- Spec file templates
│   ├── research.md
│   ├── requirements.md
│   ├── design.md
│   ├── tasks.md
│   └── progress.md
├── schemas/                    <- Validation schemas
│   └── spec.schema.json
├── hooks/                      <- Lifecycle hooks
│   └── hooks.json
└── scripts/                    <- Utility scripts (future)
```

## Spec Files Location

Specs live in `./specs/` in your project:

```
./specs/
├── .current-spec              <- Active spec name
└── my-feature/
    ├── .ralph-state.json      <- Loop state (deleted on completion)
    ├── .progress.md           <- Progress tracking
    ├── research.md
    ├── requirements.md
    ├── design.md
    └── tasks.md
```

## State Management

- `.ralph-state.json` - Runtime state: phase, taskIndex, parallelGroup, taskResults
- `.progress.md` - Learnings, completed tasks, current status
- `tasks.md` - Task list with checkboxes [ ] / [x]

## POC-First Workflow (Mandatory)

All specs follow 4 phases:

1. **Phase 1: Make It Work** - POC validation, skip tests
2. **Phase 2: Refactoring** - Code cleanup
3. **Phase 3: Testing** - Unit, integration, e2e
4. **Phase 4: Quality Gates** - Lint, types, CI, PR

Quality checkpoints (`[VERIFY]`) inserted every 2-3 tasks.

## Task Format

```markdown
- [ ] 1.1 Task name
  **Do**: Exact implementation steps
  **Files**: File paths to create/modify
  **Done when**: Success criteria
  **Verify**: Command to verify completion
  **Commit**: Conventional commit message
```

## Task Completion Protocol

Spec-executor must output `TASK_COMPLETE` for the stop-handler to advance. If missing, task retries up to 5 times then blocks with error.

### Verification Layers

The stop-handler enforces:
1. **Contradiction detection** - Rejects completion if output mentions manual action
2. **Uncommitted files check** - Validates tasks.md and .progress.md are committed
3. **Checkmark verification** - Confirms task marked [x] in tasks.md
4. **Signal verification** - Requires TASK_COMPLETE

## Parallel Execution Flow

1. Coordinator parses tasks.md for `[P]` markers
2. Detects consecutive parallel groups
3. Spawns multiple spec-executors via Task tool (all in ONE message)
4. Each executor writes to isolated `.progress-task-N.md`
5. Coordinator merges temp files after batch completes
6. Advances taskIndex past entire group

## Example Workflow

```bash
# Start a new spec
/ralph:start analytics-dashboard Build real-time analytics dashboard

# Research phase (auto-runs in quick mode)
/ralph:research

# Generate requirements
/ralph:requirements

# Create design
/ralph:design

# Break into tasks
/ralph:tasks

# Execute (parallel tasks marked with [P])
/ralph:implement

# Check status
/ralph:status

# Switch to different spec
/ralph:switch another-feature
```

## Tips

- Use `--quick` flag for rapid prototyping
- Use `[VERIFY]` for quality checkpoints
- Use `[P]` for independent tasks that can run in parallel
- Use `[SEQUENTIAL]` to force sequential execution even if [P] is present
- Progress persists across sessions via spec files
- Cancel and start fresh with `/ralph:cancel`

## Framework Execution Rules (MANDATORY)

### The Non-Negotiable Rules

1. **DELEGATION IS MANDATORY**
   - You MUST invoke `scripts/spec-executor.py` for task execution
   - You MUST NOT execute tasks yourself directly
   - Even simple tasks require delegation

2. **GIT COMMIT DISCIPLINE**
   - Every task = one commit
   - Use EXACT commit message from **Commit** field
   - Commit tasks.md, progress file, and code together

3. **TASK_COMPLETE SIGNAL**
   - spec-executor MUST output exactly `TASK_COMPLETE`
   - No output = task not complete
   - The stop-hook checks for this signal

4. **STATE FILE MANAGEMENT**
   - Only `scripts/coordinator.py` modifies `.ralph-state.json`
   - spec-executor MUST NOT touch state file
   - Read-only access only

5. **PROGRESS FILE UPDATES**
   - Write to `.progress.md` (or `.progress-task-N.md` for parallel)
   - Follow exact format: ## Completed Tasks, ## Current Task, ## Learnings, ## Next
   - Include commit hash for each completed task

## Helper Scripts

These scripts ENFORCE Ralph framework rules:

### scripts/new-spec.py
```bash
python /home/opc/clawd/skills/ralph/scripts/new-spec.py <name> [goal]
```
Creates new spec with all required files and initializes state.

### scripts/coordinator.py
```bash
python /home/opc/clawd/skills/ralph/scripts/coordinator.py <spec-name>
```
Coordinator implementation:
- Reads state to determine current task
- Invokes spec-executor for each task (DELEGATION)
- Updates state after each task
- Handles parallel task groups

### scripts/spec-executor.py
```bash
python /home/opc/clawd/skills/ralph/scripts/spec-executor.py <spec-name> <task-index> [progress-file]
```
Spec-executor implementation:
- Executes ONE task from tasks.md
- Runs verification command
- Commits with exact commit message
- Updates progress file
- Outputs `TASK_COMPLETE`

## Correct Execution Pattern

```bash
# WRONG ❌ - What I did before:
# - Executed tasks myself
# - No git commits
# - No TASK_COMPLETE signals
# - Modified state directly

# CORRECT ✅ - How to use Ralph framework:
1. python scripts/new-spec.py my-feature "Add auth"
2. Fill in research.md, requirements.md, design.md, tasks.md
3. python scripts/coordinator.py my-feature
   └── Invokes spec-executor.py for each task
   └── spec-executor.py:
       - Executes task
       - Verifies
       - Commits (exact message)
       - Updates progress
       - Outputs TASK_COMPLETE
   └── coordinator.py checks for TASK_COMPLETE
   └── coordinator.py advances taskIndex
4. Repeat until all tasks complete
```

## Related Files

- **Templates**: `templates/*.md` - Spec file structures
- **Schema**: `schemas/spec.schema.json` - State validation
- **Agents**: `agents/*.md` - Sub-agent definitions
- **Commands**: `commands/*.md` - Command implementations
- **Scripts**: `scripts/*.py` - Helper scripts that enforce rules

## Testing

Run unit tests to verify spec-executor functionality:

```bash
python /home/opc/clawd/skills/ralph/scripts/test_spec_executor.py
```

Tests cover:
- Function extraction from **Do** field
- Python code generation
- File name parsing
- Task section parsing
- Integration tests

## Troubleshooting

### Verification Fails
- Check that **Verify** command runs correctly in the spec directory
- Ensure dependencies are installed
- Verify the generated code matches requirements

### Task Not Found
- Check that tasks.md uses proper format (`- [ ] 1.1`)
- Ensure task hasn't already been marked complete

### Commit Failed
- Verify git is initialized
- Check that files exist before committing

### State File Issues
- Never edit `.ralph-state.json` manually
- Let coordinator.py manage state
- If stuck, delete state file and restart

---

## Quick Reference

### Command Cheat Sheet

| Command | Script | Purpose |
|---------|--------|---------|
| Create spec | `new-spec.py <name> <goal>` | Initialize new spec |
| Execute tasks | `coordinator.py <name>` | Run all tasks |
| Single task | `spec-executor.py <name> <idx>` | Run one task |
| Test | `test_spec_executor.py` | Run unit tests |

### File Locations

```
skills/ralph/
├── SKILL.md           ← Main documentation
├── agents/            ← 7 sub-agent definitions
├── commands/          ← 13 slash commands
├── templates/         ← 5 spec templates
├── schemas/           ← JSON schema validation
├── hooks/             ← Stop handler
└── scripts/           ← Python utilities
    ├── new-spec.py
    ├── coordinator.py
    ├── spec-executor.py
    ├── test_spec_executor.py
    └── quick-start.py
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Verification fails | Check verify command syntax |
| Git lock timeout | Wait 30s, git operation in progress |
| State file stuck | Delete `.ralph-state.json` and restart |
| Parallel tasks fail | Ensure tasks marked `[P]` consecutively |

### Environment Variables

None required. All paths are absolute.
