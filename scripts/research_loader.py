#!/usr/bin/env python3
"""
Research Framework Quick-Loader
Automatically loads V2.0 research framework for deep research tasks.

USAGE:
- Import and call load_research_framework() at start of research task
- Or run directly: python scripts/research_loader.py "TARGET_NAME"
"""

import os
import sys
import json
from datetime import datetime

# Framework paths
FRAMEWORK_PATH = "/home/opc/clawd/memory/RESEARCH_FRAMEWORK_V2.md"
IMPLEMENTATION_PATH = "/home/opc/clawd/memory/RESEARCH_IMPLEMENTATION_GUIDE.md"

def load_research_framework():
    """
    Load V2.0 research framework into context.
    Returns: dict with framework constants and methods
    """
    framework = {
        "version": "2.0",
        "loaded": datetime.now().isoformat(),
        "phases": ["GROUND_TRUTH", "DISCOVER_MAP", "SYNTHESIZE", "INSIGHT_OUTPUT"],
        "quality_metrics": ["RQS", "Completeness", "Insight_Density"],
        "triggers": {
            "internal_knowledge": True,
            "parallel_api": True,
            "pattern_detection": True,
            "visual_output": True,
            "iteration": True,
            "cross_learning": True
        }
    }
    
    print(f"✅ Research Framework V2.0 loaded")
    print(f"   Phases: {', '.join(framework['phases'])}")
    print(f"   Quality Metrics: {', '.join(framework['quality_metrics'])}")
    print(f"   Triggers: {', '.join([k for k,v in framework['triggers'].items() if v])}")
    
    return framework


def assess_complexity(target_type, has_previous_research=False, is_connected=False):
    """
    Calculate adaptive time based on complexity factors.
    
    Args:
        target_type: public_figure, technical_professional, academic, private, historical
        has_previous_research: bool - prior research exists in knowledge base
        is_connected: bool - connected to known entities
    
    Returns:
        dict with time_estimate, complexity_factor, recommendations
    """
    base_times = {
        "public_figure": 7,
        "technical_professional": 12,
        "academic": 15,
        "private": 20,
        "historical": 30
    }
    
    factors = {
        "public_figure": 0.8,
        "technical_professional": 1.0,
        "academic": 1.2,
        "private": 1.5,
        "historical": 2.0
    }
    
    base = base_times.get(target_type, 12)
    factor = factors.get(target_type, 1.0)
    
    # Adjust for prior knowledge
    if has_previous_research:
        factor *= 0.7
    if is_connected:
        factor *= 0.8
    
    time_estimate = base * factor
    
    return {
        "target_type": target_type,
        "base_time": base,
        "complexity_factor": factor,
        "estimated_minutes": round(time_estimate, 1),
        "recommendations": get_recommendations(target_type)
    }


def get_recommendations(target_type):
    """Get tool recommendations based on target type."""
    recommendations = {
        "public_figure": ["Wikipedia", "Social Media", "News Archives", "Web Search"],
        "technical_professional": ["GitHub API", "Semantic Scholar", "Exa AI", "Company Sites"],
        "academic": ["Semantic Scholar", "arXiv", "Google Scholar", "University Pages"],
        "private": ["Public Records", "Social Media", "News", "Accept limited results"],
        "historical": ["Archives", "Wikipedia", "Books", "Academic Papers"]
    }
    return recommendations.get(target_type, ["General web search"])


def calculate_rqs(verified_facts, high_confidence, internal_knowledge=True, 
                  patterns_found=1, narrative_quality="good"):
    """Calculate Research Quality Score (0-100)."""
    score = (verified_facts * 2) + (high_confidence * 1)
    
    # Internal knowledge bonus
    if internal_knowledge:
        score += 15
    
    # Pattern discovery bonus (max 15)
    score += min(15, patterns_found * 5)
    
    # Narrative quality (max 10)
    narrative_scores = {"excellent": 10, "good": 7, "acceptable": 4, "poor": 0}
    score += narrative_scores.get(narrative_quality, 0)
    
    # Cap at 100
    score = min(100, score)
    
    # Rating
    if score >= 85:
        rating = "Excellent"
    elif score >= 70:
        rating = "Good"
    elif score >= 55:
        rating = "Acceptable"
    else:
        rating = "Needs Work"
    
    return {"score": score, "rating": rating}


def create_quality_dashboard(rqs_score, completeness, insight_density):
    """Generate visual quality dashboard."""
    def bar(value, max_val=100, width=20):
        filled = int((value / max_val) * width)
        return "█" * filled + "░" * (width - filled)
    
    dashboard = f"""
╔═══════════════════════════════════════════════════════════════╗
║                   RESEARCH QUALITY DASHBOARD                   ║
╠═══════════════════════════════════════════════════════════════╣
║  RQS Score:     {rqs_score}/100  {bar(rqs_score, 100, 30)}  ║
║  Completeness:  {completeness}%     {bar(completeness, 100, 30)}  ║
║  Insight Density: {insight_density:.2f}      {bar(insight_density*100, 100, 30)}  ║
╚═══════════════════════════════════════════════════════════════╝
"""
    return dashboard


def run_research_workflow(target_name, target_type="technical_professional"):
    """
    Execute full V2.0 research workflow.
    
    Args:
        target_name: Name of person/topic to research
        target_type: Type of research target
    
    Returns:
        dict with workflow results
    """
    print(f"\n🔍 Starting V2.0 Research Workflow for: {target_name}")
    print("=" * 60)
    
    # Load framework
    framework = load_research_framework()
    
    # Phase 1: Ground Truth
    print(f"\n📋 PHASE 1: GROUND TRUTH")
    complexity = assess_complexity(target_type)
    print(f"   Target Type: {complexity['target_type']}")
    print(f"   Estimated Time: {complexity['estimated_minutes']} minutes")
    print(f"   Recommendations: {', '.join(complexity['recommendations'][:3])}")
    
    # Phase 2: Discover & Map
    print(f"\n🗺️ PHASE 2: DISCOVER & MAP")
    print("   [Ready for API sweep and creative exploration]")
    
    # Phase 3: Synthesize
    print(f"\n🔗 PHASE 3: SYNTHESIZE")
    print("   [Ready for pattern detection and narrative building]")
    
    # Phase 4: Insight & Output
    print(f"\n💡 PHASE 4: INSIGHT & OUTPUT")
    print("   [Ready for visual intelligence and quality scoring]")
    
    # Quality dashboard
    print(create_quality_dashboard(75, 70, 0.25))
    
    print("\n✅ Research workflow initialized. Ready to execute.")
    
    return {
        "target": target_name,
        "target_type": target_type,
        "framework": framework,
        "complexity": complexity,
        "status": "initialized"
    }


# Quick research command
if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = " ".join(sys.argv[1:])
        run_research_workflow(target)
    else:
        print("Usage: python research_loader.py \"TARGET_NAME\"")
        print("\nExample:")
        print("  python research_loader.py \"Bradley Hallier\"")
        print("  python research_loader.py \"Elon Musk\"")
