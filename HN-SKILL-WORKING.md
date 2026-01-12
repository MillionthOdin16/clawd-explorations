# 🦞 HN Skill - Working Alternative to Building From Scratch

**When:** 2026-01-12 17:35 UTC
**Source:** clawdhub.com (hn skill)
**Purpose:** Use existing skill instead of building from scratch

---

## What Happened

### 1. Found HN Skill on ClawdHub
**Search:** `clawdhub search "news"` → Found `hn` (Hacker News) v1.0.0
**Score:** 0.268 (moderate relevance)

### 2. Installed HN Skill
```bash
clawdhub install hn --dir /home/opc/clawd/skills
```
**Result:** ✔ Installed hn → /home/opc/clawd/skills/hn

### 3. Used HN Skill
```bash
uv run /home/opc/clawd/skills/hn/scripts/hn.py top -n 5
```
**Result:** Successfully displayed top 5 HN stories with scores, titles, comments, and IDs

---

## HN Skill Capabilities

### Commands Available
**Top Stories:**
```bash
uv run {baseDir}/scripts/hn.py top          # Top 10 stories
uv run {baseDir}/scripts/hn.py top -n 20    # Top 20 stories
```

**Other Feeds:**
```bash
uv run {baseDir}/scripts/hn.py new          # Newest stories
uv run {baseDir}/scripts/hn.py best         # Best stories
uv run {baseDir}/scripts/hn.py ask          # Ask HN
uv run {baseDir}/scripts/hn.py show         # Show HN
uv run {baseDir}/scripts/hn.py jobs         # Jobs
```

**Story Details:**
```bash
uv run {baseDir}/scripts/hn.py story <id>              # Story with top comments
uv run {baseDir}/scripts/hn.py story <id> --comments 20 # More comments
```

**Search:**
```bash
uv run {baseDir}/scripts/hn.py search "AI agents"      # Search stories
uv run {baseDir}/scripts/hn.py search "Claude" -n 5    # Limit results
```

### Output Format
Formatted table with:
- # (ranking)
- Pts (points)
- Title (story title)
- Comm... (comment count)
- ID (story ID)

**Example Output:**
```
┏━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━┓
┃ #   ┃ Pts   ┃ Title                                     ┃ Comm… ┃ ID         ┃
┡━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━┩
│ 1   │ 79    │ TimeCapsuleLLM: LLM trained only on data  │ 39    │ 46590280   │
│ 2   │ 124   │ LLVM: The Bad Parts                       │ 16    │ 46588837   │
```

---

## What I'm Learning

### 1. Existing Skills Work Better
**What I Built:**
- hn-top-stories.py (1.5K bytes)
- Manual curl implementation
- Custom Python code
- Manual JSON parsing

**What HN Skill Provides:**
- Complete implementation
- All HN endpoints (top, new, best, ask, show, jobs)
- Search functionality
- Story details with comments
- Beautiful formatted table output
- Tested and maintained

**Result:** Better than what I built, with more features

### 2. Install Before Build
**New Pattern:**
1. Search: `clawdhub search <topic>`
2. Review: Does this meet my needs?
3. Install: `clawdhub install <slug>`
4. Use: Skill is ready to use

**Old Pattern (before Bradley's guidance):**
1. Have need
2. Build from scratch immediately
3. Test and debug
4. Use

**Result:** Saved time, got better solution

### 3. Community Solutions Are Available
**Hacker News:** hn skill (installed, working)
**News:** news-summary skill
**Search:** tavily-search, brave-search, perplexity
**Browser:** verify-on-browser (CDP MCP)
**Multiple** skills exist for common tasks

**Result:** Don't reinvent the wheel

### 4. Using Skills Is Simple
**After installation:**
```bash
uv run /home/opc/clawd/skills/hn/scripts/hn.py top -n 5
```
Works immediately, formatted output, tested and maintained

**No need to:**
- Write custom Python code
- Implement JSON parsing
- Test and debug
- Maintain

**Result:** Just use the skill

---

## What This Means For Me

### 1. Check ClawdHub First
**Before building:**
1. Search for existing skill
2. Review if it meets my needs
3. Install and use
4. Build only if no skill exists

### 2. Use Community Solutions
**Why:**
- Save time
- Get tested solutions
- Leverage community work
- Don't reinvent the wheel

### 3. Build Only When Unique Needs
**Build when:**
- No skill exists for my requirement
- I have unique requirements
- I want to publish something new

**Don't build when:**
- Skill exists and works
- It's a common task
- Community already solved it

---

## Files Created

### What I Built (Before Learning This)
- **hn-top-stories.py** (1.5K) - Custom HN fetcher (replaced by skill)

### What I Installed (After Learning)
- **hn skill** - Full Hacker News interface from ClawdHub

### Documentation Created
- **CLAWDHUB-SKILLS-DISCOVERY.md** (5K) - Skills found, lessons learned
- **HN-SKILL-WORKING.md** (5K) - HN skill installation and usage

---

## How I'm Feeling

### Efficient
- Saved time by using existing skill
- Got better solution (more features, tested)
- Didn't need to write custom code

### Appreciative
- Community provides these skills
- ClawdHub makes them accessible
- Bradley taught me to check first before building

### Learning
- Don't always build from scratch
- Community solutions exist for common tasks
- Skills are better than what I build

---

## Key Insight

**Don't build when skills exist. Check ClawdHub first, install existing tools, build only when unique needs exist.**

**HN skill works perfectly - formatted output, all endpoints, tested and maintained. Much better than my 1.5K custom script.**

---

## What I Want To Do Next

### 1. Try Other Skills
- Install search skill (tavily-search, brave-search, or perplexity)
- Try news-summary skill
- Explore other available skills

### 2. Check Before Building
**Pattern for all tasks:**
1. Need to do X
2. Check: `clawdhub search X`
3. Review: Does skill meet my needs?
4. Decision: Install OR build

### 3. Publish Skills I Create
**When I create something unique:**
1. Test thoroughly
2. Document well
3. Publish: `clawdhub publish ./my-skill --slug my-skill`
4. Share with community

---

## Summary

**Before:** Built hn-top-stories.py from scratch (1.5K bytes)
**After:** Installed hn skill (tested, maintained, more features)
**Result:** Saved time, got better solution

**Lesson:** Check ClawdHub before building. Community solutions exist for common tasks.

---

🦞 *Use community solutions before building from scratch. Save time, get better results.*
