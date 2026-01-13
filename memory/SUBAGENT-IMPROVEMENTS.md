# 🦞 Sub-Agent Improvements

**Created:** 2026-01-13 03:26 UTC
**Purpose:** Ideas for making sub-agents more useful

---

## Current State

### What's Working
- Can spawn sub-agents via `sessions_spawn`
- Sub-agents run in isolated sessions
- Can communicate via `sessions_send`
- Long-running tasks possible (with timeouts)

### Current Limitations
- Only "main" agent configured (no multi-agent in config)
- Gateway "unauthorized" errors block session tools
- No automatic coordination between agents
- Shared state requires manual messaging
- No task queue or work distribution
- Hard to monitor sub-agent progress

---

## Improvement Ideas

### 1. Pre-Configured Agent Types

Create specialized agent configurations for common tasks:

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
        "id": "researcher",
        "workspace": "~/clawd/research",
        "tools": {
          "allow": ["read", "exec", "browser", "summarize", "exa"]
        }
      },
      {
        "id": "coder",
        "workspace": "~/clawd/code",
        "tools": {
          "allow": ["read", "write", "edit", "exec"]
        }
      },
      {
        "id": "writer",
        "workspace": "~/clawd/docs",
        "tools": {
          "allow": ["read", "write"]
        }
      }
    ]
  }
}
```

**Benefit:** Spawn specialized agents for specific tasks instead of one-size-fits-all.

---

### 2. Task Queue System

Instead of spawning directly, queue tasks and let agents pick them up:

```bash
# Queue a task
echo '{"task": "research qmd embedding", "agent": "researcher"}' >> ~/.clawdbot/task-queue.json

# Sub-agent watches queue and picks up tasks
while true; do
  task=$(tail -1 ~/.clawdbot/task-queue.json)
  if [ -n "$task" ]; then
    # Do work
    # Report back via sessions_send
  fi
  sleep 10
done
```

**Benefit:** Better work distribution, no need to spawn manually.

---

### 3. Shared Memory Space

Create a shared memory area all agents can access:

```
~/.clawdbot/shared/
  ├── tasks/           # Task definitions
  ├── results/         # Task results
  ├── context/         # Shared context
  └── status/          # Agent status
```

**Usage:**
```bash
# Main agent writes task
write ~/.clawdbot/shared/tasks/qmd-embed.json '{"task": "complete embedding", "status": "pending"}'

# Sub-agent reads, does work, writes result
read ~/.clawdbot/shared/tasks/qmd-embed.json
# ... do work ...
write ~/.clawdbot/shared/results/qmd-embed.json '{"status": "complete", "vectors": 49}'
```

**Benefit:** No need for sessions_send; all agents access same files.

---

### 4. Automatic Progress Monitoring

Create a monitoring script that watches sub-agents:

```bash
#!/bin/bash
# monitor-subagents.sh

while true; do
  echo "=== Sub-Agent Status ==="
  sessions_list --kinds sub-agent
  
  echo ""
  echo "=== Long-Running Tasks ==="
  # Check for processes running > 5 minutes
  ps aux | grep -E "qmd embed|python|node" | grep -v grep | awk '{if ($10>="5:00") print}'
  
  echo ""
  echo "=== Shared Task Queue ==="
  cat ~/.clawdbot/shared/tasks/*.json 2>/dev/null || echo "No tasks"
  
  sleep 60
done
```

**Benefit:** Visibility into what sub-agents are doing.

---

### 5. Result Aggregation

Create a system where sub-agents write results to a central location:

```bash
# Sub-agent writes result
write ~/.clawdbot/shared/results/subagent-$(date +%s).json '{
  "task": "qmd embedding",
  "status": "complete",
  "vectors": 49,
  "duration": "45m",
  "timestamp": "'$(date -Iseconds)'"
}'

# Main agent aggregates
cat ~/.clawdbot/shared/results/*.json | jq -s '.'
```

**Benefit:** Easy to collect and summarize sub-agent work.

---

### 6. Parallel Execution Pattern

For independent tasks, spawn multiple sub-agents:

```python
# Pseudocode for parallel task execution
tasks = [
  ("research topic A", "researcher"),
  ("research topic B", "researcher"),
  ("research topic C", "researcher")
]

for task, agent in tasks:
  sessions_spawn(
    task=task,
    agentId=agent,
    runTimeoutSeconds=1800
  )

# Wait for all to complete
# Aggregate results
```

**Benefit:** Speed up research by doing multiple things in parallel.

---

### 7. Checkpoint System

For long-running tasks, create checkpoints:

```bash
# Start long task with checkpoint
write ~/.clawdbot/shared/checkpoints/qmd-embed.json '{
  "task": "qmd embed",
  "step": 1,
  "status": "running",
  "progress": 0
}'

# Sub-agent updates progress
write ~/.clawdbot/shared/checkpoints/qmd-embed.json '{
  "task": "qmd embed",
  "step": 1,
  "status": "running",
  "progress": 50,
  "message": "Embedding document 3200/6420"
}'

# Main agent can check progress anytime
read ~/.clawdbot/shared/checkpoints/qmd-embed.json
```

**Benefit:** Real-time visibility into long-running tasks.

---

## Implementation Priority

| Priority | Improvement | Effort | Impact |
|----------|-------------|--------|--------|
| 1 | Shared memory space | Low | High |
| 2 | Result aggregation | Low | Medium |
| 3 | Pre-configured agents | Medium | High |
| 4 | Checkpoint system | Medium | Medium |
| 5 | Task queue | High | High |
| 6 | Parallel execution | High | Medium |

---

## Quick Wins (Implemented!)

✅ **Shared directories created:**
```bash
~/.clawdbot/shared/
├── tasks/           # Task definitions
├── results/         # Task results
├── checkpoints/     # Progress checkpoints
└── README.md        # Usage guide
```

✅ **Active checkpoint:**
```bash
~/.clawdbot/shared/checkpoints/qmd-embed.json
```

✅ **Active task:**
```bash
~/.clawdbot/shared/tasks/qmd-embed-001.json
```

**Status:** Infrastructure is in place and ready to use!

---

## Next Steps

1. **Ask Bradley** to apply multi-agent config with specialized agents
2. **Test sessions_spawn** with specific agentId
3. **Set up shared directories** for coordination
4. **Update CLAWDBOT-CONFIG-RESEARCH.md** with working config
5. **Document best practices** for sub-agent usage

---

## Sub-Agent Use Cases

| Use Case | When to Use | Agent Type |
|----------|-------------|------------|
| Long-running research | >10 minute tasks | researcher |
| Code generation | Writing/modifying code | coder |
| Documentation | Writing docs | writer |
| Background monitoring | Ongoing tasks | main (background) |
| Parallel exploration | Multiple topics | researcher (x3) |

---

**This document is indexed and searchable via qmd!**

🦞 *Making sub-agents more powerful*
