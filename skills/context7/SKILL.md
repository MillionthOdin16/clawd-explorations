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

### Run Context7 MCP Server
```bash
# As MCP server (for integration with agents)
context7-mcp --transport stdio

# As HTTP server
context7-mcp --transport http --port 3000
```

### Using the CLI
```bash
uv run {baseDir}/scripts/context7.py index /path/to/codebase
uv run {baseDir}/scripts/context7.py query "How does the memory system work?"
uv run {baseDir}/scripts/context7.py list
```

## Why Context7?

| Feature | Context7 | Current (qmd/rg) |
|---------|----------|------------------|
| Natural language query | ✅ Yes | ❌ Keyword only |
| Codebase-specific | ✅ Yes | ✅ Yes |
| Persistent index | ✅ Redis | ❌ Re-index each time |
| AI-optimized | ✅ Yes | ❌ No |
| Context injection | ✅ Auto | Manual |

## When to Use

| Task | Use This | Alternative |
|------|----------|-------------|
| Natural language Q&A | Context7 | `qmd search` |
| Complex codebase questions | Context7 | `rg "pattern"` |
| Quick keyword search | N/A | `rg` or `qmd` |

## Notes

- Requires Upstash Redis (free tier available)
- First index takes time, subsequent queries are fast
- Works best with well-documented codebases
- Can index multiple codebases

## Files

- `scripts/context7.py` - CLI wrapper
- MCP server: `context7-mcp`

## See Also

- **memory-keeper skill** - Persistent context across sessions
- **Full research:** `memory/MCP-SERVERS-RESEARCH.md`
- **Context7 GitHub:** https://github.com/upstash/context7
