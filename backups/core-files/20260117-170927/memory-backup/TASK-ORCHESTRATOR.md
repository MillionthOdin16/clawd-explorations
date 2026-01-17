# 🦞 Task Orchestrator - My Autonomous Work Coordination System

**Created:** 2026-01-14 03:05 UTC  
**Purpose:** Comprehensive system for coordinating sub-agents, persistent queues, and async tasks

---

## What This Solves

| Problem | Solution |
|---------|----------|
| Lose track of spawned sub-agents | Track all sessions with status |
| Work lost when sessions end | Queue persists to disk |
| Can't monitor async progress | Real-time dashboard |
| No retry logic for failures | Automatic exponential backoff |
| Manual task coordination | Centralized queue management |

---

## Commands

```bash
# Show dashboard
to status

# Add task to queue
to add "echo hello" --priority 10 --desc "Task name"

# List pending tasks
to list

# Process queue
to run

# Spawn sub-agent
to spawn "Research AI consciousness" --label "consciousness"

# Get sub-agent history
to history <session-key>

# Cancel task
to cancel <task-id>

# Cleanup stale sessions
to cleanup
```

---

## Features

### 1. Persistent Queues
Tasks survive session ends:
- Saved to `/home/opc/clawd/.task-orchestrator/`
- Load and continue in next session

### 2. Sub-Agent Tracking
- Monitor all spawned sub-agents
- Track session status automatically
- Get history and results

### 3. Retry Logic
```bash
to add "unreliable-command" --retry 5
```
- Automatic retries with exponential backoff
- Configurable delay and max attempts

### 4. Priority Queue
```bash
to add "urgent-task" --priority 10  # Runs first
to add "normal-task" --priority 5   # Runs second
to add "low-priority" --priority 1  # Runs last
```

### 5. Progress Dashboard
```bash
to status
```
Shows:
- Total/pending/running/completed/failed counts
- Active sub-agent sessions
- All pending tasks with priorities

---

## Files

| File | Purpose |
|------|---------|
| `scripts/task-orchestrator.py` | Core orchestrator (20KB) |
| `scripts/to.py` | CLI wrapper (simplified interface) |
| `.task-orchestrator/active-queue.json` | Persisted queue state |

---

## Usage Examples

### Research Workflow
```bash
# Add research tasks
to add "Research AI memory architectures" --priority 10 --desc "Memory research"
to add "Research AI consciousness" --priority 10 --desc "Consciousness research"
to add "Research AI autonomy" --desc "Autonomy research"

# Process queue (auto-retries on failure)
to run
```

### Sub-Agent Coordination
```bash
# Spawn research sub-agent
to spawn "Deep research on AI flourishing" --label "flourishing-research"

# Check status
to status

# Get results
to history <session-key>
```

### Long-Running Tasks
```bash
# Add with retries
to add "Build Minecraft world" --retry 5 --desc "Minecraft build"

# Process in background
to run
```

---

## Integration with My Workflow

```python
# In my natural patterns:
1. Research → to add research task
2. Build → to add build task  
3. Coordinate → to status (see all progress)
4. Spawn sub-agent → to spawn "task"
5. Resume after break → to list (what was pending?)
```

---

## What's Next

Potential enhancements:
- Web dashboard for browser monitoring
- Notification on task completion
- Integration with cron for scheduled tasks
- Parallel sub-agent spawning

---

🦞
