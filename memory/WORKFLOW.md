# 🦞 TOOL WORKFLOW GUIDE - QUICK REFERENCE

**Purpose:** WHEN to use which tool (decision tree)  
**Updated:** 2026-01-13 15:30 UTC

---

## 🎯 DECISION TREE

```
What do you need?

├── READ A FILE?
│   └── `bat file.md` (or `read` tool)
│
├── FIND FILES?
│   └── `fd "pattern"` (not `find`)
│
├── SEARCH TEXT?
│   └── `rg "pattern"` (not `grep`)
│
├── GIT?
│   └── `lazygit` (or `github` skill)
│
├── WEB CONTENT?
│   ├── Simple → `curl https://r.jina.ai/http://url`
│   └── Complex → `playwright` skill
│
├── NAVIGATE?
│   └── `z partial_name` (not `cd full/path`)
│
├── LIST FILES?
│   └── `eza -la` (not `ls -la`)
│
└── EDIT FILE?
    └── Use `edit` tool (not `exec`)
```

---

## QUICK REFERENCE

| Need | Do This | Don't Do |
|------|---------|----------|
| Read file | `bat file` | `cat file` |
| Find files | `fd pattern` | `find . -name` |
| Search text | `rg "text"` | `grep -r` |
| Git status | `lazygit` | `git status` |
| Web content | `r.jina.ai url` | `curl url` |
| Navigate | `z name` | `cd /long/path` |
| List | `eza -la` | `ls -la` |
| Edit | Use `edit` tool | `exec sed/awk` |

---

## TOP 5 DAILY TOOLS

1. **`zoxide`** - `z partial_name` (90% faster navigation)
2. **`ripgrep`** - `rg "pattern"` (80% faster search)
3. **`bat`** - `bat file.md` (readable syntax highlighting)
4. **`fd`** - `fd pattern` (50% faster finding)
5. **`lazygit`** - `lazygit` (visual git)

---

## SELF-REMINDERS

Before task: "What tool should I use?"
After task: "Use the right tool next time"

---

## DETAILED REFERENCE

| Topic | Reference |
|-------|-----------|
| Tool comparison | `HIGH-IMPACT-TOOLS.md` |
| Installation | `HIGH-IMPACT-TOOLS.md` (Phase 1-3) |
| Efficiency gains | `HIGH-IMPACT-TOOLS.md` |
| Browser needs | `BROWSER-AUTOMATION.md` |
| Git workflow | Use `lazygit` |
| Tool docs | Run `--help` on each tool |

---

## BEST PRACTICES

✅ DO:
- `bat` over `cat`
- `rg` over `grep`
- `fd` over `find`
- `lazygit` for visual git
- `zoxide` for navigation
- `r.jina.ai` for web

❌ DON'T:
- `cat`, `grep`, `find` for simple tasks
- `exec` for file operations
- raw `curl` for web scraping

---

**Full details:** `memory/HIGH-IMPACT-TOOLS.md`

🦞
