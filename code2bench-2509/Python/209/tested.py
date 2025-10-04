def _clean_content(content: str) -> str:
    # Remove trailing whitespace from each line
    lines = [line.rstrip() for line in content.split('\n')]
    
    # Remove empty lines from the beginning and end of the content
    filtered_lines = [line for line in lines if line]
    
    # Join the lines back into a single string
    return '\n'.join(filtered_lines)