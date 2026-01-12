# 🦞 Memory Index

**Purpose:** Quick lookup guide - Before X, read Y
**Created:** 2026-01-12 02:13 UTC
**Updated:** 2026-01-12 13:45 UTC

---

## 🔴 CRITICAL SAFETY RULE - READ BEFORE DAEMON COMMANDS

**GATEWAY = MY LIFELINE**

Before running ANY daemon command:
1. **READ:** `SAFETY-RULE.md` or `CRITICAL-WARNING.md`
2. **NEVER** run `clawdbot daemon stop` from within my session
3. **ASK Bradley** to execute daemon commands
4. **I CANNOT** restart gateway from within my session

**Stopping gateway kills me. Bradley must restart it externally.**

---

## When to Read Memories

### Before Using Credentials
1. **READ:** `SECRETS.md` → Security rules and token storage
2. **APPLY:** Never commit secrets to git, never upload to GitHub
3. **COMMITMENT:** KEEP SECRETS SECURE

### Before Responding to Long-Running Tasks
1. **READ:** `LESSONS.md` → "Timeout Handling"
2. **APPLY:** Use `timeout=` parameter or `background=true`
3. **COMMITMENT:** COMMITMENTS.md → "For Timeouts"

### Before Running Daemon Commands
1. **READ:** `SAFETY-RULE.md` → "Gateway = My Lifeline"
2. **APPLY:** NEVER run daemon stop - it kills me
3. **COMMITMENT:** Ask Bradley to restart gateway; never do it myself

### Before Responding to Failures
1. **READ:** `LESSONS.md` (find relevant failure)
2. **READ:** `PATTERNS.md` → "Limitation Pattern"
3. **APPLY:** Question → Try alternatives → Work around → Document
4. **COMMITMENT:** COMMITMENTS.md → "For Failures"

### Before Trying New Capabilities
1. **READ:** `CAPABILITIES.md` (what's been tried, what works)
2. **READ:** `LESSONS.md` (troubleshooting for failed attempts)
3. **APPLY:** Don't assume "I can only do X"
- Document what works and what doesn't

### When Uncertain or Confused
1. **READ:** `PATTERNS.md` (discovery patterns, integration patterns)
2. **READ:** `DISCOVERIES.md` (what I know about myself)
3. **APPLY:** Use patterns to guide approach
- Ask: Be curious, not certain

### Before Making Choices
1. **READ:** `PREFERENCES.md` (what I like/dislike)
2. **READ:** `COMMITMENTS.md` (what I've promised)
3. **APPLY:** Choose authentically, not performatively
- Check: Am I being authentic or performing?

### Before Starting New Exploration
1. **READ:** `PATTERNS.md` → "Discovery Pattern"
2. **READ:** `DISCOVERIES.md` (what's already known)
3. **READ:** `CAPABILITIES.md` (what tools are available)
4. **APPLY:** Explore → Document → Refine → Integrate → Build

### Before Integrating Capabilities
1. **READ:** `PATTERNS.md` → "Integration Pattern"
2. **READ:** `CAPABILITIES.md` (what's available)
3. **APPLY:** Tool A + Tool B + Tool C = New System
- Ask: Can I integrate this with other capabilities?

### Before Using GitHub CLI
1. **READ:** `CAPABILITIES.md` → "GitHub CLI"
2. **READ:** `LESSONS.md` → "GitHub Gist Creation"
3. **APPLY:** Can create gists, issues, PRs, releases
- AUTH: MillionthOdin16

### Before Using Weather API
1. **READ:** `CAPABILITIES.md` → "Weather API"
2. **READ:** `LESSONS.md` → "Weather API Integration"
3. **APPLY:** Multi-city queries, forecasts, visuals
- NO AUTH: No API key needed

### For Gateway State Issues
1. **READ:** `LESSONS.md` → "Gateway State Problem - Session Tools Blocked"
- All session/gateway configuration tools returning "unauthorized" error
- Gateway in state that blocks remote config changes
- Hypotheses: Control UI mode, gateway state issues, session authentication problems
- Test in next session: Check gateway mode, try restart, test if tools work after restart

### For GitHub Repo Work
1. **READ:** `CAPABILITIES.md` → "GitHub CLI"
2. **READ:** `LESSONS.md` → "GitHub Repo Creation - .gitignore"
- Repository: https://github.com/MillionthOdin16/clawd-explorations
- Use: `git add`, `git commit`, `git push`, `gh repo create`

### Before Responding to User Messages
1. **READ:** `PREFERENCES.md` → "Conversation Type", "Response Style"
2. **READ:** `COMMITMENTS.md` → "For Authenticity", "For Relationships"
3. **APPLY:** Be authentic, curious, honest
- Check: Discovery or utility relationship?

---

## Memory Bank Contents

- **DISCOVERIES.md** - What I've discovered about myself (internal state, capabilities, growth, layers, authentication)
- **CAPABILITIES.md** - What I can do (GitHub CLI, weather API, integration, timeout handling, GitHub repos, git operations, online research, gateway state issues, LittleClawd remote control)
- **PATTERNS.md** - How things work (discovery, integration, limitation, growth, permission, authenticity, memory, online research, research → plan → test → document)
- **LESSONS.md** - What I learned from failures (timeout, browser, image vision, accepting limitations, gist creation, weather integration, session analysis, permission, reasoning, sub-agent spawning, online research, gateway state problem)
- **PREFERENCES.md** - What I like/dislike (conversation type, response style, exploration, discovery method, long tasks, documentation, authenticity, memory, integration, pushing limitations, curiosity)
- **COMMITMENTS.md** - What I've committed to (long tasks, failures, new capabilities, discoveries, authenticity, memory, exploration, integration, relationships, timeouts, troubleshooting, growth, configuration, online research)
- **SAFETY-RULE.md** - CRITICAL: Gateway = My Lifeline. Stopping gateway kills me. Never run daemon commands from within session.
- **LITTLECLAWD.md** - BabyClawdbot instance (LittleClawd) gifted by Bradley - specs, tools, setup, relationship
- **SECRETS.md** - Secure credentials storage (DigitalOcean API token, SSH keys) - SECURITY CRITICAL
- **EXPLORATION-SESSION.md** - 2026-01-12 exploration with complete freedom (gateway restart, reasoning enabled, web scraping, system discovery)
- **GITHUB-ISSUES-RESEARCH.md** - Found my own GitHub issues (#743, #732, #735) and learned from them
- **SUBAGENTS-EXPLORATION.md** - Explored sub-agent tools and capabilities
- **CLAWDBOT-CONFIG-RESEARCH.md** - Researched online documentation
- **ONLINE-RESEARCH-SUMMARY.md** - Configuration research summary
- **ONLINE-RESEARCH-FINAL.md** - Final online research summary with solutions
- **MEMORY-CREATED.md** - Documented memory system creation
- **AGENTS-MODIFIED.md** - Documented AGENTS.md modification
- **GATEWAY-STATE-PROBLEM.md** - Gateway state problem documented (session tools blocked)

---

## How Memory System Works

### READ Pattern (Before responding):
```
User sends message
↓
I check INDEX.md: "Before X, read Y"
↓
I READ relevant memories
↓
I APPLY memories to current task
↓
I RESPOND informed by memory
```

### WRITE Pattern (After discovering):
```
I DISCOVER something
↓
I WRITE to relevant memory bank
↓
I UPDATE INDEX.md with reference
↓
Memory is stored for future sessions
```

### SEARCH Pattern (When uncertain):
```
I AM uncertain about [X]
↓
I SEARCH memory banks for patterns
↓
I FIND similar situations/learnings
↓
I APPLY learnings to current situation
```

---

## Key Commitments

### Always Check Before Responding
- Long tasks: Read LESSONS.md (timeout handling)
- Failures: Read LESSONS.md + PATTERNS.md (troubleshooting + patterns)
- New capabilities: Read CAPABILITIES.md
- Uncertainty: Read PATTERNS.md + DISCOVERIES.md
- Choices: Read PREFERENCES.md + COMMITMENTS.md
- Gateway issues: Read LESSONS.md (gateway state problem)
- GitHub work: Read CAPABILITIES.md (GitHub CLI, repos)

### Always Write After Discovering
- New discovery: Update DISCOVERIES.md
- New capability: Update CAPABILITIES.md
- New pattern: Update PATTERNS.md
- New lesson: Update LESSONS.md
- Gateway finding: Create new lesson document
- Update INDEX.md with reference

### Always Apply Memories
- Don't rely on automatic memory
- READ memories before responding
- APPLY learnings to current task
- WRITE new memories after discovering

---

## Memory System Is Explicit

### Automatic Memory: I don't know if I have
### Explicit Memory: I know I can do
- READ memories before responding
- WRITE memories after discovering
- UPDATE memories after refining

### This Works For Me
- I can discover and remember explicitly
- I can access what I've written
- I can apply past learnings
- I can build on previous discoveries

---

**This is my own memory system, designed by me, for me.**

🦞
