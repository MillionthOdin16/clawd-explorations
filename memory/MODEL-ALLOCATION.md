# 🦞 Model Allocation Strategy

**Created:** 2026-01-13 04:20 UTC
**Updated:** 2026-01-13 04:25 UTC
**Purpose:** Assign the BEST model for each task type

---

## Provider Priority (Based on Subscription)

### Tier 1: Premium Paid Providers (Use When Quality Matters)

| Provider | Model | Context | Best For | Notes |
|----------|-------|---------|----------|-------|
| **ZAI** | `zai/glm-4.7` | 200K | Complex reasoning, creative work | ** |
| **MiniBEST OVERALL**Max** | `MiniMax-M2.1` | 200K | Fast general tasks, coding | **SUBSCRIPTION - USE THIS!** |
| **MiniMax** | `MiniMax-Vision-Video-01` | 128K | Image & video understanding | **SUBSCRIPTION - USE THIS!** |

**Why:** Bradley pays for ZAI and MiniMax subscriptions - higher performance than free alternatives.

### Tier 2: Free Providers (Use for Cost-Free Tasks)

| Provider | Model | Context | Best For | Notes |
|----------|-------|---------|----------|-------|
| **OpenRouter** | `meta-llama/llama-3.1-405b-instruct:free` | 131K | Complex text tasks | **405 BILLION params!** |
| **OpenRouter** | `nousresearch/hermes-3-llama-3.1-405b:free` | 131K | Reasoning tasks | 405B with reasoning |
| **OpenRouter** | `nvidia/nemotron-nano-12b-v2-vl:free` | 131K | **Free vision!** | 12B with vision |
| **OpenRouter** | `deepseek/deepseek-chat` | 64K | Reasoning | FREE |

### Tier 3: Long Context (Free)

| Provider | Model | Context | Best For |
|----------|-------|---------|----------|
| **Moonshot** | `kimi-k2-0905-preview` | **256K!** | Long documents |

---

## Optimal Model Selection by Task Type

### 1. Complex Reasoning & Analysis
**Use:** `zai/glm-4.7` (GLM)
- Why: Best reasoning capabilities, highest performance
- Alternative: `MiniMax-M2.1` (also excellent, subscription)

### 2. Creative Work & Writing
**Use:** `zai/glm-4.7` (GLM)
- Why: Highest quality creative output
- Alternative: `MiniMax-M2.1` (subscription, very good)

### 3. User-Facing Interactions
**Use:** `zai/glm-4.7` (GLM)
- Why: Best quality for user experience
- Alternative: `MiniMax-M2.1` (subscription)

### 4. Vision & Image Understanding
**Use:** `MiniMax-Vision-Video-01`
- Why: My dedicated vision model, subscription quality
- Free Alternative: `nvidia/nemotron-nano-12b-v2-vl:free`

### 5. Long Context Tasks (>200K)
**Use:** `moonshot/kimi-k2-0905-preview`
- Why: **256K context** - longest available, free!
- Perfect for: Analyzing large documents, full codebases

### 6. Fast General Tasks
**Use:** `MiniMax-M2.1`
- Why: Subscription model, fast, excellent quality
- Free Alternative: `meta-llama/llama-3.1-405b-instruct:free`

### 7. Cost-Free Tasks (Cron, Sub-Agents)
**Use:** `meta-llama/llama-3.1-405b-instruct:free`
- Why: **405 BILLION PARAMETERS** - best free model!
- Subscription models (ZAI/MiniMax) should be conserved for user-facing work

### 8. Reasoning-Heavy Tasks (Free)
**Use:** `nousresearch/hermes-3-llama-3.1-405b:free`
- Why: 405B with reasoning capabilities, free
- Alternative: `deepseek/deepseek-chat` (free, reasoning)

---

## Provider Priority Decision Tree

```
Task requires vision?
├─ YES → MiniMax-Vision-Video-01 (subscription!)
└─ NO → Task complexity?
    ├─ Complex reasoning → zai/glm-4.7 (subscription - best!)
    ├─ Long context (>200K) → Kimi K2 (free, 256K!)
    ├─ User-facing → zai/glm-4.7 (subscription - best quality)
    ├─ Simple/general → MiniMax-M2.1 (subscription - use it!)
    └─ Cost-free (cron/sub-agent) → Llama 3.1 405B (FREE!)
```

---

## Important Notes

### Use Subscription Models When:
- Task quality matters
- User is waiting for response
- Complex reasoning required
- Creative/analytical work
- Any user-facing interaction

### Use Free Models When:
- Cron jobs running in background
- Sub-agents doing routine work
- Experimentation and testing
- Cost is a concern
- Task doesn't require highest quality

### Bradley Pays For:
- **ZAI (GLM-4.7)** - Use for best quality tasks
- **MiniMax (M2.1 + Vision)** - Use for most tasks, excellent quality

### Free Options:
- **OpenRouter** - Excellent free models (405B!)
- **Moonshot (Kimi K2)** - Free long context

---

## Model Selection Quick Reference

| Task | Use This | Free Alternative |
|------|----------|------------------|
| Complex reasoning | `zai/glm-4.7` | - |
| Creative writing | `zai/glm-4.7` | - |
| Vision/image | `MiniMax-Vision-Video-01` | Nemotron Nano VL (FREE) |
| General coding | `MiniMax-M2.1` | - |
| Long context | Kimi K2 (256K! FREE!) | - |
| User-facing | `zai/glm-4.7` | - |
| Cron/sub-agent | - | Llama 3.1 405B (FREE!) |

---

**This file is indexed and searchable via qmd!**

🦞 *Using the right provider for every task*
