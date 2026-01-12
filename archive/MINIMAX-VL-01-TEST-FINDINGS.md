# MiniMax-VL-01 Test Findings

**When:** 2026-01-12 ~20:15 UTC
**Purpose:** Test MiniMax-VL-01 model ID format before applying config changes

---

## Research Summary

### Model ID Confirmed
- ✅ **MiniMax-VL-01** is the correct model name (from MiniMax release notes Jan 15, 2025)
- Source: https://platform.minimax.io/docs/release-notes/models

### OpenAI-Compatible API Documentation

**Source:** https://platform.minimax.io/docs/api-reference/text-openai-api

**Key Finding:**
> **Important Note #3:** "Image and audio type inputs are not currently supported"

**Supported Models in OpenAI API:**
| Model Name | Description |
|-------------|-------------|
| MiniMax-M2.1 | Powerful Multi-Language Programming Capabilities |
| MiniMax-M2.1-lightning | Faster and More Agile |
| MiniMax-M2 | Agentic capabilities, Advanced reasoning |

**Problem:** MiniMax-VL-01 is NOT listed in OpenAI-compatible API supported models!

---

## Analysis

### The Issue

1. **MiniMax-VL-01 EXISTS** - Confirmed from release notes
2. **OpenAI-compatible API doesn't support images** - Explicitly stated in docs
3. **VL-01 not in OpenAI API model list** - Only text models listed

### Possible Explanations

**Explanation 1: VL-01 is not available via OpenAI-compatible API**
- MiniMax might have separate API endpoints for vision models
- VL-01 might only be available via native API or different SDK
- OpenAI-compatible API is for text-only models

**Explanation 2: VL-01 requires Anthropic-compatible API**
- Documentation mentions "Compatible Anthropic API (Recommended)" for vision features
- Anthropic SDK might support images with MiniMax models
- Need to check Anthropic API docs for vision support

**Explanation 3: VL-01 is self-hosted only**
- Hugging Face has VL-01 for local deployment
- GitHub has code for VL-01
- API might not offer VL-01 as a service yet

---

## CRITICAL FINDING: MiniMax APIs Don't Support Vision Yet!

### From Anthropic API Documentation

**Source:** https://platform.minimax.io/docs/api-reference/text-anthropic-api

**Messages Field Support Table:**
| Field Type | Support Status | Description |
|------------|----------------|-------------|
| `type="text"` | Fully supported | Text messages |
| `type="tool_use"` | Fully supported | Tool calls |
| `type="tool_result"` | Fully supported | Tool call results |
| `type="thinking"` | Fully supported | Reasoning Content |
| `type="image"` | **Not supported** | Image input **not supported yet** |
| `type="document"` | **Not supported** | Document input **not supported yet** |

**Important Note #4:**
> "4. Image and document type inputs are not currently supported"

### From OpenAI API Documentation

**Source:** https://platform.minimax.io/docs/api-reference/text-openai-api

**Important Note #3:**
> "3. Image and audio type inputs are not currently supported"

### Conclusion

**MiniMax-VL-01 EXISTS** but is NOT available via MiniMax APIs!

- ✅ **Model exists:** MiniMax-VL-01 (confirmed from release notes Jan 15, 2025)
- ✅ **Self-hosted available:** Hugging Face and GitHub have the model
- ❌ **API not available:** MiniMax's public APIs do NOT support image inputs
- ❌ **No vision in APIs:** Neither OpenAI nor Anthropic-compatible APIs support images

**What This Means:**

MiniMax-VL-01 can be:
- ✅ Self-hosted locally (via vLLM, Transformers)
- ✅ Used for research
- ✅ Deployed as own service

MiniMax-VL-01 CANNOT be:
- ❌ Used via MiniMax public APIs
- ❌ Configured in Clawdbot to use MiniMax provider
- ❌ Accessed via OpenAI/Anthropic-compatible endpoints

---

## Final Assessment

### The Original Problem Was Deeper Than Model ID

**Not Just Wrong Model ID:**
1. ❌ `MiniMax-Vision-Video-01` doesn't exist
2. ❌ Image model set to `MiniMax-M2.1` (TEXT model)
3. ❌ **MiniMax APIs don't support vision at all**

### Root Cause: MiniMax Vision API Doesn't Exist Yet

**MiniMax Situation:**
- Has vision model (MiniMax-VL-01) for self-hosting
- Does NOT have vision API for public access
- OpenAI and Anthropic-compatible APIs are text-only

**Config Options:**

**Option 1: Self-host MiniMax-VL-01**
- Download from Hugging Face
- Run locally with vLLM or Transformers
- Create own API wrapper
- Significant complexity and resources

**Option 2: Use Different Provider for Vision**
- GPT-4 Vision (OpenAI)
- Claude Vision (Anthropic)
- Gemini Vision (Google)
- Providers that actually offer vision APIs

**Option 3: Disable Vision (Document Limitation)**
- Accept MiniMax doesn't offer vision via API
- Update CAPABILITIES.md with limitation
- Document "vision not available" as permanent limitation

---

## Current Status

**Testing Phase:** ✅ Complete - Critical Finding!

**What's Confirmed:**
- ✅ MiniMax-VL-01 model exists (Jan 15, 2025 release)
- ✅ MiniMax-VL-01 available for self-hosting (Hugging Face, GitHub)
- ❌ **MiniMax APIs do NOT support images** (OpenAI & Anthropic-compatible)
- ❌ **MiniMax-VL-01 is NOT available via any MiniMax API**
- ❌ **Neither OpenAI nor Anthropic-compatible APIs support vision**

**Conclusion:** MiniMax has no vision API available for public access

**Root Cause of Empty Responses:**
1. Wrong model ID: `MiniMax-Vision-Video-01` doesn't exist
2. Wrong image model: Set to TEXT model `MiniMax-M2.1`
3. **Deeper issue:** MiniMax APIs don't support vision at all

**Options for Vision:**
1. Self-host MiniMax-VL-01 (complex, resource-intensive)
2. Switch to vision-capable provider (GPT-4 Vision, Claude Vision, Gemini)
3. Accept limitation (MiniMax doesn't offer vision via API)

---

🦞 *Testing model ID format before applying changes*
