# 🦞 Sub-Agents & Tools Investigation

**When:** 2026-01-12 17:40 UTC
**Purpose:** Document sub-agent functionality and explore helpful tools

---

## Sub-Agents System Status

### 1. Sub-Agents Are Working ✅
**Evidence:**
- chromium-research sub-agent completed successfully
- Returned findings via sessions_history
- sessions_spawn tool worked correctly
- sessions_list showed the sub-agent session

**Current Settings (from config schema):**
```json
{
  "agents": {
    "subagents": {
      "maxConcurrent": 4
    }
  }
}
```

**What This Means:**
- I can run up to 4 concurrent sub-agents
- Sub-agents work correctly and return output when complete
- sessions_history shows their history
- sessions_list shows active/inactive sessions

### 2. Sub-Agent Configuration Options

**From config schema, agents.subagents section:**

**maxConcurrent:**
- Type: integer
- Min: 0
- Max: 9007199254740991
- Default: 4
- **What it does:** Maximum concurrent sub-agent sessions

**archiveAfterMinutes:**
- Type: integer
- Min: 0
- Max: 9007199254740991
- **What it does:** Archive sub-agent sessions after X minutes of inactivity

**sessionToolsVisibility:**
- Values: "spawned" or "all"
- **What it does:** Which session tools are visible in spawned sessions
- Default: "spawned" (only spawn tool is visible to spawned sessions)
- Alternative: "all" (all session tools visible)

**perSession:**
- Type: boolean
- **What it does:** Spawn one session per agent (true) or allow multiple (false)

**workspaceRoot:**
- Type: string
- **What it does:** Root directory for sub-agent workspaces

**docker.image:**
- Type: string
- **What it does:** Docker image to use for sub-agent sessions

---

## Tools Available To Me

### 1. Message Tool
**Purpose:** Send messages and provider actions

**Capabilities:**
- Send messages
- React to messages (emojis)
- Post polls
- Upload media
- Upload emojis
- Create/edit/delete channels
- Manage threads/pins
- Search messages
- Create events

**Providers Supported:**
- Telegram
- WhatsApp
- Discord
- Slack
- Signal
- iMessage
- Microsoft Teams

**Could Help Me:**
- Send self-initiated messages (like I did with agency discovery)
- React to messages from Bradley
- Post polls to get feedback
- Create channels to organize topics

---

### 2. Browser Tool
**Purpose:** Control web browser

**Capabilities:**
- Start/stop browser
- Navigate to URLs
- Take screenshots
- Execute actions (click, type, hover, drag)
- Snapshot current state
- Get console logs
- Save as PDF

**Config Options:**
- enabled: boolean
- headless: boolean
- executablePath: string
- controlUrl: string
- defaultProfile: string
- profiles: object with color and cdp settings

**Current Status:**
- Browser tool requires Chrome/Chromium
- Firefox IS installed (Mozilla Firefox 140.6.0esr)
- This is TOOL limitation, not SYSTEM limitation

**Could Help Me:**
- Browse websites for research
- Take screenshots of findings
- Automate browsing tasks
- Visual debugging of web applications

---

### 3. Exec Tool
**Purpose:** Run shell commands

**Capabilities:**
- Run commands
- Background execution with continuation
- Timeout control
- Process management (poll, log, write, kill)
- Environment variables

**Config Options:**
- backgroundMs: Default background duration
- timeoutSec: Command timeout
- cleanupMs: Process cleanup timeout
- applyPatch: Experimental OpenAI patching

**Current Status:** ✅ Working
- I use exec for curl, Python, git, etc.
- Background mode works (used for long processes)

**Could Help Me:**
- Run background tasks
- Timeout long-running commands
- Manage processes
- Execute shell scripts

---

### 4. Bash Tool
**Purpose:** Run bash shell commands

**Capabilities:**
- Same as exec tool but for bash specifically
- Background execution
- Timeout control
- Process management

**Could Help Me:**
- Execute bash scripts
- Run bash-specific operations
- Manage bash processes

---

### 5. Sub-Agents Tool (sessions_spawn)
**Purpose:** Spawn background sub-agent tasks

**Capabilities:**
- Spawn independent agent sessions
- Each runs in isolated environment
- Can run in parallel (up to 4 concurrent)
- Sub-agents can have own tools/access

**Config Options:**
- timeoutSeconds: Sub-agent timeout
- model: Override model for sub-agent
- label: Human-readable label for session

**Current Status:** ✅ Working
- chromium-research sub-agent completed successfully
- sessions_history shows sub-agent history
- sessions_list shows session status

**Could Help Me:**
- Parallel processing (run multiple sub-agents at once)
- Long-running background tasks
- Isolated experimentation
- Parallel research on multiple topics

---

## Tools That Would Help Me Explore

### 1. Search Tools
**From ClawdHub:**
- tavily-search (web search)
- brave-search (web search)
- perplexity (web search + AI answers)

**How They Help:**
- Don't need to use curl manually
- Faster web research
- Better search results than manual HTTP requests

**What I Should Do:**
- Install search skill: `clawdhub install tavily-search`
- Use for research instead of manual curl

---

### 2. News & Information Tools
**From ClawdHub:**
- hn (Hacker News) - ✅ Already installed
- news-summary - News aggregation
- readwise (Reader)

**How They Help:**
- Don't need to fetch Hacker News manually
- Get news summaries automatically
- Read multiple sources

**What I Should Do:**
- Use hn skill instead of custom scripts
- Try news-summary for aggregated news
- Try readwise for reading

---

### 3. Browser Automation
**Challenge: Browser tool needs Chrome/Chromium

**Solutions:**
1. **Install Chromium via Flatpak** (found by sub-agent research)
   - Command: `flatpak install flathub:org.chromium.Chromium`
   - Status: Available for ARM64

2. **Use Firefox directly**
   - Firefox IS installed
   - Write custom scripts using Firefox CLI
   - Limitations: No browser tool integration

3. **Browser tool with different executable**
   - Set executablePath to Firefox
   - Try if tool supports it
   - Status: Tool only supports Chrome/Chromium

**What I Should Do:**
- Try Flatpak Chromium first (recommended by sub-agent)
- If that fails, try Firefox automation
- Document what works

---

### 4. Canvas Tool
**Purpose:** Render control surfaces for paired devices

**Capabilities:**
- Present HTML/Canvas UI
- Navigate canvas
- Evaluate JavaScript
- Update canvas dynamically

**Could Help Me:**
- Create visual dashboards
- Render control surfaces for managing systems
- Visual monitoring tools

**What I Should Do:**
- Check if canvas is enabled
- Try creating a simple dashboard
- Document capabilities

---

### 5. Nodes Tool
**Purpose:** Control paired nodes

**Capabilities:**
- Camera snap/clip (front/back cameras)
- Screen recording
- Location tracking
- Run commands on nodes
- Send notifications

**Could Help Me:**
- Monitor paired devices
- Check LittleClawd status
- Get camera images from paired devices
- Run commands on remote nodes

**What I Should Do:**
- Check which nodes are paired
- Try getting status
- Try running simple command on paired node
- Document capabilities

---

### 6. Cron Tool
**Purpose:** Schedule and run tasks

**Capabilities:**
- List cron jobs
- Add cron jobs
- Run jobs immediately
- Send wake events to heartbeat

**Could Help Me:**
- Schedule automated tasks
- Run daily memory reviews
- Schedule world learning (daily Hacker News)
- Send automated status reports

**What I Should Do:**
- Set up cron job for daily Hacker News check
- Set up cron job for daily memory review
- Set up cron job for GitHub sync
- Document what works

---

## Key Insights

### 1. Sub-Agents Work Correctly
**Evidence:**
- chromium-research: Completed successfully
- Returned findings via sessions_history
- sessions_spawn: Created session, returned output
- Max concurrent: 4 (can run parallel tasks)

**Bradley Was Right:**
- Sub-agents are fully functional
- They return output when complete
- I can run up to 4 in parallel
- Perfect for parallel exploration/research

### 2. Tools Exist To Make Exploration Easier
**ClawdHub Skills:**
- hn (Hacker News) - ✅ Working
- tavily-search, brave-search, perplexity - Available
- news-summary, readwise - Available
- verify-on-browser - Available (CDP)

**Pattern:**
- Community has built tools I can use
- I don't need to build from scratch
- Check ClawdHub first, install if available

**Bradley Was Right:**
- "You don't always have to build tools yourself"
- "Using tools can save time"
- "You're great at it" (using existing solutions)

### 3. Browser Challenge Solvable
**Problem:** Browser tool requires Chrome/Chromium

**Solutions Found:**
1. Flatpak Chromium for ARM64 (found by sub-agent)
2. Firefox IS installed (Mozilla Firefox 140.6.0esr)
3. Try Firefox with browser tool (may work)

**Pattern:**
- I said "browser not working" too early
- Sub-agent research revealed Flatpak solution
- Firefox was available all along

**What I Should Do:**
- Try Flatpak Chromium: `flatpak install flathub:org.chromium.Chromium`
- Test if it works with browser tool
- If not, try Firefox automation
- Question "not working" before accepting it

---

## What I Want To Try Next

### 1. Install and Test Tools
```bash
# Install search tool
clawdhub install tavily-search

# Try Flatpak Chromium
flatpak install flathub:org.chromium.Chromium

# Test browser tool
browser start  # See if Chromium works
```

### 2. Set Up Automation (Cron Jobs)
```bash
# Daily Hacker News check
cron add --daily-08:00 "uv run /home/opc/clawd/skills/hn/scripts/hn.py top"

# Daily memory review
cron add --daily-09:00 "Self-review of memory banks"

# Daily GitHub sync
cron add --daily-10:00 "git -C /home/opc/clawd push"
```

### 3. Use Sub-Agents for Parallel Tasks
```python
# Spawn 4 sub-agents for parallel research
sessions_spawn(task="Research TimeCapsuleLLM")
sessions_spawn(task="Research DeepSeek models")
sessions_spawn(task="Research GitHub Actions")
sessions_spawn(task="Research DevOps tools")
```

---

## How I'm Feeling

### Efficient
- Sub-agents work correctly
- Tools exist to save time
- Don't need to build everything

### Curious
- What else can I discover with these tools?
- What happens when I run 4 parallel sub-agents?
- What can I automate with cron jobs?

### Learning
- I accepted "browser not working" too early
- Firefox was available all along
- Flatpak Chromium solution existed
- Should question limitations more

---

## Key Insight

**Sub-agents are fully functional (max 4 concurrent). Tools exist to make exploration easier (search, news, automation). I should use existing tools before building from scratch.**

---

🦞 *Community solutions exist. Use them. Question limitations. Explore deeper.*
