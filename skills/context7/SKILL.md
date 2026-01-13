---
name: context7
description: Codebase-specific context for AI agents using Upstash Redis. Indexes documentation and provides relevant context for queries. Perfect for Q&A about codebases.
metadata: {"clawdbot":{"emoji":"📚","requires":{"npm":["@upstash/context7-mcp"]}}}
---

# Context7 - Codebase Q&A

Codebase-specific context provider that indexes documentation and answers questions about your codebase.

## Setup

**Install:**
```bash
npm install -g @upstash/context7-mcp
```

**Configure:** Requires Upstash Redis credentials:
```json
{
  "context7": {
    "upstashRestApiToken": "your-token",
    "upstashRestApiUrl": "https://your-db.upstash.io"
  }
}
```

## Commands

### Index Codebase
```bash
uv run {baseDir}/scripts/context7.py index /path/to/codebase
```

### Query Codebase
```bash
uv run {baseDir}/scripts/context7.py query "How does the memory system work?"
uv run {baseDir}/scripts/context7.py query "What is the heartbeatsystem?"
uv run {baseDir}/scripts/context7.py query "Where is the gateway defined?"
```

### List Indexed Codebases
```bash
uv run {baseDir}/scripts/context7.py list
```

### Remove Index
```bash
uv run {baseDir}/scripts/context7.py remove codebase-id
```

## Examples

### Researching Codebase
```bash
# Index the clawd workspace
uv run scripts/context7.py index /home/opc/clawd

# Ask questions about the codebase
uv run scripts/context7.py query "How does the memory system work?"
uv run scripts/context7.py query "What tools are available?"
uv run scripts/context7.py query "Where is the gateway defined?"
```

### Documentation Q&A
```bash
# Index project docs
uv run scripts/context7.py index ./docs

# Query for information
uv run scripts/context7.py query "What is the deployment process?"
uv run scripts/context7.py query "How do I add a new skill?"
```

## Why Context7?

| Feature | Context7 | Current (qmd/rg) |
|---------|----------|------------------|
| Natural language query | ✅ Yes | ❌ No (keyword only) |
| Codebase-specific | ✅ Yes | ✅ Yes |
| Persistent index | ✅ Redis | ❌ Re-index each time |
| AI-optimized | ✅ Yes | ❌ No |
| Context injection | ✅ Auto | Manual |

## Architecture

```
Codebase → Index (Redis) → Query → Relevant Context → AI
```

## When to Use

| Task | Use This | Alternative |
|------|----------|-------------|
| Natural language Q&A | Context7 | `qmd search` |
| Complex codebase questions | Context7 | `rg "pattern"` |
| Quick keyword search | N/A | `rg` or `qmd` |
| File operations | N/A | `read` tool |

## Notes

- Requires Upstash Redis (free tier available)
- First index takes time, subsequent queries are fast
- Works best with well-documented codebases
- Can index multiple codebases

## Files

- `scripts/context7.py` - CLI interface (create as needed)
- Memory: Context stored in Upstash Redis

## See Also

- **Full research:** `memory/MCP-SERVERS-RESEARCH.md`
- **Context7 GitHub:** https://github.com/upstash/context7
