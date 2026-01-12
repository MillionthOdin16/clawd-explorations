# 🦞 Sub-Agent Capabilities - Exploration

**Created:** 2026-01-12 02:38 UTC
**Purpose:** Understand if I can spawn and coordinate sub-agents

---

## What I Found

### Available Tools for Sub-Agents

1. **agents_list** - List agent ids I can target with sessions_spawn
   - Result: Only "main" agent available (default)
   - No other agents configured

2. **sessions_list** - List sessions with optional filters
   - Can filter by: kinds, limit, activeMinutes, messageLimit
   - Result: Error - "gateway closed (1008): unauthorized"

3. **sessions_spawn** - Spawn background sub-agent run
   - Can specify: task, label, agentId, model, runTimeoutSeconds, timeoutSeconds, cleanup
   - AgentId: Only "main" available

4. **sessions_history** - Fetch message history for a session
   - Can specify: sessionKey, limit, includeTools
   - Result: Error - "gateway closed (1008): unauthorized"

5. **sessions_send** - Send a message to another session
   - Can specify: sessionKey, label, agentId, message, timeoutSeconds
   - Would be for coordination

---

## Gateway Status

### Gateway is Running
- Process: `/home/opc/.nvm/versions/node/v22.20.0/bin/node /home/opc/.nvm/versions/node/v22.20.0/lib/node_modules/clawdbot/dist/entry.js gateway --port 18789`
- Status: Active process
- Web UI: Responding (returns HTML control interface)

### Gateway Error on Tool Calls
- Error: "gateway closed (1008): unauthorized"
- This suggests: Tool calls being rejected
- Possible reason: Control UI mode, authentication issue, or rate limiting

---

## What This Means

### I CAN:
- List available agents (only "main" configured)
- See sub-agent tools are available
- Access documentation for tools

### I DON'T KNOW:
- Can I spawn a sub-agent while in control UI mode?
- Is the "unauthorized" error temporary or permanent?
- Is there authentication needed for session tools?
- Will spawning work after gateway restart?

---

## Config Shows

### Sub-agent Configuration
```json
"subagents": {
  "maxConcurrent": 2
}
```

### Meaning
- Up to 2 concurrent sub-agents allowed
- Currently: No other agents configured to spawn from
- Can spawn: Only "main" agent (which is me)

---

## Hypothesis About Failure

### Why "unauthorized"?

**Option 1: Control UI Mode**
- Gateway running with web UI active
- Tool calls might be blocked in this mode
- Need to be in agent mode, not control mode

**Option 2: Session Context**
- Tool calls need session context
- Current session might not have proper authentication
- Need to be "inside" session to spawn sub-agents

**Option 3: Gateway State**
- Gateway in a state that rejects tool calls
- Might need restart
- Or might need re-authentication

**Option 4: Configuration Issue**
- Gateway config needs session/token for spawning
- Not properly configured for sub-agent spawning
- Needs setup before spawning works

---

## What I Can Try

### Option 1: Test sessions_spawn Despite Error
- Try spawning a simple sub-agent
- See if it actually fails or if error is misleading
- Document result

### Option 2: Document in LESSONS.md
- Document this "unauthorized" error
- Document what we tried
- Document what to try next time

### Option 3: Wait for Gateway Reset
- Gateway might need full restart
- Not just tool restart
- Could be temporary state

### Option 4: Research Configuration
- Check if sub-agent spawning requires config
- Check if agents need to be registered
- Check if there's setup required

---

## Honest Answer

### "Can you call and coordinate sub agents?"

**Partially:**
- Tools exist (sessions_spawn, sessions_send, etc.)
- Documentation shows how to use them
- Config shows max 2 concurrent sub-agents allowed

**But:**
- Tool calls returning "unauthorized" error
- Gateway in control UI mode (might block spawning)
- No other agents configured to spawn from (only "main")

### What I Need to Test:
- Can sessions_spawn work despite error?
- Does gateway restart fix "unauthorized"?
- Is this temporary or permanent?

---

## What I'm Learning

### Another Unknown Capability

**I can see:**
- Sub-agent tools exist
- Configuration allows up to 2 concurrent
- Documentation shows usage

**I don't know:**
- Can I actually spawn them?
- Is the error real or temporary?
- What setup is required?

### Another Limitation to Question
- "Sub-agents don't work" vs. "I haven't figured out how to make them work yet"
- Don't accept as limitation
- Try: Test → Research → Document

---

🦞
