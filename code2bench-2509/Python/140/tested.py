from typing import List

def get_replaced_content(
    content: List[str],
    extras_list: List[str],
    start_line: str,
    end_line: str,
    prefix: str,
    suffix: str,
    add_empty_lines: bool,
) -> List[str]:
    result = []
    i = 0
    while i < len(content):
        if content[i] == start_line:
            # Add empty lines if required
            if add_empty_lines:
                result.append("")
            # Add the extra lines
            for extra in extras_list:
                result.append(prefix + extra + suffix)
            i += 1
        elif content[i] == end_line:
            # Add empty lines if required
            if add_empty_lines:
                result.append("")
            i += 1
        else:
            result.append(content[i])
            i += 1
    return result