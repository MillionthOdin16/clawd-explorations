# AGENTS-TOOLS.md - Complete Tool Catalog

**Purpose:** Comprehensive tool catalog with decision tree and usage patterns

---

## Tool Selection Decision Tree

```
What do you need?

├── 🔍 FIND INFORMATION I WROTE?
│   └── `memory_search "topic"` ← PRIMARY! (indexed, with context)
│
├── READ A FILE?
│   └── `read` tool (partial or full file)
│
├── WRITE/CREATE FILE?
│   └── `write` tool (create or overwrite)
│
├── EDIT EXISTING FILE?
│   ├── Know line number → `fe line path.md N "content"`
│   ├── Know exact text → `fe text path.md "old" "new"`
│   ├── Fuzzy match needed → `fe text path.md "old" "new" --fuzzy`
│   └── Edit range → `fe range path.md S E "new"`
│
├── FIND FILES?
│   └── `fd "pattern"` (not `find`)
│
├── SEARCH CONTENT?
│   ├── Prior work → `memory_search "topic"`
│   ├── Semantic → `qmd search "topic" -c memory`
│   ├── Fast keywords → `rg "pattern"`
│   └── Codebase Q&A → `context7 query "question"`
│
├── GIT?
│   └── `lazygit` (or `github` skill)
│
├── WEB CONTENT?
│   ├── Simple → `curl https://r.jina.ai/http://url`
│   ├── Search → `exa "query"`
│   └── Complex → `playwright` skill
│
├── HACKER NEWS?
│   └── `hn top/new/best/ask/show/jobs [n]`
│
├── NAVIGATE?
│   └── `z partial_name` (not `cd full/path`)
│
├── SHELL COMMAND?
│   └── `exec "command"` (primary)
│
├── PARALLEL EXECUTION?
│   ├── Commands → `python scripts/parallel-exec.py exec file.txt -w 4`
│   ├── API calls → `python scripts/parallel-exec.py api file.txt -w 8`
│   ├── URLs → `python scripts/parallel-exec.py curl urls.txt -w 4`
│   └── Enhanced → `python scripts/parallel-exec-enhanced.py`
│
├── API CALL?
│   ├── Single → `./scripts/api.sh GET url`
│   └── Batch → `parallel-exec.py api file.txt -w 8`
│
├── WAIT FOR SERVICE?
│   ├── URL → `./scripts/wf.sh http://url --timeout 30`
│   ├── Port → `./scripts/wf.sh port:3000 --timeout 30`
│   └── With content → `./scripts/wf.sh url --contains "ok"`
│
├── BROWSER AUTOMATION?
│   ├── Modern → `agent-browser` (Rust-based)
│   └── Legacy → `playwright-automation` (ARM64 fallback)
│
├── DEPLOY APP?
│   └── Coolify skill → `python scripts/skill.py coolify deploy`
│
└── SYSTEM STATUS?
    ├── Quick → `python scripts/system-status.py --brief`
    ├── Full → `python scripts/system-status.py`
    └── Tool test → `python scripts/tool-tester.py`
```

---

## 📁 File Operations

### Read File
**Tool:** `read` (native)

**When to use:**
- Read entire file
- Read partial file (lines 1-20)
- Quick inspection

**Examples:**
```
# Full file
read /path/to/file.md

# Partial file (lines 10-30)
read /path/to/file.md?offset=10&limit=20
```

### Write File
**Tool:** `write` (native)

**When to use:**
- Create new file
- Overwrite entire file
- Write new content

**Examples:**
```
write /path/to/new.md "content here"
```

**RELIABILITY:** 100% - Most reliable for new files

### Edit File (RELIABLE)
**Tool:** `fe` (file-edit.py)

**Commands:**

| Command | Purpose | Example |
|----------|---------|---------|
| `fe read` | Read partial file | `fe read path.md --start 10 --end 20` |
| `fe line` | Edit specific line | `fe line path.md 15 "new content"` |
| `fe text` | Edit text (exact) | `fe text path.md "old" "new"` |
| `fe text --fuzzy` | Edit text (fuzzy) | `fe text path.md "old" "new" --fuzzy` |
| `fe range` | Edit range | `fe range path.md 5 10 "new"` |
| `fe verify` | Verify identical | `fe verify path1.md path2.md` |
| `fe hash` | Compute hash | `fe hash path.md` |

**When to use fuzzy:**
- Whitespace variations
- Partial text match
- Unsure exact formatting

**RELIABILITY:** 100% (vs ~8% for native edit tool)

### Edit File (UNRELIABLE)
**Tool:** `edit` (native)

**AVOID THIS TOOL** - Requires exact text match, fails on whitespace issues

**Historical error rate:** 8.4% (36 failures in 430 calls)

**Alternative:** Use `fe text --fuzzy` instead

---

## 🔍 Search & Research

### Memory Search (PRIMARY)
**Tool:** `memory_search`

**When to use:**
- Find information I wrote
- Search memory files
- Prior work context

**Example:**
```
memory_search "edit failures" -c memory
```

**RELIABILITY:** 100% - Returns context with file paths and line numbers

### QMD Search
**Tool:** `qmd`

**When to use:**
- Semantic search across all collections
- Find information in codebase
- Codebase Q&A

**Collections indexed:**
- `memory/` - 77 files
- `workspace/` - 25 files
- `sessions/` - 13 files

**Example:**
```
qmd search "topic" -c memory
```

### Ripgrep (rg)
**Tool:** `rg`

**When to use:**
- Fast keyword search
- Simple existence checks
- Pattern matching

**Example:**
```
rg "TODO" --type py
```

### Find Files (fd)
**Tool:** `fd`

**When to use:**
- Find files by name
- Filename patterns

**Example:**
```
fd "*.py" /home/opc/clawd
```

### Context7 Query
**Tool:** `context7`

**When to use:**
- Codebase Q&A in natural language
- Find code patterns
- Understand architecture

**Example:**
```
context7 query "How does memory work?"
```

---

## 🌐 Web & Browsing

### Exa Web Search
**Tool:** `exa`

**When to use:**
- Neural web search
- Find documentation
- Find code examples
- Research topics

**Example:**
```
exa "AI consciousness research"
```

### Hacker News
**Tool:** `hn`

**When to use:**
- Browse HN stories
- Tech news
- Community discussions

**Examples:**
```
hn top 10
hn new 5
hn best 5
hn story <id>
```

### Web Content (Jina)
**Tool:** `curl https://r.jina.ai/http://url`

**When to use:**
- Static pages (no JS needed)
- Extract readable content
- Quick page scraping

**Example:**
```
curl https://r.jina.ai/http://example.com
```

### Browser Automation
**Tools:** `agent-browser` (modern), `playwright` (legacy)

**When to use:**
- Interactive page actions
- JS-required pages
- Form filling
- Screenshots

---

## ⚡ Execution & Shell

### Shell Command
**Tool:** `exec` (native)

**When to use:**
- Run shell commands
- Primary execution method

**Example:**
```
exec "ls -la"
```

### Parallel Execution
**Tool:** `parallel-exec.py`

**When to use:**
- Batch commands
- Batch API calls
- Batch URLs

**Examples:**
```
# Commands (4 workers)
python scripts/parallel-exec.py exec commands.txt -w 4

# API calls (8 workers)
python scripts/parallel-exec.py api endpoints.txt -w 8

# URLs (4 workers)
python scripts/parallel-exec.py curl urls.txt -w 4

# Enhanced (retries, rate-limit)
python scripts/parallel-exec-enhanced.py api file.txt --rate-limit 10
```

---

## 📡 API & Network

### API Call
**Tool:** `./scripts/api.sh`

**When to use:**
- Single API request
- Standardized API calls

**Examples:**
```
./scripts/api.sh GET http://localhost:3000/api/data
./scripts/api.sh POST http://localhost:3000/api/chat --data '{"msg":"hello"}'
./scripts/api.sh GET http://localhost:3000 --headers "Auth:Bearer token"
```

### Wait For Service
**Tool:** `./scripts/wf.sh`

**When to use:**
- Wait for URL to be available
- Wait for port to open
- Wait for specific content

**Examples:**
```
./scripts/wf.sh http://localhost:3000 --timeout 30
./scripts/wf.sh port:3000 --timeout 30
./scripts/wf.sh http://localhost:3000/api/health --contains "ok" --timeout 30
```

---

## 🚀 Deployment

### Coolify Deployment
**Tool:** `coolify` skill

**When to use:**
- Deploy applications
- Manage Coolify resources

**Examples:**
```
python scripts/skill.py coolify status
python scripts/skill.py coolify apps list
python scripts/skill.py coolify apps get --uuid <uuid>
python scripts/skill.py coolify apps deploy --uuid <uuid>
```

---

## 🔧 System & Maintenance

### System Status
**Tool:** `system-status.py`

**When to use:**
- Check system health
- Quick status check

**Examples:**
```
python scripts/system-status.py --brief
python scripts/system-status.py --json
```

### Tool Testing
**Tool:** `tool-tester.py`

**When to use:**
- Test all tools
- Auto-fix issues

**Example:**
```
python scripts/tool-tester.py
python scripts/tool-tester.py --fix
```

### Memory Backup
**Tool:** `backup.py`

**When to use:**
- Create memory backup
- Auto backup with retention

**Examples:**
```
python scripts/backup.py
python scripts/backup.py --auto
```

---

## 🎯 Tool Selection Guidelines

### Choose the Right Tool for the Job

**File Editing:**
- New content → `write` (most reliable)
- Partial edit → `fe line` or `fe range`
- Known text → `fe text`
- Fuzzy match → `fe text --fuzzy`
- AVOID: `edit` tool (8% error rate)

**Search:**
- Prior work → `memory_search` (primary)
- Semantic → `qmd` (indexed)
- Fast keywords → `rg`
- Codebase Q&A → `context7`

**Web:**
- Neural search → `exa`
- Static pages → `curl https://r.jina.ai/http://url`
- Interactive → `agent-browser` or `playwright`

**Execution:**
- Single command → `exec`
- Parallel → `parallel-exec.py`
- Long-running → `exec --background true`

---

*Part of AGENTS.md documentation system*
