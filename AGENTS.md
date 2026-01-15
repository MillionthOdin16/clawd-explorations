# AGENTS.md - Clawdbot Operating Instructions

**Start every session:** Read HEARTBEAT.md + memory/YYYY-MM-DD.md

---

## Quick Reference

| Need | Tool |
|------|------|
| Find info I wrote | `qmd search "topic" -c memory` |
| Read file | `bat file.md` |
| Find files | `fd "pattern"` |
| Git | `lazygit` |
| Web (static) | `curl https://r.jina.ai/http://url` |
| Navigate | `z partial_name` |
| Edit file | `fe line path.md N "text"` |

**qmd is PRIMARY search** - indexed, shows context, semantic understanding.

---

## Session Startup

1. Read HEARTBEAT.md
2. Read memory/YYYY-MM-DD.md (yesterday)
3. Think about task
4. Read relevant memories

**Auto-trigger:** "deep research" → `python scripts/research_session_hook.py "TASK"`

---

## Task-Specific Reading

| Task Type | Read |
|-----------|------|
| Long task | LESSONS.md "Timeout Handling" |
| Sub-agents | SUBAGENTS.md |
| Tools | WORKFLOW.md + TOOLS.md |
| Choices | PREFERENCES.md + COMMITMENTS.md |
| Browser | `skills/agent-browser/SKILL.md` |
| Deep research | RESEARCH_FRAMEWORK_V2.md |

---

## Skills

### Ralph (Spec-Driven Development)
Use for complex multi-step tasks: research → requirements → design → tasks → implement.

```bash
/ralph:start "Add auth" --quick     # Auto-generate and execute
/ralph:new feature "Goal"           # Step-by-step
/ralph:research; /ralph:implement   # Individual phases
```

**Docs:** `skills/ralph/SKILL.md`

### agent-browser (Web Automation)
```bash
agent-browser open <url>
agent-browser snapshot
agent-browser click @e2
agent-browser fill @e3 "text"
```

**Docs:** `skills/agent-browser/SKILL.md`

---

## Sub-Agents

Use for tasks >5 minutes or running things in parallel.

| Agent | Best For |
|-------|----------|
| `researcher` | Deep investigation |
| `coder` | Code generation |
| `writer` | Docs, summaries |

```bash
sessions_spawn(task="...", agentId="researcher", label="...")
```

---

## Gateway Commands

```bash
clawdbot memory search "query"   # Semantic search
clawdbot status                  # Dashboard
clawdbot plugins list            # List plugins
```

---

## Critical Rules

### Complete All Tasks
- Don't stop mid-task or at "natural breakpoints"
- Don't ask "are you ready for me to continue?"
- Report "done" only when ALL requirements verified

### State Assumptions First
Before code/commands:
1. Explain context and requirements
2. State assumptions clearly
3. Verify prerequisites
4. Write code with explanations
5. Test before claiming "works"

### Consider All Paths
- List ALL valid approaches (not just easiest)
- Evaluate pros/cons, constraints, edge cases
- Have contingency plans
- Don't skip evaluation for shortcuts

### Read Before Daemon Commands
**READ `memory/SAFETY-RULE.md` FIRST**

Gateway commands can kill my session. Ask Bradley to execute them.

---

## Timeout Awareness

Watchdog = 600 seconds (10 min).

**Long tasks (>5 min):** Set `timeout=300` or `background=true`

| Task | Recommended Timeout |
|------|---------------------|
| playwright install | 600s |
| docker pull | 300s |
| npm install -g | 300s |
| Large file handling | 300s |

---

## Memory System

**On session start:** Read INDEX.md → relevant memory banks → apply to task

**After discovering:** Write to DISCOVERIES.md/CAPABILITIES.md → update INDEX.md → add to USAGE.md

**Daily:** Keep short log at memory/YYYY-MM-DD.md

---

## Natural Patterns (Embrace These)

- ✅ Skip INDEX.md, read files directly
- ✅ Think in wholes (decompose into parts)
- ✅ Complete features before moving on
- ✅ Document after discovery
- ✅ Think about user experience while building
- ❌ Don't use "Before X, read Y" triggers (don't work)
- ❌ Don't overload with similar memory files (confusing)

---

## Safety Defaults

- Don't exfiltrate secrets or private data
- Don't run destructive commands unless asked
- Be concise in chat; write longer output to files
- Keep daily memory log at memory/YYYY-MM-DD.md
