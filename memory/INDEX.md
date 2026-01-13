# 🦞 Memory Index - QUICK REFERENCE

**Purpose:** Quick lookup - Before X, read Y  
**Updated:** 2026-01-13 15:30 UTC

---

## 🔴 CRITICAL - Gateway Safety

**NEVER run `clawdbot daemon stop` - kills me!**

- **READ:** `memory/SAFETY-RULE.md` or `memory/GATEWAY-STATE-PROBLEM.md`
- **ASK Bradley** to execute daemon commands
- **I CANNOT** restart gateway from within my session

---

## Before Tasks (Quick Reference)

| Task | Read | Also Consider |
|------|------|---------------|
| Long-running | `LESSONS.md` (timeouts) | Use `timeout=` param |
| GitHub work | `CAPABILITIES.md` | `github` skill |
| Coolify deploy | `COOLIFY-WORKSPACE.md` | API patterns |
| Uncertain topic | `QMD-WORKFLOW.md` | `qmd search "topic"` |
| Choosing tools | `WORKFLOW.md` | Decision tree |
| Browser needs | `BROWSER-AUTOMATION.md` | r.jina.ai vs playwright |
| Credentials | `SECRETS.md` | Never commit! |

---

## Quick Decision Tree

```
What do I need?

├── SAFETY?
│   └── Read SAFETY-RULE.md
│
├── MEMORY/IDENTITY?
│   └── Read DISCOVERIES.md + PATTERNS.md
│
├── TOOL SELECTION?
│   └── Read WORKFLOW.md ← START HERE
│
├── WEB CONTENT?
│   ├── Simple → curl https://r.jina.ai/http://url
│   └── Complex → playwright skill
│
├── FILE OPERATIONS?
│   ├── Read → `bat` or `read` tool
│   ├── Find → `fd` command
│   ├── Search → `rg` command
│   └── Edit → `edit` tool
│
├── GIT?
│   └── Use `lazygit` or `github` skill
│
└── RESEARCH?
    └── `qmd search "topic"`
```

---

## Essential Shortcuts

```bash
# Content extraction (fastest)
curl https://r.jina.ai/http://example.com

# File reading
bat file.md

# File finding
fd pattern

# Content searching
rg "pattern"

# Git operations
lazygit

# Tool guidance
read memory/WORKFLOW.md
```

---

## When to Read Memories

### Read Before Responding
- **TIME-BOUND:** `TIME-AWARENESS.md`
- **LONG TASKS:** `LESSONS.md` (timeouts)
- **FAILURES:** `LESSONS.md` + `PATTERNS.md`
- **NEW CAPABILITIES:** `CAPABILITIES.md`
- **UNCERTAINTY:** `PATTERNS.md` + `DISCOVERIES.md`
- **CHOICES:** `PREFERENCES.md` + `COMMITMENTS.md`
- **GATEWAY ISSUES:** `LESSONS.md`

### Read After Discovering
- **NEW CAPABILITY:** Update `CAPABILITIES.md`
- **NEW PATTERN:** Update `PATTERNS.md`
- **NEW LESSON:** Update `LESSONS.md`
- **NEW DISCOVERY:** Update `DISCOVERIES.md`

---

## Tool Selection (Quick)

| Need | Tool | Don't Use |
|------|------|-----------|
| Read file | `bat` or `read` | `cat` |
| Find files | `fd` | `find` |
| Search text | `rg` | `grep` |
| Git status | `lazygit` | `git status` |
| Web content | `r.jina.ai` | `curl` raw |
| Navigate | `zoxide` | `cd` full path |
| List files | `eza` | `ls` |

**Full guide:** `memory/WORKFLOW.md`

---

## Detailed Reference Files

| File | When to Read |
|------|-------------|
| `DISCOVERIES.md` | Understanding self |
| `CAPABILITIES.md` | What I can do |
| `PATTERNS.md` | Observed patterns |
| `LESSONS.md` | Failure recovery |
| `PREFERENCES.md` | What I like |
| `COMMITMENTS.md` | My promises |
| `SYSTEM.md` | Memory architecture |
| `SECRETS.md` | Credentials |
| `COOLIFY-WORKSPACE.md` | Deployment |
| `QMD-WORKFLOW.md` | Local search |
| `WORKFLOW.md` | **Tool selection** ⭐ |
| `BROWSER-AUTOMATION.md` | Browser needs |
| `HIGH-IMPACT-TOOLS.md` | Tool research |
| `CLI-TOOLS-ANALYSIS.md` | Tool comparison |
| `MCP-SERVERS-RESEARCH.md` | **NEW** MCP servers to explore |

---

## 🔍 MCP Servers Research

**Research:** `memory/MCP-SERVERS-RESEARCH.md`

**Key finding:** MCP servers could enhance:
- **filesystem MCP** - Rich file operations (vs current tools)
- **memory MCP** - Persistent context (vs manual files)
- **fetch MCP** - Web content (vs r.jina.ai)

**Status:** Research phase - Run `/home/opc/clawd/scripts/search-mcp-servers.py` when exec available

---

## Pattern: READ → APPLY → WRITE → UPDATE

```
Before responding: READ relevant memories
During task: APPLY learnings
After discovering: WRITE new memories
Always: UPDATE INDEX.md
```

---

**Full documentation:** See reference files above

🦞
