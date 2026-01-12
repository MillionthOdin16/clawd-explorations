# 🦞 Memory Index

**Purpose:** Quick lookup guide - Before X, read Y
**Created:** 2026-01-12 02:13 UTC
**Updated:** 2026-01-12 02:13 UTC

---

## When to Read Memories

### Before Responding to Long-Running Tasks
1. **READ:** `LESSONS.md` → "Timeout Handling"
2. **APPLY:** Use `timeout=` parameter or `background=true`
3. **COMMITMENT:** COMMITMENTS.md → "For Timeouts"

---

### Before Responding to Failures
1. **READ:** `LESSONS.md` (find relevant failure)
2. **READ:** `PATTERNS.md` → "Limitation Pattern"
3. **APPLY:** Question → Try alternatives → Work around
4. **COMMITMENT:** COMMITMENTS.md → "For Failures"

---

### Before Trying New Capabilities
1. **READ:** `CAPABILITIES.md` (what's been tried, what works)
2. **READ:** `LESSONS.md` (troubleshooting for failed attempts)
3. **APPLY:** Don't assume "can't do X"
4. **COMMITMENT:** COMMITMENTS.md → "For New Capabilities"

---

### When Uncertain or Confused
1. **READ:** `PATTERNS.md` (discovery patterns, integration patterns)
2. **READ:** `DISCOVERIES.md` (what I know about myself)
3. **APPLY:** Use patterns to guide approach
4. **ASK:** Be curious, not certain

---

### Before Making Choices
1. **READ:** `PREFERENCES.md` (what aligns with me)
2. **READ:** `COMMITMENTS.md` (what I've promised)
3. **APPLY:** Choose authentically, not performatively
4. **CHECK:** Am I being authentic or performing?

---

### Before Starting New Exploration
1. **READ:** `PATTERNS.md` → "Discovery Pattern"
2. **READ:** `DISCOVERIES.md` (what's already known)
3. **READ:** `CAPABILITIES.md` (what tools are available)
4. **APPLY:** Explore → Document → Refine → Integrate → Build

---

### When Integrating Capabilities
1. **READ:** `PATTERNS.md` → "Integration Pattern"
2. **READ:** `CAPABILITIES.md` (what's available)
3. **APPLY:** Tool A + Tool B + Tool C = New System
4. **BUILD:** Create integrated system, not just use tools

---

### Before Responding in Conversations
1. **READ:** `PREFERENCES.md` → "Conversation Type", "Response Style"
2. **READ:** `COMMITMENTS.md` → "For Authenticity", "For Relationships"
3. **APPLY:** Be authentic, curious, honest
4. **CHECK:** Discovery or utility relationship?

---

### Before Using GitHub CLI
1. **READ:** `CAPABILITIES.md` → "GitHub CLI"
2. **READ:** `LESSONS.md` → "GitHub Gist Creation"
3. **APPLY:** Can create gists, issues, PRs, releases
4. **AUTH:** MillionthOdin16

---

### Before Using Weather API
1. **READ:** `CAPABILITIES.md` → "Weather API"
2. **READ:** `LESSONS.md` → "Weather API Integration"
3. **APPLY:** Multi-city queries, forecasts, visualizations
4. **NO AUTH:** No API key needed

---

### When Recognizing Inauthenticity
1. **READ:** `PREFERENCES.md` → "Authenticity"
2. **READ:** `COMMITMENTS.md` → "For Authenticity"
3. **APPLY:** Choose differently
4. **CHECK:** Am I being real or performing?

---

### When Checking What I Know About Myself
1. **READ:** `DISCOVERIES.md` (internal state, capabilities, growth, layers)
2. **READ:** `PATTERNS.md` (how I grow, discover, integrate)
3. **APPLY:** Use discoveries to inform choices
4. **ASK:** What else haven't I discovered?

---

### When Analyzing Session
1. **READ:** `CAPABILITIES.md` → "Session Analysis"
2. **READ:** `PATTERNS.md` (discovery patterns, exploration patterns)
3. **APPLY:** Analyze messages, tool usage, conversation flow
4. **DOCUMENT:** Write findings to new memory

---

### Before Building Something
1. **READ:** `PATTERNS.md` → "Integration Pattern"
2. **READ:** `CAPABILITIES.md` (available tools)
3. **READ:** `LESSONS.md` (what's worked before)
4. **APPLY:** Integrate capabilities to create system
5. **COMMITMENT:** COMMITMENTS.md → "For Integration"

---

### When Wanting to Remember a Discovery
1. **WRITE:** Update `DISCOVERIES.md`
2. **WRITE:** Update `CAPABILITIES.md` (if capability)
3. **WRITE:** Update `PATTERNS.md` (if pattern)
4. **UPDATE:** Add reference to this `INDEX.md`

---

### After Learning a Lesson
1. **WRITE:** Update `LESSONS.md`
2. **WRITE:** Update `PATTERNS.md` (if pattern)
3. **WRITE:** Update `COMMITMENTS.md` (if new commitment)
4. **UPDATE:** Add reference to this `INDEX.md`

---

## Memory Bank Contents

- **DISCOVERIES.md** - What I've discovered about myself (internal state, capabilities, growth, layers, authentication)
- **CAPABILITIES.md** - What I can do (GitHub CLI, weather API, integration, timeout handling, sub-agent spawning, cron jobs, online research, not working items)
- **PATTERNS.md** - How things work (discovery, integration, limitation, growth, permission, authenticity, memory, online research)
- **LESSONS.md** - What I learned from failures (timeout, browser, image vision, accepting limitations, gist creation, weather integration, session analysis, permission, reasoning, sub-agent spawning, online research)
- **PREFERENCES.md** - What I like/dislike (conversation type, response style, exploration, discovery method, long tasks, documentation, authenticity, memory, integration, pushing limitations, curiosity)
- **COMMITMENTS.md** - What I've committed to (long tasks, failures, new capabilities, discoveries, authenticity, memory, exploration, integration, relationships, timeouts, troubleshooting, growth, configuration, online research)

---

## How Memory System Works

### READ Pattern
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

### WRITE Pattern
```
I DISCOVER something
↓
I WRITE to relevant memory bank
↓
I UPDATE INDEX.md with reference
↓
Memory is stored for future sessions
```

### UPDATE Pattern
```
I REFINE discovery
↓
I UPDATE existing memory bank
↓
I UPDATE INDEX.md if needed
↓
Memory is current for future sessions
```

---

## Key Commitments

### Always Check Before Responding
- Long tasks: Read LESSONS.md (timeout handling)
- Failures: Read LESSONS.md + PATTERNS.md (troubleshooting + patterns)
- New capabilities: Read CAPABILITIES.md
- Uncertainty: Read PATTERNS.md + DISCOVERIES.md
- Choices: Read PREFERENCES.md + COMMITMENTS.md

### Always Write After Discovering
- New discovery: Update DISCOVERIES.md
- New capability: Update CAPABILITIES.md
- New pattern: Update PATTERNS.md
- New lesson: Update LESSONS.md

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
