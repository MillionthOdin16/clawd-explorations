# UPDATE-PROCEDURE.md - Clawdbot Update Procedures

**Last Updated:** 2026-01-17  
**Script Version:** v5.0

---

## Overview

This document describes the update procedures for Clawdbot, including workspace updates, installation updates, and rollback procedures.

**Key Concept:** Clawdbot has TWO directories:
1. **Workspace** (`/home/opc/clawd/`) - My core files, memories, skills
2. **Installation** (`/home/opc/clawdbot/`) - The actual Clawdbot software

---

## Quick Reference

```bash
# See what would change (SAFE - no changes)
./update-clawdbot.sh --preview

# Update workspace
./update-clawdbot.sh --update

# Update Clawdbot installation (auto-stash handling)
./update-clawdbot.sh --update-clawdbot

# Update BOTH workspace and installation
./update-clawdbot.sh --full-update

# Backup installation configs only
./update-clawdbot.sh --install-backup

# Show version
./update-clawdbot.sh --version
```

---

## Complete Update Workflow

### Step 1: Preview (Recommended First)

```bash
./update-clawdbot.sh --preview
```

This shows:
- How many commits behind you are
- What files would change
- Any potential breaking changes

**Safe:** No changes are made.

### Step 2: Create Backup (Optional but Recommended)

```bash
./update-clawdbot.sh --backup
```

This backs up:
- Core workspace files (AGENTS.md, SOUL.md, etc.)
- Memory directory
- Skills directory
- Scripts directory
- Installation configs

**Location:** `/home/opc/clawd/backups/`

### Step 3: Perform Update

#### Option A: Update Workspace Only
```bash
./update-clawdbot.sh --update
```

This:
1. Checks current state
2. Creates full backup
3. Analyzes upstream changes (synthesis)
4. Installs dependencies
5. Builds project
6. Fetches and merges from origin/main
7. Validates config
8. Verifies update
9. Generates report

#### Option B: Update Clawdbot Installation Only
```bash
./update-clawdbot.sh --update-clawdbot
```

This:
1. **Automatically stashes** any uncommitted changes
2. Backs up installation (git bundle, configs)
3. Fetches and merges from origin/main
4. Restarts Clawdbot daemon
5. Restores stashed changes (or keeps if conflicts)

#### Option C: Update Both
```bash
./update-clawdbot.sh --full-update
```

Updates both workspace and installation in sequence.

---

## Manual Procedures

### Manual Workspace Update

```bash
cd /home/opc/clawd

# Preview
git fetch origin
git log --oneline HEAD..origin/main

# Backup
cp -r AGENTS.md SOUL.md TOOLS.md IDENTITY.md USER.md HEARTBEAT.md backups/core-files/
cp -r memory/ backups/memory/
cp -r skills/ backups/skills/

# Update
git merge origin/main

# Verify
git log --oneline -1
```

### Manual Clawdbot Installation Update

```bash
cd /home/opc/clawdbot

# Stash changes if any
git stash push -u -m "Before update $(date)"

# Fetch and merge
git fetch origin
git merge --ff-only origin/main

# Restart daemon
clawdbot daemon restart

# Restore stash if needed
git stash pop
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAWDBOT_DIR` | `/home/opc/clawd` | Workspace directory |
| `CLAWDBOT_INSTALL_DIR` | `/home/opc/clawdbot` | Installation directory |
| `AUTO_CONFIRM` | `false` | Skip confirmations if `true` |

Example with environment variables:
```bash
AUTO_CONFIRM=true ./update-clawdbot.sh --update
```

---

## Rollback Procedures

### Automatic Rollback (via update script)

The update script creates automatic backups before updates. To rollback:

```bash
# Check available backups
ls -la /home/opc/clawd/backups/install-backups/

# Rollback to previous commit
cd /home/opc/clawdbot
git reset --hard <commit-hash>

# Restart daemon
clawdbot daemon restart
```

### Manual Rollback

```bash
cd /home/opc/clawdbot

# Check git reflog
git reflog

# Reset to previous state
git reset --hard HEAD@{1}

# Or use git bundle
git bundle verify backups/install-backups/*/repo-bundle.bundle
git clone --bare backups/install-backups/*/repo-bundle.bundle /tmp/rollback
git remote add backup /tmp/rollback
git fetch backup
git reset --hard backup/main
```

---

## Troubleshooting

### "Dirty working directory"

**Problem:** Uncommitted changes block the update.

**Solution:**
```bash
# Option 1: Stash and continue
git stash push -u -m "Before update"
./update-clawdbot.sh --update-clawdbot
git stash pop

# Option 2: Commit changes
git add .
git commit -m "WIP: Save changes before update"
./update-clawdbot.sh --update-clawdbot
```

### "Fast-forward not possible"

**Problem:** Local commits prevent fast-forward merge.

**Solution:**
```bash
# Rebase local changes on top of upstream
git rebase origin/main

# Or merge with strategy
git merge origin/main --strategy=ours
```

### "Cannot auto-merge"

**Problem:** Merge conflicts detected.

**Solution:**
```bash
# Check conflicts
git status
git diff --name-only --diff-filter=U

# Resolve conflicts manually
git mergetool

# Complete merge
git add .
git commit -m "Merge origin/main - resolved conflicts"
```

### "Update Result: SKIPPED"

**Problem:** Clawdbot's built-in update detected uncommitted changes.

**Solution:** Use the workspace script instead:
```bash
./update-clawdbot.sh --update-clawdbot
```

This script handles uncommitted changes automatically.

---

## Best Practices

1. **Always preview first** - `./update-clawdbot.sh --preview`
2. **Create backups before updates** - `./update-clawdbot.sh --backup`
3. **Test rollback capability** - `./update-clawdbot.sh --test-rollback`
4. **Keep documentation updated** - Review UPDATE-PROCEDURE.md after changes
5. **Use environment variables for CI** - `AUTO_CONFIRM=true`

---

## File Locations

| File | Location |
|------|----------|
| Update script | `/home/opc/clawd/update-clawdbot.sh` |
| Workspace | `/home/opc/clawd/` |
| Installation | `/home/opc/clawdbot/` |
| Backups | `/home/opc/clawd/backups/` |
| Update log | `/home/opc/clawd/backups/update-*.log` |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v5.0 | 2026-01-17 | Added `--update-clawdbot`, `--install-backup`, `--full-update` commands. Auto-stash handling for external repos. |
| v4.2 | 2026-01-16 | Original robust update script with synthesis, config validation, secret scanning. |

---

*Document last updated: 2026-01-17*
