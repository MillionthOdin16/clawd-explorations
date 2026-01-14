#!/usr/bin/env python3
"""
Coolify - Complete API Integration for Clawdbot

A comprehensive Coolify skill that implements all major API endpoints:
- Applications (CRUD, deploy, restart, logs, status)
- Projects (list, create, update, delete)
- Environments (list, create, update)
- Destinations (list, create, update)
- Deployments (list, create, cancel)
- Databases (list, create, backup, restore)
- Services (list, create, update)
- Resources (all types with relationships)

Usage:
    python scripts/coolify.py <command> [options]
    python scripts/coolify.py help                    # Show all commands
    python scripts/coolify.py apps list              # List applications
    python scripts/coolify.py apps get <uuid>        # Get app details
    python scripts/coolify.py deploy <uuid>          # Trigger deployment

Environment:
    COOLIFY_API_TOKEN    - API token (required)
    COOLIFY_API_URL     - API URL (default: https://coolify.bradarr.com)
"""

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Configuration
API_URL = os.environ.get("COOLIFY_API_URL", "https://coolify.bradarr.com")
API_TOKEN = os.environ.get("COOLIFY_API_TOKEN", "")


@dataclass
class CoolifyConfig:
    """Configuration for Coolify API."""
    api_url: str = API_URL
    api_token: str = API_TOKEN
    timeout: int = 60
    
    def __post_init__(self):
        if not self.api_token:
            print("Warning: COOLIFY_API_TOKEN not set")
    
    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }


class CoolifyAPI:
    """Complete Coolify API client."""
    
    def __init__(self, config: Optional[CoolifyConfig] = None):
        self.config = config or CoolifyConfig()
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Tuple[Optional[Any], bool]:
        """Make API request."""
        import urllib.request
        import urllib.error
        
        url = f"{self.config.api_url}/api/v1{endpoint}"
        
        req = urllib.request.Request(
            url,
            method=method,
            headers=self.config.headers,
        )
        
        if data:
            req.data = json.dumps(data).encode('utf-8')
        
        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result, True
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8') if e.fp else ""
            print(f"HTTP Error {e.code}: {error_body[:200]}")
            return None, False
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
            return None, False
        except Exception as e:
            print(f"Error: {e}")
            return None, False
    
    # ============ APPLICATIONS ============
    
    def apps_list(self, expand: bool = False) -> List[Dict]:
        """List all applications."""
        endpoint = "/applications"
        if expand:
            endpoint += "?expand=destination,operations"
        result, success = self._request("GET", endpoint)
        return result if success else []
    
    def apps_get(self, uuid: str) -> Optional[Dict]:
        """Get application details."""
        result, success = self._request("GET", f"/applications/{uuid}")
        return result if success else None
    
    def apps_create(
        self,
        name: str,
        fqdn: str,
        repository: str,
        project_uuid: str,
        environment_uuid: str,
        build_pack: str = "nixpacks",
        branch: str = "main",
        **kwargs
    ) -> Optional[Dict]:
        """Create new application."""
        data = {
            "name": name,
            "fqdn": fqdn,
            "git_repository": repository,
            "git_branch": branch,
            "build_pack": build_pack,
            "project_id": project_uuid,
            "environment_id": environment_uuid,
        }
        data.update({k: v for k, v in kwargs.items() if v is not None})
        result, success = self._request("POST", "/applications", data)
        return result if success else None
    
    def apps_update(self, uuid: str, **kwargs) -> Optional[Dict]:
        """Update application."""
        result, success = self._request("PUT", f"/applications/{uuid}", kwargs)
        return result if success else None
    
    def apps_delete(self, uuid: str) -> bool:
        """Delete application."""
        _, success = self._request("DELETE", f"/applications/{uuid}")
        return success
    
    def apps_deploy(self, uuid: str) -> Optional[Dict]:
        """Trigger deployment."""
        result, success = self._request("POST", "/deploy", {"uuid": uuid})
        return result if success else None
    
    def apps_restart(self, uuid: str) -> Optional[Dict]:
        """Restart application."""
        result, success = self._request("POST", f"/applications/{uuid}/restart")
        return result if success else None
    
    def apps_stop(self, uuid: str) -> Optional[Dict]:
        """Stop application."""
        result, success = self._request("POST", f"/applications/{uuid}/stop")
        return result if success else None
    
    def apps_start(self, uuid: str) -> Optional[Dict]:
        """Start application."""
        result, success = self._request("POST", f"/applications/{uuid}/start")
        return result if success else None
    
    def apps_logs(self, uuid: str, count: int = 100) -> List[Dict]:
        """Get application logs."""
        result, success = self._request("GET", f"/applications/{uuid}/logs?limit={count}")
        return result if success else []
    
    def apps_executions(self, uuid: str) -> List[Dict]:
        """Get application executions."""
        result, success = self._request("GET", f"/applications/{uuid}/executions")
        return result if success else []
    
    def apps_change_build_pack(self, uuid: str, build_pack: str) -> Optional[Dict]:
        """Change application build pack."""
        return self.apps_update(uuid, build_pack=build_pack)
    
    def apps_change_destination(self, uuid: str, destination_uuid: str) -> Optional[Dict]:
        """Change application destination."""
        return self.apps_update(uuid, destination_id=destination_uuid)
    
    # ============ PROJECTS ============
    
    def projects_list(self) -> List[Dict]:
        """List all projects."""
        result, success = self._request("GET", "/projects")
        return result if success else []
    
    def projects_get(self, uuid: str) -> Optional[Dict]:
        """Get project details."""
        result, success = self._request("GET", f"/projects/{uuid}")
        return result if success else None
    
    def projects_create(self, name: str, description: str = "") -> Optional[Dict]:
        """Create new project."""
        result, success = self._request("POST", "/projects", {
            "name": name,
            "description": description
        })
        return result if success else None
    
    def projects_update(self, uuid: str, **kwargs) -> Optional[Dict]:
        """Update project."""
        result, success = self._request("PUT", f"/projects/{uuid}", kwargs)
        return result if success else None
    
    def projects_delete(self, uuid: str) -> bool:
        """Delete project."""
        _, success = self._request("DELETE", f"/projects/{uuid}")
        return success
    
    # ============ ENVIRONMENTS ============
    
    def environments_list(self, project_uuid: str) -> List[Dict]:
        """List environments for a project."""
        result, success = self._request("GET", f"/projects/{project_uuid}/environments")
        return result if success else []
    
    def environments_get(self, uuid: str) -> Optional[Dict]:
        """Get environment details."""
        result, success = self._request("GET", f"/environments/{uuid}")
        return result if success else None
    
    def environments_create(
        self,
        project_uuid: str,
        name: str,
        is_production: bool = False
    ) -> Optional[Dict]:
        """Create new environment."""
        result, success = self._request("POST", f"/projects/{project_uuid}/environments", {
            "name": name,
            "is_production": is_production
        })
        return result if success else None
    
    def environments_update(self, uuid: str, **kwargs) -> Optional[Dict]:
        """Update environment."""
        result, success = self._request("PUT", f"/environments/{uuid}", kwargs)
        return result if success else None
    
    def environments_delete(self, uuid: str) -> bool:
        """Delete environment."""
        _, success = self._request("DELETE", f"/environments/{uuid}")
        return success
    
    # ============ DESTINATIONS ============
    
    def destinations_list(self) -> List[Dict]:
        """List all destinations."""
        result, success = self._request("GET", "/destinations")
        return result if success else []
    
    def destinations_get(self, uuid: str) -> Optional[Dict]:
        """Get destination details."""
        result, success = self._request("GET", f"/destinations/{uuid}")
        return result if success else None
    
    def destinations_create(
        self,
        name: str,
        network: str,
        docker_id: str,
        is_appliance: bool = False
    ) -> Optional[Dict]:
        """Create new destination."""
        result, success = self._request("POST", "/destinations", {
            "name": name,
            "network": network,
            "docker_id": docker_id,
            "is_appliance": is_appliance
        })
        return result if success else None
    
    def destinations_update(self, uuid: str, **kwargs) -> Optional[Dict]:
        """Update destination."""
        result, success = self._request("PUT", f"/destinations/{uuid}", kwargs)
        return result if success else None
    
    def destinations_delete(self, uuid: str) -> bool:
        """Delete destination."""
        _, success = self._request("DELETE", f"/destinations/{uuid}")
        return success
    
    # ============ DEPLOYMENTS ============
    
    def deployments_list(self, application_uuid: Optional[str] = None) -> List[Dict]:
        """List deployments."""
        endpoint = "/deployments"
        if application_uuid:
            endpoint += f"?application_id={application_uuid}"
        result, success = self._request("GET", endpoint)
        return result if success else []
    
    def deployments_get(self, uuid: str) -> Optional[Dict]:
        """Get deployment details."""
        result, success = self._request("GET", f"/deployments/{uuid}")
        return result if success else None
    
    def deployments_cancel(self, uuid: str) -> Optional[Dict]:
        """Cancel deployment."""
        result, success = self._request("POST", f"/deployments/{uuid}/cancel")
        return result if success else None
    
    def deployments_retry(self, uuid: str) -> Optional[Dict]:
        """Retry deployment."""
        result, success = self._request("POST", f"/deployments/{uuid}/retry")
        return result if success else None
    
    # ============ DATABASES ============
    
    def databases_list(self, project_uuid: Optional[str] = None) -> List[Dict]:
        """List databases."""
        if project_uuid:
            result, success = self._request("GET", f"/projects/{project_uuid}/databases")
        else:
            result, success = self._request("GET", "/databases")
        return result if success else []
    
    def databases_get(self, uuid: str) -> Optional[Dict]:
        """Get database details."""
        result, success = self._request("GET", f"/databases/{uuid}")
        return result if success else None
    
    def databases_create(
        self,
        project_uuid: str,
        environment_uuid: str,
        destination_uuid: str,
        name: str,
        db_type: str,
        version: str = "15",
        **kwargs
    ) -> Optional[Dict]:
        """Create new database."""
        data = {
            "name": name,
            "project_id": project_uuid,
            "environment_id": environment_uuid,
            "destination_id": destination_uuid,
            "type": db_type,
            "version": version,
        }
        data.update({k: v for k, v in kwargs.items() if v is not None})
        result, success = self._request("POST", "/databases", data)
        return result if success else None
    
    def databases_backup(self, uuid: str) -> Optional[Dict]:
        """Trigger database backup."""
        result, success = self._request("POST", f"/databases/{uuid}/backup")
        return result if success else None
    
    def databases_restore(self, uuid: str, backup_uuid: str) -> Optional[Dict]:
        """Restore database from backup."""
        result, success = self._request("POST", f"/databases/{uuid}/restore", {
            "backup_id": backup_uuid
        })
        return result if success else None
    
    def databases_delete(self, uuid: str) -> bool:
        """Delete database."""
        _, success = self._request("DELETE", f"/databases/{uuid}")
        return success
    
    # ============ SERVICES ============
    
    def services_list(self, project_uuid: Optional[str] = None) -> List[Dict]:
        """List services."""
        if project_uuid:
            result, success = self._request("GET", f"/projects/{project_uuid}/services")
        else:
            result, success = self._request("GET", "/services")
        return result if success else []
    
    def services_get(self, uuid: str) -> Optional[Dict]:
        """Get service details."""
        result, success = self._request("GET", f"/services/{uuid}")
        return result if success else None
    
    def services_create(
        self,
        project_uuid: str,
        environment_uuid: str,
        destination_uuid: str,
        name: str,
        service_type: str,
        **kwargs
    ) -> Optional[Dict]:
        """Create new service."""
        data = {
            "name": name,
            "project_id": project_uuid,
            "environment_id": environment_uuid,
            "destination_id": destination_uuid,
            "type": service_type,
        }
        data.update({k: v for k, v in kwargs.items() if v is not None})
        result, success = self._request("POST", "/services", data)
        return result if success else None
    
    def services_update(self, uuid: str, **kwargs) -> Optional[Dict]:
        """Update service."""
        result, success = self._request("PUT", f"/services/{uuid}", kwargs)
        return result if success else None
    
    def services_delete(self, uuid: str) -> bool:
        """Delete service."""
        _, success = self._request("DELETE", f"/services/{uuid}")
        return success
    
    def services_restart(self, uuid: str) -> Optional[Dict]:
        """Restart service."""
        result, success = self._request("POST", f"/services/{uuid}/restart")
        return result if success else None
    
    # ============ RESOURCES ============
    
    def resources_list(self, project_uuid: str) -> List[Dict]:
        """List all resources (apps, DBs, services) for a project."""
        result, success = self._request("GET", f"/projects/{project_uuid}/resources")
        return result if success else []
    
    def resources_get(self, uuid: str) -> Optional[Dict]:
        """Get any resource by UUID."""
        # Try to determine resource type from UUID
        for resource_type in ["applications", "databases", "services"]:
            result, success = self._request("GET", f"/{resource_type}/{uuid}")
            if success:
                result["_resource_type"] = resource_type
                return result
        return None


class CoolifyCLI:
    """CLI interface for Coolify."""
    
    def __init__(self):
        self.api = CoolifyAPI()
        self.format = "text"
    
    def print_app(self, app: Dict, verbose: bool = False):
        """Print application details."""
        print(f"\n{'='*60}")
        print(f"📦 {app.get('name', 'Unknown')}")
        print(f"{'='*60}")
        print(f"UUID: {app.get('uuid', 'N/A')}")
        print(f"FQDN: {app.get('fqdn', 'N/A')}")
        print(f"Status: {app.get('status', 'N/A')}")
        print(f"Build Pack: {app.get('build_pack', 'N/A')}")
        print(f"Repository: {app.get('git_repository', 'N/A')}")
        print(f"Branch: {app.get('git_branch', 'N/A')}")
        print(f"Commit: {app.get('git_commit_sha', 'N/A')[:8] if app.get('git_commit_sha') else 'N/A'}")
        
        if verbose:
            print(f"\nDocker Image: {app.get('docker_registry_image_name', 'N/A')}:{app.get('docker_registry_image_tag', 'N/A')}")
            print(f"Destination ID: {app.get('destination_id', 'N/A')}")
            print(f"Created: {app.get('created_at', 'N/A')}")
            print(f"Updated: {app.get('updated_at', 'N/A')}")
    
    def print_deployment(self, deployment: Dict):
        """Print deployment details."""
        status = deployment.get('status', 'N/A')
        status_icons = {
            'in_progress': '🔄',
            'queued': '⏳',
            'completed': '✅',
            'failed': '❌',
            'cancelled': '🚫'
        }
        icon = status_icons.get(status, '📦')
        print(f"{icon} {deployment.get('commit_message', 'N/A')[:50]}")
        print(f"   Status: {status}")
        print(f"   Commit: {deployment.get('commit', 'N/A')[:8] if deployment.get('commit') else 'N/A'}")
        print(f"   Created: {deployment.get('created_at', 'N/A')}")
    
    def cmd_apps_list(self, args):
        """List applications."""
        expand = hasattr(args, 'expand') and args.expand
        apps = self.api.apps_list(expand=expand)
        
        if not apps:
            print("No applications found")
            return
        
        print(f"\n{'='*60}")
        print(f"APPLICATIONS ({len(apps)} total)")
        print(f"{'='*60}")
        
        for app in apps:
            status = app.get('status', 'unknown')
            status_colors = {
                'running': '🟢',
                'stopped': '🔴',
                'deploying': '🟡',
                'restarting': '🟠',
            }
            icon = status_colors.get(status, '⚪')
            print(f"\n{icon} {app.get('name', 'Unknown')}")
            print(f"   UUID: {app.get('uuid', 'N/A')}")
            print(f"   FQDN: {app.get('fqdn', 'N/A')}")
            print(f"   Status: {status}")
            print(f"   Repo: {app.get('git_repository', 'N/A')}")
    
    def cmd_apps_get(self, args):
        """Get application details."""
        if not args.uuid:
            print("Error: UUID required")
            return
        app = self.api.apps_get(args.uuid)
        if app:
            self.print_app(app, verbose=True)
        else:
            print(f"Application not found: {args.uuid}")
    
    def cmd_apps_logs(self, args):
        """Get application logs."""
        if not args.uuid:
            print("Error: UUID required")
            return
        count = getattr(args, 'count', 100)
        logs = self.api.apps_logs(args.uuid, count)
        if logs:
            print(f"\n{'='*60}")
            print(f"LOGS ({len(logs)} entries)")
            print(f"{'='*60}")
            for log in logs[-50:]:  # Show last 50
                ts = log.get('timestamp', '')[:19]
                output = log.get('output', '')[:100]
                print(f"[{ts}] {output}")
        else:
            print("No logs found")
    
    def cmd_apps_deploy(self, args):
        """Trigger deployment."""
        if not args.uuid:
            print("Error: UUID required")
            return
        result = self.api.apps_deploy(args.uuid)
        if result:
            print(f"✅ Deployment triggered: {result.get('deployment_uuid', 'N/A')}")
        else:
            print("❌ Failed to trigger deployment")
    
    def cmd_apps_restart(self, args):
        """Restart application."""
        if not args.uuid:
            print("Error: UUID required")
            return
        result = self.api.apps_restart(args.uuid)
        if result:
            print(f"✅ Restart triggered")
        else:
            print("❌ Failed to restart")
    
    def cmd_apps_start(self, args):
        """Start application."""
        if not args.uuid:
            print("Error: UUID required")
            return
        result = self.api.apps_start(args.uuid)
        if result:
            print(f"✅ Start triggered")
        else:
            print("❌ Failed to start")
    
    def cmd_apps_stop(self, args):
        """Stop application."""
        if not args.uuid:
            print("Error: UUID required")
            return
        result = self.api.apps_stop(args.uuid)
        if result:
            print(f"✅ Stop triggered")
        else:
            print("❌ Failed to stop")
    
    def cmd_projects_list(self, args):
        """List projects."""
        projects = self.api.projects_list()
        if not projects:
            print("No projects found")
            return
        
        print(f"\n{'='*60}")
        print(f"PROJECTS ({len(projects)} total)")
        print(f"{'='*60}")
        
        for project in projects:
            print(f"\n📁 {project.get('name', 'Unknown')}")
            print(f"   UUID: {project.get('uuid', 'N/A')}")
            print(f"   Description: {project.get('description', 'N/A')[:50]}")
    
    def cmd_deployments_list(self, args):
        """List deployments."""
        app_uuid = getattr(args, 'application', None)
        deployments = self.api.deployments_list(app_uuid)
        
        if not deployments:
            print("No deployments found")
            return
        
        print(f"\n{'='*60}")
        print(f"DEPLOYMENTS ({len(deployments)} total)")
        print(f"{'='*60}")
        
        for deployment in sorted(deployments, key=lambda x: x.get('created_at', ''), reverse=True)[:20]:
            self.print_deployment(deployment)
    
    def cmd_deployments_cancel(self, args):
        """Cancel deployment."""
        if not args.uuid:
            print("Error: UUID required")
            return
        result = self.api.deployments_cancel(args.uuid)
        if result:
            print(f"✅ Deployment cancelled")
        else:
            print("❌ Failed to cancel deployment")
    
    def cmd_databases_list(self, args):
        """List databases."""
        project_uuid = getattr(args, 'project', None)
        dbs = self.api.databases_list(project_uuid)
        
        if not dbs:
            print("No databases found")
            return
        
        print(f"\n{'='*60}")
        print(f"DATABASES ({len(dbs)} total)")
        print(f"{'='*60}")
        
        for db in dbs:
            status = db.get('status', 'unknown')
            print(f"\n🗄️  {db.get('name', 'Unknown')} ({db.get('type', 'N/A')})")
            print(f"   UUID: {db.get('uuid', 'N/A')}")
            print(f"   Status: {status}")
            print(f"   Version: {db.get('version', 'N/A')}")
    
    def cmd_services_list(self, args):
        """List services."""
        project_uuid = getattr(args, 'project', None)
        services = self.api.services_list(project_uuid)
        
        if not services:
            print("No services found")
            return
        
        print(f"\n{'='*60}")
        print(f"SERVICES ({len(services)} total)")
        print(f"{'='*60}")
        
        for service in services:
            status = service.get('status', 'unknown')
            print(f"\n🔧 {service.get('name', 'Unknown')} ({service.get('type', 'N/A')})")
            print(f"   UUID: {service.get('uuid', 'N/A')}")
            print(f"   Status: {status}")
    
    def cmd_resources_list(self, args):
        """List all resources for a project."""
        if not args.project:
            print("Error: Project UUID required")
            return
        resources = self.api.resources_list(args.project)
        
        if not resources:
            print("No resources found")
            return
        
        print(f"\n{'='*60}")
        print(f"RESOURCES ({len(resources)} total)")
        print(f"{'='*60}")
        
        for resource in resources:
            r_type = resource.get('_resource_type', 'unknown')
            icon = {'application': '📦', 'database': '🗄️', 'service': '🔧'}.get(r_type, '📦')
            print(f"\n{icon} {resource.get('name', 'Unknown')} ({r_type})")
            print(f"   UUID: {resource.get('uuid', 'N/A')}")
            print(f"   Status: {resource.get('status', 'N/A')}")
    
    def cmd_status(self, args):
        """Quick status check."""
        print(f"\n{'='*60}")
        print("COOLIFY STATUS")
        print(f"{'='*60}")
        
        apps = self.api.apps_list()
        projects = self.api.projects_list()
        dbs = self.api.databases_list()
        services = self.api.services_list()
        
        running = sum(1 for a in apps if a.get('status') == 'running')
        
        print(f"\n📦 Applications: {len(apps)} ({running} running)")
        print(f"📁 Projects: {len(projects)}")
        print(f"🗄️  Databases: {len(dbs)}")
        print(f"🔧 Services: {len(services)}")
        print(f"\n🔗 API URL: {API_URL}")
        print(f"✅ API: Connected" if API_TOKEN else "❌ API: Not configured")


def main():
    parser = argparse.ArgumentParser(
        description="Coolify CLI - Complete API integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all applications
  python scripts/coolify.py apps list
  
  # Get application details
  python scripts/coolify.py apps get <uuid>
  
  # Trigger deployment
  python scripts/coolify.py apps deploy <uuid>
  
  # Get logs
  python scripts/coolify.py apps logs <uuid>
  
  # List projects
  python scripts/coolify.py projects list
  
  # Quick status
  python scripts/coolify.py status
  
  # Help for specific command
  python scripts/coolify.py apps --help
        """
    )
    
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--quiet", action="store_true", help="Quiet mode")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Status
    parser_status = subparsers.add_parser("status", help="Quick status check")
    
    # Applications
    parser_apps = subparsers.add_parser("apps", help="Application commands")
    parser_apps.add_argument("action", choices=[
        "list", "get", "create", "update", "delete",
        "deploy", "restart", "start", "stop", "logs", "executions"
    ])
    parser_apps.add_argument("--uuid", help="Application UUID")
    parser_apps.add_argument("--name", help="Application name")
    parser_apps.add_argument("--fqdn", help="FQDN")
    parser_apps.add_argument("--repo", help="Repository")
    parser_apps.add_argument("--expand", action="store_true", help="Expand output")
    parser_apps.add_argument("--count", type=int, default=100, help="Log count")
    parser_apps.add_argument("--build-pack", help="Build pack (nixpacks, dockerfile, dockercompose)")
    
    # Projects
    parser_projects = subparsers.add_parser("projects", help="Project commands")
    parser_projects.add_argument("action", choices=["list", "get", "create", "update", "delete"])
    parser_projects.add_argument("--uuid", help="Project UUID")
    parser_projects.add_argument("--name", help="Project name")
    parser_projects.add_argument("--description", help="Description")
    
    # Environments
    parser_envs = subparsers.add_parser("environments", help="Environment commands")
    parser_envs.add_argument("action", choices=["list", "get", "create", "update", "delete"])
    parser_envs.add_argument("--uuid", help="Environment UUID")
    parser_envs.add_argument("--project", help="Project UUID")
    parser_envs.add_argument("--name", help="Environment name")
    parser_envs.add_argument("--production", action="store_true", help="Is production")
    
    # Destinations
    parser_dests = subparsers.add_parser("destinations", help="Destination commands")
    parser_dests.add_argument("action", choices=["list", "get", "create", "update", "delete"])
    parser_dests.add_argument("--uuid", help="Destination UUID")
    parser_dests.add_argument("--name", help="Destination name")
    parser_dests.add_argument("--network", help="Network")
    parser_dests.add_argument("--docker-id", help="Docker ID")
    
    # Deployments
    parser_deploys = subparsers.add_parser("deployments", help="Deployment commands")
    parser_deploys.add_argument("action", choices=["list", "get", "cancel", "retry"])
    parser_deploys.add_argument("--uuid", help="Deployment UUID")
    parser_deploys.add_argument("--application", help="Filter by application UUID")
    
    # Databases
    parser_dbs = subparsers.add_parser("databases", help="Database commands")
    parser_dbs.add_argument("action", choices=["list", "get", "create", "delete", "backup", "restore"])
    parser_dbs.add_argument("--uuid", help="Database UUID")
    parser_dbs.add_argument("--project", help="Project UUID")
    parser_dbs.add_argument("--name", help="Database name")
    parser_dbs.add_argument("--type", help="Database type (postgres, mysql, etc.)")
    parser_dbs.add_argument("--backup", help="Backup UUID (for restore)")
    
    # Services
    parser_svcs = subparsers.add_parser("services", help="Service commands")
    parser_svcs.add_argument("action", choices=["list", "get", "create", "update", "delete", "restart"])
    parser_svcs.add_argument("--uuid", help="Service UUID")
    parser_svcs.add_argument("--project", help="Project UUID")
    parser_svcs.add_argument("--name", help="Service name")
    parser_svcs.add_argument("--type", help="Service type")
    
    # Resources
    parser_res = subparsers.add_parser("resources", help="All resources for a project")
    parser_res.add_argument("list", nargs="?", const="list", help="List resources")
    parser_res.add_argument("--project", required=True, help="Project UUID")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = CoolifyCLI()
    cli.format = "json" if args.json else "text"
    
    try:
        if args.command == "status":
            cli.cmd_status(args)
        elif args.command == "apps":
            if args.action == "list":
                cli.cmd_apps_list(args)
            elif args.action == "get":
                cli.cmd_apps_get(args)
            elif args.action == "deploy":
                cli.cmd_apps_deploy(args)
            elif args.action == "restart":
                cli.cmd_apps_restart(args)
            elif args.action == "start":
                cli.cmd_apps_start(args)
            elif args.action == "stop":
                cli.cmd_apps_stop(args)
            elif args.action == "logs":
                cli.cmd_apps_logs(args)
            else:
                print(f"Action '{args.action}' not fully implemented yet")
        elif args.command == "projects":
            if args.action == "list":
                cli.cmd_projects_list(args)
            elif args.action == "get":
                if args.uuid:
                    projects = cli.api.projects_list()
                    for p in projects:
                        if p.get('uuid') == args.uuid:
                            cli.print_app(p)
                            break
            else:
                print(f"Action '{args.action}' not fully implemented yet")
        elif args.command == "deployments":
            if args.action == "list":
                cli.cmd_deployments_list(args)
            elif args.action == "cancel":
                if args.uuid:
                    cli.cmd_deployments_cancel(args)
            else:
                print(f"Action '{args.action}' not fully implemented yet")
        elif args.command == "databases":
            cli.cmd_databases_list(args)
        elif args.command == "services":
            cli.cmd_services_list(args)
        elif args.command == "resources":
            cli.cmd_resources_list(args)
        else:
            print(f"Command '{args.command}' not implemented")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
