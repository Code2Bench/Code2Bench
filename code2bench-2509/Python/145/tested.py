def remove_consecutive_t(input_str: str) -> str:
    result = []
    i = 0
    while i < len(input_str):
        if input_str[i] == 't':
            # Check for sequences of three or more 't's
            count = 1
            while i + count < len(input_str) and input_str[i + count] == 't':
                count += 1
            if count >= 3:
                # Remove the sequence
                i += count
            else:
                # Add the sequence if it's one or two 't's
                result.append('t' * count)
                i += count
        else:
            result.append(input_str[i])
            i += 1
    return ''.join(result)