from typing import Dict, Union

def build_expected_version_hex(matches: Dict[str, Union[int, str]]) -> str:
    major = matches['MAJOR']
    minor = matches['MINOR']
    patch = matches['PATCH']

    # Convert major and minor to hex
    major_hex = f"{major:02X}"
    minor_hex = f"{minor:02X}"

    # Process patch
    if '.' in patch:
        parts = patch.split('.')
        level = parts[0]
        serial = parts[1]
        level_hex = f"{level.upper():1X}"
        serial_hex = f"{serial:1X}"
    else:
        level_hex = f"{patch.upper():1X}"
        serial_hex = "00"

    # Combine all parts
    version_hex = f"0x{major_hex}{minor_hex}{level_hex}{serial_hex}"

    return version_hex