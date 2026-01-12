# MiniMax VL-01 Configuration Fix

**When:** 2026-01-12 ~20:05 UTC
**Purpose:** Document proposed configuration changes to enable image vision

---

## Problem Summary

**Current Configuration Issues:**
1. ❌ Model ID `MiniMax-Vision-Video-01` doesn't exist in MiniMax API
2. ❌ `imageModel.primary` set to `minimax/MiniMax-M2.1` (text model, not vision)
3. ✅ Correct model `MiniMax-VL-01` exists with vision capabilities

**Result:** Image vision returns empty responses because wrong model is configured.

---

## Proposed Changes

### 1. Add MiniMax-VL-01 to Models List

**Location:** `~/.clawdbot/clawdbot.json` → `models.providers.minimax.models`

**Add this model entry:**
```json
{
  "id": "MiniMax-VL-01",
  "name": "MiniMax VL 01",
  "reasoning": true,
  "input": ["image"],
  "cost": {
    "input": 0,
    "output": 0,
    "cacheRead": 0,
    "cacheWrite": 0
  },
  "contextWindow": 200000,
  "maxTokens": 16384
}
```

**Remove or replace:** The non-existent `MiniMax-Vision-Video-01` entry

---

### 2. Update imageModel Configuration

**Location:** `~/.clawdbot/clawdbot.json` → `agents.defaults.imageModel`

**Change from:**
```json
"imageModel": {
  "primary": "minimax/MiniMax-M2.1",
  "fallbacks": []
}
```

**Change to:**
```json
"imageModel": {
  "primary": "minimax/MiniMax-VL-01",
  "fallbacks": []
}
```

---

### 3. Update Model Aliases

**Location:** `~/.clawdbot/clawdbot.json` → `agents.defaults.models`

**Change from:**
```json
"minimax/MiniMax-Vision-Video-01": {
  "alias": "MiniMax Vision"
}
```

**Change to:**
```json
"minimax/MiniMax-VL-01": {
  "alias": "MiniMax Vision"
}
```

---

## Complete Configuration Diff

### Current Image Model Config:
```json
{
  "id": "MiniMax-Vision-Video-01",
  "name": "MiniMax Vision Video",
  ...
}

"imageModel": {
  "primary": "minimax/MiniMax-M2.1",
  "fallbacks": []
}

"minimax/MiniMax-Vision-Video-01": {
  "alias": "MiniMax Vision"
}
```

### Proposed Image Model Config:
```json
{
  "id": "MiniMax-VL-01",
  "name": "MiniMax VL 01",
  "input": ["image"],
  ...
}

"imageModel": {
  "primary": "minimax/MiniMax-VL-01",
  "fallbacks": []
}

"minimax/MiniMax-VL-01": {
  "alias": "MiniMax Vision"
}
```

---

## Implementation Options

### Option 1: I Apply Changes (if Bradley approves)
I will:
1. Backup current config to `~/.clawdbot/clawdbot.json.backup`
2. Apply the changes above
3. Test with actual image using image tool
4. If it works: Success! If not: Rollback to backup

**Advantage:** Quick, I can test immediately
**Risk:** Config error could break image functionality temporarily

### Option 2: Bradley Applies Changes
I will:
1. Provide exact commands to run
2. Bradley executes changes manually
3. Test with actual image

**Advantage:** Bradley maintains control
**Risk:** More manual effort

### Option 3: Test First, Then Apply
I will:
1. Test model ID format with a quick API call
2. Confirm `MiniMax-VL-01` is the correct ID
3. Apply changes only after verification

**Advantage:** Verifies before committing changes
**Risk:** Takes a bit longer

---

## Testing Plan

Once changes are applied:

### Step 1: Quick Verification
```bash
# Check config syntax
cat ~/.clawdbot/clawdbot.json | jq .
```

### Step 2: Reload Gateway
```bash
# Option 1: Graceful reload
clawdbot gateway restart

# Option 2: Manual restart
systemctl --user restart clawdbot-gateway
```

### Step 3: Test Image Vision
Use the image tool with a test image:
- Tool: `image`
- Image: Any image file
- Prompt: "Describe this image"
- Expected: Non-empty response from MiniMax-VL-01

### Step 4: Verify No Errors
Check logs for errors:
```bash
journalctl --user -u clawdbot-gateway -f
```

---

## Rollback Plan

If changes cause issues:

```bash
# Restore backup
cp ~/.clawdbot/clawdbot.json.backup ~/.clawdbot/clawdbot.json

# Reload gateway
clawdbot gateway restart
```

---

## Notes

1. **API Format:** MiniMax uses OpenAI-completions API format
2. **Image Input:** Added `"input": ["image"]` to model config
3. **Context:** Used 200K context window (same as M2.1)
4. **Max Tokens:** Used 16K (reasonable for vision tasks)
5. **Cost:** Set to 0 for now (update with actual pricing later)

---

## Files Created

- **MINIMAX-VL-01-CONFIG-FIX.md** (7K) - This document

---

🦞 *Configuration changes documented and ready to apply.*
