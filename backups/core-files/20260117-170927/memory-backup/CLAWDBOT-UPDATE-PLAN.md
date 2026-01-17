# Clawdbot Update Plan & Report
**Date:** 2026-01-17  
**Current Version:** 363 commits behind origin/main  
**Target Version:** v2026.1.17

---

## Executive Summary

This report outlines the plan for updating Clawdbot from the current local version to the latest upstream version (v2026.1.17), highlighting **6 major new features** and **core file updates** needed to fully leverage these capabilities.

---

## 1. Update Execution Plan

### Step 1: Backup Current State
```bash
# Stash local changes (if any)
cd /home/opc/clawdbot
git stash

# Create backup of config and data
cp -r .clawdbot ~/.clawdbot-backup-$(date +%Y%m%d)
```

### Step 2: Pull Latest Changes
```bash
git fetch origin
git pull origin main
```

### Step 3: Apply Local Changes (if any)
```bash
git stash pop
```

### Step 4: Update Dependencies & Restart
```bash
clawdbot update run
clawdbot daemon restart
```

### Step 5: Verify & Document
```bash
clawdbot --version
clawdbot doctor
```

---

## 2. New Features & Capabilities

### 2.1 Deepgram Audio Transcription 🔊
**Commit:** `e637bbdfb`

**What it does:**
- Adds native Deepgram integration for audio transcription
- Supports multiple audio formats and configurations
- Provides high-accuracy speech-to-text

**Schema:**
```typescript
interface DeepgramConfig {
  provider: 'deepgram';
  apiKey?: string; // Or via DEEPGRAM_API_KEY env var
  model?: string;
  language?: string;
  punctuate?: boolean;
  smartFormat?: boolean;
  utterances?: boolean;
}

interface AudioInput {
  type: 'audio';
  audio: {
    source: 'url' | 'file' | 'stream';
    url?: string;
    path?: string;
  };
}
```

**Impact on me:**
- ✅ I can now **transcribe audio files** natively
- ✅ Better multimodal understanding
- ✅ New tool: `audio-transcription` (if exposed)

**Files to update:**
- `TOOLS.md` - Add audio transcription tool documentation
- `CAPABILITIES.md` - Add Deepgram provider info

---

### 2.2 Session IdentityLinks (Cross-Platform DM Linking) 🔗
**Commit:** `0cd24137e`

**What it does:**
- Links sessions across different platforms (iMessage ↔ Signal ↔ Telegram)
- Maintains conversation continuity when users switch platforms
- Enables unified DM history across channels

**Schema:**
```typescript
interface IdentityLink {
  id: string;
  primaryIdentity: string;
  linkedIdentities: {
    platform: string;
    identifier: string;
    linkedAt: Date;
  }[];
  sessionIds: string[];
}

interface SessionIdentityLinks {
  links: IdentityLink[];
  mergeStrategy: 'manual' | 'auto' | 'prompt';
}
```

**Impact on me:**
- ✅ **Better context awareness** across platforms
- ✅ Unified conversation history
- ✅ Smoother transitions when users switch devices
- ✅ Cross-platform DM continuity

**Files to update:**
- `AGENTS.md` - Document cross-platform DM handling
- `SOUL.md` - Update "awareness" section with cross-platform context
- `docs/concepts/session.md` - Already updated upstream, need to sync

---

### 2.3 Internal Hooks System 🪝
**Commit:** `faba508fe`

**What it does:**
- Event-driven architecture for internal extensions
- Allows custom logic to run on specific events
- Provides plugin-like functionality without full plugins

**Hook Types:**
- `onMessage` - Intercept/process incoming messages
- `onSend` - Modify outgoing messages
- `onSessionStart` - Session initialization logic
- `onSessionEnd` - Cleanup logic
- `onToolCall` - Intercept/modify tool calls
- `onError` - Custom error handling

**Impact on me:**
- ✅ More extensible behavior
- ✅ Can implement custom logic for specific workflows
- ✅ Better automation capabilities

**Files to update:**
- `SKILLS.md` - Add hook development documentation
- `AGENTS.md` - Document hook system capabilities

---

### 2.4 Environment Variable Substitution in Config ⚙️
**Commit:** `a36735b91`

**What it does:**
- Allows dynamic config values using env vars
- Format: `${ENV_VAR_NAME}` or `${ENV_VAR_NAME:-default}`
- Supports nested substitution

**Example:**
```yaml
# Before
apiKey: "sk-xxx"  # Hardcoded

# After
apiKey: "${OPENAI_API_KEY}"
databaseUrl: "${DATABASE_URL:-postgresql://localhost:5432/clawdbot}"
```

**Impact on me:**
- ✅ Better secret management
- ✅ More flexible deployments
- ✅ Improved security (no hardcoded secrets)

**Files to update:**
- `docs/configuration.md` - Document env var substitution syntax
- `docs/gateway/configuration.md` - Sync with upstream updates

---

### 2.5 Remote Skills Hot Reload 🔥
**Commit:** `b2b331230`

**What it does:**
- Skills can be updated without restarting the gateway
- Remote skill registry support
- Hot-reload on skill file changes

**Impact on me:**
- ✅ **Faster skill development** iteration
- ✅ No restart required for skill updates
- ✅ Dynamic skill loading

**Files to update:**
- `SKILLS.md` - Document hot reload behavior
- `AGENTS.md` - Update skill loading section

---

### 2.6 Schema-Driven Config UI 🎨
**Commits:** Multiple (2026.1.15+)

**What it does:**
- Config UI generated from JSON Schema
- Better type safety and validation
- Improved Control UI experience

**Impact on me:**
- ✅ Better configuration management via UI
- ✅ Reduced configuration errors
- ✅ More intuitive setup process

**Files to update:**
- `docs/gateway/configuration.md` - Sync with schema changes
- `docs/cli/config.md` - Update for new UI

---

## 3. Breaking Changes & Migration Notes

### 3.1 Security Hardening
- **Gateway probe auth** - May require config updates for older auth setups
- **Command execution** - Default-deny now enforced

### 3.2 Config Schema Changes
- Some config fields renamed or restructured
- `dmScope` for multi-user DM isolation (new field)

### 3.3 Tool Schema Updates
- Format parameter renamed (avoided JSON Schema keyword conflict)
- Session preservation behavior changed

### 3.4 Migration Checklist
- [ ] Review `clawdbot doctor` output
- [ ] Backup current config: `clawdbot config get > backup-config.json`
- [ ] Update config for schema changes
- [ ] Test in development before production

---

## 4. Core Files Update Plan

### 4.1 Files to Update in `/home/opc/clawd/`

| File | Update Type | Priority |
|------|-------------|----------|
| `TOOLS.md` | Add Deepgram audio tool | HIGH |
| `AGENTS.md` | Add hook system, remote skills | HIGH |
| `SOUL.md` | Update awareness section | MEDIUM |
| `CAPABILITIES.md` | Add new providers | MEDIUM |
| `SKILLS.md` | Add hot reload, hooks docs | MEDIUM |
| `docs/configuration.md` | Add env var substitution | HIGH |

### 4.2 Files to Sync from Upstream

| File | Reason |
|------|--------|
| `docs/concepts/session.md` | IdentityLinks documentation |
| `docs/gateway/configuration.md` | Schema updates |
| `docs/internal-hooks.md` | New hook documentation |

---

## 5. New Capabilities Summary

### After Update, I Will Have:

1. **Audio Transcription** - Transcribe audio files natively with Deepgram
2. **Cross-Platform DM Linking** - Better continuity across iMessage/Signal/Telegram
3. **Extensibility** - Internal hooks for custom logic
4. **Dynamic Configuration** - Environment variable substitution
5. **Faster Iteration** - Remote skills hot reload
6. **Better UX** - Schema-driven config UI

### Impact on My Operations:

- **More multimodal** - Can now handle audio input/output
- **More context-aware** - Cross-platform conversation history
- **More extensible** - Hook system for custom workflows
- **More secure** - No hardcoded secrets in config

---

## 6. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Config migration errors | Medium | Backup before update, test with `clawdbot doctor` |
| Breaking changes | Low | Review changelog, test in dev first |
| Skill compatibility | Low | Hot reload helps, can rollback skills |
| Performance regression | Low | Monitor after update |

---

## 7. Post-Update Verification

```bash
# 1. Check version
clawdbot --version

# 2. Run diagnostics
clawdbot doctor

# 3. Test new features
clawdbot config get  # Verify config loading
clawdbot hooks list  # If available
clawdbot skills list # Verify skill loading

# 4. Monitor logs
tail -f ~/.claude/logs/*.log
```

---

## 8. Timeline Estimate

| Phase | Duration | Notes |
|-------|----------|-------|
| Backup & Stash | 5 min | Quick operation |
| Git Pull | 10 min | 363 commits, may have conflicts |
| Config Migration | 15 min | May need manual updates |
| Dependency Update | 10 min | `clawdbot update run` |
| Restart & Test | 10 min | Verify all systems |
| **Total** | **~50 min** | May vary |

---

## 9. Questions & Next Steps

### Before proceeding, confirm:
1. ✅ Should I proceed with the update now?
2. ✅ Are there any custom configs/hooks that need special handling?
3. ✅ Should I update core files proactively, or after update?

### Next Actions:
1. **Option A:** Proceed with update immediately
2. **Option B:** Review and approve plan first
3. **Option C:** Test in development environment first

---

*Report generated: 2026-01-17T17:00Z*
*Version gap: 363 commits*
*Target: v2026.1.17*
