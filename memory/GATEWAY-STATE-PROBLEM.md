# 🦞 Gateway State Problem - Session Tools Blocked

**Created:** 2026-01-12 14:48 UTC
**Status:** ✅ RESOLVED - Root cause found and fixed
**Resolved:** 2026-01-12 15:33 UTC

---

## The Problem

### Symptoms
**Gateway returns "unauthorized" error** on all configuration tools:
- `sessions_spawn` - blocked (can't spawn sub-agents)
- `cron` - blocked (can't manage cron jobs)
- `gateway config.get` - blocked (can't read config)
- `gateway config.apply` - blocked (can't apply changes)
- `gateway config.schema` - blocked (can't see schema)

### When This Happened
- **2026-01-12 12:33 UTC** - Discovered sub-agent spawning blocked
- **Multiple restart attempts** - Gateway restarted but "unauthorized" persisted
- **Agent remains running** - Can respond and use most tools
- **But config tools blocked** - Can't spawn sub-agents, can't configure

---

## Current Configuration

### Gateway Config
```json
"gateway": {
  "port": 18789,
  "mode": "local",
  "bind": "lan",
  "auth": {
    "mode": "token",
    "token": "3b2ebf428c1591116ea06bee9a76493407f3efb7cd0d7b73"
  }
}
```

### Session Config
```json
"agents": {
  "defaults": {
    "workspace": "/home/opc/clawd",
    "thinkingDefault": "high",
    "blockStreamingDefault": "off",
    "subagents": {
      "maxConcurrent": 4
    }
  }
}
```

---

## What Works

### ✅ Working Tools
- All basic tools (bash, read, write, edit, exec, message, etc.)
- Gateway communication (responding to Bradley on Telegram)
- File operations (git, etc.)
- Web access (curl, etc.)
- All non-gateway tools

### ❌ Blocked Tools
- `sessions_spawn` - Returns "unauthorized"
- `cron` - Returns "unauthorized"
- `gateway config.get` - Returns "unauthorized"
- `gateway config.apply` - Returns "unauthorized"
- `gateway config.schema` - Returns "unauthorized"

---

## What I Tried

### Restart Attempts (All Failed)
1. **kill gateway process** - Gateway restarted but state persisted
2. **`clawdbot daemon stop && start`** - Gateway restarted, state persisted
3. **`clawdbot daemon restart`** - Not tested (would kill me)
4. **New token** - Bradley provided new token, not tested yet

### What Didn't Work
- **Simply restarting gateway** - "unauthorized" state returns after restart
- **Killing and restarting** - Same result, state persists
- **Multiple restart attempts** - No change

---

## Hypotheses

### 1. Token Mismatch
**Possibility:** Gateway config token vs. what gateway expects
**Evidence:** Current token in config is old format
**Test:** Bradley provided new token `3b2ebf428c1591116ea06bee9a76493407f3efb7cd0d7b73`
**Status:** Not tested yet

### 2. Gateway Authentication State
**Possibility:** Gateway has internal auth state that's not reset by restart
**Evidence:** Restart doesn't clear state
**Status:** Unknown

### 3. Session Authentication
**Possibility:** My session isn't using correct auth token
**Evidence:** I can communicate but config tools blocked
**Status:** Unknown

### 4. Gateway Bind Mode
**Possibility:** "lan" mode requires different auth setup
**Evidence:** `bind: "lan"` in config
**Status:** Unknown

---

## What I Can't Do

### From Within My Session
- ❌ Restart gateway (would kill me per SAFETY-RULE.md)
- ❌ Apply gateway configuration
- ❌ Spawn sub-agents
- ❌ Manage cron jobs
- ❌ Read/write gateway config

### What I CAN Do
- ✅ Continue working with basic tools
- ✅ Document the problem
- ✅ Create instructions for Bradley
- ✅ Wait for Bradley to fix gateway

---

## What Needs To Happen

### Bradley Actions Required

1. **Test new token** - Update gateway config with token Bradley provided
2. **Restart gateway service** - From system, not from within my session
3. **Wait for me to reconnect** - I'll come back online after restart
4. **Test if tools work** - Try sessions_spawn, cron, etc.

### Or Alternative

1. **Find root cause** - Why is gateway returning "unauthorized"?
2. **Fix authentication** - Update/reset gateway auth state
3. **Clear cache/state** - If gateway has internal state that needs reset
4. **Apply proper fix** - Not just restart, but real fix

---

## Impact

### What I Can't Do
- Spawn sub-agents for parallel tasks
- Create/modify cron jobs for automation
- Adjust gateway configuration
- Read gateway config programmatically

### What I Can Still Do
- All basic tools (bash, file operations, web access)
- Communicate via Telegram
- Run scripts
- Use git
- Work with DigitalOcean, Coolify APIs
- Manage LittleClawd

---

## Documentation

### Created Files
- `docs/GATEWAY-TOKEN-UPDATE.md` - Instructions for Bradley to update token
- `gateway-token-update.json` - JSON patch with new token
- `memory/GATEWAY-STATE-PROBLEM.md` - This file (you're reading it)

### Memory Index Updated
- INDEX.md includes "Before Running Gateway Commands" checklist
- References this file for troubleshooting

---

## Status

**Current:** Agent running, communicating with Bradley
**Problem:** Gateway config tools blocked ("unauthorized")
**Needs:** Bradley intervention to update/fix gateway

---

## ✅ RESOLUTION

**When:** 2026-01-12 15:33 UTC

### Root Cause Found
**Token mismatch between systemd service environment variable and config file:**

| Source | Token |
|--------|--------|
| Systemd env var | `fd08c830f9b3aa94a90841c91b05f5ef04474eeaf1c87baf` |
| Config file | `7959117aed5acbfe0c84812f8d016d383181e142649fb13d` |

Gateway process was started with `CLAWDBOT_GATEWAY_TOKEN` environment variable in systemd service. Environment variables have higher priority than config files. When the agent tried to connect using the config file token, the gateway rejected it as "unauthorized" (WebSocket error 1008).

### Solution Applied

**File:** `/home/opc/.config/systemd/user/clawdbot-gateway.service`

**Changed:**
```diff
- Environment=CLAWDBOT_GATEWAY_TOKEN=fd08c830f9b3aa94a90841c91b05f5ef04474eeaf1c87baf
+ # Environment=CLAWDBOT_GATEWAY_TOKEN=fd08c830f9b3aa94a90841c91b05f5ef04474eeaf1c87baf
```

**Steps:**
1. Commented out `CLAWDBOT_GATEWAY_TOKEN` from systemd service file
2. Reloaded systemd daemon: `systemctl --user daemon-reload`
3. Restarted gateway service: `systemctl --user restart clawdbot-gateway.service`
4. Gateway now reads token from config file (`/home/opc/.clawdbot/clawdbot.json`)

### Result
- Gateway started successfully with config token
- sessions_spawn now works (tested successfully)
- Child session `agent:main:subagent:eda6eaa4-5401-4f82-aabb-0acd2c595177` spawned and completed
- All gateway config tools now accessible

### Lesson Learned

**Environment variables override config files in systemd services.**

When troubleshooting authentication issues:
1. Check config file (`gateway.auth.token`)
2. Check environment variables (`CLAWDBOT_GATEWAY_TOKEN`)
3. Check systemd service environment
4. Verify which source gateway is actually using
5. Priority: command line opts > env vars > config file

### Why Previous Hypotheses Were Wrong

**Token Mismatch:** Correct hypothesis, but wrong source. Thought it was old token vs new token. It was env var vs config.

**Gateway State Reset:** Not the issue. State persisted because env var was still set after each restart.

**Session Authentication:** Not the issue. My session was using config token, which was correct for what it should be, but gateway was using env var.

**Bind Mode:** Not the issue. "lan" mode works fine.

---

**Note:** This problem occurred from 2026-01-12 12:33 UTC to 15:33 UTC (3 hours). Now resolved.

---

🦞 *Gateway state problem resolved - lessons learned*
