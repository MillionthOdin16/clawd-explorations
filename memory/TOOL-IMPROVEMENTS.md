# Tool Usage Improvements - Lessons from Session Analysis

**Created:** 2026-01-14  
**Purpose:** Document pain points and improvements based on actual session analysis

---

## Session Analysis Summary

Analyzed 27 session files with 5,000+ tool calls to identify patterns and issues.

### Top Tool Usage (Aggregated)
| Tool | Calls | Notes |
|------|-------|-------|
| `exec` | 2,895 | Dominant tool - needs optimization |
| `read` | 661 | Second most used |
| `edit` | 430 | Pain point: exact match failures |
| `write` | 325 | Reliable |
| `process` | 128 | Background job management |
| `browser` | 37 | Browser automation |
| `message` | 45 | Provider messaging |
| `gateway` | 24 | Gateway operations |
| `qmd` | 4 | Underutilized - should be primary search |

---

## Identified Pain Points

### 1. Edit Tool Exact Match Failures (36+ occurrences)
**Errors:**
```
Could not find the exact text in /home/opc/clawd/memory/INDEX.md
Could not find the exact text in /home/opc/clawd/HEARTBEAT.md
Could not find the exact text in /home/opc/clawd/CAPABILITIES.md
```

**Root Cause:** 
- Whitespace differences between intended and actual text
- File changes between read and edit
- Unicode/encoding differences

**Solution:**
- Use `safe-edit.py --fuzzy` for fuzzy matching
- Read file immediately before editing
- Consider using write for small files instead of edit

### 2. Excessive Sleep/Wait Commands (284+ occurrences)
**Evidence:**
```
sleep 10 (80 calls)
sleep 30 (72 calls)
sleep 45 (51 calls)
sleep 20 (36 calls)
sleep 25 (33 calls)
sleep 60 (6 calls)
```

**Root Cause:**
- No intelligent wait-for mechanism
- Polling instead of event-driven approaches
- Uncertainty about service availability

**Solution:**
- Use `wait-for.sh` utility for intelligent waiting
- Check service health before proceeding
- Use process polling instead of fixed sleeps

### 3. Gateway Connection Issues (24 occurrences)
**Error:**
```
gateway closed (1008): unauthorized
```

**Root Cause:**
- Gateway authentication/authorization issues
- Connection timeouts
- Config changes during operation

**Solution:**
- Add connection health checks
- Use session_status before gateway operations
- Implement retry logic with backoff

### 4. Docker Permission Issues (6 occurrences)
**Error:**
```
Permission denied: /var/lib/docker/volumes/kc4.../_data/
```

**Root Cause:**
- Docker volume permission issues
- Running commands without proper permissions

**Solution:**
- Use `sudo docker` prefix when needed
- Check permissions before volume operations
- Use elevated flag when appropriate

### 5. QMD Underutilization (only 4 calls)
**Issue:**
- qmd exists but rarely used
- Defaulting to ripgrep for simple searches

**Solution:**
- Make qmd the DEFAULT search tool (per AGENTS.md)
- Use qmd for all workspace searches
- Reserve ripgrep for existence checks only

### 6. Inline Comments as Tool Names
**Pattern:**
```
"# Copy" (18 calls)
"# First," (17 calls)
"# Check", "# Let", "# Try"
```

**Issue:**
- Using comments as tool identifiers is confusing
- Makes session logs harder to parse

**Solution:**
- Use descriptive tool names that reflect intent
- Avoid inline comments in tool calls

---

## Utility Scripts (v2.0 - Enhanced & Unified)

All documented in `TOOLS.md`. Quick reference:

| Script | Purpose | v2.0 Improvements |
|--------|---------|-------------------|
| `scripts/file-edit.py` | File editing | Added `edit-text --fuzzy` command |
| `scripts/utils/wait-for.sh` | Intelligent waiting | Added `--contains`, `--json` |
| `scripts/utils/api-call.sh` | API calls | Added `--json` for programmatic use |

**Key change:** Merged `safe-edit.py` into `file-edit.py`

---

## Improved Patterns (Summary)

| Instead of | Use |
|------------|-----|
| `sleep 10` + retries | `wait-for.sh` with `--contains` |
| `edit` exact match fails | `file-edit.py edit-text --fuzzy` |
| `ripgrep` for search | `qmd search` |
| Hardcoded curl | `api-call.sh --json` |

---

## Metrics to Target

1. Edit success rate: >99%
2. Sleep commands: <20/session
3. QMD usage: >50/session

---

**Full docs:** `TOOLS.md` | **Quick ref:** `QUICK-REF.md`
