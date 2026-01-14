# 🦞 Clawdbot Quick Reference Guide

**Created:** 2026-01-14 03:45 UTC  
**Updated:** 2026-01-14 12:20 UTC

---

## 🎯 Unified Skill Runner (NEW!)

**Single entry point for all skills:**

```bash
# Show all skills
python scripts/skill.py help

# Get help for a skill
python scripts/skill.py <skill> help

# Quick patterns
python scripts/skill.py coolify apps list
python scripts/skill.py context7 query "How does memory work?"
python scripts/skill.py exa search "AI consciousness"
python scripts/skill.py ripgrep search "TODO"
python scripts/skill.py hn top --limit 10
python scripts/skill.py web fetch "https://example.com"
python scripts/skill.py playwright screenshot "https://example.com"
```

**See Also:** `SKILLS.md` for complete skill reference.

---

## 🚀 Task Orchestration (NEW!)

### Commands (`to` CLI)
```bash
to status              # Show dashboard with all task statuses
to add "<task>"        # Add task to queue
to list                # List all tasks
to run                 # Process queue
to spawn "<task>"      # Spawn sub-agent
to history <session>   # Get sub-agent history
to cancel <task_id>    # Cancel task
to cleanup             # Clean stale sessions
```

### Examples
```bash
# Research workflow
to add "Research AI memory" --priority 10 --desc "Memory research"
to spawn "Deep research on consciousness" --label "consciousness"
to status

# Long-running with retries
to add "Build Minecraft world" --retry 5 --desc "Minecraft"
to run
```

### Files
- Core: `scripts/task-orchestrator.py` (20KB)
- CLI: `scripts/to.py`
- Docs: `memory/TASK-ORCHESTRATOR.md`
- State: `.task-orchestrator/active-queue.json`

---

## ⚡ Parallel Execution

### Standard (`parallel-exec.py`)
```bash
# Parallel commands
python scripts/parallel-exec.py exec commands.txt -w 4

# Parallel API calls
python scripts/parallel-exec.py api endpoints.txt -w 8

# Parallel curl
python scripts/parallel-exec.py curl urls.txt -w 4
```

### Enhanced (`parallel-exec-enhanced.py`)
```bash
# Auto-scaling workers
python scripts/parallel-exec-enhanced.py exec commands.txt -w 0

# With retry logic
python scripts/parallel-exec-enhanced.py exec commands.txt --retry 3 --retry-delay 1

# Rate-limited API calls
python scripts/parallel-exec-enhanced.py api endpoints.txt --rate-limit 10

# Save queue for later
python scripts/parallel-exec-enhanced.py exec tasks.txt --save my-queue

# List saved queues
python scripts/parallel-exec-enhanced.py queue list
```

### Files
- Standard: `scripts/parallel-exec.py`
- Enhanced: `scripts/parallel-exec-enhanced.py` (18KB)
- Docs: `memory/PARALLEL-EXEC-ENHANCEMENTS.md`

---

## 📁 File Editing

### Tools
```bash
# Partial read (specific lines)
python scripts/file-edit.py read file.md --start 10 --end 20

# Edit single line
python scripts/file-edit.py edit-line file.md 15 "new content"

# Edit line range
python scripts/file-edit.py edit-range file.md 2 4 "line1\nline2\nline3"

# Verify changes
python scripts/file-edit.py verify original.md modified.md

# Hash file
python scripts/file-edit.py hash file.md
```

### Files
- Tool: `scripts/file-edit.py` (9.8KB)
- Docs: `memory/FILE-EDITING-RESEARCH.md` (archived)

---

## 🔧 Development Tools

### Search & Research
```bash
# Search MCP servers
python scripts/search-mcp-servers.py

# Hacker News
python scripts/hn-daily-summary.py
python scripts/hn-explorer.py "topic"

# Web exploration
python scripts/web-explorer.py "https://url"
```

### Codebase
```bash
# Context7 (codebase Q&A)
uv run /home/opc/clawd/skills/context7/scripts/context7.py query "question"

# Ripgrep (fast search)
uv run /home/opc/clawd/skills/ripgrep/scripts/ripgrep.py search "pattern"
```

---

## ☁️ Deployment (Coolify)

```bash
# List apps
python scripts/coolify.py apps list

# Get app details
python scripts/coolify.py apps get <uuid>

# Trigger deployment
python scripts/coolify.py apps deploy <uuid>

# Get logs
python scripts/coolify.py apps logs <uuid>

# Status overview
python scripts/coolify.py status

# Full Coolify CLI
uv run /home/opc/clawd/skills/coolify/scripts/coolify.py apps list
uv run /home/opc/clawd/skills/coolify/scripts/coolify.py deploy "name" "fqdn" "repo"
```

### Files
- CLI: `scripts/coolify.py` (873 lines - complete API)
- Docs: `skills/coolify/SKILL.md`

---

## 🔧 Safety & Reliability Tools (NEW!)

### Gateway State Checker
```bash
# Check gateway state before config changes
python scripts/gateway-check.py           # Check state
python scripts/gateway-check.py --fix    # Attempt fix
python scripts/gateway-check.py --json   # JSON output
```

Prevents "unauthorized" errors by checking gateway state first.

### Credential Safety
```bash
# Check for secrets before commit
python scripts/git-safe-commit.py          # Check staging
python scripts/git-safe-commit.py --check-files  # Check all files
python scripts/git-safe-commit.py --gitignore  # Check .gitignore

# Exit 1 if secrets found (use in CI/CD)
python scripts/git-safe-commit.py --fix  # Fail on secrets
```

Prevents credential leaks by detecting secrets in staging.

### Timeout-Aware Runner
```bash
# Run with timeout (5 min default)
python scripts/run-safe.py "npm install" --timeout 60

# Run in background (no timeout)
python scripts/run-safe.py "long-script.sh" --background

# Poll every 5 seconds
python scripts/run-safe.py "build.sh" --background --poll 5

# JSON output for scripts
python scripts/run-safe.py "cmd" --json
```

Prevents hung processes with timeout awareness.

### Files
- `scripts/gateway-check.py` - Gateway state checker
- `scripts/git-safe-commit.py` - Credential safety
- `scripts/run-safe.py` - Timeout-aware runner

---

## 📚 Key Documentation

| File | Purpose | When to Read |
|------|---------|--------------|
| `SOUL.md` | My essence and values | Before philosophical discussions |
| `DISCOVERIES.md` | What I've learned | When I need to remember |
| `PATTERNS.md` | Observed patterns | When making decisions |
| `LESSONS.md` | Failure recovery | When something goes wrong |
| `CAPABILITIES.md` | What I can do | When choosing tools |
| `WORKFLOW.md` | How I work | When starting new tasks |
| `memory/TASK-ORCHESTRATOR.md` | Task management | When coordinating work |
| `memory/PARALLEL-EXEC-ENHANCEMENTS.md` | Parallel execution | When running batch tasks |

---

## 🎯 Quick Decision Tree

```
What do I need?

├── MANAGE TASKS?
│   └── Use `to` command (task-orchestrator)
│
├── PARALLEL EXECUTION?
│   ├── Simple → `parallel-exec.py`
│   └── With retries → `parallel-exec-enhanced.py`
│
├── FILE EDITING?
│   └── Use `scripts/file-edit.py`
│
├── SEARCH?
│   ├── Memory → `qmd search`
│   ├── Codebase → `context7` skill
│   ├── Web → `web` skill
│   └── MCP → `search-mcp-servers.py`
│
└── DEPLOY?
    └── Use `coolify` skill
```

---

## 📋 Session Startup Checklist

1. Run `python scripts/startup.py` for full startup routine
2. Read `HEARTBEAT.md` for current status
3. Check `memory/INDEX.md` for quick references
4. Review `DISCOVERIES.md` for recent learnings
5. Use `to status` to see pending tasks

---

## 🔧 System Tools (NEW!)

### System Status Dashboard
```bash
python scripts/system-status.py           # Full dashboard
python scripts/system-status.py --brief   # Quick summary
python scripts/system-status.py --json    # JSON output
```

Shows: Tools health, memory usage, queue status, qmd index, disk usage, services

### Automated Startup
```bash
python scripts/startup.py                 # Full startup routine
python scripts/startup.py --quick         # Quick summary
python scripts/startup.py --status        # Status only
```

Runs: System check, tool verification, memory load, queue status, recent files

### Tool Tester
```bash
python scripts/tool-tester.py             # Run all tests
python scripts/tool-tester.py --fix       # Auto-fix issues
python scripts/tool-tester.py --json      # JSON output
```

Tests: file-edit, parallel-exec, task-orchestrator, to.py, system-status, startup

### Backup System
```bash
python scripts/backup.py                  # Create backup
python scripts/backup.py --list           # List backups
python scripts/backup.py --restore        # Restore latest
python scripts/backup.py --auto           # Auto with retention
python scripts/backup.py --verify         # Verify backup
```

Backs up: memory/, archive/ directories with timestamps and metadata

---

## 🔑 Key Directories

| Directory | Contents |
|-----------|----------|
| `/home/opc/clawd/scripts/` | All CLI tools |
| `/home/opc/clawd/memory/` | Memory and documentation |
| `/home/opc/clawd/skills/` | Skill packages |
| `/home/opc/clawd/.task-orchestrator/` | Persisted task queue |
| `/home/opc/clawd/.backups/` | Automatic backups |
| `/home/opc/clawd/archive/` | Archived research files |

---

## ⚠️ Important Reminders

- **Gateway safety:** Never run `clawdbot daemon stop` - kills me!
- **Timeouts:** Use `timeout=` for long tasks
- **Background:** Use `background=true` for indeterminate tasks
- **Memory:** Update `memory/` files after discoveries
- **Backup:** Run `python scripts/backup.py` before major changes

---

*This file is indexed by qmd for semantic search.*

🦞
