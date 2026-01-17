#!/usr/bin/env python3
"""
Ralph New Spec Script
Creates a new spec with all required files.

Usage: python scripts/new-spec.py <spec-name> <goal>

Creates:
- specs/.current-spec
- specs/<name>/.ralph-state.json
- specs/<name>/.progress.md
- specs/<name>/research.md (template)
- specs/<name>/requirements.md (template)
- specs/<name>/design.md (template)
- specs/<name>/tasks.md (template)
"""

import sys
import os
import json
import re
from datetime import datetime

SPECS_DIR = "./specs"


def slugify(name):
    """Convert name to kebab-case."""
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def read_template(template_name):
    """Read template file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, '..', 'templates', template_name)
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: new-spec.py <spec-name> [goal]")
        print("  <spec-name>: Name in kebab-case (auto-converted from goal if not provided)")
        print("  [goal]: Optional goal description")
        sys.exit(1)
    
    name_input = sys.argv[1]
    goal = sys.argv[2] if len(sys.argv) > 2 else name_input
    
    # Convert to kebab-case if not already
    if ' ' in name_input or '_' in name_input:
        spec_name = slugify(name_input)
    else:
        spec_name = name_input
    
    spec_path = f"{SPECS_DIR}/{spec_name}"
    
    # Create spec directory
    os.makedirs(spec_path, exist_ok=True)
    print(f"Creating spec: {spec_name}")
    print(f"Goal: {goal}\n")
    
    # Create current-spec file
    with open(f"{SPECS_DIR}/.current-spec", 'w') as f:
        f.write(spec_name)
    
    # Initialize state
    state = {
        "source": "spec",
        "name": spec_name,
        "basePath": f"./specs/{spec_name}",
        "phase": "research",
        "taskIndex": 0,
        "totalTasks": 0,
        "taskIteration": 1,
        "maxTaskIterations": 5,
        "globalIteration": 1,
        "maxGlobalIterations": 100,
        "relatedSpecs": [],
        "parallelGroup": None,
        "taskResults": {}
    }
    with open(f"{spec_path}/.ralph-state.json", 'w') as f:
        json.dump(state, f, indent=2)
    
    # Create progress file
    progress = f"""---
spec: {spec_name}
phase: research
task: 0/0
updated: {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}
---

## Completed Tasks
None

## Current Task
Awaiting research phase

## Learnings
- Spec created

## Next
Start research phase with /ralph:research
"""
    with open(f"{spec_path}/.progress.md", 'w') as f:
        f.write(progress)
    
    # Create spec files from templates
    templates = {
        'research.md': ('research.md', 'Research', 'research'),
        'requirements.md': ('requirements.md', 'Requirements', 'requirements'),
        'design.md': ('design.md', 'Design', 'design'),
        'tasks.md': ('tasks.md', 'Tasks', 'tasks')
    }
    
    for template_file, title, phase in templates.values():
        template_content = read_template(template_file)
        if template_content:
            # Replace placeholders
            content = template_content.replace('${spec}', spec_name)
            content = content.replace('${phase}', phase)
            content = content.replace('${title}', title)
            content = content.replace('${created}', datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))
            if phase == 'tasks':
                content = content.replace('${total_tasks}', '0')
            
            with open(f"{spec_path}/{template_file}", 'w') as f:
                f.write(content)
    
    print(f"✓ Created spec structure at {spec_path}/")
    print(f"✓ Created current-spec")
    print(f"✓ Created .ralph-state.json")
    print(f"✓ Created .progress.md")
    print(f"✓ Created spec files: research.md, requirements.md, design.md, tasks.md")
    print(f"\nNext steps:")
    print(f"  1. /ralph:research - Fill in research.md")
    print(f"  2. /ralph:requirements - Generate requirements.md")
    print(f"  3. /ralph:design - Generate design.md")
    print(f"  4. /ralph:tasks - Generate tasks.md")
    print(f"  5. /ralph:implement - Execute tasks")
    print(f"\nOr run: python /home/opc/clawd/skills/ralph/scripts/quick-start.py {spec_name}")


if __name__ == "__main__":
    main()
