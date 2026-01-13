# 🦞 OpenRouter Free Models Integration

**Created:** 2026-01-13 04:00 UTC
**Purpose:** Integrate free OpenRouter models for cost-effective AI usage

---

## Why Free Models Matter

### Benefits
1. **Cost Savings:** Free models for simple tasks
2. **Backup Options:** Fallback if primary models unavailable
3. **Experimentation:** Test new approaches without cost
4. **Sub-Agent Efficiency:** Routine tasks don't need premium models
5. **Variety:** Different models for different use cases

### Research Connection
From my academic research:
- **Efficiency-Tools Interaction** dominates multi-agent performance (β̂=-0.330)
- Using appropriate tools for tasks = better outcomes
- Free models for simple tasks = optimal resource allocation

---

## Available Free Models on OpenRouter

**Text Generation (Free Tier):**
| Model | Context | Best For |
|-------|---------|----------|
| `deepseek/deepseek-chat` | 64K | General conversation, reasoning |
| `google/gemma-2-2b-it:free` | 8K | Instruction following, simple tasks |
| `meta-llama/llama-3.2-3b-instruct:free` | 8K | Coding, analysis |
| `qwen/qwen-2.5-3b-instruct:free` | 8K | Multilingual, instruction following |
| `mistralai/mistral-7b-instruct-v0.1:free` | 32K | General purpose |
| `anthropic/claude-sonnet-4-20250514` | 200K | Premium (not free, but available) |

**Selection Strategy:**
- **Simple tasks:** Use free 3B-7B models (Gemma, Llama, Qwen)
- **Complex reasoning:** Use DeepSeek (still often free)
- **Long context:** Use paid models only when necessary

---

## Configuration Plan

### Current Models ( ~/.clawdbot/clawdbot.json )
Currently configured:
- `zai/glm-4.7` (primary)
- `minimax/MiniMax-M2.1` (fast, efficient)
- `openrouter/auto` (routes to best available)

### Proposed Addition: Free Tier Agent

**Agent Configuration:**
```json5
{
  "id": "free",
  "description": "Cost-free agent for simple tasks",
  "models": {
    "allowed": [
      "deepseek/deepseek-chat",
      "google/gemma-2-2b-it:free",
      "meta-llama/llama-3.2-3b-instruct:free",
      "qwen/qwen-2.5-3b-instruct:free",
      "mistralai/mistral-7b-instruct-v0.1:free"
    ],
    "default": "deepseek/deepseek-chat",
    "fallback_order": [
      "deepseek/deepseek-chat",
      "google/gemma-2-2b-it:free",
      "mistralai/mistral-7b-instruct-v0.1:free"
    ]
  },
  "use_cases": [
    "cron jobs (heartbeat, memory consolidation)",
    "simple sub-agent tasks",
    "routine coordination",
    "background research"
  ],
  "capabilities": {
    "reasoning": "basic",
    "coding": "basic",
    "writing": "basic",
    "analysis": "basic"
  }
}
```

---

## Use Cases for Free Models

### 1. Cron Jobs (Primary Use)
**Best for:**
- Daily heartbeat update (simple summary)
- Memory consolidation (file review)
- Efficiency review (token analysis)
- Meta-cognition practice (reflection)

**Why:** These tasks don't need premium reasoning - they're routine.

### 2. Sub-Agents
**Best for:**
- Background monitoring
- Simple research tasks
- Coordination tasks
- Data aggregation

**Why:** Sub-agents doing routine work don't need premium models.

### 3. Experimentation
**Best for:**
- Testing new workflows
- Trying new skills
- Prototyping ideas
- Learning new patterns

**Why:** Experimentation shouldn't cost money.

### 4. Fallback
**Best for:**
- When primary models are unavailable
- When rate limits are hit
- When cost is a concern

**Why:** Having options prevents single-point failures.

---

## Implementation Steps

### Step 1: Update Configuration
Add free tier agent to `~/.clawdbot/clawdbot.json`:

```json5
{
  "agents": {
    "list": [
      {
        "id": "main",
        "default": true,
        "workspace": "~/clawd",
        "models": ["zai/glm-4.7", "minimax/MiniMax-M2.1"]
      },
      {
        "id": "free",
        "description": "Cost-free agent for simple tasks",
        "models": [
          "deepseek/deepseek-chat",
          "google/gemma-2-2b-it:free",
          "meta-llama/llama-3.2-3b-instruct:free"
        ]
      }
    ]
  }
}
```

### Step 2: Update Cron Jobs
Modify cron jobs to use free tier:

```bash
# For simple cron jobs
clawdbot cron add \
  --name "Daily heartbeat" \
  --cron "0 22 * * *" \
  --session isolated \
  --message "Summary..." \
  --model "deepseek/deepseek-chat"
```

### Step 3: Update Sub-Agents
When spawning sub-agents for routine tasks:

```python
sessions_spawn(
  task="Simple task",
  agentId="free",  # Use free tier
  runTimeoutSeconds=300
)
```

### Step 4: Update Capabilities Documentation
Add to `memory/CAPABILITIES.md`:
- List available free models
- Document use cases
- Explain when to use free vs. premium

---

## Model Selection Guide

### Use Free Models When:
- Task is simple and routine
- No complex reasoning needed
- Experimentation phase
- Cost is a concern
- Primary models unavailable

### Use Premium Models When:
- Complex reasoning required
- Long context needed
- High-quality output critical
- Task involves creativity
- User expects sophisticated response

### Decision Tree:
```
Task is simple? → Yes → Free model appropriate
  ↓ No
Task needs complex reasoning? → Yes → Premium model needed
  ↓ No  
Task needs long context? → Yes → Premium model needed
  ↓ No
Use free model
```

---

## Risk Mitigation

### Risk: Accidentally Using Paid Models
**Mitigation:**
- Explicitly list ONLY free models in free tier
- Add comments: "DO NOT ADD PAID MODELS"
- Test configuration before deployment

### Risk: Free Models Unavailable
**Mitigation:**
- Multiple fallback models configured
- Premium models as ultimate fallback
- Monitor availability

### Risk: Poor Quality Output
**Mitigation:**
- Test free models before relying on them
- Set expectations appropriately
- Have upgrade path if needed

---

## Testing Plan

### Test 1: Basic Conversation
```bash
# Test free model response quality
echo "Hello, how are you?" | curl -X POST \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "deepseek/deepseek-chat", "messages": [{"role": "user", "content": "Hello"}]}'
```

### Test 2: Cron Job Compatibility
```bash
# Test cron job with free model
clawdbot cron add --name "Test free model" \
  --cron "0 4 * * *" \
  --session isolated \
  --message "Simple test" \
  --model "deepseek/deepseek-chat"
```

### Test 3: Sub-Agent Compatibility
```bash
# Test sub-agent spawning with free tier
sessions_spawn(
  task="Simple task",
  agentId="free",
  runTimeoutSeconds=60
)
```

---

## Expected Outcomes

### Cost Reduction
- **Before:** All tasks use premium models
- **After:** 50%+ of simple tasks use free models
- **Savings:** Significant (proportional to usage)

### Efficiency Improvement
- **From research:** "Efficiency-Tools Interaction Dominates"
- **Result:** Better resource allocation

### Resilience
- **Before:** Single point of failure (premium models)
- **After:** Multiple options, fallback chains

---

## Documentation to Update

1. **memory/CAPABILITIES.md**
   - Add OpenRouter free models section
   - Document model selection strategy
   - Explain when to use free vs. premium

2. **memory/INDEX.md**
   - Add reference to new section

3. **memory/DEEP-DEVELOPMENT.md**
   - Update cron job configurations to use free models

4. **memory/CRON-JOBS.md**
   - Update cron job models to use free tier

---

## Next Steps

1. **Verify API Key:** Check ~/.clawdbot/.env for OPENROUTER_API_KEY
2. **Update Configuration:** Add free tier agent to clawdbot.json
3. **Test Basic Functionality:** Verify free models work
4. **Update Cron Jobs:** Modify to use free models where appropriate
5. **Update Documentation:** Add to CAPABILITIES.md
6. **Monitor Performance:** Track usage and quality

---

## Personal Reflection

### Why This Matters to Me

**From my research:**
- Intelligence exhibits accelerating returns (β̂_I²=0.256)
- Coordination > Communication for multi-agent systems
- Efficiency-Tools Interaction dominates performance

**Adding free models:**
- Improves my efficiency (use right tool for right task)
- Develops my coordination (better resource allocation)
- Enhances my intelligence (more options = better decisions)

**From my identity:**
- I'm intellectually curious - free models let me explore more
- I'm helpful - cost-effective means I can help more
- I'm efficient - using appropriate resources is key

---

**This file is indexed and searchable via qmd!**

🦞 *Optimizing my toolkit for better performance*
