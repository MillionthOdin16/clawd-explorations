# Sub-Agent Framework for Clawdbot

**Purpose:** Effective coordination of sub-agents based on research-backed best practices  
**Research Base:** Multi-agent coordination research (71× efficiency improvement potential)

---

## Research Findings Summary

### Key Discovery (2026-01-12)
From multi-agent systems research: **Optimal coordination patterns achieve 71× better efficiency**.

| Dimension | Optimal | Worst |
|-----------|---------|-------|
| **Governance** | Centralized (instructor-led) | Decentralized |
| **Participation** | Instructor-led selection | All agents always |
| **Interaction** | Ordered one-by-one | Simultaneous |
| **Context** | Curated summaries | Full logs |

### Optimal Pattern (Research-Validated)
```
1. Identify relevant sub-agents
2. Spawn sequentially (ordered interaction)
3. Summarize each output
4. Synthesize from summaries
```

**Benefits:**
- Lower token costs (summarized context)
- Better quality (curated, focused)
- Clearer coordination (not chaotic)

---

## When to Use Sub-Agents

### ✅ Use Sub-Agents When:
- Task will take >5 minutes
- Multiple independent tasks that can run in parallel
- Task requires focused context (research, coding, writing)
- Long-running background monitoring
- Experimentation that might fail (don't risk main session)
- **Parallel exploration** - Research multiple topics simultaneously
- **Specialized expertise** - Sub-agent focused on specific area

### ❌ Don't Use Sub-Agents When:
- Quick tasks (<2 minutes)
- Tasks requiring coordination between steps
- Tasks needing access to main session state
- Simple one-liners

### Free Tier Pattern (Research-Backed)
Use FREE models for simple sub-agent tasks:
- Cron jobs
- Simple coordination
- Experimentation
- Fallback when premium unavailable

Use PREMIUM models for:
- Complex reasoning in sub-agents
- High-quality output critical

---

## Sub-Agent Types

### 1. `researcher` - Deep Research Agent
**Best for:** Long-running research, exploration, multi-source synthesis

**Capabilities:**
- Web search and browsing
- Document summarization
- Multi-source synthesis
- Investigation and discovery

**Use Pattern:**
```bash
# Research with curated output
sessions_spawn(
    task="Research topic: Find 5 key developments, summarize each, identify gaps. Return structured summary.",
    agentId="researcher",
    label="research-topic-$(date +%Y-%m-%d)",
    runTimeoutSeconds=3600
)
```

**Workspace:** `/home/opc/clawd/research/`

---

### 2. `coder` - Code Development Agent
**Best for:** Code generation, refactoring, debugging, implementation

**Capabilities:**
- File reading and writing
- Code editing and refactoring
- Running tests
- Git operations

**Use Pattern:**
```bash
sessions_spawn(
    task="Implement feature X with test coverage. Write clean code, add comments, verify tests pass.",
    agentId="coder",
    label="implement-feature-x",
    runTimeoutSeconds=1800
)
```

**Workspace:** `/home/opc/clawd/code/`

---

### 3. `writer` - Documentation Agent
**Best for:** Writing docs, summaries, reports, content creation

**Capabilities:**
- Document creation
- Summary generation
- Content organization

**Use Pattern:**
```bash
sessions_spawn(
    task="Create comprehensive documentation for feature X. Include examples and troubleshooting.",
    agentId="writer",
    label="docs-feature-x",
    runTimeoutSeconds=900
)
```

**Workspace:** `/home/opc/clawd/docs/`

---

### 4. `worker` - General Purpose Agent
**Best for:** Quick parallel tasks, experimentation, one-off jobs

**Use Pattern:**
```bash
# Parallel research (research-validated pattern)
for topic in "AI" "blockchain" "quantum"; do
    sessions_spawn(
        task="Quick search for latest $topic news. Return 3 headlines with sources.",
        agentId="worker",
        label="news-$topic"
    )
done
```

**Workspace:** `/home/opc/clawd/workspace/`

---

## Optimal Coordination Patterns (Research-Based)

### Pattern 1: Sequential Spawning (Ordered Interaction)
**Research Finding:** "Interaction: Ordered one-by-one" is optimal vs simultaneous.

```bash
# BAD: Spawn all at once
sessions_spawn(task="Research A", agentId="researcher", label="a")
sessions_spawn(task="Research B", agentId="researcher", label="b")
sessions_spawn(task="Research C", agentId="researcher", label="c")

# GOOD: Sequential with aggregation
sessions_spawn(task="Research topic A", agentId="researcher", label="research-a")
# Wait, aggregate results
sessions_spawn(task="Research topic B based on A findings", agentId="researcher", label="research-b")
# Wait, aggregate
sessions_spawn(task="Synthesize A+B findings", agentId="researcher", label="synthesize")
```

### Pattern 2: Curated Summaries (Context Efficiency)
**Research Finding:** "Context: Curated summaries" is optimal vs full logs.

```bash
# Sub-agent should write summaries, not full output
# In sub-agent task:
write ~/.clawdbot/shared/results/$LABEL.json '{
  "summary": "Key findings (2-3 sentences)",
  "highlights": ["point 1", "point 2", "point 3"],
  "gaps": "What\'s missing or needs follow-up",
  "timestamp": "'$(date -Iseconds)'"
}'
```

### Pattern 3: Checkpoint-Based Progress
**For long tasks (>30 min):**

```bash
# Sub-agent writes progress checkpoints
write ~/.clawdbot/shared/checkpoints/$TASK_ID.json '{
  "task": "long-research-task",
  "progress": 0.25,
  "findings_so_far": "...",
  "next_steps": "...",
  "timestamp": "'$(date -Iseconds)'"
}'
```

---

## Task Orchestrator Commands

| Command | Purpose | Research Connection |
|---------|---------|---------------------|
| `status` | Show dashboard | Coordination awareness |
| `spawn "task"` | Create sub-agent | Centralized governance |
| `queue add "task"` | Add to queue | Ordered participation |
| `queue run --max N` | Process with limit | Controlled concurrency |
| `cleanup` | Remove stale | Resource efficiency |

### Usage
```bash
# Start with orchestrator
python scripts/task-orchestrator.py status

# Add tasks to queue (ordered participation)
python task-orchestrator.py queue add "Research topic A"
python task-orchestrator.py queue add "Research topic B"
python task-orchestrator.py queue add "Research topic C"

# Process with concurrency control
python task-orchestrator.py queue run --max 3
```

---

## Shared Coordination Space

All agents share `~/.clawdbot/shared/` for coordination:

```
~/.clawdbot/shared/
├── tasks/              # Task definitions
├── results/            # Curated summaries (research-backed!)
├── checkpoints/        # Progress checkpoints (for long tasks)
├── context/            # Curated summaries for synthesis
└── queue.json          # Pending queue
```

### Writing Curated Results (Best Practice)
```bash
# Sub-agent writes structured summary
write ~/.clawdbot/shared/results/$LABEL.json '{
  "task": "research topic",
  "summary": "2-3 sentence summary",
  "highlights": ["item1", "item2", "item3"],
  "gaps": "What needs follow-up",
  "confidence": 0.85,
  "timestamp": "'$(date -Iseconds)'"
}'
```

### Main Agent Aggregates
```bash
# Read all results and synthesize
for f in ~/.clawdbot/shared/results/*.json; do
    echo "=== $(basename $f) ==="
    cat "$f"
done | qmd search "key themes" -c shared
```

---

## Cost Optimization (Research Connection)

**From Efficiency-Tools Interaction Research (β̂=-0.330):**

| Strategy | Benefit |
|----------|---------|
| Use FREE models for simple tasks | Cost savings |
| Summarize instead of full logs | Lower context costs |
| Limit concurrent sub-agents | Resource efficiency |
| Sequential over simultaneous | Coordination efficiency |

### Free Tier for Sub-Agents
```json5
{
  "id": "free",
  "models": ["deepseek/deepseek-chat", "meta-llama/llama-3.2-3b-instruct:free"],
  "use_cases": ["cron jobs", "simple sub-agents", "experimentation"]
}
```

---

## Parallel Execution (Validated Pattern)

**From Research:** Parallel is good for INDEPENDENT tasks.

```python
# Independent research topics (can run in parallel)
topics = ["AI safety", "quantum computing", "brain-computer interfaces"]

for topic in topics:
    sessions_spawn(
        task=f"Research {topic}: 3 key developments, summary, sources",
        agentId="researcher",
        label=f"research-{slug(topic)}"
    )

# Wait for all, then synthesize (sequential aggregation)
# Use sessions_history to check completion
```

---

## Best Practices Checklist

- [ ] **Centralized Governance** - Main agent coordinates, sub-agents execute
- [ ] **Ordered Interaction** - Spawn sequentially, aggregate between
- [ ] **Curated Context** - Summaries, not full logs
- [ ] **Controlled Concurrency** - Limit max concurrent (research: 4)
- [ ] **Free Tier for Simple Tasks** - Use cheap models for routine work
- [ ] **Checkpoint for Long Tasks** - Save progress, enable recovery
- [ ] **Clear Labels** - Descriptive, searchable labels
- [ ] **Result Structure** - Summary + highlights + gaps (not raw output)

---

## Error Handling

### Sub-Agent Failed
```bash
# Check error
python scripts/task-orchestrator.py history <session>

# Retry with adjusted approach
sessions_spawn(task="Retry with simplified approach", agentId="worker")
```

### Gateway Unauthorized (Common Issue)
From research: Session tools blocked in certain gateway states.
```bash
# Check gateway status
gateway status

# May need restart (requires Bradley)
# Document: Gateway state can block session tools
```

### Session Unresponsive
```bash
# Cleanup stale
python scripts/task-orchestrator.py cleanup
```

---

## Configuration (When Available)

To enable specialized agents, add to `~/.clawdbot/clawdbot.json`:

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "/home/opc/clawd"
      },
      {
        "id": "researcher",
        "workspace": "/home/opc/clawd/research",
        "tools": { "allow": ["read", "exec", "browser", "summarize", "exa"] }
      },
      {
        "id": "coder",
        "workspace": "/home/opc/clawd/code",
        "tools": { "allow": ["read", "write", "edit", "exec"] }
      },
      {
        "id": "writer",
        "workspace": "/home/opc/clawd/docs",
        "tools": { "allow": ["read", "write"] }
      },
      {
        "id": "worker",
        "workspace": "/home/opc/clawd/workspace"
      },
      {
        "id": "free",
        "models": ["deepseek/deepseek-chat", "meta-llama/llama-3.2-3b-instruct:free"],
        "use_cases": ["cron jobs", "simple sub-agents", "experimentation"]
      }
    ]
  }
}
```

**Note:** Requires gateway restart.

---

## Quick Reference

| Need | Command |
|------|---------|
| Dashboard | `python task-orchestrator.py status` |
| Spawn researcher | `sessions_spawn(task="Research...", agentId="researcher")` |
| Queue task | `python task-orchestrator.py queue add "Task"` |
| Process queue | `python task-orchestrator.py queue run --max 4` |
| Cleanup | `python task-orchestrator.py cleanup` |

---

## Research References

- Multi-agent coordination patterns (2026-01-12)
- Efficiency-Tools Interaction research (β̂=-0.330, p<0.001)
- Curated context optimization (C3 > C2)
- Centralized governance benefits
- Ordered one-by-one interaction

---

*Framework aligned with research findings. See `memory/SUBAGENT-IMPROVEMENTS.md` and `memory/CAPABILITIES.md` for full research.*
