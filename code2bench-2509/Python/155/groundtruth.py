from typing import Optional

def extract_examples_section(docstring: Optional[str]) -> Optional[str]:
    """Extracts the 'Examples:' section from a Google-style docstring.

    Args:
        docstring (Optional[str]): The full docstring of a function.

    Returns:
        Optional[str]: The extracted examples section, or None if not found.
    """
    if not docstring or "Examples:" not in docstring:
        return None

    lines = docstring.strip().splitlines()
    in_examples = False
    examples_lines = []

    for line in lines:
        stripped = line.strip()

        if not in_examples and stripped.startswith("Examples:"):
            in_examples = True
            examples_lines.append(line)
            continue

        if in_examples:
            if stripped and not line.startswith(" ") and stripped.endswith(":"):
                break
            examples_lines.append(line)

    return "\n".join(examples_lines).strip() if examples_lines else None