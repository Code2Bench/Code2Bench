import re

def remove_mnemonic_marker(label: str) -> str:
    # Use regular expression to replace all single ampersands with empty string
    return re.sub(r'&', '', label)