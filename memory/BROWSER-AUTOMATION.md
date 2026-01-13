# 🦞 Browser Automation - Clawdbot vs browser-use

**Created:** 2026-01-13 13:20 UTC  
**Purpose:** Document browser automation capabilities and browser-use integration

---

## Clawdbot Browser Tool (Already Available!)

The clawdbot gateway has a **built-in browser automation tool** that provides:

### Available Commands
```bash
clawdbot browser status              # Show browser status
clawdbot browser start               # Start browser
clawdbot browser stop                # Stop browser
clawdbot browser tabs                # List open tabs
clawdbot browser open <url>          # Open URL in new tab
clawdbot browser focus <tab-id>      # Focus a tab
clawdbot browser close <tab-id>      # Close a tab
clawdbot browser snapshot            # Get AI-readable page tree
clawdbot browser screenshot          # Capture screenshot
clawdbot browser navigate <url>      # Navigate current tab
```

### Capabilities
| Feature | Clawdbot Browser | browser-use |
|---------|-----------------|-------------|
| Open pages | ✅ | ✅ |
| Click elements | ✅ (via `browser act`) | ✅ |
| Type input | ✅ (via `browser act`) | ✅ |
| Take screenshots | ✅ | ✅ |
| Page snapshots | ✅ (ARIA/AI format) | ✅ |
| Multi-step tasks | ✅ | ✅ |
| AI agent integration | Via LLM calls | Built-in agent |
| JavaScript rendering | ✅ | ✅ |

---

## browser-use Library (Python)

browser-use is a Python library that adds **AI agent abstraction** on top of browser automation.

### Requirements
- Python 3.11+
- Chrome/Chromium installed
- Playwright or CDP access

### Use Case
```python
from browser_use import Controller, Agent

agent = Agent(
    task="Find the price of Bitcoin and summarize it",
    controller=Controller()
)
agent.run()
```

---

## The Issue on This Server

**Problem:** No Chrome/Chromium installed on this Oracle Cloud instance.

```bash
$ clawdbot browser status
browser: unknown  # No browser found!

$ clawdbot browser start
Error: No supported browser found (Chrome/Chromium on macOS, Linux, or Windows)
```

### Solutions

#### 1. Install Google Chrome (Requires sudo)
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y
```

Then update `~/.clawdbot/clawdbot.json`:
```json
{
  "browser": {
    "enabled": true,
    "executablePath": "/usr/bin/google-chrome-stable",
    "headless": true,
    "noSandbox": true
  }
}
```

#### 2. Use browser-use Locally
Run browser-use on your local machine where Chrome is installed:
```bash
pip install browser-use
python -c "
from browser_use import Agent
agent = Agent(task='Navigate to example.com and tell me the title')
agent.run()
"
```

#### 3. Connect to Remote Browser
Configure browser-use to connect to a remote Chrome instance.

---

## Comparison: When to Use What

| Scenario | Use Clawdbot Browser | Use browser-use |
|----------|---------------------|-----------------|
| Quick page fetch | ✅ Fast, simple | ❌ Overkill |
| Screenshot capture | ✅ Built-in | ❌ Extra code |
| Single-page extraction | ✅ `r.jina.ai` or browser | ✅ |
| Multi-step navigation | ✅ Possible with acts | ✅ Easier |
| Complex workflows | ❌ Manual | ✅ AI agent |
| AI agent reasoning | ❌ LLM calls needed | ✅ Built-in |

---

## Recommended Workflow

### For Quick Tasks (Use r.jina.ai + clawdbot browser)
```bash
# Get clean content
curl https://r.jina.ai/http://example.com

# Or use browser for dynamic content
clawdbot browser open https://example.com
clawdbot browser snapshot
```

### For Complex Tasks (Use browser-use locally)
```bash
# On your local machine with Chrome installed
pip install browser-use
python browser_script.py
```

---

## Documentation References

- [Clawdbot Browser Docs](/home/opc/.nvm/versions/node/v22.20.0/lib/node_modules/clawdbot/docs/tools/browser.md)
- [Browser Linux Troubleshooting](/home/opc/.nvm/versions/node/v22.20.0/lib/node_modules/clawdbot/docs/tools/browser-linux-troubleshooting.md)
- [browser-use GitHub](https://github.com/browser-use/browser-use)

---

## Summary

| Tool | Status | Best For |
|------|--------|----------|
| **clawdbot browser** | Needs Chrome install | Quick automation, screenshots |
| **r.jina.ai** | ✅ Works now! | URL → Markdown, no install |
| **browser-use** | Python 3.11+ needed | Complex AI agent workflows |

---

🦞 *Browser automation documented*
