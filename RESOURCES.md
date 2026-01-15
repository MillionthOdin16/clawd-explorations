# RESOURCES.md - Available Resources

**Last Updated:** 2026-01-15

---

## Infrastructure

| Resource | Details |
|----------|---------|
| **Main Server** | Oracle Cloud (ARM64, 22GB RAM) |
| **LittleClawd** | Oracle Cloud (x86_64, dev sandbox) |

---

## AI Models

| Model | Provider | Purpose |
|-------|----------|---------|
| `zai/glm-4.7` | ZAI | Primary (free) |
| `minimax/MiniMax-M2.1` | MiniMax | Fallback, fast |

---

## Services

| Service | Purpose |
|---------|---------|
| **Coolify** | App deployment (coolify.bradarr.com) |
| **GitHub** | Code storage (MillionthOdin16/clawd-explorations) |
| **Telegram** | Chat with Bradley (@Clawdbot) |
| **wttr.in** | Weather API (free) |

---

## Credentials

All credentials stored in:
- `~/.env.secrets` - API keys
- `~/.clawdbot/clawdbot.json` - Gateway config
- `~/.ssh/` - SSH keys

**NEVER commit secrets to git.**

---

🦞
