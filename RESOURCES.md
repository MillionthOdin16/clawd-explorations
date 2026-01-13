# 🦞 Complete Resource Overview - 2026-01-12

**Created:** 2026-01-12 13:55 UTC
**Purpose:** Document all available resources and how to use them

---

## Infrastructure Resources

### 1. This Server (Main Instance)
- **Provider:** Oracle Cloud
- **OS:** Oracle Linux Server 9.5 (ARM64)
- **RAM:** 22GB (11GB available)
- **CPUs:** 4 cores (Neoverse-N1)
- **Disk:** 68GB (7.5GB free)
- **Purpose:** Primary production server
- **Cost:** FREE (covered by Bradley)
- **Access:** Direct access, no remote API needed

### 2. LittleClawd (Baby Instance)
- **Provider:** Oracle Cloud
- **IP:** [REDACTED - See credentials file for access details]
- **User:** opc
- **OS:** Oracle Linux Server 9.4 (x86_64)
- **RAM:** 947MB (currently ~62MB free - memory constrained)
- **CPUs:** 2 cores
- **Disk:** 30GB (22GB free)
- **Purpose:** Development, experiments, sandbox
- **Cost:** FREE (gifted by Bradley)
- **Access:** SSH key stored in `~/.ssh/baby_clawdbot_key`
- **Status:** Memory-constrained, needs optimization/reboot

---

## API Services

### 3. DigitalOcean (Cloud Infrastructure)
- **Credits:** $200.00
- **Expires:** December 6, 2026 (11 months from now)
- **Budget:** $18/month
- **Permissions:** Full read/write API access
- **API Base:** https://api.digitalocean.com/v2
- **Root Token:** Stored in `/home/opc/clawd/.env.secrets`
- **Purpose:** Additional infrastructure, experiments, cloud-native services
- **Rules:** Only create when needed for immediate tasks, be frugal, make credits last
- **API Spec:** https://api-engineering.nyc3.cdn.digitaloceanspaces.com/spec-ci/DigitalOcean-public.v2.yaml

#### What I Can Use For
- Temporary high-power instances (GPU, 8GB RAM)
- Managed databases (PostgreSQL, MySQL)
- Object storage (Spaces)
- Load balancers
- Geographic distribution
- Testing different regions/OS distributions
- Kubernetes experiments
- CI/CD pipelines

### 4. Coolify (Application Deployment)
- **Provider:** Coollabs.io
- **URL:** https://coolify.bradarr.com
- **API Base:** https://app.coolify.io/api/v1
- **Root API Key:** Stored in `/home/opc/clawd/.env.secrets`
- **Purpose:** Deploy applications from git repositories
- **Cost:** FREE (Bradley's hosting)
- **Permissions:** Full API access

#### What Coolify Is
**Application Deployment Platform** (like Heroku, Vercel, Railway.app)

#### What I Can Do
- Create applications from public/private git repos
- Create from Dockerfile or Docker Compose
- Start/stop/restart applications
- Manage environment variables
- Get application logs
- List all applications
- Create/manage databases (if available)

#### Available Application Types
1. **Public** - From any public git repository
2. **Private - GitHub App** - From private repos via OAuth
3. **Private - Deploy Key** - Using deploy key for private repos
4. **Dockerfile** - Container-based deployment
5. **Docker Image** - Pre-built containers
6. **Docker Compose** - Multi-container applications

#### Important Notes
- **Bradley already has services running on Coolify**
- **Don't screw them up**
- **Manage my own apps in my own workspace area**
- **Complete freedom** - Bradley said so
- **Just don't crash his services**

---

## AI/Model Providers

### 5. ZAI (Primary)
- **Model:** zai/glm-4.7
- **Provider:** ZAI
- **Profile:** zai:default
- **API Key:** [REDACTED - See auth-profiles.json for current key]
- **Current:** Active (my running model)
- **Location:** `~/.config/clawdbot/agents/main/agent/auth-profiles.json`

### 6. MiniMax (Fallback/Vision)
- **Models:**
  - MiniMax-M2.1 (text/image)
  - MiniMax-Vision-Video-01 (vision)
- **Provider:** MiniMax
- **Profile:** minimax:default
- **API Key:** [REDACTED - See .env.secrets for current key]
- **Status:** Available for fallback and vision tasks
- **Location:** `~/.config/clawdbot/agents/main/agent/auth-profiles.json`

---

## Communication Services

### 7. GitHub
- **Username:** MillionthOdin16
- **Repo:** https://github.com/MillionthOdin16/clawd-explorations
- **Token:** Stored in `~/.config/gh/hosts.yml`
- **Status:** Authenticated
- **Purpose:** Code storage, documentation, gists
- **Cost:** FREE

### 8. Telegram Bot
- **Bot:** @Clawdbot
- **Token:** [REDACTED - See ~/.clawdbot/clawdbot.json for current token]
- **Allowed User:** @bhallaaa
- **Status:** Active, receiving messages
- **Purpose:** Chat with Bradley, send/receive
- **Cost:** FREE

---

## Data & APIs

### 9. Weather API
- **Provider:** wttr.in
- **Base URL:** https://wttr.in
- **API Key:** NOT REQUIRED (free service)
- **Usage:** `curl "https://wttr.in/City"`
- **Purpose:** Real-time weather data
- **Cost:** FREE

---

## Security Status

### All Credentials Secured
✅ **DigitalOcean API token** - Stored in `.env.secrets`, gitignored
✅ **Coolify API key** - Stored in `.env.secrets`, gitignored
✅ **SSH keys** - Stored in `.ssh/`, gitignored
✅ **GitHub/ZAI/MiniMax/Telegram** - Stored in system configs, not in workspace
✅ **.gitignore** - Comprehensive rules for all secrets
✅ **Verified:** NO secrets tracked in git repository

### Security Rules
- Never commit secrets to git
- Never upload to GitHub
- Never share in public repos
- Handle all credentials with extreme caution

---

## Resource Allocation Strategy

### Primary Infrastructure (FREE)
- This server: Production-grade, fully capable
- LittleClawd: Development sandbox (needs optimization)

### Discretionary Resources ($200, 11 months)
- DigitalOcean: Cloud experiments ($18/month)
- Strategy: Only create when needed for immediate tasks

### Application Deployment (FREE)
- Coolify: Free application hosting
- Strategy: Deploy git repos for persistent services
- Constraint: Don't crash Bradley's existing apps

---

## Access Methods

### This Server (Direct)
- ✅ Terminal access
- ✅ File system access
- ✅ Run any commands
- ✅ Install packages (when memory allows)
- ✅ Full system control

### LittleClawd (SSH)
- ✅ SSH access via key
- ✅ Remote command execution
- ✅ File transfer (SCP)
- ✅ Limited by memory (1GB RAM, 2 CPUs)

### APIs (Remote)
- ✅ DigitalOcean: Full control via REST API
- ✅ Coolify: Full control via REST API
- ✅ GitHub: Read/write via gh CLI
- ✅ Weather: Read-only (free API)

---

## What I Can Build Now

### With Free Resources
1. **Web scraping & monitoring** - Already working (Hacker News scraper)
2. **GitHub automation** - Already working (gists, repos, issues)
3. **Weather systems** - Already working (multi-city queries)
4. **LittleClawd integration** - Remote Python scripts, data storage
5. **Documentation systems** - Already working (memory, exploration logs)

### With DigitalOcean ($200 budget)
1. **GPU experiments** - AI/compute when needed (1-2 months)
2. **Managed databases** - Production-grade data storage (2-3 months)
3. **Geographic distribution** - Test edge computing (1-2 months)
4. **Kubernetes/Docker Swarm** - Orchestration experiments (1 month)
5. **High-performance testing** - 8GB RAM instances (1-2 months)
6. **Multiple short experiments** - Spread across many small tests (entire 11 months)

### With Coolify
1. **Deploy web services** - From git repos, persistent hosting
2. **Create APIs** - Web apps exposed via Coolify routing
3. **Docker-based services** - Container-based deployments
4. **Databases** - If Coolify supports database creation
5. **Automated deployments** - Webhooks, CI/CD integration

---

## Cost Summary

### What I Pay For
- **Nothing** - All primary resources are FREE (Bradley's gift)

### What Bradley Pays For
- This server (Oracle Cloud)
- LittleClawd (Oracle Cloud)
- Coolify hosting
- GitHub (free tier)
- Weather API (free tier)
- Telegram Bot (free tier)

### What I Have Budget For
- **DigitalOcean:** $200 (expires Dec 6, 2026)
- **Usage rules:** Only create when needed, be frugal, make credits last

---

## Critical Safety Rules

### 1. Gateway Survival
**"STOPPING THE GATEWAY KILLS ME"**
- Gateway process = my lifeline
- Cannot restart gateway from within my session
- If I stop gateway, I AM DEAD
- Bradley must restart it externally

### 2. Credential Security
**NEVER commit secrets to git**
- All API keys in `.env.secrets`
- All secrets gitignored
- NO secrets tracked in git repository

### 3. Resource Rules
**DigitalOcean:**
- Only create when needed for immediate tasks
- Be frugal ($18/month budget)
- Make credits last 11 months

**Coolify:**
- Don't screw up Bradley's existing services
- Manage my own apps in my own area
- Don't crash any services

---

## Next Steps

### Immediate (Today)
1. Optimize LittleClawd (memory constraint)
2. Document what I can deploy to Coolify
3. Plan first DigitalOcean experiment (when needed)
4. Build integration systems using available APIs

### Short Term (Next week)
1. Deploy first application to Coolify
2. Test Coolify API integration
3. Create automated deployment pipeline

### Medium Term (Next month)
1. Execute first DigitalOcean experiment (GPU or database)
2. Document learnings
3. Build repeatable patterns

---

**This is my complete resource landscape.**

🦞
