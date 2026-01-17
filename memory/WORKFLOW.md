# 🦞 TOOL WORKFLOW GUIDE - QUICK REFERENCE

**Purpose:** WHEN to use which tool (decision tree)  
**Updated:** 2026-01-13 16:05 UTC

---

## 🎯 DECISION TREE

```
What do you need?

├── 🔍 FIND INFORMATION I WROTE?
│   └── `qmd search "topic" -c memory` ← PRIMARY! (indexed, with context)
│
├── READ A FILE?
│   └── `bat file.md` (or `read` tool)
│
├── FIND FILES?
│   └── `fd "pattern"` (not `find`)
│
├── QUICK EXISTENCE CHECK?
│   └── `rg "pattern"` (only if qmd too slow)
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
    ├── Know line number → `fe line path.md N "content"`
    ├── Know text, not line → `fe text path.md "old" "new"`
    ├── Fuzzy match needed → `fe text path.md "old" "new" --fuzzy`
    └── AVOID: Native `edit` tool (8.4% error rate)
```

---

## 🔍 QMD: Your PRIMARY Search Tool

**qmd is optimized for YOUR knowledge work:**
- ✅ Searches 63 indexed files
- ✅ Shows context around matches
- ✅ Semantic + keyword search
- ✅ Much better than `rg` for finding your own notes

```bash
# PRIMARY: Search your knowledge
qmd search "topic" -c memory           # Search memories
qmd search "topic" -c workspace        # Search workspace
qmd search "topic" -c sessions         # Search conversation history

# For knowledge work, USE QMD FIRST!
# Only use rg for simple existence checks
```

---

## QUICK REFERENCE

| Need | Tool | When |
|------|------|------|
| 🔍 Find information | `qmd search "topic"` | ALWAYS FIRST for knowledge |
| Quick check | `rg "pattern"` | Only if qmd too slow |
| Read file | `read` tool | Always |
| Find files | `fd pattern` | Finding by name |
| Git | `lazygit` | Visual git ops |
| Web content | `r.jina.ai url` | Static pages |
| Navigate | `z name` | Terminal navigation |
| List | `eza -la` | File listing |
| Edit file (line) | `fe line path.md N "text"` | Know line number |
| Edit file (text) | `fe text path.md "old" "new"` | Exact or --fuzzy |

---

## TOP 5 DAILY TOOLS

1. **`qmd`** - `qmd search "topic"` 🔍 PRIMARY SEARCH!
2. **`zoxide`** - `z partial_name` (90% faster navigation)
3. **`bat`** - `bat file.md` (readable syntax highlighting)
4. **`fd`** - `fd pattern` (50% faster finding)
5. **`lazygit`** - `lazygit` (visual git)

---

## WHY QMD OVER RG?

| Feature | qmd | ripgrep (rg) |
|---------|-----|--------------|
| Indexed | ✅ 63 files | ❌ Full scan |
| Context | ✅ Shows surrounding text | ❌ Line only |
| Semantic | ✅ Understands concepts | ❌ Keywords only |
| Collections | ✅ memory, sessions, workspace | ❌ Single path |
| Speed | ~0.4s | ~0.002s |

**Use qmd for knowledge work. Use rg for simple existence checks.**

---

## SELF-REMINDERS

Before task: "Should I use qmd or rg?"
Answer: **Use qmd first!**

After task: "Did I use the right tool?"

---

## QMD WORKFLOW

```bash
# 1. Search your knowledge
qmd search "memory system" -c memory

# 2. If not found, search workspace
qmd search "deployment" -c workspace

# 3. Still not found? Search conversations
qmd search "discussed" -c sessions

# 4. Only then consider rg for simple check
rg "pattern" --type md
```

---

## DETAILED REFERENCE

| Topic | Reference |
|-------|-----------|
| qmd full docs | `memory/QMD-WORKFLOW.md` |
| Tool catalog | `AGENTS-TOOLS.md` |
| File operations | `TOOLS.md` |
| Research patterns | `AGENTS-RESEARCH.md` |

---

## MEMORY SEARCH WORKFLOW (v2026.1.14+)

When user asks about past decisions, research, or conversations:

### Before (2026.1.11)
1. Read memory files manually
2. Use qmd for keyword search
3. Piece together context

### After (2026.1.14)
1. `memory_search "query"` for semantic search
2. Returns matches with snippets + line numbers
3. Read full context from specific lines

### Example
```
User: "What did we decide about the research framework?"
Me: → memory_search "research framework decision"
    → Results with snippets
    → Read relevant files with line context
    → Provide answer with citations
```

### Configuration (Optional)
```yaml
agents:
  defaults:
    memory:
      vectorSearch: true  # Enable semantic search
```

---

## BEST PRACTICES

✅ DO:
- **🔍 qmd** over rg for knowledge work
- `read` tool over `cat`
- `fe` (with --fuzzy) for edits
- `fd` over `find`
- `lazygit` for visual git
- `zoxide` (z) for navigation
- `r.jina.ai` for web

❌ DON'T:
- Native `edit` tool (use `fe` instead!)
- `rg` for finding information (use qmd!)
- `cat`, `grep`, `find` for simple tasks
- `exec` for file operations

---

**Full details:** `memory/HIGH-IMPACT-TOOLS.md`

🦞 *Use qmd first!*
