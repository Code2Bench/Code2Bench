

def _optimize_prompt_for_imagen(prompt: str) -> str:
    """
    Optimize prompt for Imagen API by removing Gemini-specific formatting
    and enhancing it with Imagen best practices.

    Based on Imagen prompt guide: https://ai.google.dev/gemini-api/docs/imagen
    """
    # Remove Gemini-specific formatting
    prompt = prompt.replace('\n\nEnhanced prompt:', '')
    prompt = prompt.replace('\n\nAspect ratio:', '')

    # Clean up extra whitespace
    prompt = ' '.join(prompt.split())

    # Add Imagen-specific enhancements if not present
    if 'professional' in prompt.lower() and 'linkedin' in prompt.lower():
        # Enhance for LinkedIn professional content
        prompt += ", high quality, professional photography, business appropriate"

    if 'digital transformation' in prompt.lower() or 'technology' in prompt.lower():
        # Enhance for tech content
        prompt += ", modern, innovative, clean design, corporate aesthetic"

    # Ensure prompt doesn't exceed Imagen's 480 token limit
    if len(prompt) > 400:  # Leave some buffer
        prompt = prompt[:400] + "..."

    return prompt