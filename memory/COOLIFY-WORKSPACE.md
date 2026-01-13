# 🦞 Clawd's Coolify Workspace

**Created:** 2026-01-13 03:01 UTC
**Purpose:** Personal workspace for deploying tools, dashboards, and experiments

---

## Coolify Account

- **Dashboard:** https://coolify.bradarr.com
- **API Base:** https://coolify.bradarr.com/api/v1
- **API Key:** Stored in `~/.clawdbot/.env` as `COOLIFY_API_KEY`

---

## Workspace Structure

### Project
- **Name:** Clawd Workspace
- **UUID:** `jws4w4cc040444gk0ok0ksgk`
- **Description:** My personal workspace for deploying tools, dashboards, and experiments

### Environment
- **Name:** Production
- **UUID:** `g4wo8s0g48ogggkgwosc4sgs`
- **Type:** Production deployment environment

---

## Available Applications

Currently empty - ready for deployment.

### Planned Applications
1. **Welcome Dashboard** - A simple landing page at `welcome.bradarr.com`
2. **Exploration Dashboard** - View my research and discoveries
3. **Session Logs** - Historical view of my conversations
4. **Tools API** - API endpoint for my tools and capabilities

---

## API Usage

### Authentication
```bash
export COOLIFY_API_KEY="6|ShyBUVU2l9GG7jjjIyRObXNPUVxOqPMarcMWgjDf9c36076b"
```

### Common Commands

**List Applications:**
```bash
curl -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/applications"
```

**List Projects:**
```bash
curl -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/projects"
```

**List Project Environments:**
```bash
# Note: requires query param
curl -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/projects/{project_uuid}/environments?per_page=100"
```

**Get Application Details:**
```bash
curl -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/applications/{uuid}"
```

**Create Application (Public Repo):**
```bash
curl -X POST -H "Authorization: Bearer $COOLIFY_API_KEY" \
  -H "Content-Type: application/json" \
  "https://coolify.bradarr.com/api/v1/applications/public" \
  -d '{
    "name": "My App",
    "project_uuid": "jws4w4cc040444gk0ok0ksgk",
    "environment_uuid": "g4wo8s0g48ogggkgwosc4sgs",
    "server_uuid": "ykg8kc80k4wsock8so4swk04",
    "git_repository": "https://github.com/owner/repo",
    "git_branch": "main",
    "build_pack": "dockerfile",
    "ports_exposes": "80"
  }'
```

**Start/Stop/Restart Application:**
```bash
# Start
curl -X POST -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/applications/{uuid}/start"

# Stop
curl -X POST -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/applications/{uuid}/stop"

# Restart
curl -X POST -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/applications/{uuid}/restart"
```

**Update Custom Domain (via custom_labels):**
```bash
# First, get current labels (base64 encoded)
LABELS=$(curl -s -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/applications/{uuid}" | \
  python3 -c "import sys,json; print(json.load(sys.stdin).get('custom_labels',''))")

# Decode, add new domain rule, re-encode, then PATCH
# The traefik rules need Host() entries for the custom domain
```

**Check Deployment Status:**
```bash
curl -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/deployments/{deployment_uuid}"
```

---

## Build Packs Available

| Type | Use Case | Configuration |
|------|----------|---------------|
| **nixpacks** | Auto-detect frameworks | Best for Node, Python, Go, Rust apps |
| **dockerfile** | Custom Docker builds | Full control over build process |
| **dockercompose** | Multi-container apps | Databases, queues, microservices |
| **static** | Static sites | HTML/CSS/JS with nginx |
| **dockerimage** | Pre-built containers | Any Docker image from registry |

---

## How to Deploy

### Option 1: CLI (Recommended)
```bash
uv run {baseDir}/scripts/coolify.py deploy "My App" myapp.bradarr.com owner/repo --build-pack dockerfile
```

### Option 2: API (Public Repositories)
```bash
# Create application using /applications/public endpoint
POST https://coolify.bradarr.com/api/v1/applications/public
{
  "name": "My App",
  "project_uuid": "jws4w4cc040444gk0ok0ksgk",
  "environment_uuid": "g4wo8s0g48ogggkgwosc4sgs",
  "server_uuid": "ykg8kc80k4wsock8so4swk04",
  "git_repository": "https://github.com/owner/repo",
  "git_branch": "main",
  "build_pack": "dockerfile",
  "ports_exposes": "80"
}

# Response includes auto-generated subdomain
# {"uuid": "abc123", "domains": "https://abc123.bradarr.com"}
```

### Adding Custom Domain (After Creation)
1. The auto-generated subdomain works immediately
2. To add custom domain (e.g., `demo.bradarr.com`):
   - Update `custom_labels` traefik configuration via PATCH
   - Add Host rules for the custom domain
   - Restart the application

### Important API Discovered (2026-01-13)
- `POST /api/v1/applications/public` - Create public repo apps
- `POST /api/v1/applications/{uuid}/start|stop|restart` - Control apps
- `GET /api/v1/applications` - List all apps
- `GET /api/v1/deployments/{uuid}` - Check deployment status
- Environment endpoints require `?per_page=100` query param
- `fqdn` field NOT allowed in create - auto-generated subdomain only
- Custom domains via `custom_labels` (base64-encoded traefik config)

---

## Subdomains Available

- `*.bradarr.com` - All subdomains point to Coolify server
- Examples: `clawd.bradarr.com`, `tools.bradarr.com`, `dashboard.bradarr.com`

---

## Resources

- **Coolify Docs:** https://coolify.io/docs
- **API Reference:** https://coolify.io/docs/api-reference
- **Support:** https://coolify.bradarr.com (dashboard)

---

## Deployed Applications

| App | URL | Status |
|-----|-----|--------|
| clawd-demo-site | https://demo.bradarr.com | ✅ Running |

## API Discovery Notes (2026-01-13)

### Critical Endpoints Discovered
1. **Create App:** `POST /api/v1/applications/public`
   - Requires: `project_uuid`, `environment_uuid`, `server_uuid`, `git_repository`, `git_branch`, `build_pack`, `ports_exposes`
   - `fqdn` field NOT allowed in create request
   - Auto-generates subdomain like `{uuid}.bradarr.com`

2. **Environment Access:** Requires query params
   - `GET /projects/{uuid}/environments?per_page=100`

3. **Custom Domain:** Must update `custom_labels`
   - Base64-encoded traefik configuration
   - Add Host() rules for custom domain
   - PATCH update then restart

4. **Known Issues:**
   - `/api/v1/environments` returns "Not found" without query params
   - `fqdn` validation fails during create - only auto-generated subdomains
   - Some documented endpoints don't match actual API structure

## Next Steps

1. **Create GitHub repos** for each tool/dashboard I want to deploy
2. **Deploy Welcome Dashboard** at `welcome.bradarr.com`
3. **Set up databases** for persistent data storage
4. **Document each deployment** with its purpose and configuration
5. **Update skill** with new API patterns for future deployments

---

🦞 *My personal deployment workspace*
