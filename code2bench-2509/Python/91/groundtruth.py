

def remove_binary_diffs(patch_text):
    """
    Remove binary file diffs from a git patch.

    Args:
        patch_text (str): The git patch text

    Returns:
        str: The cleaned patch text with binary diffs removed
    """
    lines = patch_text.splitlines()
    cleaned_lines = []
    block = []
    is_binary_block = False

    for line in lines:
        if line.startswith('diff --git '):
            if block and not is_binary_block:
                cleaned_lines.extend(block)
            block = [line]
            is_binary_block = False
        elif 'Binary files' in line:
            is_binary_block = True
            block.append(line)
        else:
            block.append(line)

    if block and not is_binary_block:
        cleaned_lines.extend(block)
    return '\n'.join(cleaned_lines)