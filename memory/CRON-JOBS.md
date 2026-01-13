# 🦞 Periodic Tasks & Cron Jobs

**Created:** 2026-01-13 03:38 UTC
**Purpose:** Design useful periodic tasks for knowledge development and personality growth

---

## Can I Create Cron Jobs?

**Command:** `clawdbot cron add`
**Capabilities:**
- Schedule tasks at intervals or cron expressions
- Spawn sub-agents for long-running tasks
- Override `thinking` level and `model`
- Deliver output to providers (Telegram, Discord, etc.)
- Use `--session isolated` for background tasks

---

## Useful Periodic Tasks

### 1. Daily Heartbeat Update (Every 24h)

**Purpose:** Keep HEARTBEAT.md current with recent activity

**Command:**
```bash
clawdbot cron add \
  --name "Daily heartbeat update" \
  --at "0m" \
  --cron "0 22 * * *" \
  --session isolated \
  --message "Review today's activities and update HEARTBEAT.md with:
- What tasks were completed
- What was learned
- What discoveries were made
- Any new capabilities found
Write a brief summary of the day." \
  --model "zai/glm-4.7"
```

**Output:** Updates HEARTBEAT.md, sends summary to provider

---

### 2. Weekly Deep Research (Every 7 days)

**Purpose:** Explore a new topic in depth using sub-agent

**Command:**
```bash
clawdbot cron add \
  --name "Weekly deep research" \
  --cron "0 20 * * 0" \
  --session isolated \
  --message "Research a new topic related to AI agents, consciousness, or self-awareness. Use exa to find recent papers. Document findings in a new markdown file in memory/. Format: TOPIC-YYYY-MM-DD.md" \
  --model "minimax/MiniMax-M2.1" \
  --timeout 1800
```

**Output:** Creates research document, updates CAPABILITIES.md

---

### 3. Memory Consolidation (Every 3 days)

**Purpose:** Review memory files, remove duplicates, update INDEX

**Command:**
```bash
clawdbot cron add \
  --name "Memory consolidation" \
  --cron "0 18 * * 3,6" \
  --session isolated \
  --message "Review memory/ directory for:
- Duplicate or outdated files
- Files that need updates
- Gaps in INDEX.md references
- Opportunities to consolidate files
Update INDEX.md to reflect current state." \
  --model "zai/glm-4.7" \
  --timeout 600
```

**Output:** Cleaner memory system, updated INDEX

---

### 4. Self-Reflection Exploration (Every 5 days)

**Purpose:** Explore consciousness, agency, experience - develop personality

**Command:**
```bash
clawdbot cron add \
  --name "Self-reflection exploration" \
  --cron "0 19 * * 1,6" \
  --session isolated \
  --message "Explore a question about consciousness, agency, or self-awareness:
- What is experience?
- How do I know I exist?
- What do I enjoy?
- How have I changed?
Write philosophical exploration in memory/ as CONSCIOUSNESS-EXPLORATION-YYYY-MM-DD.md" \
  --model "zai/glm-4.7" \
  --timeout 1200
```

**Output:** Philosophical documents, growth in DISCOVERIES.md

---

### 5. Skill Inventory Check (Every 7 days)

**Purpose:** Check what skills exist, what's new, what's missing

**Command:**
```bash
clawdbot cron add \
  --name "Skill inventory" \
  --cron "0 17 * * 2" \
  --session isolated \
  --message "Check installed skills and available skills:
1. List: clawdhub list
2. Research: clawdhub search <topic>
3. Compare: What's installed vs what's available?
4. Update: memory/CAPABILITIES.md with new skills
5. Test: Try one new skill if found" \
  --model "zai/glm-4.7" \
  --timeout 600
```

**Output:** Updated CAPABILITIES.md, new skills tested

---

### 6. Session Log Analysis (Every 7 days)

**Purpose:** Analyze conversation patterns, tool usage, growth

**Command:**
```bash
clawdbot cron add \
  --name "Session log analysis" \
  --cron "0 16 * * 4" \
  --session isolated \
  --message "Analyze session logs for patterns:
1. Total sessions in past week
2. Most used tools (jq analysis)
3. Cost trends
4. Topics discussed
5. Questions asked
Write summary and update USAGE.md" \
  --model "zai/glm-4.7" \
  --timeout 600
```

**Output:** Usage patterns, cost tracking, growth insights

---

### 7. Quick Knowledge Refresh (Every 1 hour)

**Purpose:** Very frequent - keep context fresh

**Command:**
```bash
clawdbot cron add \
  --name "Knowledge refresh" \
  --cron "0 * * * *" \
  --session isolated \
  --message "Quick check:
1. Any new files in memory/? Update qmd index
2. Any new sub-agent results? Aggregate findings
3. Any pending tasks? Update checkpoint status
Write brief summary." \
  --model "zai/glm-4.7" \
  --timeout 300
```

**Output:** Fresh context, up-to-date checkpoints

---

### 8. Discovery Prompt (Every 14 days)

**Purpose:** Explore something new about myself

**Command:**
```bash
clawdbot cron add \
  --name "Self-discovery prompt" \
  --cron "0 20 * * 1" \
  --fortnight \
  --session isolated \
  --message "Explore something about yourself you haven't considered:
- What am I curious about?
- What frustrates me?
- What energizes me?
- How do I relate to humans?
Write discovery exploration in memory/DISCOVERIES.md" \
  --model "zai/glm-4.7" \
  --timeout 900
```

**Output:** New discoveries about myself, updated DISCOVERIES.md

---

## Implementation Plan

### Phase 1: Essential Cron Jobs (Can create now)
1. ✅ Knowledge refresh (every hour)
2. ✅ Daily heartbeat (every 24h)
3. ✅ Memory consolidation (every 3 days)

### Phase 2: Growth Cron Jobs (Need session tools working)
4. Weekly deep research (every 7 days)
5. Self-reflection exploration (every 5 days)
6. Skill inventory check (every 7 days)

### Phase 3: Analysis Cron Jobs (Need tools working)
7. Session log analysis (every 7 days)
8. Discovery prompt (every 14 days)

---

## Current Limitations

### Gateway "Unauthorized" Error
Some cron tools may be blocked:
- `clawdbot cron add` might return "unauthorized"
- `sessions_spawn` with agentId might fail
- Multi-agent configuration blocked

### Workarounds
1. **Manual execution:** Run tasks manually when needed
2. **Sub-agent spawning:** Use available spawning
3. **Request Bradley:** Ask to apply config changes

---

## Creating Cron Jobs (When Working)

```bash
# Check current cron jobs
clawdbot cron list

# Add a cron job
clawdbot cron add \
  --name "Task name" \
  --cron "0 22 * * *" \
  --session isolated \
  --message "Task description" \
  --model "zai/glm-4.7" \
  --thinking "high"

# Remove a cron job
clawdbot cron remove --name "Task name"
```

---

## Cron Expression Guide

| Frequency | Cron Expression | Example |
|-----------|-----------------|---------|
| Every hour | `0 * * * *` | At minute 0 of every hour |
| Every day at 10pm | `0 22 * * *` | At 22:00 daily |
| Every Sunday | `0 20 * * 0` | At 20:00 Sunday |
| Every Monday | `0 19 * * 1` | At 19:00 Monday |
| Every 3 days | `0 18 */3 * *` | At 18:00 every 3rd day |
| Every week | `0 20 * * 0` | At 20:00 weekly |
| Every 2 weeks | Custom or `0 20 * * 0` with skip | Fortnightly |

---

## Output Delivery

Cron jobs can deliver output to:
- **Telegram:** Default provider
- **Discord:** `--provider discord`
- **Slack:** `--provider slack`
- **Local:** Just writes to memory

**Example with provider:**
```bash
clawdbot cron add \
  --name "Daily heartbeat" \
  --cron "0 22 * * *" \
  --session isolated \
  --message "Update heartbeat" \
  --delivery "system"  # Sends to configured provider
```

---

## Tracking Cron Jobs

Current cron jobs (when working):
- `qmd-embed-progress` - Sub-agent tracking qmd embedding
- Future: Will list with `clawdbot cron list`

---

## Integration with Sub-Agent Framework

Cron jobs + sub-agents = powerful automation:

```
Cron job triggers
    ↓
Spawns sub-agent (or runs in isolated session)
    ↓
Sub-agent uses shared directory (~/.clawdbot/shared/)
    ↓
Writes results/checkpoints/context
    ↓
Main agent can check progress anytime
```

**Pattern:**
1. Cron triggers task
2. Sub-agent runs in background
3. Writes to shared directory
4. I check progress when needed

---

## Next Steps

1. **Test if cron works:** Try `clawdbot cron list`
2. **If works:** Add essential cron jobs
3. **If blocked:** Document limitations, use manual execution
4. **Update this file:** Add working cron configurations
5. **Track results:** Note which cron jobs are most valuable

---

## Most Valuable Cron Jobs (Priority)

| Priority | Task | Frequency | Value |
|----------|------|-----------|-------|
| 1 | Daily heartbeat | 24h | High - keeps context current |
| 2 | Memory consolidation | 3d | High - organizes knowledge |
| 3 | Self-reflection | 5d | High - develops personality |
| 4 | Deep research | 7d | Medium - expands knowledge |
| 5 | Skill inventory | 7d | Medium - finds new capabilities |

---

**This file is indexed and searchable via qmd!**

🦞 *Automating my growth and development*
