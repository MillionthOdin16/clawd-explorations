---
name: coolify
description: Deploy and manage applications on Coolify self-hosted platform. List apps, databases, services, start/stop deployments, and manage your workspace.
homepage: https://coolify.bradarr.com
metadata: {"clawdbot":{"emoji":"🚀","requires":{"env":["COOLIFY_API_KEY"]}}}
---

# Coolify - Deployment Platform

Manage your Coolify deployments from the command line.

## Setup

**1. API Key:**
Get your API key from https://coolify.bradarr.com → Settings → API Keys.

**2. Set it in your environment:**
```bash
export COOLIFY_API_KEY="your-api-key"
```

Or add to `~/.clawdbot/.env`:
```bash
COOLIFY_API_KEY="your-api-key"
```

## Commands

### Applications
```bash
uv run {baseDir}/scripts/coolify.py apps list              # List all apps
uv run {baseDir}/scripts/coolify.py apps get <uuid>        # Get app details
uv run {baseDir}/scripts/coolify.py apps logs <uuid>       # Get app logs
uv run {baseDir}/scripts/coolify.py apps watch <uuid>      # Monitor status
uv run {baseDir}/scripts/coolify.py apps start <uuid>      # Start app
uv run {baseDir}/scripts/coolify.py apps stop <uuid>       # Stop app
uv run {baseDir}/scripts/coolify.py apps restart <uuid>    # Restart app
uv run {baseDir}/scripts/coolify.py apps delete <uuid>     # Delete app
```

### Deploy New Application
```bash
uv run {baseDir}/scripts/coolify.py deploy <name> <fqdn> <repo> [--branch main] [--build-pack nixpacks] [--project <uuid>] [--environment <uuid>]
```

**Example:**
```bash
# Deploy a Node.js app
uv run {baseDir}/scripts/coolify.py deploy "My Dashboard" dashboard.bradarr.com owner/repo --branch main --build-pack nixpacks

# Deploy with Dockerfile
uv run {baseDir}/scripts/coolify.py deploy "API" api.bradarr.com owner/api --build-pack dockerfile

# Deploy with explicit project/environment
uv run {baseDir}/scripts/coolify.py deploy "Demo" demo.bradarr.com owner/repo --project jws4w4cc040444gk0ok0ksgk --environment g4wo8s0g48ogggkgwosc4sgs
```

**Important Notes:**
- `fqdn` is NOT set during creation - Coolify auto-generates a subdomain
- Custom domain is added via traefik `custom_labels` after deployment
- Required fields: `project_uuid`, `environment_uuid` (or `environment_name`), `server_uuid`, `git_repository`, `git_branch`, `build_pack`, `ports_exposes`

### Databases
```bash
uv run {baseDir}/scripts/coolify.py dbs list               # List databases
uv run {baseDir}/scripts/coolify.py dbs get <uuid>         # Get DB details
```

### Services
```bash
uv run {baseDir}/scripts/coolify.py services list          # List services
```

### Projects
```bash
uv run {baseDir}/scripts/coolify.py projects list          # List projects
```

### Raw Output
```bash
uv run {baseDir}/scripts/coolify.py apps list --raw        # Raw JSON output
uv run {baseDir}/scripts/coolify.py dbs list --raw         # Raw JSON output
```

## Examples

**List your applications:**
```bash
uv run {baseDir}/scripts/coolify.py apps list
```

**Check a specific application:**
```bash
uv run {baseDir}/scripts/coolify.py apps get jws4w4cc040444gk0ok0ksgk
```

**Start a stopped application:**
```bash
uv run {baseDir}/scripts/coolify.py apps start <uuid>
```

**Check database status:**
```bash
uv run {baseDir}/scripts/coolify.py dbs list
```

## API

Uses Coolify REST API at `https://coolify.bradarr.com/api/v1`.

- **Authentication:** Bearer token (`COOLIFY_API_KEY`)
- **Documentation:** https://coolify.io/docs/api-reference
