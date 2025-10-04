def align_first_line_to_second(code_string: str) -> str:
    lines = code_string.splitlines()
    non_empty_lines = [line for line in lines if line.strip()]
    
    if len(non_empty_lines) < 2:
        return code_string
    
    first_line = non_empty_lines[0]
    second_line = non_empty_lines[1]
    
    # Find the indentation of the first non-empty line
    first_indent = first_line.lstrip()
    # Find the indentation of the second non-empty line
    second_indent = second_line.lstrip()
    
    # Align the first non-empty line's indentation to the second
    aligned_lines = []
    for line in lines:
        if line.strip() == "":
            aligned_lines.append(line)
        else:
            # Calculate the new indentation
            new_indent = " " * (len(second_indent) - len(first_indent) + len(line.lstrip()))
            aligned_lines.append(line.ljust(new_indent))
    
    return "\n".join(aligned_lines)