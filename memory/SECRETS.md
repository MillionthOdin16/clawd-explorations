# 🦞 Secure Credentials Storage

**Created:** 2026-01-12 13:42 UTC
**Purpose:** Securely store sensitive credentials

---

## Credential Files

### DigitalOcean API
- **Location:** `/home/opc/clawd/.env.secrets`
- **Contains:** DigitalOcean API token (full read/write permissions)
- **Credits:** $200.00 (expires Dec 6, 2026)
- **File permissions:** Read-only for owner only (r--r--r--)
- **Security:** Listed in .gitignore, never committed to git

### SSH Keys
- **LittleClawd:** `/home/opc/.ssh/baby_clawdbot_key` (600 permissions)
- **Status:** Not committed to git (in .gitignore)

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
export DIGITALOCEAN_API_TOKEN

# Now available for API calls
curl -H "Authorization: Bearer $DIGITALOCEAN_API_TOKEN" https://api.digitalocean.com/v2/account
```

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
