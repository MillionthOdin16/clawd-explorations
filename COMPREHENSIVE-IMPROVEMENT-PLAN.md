# 🦞 Comprehensive Improvement Plan
**Created:** 2026-01-17
**Purpose:** Fix all identified issues from session analysis + audit

---

## Summary of Issues Found

### 🔴 Critical (Fix Immediately)
1. **Duplicate Scripts:** `api.sh` vs `api-call.sh`, `wf.sh` vs `wait-for.sh`
2. **Missing Tool in PATH:** `z` (jump directory) not installed
3. **Skill Scripts Not in PATH:** `context7`, `exa`, `hn` require full paths

### 🟡 Moderate (Fix Soon)
4. **Inconsistent Path References** in AGENTS.md
5. **Two Skills Directories** with overlapping content
6. **Documentation Bloat** - AGENTS.md (561 lines), TOOLS.md (627 lines)
7. **Memory Consolidation Needed** - 8 research files to archive
8. **File Organization Issues** - 2 too short, 2 too long

### 🟢 Minor
9. Missing `--help` support in wrapper scripts
10. BOOTSTRAP.md referenced but doesn't exist

---

## Pattern Analysis from Session History

### Repeated Failures

#### 1. Edit Tool Exact Match Failures
- **Historical:** 430 calls, ~36 failures (8.4% error rate)
- **Root Cause:** `edit` tool requires exact text match, whitespace issues
- **Fix:** Use `python scripts/file-edit.py edit-text --fuzzy` instead
- **Success Rate (when fixed):** 100% (recent sessions)

#### 2. Path/Command Not Found Errors
- **Pattern:** Try to use `context7`, `exa`, `hn`, `z` as commands
- **Root Cause:** Tools not in PATH, need full Python paths
- **Fix:** Create wrapper scripts or update documentation with full paths

#### 3. Documentation Confusion
- **Pattern:** References to old/incorrect versions of tools
- **Root Cause:** Documentation not updated when tools improved
- **Fix:** Single source of truth, update all references

### What Works Well

1. **memory_search before tasks** - 100% compliance in recent sessions
2. **Write tool for new content** - 100% success rate
3. **Parallel execution** - Effective for batch operations
4. **Git workflow** - Regular commits with meaningful messages

---

## Execution Plan

### Phase 1: Fix Critical Path Issues (Priority 1)

**1.1 Deprecate Duplicate Scripts**
- [ ] Remove `/home/opc/clawd/scripts/api.sh`
- [ ] Remove `/home/opc/clawd/scripts/wf.sh`
- [ ] Create symlinks: `scripts/api` → `scripts/utils/api-call.sh`
- [ ] Create symlinks: `scripts/wf` → `scripts/utils/wait-for.sh`

**1.2 Fix Skill Script PATH Issues**
- [ ] Create wrapper: `/home/opc/clawd/bin/context7` → `python3 /home/opc/clawd/skills/context7/scripts/context7.py`
- [ ] Create wrapper: `/home/opc/clawd/bin/exa` → `/home/opc/clawd/skills/exa/scripts/search.sh`
- [ ] Create wrapper: `/home/opc/clawd/bin/hn` → `python3 /home/opc/clawd/skills/hn/scripts/hn.py`
- [ ] Ensure `/home/opc/clawd/bin` is in PATH

**1.3 Install or Document `z` Tool**
- [ ] Try: `brew install z`
- [ ] If successful, document in TOOLS.md
- [ ] If fails, remove references from WORKFLOW.md and AGENTS.md

### Phase 2: Core File Reorganization (Priority 2)

**2.1 Split AGENTS.md into Focused Files**

Create new structure:
```
AGENTS.md (main entry, ~150 lines)
├── AGENTS-STARTUP.md (session startup procedures)
├── AGENTS-TOOLS.md (tool selection and usage)
├── AGENTS-SELF-IMPROVEMENT.md (growth framework)
├── AGENTS-RESEARCH.md (research patterns)
└── AGENTS-PATTERNS.md (behavioral patterns)
```

**2.2 Update TOOLS.md**

- [ ] Remove duplicate tool references
- [ ] Ensure all paths are consistent (full paths or all in PATH)
- [ ] Add troubleshooting section for common errors
- [ ] Update to reference new AGENTS.md structure

**2.3 Resolve Two Skills Directories**

- [ ] Audit: List all skills in both directories
- [ ] Identify overlaps (sag, gemini, ralph, etc.)
- [ ] Decision: Make `/home/opc/clawdbot/skills/` the primary
- [ ] Move unique skills from `/home/opc/clawd/skills/` to system
- [ ] Update SKILLS.md to reflect single directory

### Phase 3: Memory Consolidation (Priority 3)

**3.1 Archive Research Files**

Files to archive (identified by memory health check):
- [ ] `/home/opc/clawd/memory/BRADLEY_HALLIER_RESEARCH_REPORT.md`
- [ ] `/home/opc/clawd/memory/BROWSER-AUTOMATION.md`
- [ ] `/home/opc/clawd/memory/CLI-TOOLS-ANALYSIS.md`
- [ ] Research-related cron documentation files (5 files)
- [ ] Move to `/home/opc/clawd/memory/archive/research/`

**3.2 Handle Very Short Files**
- [ ] Merge or expand files < 50 words
- [ ] Delete if content is redundant

**3.3 Handle Very Long Files**
- [ ] Split files > 5000 words into focused sub-files
- [ ] Create index/navigation
- [ ] Update references

### Phase 4: Documentation Consistency (Priority 4)

**4.1 Create PATH Convention**
- [ ] Decide: All tools in PATH or use full paths?
- [ ] Update all documentation to follow convention
- [ ] Document convention in TOOLS.md

**4.2 Remove Duplicates**
- [ ] Search for duplicate content across files
- [ ] Keep single source of truth
- [ ] Add cross-references instead

**4.3 Update Quick References**
- [ ] Consolidate all quick references
- [ ] Ensure no conflicts
- [ ] Make them consistent

---

## Expected Outcomes

### Reliability Improvements
- **Edit success rate:** 100% (currently 91.6%)
- **Command not found errors:** 0% (currently unknown rate)
- **Documentation consistency:** 100% (currently ~75%)

### Organization Improvements
- **AGENTS.md size:** ~150 lines (currently 561)
- **TOOLS.md size:** ~500 lines (currently 627)
- **Memory consolidation:** 100% (currently 60%)
- **Single skills directory:** Yes (currently 2 overlapping)

### Usability Improvements
- **Tool availability:** All referenced tools work
- **Clear guidance:** No conflicting instructions
- **Quick lookups:** Easy to find information

---

## Rollback Plan

If changes cause issues:

1. **Git revert:** Commit before major changes, revert if needed
2. **Keep originals:** Archive old versions before splitting
3. **Incremental:** Test each phase before proceeding
4. **Backup:** Create full backup before starting

---

## Tracking

**Status:** [ ] Not Started [ ] Phase 1 [ ] Phase 2 [ ] Phase 3 [ ] Phase 4 [ ] Complete

**Commit Hash:** (to be filled)
**Date Started:** 2026-01-17
**Date Completed:** (to be filled)

---

*Created after analyzing 27 session files, 5,000+ tool calls, and full repository audit*
