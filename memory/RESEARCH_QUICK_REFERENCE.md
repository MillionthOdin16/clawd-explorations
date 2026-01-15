╔═══════════════════════════════════════════════════════════════════════════╗
║           🔍 V2.0 RESEARCH FRAMEWORK - QUICK REFERENCE 🔍                 ║
║                           Researcher Command Center                        ║
╚═══════════════════════════════════════════════════════════════════════════╝

## ⚡ QUICK START (30 seconds)

```bash
# When given a research task:
python scripts/research_session_hook.py "TASK DESCRIPTION"
# OR manually:
python scripts/research_loader.py "TARGET_NAME"
```

## 🎯 THE 4-PHASE WORKFLOW

```
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: GROUND TRUTH (5 min)                                           │
├─────────────────────────────────────────────────────────────────────────┤
│ □ Check internal knowledge first:                                       │
│   qmd search "TARGET" -c memory          # Past research                │
│   qmd search "TARGET" -c workspace       # Current files                │
│                                                                            │
│ □ Define MVO (Minimum Viable Output):                                   │
│   - Current position & employer [VERIFIED]                              │
│   - Educational background [VERIFIED]                                   │
│   - 3+ key projects/achievements [VERIFIED]                             │
│   - Technical skill areas [HIGH]                                        │
│   - Career trajectory [MEDIUM]                                          │
│                                                                            │
│ □ Assess complexity:                                                     │
│   technical_professional = 12 min base                                  │
│   academic = 15 min base                                                │
│   public_figure = 7 min base                                            │
│   private_individual = 20 min base                                      │
│                                                                            │
│ ADJUST: ×0.7 if previous research exists, ×0.8 if connected to known    │
└─────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: DISCOVER & MAP (5-10 min)                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ □ Parallel API sweep:                                                    │
│   curl -s "https://api.github.com/users/USERNAME"                       │
│   curl -s "https://api.semanticscholar.org/author/search?query=NAME"    │
│   curl -sL -A "Mozilla/5.0" "https://about.me/NAME"                     │
│                                                                            │
│ □ Creative exploration (pick 1-2):                                       │
│   Week 1: Email pattern (Hunter.io) + Wayback Machine                   │
│   Week 2: Podcast search + Product attribution                          │
│   Week 3: Conference mining + Collaboration network                      │
│   Week 4: Government records + Historical archives                       │
│                                                                            │
│ □ HIGH-VALUE DISCOVERY TRIGGERS (dig deeper immediately):                │
│   • Unexpected connection to known entity                                │
│   • Hidden skill/interest discovered                                     │
│   • Major project not in initial scan                                    │
│   • Contradiction in sources                                             │
│   • Personal quote/motivation signal                                     │
│   • Network of collaborators                                             │
│                                                                            │
│   → WHEN TRIGGERED: sessions_spawn for deep dive                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: SYNTHESIZE & BUILD (5 min)                                     │
├─────────────────────────────────────────────────────────────────────────┤
│ □ Pattern detection (look for):                                          │
│   - skill_progression: How skills evolved over time                     │
│   - theme_clustering: Common themes across projects                      │
│   - influence_mapping: Who influenced their work                        │
│   - timeline_anomalies: Gaps, pivots, accelerations                     │
│   - network_density: How connected they are                             │
│   - secret_projects: Unofficial/non-work projects                       │
│                                                                            │
│ □ Calculate quality scores:                                              │
│   RQS = (VERIFIED×2) + (HIGH×1) + internal(15) + patterns(15) + narr(10)│
│   Completeness = Critical Found / Critical Total × 100                  │
│   Insight Density = Unique Insights / Total Facts                        │
│                                                                            │
│ □ Construct narrative arc:                                               │
│   [HOOK] → [JOURNEY] → [PATTERNS] → [INSIGHT] → [IMPLICATION]           │
└─────────────────────────────────────────────────────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: INSIGHT & OUTPUT (5 min)                                       │
├─────────────────────────────────────────────────────────────────────────┤
□ Generate visual intelligence:
   • Skill map (ASCII diagram)
   • Network graph
   • Timeline with milestones
   
□ Build confidence dashboard:
   VERIFIED   ████████████░░░░░░░░░░  75%
   HIGH       ████████░░░░░░░░░░░░░░░  40%
   MEDIUM     █████░░░░░░░░░░░░░░░░░░  25%
   UNVERIFIED ░░░░░░░░░░░░░░░░░░░░░░░   0%

□ Publish with quality gates PASSED:
   ✅ RQS > 70
   ✅ Completeness > 60%
   ✅ Insight Density > 0.15
   ✅ Internal knowledge integrated
   ✅ Narrative arc present
   ✅ Visual element included
   ✅ Limitations acknowledged
```

## 📊 QUALITY GATES CHECKLIST

| Metric | Excellent | Good | Acceptable | Poor |
|--------|-----------|------|------------|------|
| **RQS** | >85 | 70-84 | 55-69 | <55 |
| **Completeness** | 100% | 80% | 60% | <60% |
| **Insight Density** | >0.30 | 0.20-0.30 | 0.10-0.20 | <0.10 |

## 🎨 VISUAL OUTPUT EXAMPLES

### Skill Map Template
```ascii
                         ┌─────────────┐
                         │   DOMAIN    │◄── Main expertise
                         │   AREA      │
                         └──────┬──────┘
                                │
         ┌──────────────────────┼──────────────────────┐
         │                      │                      │
         ▼                      ▼                      ▼
   ┌───────────┐          ┌──────────┐          ┌──────────┐
   │  SKILL 1  │◄─────────┤ CORE     │          │  SKILL 3 │
   │(strength) │          │ SKILL    │          │(support) │
   └───────────┘          └──────────┘          └──────────┘
         │                      │
         ▼                      ▼
   ┌───────────┐          ┌──────────┐
   │  PROJECT  │          │  CAREER  │
   │  EXAMPLES │          │  IMPACT  │
   └───────────┘          └──────────┘
```

### Timeline Template
```
2014    ████████░░░░░░░░░░░░░░░░░░░░  Early projects (IoT, Arduino)
        └─── CAN bus, Nest integration

2015    █████████████████████████████  NASA internship, StarLab robotics
        └─── HROS1 humanoid, drone controllers

2016    ████████████████████████████░  ECE 6501 Autonomous Mobile Robots
        └─── AMRGroup8, LIFX library

2017    ██████████████████████████████  Academic research, teaching
        └─── IEEE papers, grad coursework

2018    █████████████████████████████░  Capstone, advanced embedded
        └─── Final Project, LabVIEW Kobuki

2019+   ████████████████████████████░  Leidos hardware engineer
        └─── Defense sector, career trajectory
```

## 🔧 TOOL QUICK REFERENCE

| Tool | Command | When |
|------|---------|------|
| GitHub API | `curl -s "https://api.github.com/users/..."` | Always for technical |
| Semantic Scholar | `curl -s "https://api.semanticscholar.org/..."` | Always for academic |
| Exa AI | `curl -s "https://api.exa.ai/search?q=..."` | When DDG fails |
| qmd | `qmd search "TARGET" -c memory` | Phase 1 (always) |
| Research Loader | `python scripts/research_loader.py "NAME"` | Start of research |
| Session Hook | `python scripts/research_session_hook.py "TASK"` | Auto-detect research |

## 📋 RESEARCH LOG ENTRY

```markdown
## Research Log: [TARGET NAME]

**Date:** 2026-01-14
**Time Spent:** 18 minutes
**RQS Score:** 82/100 (Good)
**Completeness:** 78%
**Insight Density:** 0.28

### Internal Knowledge Used
- qmd search "TARGET" -c memory → Found previous summary
- qmd search "RELATED_COMPANY" -c memory → Company context

### Key Findings
1. [Most important finding]
2. [Second most important]
3. [Third most important]

### Patterns Detected
- skill_progression: From academic to defense
- theme_clustering: Strong robotics focus throughout

### Quality Scores
- RQS: 82 (Good)
- Completeness: 78%
- Insight Density: 0.28

### What Worked
1. GitHub API deep dive
2. Creative: Conference mining

### What Didn't Work
1. LinkedIn blocked → used company website instead

### Next Time
1. Start with internal knowledge check
2. Use parallel API sweep
```

## 🚨 EMERGENCY ABORT CRITERIA

Stop and publish if:
- ✅ Time limit reached (25 min max)
- ✅ RQS > 70 and Completeness > 60%
- ✅ No new discoveries in 5 minutes
- ⚠️ Ethical concerns arise
- ⚠️ Target is private and requests privacy

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `/home/opc/clawd/memory/RESEARCH_FRAMEWORK_V2.md` | Complete framework (read first) |
| `/home/opc/clawd/scripts/research_loader.py` | Quick loader + quality calculator |
| `/home/opc/clawd/scripts/research_session_hook.py` | Auto-detect research triggers |
| `/home/opc/clawd/AGENTS.md` | Updated with research trigger |

---

*Auto-loaded when research is detected. Manual reference: V2.0 Quick Reference Card.*
*Last updated: 2026-01-14*
