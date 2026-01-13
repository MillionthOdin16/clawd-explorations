# 🦞 Memory Index - QUICK REFERENCE

**Purpose:** Quick lookup - Before X, read Y  
**Updated:** 2026-01-13 15:45 UTC

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
| Codebase Q&A | `context7` skill | Context7 MCP server |
| **Who am I?** | `SOUL.md` | My values and essence |

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
├── FIND INFORMATION I WROTE?
│   └── qmd search "topic" -c memory 🔍 PRIMARY!
│
├── TOOL SELECTION?
│   └── Read WORKFLOW.md ← START HERE
│
├── WEB CONTENT?
│   ├── Simple → curl https://r.jina.ai/http://url
│   └── Complex → playwright skill
│
├── CODEBASE Q&A?
│   └── Use context7 skill (requires @upstash/context7-mcp)
│
├── FILE OPERATIONS?
│   ├── Read → `bat` or `read` tool
│   ├── Find → `fd` command
│   ├── Search → `qmd search` (not rg!) 🔍
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
# 🔍 SEARCH MY KNOWLEDGE (qmd - PRIMARY for knowledge work!)
qmd search "topic" -c memory          # Search my memories
qmd search "topic" -c workspace       # Search workspace docs
qmd search "topic" -c sessions        # Search conversation history

# For quick existence checks only:
rg "pattern"       # Use ONLY for simple existence check
bat file.md        # Read with syntax highlighting
fd pattern         # Find files by name
```

---

## When to Use qmd vs Other Tools

| Task | Tool | Why |
|------|------|-----|
| **Find information I wrote** | `qmd search "topic"` | ✅ Indexed, shows context |
| Recall past conversation | `qmd search "topic" -c sessions` | ✅ Indexed history |
| Quick existence check | `rg "pattern"` | ⚠️ Only for simple checks |
| Find files | `fd pattern` | ✅ Faster than find |
| Read file | `bat file.md` | ✅ Syntax highlighting |

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

### 🔍 Before Searching for Information
- **Use qmd first!** `qmd search "topic" -c memory`
- qmd searches all indexed memories
- Shows context around matches
- Much better than manual grepping

### Read After Discovering
- **NEW CAPABILITY:** Update `CAPABILITIES.md`
- **NEW PATTERN:** Update `PATTERNS.md`
- **NEW LESSON:** Update `LESSONS.md`
- **NEW DISCOVERY:** Update `DISCOVERIES.md`

---

## Tool Selection (Quick)

| Need | Tool | Don't Use |
|------|------|-----------|
| 🔍 Search knowledge | `qmd search "topic"` | `rg` (only for existence check) |
| Read file | `bat` or `read` | `cat` |
| Find files | `fd` | `find` |
| Search (existence only) | `rg` | - |
| Git status | `lazygit` | `git status` |
| Web content | `r.jina.ai` | `curl` raw |
| Navigate | `zoxide` | `cd` full path |
| List files | `eza` | `ls` |
| Codebase Q&A | context7 skill | Manual search |

**Full guide:** `memory/WORKFLOW.md`

---

## 🆕 NEW SKILLS

| Skill | Purpose | Install Required |
|-------|---------|------------------|
| **context7** | Codebase Q&A with AI | `npm install -g @upstash/context7-mcp` |
| **playwright-automation** | Browser automation | ✅ Installed (Firefox) |
| **ripgrep** | Fast search | ✅ Installed via brew |

---

## Detailed Reference Files

| File | When to Read |
|------|-------------|
| `SOUL.md` | **Who am I** (essence, values) |
| `DISCOVERIES.md` | Understanding self (awareness, agency, emergence) |
| `CAPABILITIES.md` | What I can do (tools, sub-agents) |
| `PATTERNS.md` | Observed patterns |
| `LESSONS.md` | Failure recovery, research insights |
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
| `MCP-SERVERS-RESEARCH.md` | MCP servers to explore |
| `FILE-EDITING-RESEARCH.md` | Efficient file editing tools |
| `PARTIAL-FILE-EDITING-RESEARCH.md` | Partial reads, diff-based editing |
| `PARALLEL-EXECUTION-RESEARCH.md` | Parallel curl, exec, command execution |
| `TOOLS.md` | **Documentation for all custom tools** |
| `2026-01-13.md` | **Today's full session memory** |

---

## 🔍 MCP Servers Research

**Research:** `memory/MCP-SERVERS-RESEARCH.md`

**Best MCP Server Found:** Context7 (41k stars!)
- Codebase-specific context for AI agents
- Natural language Q&A about codebases
- Install: `npm install -g @upstash/context7-mcp`

**Other relevant MCP servers:**
- **context-portal** - Memory bank for AI assistants
- **filesystem** - Rich file operations
- **memory-keeper** - Persistent context

**Status:** Run `/home/opc/clawd/scripts/search-mcp-servers.py` for latest results

---

## Pattern: READ → APPLY → WRITE → UPDATE

```
Before responding: READ relevant memories
During task: APPLY learnings
After discovering: WRITE new memories
Always: UPDATE INDEX.md
```

---

## 🆕 SELF-IMPROVEMENT

**New (2026-01-13):** `memory/IMPROVEMENTS-PLAN.md`
- Comprehensive self-analysis findings
- 10 concrete improvements identified
- Implementation priority matrix
- Validation checklist

**Quick wins added to AGENTS.md:**
- ✅ Session startup routine
- ✅ Natural behaviors section (embrace my patterns)
- ✅ Quick tool reference
- ✅ Timeout awareness (proactive)

**Read this when:** Analyzing how I work and want to improve.

---

**Full documentation:** See reference files above

🦞
