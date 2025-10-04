from typing import str
import re

def _optimize_prompt_for_imagen(prompt: str) -> str:
    # Remove Gemini-specific formatting
    prompt = re.sub(r'Enhanced prompt:\s*$', '', prompt, flags=re.MULTILINE)
    prompt = re.sub(r'Aspect ratio:\s*$', '', prompt, flags=re.MULTILINE)
    
    # Clean up extra whitespace
    prompt = ' '.join(prompt.split())
    
    # Add enhancements based on content (example: LinkedIn professional content or technology)
    if 'linkedin' in prompt.lower() or 'technology' in prompt.lower():
        prompt += " Ensure the output is professional and tailored for a LinkedIn audience."
    
    # Truncate to 480 tokens
    max_tokens = 480
    if len(prompt) > max_tokens:
        prompt = prompt[:max_tokens]
    
    return prompt