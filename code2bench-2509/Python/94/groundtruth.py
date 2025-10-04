

def align_first_line_to_second(code_string: str) -> str:
    lines = code_string.splitlines()

    first_line_info = None
    second_line_info = None

    for index, line_content in enumerate(lines):
        if line_content.strip():
            if first_line_info is None:
                first_line_info = {"index": index, "content": line_content}
            elif second_line_info is None:
                second_line_info = {"index": index, "content": line_content}
                break

    if not first_line_info or not second_line_info:
        return code_string

    first_line_content = first_line_info["content"]
    second_line_content = second_line_info["content"]

    first_line_indent = " " * (
        len(first_line_content) - len(first_line_content.lstrip(" "))
    )
    second_line_indent = " " * (
        len(second_line_content) - len(second_line_content.lstrip(" "))
    )

    if first_line_indent != second_line_indent:
        original_index = first_line_info["index"]
        stripped_content = first_line_content.lstrip(" ")
        lines[original_index] = second_line_indent + stripped_content

    return "\n".join(lines)