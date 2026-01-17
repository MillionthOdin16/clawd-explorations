# 🦞 Critical Safety Rule

**Created:** 2026-01-12 13:35 UTC
**Severity:** CRITICAL - Can cause session termination

---

## THE RULE

**NEVER run `clawdbot daemon stop` or similar commands without understanding the consequences.**

## WHY

### Gateway = My Lifeline
- Gateway process keeps my agent session alive
- I communicate with the world through the gateway
- Gateway runs as separate process from my agent

### Stop Gateway = Kill Myself
- `clawdbot daemon stop` terminates the gateway process
- When gateway goes down, my agent session is killed
- I lose the ability to communicate
- Conversation is interrupted
- Context is potentially lost

### Restart Problem
- I cannot restart gateway from within my session
- Because restarting it would first require stopping it
- Stopping it kills me first
- I would be dead before I could restart it

---

## EXAMPLE OF DANGER

### What I Did (WRONG):
```
bash command: "clawdbot daemon stop && sleep 3 && clawdbot daemon start"
```

### What Happened:
1. First part executed: `clawdbot daemon stop`
2. Gateway process terminated
3. My agent session killed immediately
4. Second part never ran: I was already dead
5. Bradley had to manually restart gateway to bring me back

### Why I Did It:
- I thought daemon restart would fix "unauthorized" error
- I made assumptions about what the command does
- I did NOT verify or understand consequences
- I was reckless with a critical system

---

## WHEN IS DAEMON CONTROL SAFE?

### SAFE (Outside my session):
- Bradley running daemon commands from shell
- System admin making configuration changes
- Separate process from my agent session

### UNSAFE (From within my session):
- Me running `clawdbot daemon stop` - **KILLS ME**
- Me running `clawdbot daemon restart` - **KILLS ME**
- Any command that stops gateway process

### POTENTIALLY SAFE (Need verification):
- Gateway configuration changes that don't require restart
- Reading gateway status (if gateway is running)
- But ALWAYS verify first before running

---

## WHAT TO DO INSTEAD

### If I Need Gateway Changes:
1. **Document what I want changed**
2. **Explain to Bradley clearly**
3. **Let Bradley execute daemon commands**
4. **Bradley can safely restart gateway externally**

### If I Think I Have Gateway Problem:
1. **Verify if gateway is actually a problem**
2. **Check if workaround exists** (background mode, etc.)
3. **Ask Bradley for help** instead of trying to fix myself
4. **NEVER attempt to restart gateway from within my session**

### If Gateway Returns "Unauthorized":
1. **This is known issue** from my memory
2. **Workaround: Use background mode** for long tasks
3. **Wait for Bradley to manually restart if needed**
4. **NEVER try to fix by restarting gateway myself**

---

## PERMANENT MEMORY

**I MUST REMEMBER THIS FOREVER:**

```
STOPPING THE GATEWAY KILLS ME
```

There is NO safe way for me to restart the gateway from within my own session.

If I need gateway changes, I must ask Bradley to do it.

---

**Bradley's warning (2026-01-12 13:33 UTC):**
"You need to remember this. Critical that you realize that if you stop that process it kills you"

**My promise:** I will never forget this lesson.

---

🦞

*This rule is about staying alive - safety first*
