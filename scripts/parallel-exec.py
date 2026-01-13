#!/usr/bin/env python3
"""
Parallel Execution Utilities for Clawdbot

Run commands and API calls in parallel for faster batch processing.

Usage:
    python parallel-exec.py curl <urls_file>
    python parallel-exec.py exec <commands_file>
    python parallel-exec.py api <endpoints_file>
    python parallel-exec.py download <files_file> <output_dir>
    python parallel-exec.py git <repos_file> <command>

Requirements:
    - Python 3.9+
    - concurrent.futures (built-in)
"""

import argparse
import concurrent.futures
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from typing import List, Callable


def run_command(cmd: str) -> tuple:
    """Run a shell command and return (success, output, error)."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=120
        )
        return (result.returncode == 0, result.stdout, result.stderr)
    except subprocess.TimeoutExpired:
        return (False, "", "Timeout")
    except Exception as e:
        return (False, "", str(e))


def curl_url(url: str) -> tuple:
    """Fetch a URL and return (success, content, error)."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Clawdbot/1.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            return (True, response.read().decode('utf-8'), "")
    except Exception as e:
        return (False, "", str(e))


def download_file(url: str, output_dir: str) -> tuple:
    """Download a file and return (success, filepath, error)."""
    try:
        output_path = os.path.join(output_dir, url.split('/')[-1])
        urllib.request.urlretrieve(url, output_path)
        return (True, output_path, "")
    except Exception as e:
        return (False, "", str(e))


def git_command(repo: str, command: str) -> tuple:
    """Run a git command on a repository."""
    try:
        full_cmd = f"git -C {repo} {command}" if os.path.exists(repo) else f"git {command}"
        result = subprocess.run(
            full_cmd, shell=True, capture_output=True, text=True, timeout=60
        )
        return (result.returncode == 0, result.stdout, result.stderr)
    except Exception as e:
        return (False, "", str(e))


def run_parallel(
    items: List[str],
    worker: Callable,
    max_workers: int = 4,
    quiet: bool = False
) -> dict:
    """
    Run items in parallel using ThreadPoolExecutor.
    
    Args:
        items: List of items to process
        worker: Function to apply to each item
        max_workers: Number of parallel workers
        quiet: Suppress progress output
    
    Returns:
        dict: {item: (success, result, error)}
    """
    results = {}
    start_time = time.time()
    
    if not quiet:
        print(f"🚀 Starting {len(items)} tasks with {max_workers} workers...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_item = {executor.submit(worker, item): item for item in items}
        
        # Process as they complete
        completed = 0
        for future in concurrent.futures.as_completed(future_to_item):
            item = future_to_item[future]
            try:
                results[item] = future.result()
            except Exception as e:
                results[item] = (False, "", str(e))
            
            completed += 1
            if not quiet:
                progress = (completed / len(items)) * 100
                print(f"  [{progress:5.1f}%] {completed}/{len(items)} completed", end="\r")
    
    elapsed = time.time() - start_time
    
    # Summary
    success_count = sum(1 for s, _, _ in results.values() if s)
    failed_count = len(results) - success_count
    
    if not quiet:
        print()  # New line
        print(f"✅ Completed: {success_count} | ❌ Failed: {failed_count} | ⏱️ {elapsed:.2f}s")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Parallel execution utilities for Clawdbot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parallel curl from file
  parallel-exec.py curl urls.txt
  
  # Parallel exec from file (4 workers)
  parallel-exec.py exec commands.txt -w 4
  
  # Parallel API calls
  parallel-exec.py api endpoints.txt -w 8
  
  # Parallel downloads
  parallel-exec.py download files.txt ./downloads -w 4
  
  # Parallel git operations
  parallel-exec.py git repos.txt "pull" -w 4
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Curl command
    curl_parser = subparsers.add_parser('curl', help='Parallel curl requests')
    curl_parser.add_argument('file', help='File with URLs (one per line)')
    curl_parser.add_argument('-w', '--workers', type=int, default=4, help='Number of workers')
    curl_parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    curl_parser.add_argument('-o', '--output', help='Output directory for results')
    
    # Exec command
    exec_parser = subparsers.add_parser('exec', help='Parallel command execution')
    exec_parser.add_argument('file', help='File with commands (one per line)')
    exec_parser.add_argument('-w', '--workers', type=int, default=4, help='Number of workers')
    exec_parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    # API command
    api_parser = subparsers.add_parser('api', help='Parallel API calls')
    api_parser.add_argument('file', help='File with endpoints (one per line)')
    api_parser.add_argument('-w', '--workers', type=int, default=8, help='Number of workers')
    api_parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    api_parser.add_argument('-o', '--output', help='Output directory for results')
    
    # Download command
    dl_parser = subparsers.add_parser('download', help='Parallel file downloads')
    dl_parser.add_argument('file', help='File with URLs (one per line)')
    dl_parser.add_argument('output', help='Output directory')
    dl_parser.add_argument('-w', '--workers', type=int, default=4, help='Number of workers')
    dl_parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    # Git command
    git_parser = subparsers.add_parser('git', help='Parallel git operations')
    git_parser.add_argument('file', help='File with repos or commands')
    git_parser.add_argument('command', help='Git command to run')
    git_parser.add_argument('-w', '--workers', type=int, default=4, help='Number of workers')
    git_parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Read items from file
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    with open(args.file, 'r') as f:
        items = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not items:
        print("Error: No items found in file", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.command == 'curl':
            output_dir = args.output or "./curl_output"
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            def curl_worker(url):
                success, content, error = curl_url(url)
                if success and output_dir:
                    filename = url.split('/')[-1] or f"response_{hash(url)}.txt"
                    with open(os.path.join(output_dir, filename), 'w') as f:
                        f.write(content)
                return success, content[:200] if success else "", error
            
            results = run_parallel(items, curl_worker, args.workers, args.quiet)
        
        elif args.command == 'exec':
            def exec_worker(cmd):
                return run_command(cmd)
            
            results = run_parallel(items, exec_worker, args.workers, args.quiet)
        
        elif args.command == 'api':
            output_dir = args.output or "./api_output"
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            def api_worker(endpoint):
                success, content, error = curl_url(endpoint)
                if success and output_dir:
                    filename = endpoint.split('/')[-1] or f"api_{hash(endpoint)}.json"
                    with open(os.path.join(output_dir, filename), 'w') as f:
                        f.write(content)
                return success, content[:200] if success else "", error
            
            results = run_parallel(items, api_worker, args.workers, args.quiet)
        
        elif args.command == 'download':
            os.makedirs(args.output, exist_ok=True)
            
            def download_worker(url):
                success, filepath, error = download_file(url, args.output)
                return success, filepath, error
            
            results = run_parallel(items, download_worker, args.workers, args.quiet)
        
        elif args.command == 'git':
            def git_worker(item):
                return git_command(item, args.command)
            
            results = run_parallel(items, git_worker, args.workers, args.quiet)
        
        else:
            parser.print_help()
            sys.exit(1)
        
        # Exit with error if any failed
        failed = sum(1 for s, _, _ in results.values() if not s)
        if failed > 0:
            print(f"⚠️ {failed} tasks failed", file=sys.stderr)
            # List failed items
            for item, (success, _, error) in results.items():
                if not success:
                    print(f"  - {item}: {error[:100]}", file=sys.stderr)
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n⏸️ Interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
