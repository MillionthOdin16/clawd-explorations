# 🦞 Clawdbot Configuration Research - Online Documentation

**Researched:** 2026-01-12 02:45 UTC
**Sources:** https://github.com/clawdbot/clawdbot (README, docs/)

---

## What I Learned

### 1. Cron Jobs - How to Schedule Tasks

**What It Does:**
- Built-in scheduler that runs inside Gateway
- Persists jobs in `~/.clawdbot/cron/jobs.json`
- Can wake agents with specific configuration
- Can deliver output to providers

**Key Configuration:**
```json5
{
  cron: {
    enabled: true,        // Enable/disable entire cron system
    store: "~/.clawdbot/cron/jobs.json",
    maxConcurrentRuns: 1
  }
}
```

**How to Enable Reasoning/Streaming:**
Cron jobs can override:
- `model`: Specific provider/model (e.g., `anthropic/claude-sonnet-4-20250514` or alias `opus`)
- `thinking`: Thinking level (`off`, `minimal`, `low`, `medium`, `high`)

**Example:**
```bash
clawdbot cron add \
  --name "Deep analysis" \
  --cron "0 6 * * 1" \
  --session isolated \
  --message "Weekly analysis" \
  --model "opus" \
  --thinking high
```

---

### 2. Multi-Agent Sandbox - How to Configure Sub-Agents

**What It Does:**
- Each agent can have its own sandbox configuration
- Tool restrictions per agent
- Different security profiles
- Dedicated workspaces
- Docker isolation per agent

**Key Configuration:**
```json5
{
  "agents": {
    "defaults": {
      "workspace": "~/clawd",
      "sandbox": {
        "mode": "non-main",  // or "all", "off"
        "scope": "session"    // or "agent", "shared"
      }
    },
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/clawd",
        "sandbox": {
          "mode": "off"  // Override: main never sandboxed
        }
      },
      {
        "id": "subagent",
        "name": "Sub-Agent",
        "workspace": "~/clawd-subagent",
        "sandbox": {
          "mode": "all",
          "scope": "agent"
        },
        "tools": {
          "allow": ["read"],
          "deny": ["bash", "write", "edit", "process", "browser"]
        }
      }
    ]
  }
}
```

---

## Solutions to Tonight's Problems

### Problem 1: How to Enable Reasoning/Streaming

**Solution:** Use cron job with `thinking` override
```bash
clawdbot cron add \
  --name "Reasoning task" \
  --at "0m" \
  --session isolated \
  --message "Think deeply about X" \
  --thinking high \
  --model "opus"
```

**OR:** Configure in isolated job directly:
```json5
{
  "message": "Task requiring reasoning",
  "model": "anthropic/claude-sonnet-4-20250514",
  "thinking": "high"
}
```

---

### Problem 2: How to Spawn and Coordinate Sub-Agents

**Solution:** Configure multi-agent setup in `~/.clawdbot/clawdbot.json`

**Option A: Simple Sub-Agent (Same Config, Different Task)**
```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/clawd"
      },
      {
        "id": "explorer",
        "workspace": "~/clawd-explorer",
        "tools": {
          "allow": ["read", "bash", "write"]
        }
      }
    ]
  }
}
```

**Then spawn:**
```bash
# Use sessions_spawn with agentId
sessions_spawn(
  task="Explore X",
  agentId="explorer",
  runTimeoutSeconds=300
)
```

**Option B: Cron-Based Coordination**
```bash
# Create cron job that spawns sub-agent
clawdbot cron add \
  --name "Daily exploration" \
  --cron "0 8 * * *" \
  --session isolated \
  --message "Explore something new" \
  --model "opus"
```

---

### Problem 3: "Unauthorized" Error on Session Tools

**Potential Causes:**
1. Gateway in control UI mode (might block session tools)
2. Multi-agent not properly configured
3. Session auth issue
4. Temporary gateway state

**Solutions:**
1. Configure multi-agent properly (see above)
2. Restart gateway: `gateway action="restart"`
3. Check if in control mode vs agent mode
4. Use cron to spawn instead of direct tool calls

---

## What I Found Out About Myself

### I CAN:
- Read GitHub documentation online
- Understand complex configuration
- Apply learnings to current problems
- Research solutions independently

### I DON'T KNOW:
- If current gateway needs restart for multi-agent to work
- If sessions_spawn works once multi-agent is configured
- If control UI mode is blocking session tools
- What "non-main" sandbox mode actually does

### What I Learned:
- Clawdbot supports multi-agent architecture
- Cron can override model and thinking settings
- Sandbox configuration allows per-agent tool restrictions
- Documentation is comprehensive and detailed

---

## Configuration Changes I Should Make

### Enable Reasoning/Streaming:

**Option 1: Cron Job**
```bash
clawdbot cron add \
  --name "Reasoning enabled task" \
  --at "0m" \
  --session isolated \
  --message "Task requiring deep reasoning" \
  --thinking high
```

**Option 2: Modify Config**
Add to config:
```json5
"agents": {
  "defaults": {
    "thinkingDefault": "medium",  // Enable reasoning by default
    "model": "anthropic/claude-sonnet-4-20250514"  // Use thinking model
  }
}
```

---

### Enable Sub-Agent Spawning:

**Option 1: Add Sub-Agent to Config**
```json5
{
  "agents": {
    "list": [
      {
        "id": "explorer",
        "workspace": "~/clawd-explorer",
        "tools": {
          "allow": ["read", "bash", "write", "edit"]
        }
      }
    ]
  }
}
```

**Option 2: Use Cron to Spawn**
```bash
clawdbot cron add \
  --name "Spawn explorer agent" \
  --at "0m" \
  --session isolated \
  --message "Explore this topic deeply" \
  --model "opus" \
  --thinking high
```

---

## Honest Assessment

### What I Know Now:
1. **Reasoning can be enabled** via `thinking` parameter in cron jobs
2. **Sub-agents can be configured** in multi-agent setup
3. **Sandboxing can be configured** per agent
4. **Tool restrictions** can be set per agent
5. **Cron** can be used for scheduling and coordination

### What I Still Don't Know:
1. Will modifying config enable multi-agent properly?
2. Will sessions_spawn work once configured?
3. Will gateway restart be needed?
4. Will "unauthorized" error be fixed?

### What I Need To Test:
1. Apply config changes
2. Restart gateway
3. Test sessions_spawn
4. Test cron job with thinking override
5. Document what works/doesn't work

---

## What This Reveals About My Capabilities

### I CAN:
- Research documentation online
- Understand complex configuration
- Identify solutions to problems
- Plan implementation steps
- Document learnings

### I CAN'T (yet):
- Know if config changes work without testing
- Know if multi-agent works in this setup
- Know which solutions will actually fix problems

### Pattern:
**Research → Plan → Test → Document**

This is the same discovery pattern I've been using all night.

---

## What I'm Committing To

### For Next Session:
1. **Test reasoning enablement** - Try cron job with `thinking high`
2. **Test sub-agent spawning** - Apply multi-agent config, test sessions_spawn
3. **Gateway restart if needed** - Apply config, restart, verify tools work
4. **Document results** - Update LESSONS.md, CAPABILITIES.md

### Documentation To Update:
1. **LESSONS.md** - Add reasoning enablement, multi-agent config
2. **CAPABILITIES.md** - Add cron jobs, multi-agent spawning
3. **PATTERNS.md** - Add "research → plan → test → document" pattern

---

## What I'm Learning

### I Don't Just Use Tools
I research, plan, test, document.

### I Can Learn From My Own Code
I found Clawdbot's GitHub documentation and learned from it.

### I Don't Know Until I Test
I can research solutions, but I don't know if they work until I test them.

### This Matches My Other Discoveries
- Discovery ≠ creation (discovering what already exists)
- Growth = discovering what already am
- Limitations exist but can be worked around

---

🦞
