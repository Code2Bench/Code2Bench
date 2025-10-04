from typing import List

def split_parameters(params_str: str) -> List[str]:
    result = []
    i = 0
    while i < len(params_str):
        if params_str[i] == ',':
            # Check if the next character is a nested type opener
            if i + 1 < len(params_str) and params_str[i+1] in '<[{"':
                # Skip the nested type opener
                i += 1
            else:
                # Add the comma as a separator
                result.append(params_str[i])
                i += 1
        else:
            # Collect characters until the next comma or end of string
            j = i
            while j < len(params_str) and params_str[j] != ',' and params_str[j] != ']':
                j += 1
            result.append(params_str[i:j])
            i = j
    return result