#!/usr/bin/env python3
"""Coolify CLI - Manage deployments on Coolify (v2.2.0).

Provides convenient commands for:
- Listing and managing applications
- Creating and deploying applications
- Managing custom domains
- Monitoring deployment status

Usage:
    python scripts/coolify.py <command> [options]

Examples:
    python scripts/coolify.py apps list
    python scripts/coolify.py apps get --uuid <uuid>
    python scripts/coolify.py apps deploy --uuid <uuid>
    python scripts/coolify.py apps wait --uuid <uuid>
    python scripts/coolify.py status
"""

import argparse
import json
import os
import sys
import time
import base64
from typing import Any, Dict, List, Optional, Tuple

# Configuration
API_URL = os.environ.get("COOLIFY_API_URL", "https://coolify.bradarr.com")
API_TOKEN = os.environ.get("COOLIFY_API_TOKEN", "")


class CoolifyValidators:
    """Validators for Coolify API inputs."""
    
    @staticmethod
    def validate_uuid(uuid: str) -> bool:
        """Validate Coolify UUID format."""
        import re
        if not uuid or not isinstance(uuid, str):
            return False
        uuid_clean = uuid.strip().lower()
        full_pattern = r'^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}$'
        short_pattern = r'^[0-9a-z]{8,32}$'
        return bool(re.match(full_pattern, uuid_clean) or re.match(short_pattern, uuid_clean))
    
    @staticmethod
    def validate_repository_url(url: str) -> Optional[str]:
        """Validate git repository URL."""
        valid_prefixes = ['https://', 'http://', 'git://', 'git@']
        for prefix in valid_prefixes:
            if url.lower().startswith(prefix):
                return url
        return None
    
    @staticmethod
    def validate_domain(domain: str) -> Optional[str]:
        """Validate domain format."""
        import re
        if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)+$', domain):
            return domain
        return None
    
    @staticmethod
    def validate_build_pack(pack: str) -> Optional[str]:
        """Validate build pack."""
        valid = ['dockerfile', 'dockercompose', 'nixpacks', 'static', 'dockerimage']
        return pack if pack.lower() in valid else None


class CoolifyAPI:
    """Complete Coolify API client (v2.2.0)."""
    
    def __init__(self, api_url: str = None, api_token: str = None):
        self.api_url = api_url or API_URL
        self.api_token = api_token or API_TOKEN
        self.validators = CoolifyValidators()
        
        if not self.api_token:
            print("Error: COOLIFY_API_TOKEN not set")
            print("Set it with: export COOLIFY_API_TOKEN='your-token'")
    
    def _request(self, method: str, endpoint: str, data: Dict = None) -> Tuple[Optional[Any], bool]:
        """Make API request."""
        import urllib.request
        import urllib.error
        
        url = f"{self.api_url}/api/v1{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        
        req = urllib.request.Request(url, method=method, headers=headers)
        
        if data:
            req.data = json.dumps(data).encode('utf-8')
        
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result, True
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ""
            print(f"HTTP Error {e.code}: {error_body[:200]}")
            return None, False
        except Exception as e:
            print(f"Error: {e}")
            return None, False
    
    def health_check(self) -> bool:
        """Check if API is accessible."""
        apps, success = self._request("GET", "/applications")
        return success and apps is not None
    
    def apps_list(self) -> List[Dict]:
        """List all applications."""
        result, success = self._request("GET", "/applications")
        return result if success else []
    
    def apps_get(self, uuid: str) -> Optional[Dict]:
        """Get application details."""
        if not self.validators.validate_uuid(uuid):
            print(f"Invalid UUID format: {uuid}")
            return None
        result, success = self._request("GET", f"/applications/{uuid}")
        return result if success else None
    
    def apps_create(
        self,
        name: str,
        repository: str,
        project_uuid: str = "jws4w4cc040444gk0ok0ksgk",
        environment_uuid: str = "g4wo8s0g48ogggkgwosc4sgs",
        server_uuid: str = "ykg8kc80k4wsock8so4swk04",
        build_pack: str = "dockerfile",
        branch: str = "main"
    ) -> Optional[Dict]:
        """Create new application."""
        repo = self.validators.validate_repository_url(repository)
        if not repo:
            print("Error: Repository URL must start with https://, http://, git://, or git@")
            return None
        
        pack = self.validators.validate_build_pack(build_pack)
        if not pack:
            print(f"Error: Invalid build pack '{build_pack}'")
            return None
        
        data = {
            "name": name,
            "git_repository": repo,
            "git_branch": branch,
            "build_pack": pack,
            "project_uuid": project_uuid,
            "environment_uuid": environment_uuid,
            "server_uuid": server_uuid,
            "ports_exposes": "80",
        }
        result, success = self._request("POST", "/applications/public", data)
        return result if success else None
    
    def apps_deploy(self, uuid: str, force: bool = True) -> Optional[Dict]:
        """Trigger deployment."""
        if not self.validators.validate_uuid(uuid):
            print(f"Invalid UUID format: {uuid}")
            return None
        result, success = self._request("POST", f"/deploy?uuid={uuid}&force={force}", {})
        return result if success else None
    
    def apps_logs(self, uuid: str, count: int = 100) -> Dict:
        """Get application logs."""
        if not self.validators.validate_uuid(uuid):
            return {"logs": "Invalid UUID"}
        result, success = self._request("GET", f"/applications/{uuid}/logs?limit={count}")
        return result if success else {"logs": ""}
    
    def apps_status(self, uuid: str) -> str:
        """Get simplified status."""
        app = self.apps_get(uuid)
        if not app:
            return "not_found"
        status = app.get('status', 'unknown')
        if 'running' in status:
            return "running"
        elif 'exited' in status:
            return "stopped"
        return status
    
    def apps_wait_for_deployment(self, uuid: str, timeout: int = 300, poll_interval: int = 5) -> Dict:
        """Wait for deployment to complete."""
        if not self.validators.validate_uuid(uuid):
            return {"status": "error", "success": False, "message": "Invalid UUID"}
        
        deploy_result = self.apps_deploy(uuid, force=True)
        if not deploy_result:
            return {"status": "error", "success": False, "message": "Failed to trigger deployment"}
        
        deployment_uuid = deploy_result.get('deployments', [{}])[0].get('deployment_uuid', '')
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            app = self.apps_get(uuid)
            if app:
                app_status = app.get('status', '')
                if 'running' in app_status:
                    return {"status": "success", "success": True, "message": "Application is running"}
            time.sleep(poll_interval)
        
        return {"status": "timeout", "success": False, "message": f"Timeout after {timeout}s"}
    
    def apps_add_domain(self, uuid: str, domain: str) -> Optional[Dict]:
        """Add custom domain."""
        if not self.validators.validate_uuid(uuid):
            return None
        
        domain_valid = self.validators.validate_domain(domain)
        if not domain_valid:
            print(f"Invalid domain: {domain}")
            return None
        
        app = self.apps_get(uuid)
        if not app:
            return None
        
        current_labels = app.get('custom_labels', '')
        if current_labels:
            labels = base64.b64decode(current_labels).decode('utf-8')
        else:
            labels = ""
        
        app_short_uuid = uuid[:8]
        new_routes = f"""
traefik.http.routers.http-0-{app_short_uuid}-{domain.replace('.', '-')}.entryPoints=http
traefik.http.routers.http-0-{app_short_uuid}-{domain.replace('.', '-')}.middlewares=redirect-to-https
traefik.http.routers.http-0-{app_short_uuid}-{domain.replace('.', '-')}.rule=Host(`{domain}`) && PathPrefix(`/`)
traefik.http.routers.http-0-{app_short_uuid}-{domain.replace('.', '-')}.service=http-0-{app_short_uuid}
traefik.http.routers.https-0-{app_short_uuid}-{domain.replace('.', '-')}.entryPoints=https
traefik.http.routers.https-0-{app_short_uuid}-{domain.replace('.', '-')}.middlewares=gzip
traefik.http.routers.https-0-{app_short_uuid}-{domain.replace('.', '-')}.rule=Host(`{domain}`) && PathPrefix(`/`)
traefik.http.routers.https-0-{app_short_uuid}-{domain.replace('.', '-')}.service=https-0-{app_short_uuid}
traefik.http.routers.https-0-{app_short_uuid}-{domain.replace('.', '-')}.tls.certresolver=letsencrypt
traefik.http.routers.https-0-{app_short_uuid}-{domain.replace('.', '-')}.tls=true
caddy_0.handle_path.0_reverse_proxy={{{{upstreams 80}}}}
caddy_0.handle_path=/*
caddy_0.header=-Server
caddy_0.try_files={{path}} /index.html /index.php
caddy_0=https://{domain}
"""
        
        new_labels = labels + new_routes
        new_labels_b64 = base64.b64encode(new_labels.encode('utf-8')).decode('utf-8')
        
        result, success = self._request("PATCH", f"/applications/{uuid}", {"custom_labels": new_labels_b64})
        return result if success else None
    
    def projects_list(self) -> List[Dict]:
        """List projects."""
        result, success = self._request("GET", "/projects")
        return result if success else []
    
    def servers_list(self) -> List[Dict]:
        """List servers."""
        result, success = self._request("GET", "/servers")
        return result if success else []


def cmd_status(args):
    """Quick status check."""
    api = CoolifyAPI()
    
    print(f"\n{'='*60}")
    print("COOLIFY STATUS (v2.2.0)")
    print(f"{'='*60}")
    
    apps = api.apps_list()
    projects = api.projects_list()
    servers = api.servers_list()
    
    running = sum(1 for a in apps if 'running' in a.get('status', ''))
    
    print(f"\n📦 Applications: {len(apps)} ({running} running)")
    print(f"📁 Projects: {len(projects)}")
    print(f"🖥️  Servers: {len(servers)}")
    print(f"\n🔗 API: {'✅ Connected' if api.health_check() else '❌ Not connected'}")


def cmd_apps_list(args):
    """List applications."""
    api = CoolifyAPI()
    apps = api.apps_list()
    
    if not apps:
        print("No applications found")
        return
    
    print(f"\n{'='*60}")
    print(f"APPLICATIONS ({len(apps)} total)")
    print(f"{'='*60}")
    
    for app in apps:
        status = app.get('status', 'unknown')
        icon = '🟢' if 'running' in status else '🔴' if 'stopped' in status else '🟡'
        print(f"\n{icon} {app.get('name', 'Unknown')}")
        print(f"   UUID: {app.get('uuid', 'N/A')}")
        print(f"   Status: {status}")


def cmd_apps_get(args):
    """Get application details."""
    if not args.uuid:
        print("Error: --uuid required")
        return
    
    api = CoolifyAPI()
    app = api.apps_get(args.uuid)
    
    if app:
        print(f"\n{'='*60}")
        print(f"📦 {app.get('name', 'Unknown')}")
        print(f"{'='*60}")
        print(f"UUID: {app.get('uuid', 'N/A')}")
        print(f"FQDN: {app.get('fqdn', 'N/A')}")
        print(f"Status: {app.get('status', 'N/A')}")
        print(f"Repository: {app.get('git_repository', 'N/A')}")
    else:
        print(f"Application not found: {args.uuid}")


def cmd_apps_deploy(args):
    """Deploy application."""
    if not args.uuid:
        print("Error: --uuid required")
        return
    
    api = CoolifyAPI()
    force = not getattr(args, 'no_force', False)
    
    result = api.apps_deploy(args.uuid, force=force)
    if result:
        deployment_uuid = result.get('deployments', [{}])[0].get('deployment_uuid', 'N/A')
        print(f"✅ Deployment triggered: {deployment_uuid}")
    else:
        print("❌ Failed to trigger deployment")


def cmd_apps_wait(args):
    """Wait for deployment."""
    if not args.uuid:
        print("Error: --uuid required")
        return
    
    api = CoolifyAPI()
    timeout = getattr(args, 'timeout', 300)
    
    print(f"Waiting for deployment (timeout: {timeout}s)...")
    result = api.apps_wait_for_deployment(args.uuid, timeout=timeout)
    
    if result['success']:
        print(f"✅ {result['message']}")
    else:
        print(f"❌ {result['message']}")


def cmd_apps_logs(args):
    """Get logs."""
    if not args.uuid:
        print("Error: --uuid required")
        return
    
    api = CoolifyAPI()
    count = getattr(args, 'count', 100)
    logs = api.apps_logs(args.uuid, count)
    
    print(f"\n{'='*60}")
    print("LOGS")
    print(f"{'='*60}")
    print(logs.get('logs', 'No logs')[:5000])


def cmd_apps_create(args):
    """Create application."""
    api = CoolifyAPI()
    
    if not args.name or not args.repository:
        print("Error: --name and --repository required")
        return
    
    print(f"Creating application '{args.name}'...")
    app = api.apps_create(
        name=args.name,
        repository=args.repository,
        build_pack=getattr(args, 'build_pack', 'dockerfile'),
        branch=getattr(args, 'branch', 'main')
    )
    
    if app:
        print(f"✅ Created: {app['uuid']}")
        print(f"   Domain: {app.get('domains', 'N/A')}")
    else:
        print("❌ Failed to create application")


def cmd_projects_list(args):
    """List projects."""
    api = CoolifyAPI()
    projects = api.projects_list()
    
    if not projects:
        print("No projects found")
        return
    
    print(f"\n{'='*60}")
    print(f"PROJECTS ({len(projects)} total)")
    print(f"{'='*60}")
    
    for project in projects:
        print(f"\n📁 {project.get('name', 'Unknown')}")
        print(f"   UUID: {project.get('uuid', 'N/A')}")


def cmd_servers_list(args):
    """List servers."""
    api = CoolifyAPI()
    servers = api.servers_list()
    
    if not servers:
        print("No servers found")
        return
    
    print(f"\n{'='*60}")
    print(f"SERVERS ({len(servers)} total)")
    print(f"{'='*60}")
    
    for server in servers:
        status = "🟢" if server.get('is_reachable') else "🔴"
        print(f"\n{status} {server.get('name', 'Unknown')}")
        print(f"   UUID: {server.get('uuid', 'N/A')}")
        print(f"   IP: {server.get('ip', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(
        description="Coolify CLI v2.2.0 - Manage deployments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
    python scripts/coolify.py status
    python scripts/coolify.py apps list
    python scripts/coolify.py apps get --uuid <uuid>
    python scripts/coolify.py apps deploy --uuid <uuid>
    python scripts/coolify.py apps wait --uuid <uuid>
    python scripts/coolify.py apps create --name my-app --repository https://github.com/user/repo
    python scripts/coolify.py projects list
    python scripts/coolify.py servers list
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Status
    subparsers.add_parser("status", help="Quick status check")
    
    # Apps
    parser_apps = subparsers.add_parser("apps", help="Application commands")
    parser_apps.add_argument("action", choices=[
        "list", "get", "deploy", "wait", "logs", "create"
    ])
    parser_apps.add_argument("--uuid", help="Application UUID")
    parser_apps.add_argument("--count", type=int, default=100, help="Log count")
    parser_apps.add_argument("--no-force", action="store_true", help="Don't force rebuild")
    parser_apps.add_argument("--timeout", type=int, default=300, help="Wait timeout")
    parser_apps.add_argument("--name", help="App name (for create)")
    parser_apps.add_argument("--repository", help="Repository URL (for create)")
    parser_apps.add_argument("--build-pack", default="dockerfile", help="Build pack")
    parser_apps.add_argument("--branch", default="main", help="Git branch")
    
    # Projects
    parser_projects = subparsers.add_parser("projects", help="Project commands")
    parser_projects.add_argument("action", choices=["list"], default="list")
    
    # Servers
    parser_servers = subparsers.add_parser("servers", help="Server commands")
    parser_servers.add_argument("action", choices=["list"], default="list")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "status":
            cmd_status(args)
        elif args.command == "apps":
            if args.action == "list":
                cmd_apps_list(args)
            elif args.action == "get":
                cmd_apps_get(args)
            elif args.action == "deploy":
                cmd_apps_deploy(args)
            elif args.action == "wait":
                cmd_apps_wait(args)
            elif args.action == "logs":
                cmd_apps_logs(args)
            elif args.action == "create":
                cmd_apps_create(args)
        elif args.command == "projects":
            cmd_projects_list(args)
        elif args.command == "servers":
            cmd_servers_list(args)
        else:
            print(f"Unknown command: {args.command}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
