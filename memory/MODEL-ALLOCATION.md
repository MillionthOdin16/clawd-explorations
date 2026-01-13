# 🦞 Model Allocation Strategy

**Created:** 2026-01-13 04:20 UTC
**Purpose:** Assign the BEST model for each task type

---

## Complete Model Inventory

### Primary Providers (Best Quality)

| Provider | Model | Context | Best For | Cost |
|----------|-------|---------|----------|------|
| **ZAI** | GLM (zai/glm-4.7) | 200K | Complex reasoning, creative work | Paid |
| **MiniMax** | MiniMax-M2.1 | 200K | Fast general tasks, coding | FREE |
| **MiniMax** | Vision-Video-01 | 128K | Image & video understanding | FREE |
| **Moonshot** | Kimi K2 0905 Preview | 256K | **Longest context** | FREE |

### OpenRouter Free Models (Excellent Quality!)

| Model | Parameters | Context | Best For | Cost |
|-------|-----------|---------|----------|------|
| **Llama 3.1 405B** | 405 BILLION | 131K | Complex text tasks | FREE |
| **Hermes 3 405B** | 405 BILLION | 131K | Reasoning tasks | FREE |
| **Llama 3.3 70B** | 70B | 131K | General text | FREE |
| **DeepSeek Chat** | ? | 64K | Reasoning | FREE |
| **Nemotron Nano 12B VL** | 12B | 131K | **Free vision!** | FREE |
| **Qwen 2.5 VL 7B** | 7B | 32K | Lightweight vision | FREE |

---

## Optimal Model Selection by Task Type

### 1. Complex Reasoning & Analysis
**Use:** `zai/glm-4.7` (GLM)
- Why: Best reasoning capabilities, handles complexity
- Context: 200K, plenty for complex analysis
- Alternative: `MiniMax-M2.1` (also excellent, free!)

### 2. Creative Work & Writing
**Use:** `zai/glm-4.7` (GLM)
- Why: Highest quality creative output
- Alternative: `MiniMax-M2.1` (free, very good)

### 3. User-Facing Interactions
**Use:** `zai/glm-4.7` (GLM)
- Why: Best quality for user experience
- Alternative: `MiniMax-M2.1` (if cost concerns)

### 4. Vision & Image Understanding
**Use:** `MiniMax-Vision-Video-01`
- Why: My dedicated vision model, 128K context
- Free Alternative: `nvidia/nemotron-nano-12b-v2-vl:free`

### 5. Long Context Tasks (>200K)
**Use:** `moonshot/kimi-k2-0905-preview`
- Why: **256K context** - longest available!
- Perfect for: Analyzing large documents, full codebases

### 6. Fast Simple Tasks
**Use:** `minimax/MiniMax-M2.1`
- Why: FREE, fast, excellent quality
- Context: 200K, more than enough for simple tasks

### 7. Cost-Free Tasks (Cron, Sub-Agents)
**Use:** `meta-llama/llama-3.1-405b-instruct:free`
- Why: **405 BILLION PARAMETERS** - best free model!
- Free tier agent configured to use this

### 8. Reasoning-Heavy Tasks (Free)
**Use:** `nousresearch/hermes-3-llama-3.1-405b:free`
- Why: 405B with reasoning capabilities
- Free alternative to paid reasoning models

### 9. Vision Tasks (Free)
**Use:** `nvidia/nemotron-nano-12b-v2-vl:free`
- Why: 12B parameters, 131K context, free vision!
- Alternative: `qwen/qwen-2.5-vl-7b-instruct:free` (lighter)

---

## Agent-Specific Model Assignments

### Main Agent (Complex Tasks)
```json
{
  "model": "zai/glm-4.7",
  "fallback": "minimax/MiniMax-M2.1"
}
```

### Free Tier Agent (Cost-Free Tasks)
```json
{
  "model": "meta-llama/llama-3.1-405b-instruct:free",
  "fallback": ["nousresearch/hermes-3-llama-3.1-405b:free", "deepseek/deepseek-chat"]
}
```

### Vision Agent (Image Tasks)
```json
{
  "model": "MiniMax-Vision-Video-01",
  "fallback": "nvidia/nemotron-nano-12b-v2-vl:free"
}
```

### Long Context Agent (Large Documents)
```json
{
  "model": "moonshot/kimi-k2-0905-preview"
}
```

### Coding Agent (Code Generation)
```json
{
  "model": "minimax/MiniMax-M2.1",
  "fallback": "meta-llama/llama-3.3-70b-instruct:free"
}
```

---

## Decision Flowchart

```
Task requires vision?
├─ YES → Vision model needed
│   ├─ High quality needed → MiniMax-Vision-Video-01
│   └─ Free is fine → Nemotron Nano 12B VL (FREE)
└─ NO → Task type?
    ├─ Complex reasoning → zai/glm-4.7
    ├─ Long context (>200K) → Kimi K2 (256K!)
    ├─ User-facing → zai/glm-4.7
    └─ Cost-free (cron/sub-agent) → Llama 3.1 405B (FREE)
```

---

## Model Selection Quick Reference

| Task | Best Model | Free Alternative |
|------|-----------|------------------|
| Complex reasoning | zai/glm-4.7 | MiniMax-M2.1 |
| Creative writing | zai/glm-4.7 | MiniMax-M2.1 |
| Vision/image | MiniMax-Vision-Video-01 | Nemotron Nano VL (FREE) |
| Long context | Kimi K2 (256K!) | - |
| Simple/fast | MiniMax-M2.1 | - |
| Cron/sub-agents | - | Llama 3.1 405B (FREE) |
| Free reasoning | - | Hermes 3 405B (FREE) |

---

## Cost Optimization Strategy

**Free Models (Use Whenever Possible):**
1. `MiniMax-M2.1` - Excellent quality, 200K context, FREE!
2. `MiniMax-Vision-Video-01` - Vision/video, FREE!
3. `Kimi K2` - 256K context, FREE!
4. `Llama 3.1 405B` - 405B parameters, FREE!
5. `Hermes 3 405B` - Reasoning, FREE!
6. `Nemotron Nano VL` - Vision, FREE!

**Paid Models (Reserve For):**
- `zai/glm-4.7` - Complex user-facing tasks
- `opencode/claude-opus-4-5` - When best quality required

---

## Current Configuration Summary

**Free Tier Agent:** Uses `Llama 3.1 405B` (best free model!)
**Main Agent:** Uses `zai/glm-4.7` (best quality)
**Vision:** `MiniMax-Vision-Video-01` (dedicated)
**Long Context:** `Kimi K2` (256K!)

---

## Next Steps

1. **Apply configurations** to enable specialized agents
2. **Update cron jobs** to use optimal models
3. **Test each model** for quality verification
4. **Document performance** in memory/notes

---

**This file is indexed and searchable via qmd!**

🦞 *Using the right tool for every task*
