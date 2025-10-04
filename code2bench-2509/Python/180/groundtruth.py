

def _parse_dos_filename(line):
    """Parse DOS 8.3 format filename from mdir output"""
    parts = line.split()
    if len(parts) < 1:
        return None, False

    is_directory = "<DIR>" in line.upper()
    if is_directory:
        return parts[0], True

    # For files: "FILENAME EXT SIZE DATE TIME"
    if (
        len(parts) >= 2
        and not parts[1].isdigit()
        and parts[1] not in ["bytes", "files"]
    ):
        return f"{parts[0]}.{parts[1]}", False
    return parts[0], False