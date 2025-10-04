def extract_boxed_content(ans: str) -> str:
    import re
    # Find all occurrences of \boxed{...}
    matches = re.findall(r'\\boxed{(.*?)}', ans)
    if not matches:
        return ans
    # Check if the last match is balanced
    last_match = matches[-1]
    if re.match(r'^\boxed{(.+)}$', last_match):
        return last_match[1:]
    return ans