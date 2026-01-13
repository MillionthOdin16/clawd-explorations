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

🦞 *Analysis complete - tools ranked by impact and ease of use*
