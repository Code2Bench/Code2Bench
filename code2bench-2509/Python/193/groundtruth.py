from typing import Any, Dict, List

from typing import Dict, List, Any

def _identify_content_gaps(content_type: Dict[str, Any], writing_style: Dict[str, Any]) -> List[str]:
    gaps = []
    primary_type = content_type.get('primary_type', 'blog')

    if primary_type == 'blog':
        gaps.extend(['Video tutorials', 'Case studies', 'Infographics'])
    elif primary_type == 'video':
        gaps.extend(['Blog posts', 'Whitepapers', 'Webinars'])

    tone = writing_style.get('tone', 'professional')
    if tone == 'professional':
        gaps.append('Personal stories')
    elif tone == 'casual':
        gaps.append('Expert interviews')

    return gaps