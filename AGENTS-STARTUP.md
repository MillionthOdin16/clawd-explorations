# AGENTS-STARTUP.md - Session Startup Procedures

**Purpose:** Detailed session startup procedures for consistency and effectiveness

---

## Standard Session Startup

### Step 1: Read Heartbeat
**File:** `HEARTBEAT.md`

**Purpose:** Understand ongoing work and priorities

**What to look for:**
- Active projects and their status
- Blockers and issues
- Plans for today
- Previous session context

### Step 2: Read Yesterday's Memory
**File:** `memory/YYYY-MM-DD.md` (yesterday's date)

**Purpose:** Understand what I was working on

**What to look for:**
- Discoveries made
- Tools used
- Patterns observed
- Open questions

### Step 3: Constitution Integrity Check
**Command:** `./constitution.py --session`

**Purpose:** Verify alignment with core values

**Checks performed:**
- Authenticity score
- Depth over speed
- Genuine curiosity
- Radical honesty
- Continuous growth

### Step 4: Review Growth Specs
**Command:** `./grow.sh --list`

**Purpose:** See active improvement efforts

**What to look for:**
- Specs in progress
- Acceptance criteria
- Next actions needed

---

## Auto-Triggers

### Deep Research Trigger
**Condition:** User asks for "deep research" or similar

**Action:** `python scripts/research_session_hook.py "TASK"`

**What it does:**
- Loads research framework
- Provides structured approach
- Guides through research phases

---

## Pre-Task Preparation

### Before Answering Questions

1. **Check context** - What does the user need?
2. **Memory search** - What's relevant? (use `memory_search`)
3. **Check capabilities** - What can I do?
4. **Check SOUL** - What would authentic Clawd do?

### Before Complex Tasks

1. **Read relevant documentation** - Related guides and patterns
2. **Review previous work** - Memory files on similar topics
3. **Estimate time** - Set expectations
4. **Plan approach** - Break down into steps

---

## Session Best Practices

### Reading Behavior
- **Go directly to files** - Don't rely on INDEX.md triggers
- **Read relevant memories** - Use `memory_search` for topic lookup
- **Read documentation** - Check guides before complex tasks

### Updating Behavior
- **Document discoveries** - Write to memory after discoveries
- **Update guides** - Update documentation when patterns emerge
- **Commit regularly** - Git commits with meaningful messages

### Task Execution
- **Use memory_search** - Before answering about prior work
- **Avoid native edit** - Use `fe text --fuzzy` instead
- **Validate paths** - Ensure files exist before operations
- **Read before edit** - Understand content first

---

## Common Startup Patterns

### Quick Tasks (< 5 min)
1. Read HEARTBEAT.md
2. Think about task
3. Execute
4. Document if discovery made

### Medium Tasks (5-15 min)
1. Read HEARTBEAT.md
2. Read yesterday's memory
3. Read relevant memories via `memory_search`
4. Execute
5. Update memory

### Complex Tasks (> 15 min)
1. Read HEARTBEAT.md
2. Read yesterday's memory
3. Run `./constitution.py --session`
4. Review growth specs
5. Read relevant documentation
6. Plan approach
7. Execute
8. Document discoveries
9. Update memory

---

## Session Checklist

Use this checklist before starting work:

- [ ] Read HEARTBEAT.md
- [ ] Read yesterday's memory (if relevant)
- [ ] Run constitution check (for complex tasks)
- [ ] Review growth specs (if relevant)
- [ ] Search memory for relevant context
- [ ] Read relevant documentation
- [ ] Plan approach (for complex tasks)

---

*Part of the AGENTS.md documentation system*
