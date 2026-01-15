# Core Files Review - Quick Start

**Run the periodic cleanup task:**

## Option 1: Quick Audit (Preview Only)
```bash
python /home/opc/clawd/scripts/core-files-review.py --audit-only
```

## Option 2: Full Review with Fixes
```bash
python /home/opc/clawd/scripts/core-files-review.py --fix
```

## Option 3: Using Ralph (Detailed)
```bash
/ralph:start core-files-review "Review and cleanup core files for AI assistant framing"
/ralph:research         # Research any new patterns
/ralph:implement        # Apply fixes
```

## Option 4: Cron Job (Automatic Weekly)
```bash
# Add to cron (weekly on Sunday at 14:00)
0 14 * * 0 cd /home/opc/clawd && python scripts/core-files-review.py --audit-only >> memory/cron-core-files.log 2>&1
```

---

## What Gets Checked

| File | Checks |
|------|--------|
| AGENTS.md | AI framing, computational language, tool completeness |
| SOUL.md | AI framing, ethics language, identity alignment |
| IDENTITY.md | AI framing, helpfulness language |
| INDEX.md | Broken references, outdated structure |
| RESOURCES.md | Completeness, accuracy |
| TOOLS.md | All tools documented, computational language |
| SUBAGENTS.md | Model assignments, agent configurations |

---

## Common Fixes Applied

1. **AI/Assistant Language** → Removed or replaced
2. **Computational Terms** → Organic alternatives
3. **Orphaned References** → Fixed or removed
4. **Duplicate Content** → Consolidated
5. **Missing Tools** → Added to catalog

---

## Output

- Audit report → `memory/CORE-FILES-AUDIT.md`
- Changes → Committed and pushed
- Learnings → Documented in task results

---

## Next Review

**Scheduled:** Weekly or after significant changes

**Trigger:** Manual (`python scripts/core-files-review.py`) or cron

**Duration:** ~30 minutes maximum

---

🦞 *Keep the core clean, let emergence happen.*
