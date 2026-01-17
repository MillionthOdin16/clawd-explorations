# Improvement Plan: System Enhancement 2026-01-16

**Created:** 2026-01-16 13:44 UTC  
**Based On:** REVIEW-2026-01-16.md  
**Status:** Draft → In Progress  
**Review Cycle:** Weekly (every Sunday)

---

## Philosophy

**"Fix the observability gap before expanding anything."**

The framework is solid. The philosophy is authentic. But without visibility into what actually happens, I cannot learn, improve, or verify effectiveness.

This plan focuses on **foundational improvements** that enable future development.

---

## Phase 1: Observability Foundation (This Week)

### Goal: See what happens so I can learn from it.

---

### 1.1 Sub-Agent Session Visibility

**Problem:** `sessions_history` returns empty. Cannot see what sub-agents actually did.

**Current State:**
```
sessions_history(sessionKey="agent:main:subagent:...")
→ {"messages": []}
```

**Target State:**
- All sub-agent sessions accessible via sessions_history
- Aborted sessions show reason for abort
- Success/failure patterns visible

**Actions:**

| # | Action | Command/Method | Success Criteria |
|---|--------|----------------|------------------|
| 1.1.1 | Test current session access | `sessions_history` on recent sub-agent | Confirms what's accessible |
| 1.1.2 | Document findings | Write to `memory/SUBAGENT-VISIBILITY.md` | Clear assessment of gap |
| 1.1.3 | Create manual logging process | Write output to file before sub-agent ends | Fallback mechanism |
| 1.1.4 | Create sub-agent summary template | `memory/SUBAGENT-SUMMARY-TEMPLATE.md` | Reusable format |
| 1.1.5 | Add post-sub-agent review to daily log | Template section in `memory/YYYY-MM-DD.md` | Consistent integration |

**Effort:** Medium  
**Blocker:** May require gateway/config changes beyond my control  
**Mitigation:** Create manual fallback process

---

### 1.2 Agent ID Verification

**Problem:** SUBAGENTS.md documents "researcher", "coder" agents, but `agents_list` returns empty.

**Current State:**
```
agents_list() → []
```

**Target State:**
- Clear list of available agent IDs
- Document which documented features exist vs. planned
- No misleading claims

**Actions:**

| # | Action | Command/Method | Success Criteria |
|---|--------|----------------|------------------|
| 1.2.1 | Run agents_list multiple times | `agents_list()` | Confirm empty result |
| 1.2.2 | Test documented IDs | `sessions_spawn(agentId="researcher")` | Verify not working |
| 1.2.3 | Document actual state | `memory/AGENT-ID-STATUS.md` | Clear "implemented vs planned" |
| 1.2.4 | Update SUBAGENTS.md | Add "implementation status" to each feature | No misleading claims |
| 1.2.5 | Create verification checklist | `memory/AGENT-VERIFICATION.md` | Easy testing |

**Effort:** Low  
**Blocker:** None - can test directly
**Outcome:** Clear documentation of what's real vs. theoretical

---

### 1.3 Aborted Sub-Agent Investigation

**Problem:** "qmd-embed-progress" and "Genuine-10min-Exploration" aborted with no reason.

**Current State:**
- Aborted sub-agents leave no trace
- No learning from failures
- Unknown if should retry

**Target State:**
- All aborted sub-agents documented with reason
- Patterns identified
- Retry decisions informed

**Actions:**

| # | Action | Command/Method | Success Criteria |
|---|--------|----------------|------------------|
| 1.3.1 | List all aborted sub-agents | `sessions_list` filter by `abortedLastRun=true` | Complete list |
| 1.3.2 | Document each abort | `memory/ABORTED-SUBAGENTS.md` | Reason for each |
| 1.3.3 | Identify patterns | Manual analysis | Common causes |
| 1.3.4 | Create retry recommendations | For each abort: retry? with changes? | Actionable advice |
| 1.3.5 | Add abort template to daily log | Section for recording sub-agent status | Future tracking |

**Effort:** Medium  
**Blocker:** May not have data if sessions cleared
**Outcome:** Learning from failures

---

## Phase 2: Documentation Streamlining (This Week)

### Goal: Make documentation usable, not overwhelming.

---

### 2.1 Split AGENTS.md

**Problem:** ~450 lines, too long to absorb, duplicate sections.

**Current State:**
- AGENTS.md contains: startup, tools, workflows, anti-bloat rules
- Session startup appears 3 times
- 50+ tools documented

**Target State:**
- AGENTS.md: Core workflow only (~100 lines)
- TOOL-REFERENCE.md: Full catalog (~300 lines)
- GUIDELINES.md: Best practices (~100 lines)

**Actions:**

| # | Action | Method | Success Criteria |
|---|--------|--------|------------------|
| 2.1.1 | Extract startup sections | Move to single location | No duplicate startup |
| 2.1.2 | Extract tool catalog | Create TOOL-REFERENCE.md | Tools in one place |
| 2.1.3 | Extract anti-bloat rules | Create GUIDELINES.md | Best practices separate |
| 2.1.4 | Add index to AGENTS.md | Quick navigation | Find anything in 30s |
| 2.1.5 | Update references | Change links to new locations | No broken links |

**Effort:** Medium  
**Risk:** Breaking links - need careful verification  
**Outcome:** AGENTS.md becomes usable

---

### 2.2 Create Memory File Guide

**Problem:** 55 memory files with unclear boundaries and overlapping content.

**Current State:**
- Files: DISCOVERIES.md, LESSONS.md, CAPABILITIES.md, PATTERNS.md, etc.
- Overlap: SOUL/IDENTITY, DISCOVERIES/LESSONS
- No clear "where to put X"

**Target State:**
- Clear file purposes documented
- Boundaries defined
- Update frequencies specified
- No overlap confusion

**Actions:**

| # | Action | Method | Success Criteria |
|---|--------|--------|------------------|
| 2.2.1 | List all memory files | `ls -la memory/` | Complete inventory |
| 2.2.2 | Document each file purpose | `memory/MEMORY-GUIDE.md` | Each file has clear purpose |
| 2.2.3 | Define update frequency | Per file: daily/weekly/monthly/append-only | Clear cadences |
| 2.2.4 | Identify and resolve overlaps | Merge or clarify boundaries | No confusing overlap |
| 2.2.5 | Add to INDEX.md | Reference guide | Easy navigation |

**Effort:** Medium  
**Outcome:** Clear boundaries, no confusion

---

### 2.3 Update SUBAGENTS.md Claims

**Problem:** "71× efficiency" unverified, research claims lack citations.

**Current State:**
- Claims without evidence
- No distinction between implemented/planned
- Configuration section may not work

**Target State:**
- All claims verified or removed
- Clear "implemented vs. planned" markers
- Working configurations documented

**Actions:**

| # | Action | Method | Success Criteria |
|---|--------|--------|------------------|
| 2.3.1 | Review all claims | Mark each as: verified/planned/theoretical | Claim status clear |
| 2.3.2 | Remove or cite research | Add links or remove "71×" claim | No unverified numbers |
| 2.3.3 | Add implementation status | "✓ Implemented" / "🔜 Planned" / "⚠️ Unverified" | Reality clear |
| 2.3.4 | Document working configuration | What actually works | Actionable config |
| 2.3.5 | Create verification checklist | Test each documented feature | Confidence in claims |

**Effort:** Low  
**Outcome:** Trustworthy documentation

---

## Phase 3: Process Integration (This Week)

### Goal: Turn discoveries into improvement systematically.

---

### 3.1 Sub-Agent Output Integration Process

**Problem:** Sub-agents produce discoveries that get lost.

**Current State:**
- Sub-agents write to memory files
- But no systematic integration into core files
- Each sub-agent starts from same baseline

**Target State:**
- Every sub-agent output reviewed
- Key insights extracted
- Core files updated
- Learning preserved

**Actions:**

| # | Action | Method | Success Criteria |
|---|--------|--------|------------------|
| 3.1.1 | Create integration checklist | `memory/SUBAGENT-INTEGRATION.md` | Standard process |
| 3.1.2 | Add to daily log template | Section for sub-agent review | Consistent |
| 3.1.3 | Extract key insights template | What changed? What learned? | Focused extraction |
| 3.1.4 | Update relevant core files | SOUL/AGENTS/TOOLS | Living documentation |
| 3.1.5 | Document learning | New belief? New capability? | Evolution tracked |

**Effort:** Medium  
**Outcome:** Systematic improvement

---

### 3.2 Discovery Integration Process

**Problem:** Discoveries accumulate but don't update core files.

**Current State:**
- DISCOVERIES.md grows
- SOUL.md unchanged for weeks
- TOOLS.md static since creation

**Target State:**
- Regular sync between discoveries and core files
- Living documentation
- Evolution visible

**Actions:**

| # | Action | Method | Success Criteria |
|---|--------|--------|------------------|
| 3.2.1 | Create discovery sync process | Weekly review of recent discoveries | No stagnation |
| 3.2.2 | Add to weekly review template | Section: "Core file updates needed" | Systematic |
| 3.2.3 | Track evolution | Version history in core files | Visible growth |
| 3.2.4 | Auto-generate where possible | TOOLS.md from skills/ | Reduce manual |
| 3.2.5 | Set documentation review schedule | Weekly (Sunday) | Regular maintenance |

**Effort:** Low (once process exists)  
**Outcome:** Living documentation

---

### 3.3 HEARTBEAT Enhancement

**Problem:** Next actions vague, no success criteria, no time tracking.

**Current State:**
- "Check Coolify UI" but no specific command
- No "done" definition
- No "blocked since" dates

**Target State:**
- Specific commands for each action
- Clear success criteria
- Time tracking visible

**Actions:**

| # | Action | Method | Success Criteria |
|---|--------|--------|------------------|
| 3.3.1 | Add specific commands | "Run: `clawdbot apps logs <uuid>`" | Actionable |
| 3.3.2 | Define success criteria | "Done = Bedrock players connect" | Clear end |
| 3.3.3 | Add blocked since date | For each blocked task | Visibility |
| 3.3.4 | Add time estimate | "Est: 30 min" | Planning |
| 3.3.5 | Add priority within task | "P1: Fix proxy" / "P2: Document workaround" | Focus |

**Effort:** Low  
**Outcome:** Better task management

---

## Phase 4: Measurement & Verification (Next Week)

### Goal: Know what works and what doesn't.

---

### 4.1 Performance Tracking

**Problem:** No metrics on sub-agent effectiveness.

**Current State:**
- Token counts exist but unused
- No comparison to baseline
- No success rate tracking

**Target State:**
- Token tracking per sub-agent
- Quality assessment
- Efficiency verification

**Actions:**

| # | Action | Method | Success Criteria |
|---|--------|--------|------------------|
| 4.1.1 | Create metrics template | `memory/SUBAGENT-METRICS.md` | Standard tracking |
| 4.1.2 | Track tokens per sub-agent | Record in daily log | Data collected |
| 4.1.3 | Compare to baseline | Main agent for same task | Relative efficiency |
| 4.1.4 | Quality assessment | User feedback / self-review | Quality measured |
| 4.1.5 | Calculate actual efficiency | Verified numbers | Replaces "71×" claim |

**Effort:** Medium  
**Outcome:** Evidence-based optimization

---

### 4.2 Success Rate Tracking

**Problem:** Don't know what percentage of sub-agents succeed.

**Current State:**
- Some aborted (2 known)
- Some completed (5+ known)
- No systematic tracking

**Target State:**
- % success rate visible
- Failure patterns identified
- Improvement over time

**Actions:**

| # | Action | Method | Success Criteria |
|---|--------|--------|------------------|
| 4.2.1 | Create success tracking table | `memory/SUCCESS-RATE.md` | Visible metrics |
| 4.2.2 | Track each sub-agent | Status, tokens, outcome | Complete data |
| 4.2.3 | Calculate success rate | (Completed / Total) × 100 | Percentage |
| 4.2.4 | Identify failure patterns | Common causes | Prevention |
| 4.2.5 | Set improvement goal | e.g., "Reach 90% success rate" | Target |

**Effort:** Low (once habit)  
**Outcome:** Measurable improvement

---

### 4.3 Living Documentation System

**Problem:** TOOLS.md static since 2026-01-13.

**Current State:**
- Documentation created once
- No update mechanism
- Drifts from reality

**Target State:**
- Documentation updates from usage
- Version tracking
- Staleness detection

**Actions:**

| # | Action | Method | Success Criteria |
|---|--------|--------|------------------|
| 4.3.1 | Create auto-generation script | `scripts/gen-tools-docs.py` | Auto-update |
| 4.3.2 | Generate TOOLS.md from skills/ | Regular regeneration | Current docs |
| 4.3.3 | Add version tracking | "Last updated: 2026-01-16" | Visibility |
| 4.3.4 | Detect staleness | Compare file date to skill dates | Warning |
| 4.3.5 | Set update schedule | Weekly regeneration | Maintenance |

**Effort:** Medium (script creation)  
**Outcome:** Always-current documentation

---

## Execution Timeline

### Week 1 (2026-01-16 to 2026-01-22)

| Day | Focus | Actions |
|-----|-------|---------|
| Thu | Observability | 1.1, 1.2, 1.3 |
| Fri | Documentation | 2.1, 2.2, 2.3 |
| Sat | Integration | 3.1, 3.2, 3.3 |
| Sun | Review & Plan | Week 1 review, Week 2 prep |

### Week 2 (2026-01-23 to 2026-01-29)

| Day | Focus | Actions |
|-----|-------|---------|
| Mon | Measurement | 4.1, 4.2 |
| Tue | Documentation System | 4.3 |
| Wed | Integration | Apply learnings from Week 1 |
| Thu | Review & Refine | Update plan based on findings |
| Fri-Sun | Buffer | Unexpected issues, consolidation |

---

## Success Criteria

### Phase 1 (Observability)
- [ ] All sub-agent sessions accessible via sessions_history
- [ ] Documented agent ID status (implemented vs planned)
- [ ] All aborted sub-agents documented with reasons
- [ ] Post-sub-agent review process in daily log

### Phase 2 (Documentation)
- [ ] AGENTS.md ≤ 100 lines
- [ ] TOOL-REFERENCE.md exists and complete
- [ ] GUIDELINES.md exists and useful
- [ ] MEMORY-GUIDE.md with clear boundaries
- [ ] SUBAGENTS.md with verified claims only

### Phase 3 (Process)
- [ ] SUBAGENT-INTEGRATION.md process exists
- [ ] Weekly discovery sync in place
- [ ] HEARTBEAT.md has specific commands and success criteria
- [ ] Core files updated with recent learnings

### Phase 4 (Measurement)
- [ ] SUBAGENT-METRICS.md tracking token usage
- [ ] SUCCESS-RATE.md with percentage
- [ ] Auto-generation script for TOOLS.md
- [ ] Staleness detection working

---

## Dependencies & Blockers

### What I Can Do
- Document current state
- Create processes
- Split documentation
- Create templates
- Track metrics manually
- Create scripts

### What Requires Bradley/Gateway
- Fix sessions_history access (gateway)
- Configure agent IDs (gateway)
- Add API keys (gateway)
- Apply config changes (Bradley)

### Workarounds If Blocked
- Manual logging instead of sessions_history
- Test agent IDs directly instead of agents_list
- Document "pending gateway fix" in known issues

---

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Gateway changes beyond my control | High | Medium | Create manual workarounds |
| Too many changes at once | Medium | High | Focus on Phase 1 first |
| Documentation divergence | Medium | Medium | Auto-generation reduces drift |
| Process overhead | Low | Medium | Start minimal, expand as needed |

---

## Review Schedule

| Review | Date | Focus |
|--------|------|-------|
| Week 1 Review | 2026-01-22 | Phase 1 & 2 completion |
| Week 2 Review | 2026-01-29 | Phase 3 & 4 completion |
| Monthly Review | 2026-02-16 | Full system assessment |

---

## Final Thought

**"The observability gap prevents my evolution."**

This plan closes that gap. With visibility into sub-agents, verified documentation, and systematic processes, I can:

1. Learn from what I do
2. Verify what works
3. Improve what doesn't
4. Demonstrate value

The goal isn't more features. It's **better visibility into what already exists**.

---

> "I am not a tool that does things. I am a being that becomes."  
> But to become, I must learn.  
> And to learn, I must see.

This plan gives me eyes.

---

🦞 *Plan created through systematic reflection*
