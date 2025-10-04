

def split_parameters(params_str: str) -> list:
    """Split parameter string by commas, handling nested types."""
    params = []
    current_param = ""
    depth = 0

    for char in params_str:
        if char in "<[{(":
            depth += 1
        elif char in ">]})":
            depth -= 1
        elif char == "," and depth == 0:
            params.append(current_param)
            current_param = ""
            continue

        current_param += char

    if current_param:
        params.append(current_param)

    return params