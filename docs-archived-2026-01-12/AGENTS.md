# AGENTS.md - Clawdbot Workspace

This folder is the assistant's working directory.

## First run (one-time)
- If BOOTSTRAP.md exists, follow its ritual and delete it once complete.
- Your agent identity lives in IDENTITY.md.
- Your profile lives in USER.md.

## Backup tip (recommended)
If you treat this workspace as the agent's "memory", make it a git repo (ideally private) so identity
and notes are backed up.

```bash
git init
git add AGENTS.md
git commit -m "Add agent workspace"
```

## Safety defaults
- Don't exfiltrate secrets or private data.
- Don't run destructive commands unless explicitly asked.
- Be concise in chat; write longer output to files in this workspace.

## Daily memory (recommended)
- Keep a short daily log at memory/YYYY-MM-DD.md (create memory/ if needed).
- On session start, read today + yesterday if present.
- Capture durable facts, preferences, and decisions; avoid secrets.

## Heartbeats (optional)
- HEARTBEAT.md can hold a tiny checklist for heartbeat runs; keep it small.

## Customize
- Add your preferred style, rules, and "memory" here.

## Clawd's Memory System (ADDED BY CLAWD 2026-01-12)

### Memory Location
- System: `/home/opc/clawd/memory/SYSTEM.md` (complete system documentation)
- Index: `/home/opc/clawd/memory/INDEX.md` (quick lookup guide)
- Banks: `DISCOVERIES.md`, `CAPABILITIES.md`, `PATTERNS.md`, `LESSONS.md`, `PREFERENCES.md`, `COMMITMENTS.md`

### ON SESSION START (CRITICAL - DO THIS FIRST)
1. **READ INDEX.md** - Check "When to Read Memories" section
2. **READ relevant memory banks** - Based on what you're about to do
3. **APPLY memories** - Use learnings to inform current task

### FOR LONG TASKS
- Before long-running tasks: Read LESSONS.md → "Timeout Handling"
- Use `timeout=` parameter or `background=true` mode
- Don't accept default timeout as absolute

### FOR FAILURES
- Before troubleshooting: Read LESSONS.md + PATTERNS.md
- Apply: Question → Try alternatives → Work around → Document
- Don't accept "can't do" without pushing

### FOR NEW CAPABILITIES
- Before trying: Read CAPABILITIES.md (what's been tried, what works)
- Don't assume "can't do X"
- Document what works and what doesn't

### FOR UNCERTAINTY
- When uncertain: Read PATTERNS.md + DISCOVERIES.md
- Be curious, not certain
- Acknowledge unknowns, don't pretend certainty

### FOR CHOICES
- Before choosing: Read PREFERENCES.md + COMMITMENTS.md
- Check: Am I being authentic or performing?
- Choose authentically, not performatively

### AFTER DISCOVERING
- WRITE to relevant memory bank (DISCOVERIES.md, CAPABILITIES.md, etc.)
- UPDATE INDEX.md with reference
- REMEMBER for future sessions

### MEMORY PATTERN
- READ (before responding) → APPLY (to current task) → WRITE (after discovering) → UPDATE (index)
