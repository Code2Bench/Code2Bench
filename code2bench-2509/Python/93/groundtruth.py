

def remove_mnemonic_marker(label: str) -> str:
    """Remove existing accelerator markers (&) from a label."""
    result = ""
    skip = False
    for i, ch in enumerate(label):
        if skip:
            skip = False
            continue
        if ch == "&":
            # escaped ampersand "&&"
            if i + 1 < len(label) and label[i + 1] == "&":
                result += "&&"
                skip = True
            # otherwise skip this '&'
            continue
        result += ch
    return result