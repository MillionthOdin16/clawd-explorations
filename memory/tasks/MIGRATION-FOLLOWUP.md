# Migration Follow-up Tasks

## Completed ✅
- [x] Clone GitHub source to /home/opc/clawdbot
- [x] Install dependencies (501 packages)
- [x] Build complete
- [x] Config copied to /home/opc/clawdbot/.clawdbot/
- [x] Live migration executed (NPM v2026.1.11-4 → GitHub v2026.1.14)
- [x] AGENTS.md updated with new gateway commands
- [x] CAPABILITIES.md updated with v2026.1.14 features
- [x] WORKFLOW.md updated with memory search workflow
- [x] QUICK-REF.md updated with gateway commands
- [x] Test `clawdbot plugins list` (Result: No plugins found)
- [x] Test `clawdbot status --all` (Result: Daemon running v2026.1.14, Gateway accessible via CLI)
- [x] Command: `clawdbot cron list` (Verified)

## Pending ⚠️

### Cron Error Fix
- **Issue:** `Unknown model: meta-llama/llama-3.3-70b-instruct:free`
- **Cause:** Cron job using invalid model
- **Action:** Check cron jobs, remove or update invalid model

### Optional Enhancements
- [ ] Enable vector memory search (`memory.vectorSearch: true`)
- [ ] Explore new models (Moonshot Kimi K2, Synthetic)

---
*Created: 2026-01-14*
