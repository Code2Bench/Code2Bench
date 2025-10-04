

def _format_community_content(base_text: str, entities: list[str], keywords: list[str]) -> str:
    if not entities and not keywords:
        return base_text

    content_parts = [base_text, "\n  Contains:"]

    if entities:
        shown = entities[:3]
        entities_text = f"\n    Entities: {', '.join(shown)}"
        if len(entities) > 3:
            entities_text += f" and {len(entities) - 3} more"
        content_parts.append(entities_text)

    if keywords:
        shown = keywords[:3]
        keywords_text = f"\n    Keywords: {', '.join(shown)}"
        if len(keywords) > 3:
            keywords_text += f" and {len(keywords) - 3} more"
        content_parts.append(keywords_text)

    return "".join(content_parts)