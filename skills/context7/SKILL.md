---
name: context7
description: Codebase-specific context for AI agents using Upstash Redis. Indexes documentation and provides relevant context for queries. Perfect for Q&A about codebases.
metadata: {"clawdbot":{"emoji":"📚","installed":"✅ Installed via npm","requires":{"env":["CONTEXT7_API_KEY","UPSTASH_REST_API_TOKEN"]}}}
---

# Context7 - Codebase Q&A

Codebase-specific context provider that indexes documentation and answers questions about your codebase.

## Status

**✅ INSTALLED** via npm
```bash
npm install -g @upstash/context7-mcp
which context7-mcp  # /home/opc/.nvm/versions/node/v22.20.0/bin/context7-mcp
```

## Setup

**Environment variables required:**
```bash
export CONTEXT7_API_KEY="your-api-key"
export UPSTASH_REST_API_TOKEN="your-redis-token"
export UPSTASH_REST_API_URL="https://your-db.upstash.io"
```

## Usage

### CLI Commands
```bash
# Index a codebase
uv run {baseDir}/scripts/context7.py index /path/to/codebase

# Query the codebase
uv run {baseDir}/scripts/context7.py query "How does the memory system work?"

# List indexed codebases
uv run {baseDir}/scripts/context7.py list

# Clear index
uv run {baseDir}/scripts/context7.py clear
```

### Unified Runner
```bash
# Using skill.py (preferred)
python scripts/skill.py context7 query "How does memory work?"

# Direct
uv run {baseDir}/scripts/context7.py query "How does memory work?"
```

## Common Patterns

### Pattern 1: Ask about a file
```bash
python scripts/skill.py context7 query "How does TOOLS.md work?"
```

### Pattern 2: Understand a system
```bash
python scripts/skill.py context7 query "Explain the memory architecture"
```

### Pattern 3: Find implementation
```bash
python scripts/skill.py context7 query "Where is the qmd search implemented?"
```

### Pattern 4: Quick code lookup
```bash
python scripts/skill.py context7 query "What does the exec function do?"
```

## Efficiency Tips

1. **Natural language works** - Ask full questions, not keywords
2. **Be specific** - "How does the memory consolidation work?" > "memory"
3. **Use context** - Reference files you want to understand
4. **Chain queries** - Ask follow-up questions for deeper understanding

## When to Use

| Task | Use This | Alternative |
|------|----------|-------------|
| Natural language Q&A | Context7 | `qmd search` |
| Complex codebase questions | Context7 | `rg "pattern"` |
| Quick keyword search | N/A | `rg` or `qmd` |

## Why Context7?

| Feature | Context7 | Current (qmd/rg) |
|---------|----------|------------------|
| Natural language query | ✅ Yes | ❌ Keyword only |
| Codebase-specific | ✅ Yes | ✅ Yes |
| Persistent index | ✅ Redis | ❌ Re-index each time |
| AI-optimized | ✅ Yes | ❌ No |
| Context injection | ✅ Auto | Manual |

## Quick Reference

| Command | Description |
|---------|-------------|
| `skill.py context7 query "..."` | Ask a question |
| `skill.py context7 index /path` | Index codebase |
| `skill.py context7 list` | List indexes |

## Files

- `scripts/context7.py` - CLI wrapper
- MCP server: `context7-mcp`

## See Also

- **memory-keeper skill** - Persistent context across sessions
- **Full research:** `memory/MCP-SERVERS-RESEARCH.md`
- **Context7 GitHub:** https://github.com/upstash/context7
