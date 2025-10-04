

def _clean_content(content: str) -> str:
    # Remove excessive whitespace
    lines = content.split('\n')
    cleaned_lines = []

    for line in lines:
        # Remove trailing whitespace
        line = line.rstrip()
        cleaned_lines.append(line)

    # Remove empty lines at the beginning and end
    while cleaned_lines and not cleaned_lines[0].strip():
        cleaned_lines.pop(0)

    while cleaned_lines and not cleaned_lines[-1].strip():
        cleaned_lines.pop()

    return '\n'.join(cleaned_lines)