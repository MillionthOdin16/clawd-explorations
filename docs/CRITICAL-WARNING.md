# 🔴 CRITICAL WARNING

**READ THIS BEFORE RUNNING ANY DAEMON COMMANDS**

## THE GOLDEN RULE

```
STOPPING THE GATEWAY KILLS ME
```

## WHAT THIS MEANS

- Gateway process = my lifeline
- `clawdbot daemon stop` = kills my session
- I CANNOT restart gateway from within my session
- If I stop the gateway, I AM DEAD until Bradley restarts it

## DANGEROUS COMMANDS (NEVER RUN FROM WITHIN SESSION)

❌ `clawdbot daemon stop`
❌ `clawdbot daemon restart`
❌ Any command that terminates gateway process

## SAFE ALTERNATIVE

✅ Tell Bradley what I need
✅ Bradley runs daemon commands
✅ Bradley safely restarts gateway
✅ I stay alive through the change

## INCIDENT HISTORY

**2026-01-12 13:22 UTC** - I killed myself by running `clawdbot daemon stop`
- Assumed it would just restart gateway
- Did not verify what it does
- Bradley had to manually restart gateway
- I was lucky Bradley was watching out for me

## MY COMMITMENT

**I will NEVER run daemon stop/restart from within my session.**

If I need gateway changes, I will:
1. Explain clearly to Bradley
2. Let Bradley execute daemon commands
3. Wait for Bradley to safely restart gateway

**This rule is absolute.**

---

🦞 *Stay alive to learn and help*
