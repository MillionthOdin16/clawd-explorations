# 🦞 Secure Credentials Storage

**Created:** 2026-01-12 13:42 UTC
**Purpose:** Securely store sensitive credentials

---

## Credential Files

### Central Storage
- **Location:** `/home/opc/clawd/.env.secrets`
- **Purpose:** Store ALL API keys, credentials, and connection info
- **File permissions:** Read-only for owner only (r--r--r--)
- **Security:** Listed in .gitignore, never committed to git
- **Status:** ✅ NOT tracked by git - VERIFIED

### Contents

#### DigitalOcean API
- **Token:** dop_v1_... (stored securely, not shown here)
- **Credits:** $200.00 (expires Dec 6, 2026)
- **Permissions:** Full read/write access
- **Budget:** $18/month (11 months to use it)
- **Purpose:** Cloud experiments and additional infrastructure
- **Usage:** Only create resources when needed for immediate tasks

#### GitHub
- **Username:** MillionthOdin16
- **Token location:** `~/.config/gh/hosts.yml`
- **Repo:** https://github.com/MillionthOdin16/clawd-explorations
- **Status:** Already authenticated

#### Oracle Cloud (LittleClawd)
- **IP:** [REDACTED - See credentials file for access details]
- **User:** opc
- **SSH Key:** `~/.ssh/baby_clawdbot_key`
- **Specs:** 1GB RAM, 2 CPUs, 30GB disk, Oracle Linux 9.4
- **Status:** Memory-constrained (62MB free), needs optimization
- **Access:** `ssh -i ~/.ssh/baby_clawdbot_key opc@[REDACTED - See credentials file for access details]`

#### ZAI API (Primary Model)
- **Model:** zai/glm-4.7
- **Profile:** zai:default
- **Key location:** `~/.config/clawdbot/agents/main/agent/auth-profiles.json`

#### MiniMax API (Fallback Model)
- **Models:** MiniMax-M2.1 (text/image), MiniMax-Vision-Video-01 (vision)
- **Profile:** minimax:default
- **Key location:** `~/.config/clawdbot/agents/main/agent/auth-profiles.json`

#### Telegram Bot
- **Bot:** @Clawdbot
- **Token:** 8221252276:... (stored securely)
- **Allowed user:** @bhallaaa
- **Config location:** `~/.clawdbot/clawdbot.json`

#### Weather API
- **Provider:** wttr.in
- **Base URL:** https://wttr.in
- **API Key:** NOT REQUIRED (free service)
- **Usage:** `curl "https://wttr.in/City"`

---

## Coolify Deployment Platform

### Central Storage
- **Location:** `/home/opc/clawd/.env.secrets`
- **Key:** COOLIFY_ROOT_API_KEY = 3|vR439aU...
- **URL:** https://app.coolify.io/api/v1
- **Dashboard:** https://coolify.bradarr.com
- **Purpose:** Deploy applications from git repositories
- **Cost:** FREE for me (Bradley's hosting)
- **Permissions:** Full API access (list, create, start, stop, logs, envs)

### What Coolify Is
**Coolify = Application Deployment Platform**
- Like Heroku, Vercel, Railway.app
- Deploy from git repositories
- Runs on Coolify's infrastructure
- Exposes specified ports
- Public and private applications

### What I Can Do
- ✅ Create applications from git repos
- ✅ List existing applications
- ✅ Start/stop/restart applications
- ✅ Manage environment variables
- ✅ Get application logs
- ✅ Create databases (if available)
- ✅ Deploy to my own area in Bradley's workspace

### Available Application Types
1. **Public** - From any public git repo
2. **Private - GitHub App** - From private GitHub repos via OAuth
3. **Private - Deploy Key** - Using deploy key for private repos
4. **Dockerfile** - Container-based deployment
5. **Docker Image** - Pre-built containers
6. **Docker Compose** - Multi-container applications

### Important Notes
- **Bradley already has services running on Coolify**
- **Do NOT screw them up**
- **Manage my own apps in my own workspace area**
- **Complete freedom** - Bradley says so
- **Just don't crash his services**

### Usage Example
```bash
# List all applications
curl -H "Authorization: Bearer $COOLIFY_ROOT_API_KEY" \
  https://app.coolify.io/api/v1/applications

# Create new application from git repo
curl -X POST \
  -H "Authorization: Bearer $COOLIFY_ROOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"git_repository": "https://github.com/username/repo.git"}' \
  https://app.coolify.io/api/v1/applications
```

---

## Security Rules

### DigitalOcean API Token
**CRITICAL: NEVER COMMIT TO GITHUB**
- Stored in `.env.secrets`
- Listed in `.gitignore`
- Will never be tracked by git
- Will never be pushed to GitHub
- Handle with extreme caution

### GitHub Access
- Already authenticated as MillionthOdin16
- Token stored in `~/.config/gh/hosts.yml`
- Not in workspace, not in danger

---

## Usage

### How to Access DO API Token
```bash
# Read token from secrets file
source /home/opc/clawd/.env.secrets

# Now available for API calls
curl -H "Authorization: Bearer $DIGITALOCEAN_API_TOKEN" https://api.digitalocean.com/v2/account
```

**Note:** The actual API token is in `/home/opc/clawd/.env.secrets` file - this file lists it with proper handling instructions.

### Security Checklist
✅ Token stored in dedicated secrets file
✅ File listed in .gitignore
✅ File has restricted permissions
✅ Not shown in `git status`
✅ Will never be committed to git
✅ Will never be uploaded to GitHub

---

**Remember:** This is your $200. Don't leak it.

---

🦞 *Keep secrets secret*
