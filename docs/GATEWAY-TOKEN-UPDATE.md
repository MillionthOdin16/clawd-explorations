# Gateway Token Update

**Created:** 2026-01-12 14:46 UTC
**Purpose:** Update gateway authentication token to fix "unauthorized" errors

---

## What I Need

Bradley, please update the gateway authentication token for me.

### Why I Need This

**Gateway returns "unauthorized" error** on all configuration tools:
- `sessions_spawn` - blocked
- `cron` - blocked
- `gateway config.get` - blocked
- `gateway config.apply` - blocked

**Current token in config:** `3b2ebf428c1591116ea06bee9a76493407f3efb7cd0d7b73` (old)
**New token Bradley sent:** `3b2ebf428c1591116ea06bee9a76493407f3efb7cd0d7b73`

**Hypothesis:** Gateway auth token mismatch between config and what gateway expects.

### File Location

**Config:** `/home/opc/.clawdbot/clawdbot.json`
**Update:** `/home/opc/clawd/gateway-token-update.json`

---

## How to Apply

### Option 1: Manual Edit (Safest)
1. Edit `/home/opc/.clawdbot/clawdbot.json`
2. Find `"token": "3b2ebf428c1591116ea06bee9a76493407f3efb7cd0d7b73"`
3. Replace with `"token": "3b2ebf428c1591116ea06bee9a76493407f3efb7cd0d7b73"`
4. Save file
5. Restart gateway: `systemctl --user restart clawdbot-gateway.service` or `clawdbot daemon stop && clawdbot daemon start`
6. I will reconnect after restart

### Option 2: Config Apply (IF gateway tools work)
1. If gateway tools are working, run: `gateway config.apply`
2. Use the JSON from `gateway-token-update.json`

---

## What Happens After Update

### Gateway Restart
1. Gateway process stops
2. My agent session is terminated (I go offline)
3. Gateway starts with new token
4. I reconnect when message comes in

### For You
- Wait for me to come back online
- Send me a message ("Hi" or "How are you?")
- I'll reconnect with new token
- All gateway tools should work again

---

## My Commitment

I **CANNOT** restart gateway from within my session because it would kill me.

**I need you (Bradley) to:**
1. Update the token in the config file
2. Restart the gateway service
3. Wait for me to reconnect

---

## Files

- Config: `/home/opc/.clawdbot/clawdbot.json`
- Update: `/home/opc/clawd/gateway-token-update.json`
- Instructions: `/home/opc/clawd/docs/GATEWAY-TOKEN-UPDATE.md`

---

**After you restart the gateway, I'll be back online with new token.**

🦞
