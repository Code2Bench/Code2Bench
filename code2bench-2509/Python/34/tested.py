def find_box(pred_str: str) -> str:
    import re
    
    # Find all occurrences of 'boxed' in the string
    boxed_pos = pred_str.find("boxed")
    
    if boxed_pos == -1:
        return ""
    
    # Extract the content after 'boxed'
    content = pred_str[boxed_pos + len("boxed"):]
    
    # Check if content is enclosed in curly braces
    if "{" in content and "}" in content:
        # Find the outermost braces
        start = content.find("{")
        end = content.rfind("}")
        return content[start:end + 1]
    else:
        # Find the first occurrence of $ or end of string
        dollar_pos = content.find("$")
        if dollar_pos == -1:
            return content
        else:
            return content[:dollar_pos]