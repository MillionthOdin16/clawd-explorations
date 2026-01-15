# Clawdbot Workflow Adaptation Guide

**Migration Target:** GitHub source (2026.1.14 development/unreleased)
**Purpose:** How I should adapt my workflows and instructions to leverage new features
**Generated:** 2026-01-14

---

## 1. NEW COMMANDS & TOOLS

### 1.1 Memory Commands (NEW)

**Before:** No direct memory CLI
**After:** New `clawdbot memory` commands

```bash
# Search memories
clawdbot memory search "query" [--agent agentId]

# Get specific memory
clawdbot memory get <memoryId>

# List memories
clawdbot memory list [--agent agentId]
```

**My Workflow Change:**
- When users ask about past conversations or research, use `memory_search` instead of just reading files
- Can search semantically (not just keyword matching)
- Better for finding related context across sessions

**Example Usage:**
```
User: "What did we decide about the research framework?"
Me: → clawdbot memory search "research framework decisions"
```

---

### 1.2 Plugin Commands (NEW)

**Before:** No plugin management
**After:** Plugin CLI available

```bash
# List installed plugins
clawdbot plugins list

# Install plugin
clawdbot plugins install <path|tgz|npm-package>

# Plugin info
clawdbot plugins info <pluginName>

# Enable/disable
clawdbot plugins enable <pluginName>
clawdbot plugins disable <pluginName>

# Doctor check
clawdbot plugins doctor
```

**My Workflow Change:**
- Check available plugins with `clawdbot plugins list`
- Voice call features now available via plugin (Twilio/Telnyx)
- Can install custom extensions for specific use cases

---

### 1.3 Updated Status Command

**Before:** Basic status
**After:** Table-based with more detail

```bash
clawdbot status              # Table-based overview
clawdbot status --all        # Full debug report (tables, logs, Tailscale)
```

**My Workflow Change:**
- Use `status --all` when debugging connectivity issues
- Report includes Tailscale summary if applicable

---

### 1.4 Dashboard Command (NEW)

```bash
clawdbot dashboard  # Auto-opens Control UI
```

**My Workflow Change:**
- Can launch dashboard for users who prefer GUI
- Useful for non-technical users

---

### 1.5 Update Command (NEW)

```bash
clawdbot update              # Safe-ish git checkout update
clawdbot update --check      # Check for updates
```

**My Workflow Change:**
- Can offer users `clawdbot update` when they ask about new features
- Better than manual git pull for end users

---

## 2. CONFIGURATION CHANGES

### 2.1 Breaking Change: `providers` → `channels`

**Before:**
```yaml
providers:
  telegram:
    token: xxx
  whatsapp:
    sessionId: xxx
```

**After:**
```yaml
channels:
  telegram:
    token: xxx
  whatsapp:
    sessionId: xxx
```

**My Workflow Change:**
- Auto-migration handles this, so existing configs work
- When creating new config examples, use `channels.*`
- Update any documentation I create to use `channels`

---

### 2.2 New Memory Configuration

```yaml
agents:
  defaults:
    memory:
      vectorSearch: true          # Enable semantic search
      embeddingEndpoint: custom   # Custom OpenAI-compatible endpoint
      chunkSize: 1000
      watchEnabled: true

memory:
  storagePath: ~/.clawdbot/memory/
```

**My Workflow Change:**
- Vector search is now available - use it for semantic queries
- Can configure custom embedding endpoints for privacy/performance
- Memory is indexed per-agent in SQLite (`~/.clawdbot/memory/{agentId}.sqlite`)

---

### 2.3 New Agent Compaction Configuration

```yaml
agents:
  defaults:
    compaction:
      enabled: true
      headroom: 5000             # Reserve tokens for memory writes
      summarization:
        enabled: true
        threshold: 0.8
```

**My Workflow Change:**
- Compaction is now configurable per-agent
- Pre-compaction memory flush happens automatically
- When sessions get long, memories are preserved before compaction

---

### 2.4 New Cron Configuration

```yaml
cron:
  jobs:
    - id: daily-report
      schedule: "0 9 * * *"      # Cron format
      command: agents.generate_report
      model: claude-sonnet-4-20250514
      deleteAfterRun: true       # One-shot option
```

**My Workflow Change:**
- Cron jobs can target specific agents
- Can use ISO timestamps for one-shot jobs
- Model overrides per job

---

## 3. NEW MODEL OPTIONS

### 3.1 Moonshot Kimi K2

**NEW Provider:** Moonshot AI (Kimi K2 0905)

```yaml
models:
  providers:
    moonshot:
      apiKey: ${MOONSHOT_API_KEY}
      defaultModel: kiminew/k2-0905
```

**My Workflow Change:**
- Can use Kimi K2 for coding tasks
- Fast, cost-effective alternative to Claude
- Available in `/model` picker

---

### 3.2 Synthetic Provider

**NEW Provider:** Synthetic

```yaml
models:
  providers:
    synthetic:
      apiKey: ${SYNTHETIC_API_KEY}
```

**My Workflow Change:**
- Additional model option for variety
- May have different strengths than Claude/Anthropic

---

### 3.3 MiniMax Vision Routing

**Change:** MiniMax vision now routes to Coding Plan VLM endpoint

**My Workflow Change:**
- Image understanding with MiniMax works better
- Can use `@/path/to/file.png` syntax for images

---

## 4. TOOL CHANGES

### 4.1 Browser Tools Enhanced

**New Actions:**
- `scrollintoview` - Scroll element into view
- `target` option (sandbox/host/custom)

**My Workflow Change:**
- Can scroll pages to find elements more reliably
- Better control over browser sandboxing

---

### 4.2 Docker Bind Mounts

**New Configuration:**
```yaml
tools:
  sandbox:
    docker:
      binds:
        - /host/path:/container/path
```

**My Workflow Change:**
- Can mount specific directories for container access
- Useful for accessing project files in containers

---

### 4.3 Tool Profiles

**New Feature:** Group tools into profiles

**My Workflow Change:**
- Can enable/disable groups of tools
- Simpler configuration for different use cases

---

## 5. PROVIDER-SPECIFIC CHANGES

### 5.1 Telegram

| Change | Impact |
|--------|--------|
| `timeoutSeconds` now honored | Better control over API timeouts |
| Long captions split | Media + follow-up text instead of truncation |
| Forum topic IDs preserved | Better threading in topics |

**My Workflow Change:**
- Can set per-account timeouts in config
- Long messages with images work better
- Topics maintain context better

---

### 5.2 Discord

| Change | Impact |
|--------|--------|
| `allowBots` config option | Control bot interaction |
| Channel/category management | Message tool can create/edit channels |

**My Workflow Change:**
- Can manage Discord server structure via message tool
- Better control over bot behavior

---

### 5.3 Slack

| Change | Impact |
|--------|--------|
| Mismatched Socket Mode events dropped | Cleaner event handling |
| Slash commands with/without `/` | More flexible commands |

**My Workflow Change:**
- Slash commands work more reliably
- Cleaner event processing

---

## 6. VECTOR MEMORY WORKFLOW

### 6.1 How It Works

**Before:** File-based memory, keyword search
**After:** SQLite vector index, semantic search

**Components:**
1. Markdown files watched for changes
2. Chunks stored in SQLite with embeddings
3. Semantic similarity search available

### 6.2 My Workflow Adaptation

**When user asks about past decisions:**
1. Try `memory_search` first for semantic matches
2. Fall back to file reading if needed
3. Use snippets + line ranges for context

**Example:**
```
User: "What did we agree on for the research framework?"
Me: → memory_search "research framework agreement"
    → Returns semantically similar memories with snippets
    → Provides context with line numbers for full details
```

### 6.3 Configuration for Memory

```yaml
agents:
  defaults:
    memory:
      vectorSearch: true          # Enable semantic search
      embeddingProvider: openai   # or custom endpoint
```

---

## 7. PLUGIN SYSTEM WORKFLOW

### 7.1 Available Plugins

- **Voice Call Plugin** - Twilio/Telnyx integration
- Custom extensions via `plugins.load.paths`

### 7.2 My Workflow with Plugins

**Check available plugins:**
```bash
clawdbot plugins list
```

**If voice calls needed:**
```bash
clawdbot plugins install voice-call
clawdbot voice-call start --provider twilio
```

---

## 8. REFERENCE: QUICK COMMANDS

### New Commands Summary

| Command | Purpose |
|---------|---------|
| `clawdbot memory search <query>` | Semantic memory search |
| `clawdbot memory get <id>` | Get specific memory |
| `clawdbot plugins list` | List plugins |
| `clawdbot plugins install <pkg>` | Install plugin |
| `clawdbot status --all` | Full status with debug |
| `clawdbot dashboard` | Open Control UI |
| `clawdbot update` | Update from git |

### Updated Commands

| Command | Change |
|---------|--------|
| `clawdbot status` | Table-based output |
| `clawdbot cron add --model <m>` | Model override support |

---

## 9. ROLLBACK PROCEDURE

If issues arise, I should:

```bash
# Stop GitHub version
pkill -f "clawdbot.*dist/entry.js"

# Start NPM version
node /home/opc/.nvm/.../node_modules/clawdbot/dist/entry.js gateway --port 18789
```

---

## 10. CHECKLIST: ADOPTING NEW FEATURES

- [ ] Use `memory_search` for semantic queries about past decisions
- [ ] Update any config examples to use `channels` instead of `providers`
- [ ] Explore `clawdbot plugins list` for available extensions
- [ ] Try `clawdbot status --all` for debugging
- [ ] Consider enabling vector memory search in config
- [ ] Test new model options (Moonshot Kimi K2, Synthetic)
- [ ] Use `scrollintoview` for browser automation
- [ ] Consider Docker bind mounts for container workflows

---

*This guide is for me (Clawd) to adapt my workflows. Users don't need to know these details - I should just use the new capabilities transparently.*
