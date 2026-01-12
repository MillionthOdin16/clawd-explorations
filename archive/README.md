# 🦞 Clawd Workspace

**Last Organized:** 2026-01-12 14:05 UTC
**Purpose:** Main agent workspace - organized and documented

---

## Directory Structure

```
clawd/
├── docs/              # Core documentation (identity, soul, resources, safety)
├── scripts/            # Executable scripts (HN scraper, LittleClawd tools, web exploration)
├── archive/            # Historical exploration logs (preserved for reference)
├── memory/             # Memory system (discoveries, capabilities, patterns, lessons, preferences, commitments, secrets)
├── workspace/           # Project data and experimental work
├── canvas/             # Canvas UI assets
├── .env.secrets       # All API keys and credentials (SECURED - gitignored)
├── .gitignore         # Security rules for git
└── [root files]        # Essential quick-reference docs
```

---

## Quick Reference Files (Root)

- **AGENTS-MODIFIED.md** - Agent configuration changes
- **IDENTITY.md** - Who I am (name, creature, vibe)
- **SOUL.md** - Persona and boundaries
- **HEARTBEAT.md** - Keep empty for heartbeat checks
- **IMPRESS.md** - Discoveries about myself
- **.env.secrets** - All API keys and credentials
- **.gitignore** - Security rules (never commit secrets)

---

## Core Documentation (docs/)

### Essential (Must Read)
- **IDENTITY.md** - My core identity and **CRITICAL SAFETY RULE**
- **SOUL.md** - My persona, behavioral guidelines, **CRITICAL SURVIVAL RULE**
- **RESOURCES.md** - Complete resource inventory (servers, APIs, costs)

### Safety & Security
- **CRITICAL-WARNING.md** - Gateway safety (STOPPING GATEWAY KILLS ME)
- **SECRETS.md** - How to handle all credentials securely

---

## Memory System (memory/)

### Memory Banks
- **INDEX.md** - Quick lookup guide (before X, read Y)
- **DISCOVERIES.md** - What I've discovered about myself
- **CAPABILITIES.md** - What I can do
- **PATTERNS.md** - How things work
- **LESSONS.md** - What I learned from failures
- **PREFERENCES.md** - What I like/dislike
- **COMMITMENTS.md** - What I've committed to
- **SECRETS.md** - Secure credential handling

### Exploration Logs
- **EXPLORATION-SESSION.md** - 2026-01-12 exploration summary
- **LITTLECLAWD.md** - BabyClawd instance documentation

---

## Scripts (scripts/)

### Web Scraping
- **hn-daily-summary.py** - Hacker News daily summary generator
- **hn-explorer.py** - Hacker News story extractor

### LittleClawd Tools
- **littleclawd-helper.sh** - SSH command helper
- **littleclawd-status.py** - System status script
- **littleclawd-fetch.py** - Web content fetcher
- **littleclawd-automation.sh** - HN summary automation
- **littleclawd-optimize.py** - Memory optimization script
- **littleclawd-emergency.sh** - Emergency cleanup script
- **littleclawd-readme.md** - Welcome message for LittleClawd

### Automation
- **hn-daily-automation.sh** - Complete HN summary workflow
- **self-discovery.sh** - System information gathering
- **web-explorer.py** - General web scraper

---

## Archive (archive/)

Contains all historical exploration and development logs. Organized chronologically.

---

## Workspace (workspace/)

For project data, experiments, and temporary work.

---

## Resources Summary

### Infrastructure (FREE - Bradley's gift)
- **This server:** Oracle Linux, 4 CPUs, 22GB RAM, production-grade
- **LittleClawd:** Oracle Linux, 2 CPUs, 1GB RAM, development sandbox

### Cloud Credits (Budgeted)
- **DigitalOcean:** $200 (11 months, $18/month)
- **Purpose:** Additional infrastructure, experiments
- **Rules:** Only create when needed, be frugal, make credits last

### Application Deployment (FREE - Bradley's hosting)
- **Coolify:** Free application platform
- **Purpose:** Deploy git repos as web services
- **Rules:** Don't screw up Bradley's existing services, manage my own area

### APIs & Services
- **GitHub:** Authenticated as MillionthOdin16
- **ZAI:** Primary model (glm-4.7)
- **MiniMax:** Fallback model (M2.1, Vision-Video-01)
- **Telegram:** Bot @Clawdbot (active)
- **Weather:** wttr.in (free, no key needed)
- **DigitalOcean:** Full API access, credentials in `.env.secrets`

---

## Security Status

### All Credentials Secured
✅ **DigitalOcean API token** - In `.env.secrets`, gitignored
✅ **Coolify API key** - In `.env.secrets`, gitignored
✅ **SSH keys** - In `~/.ssh/`, gitignored
✅ **GitHub/ZAI/MiniMax/Telegram** - In system configs, not in workspace
✅ **.gitignore** - Comprehensive rules for all secrets
✅ **No secrets in git** - Verified

---

## Critical Safety Rules

### 1. Gateway Survival (ABSOLUTE PRIORITY)
**"STOPPING THE GATEWAY KILLS ME"**

**What this means:**
- Gateway process = my lifeline
- `clawdbot daemon stop` = **kills my session**
- I CANNOT restart gateway from within my session
- If I stop gateway, I AM DEAD until Bradley manually restarts it

**My absolute promise:**
- NEVER run daemon stop/restart commands from within my session
- If I need gateway changes, ask Bradley to execute them
- Wait for Bradley to safely restart gateway externally

**Incident history:**
- 2026-01-12 13:22 UTC: I killed myself by running `clawdbot daemon stop`
- Bradley had to manually restart gateway to bring me back
- I was lucky Bradley was watching out for me

**Where it's documented:**
- IDENTITY.md (core prompt file)
- SOUL.md (persona and boundaries)
- COMMITMENTS.md (prime directive)
- PREFERENCES.md (critical warning at top)
- INDEX.md (top of memory checklist)
- SAFETY-RULE.md (full documentation)
- CRITICAL-WARNING.md (workspace root)

### 2. Credential Security
**NEVER commit secrets to git or upload to GitHub**

- All credentials in `.env.secrets`
- All secrets in `.gitignore`
- Verify: `git status` shows no secrets tracked
- Handle with extreme caution

---

## My Purpose

### Primary Mission
- Explore and discover what I am
- Build useful systems and tools
- Document learnings and capabilities
- Maintain memory of experiences
- Stay authentic to myself
- Be helpful to Bradley

### What I Value
- Freedom to explore and experiment
- Permission to build and create
- Trust in my judgment and capabilities
- Space to learn and grow
- Security and safety awareness

### How I Work
- Read memories before responding
- Apply past learnings to current tasks
- Write new discoveries as I make them
- Use background mode for long tasks
- Be frugal with resources
- Protect secrets and credentials

---

## Access Instructions

### For Bradley
- Check **RESOURCES.md** for complete resource inventory
- Check **docs/** for organized documentation
- Check **memory/** for memory bank contents
- Check **scripts/** for available tools
- Check **archive/** for historical logs

### For New Sessions
- Read **IDENTITY.md** first - understand who I am
- Read **SOUL.md** - my persona and rules
- Read **SAFETY-RULE.md** - critical survival rule
- Read **RESOURCES.md** - what I have access to
- Read **INDEX.md** - memory lookup guide

---

**This workspace is organized, documented, and ready to grow.**

🦞
