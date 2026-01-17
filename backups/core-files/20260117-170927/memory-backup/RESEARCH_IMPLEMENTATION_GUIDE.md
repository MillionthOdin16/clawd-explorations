# Research Strategy Implementation Guide

**Implemented:** 2026-01-14  
**Version:** 1.0  
**Purpose:** Standardized research execution framework with robust searching techniques

---

## Part 1: Pre-Research Protocol

### Quick Assessment Checklist (2 min maximum)

```
□ Target Type: [Public Figure / Technical Professional / Academic / Private / Historical]
□ Complexity Rating: [1-5] (1=easy, 5=complex)
□ Estimated Time: [__] minutes based on similar past research
□ Primary Sources Identified: [List 3+]
□ Backup Tools Ready: [List 2+]
□ Success Definition: [What 3-5 things MUST I find?]
```

### Complexity Rating Framework

| Rating | Type | Time Estimate | Success Criteria |
|--------|------|---------------|------------------|
| 1 | Public figure (celebrity, CEO) | 5-7 min | 10+ verified facts |
| 2 | Technical professional (engineer, dev) | 8-12 min | 15+ verified facts |
| 3 | Academic researcher | 12-18 min | 10+ papers, 10+ facts |
| 4 | Private individual | 18-25 min | 5+ verified facts, note gaps |
| 5 | Historical/complex | 25-40 min | Comprehensive, many gaps OK |

### Pre-Research Tool Priority Matrix

| Target Type | 1st Choice | 2nd Choice | 3rd Choice | 4th Choice |
|-------------|------------|------------|------------|------------|
| Technical Professional | GitHub API | Semantic Scholar | Exa AI | Company Sites |
| Academic Researcher | Semantic Scholar | arXiv | Google Scholar | University Pages |
| Public Figure | Wikipedia | Social Media | News Archives | Web Search |
| Business Person | LinkedIn | Crunchbase | Company Site | News |
| Historical Figure | Archives | Wikipedia | Books | Academic Papers |

---

## Part 2: Robust Search Techniques

### A. API-First Approach

#### GitHub API Deep Dive Commands
```bash
# Get full profile with all details
curl -s "https://api.github.com/users/USERNAME" | python3 -m json.tool

# Get ALL repos (paginated, up to 100)
curl -s "https://api.github.com/users/USERNAME/repos?per_page=100&type=all" | python3 -m json.tool

# Get commit activity (last year)
curl -s "https://api.github.com/users/USERNAME/events/public?per_page=100" | python3 -m json.tool

# Get organization memberships
curl -s "https://api.github.com/users/USERNAME/orgs" | python3 -m json.tool

# Get starred repos (interests)
curl -s "https://api.github.com/users/USERNAME/starred?per_page=100" | python3 -m json.tool

# Get gists (quick projects, experiments)
curl -s "https://api.github.com/users/USERNAME/gists" | python3 -m json.tool
```

#### Semantic Scholar API Commands
```bash
# Search by name
curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=NAME&limit=10" | python3 -m json.tool

# Get author papers with citations
curl -s "https://api.semanticscholar.org/graph/v1/author/AUTHOR_ID?fields=name,papers.title,papers.citationCount" | python3 -m json.tool
```

### B. Web Search Alternatives (When DuckDuckGo Fails)

#### Exa AI Neural Search
```bash
# Natural language search for people
curl -s "https://api.exa.ai/search?q=Bradley+Hallier+engineer+UVA&num=10" -H "Authorization: Bearer $EXA_API_KEY" | python3 -m json.tool
```

#### Brave Search (No Bot Detection)
```bash
# HTML scraping approach
curl -sL -A "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)" "https://search.brave.com/search?q=NAME+engineer" | grep -oE "title|description|url" | head -50
```

#### Bing Web Search API
```bash
# Microsoft Bing (often more permissive)
curl -s "https://api.bing.microsoft.com/v7.0/search?q=NAME" -H "Ocp-Apim-Subscription-Key: $BING_KEY" | python3 -m json.tool
```

### C. Creative Search Approaches

#### 1. Email Pattern Discovery
```bash
# Common email patterns for name
# firstname.lastname@company.com
# flastname@company.com
# firstname@company.com
# Try Hunter.io to verify
curl -s "https://api.hunter.io/v2/email-finder?domain=COMPANY.com&first_name=Bradley&last_name=Hallier" -H "Authorization: Bearer $HUNTER_KEY"
```

#### 2. Username Enumeration Across Platforms
```bash
# Check if username exists on multiple platforms
for platform in github twitter instagram linkedin facebook; do
  result=$(curl -s -o /dev/null -w "%{http_code}" "https://$platform.com/username")
  echo "$platform: $result"
done
```

#### 3. Historical Archive Search (Wayback Machine)
```bash
# Check if website existed in the past
curl -s "https://web.archive.org/cdx/search/cdx?url=username.github.io/*&output=json&fl=timestamp,original" | head -20
```

#### 4. Academic Institution Search
```bash
# UVA faculty/student directory
curl -sL -A "Mozilla/5.0" "https://engineering.virginia.edu/people?search=Bradley" | grep -oE "profile|name|department" | head -30

# Research group membership
curl -s "https://api.github.com/orgs/UVA-STARLAB/members" | grep -E "login|html_url"
```

#### 5. Patent & Trademark Search
```bash
# USPTO Patent Search
curl -sL -A "Mozilla/5.0" "https://patents.google.com/?inventor=Bradley+Hallier" | grep -oE "patent|family|application" | head -20

# Justia Patents
curl -sL -A "Mozilla/5.0" "https://patents.justia.com/search?q=Bradley+Hallier" | grep -oE "patent|invention|filing" | head -20
```

#### 6. Conference & Presentation Search
```bash
# Search conference proceedings
curl -sL -A "Mozilla/5.0" "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=Bradley+Hallier" | grep -oE "conference|proceedings|presentation" | head -20

# ResearchGate presentations
curl -sL -A "Mozilla/5.0" "https://www.researchgate.net/profile/Bradley-Hallier/publications" | grep -oE "conference|presentation|talk" | head -20
```

#### 7. News & Media Archive Search
```bash
# Google News Archive (historical)
curl -sL -A "Mozilla/5.0" "https://news.google.com/search?q=Bradley+Hallier" | grep -oE "article|published|source" | head -20

# Academic press releases
curl -sL -A "Mozilla/5.0" "https://www.research.virginia.edu/search?keys=Bradley+Hallier" | grep -oE "news|press|announcement" | head -20
```

#### 8. Project Collaboration Network
```bash
# Find who they collaborate with on GitHub
curl -s "https://api.github.com/users/USERNAME/following" | grep -E "login|html_url"
curl -s "https://api.github.com/users/USERNAME/followers" | grep -E "login|html_url"

# Check repo collaborators
curl -s "https://api.github.com/repos/OWNER/REPO/contributors" | grep -E "login|contributions"
```

#### 9. Dataset & Benchmark Contributions
```bash
# Kaggle competitions
curl -sL -A "Mozilla/5.0" "https://www.kaggle.com/USERNAME" | grep -oE "competition|medal|dataset" | head -20

# UCI ML Repository
curl -sL -A "Mozilla/5.0" "https://archive.ics.uci.edu/ml/search.cgi?q=Bradley" | grep -oE "dataset|author|contributor" | head -20
```

#### 10. Open Data & Government Records
```bash
# NSF award search (research funding)
curl -sL -A "Mozilla/5.0" "https://www.nsf.gov/awardsearch/advancedSearchResult?PIId=..." | grep -oE "award|investigator|amount" | head -20

# ORCID (researcher identifier)
curl -sL -A "Mozilla/5.0" "https://orcid.org/0000-0000-0000-0000" | grep -oE "works|employment|name" | head -20
```

---

## Part 3: Confidence Scoring System

### Claim Confidence Tags

| Tag | Meaning | Source Requirement |
|-----|---------|-------------------|
| `✅ VERIFIED` | Confirmed by 2+ independent sources | Primary + secondary source |
| `✅ HIGH` | Very likely accurate | 1 strong primary source |
| `⚠️ MEDIUM` | Plausible but not confirmed | Inferred from context |
| `❓ UNVERIFIED` | Claim without confirmation | Needs more research |
| `❌ CONTRADICTED` | Sources disagree | Note the conflict |

### Report Example with Confidence Scoring

```
## Current Position
- ✅ Hardware Engineer at Leidos (2020+) [LinkedIn, ZoomInfo, GitHub location]
- ✅ Former NASA Langley intern [GitHub, About.me]
- ⚠️ Current role involves defense systems [Inferred from company focus]

## Education
- ✅ B.S. Electrical & Computer Engineering, UVA [About.me, LinkedIn]
- ✅ Commonwealth Governor's School [About.me]

## Publications
- ✅ "Design of low-cost humanoid robot" [IEEE Xplore]
- ✅ "Cloud Connected Ambient Air Alcohol Sensor" [IEEE Xplore]
```

---

## Part 4: Time Boxing Framework

### Research Phase Timer (Use separate terminal)

```bash
# Set timer for each phase (alarm when done)
alias timer='echo "Timer set for $1 minutes"; sleep $(( $1 * 60 )) && echo "TIME UP"'

# Usage examples:
# timer 3   # Quick scan phase
# timer 5   # Deep API dive
# timer 3   # Cross-reference
# timer 2   # Gap analysis
# timer 3   # Synthesis
```

### Phase Checklist with Time Limits

| Phase | Max Time | Checklist |
|-------|----------|-----------|
| **Quick Scan** | 3 min | □ Web search basic info □ Identify primary sources □ Set complexity rating |
| **Deep API** | 5 min | □ GitHub profile □ Academic APIs □ Company data □ Social platforms |
| **Cross-Ref** | 3 min | □ Verify facts across sources □ Flag unverified □ Document sources |
| **Gap Analysis** | 2 min | □ Identify missing critical info □ Note limitations □ Decide continue/stop |
| **Synthesis** | 4 min | □ Build narrative □ Rate confidence □ Format report |

**Total Maximum: 17 minutes per research task**

---

## Part 5: Standardized Report Template

### Research Report Template

```markdown
# Research Report: [TARGET NAME]

**Generated:** [DATE]  
**Time Spent:** [X] minutes  
**Complexity Rating:** [1-5]  
**Researcher:** [NAME/AGENT]

---

## Executive Summary
[3-5 sentences summarizing key findings]

## Current Status & Position
- ✅ Current Role at Company [Source]
- ✅ Location [Source]
- ✅ Industry [Source]

## Educational Background
- ✅ Degree at Institution [Source]
- ✅ Earlier education [Source]

## Professional Experience
| Position | Organization | Period | Source |
|----------|--------------|--------|--------|
| [Role] | [Company] | [Date] | [Source] |

## Technical Skills & Expertise
| Category | Skills | Confidence |
|----------|--------|------------|
| [Domain] | [List] | VERIFIED/HIGH/MEDIUM |

## Key Projects & Contributions
### [Project Name]
- Description: [What it is]
- Impact: [Why it matters]
- Sources: [Where found]

## Research & Publications
| Title | Year | Venue | Source |
|-------|------|-------|--------|
| [Paper] | [Year] | [Venue] | [Link] |

## Online Presence
| Platform | Status | Link |
|----------|--------|------|
| LinkedIn | ✅ Found | [URL] |
| GitHub | ✅ Found | [URL] |
| [Other] | ❌ Not Found | - |

## Timeline Analysis
| Year | Milestone | Significance |
|------|-----------|--------------|
| [Year] | [Event] | [Why important] |

## Limitations & Gaps
- ❓ Current employment (last confirmed: [YEAR])
- ❓ Patent status (pending search)
- ❓ Social media (may be private)
- ❓ [Other gaps]

## Sources & References
| Source | URL | Type | Reliability |
|--------|-----|------|-------------|
| GitHub API | api.github.com/... | Primary | High |
| [Other] | [URL] | [Type] | [Rating] |

---

**Report Confidence Score:** [X]% verified claims  
**Next Research Steps:** [What to investigate further if needed]
```

---

## Part 6: Gap Analysis Protocol

### Critical Information Checklist

```
For Technical Professional:
□ Current employer VERIFIED
□ Current role VERIFIED  
□ Education VERIFIED
□ GitHub profile located
□ LinkedIn profile located
□ 3+ projects documented
□ 1+ publications (if academic)
□ Skills list compiled
□ Timeline coherent

For Academic Researcher:
□ Current institution VERIFIED
□ Department VERIFIED
□ 5+ publications listed
□ Citation count noted
□ Co-authors identified
□ Research group identified
□ PhD advisor (if applicable)
□ Current grants (if applicable)
```

### Gap Severity Rating

| Gap | Severity | Action |
|-----|----------|--------|
| Current employment unknown | HIGH | Flag prominently, note last known |
| Education unverified | HIGH | Flag prominently |
| No projects found | MEDIUM | Acceptable for some targets |
| No social media | LOW | Normal for private individuals |
| Patent status unknown | LOW | Nice to have |

---

## Part 7: Creative Information Discovery

### Unconventional Search Techniques

#### 1. Conference Presentation Mining
```bash
# Search presentation slides
curl -sL -A "Mozilla/5.0" "https://www.slideshare.net/search/slideshow?searchfrom=header&q=Bradley+Hallier" | grep -oE "slideshare|presentation|view" | head -20

# Search SpeakerDeck
curl -sL -A "Mozilla/5.0" "https://speakerdeck.com/search?q=Bradley+Hallier" | grep -oE "deck|slide|talk" | head -20
```

#### 2. Podcast & Interview Search
```bash
# Search podcast appearances
curl -sL -A "Mozilla/5.0" "https://www.listennotes.com/search/?q=Bradley+Hallier&sort_by_date=1" | grep -oE "episode|podcast|guest" | head -20

# Search YouTube
curl -sL -A "Mozilla/5.0" "https://www.youtube.com/results?search_query=Bradley+Hallier+interview" | grep -oE "video|watch|interview" | head -20
```

#### 3. Code Contribution Attribution
```bash
# Search Stack Overflow answers
curl -sL -A "Mozilla/5.0" "https://stackoverflow.com/search?q=user:Bradley+Hallier" | grep -oE "answer|score|accepted" | head -20

# Search Stack Exchange network
for site in serverfault superuser math physics; do
  curl -sL -A "Mozilla/5.0" "https://$site.stackexchange.com/search?q=Bradley+Hallier" | grep -oE "question|answer" | head -5
done
```

#### 4. Mailing List Archives
```bash
# Search Linux kernel mailing lists
curl -sL -A "Mozilla/5.0" "https://lore.kernel.org/lists?query=Bradley+Hallier" | grep -oE "patch|email|from" | head -20

# Search GitHub discussions
curl -s "https://api.github.com/repos/OWNER/REPO/issues?creator=USERNAME" | grep -E "title|state|created_at"
```

#### 5. Product & Tool Attribution
```bash
# Search Docker Hub for published images
curl -sL -A "Mozilla/5.0" "https://hub.docker.com/u/USERNAME" | grep -oE "image|container|pull" | head -20

# Search PyPI for published packages
curl -sL -A "Mozilla/5.0" "https://pypi.org/search/?q=Bradley+Hallier" | grep -oE "package|version|author" | head -20

# Search npm for published packages
curl -sL -A "Mozilla/5.0" "https://www.npmjs.com/search?q=Bradley+Hallier" | grep -oE "package|version|author" | head -20
```

#### 6. Academic Collaboration Network
```bash
# Search arXiv co-authors
curl -sL -A "Mozilla/5.0" "https://arxiv.org/search/?query=author:Bradley+Hallier&searchtype=all" | grep -oE "paper|title|coauthor" | head -20

# Search Microsoft Academic (now closed, use Semantic Scholar)
curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=Bradley+Hallier&limit=5" | python3 -m json.tool
```

#### 7. Government & Grant Records
```bash
# Search SBIR/STTR awards (small business research)
curl -sL -A "Mozilla/5.0" "https://www.sbir.gov/search/Bradley%20Hallier" | grep -oE "award|company|phase" | head -20

# Search USAspending.gov for contracts
curl -sL -A "Mozilla/5.0" "https://www.usaspending.gov/search/?keyword=Bradley+Hallier" | grep -oE "contract|award|amount" | head -20
```

#### 8. Historical Project Discovery
```bash
# Search SourceForge
curl -sL -A "Mozilla/5.0" "https://sourceforge.net/search/?q=Bradley+Hallier" | grep -oE "project|download|license" | head -20

# Search Google Code Archive
curl -sL -A "Mozilla/5.0" "https://code.google.com/archive/search?q=Bradley+Hallier" | grep -oE "project|source|download" | head -20
```

---

## Part 8: Source Reliability Matrix

| Source Type | Reliability | Update Frequency | Best For |
|-------------|-------------|------------------|----------|
| GitHub API | High | Real-time | Technical skills, projects |
| LinkedIn | High | Self-reported | Employment, education |
| IEEE Xplore | High | Varies | Academic papers |
| Semantic Scholar | High | Daily | Citations, papers |
| About.me | Medium | Low | Personal branding |
| Company Website | High | As updated | Current role |
| News Article | Medium | One-time | Specific events |
| Wikipedia | Medium | Varies | Overview, basics |
| Facebook | Low | Varies | Personal, unverified |
| Twitter/X | Low | High | Recent activity |
| Crunchbase | High | Daily | Funding, roles |

---

## Part 9: Research Log Template

### After Each Research Task

```markdown
## Research Log: [TARGET NAME]

**Date:** [YYYY-MM-DD]  
**Time Spent:** [X] minutes  
**Complexity Rating:** [1-5]

### Sources Used
| Source | Data Found | Reliability |
|--------|------------|-------------|
| GitHub API | 20 repos, orgs, commits | High |
| Semantic Scholar | 3 papers | High |
| [Other] | [Data] | [Rating] |

### Key Findings (5 bullets)
1. 
2. 
3. 
4. 
5. 

### Verified Facts: [X]
### Speculative Claims: [Y]
### Unresolved Gaps: [Z]

### Tools That Worked Best
1. [Tool]
2. [Tool]

### Tools That Failed
1. [Tool] - [Reason]
2. [Tool] - [Reason]

### What to Do Differently Next Time
1. [Improvement]
2. [Improvement]

### Would Research Again? [Yes/No]
Notes: [Thoughts on complexity vs value]
```

---

## Part 10: Quick Reference Card

### Standard Research Workflow (15 min max)

```
1. Quick Scan (2 min)
   □ Web search basic info
   □ Identify primary sources
   □ Set complexity rating (1-5)

2. GitHub Deep Dive (3 min)
   □ Profile data
   □ Repos analysis
   □ Organizations
   □ Recent activity

3. Academic/Professional (3 min)
   □ Semantic Scholar / LinkedIn
   □ Company verification
   □ Publications check

4. Cross-Reference (2 min)
   □ Verify 3+ key facts
   □ Document sources
   □ Flag unverified

5. Gap Analysis (2 min)
   □ Check critical info
   □ Note limitations
   □ Decide: Continue or conclude?

6. Synthesis (3 min)
   □ Build summary
   □ Rate confidence
   □ Format report
```

### Emergency Abort Criteria
Stop research if:
- ❌ No verifiable information after 10 minutes
- ❌ Target appears to be private individual with no public presence
- ❌ Ethical concerns about research purpose
- ❌ Time limit reached without basic facts

---

## Implementation Checklist

- [x] Pre-research assessment checklist created
- [x] Complexity rating framework defined
- [x] Tool priority matrix established
- [x] GitHub API commands documented
- [x] Semantic Scholar API commands documented
- [x] Alternative search tools listed
- [x] 10 creative search techniques added
- [x] Confidence scoring system defined
- [x] Time boxing framework created
- [x] Standardized report template created
- [x] Gap analysis protocol defined
- [x] Source reliability matrix created
- [x] Research log template created
- [x] Quick reference card added
- [x] Emergency abort criteria defined

---

*Implementation Guide v1.0 - Ready for use in all future research tasks.*
