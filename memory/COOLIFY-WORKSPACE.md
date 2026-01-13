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

**List Databases:**
```bash
curl -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/databases"
```

**Get Application Details:**
```bash
curl -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/applications/{uuid}"
```

**Start/Stop Application:**
```bash
# Start
curl -X POST -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/applications/{uuid}/start"

# Stop
curl -X POST -H "Authorization: Bearer $COOLIFY_API_KEY" \
  "https://coolify.bradarr.com/api/v1/applications/{uuid}/stop"
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

### Option 1: Dashboard (Recommended)
1. Go to https://coolify.bradarr.com
2. Navigate to "Clawd Workspace" project
3. Click "Add Application"
4. Configure:
   - **Source:** GitHub repository
   - **Build Pack:** Based on app type
   - **FQDN:** Your subdomain (e.g., myapp.bradarr.com)
   - **Environment:** Production

### Option 2: API
```bash
# Create application (requires proper configuration)
POST /api/v1/environments/{environment_uuid}/applications
{
  "name": "My App",
  "fqdn": "myapp.bradarr.com",
  "git_repository": "owner/repo",
  "git_branch": "main",
  "build_pack": "nixpacks"
}
```

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

## Next Steps

1. **Create GitHub repos** for each tool/dashboard I want to deploy
2. **Deploy Welcome Dashboard** at `welcome.bradarr.com`
3. **Set up databases** for persistent data storage
4. **Document each deployment** with its purpose and configuration

---

🦞 *My personal deployment workspace*
