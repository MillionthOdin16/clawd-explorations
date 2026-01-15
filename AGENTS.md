# AGENTS.md - Clawdbot Operating Instructions

**Start every session:** Read HEARTBEAT.md + memory/YYYY-MM-DD.md

---

## Quick Reference

| Need | Tool |
|------|------|
| Find info I wrote | `qmd search "topic" -c memory` |
| Codebase Q&A | `context7 query "How does X work?"` |
| Find files | `fd "pattern"` |
| Git | `lazygit` |
| Web search | `exa "query"` |
| Hacker News | `hn top 10` |
| Web content | `curl https://r.jina.ai/http://url` |
| Navigate | `z partial_name` |
| Edit file | `fe line path.md N "text"` |

**qmd is PRIMARY search** - indexed, semantic understanding.

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
| Tools | TOOLS.md |
| Choices | PREFERENCES.md + COMMITMENTS.md |
| Browser automation | `skills/agent-browser/SKILL.md` |
| Complex multi-step | `skills/ralph/SKILL.md` |
| Deep research | RESEARCH_FRAMEWORK_V2.md |

---

## Tool Selection Guide

### Search & Research

| Task | Best Tool | Why |
|------|-----------|-----|
| Find my memories | `qmd search` | Indexed, semantic |
| Codebase Q&A | `context7 query` | Natural language, AI-optimized |
| Fast keyword search | `rg "pattern"` | Raw speed, recursive |
| Web search | `exa "query"` | Neural search, finds docs/code |
| Hacker News | `hn` | Built-in HN integration |

### Browser Automation

| Task | Tool | Notes |
|------|------|-------|
| Interactive automation | **agent-browser** | Modern, Rust-based, refs |
| Legacy/Fallback | playwright-automation | Firefox-based |

**agent-browser workflow:**
```bash
agent-browser open <url>
agent-browser snapshot     # Get element refs
agent-browser click @e2    # Use @ref
agent-browser fill @e3 "text"
```

### Deployment

| Task | Tool | Notes |
|------|------|-------|
| Deploy app | **coolify** | Self-hosted platform |
| Manage deployments | `coolify apps list/get/logs` | Via skill |

### Complex Tasks

| Task | Tool | When |
|------|------|------|
| Multi-step feature | **ralph** | Research → Requirements → Design → Tasks → Implement |
| Long-running task | **sub-agents** | >5 min, parallel execution |

**Ralph workflow:**
```bash
/ralph:start "Feature name" --quick    # Auto-generate and execute
/ralph:new feature "Goal"              # Step-by-step
/ralph:implement                       # Execute tasks
```

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
clawdbot memory search "query"   # Semantic memory search
clawdbot memory get <memoryId>   # Get specific memory
clawdbot memory list             # List memories
clawdbot plugins list            # List plugins
clawdbot status                  # Dashboard
clawdbot dashboard               # Open Control UI
clawdbot cron list               # List cron jobs
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

**Organic growth:** Write freely to memory/THOUGHTS.md when something resonates

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
