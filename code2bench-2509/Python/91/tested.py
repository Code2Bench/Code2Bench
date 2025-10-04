def remove_binary_diffs(patch_text: str) -> str:
    import re
    
    # Regular expression to match diff blocks
    diff_block_pattern = r'diff --git a/(.*?)[\s\S]+?diff --git b/(.*?)[\s\S]*?Binary files'
    
    # Find all diff blocks
    diff_blocks = re.finditer(diff_block_pattern, patch_text)
    
    # Process each diff block
    result = []
    for match in diff_blocks:
        # Extract the file paths
        a_file = match.group(1)
        b_file = match.group(2)
        
        # Skip the block if it contains a 'Binary files' line
        if 'Binary files' in patch_text[match.start():match.end()]:
            continue
        
        # Add the non-binary diff block to the result
        result.append(patch_text[match.start():match.end()])
    
    return ''.join(result)