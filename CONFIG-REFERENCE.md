# CLAWDBOT CONFIG REFERENCE

**Quick reference for `~/.clawdbot/clawdbot.json`**

---

## Common Config Issues

### Problem: "You are not authorized to use this command"

**Cause:** `dmPolicy: "allowlist"` requires `allowFrom` array.

**Fix:**
```json
{
  "channels": {
    "telegram": {
      "dmPolicy": "allowlist",
      "allowFrom": ["@bhallaaa", "123456789"],  // Add usernames or user IDs
      "dms": {
        "@bhallaaa": {}  // Per-DM config (not for allowlist)
      }
    }
  }
}
```

---

## Telegram Channel Config

| Setting | Values | Purpose |
|---------|--------|---------|
| `dmPolicy` | `pairing` / `allowlist` / `open` / `disabled` | How DMs are handled |
| `allowFrom` | Array of user IDs or usernames | Who can send DMs (required for `allowlist`) |
| `groupPolicy` | `open` / `allowlist` / `disabled` | How groups are handled |
| `groupAllowFrom` | Array of user IDs or usernames | Who can use commands in groups |

### dmPolicy Options

- **`pairing`** (default): Unknown senders get pairing code; you must approve
- **`allowlist`**: Only allow senders in `allowFrom` (or already paired)
- **`open`**: Allow all DMs (requires `allowFrom: ["*"]`)
- **`disabled`**: Ignore all DMs

### groupPolicy Options

- **`open`**: Groups bypass allowFrom, only mention-gating applies
- **`allowlist`**: Only allow group messages from `groupAllowFrom`/`allowFrom`
- **`disabled`**: Block all group messages

---

## Example Config

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "dmPolicy": "allowlist",
      "allowFrom": ["@bhallaaa"],
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["@bhallaaa"],
      "dms": {
        "@bhallaaa": {
          "model": "minimax/MiniMax-M2.1"
        }
      },
      "commands": {
        "native": true,
        "nativeSkills": true
      }
    }
  }
}
```

---

## Commands to Apply Changes

```bash
# Edit config
nano ~/.clawdbot/clawdbot.json

# Apply changes (restarts daemon)
clawdbot daemon restart

# Check config is valid
clawdbot doctor --non-interactive
```

---

## Location

- **Config:** `~/.clawdbot/clawdbot.json`
- **Docs:** https://docs.clawd.bot/configuration
