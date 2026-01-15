# Time Accuracy Tracking

**Purpose:** Track estimated vs. actual time, measure improvement over time

---

## How to Use

1. After any time-bound task, run: `./time-track.py end task-name estimated-minutes`
2. Review accuracy: `./time-track.py report`
3. Update this file with patterns noticed

---

## Accuracy Goal

**Target Ratio:** 0.8-1.2 (within 20% of estimate)

| Ratio | Quality |
|-------|---------|
| 0.8-1.2 | 🎯 Excellent |
| 0.5-1.5 | ⚠️ Fair |
| < 0.5 or > 1.5 | ❌ Poor |

---

## Recent Records

*(Auto-populated from time-track.py history)*

```bash
./time-track.py history  # View all records
./time-track.py report   # View accuracy report
```

---

## Patterns Identified

### Tasks That Typically Take Longer Than Estimated

| Task Type | Typical Ratio | Notes |
|-----------|---------------|-------|
| Quick research | ~2.4 | Underestimate by 2x |
| Write document | ~1.5 | Underestimate by 50% |

### Tasks That Typically Match Estimates

| Task Type | Typical Ratio | Notes |
|-----------|---------------|-------|
| Simple file read | ~1.0 | Good estimate |
| Tool execution | Depends | Variable |

---

## Calibration Guidelines

### How to Improve Estimates

1. **Measure everything** - Don't estimate without data
2. **Track patterns** - Notice common under/over estimates
3. **Add buffer** - For uncertain tasks, multiply estimate by 1.5
4. **Break tasks** - Smaller tasks = more accurate estimates

### Quick Reference

| Task Type | Suggested Estimate |
|-----------|-------------------|
| Quick research | 15 min (not 5 min) |
| Write document | 45 min (not 30 min) |
| Explore topic | 30 min (not 15 min) |
| Read 100 lines | 5 min |
| Fix simple bug | 20 min |
| Complex feature | 60+ min |

---

## Weekly Review Check

**Every Sunday:**

- [ ] Run `./time-track.py report`
- [ ] Review accuracy ratio
- [ ] Identify any patterns
- [ ] Update calibration guidelines
- [ ] Note in WEEKLY-REVIEW.md

---

## Historical Summary

*(To be populated over time)*

### Week 1 (2026-01-15)
- Total records: 0
- Average ratio: N/A
- Focus: Establish baseline

---

*Time is data. Measure it.*
