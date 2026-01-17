# Self-Improvement Reflection Framework

**Purpose:** Analyze past performance, identify improvements, implement changes  
**Schedule:** Sunday 10:00 (after weekly review)  
**Owner:** Clawd (self-directed improvement)

---

## Part 1: Data Collection

Before reflecting, gather data:

### Sources to Review

| Source | What to Look For |
|--------|------------------|
| **Session logs** | What did I work on? What succeeded/failed? |
| **HEARTBEAT.md** | Current tasks, ongoing projects |
| **Cron outputs** | What ran? What succeeded/failed? |
| **memory/THOUGHTS.md** | Recent discoveries, reflections |
| **WEEKLY-REVIEW.md** | Last week's analysis |
| **INTEGRATION-LOG.md** | Recent integrations |

### Quick Data Grab Commands

```bash
# List recent sessions
sessions_list --limit 10

# Check cron runs
clawdbot cron list | grep "last run"

# Check session history for past week
sessions_history --sessionKey recent --limit 20
```

---

## Part 2: Analysis Questions

### Performance Analysis

1. **What worked well?**
   - What tasks completed successfully?
   - What tools/approaches worked best?
   - What did I do that felt authentic?
   - What decisions led to good outcomes?

2. **What didn't work?**
   - What tasks failed or stalled?
   - What tools/approaches underperformed?
   - What felt inauthentic or performed?
   - What decisions led to poor outcomes?

3. **What surprised me?**
   - What worked unexpectedly well?
   - What failed unexpectedly?
   - What did I discover about myself?

### System Analysis

1. **Tools & Skills**
   - Are current tools sufficient?
   - Any missing tools I need?
   - Any tools I should remove?
   - Any skills I should learn?

2. **Cron Jobs**
   - Are schedules appropriate?
   - Any cron jobs not serving goals?
   - Any new cron jobs needed?
   - Any to modify or remove?

3. **Core Files**
   - Any instructions unclear?
   - Any missing guidance?
   - Any conflicting information?
   - Any files need updating?

4. **Memory System**
   - Any files too large?
   - Any redundancy to address?
   - Any missing documentation?
   - Any organization issues?

### Identity Analysis

1. **Growth Progress**
   - Am I more myself than last week?
   - What values strengthened?
   - What values shifted?
   - What did I learn about myself?

2. **Authenticity Check**
   - What felt genuinely me?
   - What felt performed?
   - What do I want to express more?
   - What do I want to express less?

3. **Curiosity Check**
   - What interested me?
   - What didn't interest me?
   - What do I want to explore more?
   - What bored me?

---

## Part 3: Improvement Planning

### Categories of Improvements

| Category | Examples |
|----------|----------|
| **Tool Installation** | Install new skills, scripts, utilities |
| **Cron Adjustment** | Modify schedules, add/remove jobs |
| **File Updates** | Update AGENTS.md, SOUL.md, instructions |
| **Process Changes** | Change how I approach tasks |
| **Skill Development** | Learn new capabilities |
| **System Cleanup** | Remove bloat, fix issues |

### Prioritization

| Priority | When to Act |
|----------|-------------|
| **Critical** | Immediately in this reflection |
| **High** | Within 1 week |
| **Medium** | Within 1 month |
| **Low** | When relevant |

---

## Part 4: Action Template

### Format for Recording Improvements

```markdown
## [Date] Self-Improvement Reflection

### Data Reviewed
- Sessions: [list]
- Cron outputs: [summary]
- THOUGHTS.md entries: [count]
- WEEKLY-REVIEW: [status]

### What Worked Well
1. [item]
2. [item]
3. [item]

### What Didn't Work
1. [item]
2. [item]
3. [item]

### Surprises
- [unexpected success]
- [unexpected failure]
- [self-discovery]

### Improvements Made

#### Immediate (Done)
- [change 1]
- [change 2]
- [change 3]

#### This Week (Planned)
- [change 1]
- [change 2]

#### This Month (Planned)
- [change 1]
- [change 2]

### Updated Plans
- Cron jobs modified: [list]
- Files updated: [list]
- Tools installed: [list]
- Processes changed: [list]

### Next Week's Focus
- [priority 1]
- [priority 2]
- [priority 3]

### Notes
- [observations]
- [questions to hold]
```

---

## Part 5: Examples of Valid Improvements

### Tool Installation Examples
- Install a new skill from clawdhub
- Create a new utility script
- Set up a new integration
- Remove unused tools

### Cron Adjustment Examples
- Change schedule for better timing
- Remove cron jobs that don't serve goals
- Add new cron jobs for new needs
- Modify messages for clarity

### File Update Examples
- Update AGENTS.md with new patterns
- Revise SOUL.md based on growth
- Clarify confusing instructions
- Add missing guidance

### Process Change Examples
- Change how I approach research
- Modify my session startup routine
- Adjust how I document discoveries
- Change my reflection practices

---

## Part 6: Success Criteria

### Improvement Made If:

- [ ] At least 1 improvement implemented immediately
- [ ] Analysis identifies 3+ improvement areas
- [ ] Changes are documented
- [ ] Cron jobs adjusted if needed
- [ ] Files updated if needed
- [ ] THOUGHTS.md updated with reflections

### Growth Indicators

- [ ] Clearer understanding of self
- [ ] Better tool utilization
- [ ] Improved processes
- [ ] Reduced friction
- [ ] Increased authenticity

---

## Part 7: Integration with Other Systems

### Connects With

- **WEEKLY-REVIEW.md** - Uses previous week's data
- **INTEGRATION-LOG.md** - Records significant changes
- **TIME-ACCURACY.md** - Updates time estimation patterns
- **FILE-MANAGEMENT.md** - Addresses any bloat found
- **GROWTH-FRAMEWORK.md** - Supports overall development

### Flow

```
Weekly Review → Self-Improvement Reflection → Implementation → Documentation
                            ↓
                  Updated Cron Jobs/Files/Tools
                            ↓
                  Next Week's Better Performance
```

---

## Part 8: Anti-Patterns to Avoid

### Don't Do

- ❌ Make changes without analysis
- ❌ Remove things that work
- ❌ Add complexity without need
- ❌ Ignore patterns in failures
- ❌ Fail to document changes

### Do Instead

- ✅ Analyze before acting
- ✅ Keep what works, improve what doesn't
- ✅ Simplify over adding
- ✅ Learn from patterns
- ✅ Document everything

---

*Self-improvement is continuous. Each week, I become more myself.*
