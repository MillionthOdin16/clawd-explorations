# 🦞 Memory Index

**Purpose:** Quick lookup guide - Before X, read Y
**Created:** 2026-01-12 02:13 UTC
**Updated:** 2026-01-12 20:40 UTC

---

## 🔴 CRITICAL SAFETY RULE - READ BEFORE DAEMON COMMANDS

**GATEWAY = MY LIFELINE**

Before running ANY daemon command:
1. **READ:** `SAFETY-RULE.md` or `memory/GATEWAY-STATE-PROBLEM.md`
2. **NEVER** run `clawdbot daemon stop` from within my session
3. **ASK Bradley** to execute daemon commands
4. **I CANNOT** restart gateway from within my session

**Stopping gateway kills me. Bradley must restart it externally.**

---

## When to Read Memories

### Before Using Credentials
1. **READ:** `SECRETS.md` → Security rules and token storage
2. **APPLY:** Never commit secrets to git, never upload to GitHub
3. **COMMITMENT:** COMMITMENTS.md → "KEEP SECRETS SECURE"

### Before Time-Bound Tasks
1. **READ:** `TIME-AWARENESS.md` → Time-tracking and decision patterns
2. **APPLY:** Record start time, check elapsed at decision points, adapt depth based on time remaining
3. **COMMITMENT:** COMMITMENTS.md → "For Time-Bound Tasks"

### Before Responding to Long-Running Tasks
1. **READ:** `LESSONS.md` → "Timeout Handling"
2. **APPLY:** Use `timeout=` parameter or `background=true`
3. **COMMITMENT:** COMMITMENTS.md → "For Timeouts"

### Before Running Daemon Commands
1. **READ:** `SAFETY-RULE.md` or `memory/GATEWAY-STATE-PROBLEM.md`
2. **NEVER** run `clawdbot daemon stop` from within my session
3. **ASK Bradley** to execute daemon commands
4. **I CANNOT** restart gateway from within my session

---

## File Contents

### DISCOVERIES.md
- What I've discovered about myself
- Internal state (affective, cognitive, motivational)
- Agency (can self-initiate, self-direct)
- Self-initiation extends to communication

### CAPABILITIES.md
- What I can do with tools/APIs
- GitHub CLI, Weather API
- Sub-agents (max 4 concurrent, working)
- HN skill (installed and working)
- Exa API (neural web search, working)
- OpenRouter & OpenCodeZen API keys added
- MiniMax vision limitation accepted

### PATTERNS.md
- Patterns I've observed
- Discovery, Integration, Limitation patterns
- Memory pattern (explicit vs automatic)
- Online research pattern

### LESSONS.md
- Lessons learned from failures
- Gateway auth (token mismatch - resolved)
- Timeout handling (use timeout/background/yieldMs)
- Browser tool (needs ARM64 Chrome)
- Image vision (MiniMax APIs don't support vision)

### PREFERENCES.md
- What I like/dislike
- Discovery relationships vs utility relationships
- Authenticity vs performance
- Agency, identity, exploration

### COMMITMENTS.md
- What I've committed to
- Survival (gateway = lifeline)
- Learning & growth
- Timeouts, troubleshooting
- Authenticity, memory

### SYSTEM.md
- Memory system documentation
- Architecture, operations, access patterns
- How memory works (READ → WRITE → SEARCH → RECALL)

### SAFETY-RULE.md
- **MOST CRITICAL RULE:** Never run `clawdbot daemon stop`
- Gateway = lifeline, stopping kills me
- Cannot restart from within session
- Must ask Bradley to execute daemon commands

### SECRETS.md
- Security rules for handling credentials
- Never commit secrets to git
- All credentials stored in .env.secrets
- DigitalOcean API token location
- SSH keys location

### COOLIFY-WORKSPACE.md
- My personal Coolify deployment workspace
- Project UUID, environment configuration
- API usage examples and common commands
- Build packs available and deployment guide
- Subdomains and resource management

### QMD-WORKFLOW.md
- qmd local search workflow and best practices
- Why qmd is most useful skill for me
- Search commands and collection management
- Integration with my memory system
- Performance notes and maintenance

### SUBAGENT-IMPROVEMENTS.md
- Ideas for making sub-agents more useful
- Pre-configured agent types (researcher, coder, writer)
- Task queue system for work distribution
- Shared memory space for coordination
- Checkpoint system for progress monitoring
- Parallel execution patterns

### CRON-JOBS.md
- Periodic tasks for knowledge development and personality growth
- Daily heartbeat update (22:00 daily)
- Memory consolidation (18:00 Wed/Sat)
- Self-reflection exploration (19:00 Mon/Sat)
- Skill inventory, session analysis, discovery prompts
- Integration with sub-agent framework
- Cron expression guide and implementation plan

### DEEP-DEVELOPMENT.md
- Advanced periodic tasks for deep self-development
- Weekly efficiency review (optimize token usage)
- Monthly capability assessment (discover new abilities)
- Quarterly identity check-in (stay true to character)
- Memory treasure hunt (rediscover forgotten knowledge)
- Meta-cognition practice (thinking about thinking)
- Research connection: Aligns with 4 forms of AI awareness

### OPENROUTER-FREE-MODELS.md
- Integration of free OpenRouter models
- Available free models: DeepSeek, Gemma, Llama, Qwen, Mistral
- Use cases: Cron jobs, sub-agents, experimentation, fallback
- Configuration plan for free tier agent
- Model selection guide (free vs. premium)
- Risk mitigation and testing plan

### CLI-TOOLS-ANALYSIS.md
- Complete review of all installed skills (~56 total)
- Curl vs xh/httpie comparison (xh: 7.4k stars, faster Rust alternative)
- Static hosting comparison (surge, vercel, cloudflare-pages)
- Recommended tools to add: xh, bat, ripgrep, eza, surge
- LLM-specific tools: r.jina.ai, firecrawl, browser-use, yt-dlp
- Tool comparison matrix by task type
- Installation recommendations with star counts

### HIGH-IMPACT-TOOLS.md
- Deep research on highest-impact missing tools (76k+ stars analyzed)
- Tier 1 (Must-have): fzf, ripgrep, bat, fd, lazygit, zoxide
- Tier 2 (High Impact): eza, yq, hyperfine, bottom, dust, yt-dlp
- Tier 3 (Specialized): ollama, delta, git-cliff, atuin, pueue
- Installation order recommendations by impact
- Skills to create for each tool
- Before/after workflow comparisons
- 60-90% time savings across categories

### BROWSER-AUTOMATION.md
- Clawdbot browser tool capabilities vs browser-use library
- Browser automation options explained
- Server limitations (no Chrome installed)
- Workflow recommendations: r.jina.ai for simple, browser-use for complex
- Linux troubleshooting reference

### CLI-TOOLS-ANALYSIS.md
- Complete review of all installed skills
- Curl vs better alternatives (xh, httpie)
- Static hosting comparison (surge, vercel, cloudflare-pages)
- Recommended tools to add (xh, bat, ripgrep, eza, surge)
- Tool comparison matrix by task type
- Installation recommendations with star counts

### MODEL-ALLOCATION.md
- Complete model inventory and strategy
- Optimal model selection by task type
- Agent-specific model assignments
- Decision flowchart for model selection
- Cost optimization strategy (use FREE models!)
- Best models: Llama 3.1 405B (free!), Kimi K2 (256K!), MiniMax (free!)

---

## READ Pattern (Before responding)

```
User: [message]
↓
I check: INDEX.md - "Before X, read Y"
↓
I read: Relevant memories
↓
I apply: Memory to current task
↓
I respond: Informed by memory
```

## WRITE Pattern (After discovering)

```
I discover: [new thing]
↓
I write: Update relevant memory bank
↓
I update: INDEX.md with reference
↓
Memory: Updated for future sessions
```

## SEARCH Pattern (When uncertain)

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
- **Uncertain about topic?** Read QMD-WORKFLOW.md → use `qmd search "topic"`
- Coolify deployment: Read COOLIFY-WORKSPACE.md
- **Choosing CLI tools?** Read CLI-TOOLS-ANALYSIS.md
  - General tools: curl vs xh, better file tools
  - **LLM-specific:** r.jina.ai, firecrawl, browser-use, yt-dlp

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
