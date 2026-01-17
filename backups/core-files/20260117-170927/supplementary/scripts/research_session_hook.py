#!/usr/bin/env python3
"""
Research Session Hook
Automatically activates V2.0 research framework when deep research is requested.

INTEGRATION:
- Import at session start: from scripts.research_session_hook import *
- Auto-detects research keywords in task description
- Loads framework automatically if research is detected

TRIGGERS:
- "deep research", "research report", "investigate"
- "background check", "profile analysis", "due diligence"
- "find information on", "learn about", "compile report on"
"""

import os
import sys
import re
from datetime import datetime

# Research keywords that trigger automatic framework loading
RESEARCH_TRIGGERS = [
    r"deep\s*research",
    r"research\s*(report|on|about)?",
    r"investigate",
    r"background\s*(check|analysis)",
    r"profile\s*(analysis|research)",
    r"due\s*diligence",
    r"find\s*(information|details|data)\s*(on|about)",
    r"learn\s*about",
    r"compile\s*(a\s*)?report\s*(on|about)",
    r"full\s*analysis",
    r"comprehensive\s*(research|report)",
    r"background\s*on",
    r"investigation\s*(of|into)?",
    r"intelligence\s*(report|on|about)?",
]

# Research task types
TARGET_TYPES = {
    "technical_professional": ["engineer", "developer", "programmer", "technologist", "scientist"],
    "academic": ["professor", "researcher", "phd", "academic", "scholar"],
    "public_figure": ["ceo", "founder", "politician", "celebrity", "executive"],
    "business": ["entrepreneur", "businessman", "businesswoman", "investor"],
    "historical": ["historical", "figure", "leader", "pioneer"],
}


def detect_research_request(task_description):
    """
    Analyze task description for research request.
    
    Args:
        task_description: String describing the task
    
    Returns:
        dict with is_research, trigger_match, suggested_type
    """
    task_lower = task_description.lower()
    
    # Check for research triggers
    is_research = False
    trigger_match = None
    
    for pattern in RESEARCH_TRIGGERS:
        if re.search(pattern, task_lower):
            is_research = True
            trigger_match = pattern
            break
    
    # Detect target type
    suggested_type = "technical_professional"  # default
    
    for target_type, keywords in TARGET_TYPES.items():
        for keyword in keywords:
            if keyword in task_lower:
                suggested_type = target_type
                break
    
    return {
        "is_research": is_research,
        "trigger_pattern": trigger_match,
        "suggested_type": suggested_type,
        "task_preview": task_description[:100] + "..." if len(task_description) > 100 else task_description
    }


def auto_load_research_framework(task_description):
    """
    Automatically load research framework if research detected.
    
    Args:
        task_description: The task to analyze
    
    Returns:
        dict with framework loaded status and quick actions
    """
    detection = detect_research_request(task_description)
    
    if detection["is_research"]:
        print(f"\n🔍 RESEARCH DETECTED: {detection['trigger_pattern']}")
        print(f"   Target Type: {detection['suggested_type']}")
        print(f"   Task: {detection['task_preview']}")
        
        # Auto-load framework
        try:
            sys.path.insert(0, "/home/opc/clawd/scripts")
            from research_loader import load_research_framework, assess_complexity, calculate_rqs
            framework = load_research_framework()
            
            # Calculate complexity
            complexity = assess_complexity(detection["suggested_type"])
            
            return {
                "status": "loaded",
                "framework": framework,
                "complexity": complexity,
                "quick_actions": [
                    f"python scripts/research_loader.py '{task_description}'",
                    "qmd search target -c memory (check existing)",
                    "git clone --bare https://github.com/user/repo.git"
                ]
            }
        except ImportError as e:
            return {
                "status": "error",
                "message": f"Could not load framework: {e}",
                "manual_steps": [
                    "1. Read RESEARCH_FRAMEWORK_V2.md",
                    "2. Load framework manually",
                    "3. Execute research workflow"
                ]
            }
    else:
        return {
            "status": "not_research",
            "message": "No research trigger detected",
            "task_type": "general"
        }


def print_research_banner():
    """Print V2.0 research framework banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════════╗
║          🔍 V2.0 RESEARCH FRAMEWORK AUTO-LOADED 🔍                ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  PHASES:                                                          ║
║  1. GROUND TRUTH    → Internal check, complexity, MVO             ║
║  2. DISCOVER & MAP  → API sweep, creative exploration, dig deeper ║
║  3. SYNTHESIZE      → Pattern detection, narrative, quality scores║
║  4. INSIGHT OUTPUT  → Visual intelligence, confidence dashboard   ║
║                                                                   ║
║  QUALITY GATES:                                                   ║
║  • RQS > 70                                                        ║
║  • Completeness > 60%                                              ║
║  • Insight Density > 0.15                                          ║
║  • Internal knowledge integrated                                   ║
║  • Narrative arc present                                           ║
║  • Visual element included                                         ║
║                                                                   ║
║  DOCS: /home/opc/clawd/memory/RESEARCH_FRAMEWORK_V2.md            ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


# Auto-execute if run directly
if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = " ".join(sys.argv[1:])
        result = auto_load_research_framework(task)
        
        if result["status"] == "loaded":
            print_research_banner()
            print(f"\n✅ Framework loaded for: {task}")
            print(f"   Estimated time: {result['complexity']['estimated_minutes']} minutes")
    else:
        print("Usage: python research_session_hook.py \"RESEARCH TASK DESCRIPTION\"")
        print("\nExamples:")
        print('  python research_session_hook.py "Deep research on Bradley Hallier"')
        print('  python research_session_hook.py "Compile a report on Elon Musk"')
        print('  python research_session_hook.py "Investigate competitor background"')
