#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "rich"]
# ///
"""Coolify CLI - Manage deployments on Coolify."""

import argparse
import os
import sys
import json
import httpx
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.syntax import Syntax

console = Console()
API_BASE = "https://coolify.bradarr.com/api/v1"

def get_api_key() -> str:
    """Get API key from environment."""
    key = os.environ.get("COOLIFY_API_KEY", "").strip()
    if not key:
        rprint("[bold red]Error: COOLIFY_API_KEY not set[/bold red]")
        rprint("Set it with: export COOLIFY_API_KEY='your-key'")
        sys.exit(1)
    return key

def get_headers() -> dict:
    """Get headers with authentication."""
    return {"Authorization": f"Bearer {get_api_key()}"}

def make_request(method: str, endpoint: str, **kwargs) -> dict:
    """Make an API request and return JSON."""
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    try:
        r = httpx.request(method, url, headers=get_headers(), timeout=30, **kwargs)
        r.raise_for_status()
        return r.json() if r.content else {}
    except httpx.HTTPStatusError as e:
        error_msg = e.response.text[:500] if e.response.text else str(e)
        rprint(f"[red]API Error: {e.response.status_code}[/red]")
        rprint(f"[red]{error_msg}[/red]")
        sys.exit(1)
    except Exception as e:
        rprint(f"[red]Error: {e}[/red]")
        sys.exit(1)

# Applications

def list_apps(raw: bool = False):
    """List all applications."""
    apps = make_request("GET", "applications")
    if not apps:
        rprint("[yellow]No applications found[/yellow]")
        return
    
    if raw:
        rprint(json.dumps(apps, indent=2))
        return
    
    table = Table(title="Applications", show_lines=False)
    table.add_column("Name", style="bold")
    table.add_column("URL", style="blue")
    table.add_column("Status", style="green")
    table.add_column("Repo", style="dim")
    
    for app in apps:
        status = app.get("status", "unknown")
        # Color code status
        if "running" in status:
            status_style = "green"
        elif "exited" in status or "unhealthy" in status:
            status_style = "red"
        else:
            status_style = "yellow"
        
        table.add_row(
            app.get("name", "Unnamed")[:40],
            app.get("fqdn", "-")[:30],
            f"[{status_style}]{status}[/{status_style}]",
            app.get("git_repository", "-")[:40]
        )
    console.print(table)

def get_app(uuid: str, raw: bool = False):
    """Get application details."""
    app = make_request("GET", f"applications/{uuid}")
    
    if raw:
        rprint(json.dumps(app, indent=2))
        return
    
    rprint(f"\n[bold]{app.get('name', 'Unnamed')}[/bold]")
    rprint(f"URL: [blue]{app.get('fqdn', 'N/A')}[/blue]")
    rprint(f"Status: {app.get('status', 'unknown')}")
    rprint(f"Repository: {app.get('git_repository', 'N/A')}")
    rprint(f"Branch: {app.get('git_branch', 'N/A')}")
    rprint(f"Build Pack: {app.get('build_pack', 'N/A')}")
    
    # Resource limits
    limits = app.get("limits", {})
    if limits:
        rprint(f"\n[bold]Resources:[/bold]")
        rprint(f"  CPU: {limits.get('cpus', 'unlimited')}")
        rprint(f"  Memory: {limits.get('memory', 'unlimited')}")
    
    # Health check
    hc = app.get("health_check", {})
    if hc:
        rprint(f"\n[bold]Health Check:[/bold]")
        rprint(f"  Path: {hc.get('path', 'N/A')}")
        rprint(f"  Retries: {hc.get('retries', 'N/A')}")

def start_app(uuid: str):
    """Start an application."""
    rprint(f"[yellow]Starting application...[/yellow]")
    make_request("POST", f"applications/{uuid}/start")
    rprint("[green]Started successfully[/green]")

def stop_app(uuid: str):
    """Stop an application."""
    rprint(f"[yellow]Stopping application...[/yellow]")
    make_request("POST", f"applications/{uuid}/stop")
    rprint("[green]Stopped successfully[/green]")

def restart_app(uuid: str):
    """Restart an application."""
    rprint(f"[yellow]Restarting application...[/yellow]")
    make_request("POST", f"applications/{uuid}/restart")
    rprint("[green]Restarted successfully[/green]")

def delete_app(uuid: str, force: bool = False):
    """Delete an application."""
    if not force:
        rprint(f"[yellow]This will delete application {uuid}[/yellow]")
        confirm = input("Continue? [y/N]: ")
        if confirm.lower() != "y":
            rprint("Cancelled")
            return
    
    make_request("DELETE", f"applications/{uuid}")
    rprint("[green]Deleted successfully[/green]")

# Databases

def list_dbs(raw: bool = False):
    """List all databases."""
    dbs = make_request("GET", "databases")
    if not dbs:
        rprint("[yellow]No databases found[/yellow]")
        return
    
    if raw:
        rprint(json.dumps(dbs, indent=2))
        return
    
    table = Table(title="Databases", show_lines=False)
    table.add_column("Name", style="bold")
    table.add_column("Status", style="green")
    table.add_column("Type", style="cyan")
    
    for db in dbs:
        status = db.get("status", "unknown")
        if "running" in status:
            status_style = "green"
        elif "exited" in status or "unhealthy" in status:
            status_style = "red"
        else:
            status_style = "yellow"
        
        table.add_row(
            db.get("name", "Unnamed")[:50],
            f"[{status_style}]{status}[/{status_style}]",
            db.get("type", "-")[:20]
        )
    console.print(table)

def get_db(uuid: str, raw: bool = False):
    """Get database details."""
    db = make_request("GET", f"databases/{uuid}")
    
    if raw:
        rprint(json.dumps(db, indent=2))
        return
    
    rprint(f"\n[bold]{db.get('name', 'Unnamed')}[/bold]")
    rprint(f"Status: {db.get('status', 'unknown')}")
    rprint(f"Type: {db.get('type', 'N/A')}")

# Services

def list_services(raw: bool = False):
    """List all services."""
    services = make_request("GET", "services")
    if not services:
        rprint("[yellow]No services found[/yellow]")
        return
    
    if raw:
        rprint(json.dumps(services, indent=2))
        return
    
    table = Table(title="Services", show_lines=False)
    table.add_column("Name", style="bold")
    table.add_column("Status", style="green")
    
    for svc in services:
        status = svc.get("status", "unknown")
        if "running" in status:
            status_style = "green"
        elif "exited" in status:
            status_style = "red"
        else:
            status_style = "yellow"
        
        table.add_row(
            svc.get("name", "Unnamed")[:50],
            f"[{status_style}]{status}[/{status_style}]"
        )
    console.print(table)

# Projects

def list_projects(raw: bool = False):
    """List all projects."""
    projects = make_request("GET", "projects")
    if not projects:
        rprint("[yellow]No projects found[/yellow]")
        return
    
    if raw:
        rprint(json.dumps(projects, indent=2))
        return
    
    table = Table(title="Projects", show_lines=False)
    table.add_column("Name", style="bold")
    table.add_column("UUID", style="dim")
    
    for p in projects:
        table.add_row(
            p.get("name", "Unnamed"),
            p.get("uuid", "-")
        )
    console.print(table)

# Main CLI

def main():
    parser = argparse.ArgumentParser(
        description="Coolify CLI - Manage deployments",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--raw", action="store_true", help="Output raw JSON")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Apps subcommand
    apps_p = subparsers.add_parser("apps", help="Manage applications")
    apps_sub = apps_p.add_subparsers(dest="subcommand")
    
    apps_sub.add_parser("list", help="List applications")
    apps_sub.add_parser("list-dbs", help="List databases")
    apps_sub.add_parser("list-services", help="List services")
    apps_sub.add_parser("list-projects", help="List projects")
    
    get_p = apps_sub.add_parser("get", help="Get application details")
    get_p.add_argument("uuid", help="Application UUID")
    
    start_p = apps_sub.add_parser("start", help="Start application")
    start_p.add_argument("uuid", help="Application UUID")
    
    stop_p = apps_sub.add_parser("stop", help="Stop application")
    stop_p.add_argument("uuid", help="Application UUID")
    
    restart_p = apps_sub.add_parser("restart", help="Restart application")
    restart_p.add_argument("uuid", help="Application UUID")
    
    delete_p = apps_sub.add_parser("delete", help="Delete application")
    delete_p.add_argument("uuid", help="Application UUID")
    delete_p.add_argument("--force", action="store_true", help="Skip confirmation")
    
    # Databases
    dbs_p = subparsers.add_parser("dbs", help="Manage databases")
    dbs_sub = dbs_p.add_subparsers(dest="subcommand")
    
    dbs_sub.add_parser("list", help="List databases")
    get_db_p = dbs_sub.add_parser("get", help="Get database details")
    get_db_p.add_argument("uuid", help="Database UUID")
    
    # Services
    svc_p = subparsers.add_parser("services", help="Manage services")
    svc_sub = svc_p.add_subparsers(dest="subcommand")
    svc_sub.add_parser("list", help="List services")
    
    # Projects
    proj_p = subparsers.add_parser("projects", help="Manage projects")
    proj_sub = proj_p.add_subparsers(dest="subcommand")
    proj_sub.add_parser("list", help="List projects")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        rprint("\n[bold]Quick Examples:[/bold]")
        rprint("  coolify apps list          # List all applications")
        rprint("  coolify apps get <uuid>    # Get app details")
        rprint("  coolify apps start <uuid>  # Start an app")
        rprint("  coolify dbs list           # List databases")
        rprint("  coolify services list      # List services")
        return
    
    # Route commands
    if args.command == "apps":
        if args.subcommand == "list" or not args.subcommand:
            list_apps(args.raw)
        elif args.subcommand == "list-dbs":
            list_dbs(args.raw)
        elif args.subcommand == "list-services":
            list_services(args.raw)
        elif args.subcommand == "list-projects":
            list_projects(args.raw)
        elif args.subcommand == "get":
            get_app(args.uuid, args.raw)
        elif args.subcommand == "start":
            start_app(args.uuid)
        elif args.subcommand == "stop":
            stop_app(args.uuid)
        elif args.subcommand == "restart":
            restart_app(args.uuid)
        elif args.subcommand == "delete":
            delete_app(args.uuid, args.force)
    
    elif args.command == "dbs":
        if args.subcommand == "list" or not args.subcommand:
            list_dbs(args.raw)
        elif args.subcommand == "get":
            get_db(args.uuid, args.raw)
    
    elif args.command == "services":
        if args.subcommand == "list" or not args.subcommand:
            list_services(args.raw)
    
    elif args.command == "projects":
        if args.subcommand == "list" or not args.subcommand:
            list_projects(args.raw)

if __name__ == "__main__":
    main()
