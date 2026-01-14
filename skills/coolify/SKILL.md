---
name: coolify
description: Complete Coolify API integration. Deploy and manage applications, projects, environments, databases, services, and resources. Full CRUD operations, deployments, logs, and status monitoring.
homepage: https://coolify.bradarr.com
metadata: {"clawdbot":{"emoji":"🚀","requires":{"env":["COOLIFY_API_KEY"]}}}
---

# Coolify - Complete Deployment Platform Integration

Deploy and manage applications, databases, services, and infrastructure on Coolify self-hosted platform.

## Status

**✅ INSTALLED** via npm
```bash
npm install -g coolify
which coolify  # /home/opc/.nvm/versions/node/v22.20.0/bin/coolify
```

## Setup

**1. Get API Key:**
Get your API key from https://coolify.bradarr.com → Settings → API Keys.

**2. Set environment variable:**
```bash
export COOLIFY_API_TOKEN="your-api-token"
```

Or add to `~/.clawdbot/.env`:
```bash
COOLIFY_API_TOKEN="your-api-token"
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `python scripts/coolify.py status` | Quick status overview |
| `python scripts/coolify.py apps list` | List all applications |
| `python scripts/coolify.py apps get <uuid>` | Get app details |
| `python scripts/coolify.py apps deploy <uuid>` | Trigger deployment |
| `python scripts/coolify.py apps logs <uuid>` | Get application logs |
| `python scripts/coolify.py apps restart <uuid>` | Restart application |
| `python scripts/coolify.py projects list` | List all projects |
| `python scripts/coolify.py deployments list` | List deployments |
| `python scripts/coolify.py databases list` | List databases |
| `python scripts/coolify.py services list` | List services |
| `python scripts/coolify.py resources --project <uuid>` | List all project resources |

---

## Applications

### List Applications
```bash
python scripts/coolify.py apps list

# With expanded details
python scripts/coolify.py apps list --expand
```

**Output:**
```
============================================================
APPLICATIONS (2 total)
============================================================

🟢 clawd-demo-site
   UUID: gw48wk08owg4ckkwc0sckk84
   FQDN: gw48wk08owg4ckkwc0sckk84.bradarr.com
   Status: running
   Repo: MillionthOdin16/clawd-demo-site
```

### Get Application Details
```bash
python scripts/coolify.py apps get <uuid>
```

**Includes:** Name, FQDN, status, repository, branch, commit, Docker config, health checks, resource limits, created/updated timestamps.

### Trigger Deployment
```bash
python scripts/coolify.py apps deploy <uuid>
```

### Restart Application
```bash
python scripts/coolify.py apps restart <uuid>
```

### Start/Stop Application
```bash
python scripts/coolify.py apps start <uuid>
python scripts/coolify.py apps stop <uuid>
```

### Get Application Logs
```bash
python scripts/coolify.py apps logs <uuid>
python scripts/coolify.py apps logs <uuid> --count 50  # Last 50 entries
```

---

## Projects

### List Projects
```bash
python scripts/coolify.py projects list
```

### Get Project
```bash
python scripts/coolify.py projects get <uuid>
```

### Create Project
```bash
python scripts/coolify.py projects create --name "My Project" --description "Description"
```

### Update Project
```bash
python scripts/coolify.py projects update <uuid> --name "New Name"
```

### Delete Project
```bash
python scripts/coolify.py projects delete <uuid>
```

---

## Environments

### List Environments
```bash
python scripts/coolify.py environments list --project <project_uuid>
```

### Create Environment
```bash
python scripts/coolify.py environments create --project <uuid> --name "Production" --production
```

---

## Deployments

### List Deployments
```bash
# All deployments
python scripts/coolify.py deployments list

# For specific application
python scripts/coolify.py deployments list --application <uuid>
```

**Output:**
```
============================================================
DEPLOYMENTS (10 total)
============================================================

✅ Fix deployment error
   Status: completed
   Commit: a5f7e8d
   Created: 2026-01-14 04:50:30
```

### Cancel Deployment
```bash
python scripts/coolify.py deployments cancel <uuid>
```

### Retry Deployment
```bash
python scripts/coolify.py deployments retry <uuid>
```

---

## Databases

### List Databases
```bash
python scripts/coolify.py databases list
python scripts/coolify.py databases list --project <uuid>
```

### Get Database Details
```bash
python scripts/coolify.py databases get <uuid>
```

### Trigger Backup
```bash
python scripts/coolify.py databases backup <uuid>
```

### Restore from Backup
```bash
python scripts/coolify.py databases restore <uuid> --backup <backup_uuid>
```

### Delete Database
```bash
python scripts/coolify.py databases delete <uuid>
```

---

## Services

### List Services
```bash
python scripts/coolify.py services list
python scripts/coolify.py services list --project <uuid>
```

### Get Service Details
```bash
python scripts/coolify.py services get <uuid>
```

### Restart Service
```bash
python scripts/coolify.py services restart <uuid>
```

### Delete Service
```bash
python scripts/coolify.py services delete <uuid>
```

---

## Resources (All-in-One)

### List All Resources in Project
```bash
python scripts/coolify.py resources list --project <uuid>
```

Shows applications, databases, and services together.

---

## Status Dashboard

### Quick Overview
```bash
python scripts/coolify.py status
```

**Output:**
```
============================================================
COOLIFY STATUS
============================================================

📦 Applications: 2 (2 running)
📁 Projects: 1
🗄️  Databases: 0
🔧 Services: 0

🔗 API URL: https://coolify.bradarr.com
✅ API: Connected
```

---

## Common Patterns

### Pattern 1: Deploy Updated Code
```bash
# 1. Make code changes to git
git add . && git commit -m "Update" && git push

# 2. Find application UUID
python scripts/coolify.py apps list

# 3. Trigger deployment
python scripts/coolify.py apps deploy <uuid>

# 4. Watch logs
python scripts/coolify.py apps logs <uuid>
```

### Pattern 2: Check Deployment History
```bash
# List deployments
python scripts/coolify.py deployments list --application <uuid>

# Get details
python scripts/coolify.py deployments get <deployment_uuid>
```

### Pattern 3: Manage Multiple Environments
```bash
# List environments
python scripts/coolify.py environments list --project <uuid>

# Deploy to production
python scripts/coolify.py apps deploy <uuid>
```

### Pattern 4: Debug Application Issues
```bash
# Check status
python scripts/coolify.py apps get <uuid>

# Check logs
python scripts/coolify.py apps logs <uuid> --count 200

# Check deployments
python scripts/coolify.py deployments list --application <uuid>
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `COOLIFY_API_TOKEN` | API token for authentication |
| `COOLIFY_API_URL` | API URL (default: https://coolify.bradarr.com) |

---

## API Reference

### Endpoints Implemented

| Category | Endpoint | Method | Status |
|----------|----------|--------|--------|
| **Applications** | | | |
| List | `/applications` | GET | ✅ |
| Get | `/applications/{uuid}` | GET | ✅ |
| Create | `/applications` | POST | ✅ |
| Update | `/applications/{uuid}` | PUT | ✅ |
| Delete | `/applications/{uuid}` | DELETE | ✅ |
| Deploy | `/deploy` | POST | ✅ |
| Restart | `/applications/{uuid}/restart` | POST | ✅ |
| Start | `/applications/{uuid}/start` | POST | ✅ |
| Stop | `/applications/{uuid}/stop` | POST | ✅ |
| Logs | `/applications/{uuid}/logs` | GET | ✅ |
| **Projects** | | | |
| List | `/projects` | GET | ✅ |
| Get | `/projects/{uuid}` | GET | ✅ |
| Create | `/projects` | POST | ✅ |
| Update | `/projects/{uuid}` | PUT | ✅ |
| Delete | `/projects/{uuid}` | DELETE | ✅ |
| **Environments** | | | |
| List | `/projects/{uuid}/environments` | GET | ✅ |
| Get | `/environments/{uuid}` | GET | ✅ |
| Create | `/projects/{uuid}/environments` | POST | ✅ |
| Update | `/environments/{uuid}` | PUT | ✅ |
| Delete | `/environments/{uuid}` | DELETE | ✅ |
| **Deployments** | | | |
| List | `/deployments` | GET | ✅ |
| Get | `/deployments/{uuid}` | GET | ✅ |
| Cancel | `/deployments/{uuid}/cancel` | POST | ✅ |
| Retry | `/deployments/{uuid}/retry` | POST | ✅ |
| **Databases** | | | |
| List | `/databases` | GET | ✅ |
| Get | `/databases/{uuid}` | GET | ✅ |
| Create | `/databases` | POST | ✅ |
| Backup | `/databases/{uuid}/backup` | POST | ✅ |
| Restore | `/databases/{uuid}/restore` | POST | ✅ |
| Delete | `/databases/{uuid}` | DELETE | ✅ |
| **Services** | | | |
| List | `/services` | GET | ✅ |
| Get | `/services/{uuid}` | GET | ✅ |
| Create | `/services` | POST | ✅ |
| Update | `/services/{uuid}` | PUT | ✅ |
| Delete | `/services/{uuid}` | DELETE | ✅ |
| Restart | `/services/{uuid}/restart` | POST | ✅ |
| **Resources** | | | |
| List | `/projects/{uuid}/resources` | GET | ✅ |

---

## See Also

- **Quick Reference:** `QUICK-REF.md`
- **Full API Docs:** https://coolify.io/docs/api-reference
- **Coolify Dashboard:** https://coolify.bradarr.com
