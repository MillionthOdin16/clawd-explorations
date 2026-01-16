# MCP Tool Search - Deep Investigation

**Date:** 2026-01-16
**Source:** Anthropic Claude Code MCP Tool Search announcement

---

## The Problem

**Context Explosion from MCP Tools:**

- MCP servers can have 50+ tools
- Users reported setups with 7+ servers consuming 67k+ tokens
- Tool descriptions take up significant context window
- Every tool definition is included in every message, whether used or not

**Real-world Example:**
```
7 MCP servers
├── Context7: 15 tools (codebase Q&A)
├── Filesystem: 10 tools (file operations)
├── Memory: 8 tools (persistent context)
├── Kubernetes: 12 tools (K8s management)
├── Firebase: 6 tools (backend integration)
├── GraphQL: 5 tools (API querying)
└── Terminal: 8 tools (command execution)

Total: 64 tools ~ 67k+ tokens in descriptions alone
```

**Impact:**
- Reduced context for actual work
- Slower inference (more tokens to process)
- Higher costs (especially for premium models)
- Diminishing returns as tool count grows

---

## The Solution: MCP Tool Search

### Core Concept

**Dynamic Loading:** Load tools into context only when they're likely to be needed, instead of preloading all tool definitions.

### How It Works

**1. Context Threshold Detection**
```
- Claude Code monitors total context usage
- When MCP tool descriptions exceed 10% of context window
- Triggers deferred loading mode
- Default enabled, can be disabled
```

**2. Tool Discovery via Search**
```
Instead of:
  "Here are 64 tools with full descriptions..."

Tool Search:
  "When you need a tool, call MCPSearch tool"
  → Returns relevant tools with descriptions
  → Only tools matching the query are loaded
```

**3. Intelligent Tool Matching**
```
User Request: "Query the codebase about memory system"
↓
Model thinks: "I need Context7 tools"
↓
Calls: MCPSearch("codebase query", "context7")
↓
Returns: Relevant Context7 tools only
↓
Model uses: query_context7_tool
```

### Configuration Options

**Auto Threshold:**
```json
{
  "mcp": {
    "toolSearch": "auto:10"  // 10% of context window
  }
}
```

**Disable Tool Search:**
```json
{
  "disallowedTools": ["MCPSearch"]
}
```

---

## For MCP Server Authors

### Server Instructions Become Critical

**Before Tool Search:**
```json
{
  "tools": [...],
  "description": "File operations for project files"
}
```

**With Tool Search:**
```json
{
  "tools": [...],
  "description": "File operations for project files",
  "instructions": "Use when user needs to read, write, or manipulate files in the project directory. Includes file search, content editing, and directory navigation tools."
}
```

**Why:** The "instructions" field helps the model know:
- When to search for tools from this server
- What types of tasks these tools handle
- When to skip this server entirely

### Example: Context7 Server

```json
{
  "name": "context7",
  "description": "Codebase Q&A with Upstash Redis",
  "instructions": "Use when user asks questions about codebase, needs to find implementations, or wants to understand how systems work. Provides natural language queries against indexed documentation.",
  "tools": [
    {
      "name": "query",
      "description": "Query indexed codebase with natural language",
      "inputSchema": {...}
    },
    {
      "name": "index",
      "description": "Index a codebase directory",
      "inputSchema": {...}
    }
  ]
}
```

---

## For MCP Client Authors

### Implementing ToolSearchTool

**Tool Definition:**
```typescript
{
  name: "ToolSearchTool",
  description: "Search for tools from MCP servers by keyword or semantic query",
  inputSchema: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "Search query describing what tools are needed"
      },
      serverFilter: {
        type: "string",
        description: "Optional: restrict search to specific server"
      }
    },
    required: ["query"]
  }
}
```

**Implementation Approach:**

**Option 1: Keyword Matching**
```typescript
async function searchTools(query: string, serverFilter?: string) {
  const results = [];

  for (const server of mcpServers) {
    if (serverFilter && server.name !== serverFilter) continue;

    for (const tool of server.tools) {
      const score = keywordMatch(query, tool);
      if (score > threshold) {
        results.push({ tool, server, score });
      }
    }
  }

  return results.sort((a, b) => b.score - a.score);
}
```

**Option 2: Semantic Search (Recommended)**
```typescript
async function searchTools(query: string, serverFilter?: string) {
  const queryEmbedding = await embed(query);
  const results = [];

  for (const server of mcpServers) {
    if (serverFilter && server.name !== serverFilter) continue;

    for (const tool of server.tools) {
      const toolEmbedding = tool.cachedEmbedding || await embed(tool.description);
      const similarity = cosineSimilarity(queryEmbedding, toolEmbedding);

      if (similarity > 0.7) {  // Threshold
        results.push({ tool, server, score: similarity });
      }
    }
  }

  return results.sort((a, b) => b.score - a.score);
}
```

**Option 3: Hybrid (Claude Code's Approach)**
```typescript
async function searchTools(query: string, serverFilter?: string) {
  // 1. Check server instructions first (broad filter)
  const relevantServers = filterServersByInstructions(query);

  // 2. Search within relevant servers (semantic)
  const results = [];
  for (const server of relevantServers) {
    const serverTools = await semanticSearch(query, server.tools);
    results.push(...serverTools.map(t => ({ tool: t, server })));
  }

  // 3. Fallback to keyword if no results
  if (results.length === 0) {
    return keywordSearch(query, mcpServers);
  }

  return results;
}
```

---

## How This Works for Clawdbot

### Current Tool Architecture

**Clawdbot's Tools:**
```
Native Tools (built-in):
  ├─ read/write/edit (file operations)
  ├─ exec/bash (shell commands)
  ├─ browser (web automation)
  ├─ canvas (node control)
  ├─ nodes (paired devices)
  ├─ cron (scheduled tasks)
  ├─ message (messaging)
  ├─ gateway (gateway control)
  ├─ sessions (session management)
  ├─ memory_search/memory_get (memory system)
  └─ image (image analysis)

Skills (via scripts/):
  ├─ discord
  ├─ slack
  ├─ github
  ├─ notion
  ├─ obsidian
  ├─ weather
  ├─ hn
  ├─ exa
  ├─ ripgrep
  ├─ playwright
  ├─ agent-browser
  └─ context7 (planned)
```

**Total:** ~30 tool endpoints

### Tool Search Opportunity

**Immediate Benefit: Limited**

Reason:
- Clawdbot's tools are **native**, not MCP-based
- Tool descriptions are **internal** to Clawdbot gateway
- Not exposed in the same way as Claude Code's MCP tools

**However:** This pattern is still valuable for:

1. **Future MCP Integration**
   - If Clawdbot adopts MCP protocol for extensibility
   - If skills become MCP servers
   - If we want to support external MCP tools

2. **Optimizing Skill Discovery**
   - Skills are currently loaded as tool endpoints
   - Tool descriptions are included in context
   - Could benefit from lazy loading

3. **Session Tool Filtering**
   - Not all tools are needed in every session
   - Could filter tools based on user's stated intent
   - Dynamic tool loading based on conversation context

---

## Implementation Strategy for Clawdbot

### Option 1: Skill-Level Tool Search

**Concept:** Search and load skills on-demand instead of preloading all.

**How it Would Work:**
```
1. Startup: Load only core tools (read, write, exec, memory)
2. User Message: "Check weather in Boston"
3. Model: Recognizes need for weather tool
4. Call: ToolSearch("weather")
5. Response: Returns weather tool definition
6. Use: Model now has weather tool in context
```

**Benefits:**
- Reduced initial context load
- Faster startup
- Only load what's needed

**Challenges:**
- Need tool search infrastructure
- Tool discovery heuristics
- Latency when loading new tools

### Option 2: MCP Gateway for External Tools

**Concept:** Use MCP protocol for external tools while keeping native tools.

**Architecture:**
```
Clawdbot Gateway
├─ Native Tools (always loaded)
│  ├─ read/write/exec
│  ├─ memory
│  ├─ sessions
│  └─ browser
│
└─ MCP Layer (lazy loaded)
   ├─ Context7 (external MCP server)
   ├─ GitHub (external MCP server)
   ├─ Slack (external MCP server)
   └─ Custom MCP servers
```

**Benefits:**
- Clean separation: core vs external
- Leverage existing MCP ecosystem
- Tool search applies only to MCP tools
- Native tools remain fast (no search overhead)

**Implementation:**
```typescript
// Clawdbot Gateway
class ToolLoader {
  nativeTools: Tool[];  // Always loaded
  mcpToolSearch: ToolSearchTool;  // For MCP tools

  async loadToolsForRequest(request: UserMessage) {
    // 1. Native tools always available
    const tools = this.nativeTools;

    // 2. Check if MCP tools needed
    const needsMCP = this.detectMCPNeed(request);
    if (!needsMCP) return tools;

    // 3. Search for relevant MCP tools
    const mcpTools = await this.mcpToolSearch.search(request);

    // 4. Combine
    return [...tools, ...mcpTools];
  }
}
```

### Option 3: Intent-Based Tool Filtering

**Concept:** Filter tools based on detected intent from conversation.

**How it Works:**
```
1. Analyze conversation for intent categories:
   - Code operations → load file tools, context7
   - Messaging → load discord, slack, message
   - Research → load exa, hn, browser
   - Deployment → load coolify, github
   - System → load exec, gateway

2. Load only tools matching detected intent

3. Update as conversation evolves
```

**Benefits:**
- More relevant tools in context
- Reduced tool pollution
- Faster inference

**Challenges:**
- Intent detection accuracy
- Dynamic tool loading overhead
- May miss edge cases

---

## Proposed Implementation: Hybrid Approach

### Phase 1: MCP Tool Search Foundation (1-2 weeks)

**Goal:** Add ToolSearchTool and MCP integration layer.

**Tasks:**
1. Implement ToolSearchTool
   - Keyword-based search initially
   - Server instructions support
   - Tool metadata caching

2. Add MCP client support
   - MCP protocol client
   - Server connection management
   - Tool discovery

3. Update skill system
   - Skills can expose as MCP servers
   - Optional MCP integration

**Deliverables:**
- ToolSearchTool implementation
- MCP client module
- Documentation for skill authors

### Phase 2: Tool Filtering & Optimization (2-3 weeks)

**Goal:** Reduce tool context based on conversation.

**Tasks:**
1. Intent detection
   - Analyze user request patterns
   - Classify by tool category
   - Update as conversation evolves

2. Dynamic tool loading
   - Load tools on-demand
   - Cache frequently used tools
   - Unload idle tools

3. Metrics & optimization
   - Track tool usage patterns
   - Measure context savings
   - Tune thresholds

**Deliverables:**
- Intent detection system
- Dynamic tool loader
- Tool usage analytics

### Phase 3: Full MCP Ecosystem (ongoing)

**Goal:** Leverage external MCP servers.

**Tasks:**
1. Integrate popular MCP servers
   - Context7 (already planned)
   - Filesystem MCP
   - Memory MCP servers

2. Community contribution
   - Document how to write MCP skills
   - Publish example skills
   - Community marketplace

3. Tool search improvements
   - Semantic search for better matching
   - Learning from usage patterns
   - Adaptive thresholds

**Deliverables:**
- MCP skill ecosystem
- Community resources
- Advanced tool search

---

## Specific Recommendations

### Immediate Actions (This Week)

1. **Research Tool Search Implementation**
   - Study Claude Code's implementation patterns
   - Evaluate search strategies (keyword vs semantic)
   - Prototype simple ToolSearchTool

2. **Audit Tool Descriptions**
   - Review current tool descriptions
   - Add "instructions" field where missing
   - Optimize description length

3. **Tool Usage Analysis**
   - Track which tools are used most
   - Identify rarely-used tools
   - Find opportunity for lazy loading

### Short-term (Next 2-4 Weeks)

1. **Implement Basic ToolSearch**
   - Keyword-based search
   - Server instruction support
   - Tool metadata indexing

2. **Add MCP Client**
   - Basic MCP protocol support
   - Connection management
   - Tool discovery

3. **Convert Context7 Skill to MCP**
   - Test MCP integration
   - Validate tool search workflow
   - Document the pattern

### Long-term (1-3 Months)

1. **Full Skill → MCP Migration**
   - Convert skills to MCP servers
   - Maintain backward compatibility
   - Add tool search to all skills

2. **Semantic Tool Search**
   - Embedding-based search
   - Better tool matching
   - Adaptive learning

3. **Tool Search Analytics**
   - Dashboard for tool usage
   - Optimization recommendations
   - Performance metrics

---

## Potential Risks & Mitigations

### Risk 1: Increased Latency

**Issue:** Tool search adds overhead before tool execution.

**Mitigation:**
- Cache frequently used tools
- Preload likely tools based on conversation context
- Keep search lightweight (keyword first, semantic on-demand)

### Risk 2: Missed Tools

**Issue:** Tool search might not return the right tool.

**Mitigation:**
- Fallback to loading all tools if search fails
- Provide "show all tools" option
- Learn from corrections

### Risk 3: Complexity

**Issue:** Tool search adds system complexity.

**Mitigation:**
- Phase rollout (basic → advanced)
- Comprehensive testing
- Clear documentation

### Risk 4: User Confusion

**Issue:** Users might not understand why tools aren't available.

**Mitigation:**
- Transparent tool loading notifications
- Clear error messages when tool not found
- Documentation explaining the system

---

## Success Metrics

**Context Savings:**
- Target: 20-30% reduction in tool-related context
- Measure: Average tokens used for tool definitions per session

**Performance:**
- Target: < 100ms additional latency for tool search
- Measure: Time from request to tool availability

**User Experience:**
- Target: 95% tool discovery accuracy
- Measure: % of requests that successfully find needed tools

**Cost:**
- Target: 15-25% reduction in inference costs
- Measure: Token usage per session (before vs after)

---

## Conclusion

MCP Tool Search is a powerful pattern for managing tool explosion in AI agents. For Clawdbot:

**High Impact Areas:**
1. MCP ecosystem integration (future extensibility)
2. Skill-based tool discovery (current pain point)
3. Conversation-aware tool filtering (immediate benefit)

**Recommended Path:**
- Start with simple tool search (keyword-based)
- Add MCP support gradually
- Optimize based on actual usage data
- Iterate toward semantic search

**Key Insight:** Don't just implement the feature—understand the underlying problem (context explosion from tool descriptions) and solve that in whatever way makes sense for Clawdbot's architecture.

---

## References

- [Claude Code Announcement](https://twitter.com/trq212/status/2011523109871108570)
- [Claude Code Repository](https://github.com/anthropics/claude-code)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Registry](https://github.com/mcp)
- [Upstash Context7](https://github.com/upstash/context7)
