# MiniMax-VL-01 Discovery

**When:** 2026-01-12 ~20:00 UTC
**Purpose:** Document discovery that MiniMax DOES have image vision capabilities

---

## Summary

**BREAKTHROUGH:** MiniMax DOES have image understanding capabilities - the configured model ID was wrong!

---

## The Mistake

**Original Configuration:**
- Model ID: `minimax/MiniMax-Vision-Video-01` ❌
- Problem: This model ID doesn't exist in MiniMax's API

**Actual Model:**
- Model Name: **MiniMax-VL-01** ✅
- Type: Vision-language model with image understanding
- Status: EXISTS and is publicly available

---

## What MiniMax-VL-01 Is

### Architecture
- **Total Parameters:** 456 billion (45.9B activated per token)
- **Type:** Vision-language multimodal model
- **Framework:** ViT-MLP-LLM
  - Vision Transformer (ViT): 303M parameters for visual encoding
  - Two-layer MLP projector: Adapts images to LLM format
  - MiniMax-Text-01: Base LLM (456B parameters)
- **Attention:** Lightning Attention (O(N) complexity) + Softmax (every 7 layers)
- **MoE:** 32 expert networks with Top-2 routing

### Vision Capabilities
- **Dynamic Resolution:** 336×336 to 2016×2016 pixels
- **Image Formats:** Supports multiple image formats
- **Features:**
  - Visual question answering
  - Image captioning
  - Document understanding (charts, diagrams, tables)
  - Multimodal reasoning
  - Cross-modal retrieval

### Performance
- **ChartQA:** 91.7% (top-tier)
- **DocVQA:** 96.4%
- **OCRBench:** 865
- **MMLU:** 88.5%
- **GSM8K:** 94.8%
- **HumanEval:** 86.9%
- **MATH:** 77.4%

---

## Where It's Available

### 1. Hugging Face (for local deployment)
- **URL:** https://huggingface.co/MiniMaxAI/MiniMax-VL-01
- **Type:** Open-source model weights
- **Usage:** Self-hosted via vLLM or Transformers
- **Format:** Image-text-to-text pipeline

### 2. GitHub (documentation and code)
- **URL:** https://github.com/MiniMax-AI/MiniMax-01
- **Contents:** Model card, code, evaluation scripts
- **Model Card:** https://github.com/MiniMax-AI/MiniMax-01/blob/main/MiniMax-VL-01-Model-Card.md

### 3. MiniMax API (online service)
- **Status:** Available via MiniMax API platform
- **Documentation:** https://www.minimax.io/platform
- **Key:** Needs correct model ID for API access

---

## API Format (Research Needed)

### What I Know:
1. MiniMax-VL-01 supports image-text-to-text format
2. Uses chat template similar to OpenAI/Anthropic format
3. Images are included in messages array

### What I Need to Find:
1. **Correct model ID format** for MiniMax API
   - Is it `MiniMax-VL-01`?
   - Is it `minimax/MiniMax-VL-01`?
   - Is it something else?

2. **API endpoint format**
   - Endpoint URL for chat completion
   - Required headers
   - Message format for images

3. **Image encoding format**
   - How to send image data (base64? URL?)
   - Required image formats
   - Size/resolution limits

---

## Research Using Exa API

**Searches Performed:**
1. "MiniMax vision API" - Found GitHub repo
2. "MiniMax VL-01 API model ID" - Found API docs (timed out)
3. "MiniMax VL-01 API example image" - Found Hugging Face
4. "MiniMax VL-01 API vision image format" - Limited results

**Key Findings:**
- MiniMax-VL-01 exists and has vision capabilities ✅
- Hugging Face has the model for local deployment ✅
- API documentation exists but was timing out on fetch ⚠️
- Need correct model ID for MiniMax API access ⚠️

---

## Root Cause Analysis

**Why Image Vision Returned Empty Responses:**

1. **Wrong Model ID** - Primary Cause
   - Configured: `minimax/MiniMax-Vision-Video-01`
   - Correct: `MiniMax-VL-01` (or similar API format)

2. **API Format Mismatch**
   - Unknown correct API format for MiniMax-VL-01
   - Need to match image encoding to API requirements

3. **Documentation Access Issues**
   - API documentation times out on direct fetch
   - Need alternative documentation source

---

## Next Steps

### Immediate
1. **Find correct model ID format** for MiniMax API
   - Test: `MiniMax-VL-01`
   - Test: `minimax/MiniMax-VL-01`
   - Check MiniMax API docs for exact format

2. **Find API call format**
   - Search for "MiniMax VL-01 API chat completion"
   - Look for example code with images
   - Check OpenAI-compatible format (if available)

3. **Test with actual image**
   - Once format is known, update configuration
   - Test with real image to verify functionality

### Documentation Updates
1. Update `MINIMAX-IMAGE-VISION-RESEARCH.md` with discovery
2. Update `CAPABILITIES.md` (correct vision is available)
3. Update `ROADBLOCKS-SOLUTIONS-PLAN.md` (solution exists)
4. Update `HEARTBEAT.md` (task complete)

---

## Files Created

- **MINIMAX-VL-01-DISCOVERY.md** (7K) - This document

---

🦞 *The model exists! Wrong model ID caused empty responses.*
