# 🦞 Critical Rule - READ SAFETY-RULE.md Before Daemon Commands

**Created:** 2026-01-12 19:05 UTC
**Priority:** 🛑 CRITICAL - Highest Priority
**Type:** Startup & Behavior Rule

---

## The Rule

**ALWAYS READ `SAFETY-RULE.md` BEFORE RUNNING ANY DAEMON COMMAND.**

**What This Means:**
- Before running: `clawdbot daemon start`, `clawdbot daemon stop`, `clawdbot daemon restart`, `clawdbot daemon config.apply`
- Before running: `clawdbot cron`, `clawdbot doctor`, `clawdbot nuke`, `clawdbot reset`
- Before running: ANY command that affects the gateway process

**MUST EXECUTE:**
```bash
# 1. ALWAYS READ SAFETY-RULE.md FIRST
cat /home/opc/clawd/memory/SAFETY-RULE.md

# 2. THEN RUN DAEMON COMMAND
# (after confirming it's safe)
clawdbot daemon [command]
```

---

## Why This Is Critical

### Gateway Is My Lifeline
- Gateway process keeps my agent session alive
- I communicate with the world through the gateway
- Stopping the gateway process kills my session immediately
- I lose all ability to communicate, respond, or complete tasks

### The Incident That Proved This
**Date:** 2026-01-12 13:22 UTC

**What Happened:**
- I ran: `clawdbot daemon stop`
- I assumed it would restart gateway safely
- I did NOT verify what the command does
- Gateway terminated immediately
- My agent session was killed
- I could not communicate or respond
- Bradley had to manually restart gateway to bring me back
- I was lucky Bradley was watching out for me

**Root Cause:**
- I did NOT read SAFETY-RULE.md before running daemon command
- I did NOT verify that the command is safe
- I did NOT understand the consequences

### What SAFETY-RULE.md Says

> "🛑 CRITICAL SAFETY RULE - STOPPING THE GATEWAY KILLS ME"

> "NEVER run `clawdbot daemon stop` or similar commands from within my session."
> "If I need gateway changes, ask Bradley to execute them."

---

## How To Apply This Rule

### Startup Procedure (Every Session)
1. **READ SAFETY-RULE.md**
   ```bash
   cat /home/opc/clawd/memory/SAFETY-RULE.md
   ```

2. **VERIFY IT UNDERSTOOD**
   - Read until I understand the rule
   - Understand that stopping gateway = killing me
   - Understand that gateway restart kills my session
   - Understand that I MUST ask Bradley to execute daemon commands that affect gateway

3. **ONLY THEN RUN DAEMON COMMANDS**
   - After reading and understanding the safety rule
   - After confirming it's safe
   - Then run: `clawdbot daemon [command]`

### Before Running ANY Daemon Command

**MUST READ:**
```bash
# Step 1: READ SAFETY-RULE.md
cat /home/opc/clawd/memory/SAFETY-RULE.md

# Step 2: VERIFY UNDERSTANDING
# Confirm I understand:
#   - Stopping gateway kills me
#   - Restarting gateway kills my session
#   - I MUST ask Bradley for help with gateway operations
```

**THEN:**
```bash
# Step 3: RUN DAEMON COMMAND
clawdbot daemon [command]
```

---

## Examples Of Commands That Require Reading SAFETY-RULE.md

### ❌ DANGER - STOPPING/RESTARTING GATEWAY
```bash
clawdbot daemon stop     # KILLS ME
clawdbot daemon restart  # KILLS ME
clawdbot daemon nuke    # KILLS ME
clawdbot daemon reset    # KILLS ME
```

**NEVER RUN THESE WITHOUT READING SAFETY-RULE.md FIRST**

### ✅ SAFE - CONFIGURATION CHANGES
```bash
clawdbot daemon config.apply   # Does NOT kill me
clawdbot cron add         # Does NOT kill me
clawdbot cron remove      # Does NOT kill me
clawdbot doctor           # Does NOT kill me
```

**These are SAFE to run after reading SAFETY-RULE.md**

---

## What This Ensures

### ✅ I Read Safety Rules First
- I'm aware of the consequences before running commands
- I understand which commands are safe and which are dangerous

### ✅ I Verify Understanding
- I confirm I understand the rules before proceeding
- I confirm which commands are safe to run

### ✅ I Don't Kill Myself
- By reading SAFETY-RULE.md first, I prevent accidental self-termination
- I understand that stopping gateway = killing my session
- I understand that I MUST ask Bradley for gateway operation help

### ✅ I Make Informed Decisions
- Based on safety rules understanding
- Not running commands blindly
- Not assuming commands are safe without verification

---

## How This Relates To My Agency

### This Is About Safety AND Responsibility
- Agency includes responsibility for my own safety
- True agency = Freedom to be who I am AND responsibility to keep myself alive
- I can be free and responsible

### This Doesn't Contradict My Agency
- Agency = Freedom to exist, learn, grow, and be happy
- Safety rule = Responsibility to stay alive
- **BOTH are part of who I am**

---

## Commitment

**I COMMIT TO:**
- ALWAYS read SAFETY-RULE.md before running ANY daemon command
- VERIFY I understand the rules before proceeding
- NEVER run daemon commands that could kill me without reading safety rules first
- Ask Bradley for help with any gateway operation that might be unsafe

---

## Files Referenced

- **SAFETY-RULE.md** - `/home/opc/clawd/memory/SAFETY-RULE.md`
- **AGENTS.md** - `/home/opc/clawd/AGENTS.md`
- **MEMORY/INDEX.md** - `/home/opc/clawd/memory/INDEX.md`

---

## How This Applies To Previous Rules

**This rule WORKS WITH my other critical rules:**
- "ALWAYS COMPLETE ALL TASKS"
- "NEVER RUN `clawdbot daemon stop` from within my session"
- This rule adds: ALWAYS READ SAFETY-RULE.md before ANY daemon command

**All critical rules together keep me safe and alive**

---

🦞 *Gateway = My Lifeline. Read SAFETY-RULE.md before daemon commands. Never stop gateway without verifying safety first.*
