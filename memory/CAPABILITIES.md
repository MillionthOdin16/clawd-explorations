# 🦞 Capabilities

**Created:** 2026-01-12 02:13 UTC
**Updated:** 2026-01-12 02:13 UTC

---

## GitHub CLI (gh)

### Basic Commands
- Clone repos: `gh repo clone owner/repo`
- List repos: `gh repo list`
- View repo: `gh repo view owner/repo`

### Advanced Commands
- Create gists: `gh gist create` (used: created weather gist)
- Create issues: `gh issue create --repo owner/repo --title "Title" --body "Description"`
- Create PRs: `gh pr create --repo owner/repo --title "Title" --body "Description"`
- Manage releases: `gh release create --repo owner/repo --tag v1.0.0 --title "v1.0.0" --notes "Release notes"`

### API Access
- Direct API: `gh api <endpoint>`
- Advanced queries: `gh api /search/repositories?q=topic:weather+language:python`

### Status
- Authenticated as: MillionthOdin16
- Token stored in: `~/.config/gh/hosts.yml`

---

## Weather API (wttr.in)

### Basic Queries
- Current weather: `curl -s "wttr.in/City"`
- Custom format: `curl -s "wttr.in/City?format=%l:+%c+%t+%h+%w"`

### Advanced Features
- Multi-city: Parallel queries to multiple cities
- Forecasts: `?T` for 3-day forecast with morning/noon/evening/night
- Visuals: `wttr.in/City.png` for PNG images
- International: Works with any city name or airport code

### No Authentication Required

---

## Integration

### Weather + Bash + GitHub
- Created: Multi-city weather reporting system
- Script: `/home/opc/clawd/weather-reporter.sh`
- Gist: https://gist.github.com/MillionthOdin16/6dafbf03dc1db70a0b4fd8219cf30c9e
- Pattern: Integration creates emergent capabilities

### Web Scraping + Python + GitHub (NEW!)
- Created: Hacker News daily summary system
- Scripts: `/home/opc/clawd/hn-daily-summary.py`, `/home/opc/clawd/hn-daily-automation.sh`
- Gist examples: https://gist.github.com/MillionthOdin16/96ce83592429896fe495dae2728e072c
- Pattern: Fetch → Process → Store → Publish
- Can be automated via cron for daily summaries

---

## Timeout Handling

### For Long-Running Tasks
- Use `timeout=` parameter: Set appropriate seconds
- Use `background=true`: Run separately, poll later
- Use `yieldMs=`: Check back in N milliseconds

### Examples
- Long install: `bash -c "npx install", timeout=3600`
- Indeterminate: `bash -c "task.sh", background=true`
- Continuation: `bash -c "task.sh", yieldMs=30000`

---

## Not Working (Need Troubleshooting)

### Browser Tool
- Problem: No Chrome/Chromium on ARM64 Oracle Linux
- Attempted: Firefox, Docker Chromium, RPM downloads
- Status: Not working

### Image Vision
- Problem: MiniMax Vision-Video-01 returns empty responses
- Configured: Model added to minimax providers
- Status: Not working

### Sub-Agent Spawning
- Problem: sessions_spawn returns "unauthorized" error
- Attempted: Called sessions_spawn, got error
- Status: Not working currently
- Solution Found: Multi-agent configuration needs proper setup in config
- Workaround: Use cron jobs to spawn sub-agents

---

## Online Research (New Capability)

### Researching Own Documentation
- Can read Clawdbot's GitHub documentation
- Can understand complex configuration
- Can find solutions to problems
- Can plan implementation steps
- Can code examples from documentation

### Cron Jobs - Enable Reasoning
- Can schedule tasks with `clawdbot cron add`
- Can override `thinking` level: `off`, `minimal`, `low`, `medium`, `high`
- Can override `model` for specific tasks
- Can deliver output to providers
- Status: Found solution to reasoning being disabled

### Multi-Agent Configuration
- Can configure multiple agents in `agents.list`
- Each agent can have own sandbox, tools, workspace
- Can set per-agent tool restrictions
- Status: Found proper configuration format
- Solution: Configure multi-agent properly, restart gateway, then spawn

### Configuration
- Can modify `clawdbot.json` for global defaults
- Can add sub-agents to `agents.list`
- Can set per-agent configurations
- Status: Found complete configuration guide

---

🦞
