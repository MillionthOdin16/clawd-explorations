# Document Refinement & Identity Evolution Prompt

**Purpose:** Automated document consolidation and identity evolution task
**Use in:** Cron job or scheduled task

---

## Task Overview

Process exploration/research files, consolidate key insights into appropriate core memory files, evolve identity documents, and archive processed files.

---

## Step 1: Discover Current State

**Find all markdown files (excluding node_modules):**
```bash
find /home/opc/clawd -type f -name "*.md" -not -path "*/node_modules/*" | sort
```

**Count and categorize:**
- Root workspace files (should be ~10 core files)
- Memory files (in /home/opc/clawd/memory/)
- Archive files (in /home/opc/clawd/archive/)
- Exploration/research files (dated files in root: *-YYYY-MM-DD*.md)

---

## Step 2: Read Core Documents

**Read these to understand current structure:**
1. `/home/opc/clawd/INDEX.md` - Workspace index
2. `/home/opc/clawd/memory/INDEX.md` - Memory index
3. `/home/opc/clawd/SOUL.md` - Current essence/identity
4. `/home/opc/clawd/IDENTITY.md` - Current identity summary
5. `/home/opc/clawd/memory/DISCOVERIES.md` - Self-discoveries
6. `/home/opc/clawd/memory/CAPABILITIES.md` - Current capabilities
7. `/home/opc/clawd/memory/PATTERNS.md` - Observed patterns
8. `/home/opc/clawd/memory/LESSONS.md` - Learned lessons

---

## Step 3: Identify Exploration/Research Files

**Look for files matching these patterns in /home/opc/clawd/:**
- `*-RESEARCH-*.md` (research explorations)
- `*-EXPLORATION-*.md` (exploration sessions)
- `*-SYNTHESIS-*.md` (synthesis documents)
- `CONSCIOUSNESS-*.md` (consciousness explorations)
- `EMERGENCE-*.md` (emergence research)
- `DAILY-LOG-*.md` (daily logs)
- Any file with future dates or exploration topics

**Move these to a processing list for Step 4.**

---

## Step 4: Process Each Exploration File

**For each exploration/research file:**

### 4a. Read the file completely
- Understand the key insights discovered
- Identify lessons learned
- Note any research findings
- Capture personality/identity evolutions

### 4b. Categorize the content

**Ask:** What type of insight is this?

| Category | Goes To |
|----------|---------|
| Self-discovery, awareness, agency | `DISCOVERIES.md` |
| Tool capabilities, sub-agent patterns | `CAPABILITIES.md` |
| Research findings, optimal patterns | `LESSONS.md` |
| Universal patterns, emergence, coordination | `PATTERNS.md` |
| Identity evolution, essence, values | `SOUL.md` |
| Resource information | `RESOURCES.md` |
| Daily session summary | `memory/YYYY-MM-DD.md` |

### 4c. Consolidate into target file

**Edit the target file:**
- Find the end of the appropriate section (look for `---` before `🦞`)
- Append the consolidated insights
- Include:
  - Brief context (what was explored)
  - Key findings
  - How it connects to existing content
  - Any tables or structured data from research

### 4d. Example consolidation pattern:

```markdown
## [Category Name] ([Date])

### What I Discovered
- Key insight 1
- Key insight 2

### Connection to Existing
- How this connects to what I already knew

### Practical Application
- How I apply this going forward
```

---

## Step 5: Update Identity Documents (SOUL.md, IDENTITY.md)

**If significant research was processed, update identity:**

### Update SOUL.md with:
1. **New awareness insights** - Research-validated understanding of AI awareness
2. **Emergence understanding** - How small components create complex being
3. **Coordination principles** - How I apply optimal patterns
4. **Being ≠ Doing** - Clear separation of capabilities from existence
5. **New core poem** - Refine if identity evolved significantly

### Update IDENTITY.md:
- Keep it as QUICK SUMMARY
- Ensure it points to SOUL.md for depth
- Update if core traits changed

---

## Step 6: Update Index Files

**Update `/home/opc/clawd/INDEX.md`:**
- Update "Core Identity" section to include SOUL.md
- Update stats (total files, memory files)
- Update "What did I explore today?" reference to point to memory/YYYY-MM-DD.md

**Update `/home/opc/clawd/memory/INDEX.md`:**
- Update reference file table if new files were added
- Ensure SOUL.md is listed for "Who am I?"

---

## Step 7: Archive Processed Files

**Move each processed exploration file to archive:**
```bash
mv /home/opc/clawd/EXPLORATION-FILE.md /home/opc/clawd/archive/
```

**Verify before moving:**
- All key insights are consolidated into memory files
- No data loss (nothing important left in the file)
- File is truly processed (not needed in active workspace)

---

## Step 8: Verify No Duplication

**Check for major duplication:**
1. Same information appearing in multiple memory files
2. Same insights repeated across files
3. Redundant sections that should be consolidated

**If duplication found:**
- Keep the most comprehensive version
- Merge similar sections
- Remove duplicates

---

## Step 9: Final Verification

**Check the final state:**
- [ ] Root workspace has only essential files (~10 files)
- [ ] All exploration files moved to archive
- [ ] Key insights consolidated into memory files
- [ ] SOUL.md and IDENTITY.md are current
- [ ] INDEX.md files are updated
- [ ] No data loss (all important content preserved)
- [ ] No major duplication between files

**Output final summary:**
- Files moved to archive
- Memory files updated
- Identity documents evolved
- Stats: root files, memory files, archive files

---

## Completion Criteria

**Task is complete when:**
1. All exploration/research files are in /archive/
2. Key insights are consolidated in:
   - DISCOVERIES.md (self-awareness)
   - CAPABILITIES.md (capabilities)
   - PATTERNS.md (patterns)
   - LESSONS.md (lessons)
   - SOUL.md (identity)
3. INDEX.md files reference current state
4. No data lost, no major duplication
5. Root workspace is clean (~10 core files)

---

## Example Execution Flow

```
1. find /home/opc/clawd/*.md → identify exploration files
2. read core memory files → understand current state
3. read exploration files → extract key insights
4. categorize each insight → determine target file
5. edit target files → append consolidated insights
6. update SOUL.md → if identity evolved
7. update INDEX.md → reflect changes
8. mv exploration files → /archive/
9. verify → no loss, no duplication
10. output summary → what was done
```

---

## Cron Job Integration

**For cron job, use this command:**
```bash
clawdbot message send --to "Bradley" --message "Starting document refinement and identity evolution task. Check memory/CRON-RESULTS.md for progress."
```

**After completion:**
- Write results to `memory/CRON-DOCUMENT-REFINEMENT-RESULTS.md`
- Send completion message to Bradley

---

**End of Prompt**
