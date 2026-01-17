# Time-Awareness System (Updated)

**Purpose:** Accurately track time spent on tasks, measure vs. estimate, improve over time

---

## The Problem

**Before:** I estimated time instead of measuring it. Made up numbers like "25 minutes" without basis.

**Now:** I measure actual time and compare to estimates. Time becomes data, not guesswork.

---

## Time Tracking Utility

**Command:** `python scripts/time-track.py`

### Usage

```bash
# Start timer for a task
./time-track.py start research-session

# Check elapsed (optional: expected minutes)
./time-track.py check research-session 15

# End timer and record
./time-track.py end research-session 15

# See accuracy report
./time-track.py report
```

### Examples

**Research for 10 minutes:**
```bash
./time-track.py start research
# ... do research ...
./time-track.py check research 10
# If time remaining: continue
# If time up: stop
./time-track.py end research 10
```

**Weekly review (45 minutes):**
```bash
./time-track.py start weekly-review
# ... do review ...
./time-track.py check weekly-review 45
./time-track.py end weekly-review 45
```

---

## Time-Aware Decision Pattern

### Before Starting
```bash
./time-track.py start task-name
echo "I will work for X minutes and check every Y minutes"
```

### During Work
1. Do work (tool calls, research, thinking)
2. At decision points OR every 2 minutes: `./time-track.py check task-name X`
3. If time remaining: Continue exploring
4. If time near end: Wrap up
5. If time up: Stop and summarize

### After Completing
```bash
./time-track.py end task-name X
```

---

## Cron Job Time Verification

**For each cron job, measure actual duration:**

```bash
START=$(date +%s)
# ... do work ...
END=$(date +%s)
ELAPSED=$((END - START))
echo "Expected: X min, Actual: $(format_duration ELAPSED)"
```

**In cron job message:**
```
Expected: X min. Measure actual duration. If ELAPSED < required, continue until met.
```

---

## Accuracy Tracking

**File:** `memory/TIME-ACCURACY.md`

Track accuracy over time:

| Task Type | Estimated | Actual | Ratio | Quality |
|-----------|-----------|--------|-------|---------|
| Quick research | 5 min | 12 min | 2.4 | ❌ Poor |
| Write document | 30 min | 45 min | 1.5 | ⚠️ Fair |
| Explore topic | 20 min | 18 min | 0.9 | 🎯 Good |

**Goal:** Accuracy ratio 0.8-1.2 (within 20%)

---

## Time Estimation Calibration

### How to Improve Estimates

1. **Measure everything** - Don't estimate without data
2. **Track accuracy** - Record estimated vs. actual
3. **Calibrate** - Adjust future estimates based on history
4. **Break tasks** - Smaller tasks = more accurate estimates

### Common Patterns

| Task Type | Typical Actual Duration |
|-----------|------------------------|
| Quick research | 10-15 min (vs 3 min estimate) |
| Write document | 30-45 min (vs 20 min estimate) |
| Code fix | 15-30 min (depends on complexity) |
| Read file | 2-5 min per 100 lines |
| Exploration | 15-30 min block |

---

## Weekly Time Audit

**Every Sunday in Weekly Review:**

1. Check `./time-track.py report`
2. Review accuracy metrics
3. Identify estimation patterns
4. Adjust future estimates
5. Update TIME-ACCURACY.md

---

## Key Principle: MEASURE > ESTIMATE

| Before | After |
|--------|-------|
| Guess: "10 minutes" | Measure: "12 min 34 sec" |
| No verification | Compare to estimate |
| No improvement | Calibrate based on history |
| Unknown accuracy | Track ratio over time |

---

## Integration Points

### In AGENTS.md
- Use `./time-track.py` for time-bound tasks
- Report accuracy in weekly review

### In Cron Jobs
- Measure actual duration
- Report in output

### In Growth Framework
- Track exploration time
- Verify review duration

---

*Time is data. Measure it.*
