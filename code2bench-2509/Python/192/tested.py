from typing import Dict, Any

def _format_platform_constraints(platform: str, platform_adaptation: Dict[str, Any]) -> str:
    constraints = []

    # Extract content format rules and engagement patterns
    content_format_rules = platform_adaptation.get('content_format_rules', {})
    engagement_patterns = platform_adaptation.get('engagement_patterns', {})

    # Add constraints based on content format rules
    if 'character_limit' in content_format_rules:
        constraints.append(f'- Character limit: {content_format_rules["character_limit"]}')
    if 'optimal_length' in content_format_rules:
        constraints.append(f'- Optimal length: {content_format_rules["optimal_length"]}')

    # Add constraints based on engagement patterns
    if 'posting_frequency' in engagement_patterns:
        constraints.append(f'- Posting frequency: {engagement_patterns["posting_frequency"]} posts per day')

    # Add platform-specific constraints
    if platform == 'twitter':
        constraints.append('- Twitter-specific constraints: 280 characters max, 2-3 posts per day')
    elif platform == 'linkedin':
        constraints.append('- LinkedIn-specific constraints: 250 characters max, 1 post per day')
    elif platform == 'blog':
        constraints.append('- Blog-specific constraints: 5000 characters max, 1 post per day')

    # Return the formatted constraints or default message
    return '\n'.join(constraints) if constraints else '- Standard platform optimization'