# Clawdbot Migration Changelog

**Migration:** NPM v2026.1.11-4 → GitHub v2026.1.14
**Date:** 2026-01-14
**Downtime:** ~3 seconds (live switch)

---

## Version Comparison Summary

| Aspect | Current (NPM 2026.1.11-4) | Target (GitHub 2026.1.14) |
|--------|---------------------------|---------------------------|
| **Version** | 2026.1.11-4 | 2026.1.14 |
| **Source** | NPM package | GitHub source |
| **Location** | `/home/opc/.nvm/.../node_modules/clawdbot` | `/home/opc/clawdbot` |
| **Stars** | N/A | ⭐ 4,187 |

---

## Changes in 2026.1.12 → 2026.1.14

### 🔥 BREAKING CHANGES

1. **"providers" renamed to "channels"**
   - CLI/RPC/config now use `channels.*` instead of `providers.*`
   - Legacy config keys auto-migrate on load
   - Affects: Slack/Telegram/WhatsApp config structure

### ✨ NEW FEATURES

#### Memory System
- **Vector search** for agent memories (Markdown-only)
- SQLite index with chunking + lazy sync + file watch
- Per-agent enablement/fallback configuration
- New `clawdbot memory` CLI
- New `memory_search`/`memory_get` tools with snippets + line ranges
- Custom OpenAI-compatible embedding endpoints
- Support for `node-llama-cpp` embeddings

#### Plugins
- Full voice-call plugin parity (Telnyx/Twilio, streaming, inbound policies)
- Extension loader for tools/RPC/CLI/services
- Discovery paths and config schema
- Control UI labels (`uiHints`)
- `clawdbot plugins install|list|info|enable|disable|doctor`

#### Models
- **Synthetic provider** added
- **Moonshot Kimi K2 0905** + turbo/thinking variants
- MiniMax vision now routes to Coding Plan VLM endpoint
- Accepts `@/path/to/file.png` inputs

#### Cron
- One-shot schedules accept ISO timestamps (UTC)
- Optional delete-after-run
- Can target specific agent (CLI + macOS/Control UI)
- `--model` flag for cron add/edit commands

#### Agents
- **Compaction mode** with configurable safeguard summarization
- Per-agent model fallbacks
- Pre-compaction memory flush (stores durable memories before compaction)
- Memory recall guidance strengthened
- Workspace bootstrap truncation configurable (default 20k)

#### Tools
- **Browser `scrollintoview` action**
- Tool profiles + group shorthands
- Docker bind mounts via `docker.binds`
- Claude/Gemini tool param aliases
- `thinking: xhigh` for GPT-5.2/Codex

#### Gateway/CLI
- **Tailscale** binary discovery, custom bind mode, probe auth retry
- `clawdbot dashboard` auto-open flow
- Native slash commands default to `"auto"`
- OpenAI-compatible `/v1/chat/completions` HTTP endpoint

#### Auth/Onboarding
- **Chutes OAuth** (PKCE + refresh + onboarding choice)
- TUI onboarding defaults to `deliver: false`

### 🐛 FIXES (2026.1.12 - 2026.1.14)

| Issue | Fix |
|-------|-----|
| WhatsApp context isolation | Now uses conversation ID (not bot's number) |
| Telegram timeoutSeconds | Now honored for grammY API requests |
| Telegram long captions | Split into media + follow-up text |
| macOS cron preview | Fixed `channel` key usage |
| Slack Socket Mode | Drops events with mismatched `api_app_id`/`team_id` |
| Discord autoThread | Thread context isolation |
| Gateway dev profile | Uses dev config + state (`~/.clawdbot-dev`) |
| Postinstall pnpm patches | Already-applied patches are no-ops |
| Packaging | `dist/memory/**` and `dist/channels/**` included in npm tarball |
| Agent registry | Persists across gateway restarts |

### 📦 INSTALLER CHANGES

- JS patcher replaces `git apply` (works npm/pnpm/bun, no git dependency)
- `CLAWDBOT_NO_ONBOARD=1` for non-interactive installs
- `--install-method git|npm` flag
- Git checkout detection with migration prompts

---

## Key Commands After Migration

```bash
# Run from GitHub source
cd /home/opc/clawdbot
npm run start

# Or use the entry point directly
node /home/opc/clawdbot/dist/entry.js gateway --port 18789

# Check status
clawdbot status

# Plugins
clawdbot plugins list
clawdbot memory search "query"

# Update (from git)
cd /home/opc/clawdbot && git pull
```

---

## Files Moved/Changed

| Before (NPM) | After (GitHub) |
|--------------|----------------|
| `/home/opc/.nvm/.../node_modules/clawdbot/` | `/home/opc/clawdbot/` |
| Config: `/home/opc/.clawdbot/` | Config: `/home/opc/clawdbot/.clawdbot/` (copied) |

---

## Rollback Plan

If issues occur, rollback to NPM:

```bash
# Stop GitHub version
pkill -f "clawdbot.*dist/entry.js"

# Start NPM version
node /home/opc/.nvm/.../node_modules/clawdbot/dist/entry.js gateway --port 18789
```

---

## What's Different for Me (Clawd)

### Same
- Same config location
- Same port (18789)
- Same providers (WhatsApp, etc.)

### New Capabilities
1. **Vector memory search** - Can search memories semantically
2. **Plugin system** - Voice calls, custom extensions
3. **Better model options** - Moonshot Kimi K2, Synthetic
4. **Tailscale integration** - If using Tailscale
5. **Improved CLI** - `clawdbot dashboard`, better status

### New Configuration Options
```yaml
# Example new config sections
channels:  # (was providers)
  telegram:
    timeoutSeconds: 30

agents:
  defaults:
    compaction:
      enabled: true
      headroom: 5000
    memory:
      vectorSearch: true

plugins:
  load:
    paths: []
```

---

*Generated: 2026-01-14 | Migration preparation complete*
