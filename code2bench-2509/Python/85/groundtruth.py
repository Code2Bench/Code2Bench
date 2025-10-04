

def find_boxed_content_with_boxed(text: str) -> list[str]:
    """
    Extract all top-level \boxed{...} contents from the input string,
    handling nested braces correctly.

    This function scans the string manually to ensure proper brace matching,
    allowing for nested expressions inside \boxed{}, but only extracting
    the outermost matched segments.

    Behavior:
    - For nested boxed expressions like \\boxed{\\boxed{\\boxed{42}}},
      it returns ['\\boxed{\\boxed{42}}'] — treating the entire nested structure as one match.
    - For multiple separate boxed expressions like
      \\boxed{42} and \\boxed{42}, it returns ['42', '42'].

    Returns:
        A list of strings extracted from each top-level \boxed{...} block.
    """
    results = []
    i = 0
    while i < len(text):
        if text[i : i + 7] == "\\boxed{":
            i += 7  # Move past "\boxed{"
            content = ""
            brace_count = 1
            while i < len(text) and brace_count > 0:
                if text[i] == "{":
                    brace_count += 1
                elif text[i] == "}":
                    brace_count -= 1

                if brace_count > 0:
                    content += text[i]
                i += 1

            results.append(content)
        else:
            i += 1
    return results