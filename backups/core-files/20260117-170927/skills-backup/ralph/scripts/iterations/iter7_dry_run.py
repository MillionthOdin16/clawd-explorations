#!/usr/bin/env python3
"""
Dry-run mode support for Ralph coordinator.

Add --dry-run flag to preview without executing.
"""

import sys


def add_dry_run_args():
    """Add dry-run argument parsing."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview actions without executing')
    return parser.parse_known_args()


# To implement dry-run, modify coordinator.py:

DRY_RUN_TEMPLATE = '''
# In coordinator.py main() function, add near the top:

if __name__ == "__main__":
    dry_run, argv = add_dry_run_args()
    
    if dry_run:
        print("="*60)
        print("🔍 DRY RUN MODE - No changes will be made")
        print("="*60)
    
    # Rest of main() logic...
    
    # When about to execute a task:
    if dry_run:
        print(f"\\n📋 Would execute task {task_index}: {task['description']}")
        print(f"   Files: {task.get('files', 'N/A')}")
        print(f"   Verify: {task.get('verify', 'N/A')}")
        print(f"   Commit: {task.get('commit', 'N/A')}")
        continue  # Skip actual execution
'''

# Implementation for new-spec.py:
NEW_SPEC_DRY_RUN = '''
# In new-spec.py main() function:

def main():
    import sys
    dry_run = '--dry-run' in sys.argv
    
    if dry_run:
        sys.argv.remove('--dry-run')
    
    if len(sys.argv) < 2:
        print("Usage: new-spec.py [--dry-run] <name> [goal]")
        sys.exit(1)
    
    name_input = sys.argv[1]
    goal = sys.argv[2] if len(sys.argv) > 2 else name_input
    
    if dry_run:
        print("="*60)
        print("🔍 DRY RUN MODE - Would create:")
        print(f"   Spec name: {slugify(name_input)}")
        print(f"   Goal: {goal}")
        print(f"   Files:")
        for t in ['research.md', 'requirements.md', 'design.md', 'tasks.md']:
            print(f"     - specs/{slugify(name_input)}/{t}")
        print("="*60)
        return
    
    # Rest of existing code...
'''
