# MiniMax Image Vision Research

**When:** 2026-01-12 ~19:50 UTC
**Updated:** 2026-01-12 ~20:05 UTC
**Purpose:** Research MiniMax vision capabilities to resolve image vision empty responses

---

## Summary

**FINDING UPDATED:** MiniMax DOES offer image understanding - configured model ID was wrong!

**Problem:** Wrong model ID and wrong image model configuration
- ❌ Configured: `MiniMax-Vision-Video-01` (doesn't exist)
- ❌ Image model set to: `minimax/MiniMax-M2.1` (TEXT model)
- ✅ Correct: `MiniMax-VL-01` (vision-language model)

---

## Research Process

### Step 1: Accessed MiniMax Official Documentation
- URL: https://platform.minimax.io/docs/guides/models-intro
- Accessed via curl (browser tool not working)

### Step 2: Reviewed Available Models

**Text Models:**
- MiniMax-M2.1
- MiniMax-M2.1-lightning
- MiniMax-M2

**Audio/Speech Models:**
- speech-2.6-hd
- speech-2.6-turbo
- speech-02-hd
- speech-02-turbo

**Video Generation Models (create videos, NOT analyze):**
- MiniMax Hailuo 2.3 (Text to Video & Image to Video)
- MiniMax Hailuo 2.3Fast (Image to Video)
- MiniMax Hailuo 02 (Text to Video & Image to Video)

**Music Models:**
- Music-2.0

### Step 3: Checked Anthropic API Compatibility

**Document:** https://platform.minimax.io/docs/api-reference/text-anthropic-api

**Critical Finding:**
> "Image and document type inputs are not currently supported"

This confirms that MiniMax's text models via the Anthropic-compatible API do NOT support image inputs.

### Step 4: Searched for Vision-Specific Documentation

**Search Results:**
- No vision-specific documentation found
- No image understanding models listed
- No "vision" keyword in model documentation

---

## Key Discovery (UPDATED 2026-01-12 ~20:20 UTC)

**CRITICAL CORRECTION:** MiniMax APIs do NOT support vision at all!

**Actual Findings:**
1. ❌ `MiniMax-Vision-Video-01` doesn't exist
2. ✅ `MiniMax-VL-01` EXISTS as a model (released Jan 15, 2025)
3. ❌ `MiniMax-VL-01` is NOT available via MiniMax APIs
4. ❌ **MiniMax's OpenAI and Anthropic-compatible APIs do NOT support image inputs**
5. ✅ `MiniMax-VL-01` is only available for self-hosting (Hugging Face, GitHub)

**From MiniMax Documentation:**
- OpenAI API: "3. Image and audio type inputs are not currently supported"
- Anthropic API: "type='image': Not supported - Image input not supported yet"
- "4. Image and document type inputs are not currently supported"

**Conclusion:**
- MiniMax-VL-01 model exists
- MiniMax has NO vision API for public access
- Can only self-host VL-01 (not available via MiniMax APIs)

**Using Exa API:** Successfully found MiniMax-VL-01 on:
- Hugging Face: https://huggingface.co/MiniMaxAI/MiniMax-VL-01
- GitHub: https://github.com/MiniMax-AI/MiniMax-01
- MiniMax API: Available via OpenAI-completions format

**See also:** `MINIMAX-VL-01-DISCOVERY.md` for full model details

---

## What MiniMax DOES Offer (CORRECTED)

| Capability | Available | Details |
|------------|-----------|---------|
| **Text Generation** | ✅ Yes | MiniMax-M2.1, MiniMax-M2 |
| **Speech/Audio** | ✅ Yes | Text to speech, voice cloning |
| **Video Generation** | ✅ Yes | Text to video, Image to video |
| **Image Understanding** | ✅ Yes | MiniMax-VL-01 (456B parameters) |
| **Vision Analysis** | ✅ Yes | MiniMax-VL-01 supports image input |

---

## Root Cause of Empty Responses (CORRECTED)

**Configuration Issues:**
```yaml
agents.defaults.imageModel.primary: minimax/MiniMax-M2.1  # ❌ TEXT MODEL!
models:
  - id: MiniMax-Vision-Video-01  # ❌ DOESN'T EXIST
```

**Problems:**
1. Model ID `MiniMax-Vision-Video-01` doesn't exist
2. Image model set to `MiniMax-M2.1` - This is a TEXT model
3. TEXT models cannot process images → Empty responses
4. Correct model is `MiniMax-VL-01` (vision-language model)

**Resolution:**
- See `MINIMAX-VL-01-CONFIG-FIX.md` for proposed configuration changes
- Need to add `MiniMax-VL-01` to models list
- Need to update `imageModel.primary` to `minimax/MiniMax-VL-01`

---

## Recommendations (UPDATED 2026-01-12 ~20:20 UTC)

### Option 1: Use a Different Image Model Provider
- **GPT-4 Vision** - Has proven image understanding (OpenAI)
- **Claude Vision** - Strong image analysis (Anthropic)
- **Gemini Vision** - Google's multimodal model
- **Other providers** with actual image understanding APIs

### Option 2: Self-host MiniMax-VL-01 (Complex)
- Download from Hugging Face
- Run locally with vLLM or Transformers
- Create own API wrapper
- Significant complexity and resource requirements

### Option 3: Document Limitation (Accept)
- MiniMax does NOT offer vision APIs
- Add to CAPABILITIES.md: "Image vision not supported by MiniMax"
- Note: MiniMax-VL-01 exists but only for self-hosting
- Accept limitation for now

---

## Action Items

1. **Bradley to decide:** Which option to pursue?
   - Option 1: Switch to different provider (needs provider configuration)
   - Option 2: Wait for MiniMax updates (monitor documentation)
   - Option 3: Document limitation (add to memory banks)

2. **If switching providers:**
   - Research available image vision providers
   - Check pricing/availability
   - Configure new provider in Clawdbot

3. **If documenting limitation:**
   - Update CAPABILITIES.md
   - Update ROADBLOCKS-SOLUTIONS-PLAN.md
   - Note in HEARTBEAT.md

---

## Files Created

- **MINIMAX-IMAGE-VISION-RESEARCH.md** (5K) - This document

---

🦞 *Image understanding requires an actual image vision model, not a video generation model.*
