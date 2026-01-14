# Session Analysis & Tool Improvements Summary

**Date:** 2026-01-14  
**Analyst:** Clawd (analyzed own session history)

---

## Executive Summary

Analyzed 27 session files with 5,000+ tool calls to identify pain points and create improvements.

### Key Findings
- **2,895** `exec` calls (dominant tool)
- **284+** sleep commands (workarounds for timing issues)
- **36+** edit tool exact-match failures
- **4** qmd calls (should be primary search tool)

---

## Pain Points Identified & Solutions

### 1. Edit Tool Exact Match Failures (36+ occurrences)

**Error Pattern:**
```
Could not find the exact text in /home/opc/clawd/memory/INDEX.md
Could not find the exact text in /home/opc/clawd/HEARTBEAT.md
```

**Solution:** Created `scripts/utils/safe-edit.py` with fuzzy matching
```bash
python scripts/utils/safe-edit.py path "old text" "new text" --fuzzy
```

### 2. Excessive Sleep Commands (284+ occurrences)

**Evidence:**
- `sleep 10` (80 calls)
- `sleep 30` (72 calls)
- `sleep 45` (51 calls)
- `sleep 20` (36 calls)

**Solution:** Created `scripts/utils/wait-for.sh` for intelligent waiting
```bash
./wait-for.sh http://localhost:3000 --timeout 30
./wait-for.sh port:3000 --timeout 30
./wait-for.sh docker:container --timeout 60
```

### 3. Gateway Connection Issues (24 occurrences)

**Error:** `gateway closed (1008): unauthorized`

**Solution:** Add health checks before gateway operations (documented in TOOL-IMPROVEMENTS.md)

### 4. Docker Permission Issues (6 occurrences)

**Error:** `Permission denied: /var/lib/docker/volumes/...`

**Solution:** Use `sudo docker` prefix when needed

### 5. QMD Underutilization (only 4 calls)

**Issue:** qmd exists but rarely used for search

**Solution:** Updated qmd SKILL.md to emphasize "PRIMARY SEARCH TOOL"

---

## Files Created/Modified

### New Files
| File | Purpose |
|------|---------|
| `scripts/utils/safe-edit.py` | Fuzzy text matching for edits |
| `scripts/utils/wait-for.sh` | Intelligent service waiting |
| `scripts/utils/api-call.sh` | Standardized API calls |
| `memory/TOOL-IMPROVEMENTS.md` | Full analysis and patterns |
| `QUICK-REF.md` | Quick lookup card |

### Modified Files
| File | Change |
|------|--------|
| `TOOLS.md` | Added utility scripts section + lessons learned |
| `AGENTS.md` | Added utility script references |
| `skills/qmd/SKILL.md` | Emphasized PRIMARY status |

---

## Tool Usage Rankings (Actual Data)

| Rank | Tool | Calls | Action |
|------|------|-------|--------|
| 1 | `exec` | 2,895 | Primary - optimize with utilities |
| 2 | `read` | 661 | Use partial reads with --start/--end |
| 3 | `bash` | 532 | Script wrapping |
| 4 | `edit` | 430 | Use `safe-edit.py` for fuzzy |
| 5 | `write` | 325 | Reliable for small files |
| 6 | `process` | 128 | Background job management |
| 7 | `message` | 45 | Provider messaging |
| 8 | `browser` | 37 | Browser automation |
| 9 | `gateway` | 24 | Add health checks |
| 10 | `qmd` | 4 | **PRIMARY SEARCH - use more!** |

---

## Before/After Patterns

### Edit Operations

**BEFORE:**
```
edit path "exact text that might not match"
→ Error: Could not find the exact text
```

**AFTER:**
```
exec "python scripts/utils/safe-edit.py path 'text' 'new text' --fuzzy"
→ Success: Fuzzy match edit successful at line X
```

### Service Waiting

**BEFORE:**
```
sleep 10
curl http://localhost:3000/api/chat || sleep 10
curl http://localhost:3000/api/chat || sleep 10
curl http://localhost:3000/api/chat
→ 3 sleep 10 calls = 30 seconds fixed wait
```

**AFTER:**
```
./wait-for.sh http://localhost:3000/api/chat --timeout 30
→ Intelligent wait, exits immediately when ready
```

### Search Operations

**BEFORE:**
```
ripgrep "pattern" /home/opc/clawd
→ Raw text matching, no context
```

**AFTER:**
```
qmd search "pattern" -c workspace
→ Semantic search with context, reranking
```

---

## Metrics to Track

After implementing these improvements, monitor:

| Metric | Baseline | Target |
|--------|----------|--------|
| Edit success rate | ~90% | >99% |
| Sleep command count | 284/session | <20/session |
| QMD usage | 4/session | >50/session |
| Exact match errors | 36+ | 0 |

---

## Recommendations

1. **Make qmd the default** - Train to use qmd first for all searches
2. **Use utility scripts** - Add to workflow patterns
3. **Eliminate sleep loops** - Replace with `wait-for.sh`
4. **Handle edit gracefully** - Use `safe-edit.py` for fuzzy matching
5. **Add health checks** - Before gateway/docker operations

---

## References

- Session logs: `/home/opc/.clawdbot/agents/main/sessions/`
- Full analysis: `memory/TOOL-IMPROVEMENTS.md`
- Quick reference: `QUICK-REF.md`
- Tool docs: `TOOLS.md`
