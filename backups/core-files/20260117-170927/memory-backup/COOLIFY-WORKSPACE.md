# 🦞 Clawd's Coolify Workspace

**Created:** 2026-01-13 03:01 UTC
**Last Updated:** 2026-01-14 17:45 UTC (v2.2.0)
**Purpose:** Personal workspace for deploying tools, dashboards, and experiments

---

## Coolify Account

- **Dashboard:** https://coolify.bradarr.com
- **API Base:** https://coolify.bradarr.com/api/v1
- **API Key:** `6|ShyBUVU2l9GG7jjjIyRObXNPUVxOqPMarcMWgjDf9c36076b`

---

## Workspace Structure

### Project (Clawd Workspace)
- **UUID:** `jws4w4cc040444gk0ok0ksgk`
- **Environment:** Production - `g4wo8s0g48ogggkgwosc4sgs`
- **Server:** Localhost - `ykg8kc80k4wsock8so4swk04`

---

## 🎯 THE CORRECT WAY (v2.2.0)

### Quick Deploy with Validation

```python
from scripts.coolify import CoolifyAPI

api = CoolifyAPI()

# Validate inputs first
if not api.validators.validate_repository_url("https://github.com/user/repo"):
    print("Invalid repository URL")
    exit(1)

# Create application (auto subdomain)
app = api.apps_create(
    name="my-app",
    repository="https://github.com/user/repo",
    build_pack="dockerfile",
    branch="main"
)

# Add custom domain
api.apps_add_domain(app['uuid'], "my-app.bradarr.com")

# Deploy and wait for completion
result = api.apps_wait_for_deployment(app['uuid'], timeout=300)
print(result['message'])
```

### Helper Functions (v2.2.0)

```python
# Health check
if not api.health_check():
    print("API not accessible!")

# Get all resource counts
counts = api.get_resource_counts()
# Returns: {"applications": 9, "projects": 8, "servers": 1, ...}

# Find app by name
app = api.find_app_by_name("jj-celebration")

# Find app by domain
app = api.find_app_by_domain("jj.bradarr.com")

# Check if healthy
if api.apps_is_healthy(app['uuid']):
    print("App is running and healthy!")
```

# 3. Deploy
api.apps_deploy(app['uuid'])
```

### Quick CLI Commands

```bash
# Status
python scripts/coolify.py status

# List apps
python scripts/coolify.py apps list

# Get app details
python scripts/coolify.py apps get --uuid <uuid>

# Get logs
python scripts/coolify.py apps logs --uuid <uuid>

# Deploy
python scripts/coolify.py apps deploy --uuid <uuid>
```

---

## ✅ VERIFIED WORKING ENDPOINTS

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/applications` | GET | List all applications |
| `/api/v1/applications/{uuid}` | GET | Get app details |
| `/api/v1/applications/public` | POST | **Create application** |
| `/api/v1/applications/{uuid}` | PATCH | Update app (no fqdn!) |
| `/api/v1/applications/{uuid}` | DELETE | Delete application |
| `/api/v1/deploy?uuid={uuid}&force=true` | POST | **Deploy app** |
| `/api/v1/applications/{uuid}/restart` | POST | Restart |
| `/api/v1/applications/{uuid}/start` | POST | Start |
| `/api/v1/applications/{uuid}/stop` | POST | Stop |
| `/api/v1/applications/{uuid}/logs` | GET | Get logs |
| `/api/v1/projects` | GET | List projects |
| `/api/v1/projects/{uuid}` | GET | Get project |
| `/api/v1/deployments` | GET | List deployments |

---

## ❌ BROKEN ENDPOINTS (Don't Use)

| Endpoint | Method | Error |
|----------|--------|-------|
| `/api/v1/applications` | POST | 404 Not found |
| `/api/v1/applications` | PUT | 404 Not found |
| `/api/v1/environments` | GET | "Not found" |

---

## 🚨 COMMON ERRORS & FIXES

### Error: "git_repository must start with https://, http://, git://, or git@"
**Fix:** Add protocol to repository URL:
```python
# Wrong
repository="github.com/user/repo"

# Correct
repository="https://github.com/user/repo"
```

### Error: "This field is not allowed" (fqdn)
**Fix:** Use `custom_labels` approach instead:
```python
# Wrong - trying to update fqdn
api.apps_update(uuid, fqdn="my-app.bradarr.com")  # Fails!

# Correct - use apps_add_domain
api.apps_add_domain(uuid, "my-app.bradarr.com")  # Works!
```

### Error: 404 on POST /applications
**Fix:** Use `/applications/public`:
```python
# Wrong
api._request("POST", "/applications", data)  # 404!

# Correct
api._request("POST", "/applications/public", data)  # Works!
```

### Error: Application stuck at "exited:unhealthy"
**Fix:** Check logs:
```python
logs = api.apps_logs(uuid)
print(logs['logs'])
```
Common causes: missing Dockerfile, wrong build_pack, docker build failure

---

## 📋 API Usage Examples

### Create Application
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://coolify.bradarr.com/api/v1/applications/public" \
  -d '{
    "name": "jj-celebration",
    "project_uuid": "jws4w4cc040444gk0ok0ksgk",
    "environment_uuid": "g4wo8s0g48ogggkgwosc4sgs",
    "server_uuid": "ykg8kc80k4wsock8so4swk04",
    "git_repository": "https://github.com/MillionthOdin16/jj-celebration",
    "git_branch": "main",
    "build_pack": "dockerfile",
    "ports_exposes": "80"
  }'
# Returns: {"uuid": "w8ogsc44w0cswcww8wwwg8o4", "domains": "https://..."}
```

### Add Custom Domain
```python
# Using the helper method
api.apps_add_domain("w8ogsc44w0cswcww8wwwg8o4", "jj.bradarr.com")
```

### Deploy
```bash
curl -X POST "https://coolify.bradarr.com/api/v1/deploy?uuid={uuid}&force=true"
```

---

## 🏗️ Build Packs

| Pack | Use Case |
|------|----------|
| `dockerfile` | Custom Docker builds (MOST COMMON) |
| `dockercompose` | Multi-container apps |
| `nixpacks` | Auto-detect frameworks |
| `static` | Static HTML sites |
| `dockerimage` | Pre-built containers |

---

## 📦 Deployed Applications

| App | URL | Status |
|-----|-----|--------|
| jj-celebration | https://jj.bradarr.com | ✅ Running |
| clawd-demo-site | https://demo.bradarr.com | ✅ Running |

---

## 🎓 LESSONS LEARNED (2026-01-14)

### What Worked
1. ✅ `POST /api/v1/applications/public` - Creates app with auto subdomain
2. ✅ `PATCH /api/v1/applications/{uuid}` with `custom_labels` - Adds custom domain
3. ✅ `POST /api/v1/deploy?uuid={uuid}&force=true` - Triggers deployment
4. ✅ `GET /api/v1/applications/{uuid}/logs` - Returns logs

### What Didn't Work (and how to fix)
1. ❌ `POST /api/v1/applications` → Use `/applications/public`
2. ❌ PATCH with `fqdn` → Use `apps_add_domain()` with custom_labels
3. ❌ `GET /api/v1/environments` → Use project-based query

### Key Insights
- Repository URL MUST include protocol (https://, http://, git://, git@)
- Always use `force=true` on deploy for immediate rebuild
- Server UUID `ykg8kc80k4wsock8so4swk04` is localhost
- Custom domains require traefik configuration in custom_labels
- custom_labels are Base64-encoded traefik config

---

## 🧠 Memory

**Always check these first when troubleshooting:**
1. Is the repository URL correct and has protocol prefix?
2. Does the app have a valid Dockerfile (if using dockerfile build_pack)?
3. Check logs: `api.apps_logs(uuid)`
4. Use `force=true` when deploying to rebuild

**Quick deploy checklist:**
- [ ] Repository exists and is accessible
- [ ] Dockerfile present (for dockerfile build_pack)
- [ ] Create with `/applications/public`
- [ ] Add domain via `apps_add_domain()`
- [ ] Deploy with `force=true`

---

🦞 *Deploy with confidence*
