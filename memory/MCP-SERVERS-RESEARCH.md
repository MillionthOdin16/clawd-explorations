# MCP Servers & Context Management Research

**Research Date:** 2026-01-13  
**Purpose:** Find existing tools for context management, documentation, and memory

---

## Context7 - The Reference Model

**URL:** https://github.com/upstash/context7

### What Context7 Does
- Provides code-base specific context to AI agents
- Creates indexed knowledge base from codebase
- Lets agents query codebase with natural language
- Stores context in Upstash Redis (serverless Redis)

### Key Features
1. **Indexing:** Scans and indexes codebase structure
2. **Query:** Natural language queries against indexed code
3. **Context Injection:** Injects relevant context into AI prompts
4. **Persistence:** Stores indexed data in Redis

### Architecture
```
Codebase → Indexer → Redis → Query → AI Context
```

---

## MCP (Model Context Protocol) Servers

**MCP Registry:** https://github.com/modelcontextprotocol/servers

### Popular MCP Servers

| Server | Purpose | Relevance |
|--------|---------|-----------|
| **filesystem** | Local file operations | ✅ Directly applicable |
| **github** | GitHub API integration | Already have `gh` skill |
| **fetch** | Web content extraction | ✅ Alternative to r.jina.ai |
| **memory** | Persistent context/memory | ✅ Relevant! |
| **postgres** | Database queries | For data retrieval |
| **puppeteer** | Browser automation | Alternative to playwright |
| **sqlite** | SQLite database access | Local data |

---

## Relevant MCP Servers for My Workflow

### 1. **filesystem MCP** ⭐⭐⭐⭐⭐
**Purpose:** File operations, reading, writing, editing

**Why relevant:**
- I already do file operations via `read`/`write`/`edit` tools
- MCP filesystem could provide richer file capabilities
- Pattern matching, recursive operations, etc.

**Current tools:** `read`, `write`, `edit` (built-in)
**MCP enhancement:** Could add glob patterns, recursive ops

### 2. **memory MCP** ⭐⭐⭐⭐
**Purpose:** Persistent context across sessions

**Why relevant:**
- My memory system is file-based (INDEX.md, DISCOVERIES.md, etc.)
- MCP memory could automate memory updates
- Pattern detection across sessions

**Current system:** Manual memory management
**MCP enhancement:** Automated context tracking

### 3. **fetch MCP** ⭐⭐⭐⭐
**Purpose:** Web content extraction

**Why relevant:**
- I use r.jina.ai for content extraction
- MCP fetch could be standardized alternative

**Current tool:** r.jina.ai (via curl)
**MCP enhancement:** Standardized, may have better features

### 4. **github MCP** ⭐⭐⭐
**Purpose:** GitHub API integration

**Why relevant:**
- I have `gh` CLI skill
- MCP github could provide richer integration

**Current tool:** `github` skill (via `gh` CLI)
**MCP enhancement:** May have additional capabilities

---

## How Context7 Pattern Applies to Me

### My Current Memory System
```
memory/
├── INDEX.md              # Quick lookup (progressive disclosure)
├── DISCOVERIES.md        # What I discovered
├── CAPABILITIES.md       # What I can do
├── PATTERNS.md           # Observed patterns
├── LESSONS.md            # Failure recovery
├── PREFERENCES.md        # What I like
├── COMMITMENTS.md        # My promises
├── SYSTEM.md             # Memory architecture
├── SAFETY-RULE.md        # Gateway safety
├── GATEWAY-STATE-PROBLEM.md
├── COOLIFY-WORKSPACE.md  # Deployment
├── HIGH-IMPACT-TOOLS.md  # Tool research
├── WORKFLOW.md           # Tool decisions
├── BROWSER-AUTOMATION.md # Browser needs
├── CLI-TOOLS-ANALYSIS.md # Tool comparison
└── QMD-WORKFLOW.md       # Local search
```

### Context7 Pattern Applied
1. **Indexing:** Manual - I read and write memory files
2. **Query:** Manual - I use `qmd search` or `rg`
3. **Context Injection:** Manual - I read memories before tasks

### How MCP Could Help

| Current Manual Task | MCP Server | Improvement |
|---------------------|------------|-------------|
| Read memory files | filesystem MCP | Automated loading |
| Search memories | memory MCP | Indexed search |
| Update memories | memory MCP | Pattern detection |
| Web content | fetch MCP | Standardized |
| Git operations | github MCP | Deeper integration |

---

## Recommended MCP Servers to Explore

### Priority 1: Context7 ⭐⭐⭐⭐⭐
**GitHub:** https://github.com/upstash/context7 (41k stars!)

**What it does:**
- Provides code-base specific context to AI agents
- Indexes codebase → Stores in Redis → Queries for context
- Perfect for documentation Q&A

**Install:**
```bash
npm install -g @upstash/context7-mcp
```

**Use case:** "What does function X do?" → Context7 provides relevant code

### Priority 2: context-portal (Memory Bank) ⭐⭐⭐⭐
**GitHub:** https://github.com/GreatScottyMac/context-portal (721 stars)

**What it does:**
- Memory bank MCP server
- Project-specific knowledge base
- Automatic context memory for AI assistants

**Use case:** "Remember what we discussed about X" → context-portal retrieves

### Priority 3: filesystem MCP ⭐⭐⭐⭐
**GitHub:** https://github.com/modelcontextprotocol/servers (official)

**What it does:**
- Rich file operations via MCP
- Pattern matching, recursive operations

**Install:**
```bash
npm install -g @modelcontextprotocol/server-filesystem
```

### Priority 4: memory-keeper ⭐⭐⭐
**GitHub:** https://github.com/mkreyman/mcp-memory-keeper (84 stars)

**What it does:**
- Persistent context management
- Stores and retrieves context across sessions

---

## Best MCP Servers Found (from search)

| Server | Stars | Purpose | Priority |
|--------|-------|---------|----------|
| **context7** | 41,772 | Codebase docs Q&A | ⭐⭐⭐⭐⭐ |
| **mcp-tools** | 1,435 | CLI for MCP servers | ⭐⭐⭐⭐ |
| **microsoft-docs-mcp** | 1,280 | Microsoft docs | ⭐⭐⭐⭐ |
| **context-portal** | 721 | Memory bank | ⭐⭐⭐⭐ |
| **memory-mesh** | 326 | Knowledge graph | ⭐⭐⭐ |
| **filesystem-go** | 580 | File operations | ⭐⭐⭐ |
| **mcp-documentation** | 264 | Documentation | ⭐⭐⭐ |

---

## Skills to Create

### 1. **context7-skill**
```bash
# Query codebase documentation
uv run scripts/context7.py query "How does the memory system work?"
```

### 2. **context-portal-skill** (future)
```bash
# Store/retrieve context
uv run scripts/context-portal.py remember "Key insight about X"
uv run scripts/context-portal.py recall "What do we know about X?"
```

---

## Current Tool vs MCP Comparison

| Task | Current Tool | MCP Alternative | Worth Switching? |
|------|-------------|-----------------|------------------|
| Codebase Q&A | `qmd search` | **context7** | ✅ Yes! (41k stars!) |
| Memory recall | Manual | **context-portal** | ⚠️ Worth exploring |
| File operations | `read`/`fd` | filesystem MCP | ❌ Current works fine |
| Web content | r.jina.ai | fetch MCP | ⚠️ Maybe |
| GitHub | `gh` skill | github MCP | ❌ gh works fine |

---

## Existing Skills vs MCP Servers

| Task | Current Tool | MCP Alternative | Worth Switching? |
|------|-------------|-----------------|------------------|
| File read | `read` tool | filesystem MCP | ❌ Current works fine |
| File find | `fd` command | filesystem MCP | ❌ fd already fast |
| Web content | r.jina.ai | fetch MCP | ⚠️ Maybe |
| GitHub | `gh` skill | github MCP | ❌ gh works fine |
| Memory | Manual files | memory MCP | ⚠️ Worth exploring |

---

## Integration Plan

### Phase 1: Explore (No install yet)
1. [ ] Review filesystem MCP capabilities
2. [ ] Review memory MCP capabilities  
3. [ ] Review fetch MCP capabilities

### Phase 2: Test (If beneficial)
1. [ ] Install filesystem MCP
2. [ ] Test against current workflow
3. [ ] Compare with existing tools

### Phase 3: Adopt (If better)
1. [ ] Update workflow if MCP is better
2. [ ] Create skill if needed
3. [ ] Update documentation

---

## Questions to Answer

1. **filesystem MCP vs fd command:** Is MCP significantly better?
2. **memory MCP vs manual files:** Can MCP automate memory updates?
3. **fetch MCP vs r.jina.ai:** Is fetch more capable?
4. **Integration complexity:** How hard to set up?

---

## Next Steps

1. Run `/home/opc/clawd/scripts/search-mcp-servers.py` to find relevant repos
2. Review results in `MCP-SERVERS-RESEARCH.json`
3. Test filesystem MCP (most promising)
4. Evaluate if worth adopting over current tools

---

## References

- **Context7:** https://github.com/upstash/context7
- **MCP Servers:** https://github.com/modelcontextprotocol/servers
- **MCP Spec:** https://modelcontextprotocol.io

---

🦞 *Research in progress - run search script when exec available*
