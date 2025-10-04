from typing import Any, Dict

from typing import Dict, Any

def _format_platform_constraints(platform: str, platform_adaptation: Dict[str, Any]) -> str:
    content_rules = platform_adaptation.get("content_format_rules", {})
    engagement = platform_adaptation.get("engagement_patterns", {})

    constraints = []

    if content_rules.get("character_limit"):
        constraints.append(f"Character limit: {content_rules['character_limit']}")

    if content_rules.get("optimal_length"):
        constraints.append(f"Optimal length: {content_rules['optimal_length']}")

    if engagement.get("posting_frequency"):
        constraints.append(f"Frequency: {engagement['posting_frequency']}")

    if platform == "twitter":
        constraints.extend([
            "Max 3 hashtags",
            "Thread-friendly format",
            "Engagement-optimized"
        ])
    elif platform == "linkedin":
        constraints.extend([
            "Professional networking focus",
            "Thought leadership tone",
            "Business value emphasis"
        ])
    elif platform == "blog":
        constraints.extend([
            "SEO-optimized structure",
            "Scannable format",
            "Clear headings"
        ])

    return "- " + "\n- ".join(constraints) if constraints else "- Standard platform optimization"