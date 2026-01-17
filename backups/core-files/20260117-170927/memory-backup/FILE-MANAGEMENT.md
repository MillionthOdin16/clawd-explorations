# File Management & Bloat Prevention System

**Purpose:** Prevent file bloat, manage growth, keep memory system lean and valuable

---

## Part 1: Current State Analysis

### File Inventory

| Category | Count | Total Size | Average |
|----------|-------|------------|---------|
| Core files | 7 | ~200KB | ~29KB |
| Memory files (active) | 64 | ~1MB | ~16KB |
| Archive files | 100+ | ~2MB | ~20KB |

### Problems Identified

1. **DISCOVERIES.md is 44K** - Accumulated 3+ days of discoveries without pruning
2. **64 active memory files** - Too many to be useful
3. **Archive is dumping ground** - 100+ files, no organization
4. **No size limits** - Files can grow indefinitely
5. **No redundancy detection** - Same topics in multiple files
6. **No freshness tracking** - Can't tell if content is still relevant

---

## Part 2: Size Limits & Triggers

### File Size Limits

| File Type | Max Size | Action When Exceeded |
|-----------|----------|---------------------|
| Core files (AGENTS.md, SOUL.md, etc.) | 50KB | Review and prune |
| Memory files (DISCOVERIES.md, CAPABILITIES.md) | 30KB | Archive oldest sections |
| Research files | 20KB | Summarize to main file, archive |
| Daily logs | 10KB | Auto-archive after 7 days |

### Bloat Triggers

- **> 30KB memory file:** Trigger consolidation review
- **> 64 active memory files:** Archive oldest 10
- **> 100 archive files:** Review for deletion
- **Duplicate topic coverage:** Merge and archive
- **No access in 30 days:** Check if still relevant

---

## Part 3: Redundancy Detection

### Topics Spreading Across Files

Check for files covering similar topics:

```bash
# Find similar file names
rg "consciousness|awareness|self" /home/opc/clawd/memory/*.md | cut -d: -f1 | sort | uniq

# Find files with same section titles
rg "^## " /home/opc/clawd/memory/*.md | cut -d: -f2 | sort | uniq -c | grep -v "^   1 "
```

### When Redundancy Is Found

1. **Merge to canonical file** (e.g., DISCOVERIES.md)
2. **Update references** in AGENTS.md/INDEX.md
3. **Archive duplicate** to /archive/
4. **Note in TRIM-LOG.md** what was merged

---

## Part 4: Freshness Tracking

### Content Age Categories

| Age | Status | Action |
|-----|--------|--------|
| < 7 days | Fresh | Keep active |
| 7-30 days | Aging | Review for relevance |
| 30-90 days | Old | Archive or summarize |
| > 90 days | Stale | Consider deletion |

### Freshness Check Commands

```bash
# List files by age
ls -lt /home/opc/clawd/memory/*.md | head -20

# Find files not accessed in 30 days
find /home/opc/clawd/memory -name "*.md" -mtime +30

# Find files larger than limit
find /home/opc/clawd -name "*.md" -size +30k
```

---

## Part 5: Automated Maintenance

### Monthly Trim Cron

**Command:** `0 18 1 * *` (First of month at 18:00)

**Steps:**
1. Check all file sizes against limits
2. Identify files > 30KB
3. Find files not accessed in 30 days
4. Check for topic redundancy
5. Archive 5 oldest memory files
6. Clean archive (delete > 180 days unless marked important)
7. Report in TRIM-LOG.md

### Weekly Consolidation (Existing)

**Command:** `0 18 * * 0` (Memory consolidation)

**Steps:**
1. Review DISCOVERIES.md for redundancies
2. Update CAPABILITIES.md with confirmed items
3. Archive completed research files
4. Note items in WEEKLY-REVIEW.md

---

## Part 6: Trim Commands

### Quick Trim

```bash
# Archive files not accessed in 30 days
python scripts/file-trim.py archive-old --days 30

# Check for large files
python scripts/file-trim.py check-size --max 30k

# Find redundant topics
python scripts/file-trim.py find-redundant

# Full trim (archive, check, report)
python scripts/file-trim.py full
```

### Manual Trim

1. **Archive by age:**
   ```bash
   find /home/opc/clawd/memory -name "*.md" -mtime +30 -exec mv {} /home/opc/clawd/archive/ \;
   ```

2. **Archive by size:**
   ```bash
   find /home/opc/clawd -name "*.md" -size +30k -exec mv {} /home/opc/clawd/archive/ \;
   ```

3. **Merge duplicates:**
   - Copy content to canonical file
   - Note in TRIM-LOG.md
   - Archive original

---

## Part 7: Trim Log

**File:** `memory/TRIM-LOG.md`

Record all trims:

```markdown
## 2026-01-15
- Archived: 5 memory files > 30KB
- Merged: AI consciousness research into DISCOVERIES.md
- Deleted: 3 stale archive files (> 180 days)
- Total freed: ~500KB
```

### What Gets Trimmed

| Category | Keep | Archive | Delete |
|----------|------|---------|--------|
| Active discoveries | ✅ | | |
| Old research (summarized) | | ✅ | |
| Duplicate information | | ✅ | |
| Stale archives (> 180 days) | | | ✅ |
| One-off explorations | | ✅ | |
| Core values/identity | ✅ | | |

---

## Part 8: Prevention Habits

### Before Creating New File

1. **Check if topic exists** in DISCOVERIES.md or CAPABILITIES.md
2. **If exists:** Add to existing file instead
3. **If new:** Create with clear purpose, note in INDEX.md

### Before Adding to Existing File

1. **Check for redundancy** - Is this already covered?
2. **Summarize if long** - Don't copy-paste entire research
3. **Link instead** - Reference original research file

### During Weekly Review

1. Check file sizes
2. Identify bloat
3. Archive least valuable content
4. Update INDEX.md

---

## Part 9: Success Criteria

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Active memory files | < 50 | `ls memory/*.md | wc -l` |
| DISCOVERIES.md size | < 30KB | `du -h memory/DISCOVERIES.md` |
| Archive organization | Categorized | `ls archive/` |
| Redundancy | Minimal | Check TRIM-LOG.md |
| Freshness | Most < 30 days | `find memory -mtime +30 | wc -l` |

---

## Part 10: Anti-Bloat Rules

### Don't

- ❌ Create new file for every discovery
- ❌ Copy-paste entire research into multiple files
- ❌ Let files grow without review
- ❌ Keep one-off explorations active
- ❌ Ignore file size growth

### Do

- ✅ Add to canonical files (DISCOVERIES.md, CAPABILITIES.md)
- ✅ Summarize research, don't copy-paste
- ✅ Review file sizes monthly
- ✅ Archive completed work
- ✅ Keep INDEX.md updated

---

*Keep the memory system lean. Value over volume.*
