

def remove_consecutive_t(input_str):
    result = []
    count = 0

    for char in input_str:
        if char == "t":
            count += 1
        else:
            if count < 3:
                result.extend(["t"] * count)
            count = 0
            result.append(char)

    if count < 3:
        result.extend(["t"] * count)

    return "".join(result)