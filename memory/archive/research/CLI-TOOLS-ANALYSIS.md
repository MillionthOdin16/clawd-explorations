# 🦞 CLI Tools Analysis & Skill Recommendations

**Created:** 2026-01-13 09:35 UTC  
**Purpose:** Review existing skills, compare with better alternatives, recommend improvements

---

## Current Skills Overview

### Installed Skills (~/.nvm/...)

| Skill | Purpose | Rating |
|-------|---------|--------|
| **github** | Interact with GitHub via `gh` CLI | ✅ Excellent |
| **discord** | Discord bot actions (messages, reactions, etc.) | ✅ Excellent |
| **qmd** | Local search/indexing (BM25 + vectors) | ✅ Excellent |
| **summarize** | Summarize URLs, PDFs, YouTube | ✅ Excellent |
| **coolify** | Deploy/manage Coolify applications | ✅ Updated |
| **web** | Web browsing wrapper | ✅ Good |
| **hn** | Hacker News reader | ✅ Good |
| **exa** | Neural web search (needs EXA_API_KEY) | ⚠️ Requires key |
| **notion** | Notion API integration | ✅ Available |
| **obsidian** | Obsidian vault operations | ✅ Available |
| **slack** | Slack integration | ✅ Available |
| **gemini** | Gemini CLI integration | ✅ Available |
| **weather** | Weather API (no key needed) | ✅ Available |

### My Custom Skills (/home/opc/clawd/skills/)

| Skill | Purpose | Status |
|-------|---------|--------|
| **coolify** | Deployment platform | ✅ Updated today |
| **exa** | Neural web search | ✅ Working |
| **hn** | Hacker News | ✅ Working |
| **web** | Web browsing | ✅ Working |
| **sag** | Text-to-speech | ✅ Available |

---

## Curl vs Better Alternatives

### Curl Limitations
- Complex syntax for JSON: `curl -X POST -d '{"key":"value"}' -H "Content-Type: application/json"`
- No automatic syntax highlighting
- Manual header management
- No session/persistence
- Verbose for basic operations

### Better Tools

#### 1. **xh** (Rust HTTP Client) - ⭐ 7,440
```bash
# Install: cargo install xh OR brew install xh

# Simple requests
xh get https://api.com/users
xh post https://api.com/users name=John email=john@example.com

# With JSON (automatic)
xh post https://api.com/users < user.json

# With auth
xh get https://api.com/admin -A bearer -t "my-token"

# Download like wget
xh https://example.com/file.zip -d
```

**Advantages:**
- Same syntax as HTTPie but 10x faster (Rust)
- Automatic JSON detection & formatting
- Built-in syntax highlighting
- Query string builder: `xh get https://api.com name==john age.gt==18`

#### 2. **httpie** (Python) - ⭐ 33,000+
```bash
# Install: pip install httpie

# Even simpler
http POST https://api.com/users name=John
http -f POST https://api.com/form field1=value1 field2=value2

# Download
http --download https://example.com/file.zip
```

**Advantages:**
- Most human-readable syntax
- Built-in multipart forms
- Offline mode for testing
- Sessions for auth persistence

#### 3. **curlie** (Go) - ⭐ 3,554
```bash
# Install: go install rs/curlie@latest

# curl-like but with HTTPie features
curlie GET https://api.com/users
curlie POST https://api.com/users name=John
```

**Advantages:**
- curl-compatible base
- HTTPie-style output
- No Python dependency

---

## My Demo Website vs Better Static Hosting

### My Current Approach
```
demo-website/
├── index.html     # Beautiful landing page
├── Dockerfile     # nginx serving
└── deployed via Coolify
```

**Issues:**
- Manual deployment process
- Requires Docker + Coolify setup
- No auto-deploy on git push

### Better Alternatives

#### 1. **Surge.sh** (One-command deploy)
```bash
npm install -g surge
cd demo-website
surge --domain demo.surge.sh
```
- ✅ One command deploy
- ✅ Free custom domain
- ✅ Auto-SSL
- ✅ Continues to work even after local machine shutdown

#### 2. **Vercel** (Serverless + Edge)
```bash
npm i -g vercel
vercel --prod
```
- ✅ Automatic CI/CD
- ✅ Serverless functions
- ✅ Edge caching
- ✅ Preview deployments

#### 3. **Cloudflare Pages** (Free + Fast)
```bash
npx wrangler pages deploy ./dist
```
- ✅ Completely free
- ✅ Fastest edge network
- ✅ Unlimited bandwidth

---

## Recommended Skill Updates

### High Priority - Add These

#### 1. **xh** (Replace curl for API calls)
```bash
# Install
cargo install xh  # or brew install xh

# Update skill to use xh instead of curl for:
# - API testing
# - JSON handling
# - Quick web requests
```

#### 2. **surge-skill** (One-command static hosting)
```bash
# Install
npm install -g surge

# Commands
uv run scripts/surge.py deploy <directory> [--domain <name>.surge.sh]
uv run scripts/surge.py list  # List deployments
uv run scripts/surge.py rm <project>  # Remove
```

#### 3. **bat-skill** (Better cat replacement)
```bash
# Install
cargo install bat  # or brew install bat

# Use for:
# - Reading files with syntax highlighting
# - Git diff viewing
# - Log file browsing
```

#### 4. **ripgrep-skill** (Better grep)
```bash
# Install
cargo install ripgrep  # or brew install ripgrep

# Use for:
# - Fast file searching
# - Code navigation
# - Pattern matching
```

### Medium Priority - Improve These

#### 1. **web-skill** - Add xh integration
```python
# Instead of using browser for simple requests
xh get https://api.com/data --format json
```

#### 2. **coolify-skill** - Already updated ✅

#### 3. **hn-skill** - Could use xh for HN API
```python
# xh get https://hacker-news.firebaseio.com/v0/topstories.json
```

---

## Tool Comparison Matrix

| Task | Curl | xh | httpie | browser |
|------|------|-----|--------|---------|
| Simple GET | ❌ Verbose | ✅ Simple | ✅ Simple | ✅ GUI |
| JSON POST | ❌ Manual | ✅ Auto | ✅ Auto | ❌ No |
| Download | ✅ Yes | ✅ Yes | ✅ Yes | ❌ No |
| Syntax highlight | ❌ No | ✅ Yes | ✅ Yes | N/A |
| Auth | ❌ Manual | ✅ Built-in | ✅ Built-in | ❌ No |
| JavaScript | ❌ No | ❌ No | ❌ No | ✅ Yes |
| Screenshots | ❌ No | ❌ No | ❌ No | ✅ Yes |

---

## Installation Recommendations

### Install These First (Highest Impact)

```bash
# 1. xh - HTTP client (Rust, fast)
cargo install xh
# or
brew install xh

# 2. bat - Better cat (Rust, syntax highlighting)
cargo install bat
# or
brew install bat

# 3. ripgrep - Better grep (Rust, fast)
cargo install ripgrep
# or
brew install ripgrep

# 4. eza - Better ls (Rust, modern)
cargo install eza
# or
brew install eza

# 5. surge - Static hosting (Node)
npm install -g surge
```

### Skills to Add

1. **xh-skill** - Replace curl for API calls
2. **bat-skill** - File reading with highlighting
3. **surge-skill** - One-command static hosting
4. **eza-skill** - Modern ls replacement
5. **ripgrep-skill** - Fast searching

---

## Summary

### What I Should Do

1. **Keep:** github, discord, coolify, hn, web, summarize, weather
2. **Add:** xh, bat, ripgrep, eza, surge
3. **Update:** web skill to use xh for API calls
4. **Replace:** curl with xh for most operations

### Tools Better Than Curl

| Tool | Best For | Install |
|------|----------|---------|
| **xh** | API testing, JSON | `cargo install xh` |
| **httpie** | Human-friendly requests | `pip install httpie` |
| **surge** | Static site deploy | `npm i -g surge` |

### My Demo Website Assessment

- **Current:** Manual Docker deploy via Coolify
- **Better:** `surge` or `vercel` for one-command deploy
- **Recommendation:** Add surge-skill for quick demos

---

## LLM-Specific & AI Agent Tools

### Web Scraping & Content Extraction for LLMs

#### 1. **Jina AI Reader** (r.jina.ai) - ⭐ 9,600+
```
URL: https://github.com/jina-ai/reader

Usage:
  curl https://r.jina.ai/http://example.com
  curl -H "Accept: application/json" https://r.jina.ai/http://example.com

Features:
  ✅ Converts any URL to LLM-friendly markdown
  ✅ Automatic content extraction (removes ads/nav)
  ✅ SPA (JavaScript) rendering support
  ✅ Streaming mode for real-time processing
  ✅ JSON output option
  ✅ Generated alt text for images
  ✅ No API key needed (free tier available)
```

**Why It's Better Than Curl:**
- Curl just gets raw HTML
- Jina Reader extracts meaningful content
- Handles JavaScript-rendered pages
- Outputs clean markdown for LLMs

#### 2. **Firecrawl** - ⭐ 74,600+
```
URL: https://github.com/firecrawl/firecrawl
Site: https://firecrawl.dev

Features:
  ✅ Turn entire websites into LLM-ready markdown
  ✅ Intelligent link discovery
  ✅ JavaScript rendering
  ✅ Proxy rotation
  ✅ Rate limiting protection
  ✅ Markdown, HTML, or JSON output

Install: npm install -g @firecrawl/cli

Usage:
  firecrawl scrape https://example.com --format markdown
  firecrawl crawl https://example.com --limit 100
```

**Use Cases:**
- Scrape documentation sites
- Build knowledge bases from websites
- Extract content for RAG systems

#### 3. **Unstructured IO** - ⭐ 13,600+
```
URL: https://github.com/unstructured-io/unstructured

Features:
  ✅ Convert documents to structured data
  ✅ PDF, Word, PowerPoint, HTML, Markdown support
  ✅ Extract tables, images, metadata
  ✅ Local processing (no data leaves your machine)

Install: pip install unstructured

Usage:
  from unstructured.partition.html import partition_html
  elements = partition_html(filename="example.html")
```

**Why It Matters:**
- PDFs/documents → LLM-ready chunks
- Preserves document structure
- Free and open source

---

### Browser Automation for AI Agents

#### 4. **Browser Use** - ⭐ 75,300+
```
URL: https://github.com/browser-use/browser-use

Features:
  ✅ Make websites accessible for AI agents
  ✅ Browser automation via Python
  ✅ Click, type, scroll, extract
  ✅ Vision capabilities
  ✅ Multi-step task automation

Install: pip install browser-use

Use Case:
  AI agents can browse the web autonomously
  Example: "Find and book a restaurant near me"
```

#### 5. **Playwright** - ⭐ 81,100+
```
URL: https://github.com/microsoft/playwright

Features:
  ✅ Web testing and automation
  ✅ Chromium, Firefox, WebKit support
  ✅ Auto-wait for elements
  ✅ Network interception
  ✅ Screenshots and PDFs

Install: npm install playwright
         npx playwright install

Why It's Better Than Puppeteer:
  ✅ Faster execution
  ✅ Better auto-waiting
  ✅ Built-in test runner
  ✅ Mobile device emulation
```

---

### Model Context Protocol (MCP)

#### 6. **MCP Servers** - ⭐ 76,000+
```
URL: https://github.com/modelcontextprotocol/servers

What is MCP?
  Standardized way for AI agents to connect to tools
  Like "USB-C for AI agents"

Key Servers:
  - filesystem: Local file operations
  - github: GitHub API integration
  - postgres: Database queries
  - fetch: Web content extraction
  - memory: Persistent context storage

Install MCP CLI:
  npm install -g @modelcontextprotocol/cli
```

---

### Specialized LLM Tools

#### 7. **yt-dlp** - ⭐ 141,600+
```
URL: https://github.com/yt-dlp/yt-dlp

Features:
  ✅ Download YouTube videos/audio
  ✅ Extract transcripts
  ✅ Support for 1700+ sites
  ✅ Use with summarize tool

Install: pip install yt-dlp

Usage:
  yt-dlp --write-auto-subs https://youtube.com/watch?v=...
  yt-dlp -x --audio-format mp3 https://youtube.com/watch?v=...
```

#### 8. **AgentOps** - ⭐ 5,200+
```
URL: https://github.com/AgentOps-AI/agentops

Features:
  ✅ AI agent monitoring
  ✅ LLM cost tracking
  ✅ Benchmarking
  ✅ Session recording

Install: pip install agentops

Use Case:
  Track your AI agent sessions and costs
```

#### 9. **Composio** - ⭐ 26,300+
```
URL: https://github.com/ComposioHQ/composio

Features:
  ✅ 100+ tool integrations for AI agents
  ✅ GitHub, Jira, Slack, Google, etc.
  ✅ MCP-compatible

Install: pip install composio-core

Use Case:
  Give your agents access to many services
```

---

## Recommended LLM-Specific Skills to Add

### Priority 1: Jina Reader Skill
```python
# Quick URL to markdown
curl https://r.jina.ai/http://example.com

# JSON output
curl -H "Accept: application/json" https://r.jina.ai/http://example.com
```

### Priority 2: Firecrawl Skill
```bash
# Install
npm install -g @firecrawl/cli

# Scrape to markdown
firecrawl scrape https://docs.example.com --format markdown
```

### Priority 3: yt-dlp + Summarize Combo
```bash
# Get YouTube transcript
yt-dlp --write-auto-subs -o transcript.txt https://youtube.com/watch?v=...

# Summarize
summarize transcript.txt --model gemini-flash
```

### Priority 4: Browser Use Skill
```python
from browser_use import Controller

controller = Controller()
# AI can now browse autonomously
```

---

## Tool Selection Decision Tree

```
Need to fetch web content?
├── Simple page → use r.jina.ai (free, no install)
├── JavaScript/SPA → use r.jina.ai with x-wait-for-selector
├── Full website → use firecrawl
└── Interactive → use browser-use

Need to process documents?
├── PDFs/docs → use unstructured-io
└── Word/PPT → use unstructured-io

Need browser automation?
├── Testing → use playwright
└── AI agent → use browser-use

Need YouTube?
├── Download → use yt-dlp
└── Transcript → use yt-dlp --write-auto-subs
```

---

## Installation Priority

```bash
# Priority 1: No-install tools (use directly)
# r.jina.ai - just curl it!
curl https://r.jina.ai/http://example.com

# Priority 2: Quick installs
pip install yt-dlp  # YouTube downloads
npm install -g @firecrawl/cli  # Web scraping

# Priority 3: Full frameworks
pip install unstructured  # Document processing
pip install browser-use  # AI browser automation
```

---

## Summary: LLM-Specific Tools

| Tool | Purpose | Why It's Special |
|------|---------|------------------|
| **r.jina.ai** | URL → LLM markdown | Free, no install, works via curl |
| **firecrawl** | Full website scraping | Discovers all links, JavaScript support |
| **unstructured-io** | Document → chunks | Local processing, preserves structure |
| **browser-use** | AI browser automation | Let AI browse for you |
| **yt-dlp** | YouTube + transcripts | Works with summarize skill |
| **MCP servers** | Standardized tools | Like USB-C for AI agents |

---

🦞 *Analysis complete - LLM-specific tools that supercharge AI workflows*
