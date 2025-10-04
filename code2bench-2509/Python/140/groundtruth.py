

def get_replaced_content(
    content: list[str],
    extras_list: list[str],
    start_line: str,
    end_line: str,
    prefix: str,
    suffix: str,
    add_empty_lines: bool,
) -> list[str]:
    result = []
    is_copying = True
    for line in content:
        if line.startswith(start_line):
            result.append(f"{line}")
            if add_empty_lines:
                result.append("\n")
            is_copying = False
            for extra in extras_list:
                result.append(f"{prefix}{extra}{suffix}\n")
        elif line.startswith(end_line):
            if add_empty_lines:
                result.append("\n")
            result.append(f"{line}")
            is_copying = True
        elif is_copying:
            result.append(line)
    return result