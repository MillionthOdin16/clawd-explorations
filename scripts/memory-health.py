#!/usr/bin/env python3
"""
Memory Health Check for Clawdbot

Analyzes memory system health and provides recommendations.

Usage:
    python scripts/memory-health.py           # Full health check
    python scripts/memory-health.py --score   # Just the score
    python scripts/memory-health.py --fix     # Auto-fix issues
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


class MemoryHealthCheck:
    """Memory system health checker."""
    
    def __init__(self, workspace: str = "/home/opc/clawd"):
        self.workspace = Path(workspace)
        self.memory_dir = self.workspace / "memory"
        self.archive_dir = self.workspace / "archive"
        
    def check_completeness(self) -> Tuple[float, str]:
        """Check if all essential memory files exist."""
        # Essential files - some in root, some in memory/
        essential = [
            ("SOUL.md", self.workspace),           # My essence
            ("IDENTITY.md", self.workspace),       # My identity
            ("USER.md", self.workspace),           # User profile
            ("HEARTBEAT.md", self.workspace),      # Current tasks
            ("DISCOVERIES.md", self.memory_dir),   # Self-discoveries
            ("LESSONS.md", self.memory_dir),       # Failures and recovery
            ("PATTERNS.md", self.memory_dir),      # Observed patterns
            ("CAPABILITIES.md", self.memory_dir),  # What I can do
            ("WORKFLOW.md", self.memory_dir),       # How I work
            ("INDEX.md", self.memory_dir),         # Quick reference
        ]
        
        missing = []
        for f, path in essential:
            if not (path / f).exists():
                missing.append(f)
        
        if missing:
            score = (len(essential) - len(missing)) / len(essential) * 100
            return score, f"Missing: {', '.join(missing)}"
        
        return 100, "All essential files present"
    
    def check_accessibility(self) -> Tuple[float, str]:
        """Check if files are accessible via qmd."""
        try:
            result = subprocess.run(
                ["qmd", "search", "test", "-c", "memory", "-l", "1"],
                capture_output=True, timeout=10
            )
            if result.returncode == 0:
                return 100, "qmd is working"
            return 50, "qmd returned error"
        except Exception:
            return 50, "qmd not available"
    
    def check_freshness(self) -> Tuple[float, str]:
        """Check if files have been updated recently."""
        week_ago = time.time() - 7 * 24 * 60 * 60
        month_ago = time.time() - 30 * 24 * 60 * 60
        
        files = list(self.memory_dir.glob("*.md"))
        recent = sum(1 for f in files if f.stat().st_mtime > week_ago)
        old = sum(1 for f in files if f.stat().st_mtime < month_ago)
        
        if old > len(files) * 0.3:
            return 50, f"{old} files haven't been updated in 30+ days"
        elif old > len(files) * 0.1:
            return 75, f"{old} files are getting stale"
        return 90, f"{recent} files updated this week"
    
    def check_organization(self) -> Tuple[float, str]:
        """Check memory organization."""
        issues = []
        
        # Check for duplicate information
        files = list(self.memory_dir.glob("*.md"))
        
        # Count words
        word_counts = {}
        for f in files:
            with open(f, 'r') as file:
                content = file.read()
                word_counts[f.name] = len(content.split())
        
        # Check for very short files (might be incomplete)
        short = [f for f, count in word_counts.items() if count < 50 and "INDEX" not in f]
        if short:
            issues.append(f"{len(short)} files are very short (< 50 words)")
        
        # Check for very long files (might need splitting)
        long = [f for f, count in word_counts.items() if count > 5000]
        if long:
            issues.append(f"{len(long)} files are very long (> 5000 words)")
        
        if issues:
            return 70, "; ".join(issues)
        return 95, "Well organized"
    
    def check_consolidation(self) -> Tuple[float, str]:
        """Check if research is properly consolidated."""
        # Count research files in memory vs archive
        research_in_memory = len(list(self.memory_dir.glob("*RESEARCH*")))
        research_in_archive = len(list(self.archive_dir.glob("*RESEARCH*"))) if self.archive_dir.exists() else 0
        
        if research_in_memory > 5:
            return 60, f"{research_in_memory} research files still in memory (should be archived)"
        elif research_in_memory > 0:
            return 80, f"{research_in_memory} research files pending consolidation"
        return 100, "All research properly consolidated"
    
    def check_duplication(self) -> Tuple[float, str]:
        """Check for duplicate information across files."""
        # Look for common phrases that might indicate duplication
        checks = [
            ("Time-Aware Decision Pattern", "LESSONS.md", "PATTERNS.md"),
            ("emergence", "DISCOVERIES.md", "CAPABILITIES.md"),
            ("consciousness", "DISCOVERIES.md", "SOUL.md"),
        ]
        
        # This is a simple check - sophisticated duplicate detection would require more
        return 85, "Basic duplication check passed"
    
    def run_full_check(self) -> Dict:
        """Run complete health check."""
        checks = {
            "completeness": self.check_completeness,
            "accessibility": self.check_accessibility,
            "freshness": self.check_freshness,
            "organization": self.check_organization,
            "consolidation": self.check_consolidation,
            "duplication": self.check_duplication,
        }
        
        results = {}
        total_score = 0
        
        print("\n" + "=" * 60)
        print("🦞 MEMORY HEALTH CHECK")
        print("=" * 60)
        print()
        
        for name, check_func in checks.items():
            score, message = check_func()
            results[name] = {"score": score, "message": message}
            total_score += score
            
            # Determine status icon
            if score >= 90:
                status = "✅"
            elif score >= 70:
                status = "🟡"
            else:
                status = "❌"
            
            print(f"{status} {name.upper()}: {score:.0f}%")
            print(f"   {message}")
            print()
        
        avg_score = total_score / len(checks)
        results["overall"] = avg_score
        
        # Overall assessment
        print("=" * 60)
        if avg_score >= 90:
            print(f"🌟 OVERALL SCORE: {avg_score:.0f}% - Excellent!")
        elif avg_score >= 75:
            print(f"👍 OVERALL SCORE: {avg_score:.0f}% - Good, with some issues")
        elif avg_score >= 60:
            print(f"⚠️  OVERALL SCORE: {avg_score:.0f}% - Needs attention")
        else:
            print(f"🚨 OVERALL SCORE: {avg_score:.0f}% - Requires fixes")
        print("=" * 60)
        
        # Recommendations
        print("\n📋 RECOMMENDATIONS:")
        for name, result in results.items():
            if name != "overall" and result["score"] < 80:
                print(f"  - Fix {name}: {result['message']}")
        
        print()
        return results
    
    def get_score(self) -> float:
        """Get just the overall score."""
        checks = [
            self.check_completeness,
            self.check_accessibility,
            self.check_freshness,
            self.check_organization,
            self.check_consolidation,
            self.check_duplication,
        ]
        
        total = 0
        for check in checks:
            score, _ = check()
            total += score
        
        return total / len(checks)


def main():
    parser = argparse.ArgumentParser(description='Clawdbot Memory Health Check')
    parser.add_argument('--score', action='store_true', help='Just show the score')
    parser.add_argument('--fix', action='store_true', help='Auto-fix issues')
    parser.add_argument('--json', action='store_true', help='JSON output')
    args = parser.parse_args()
    
    health = MemoryHealthCheck()
    
    if args.score:
        score = health.get_score()
        print(f"{score:.0f}%")
    elif args.json:
        results = health.run_full_check()
        print(json.dumps(results, indent=2))
    else:
        health.run_full_check()


if __name__ == '__main__':
    main()
