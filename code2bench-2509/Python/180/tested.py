from typing import Tuple, Optional

def _parse_dos_filename(line: str) -> Tuple[Optional[str], bool]:
    # Check if the line is empty or contains only whitespace
    if not line.strip():
        return (None, False)
    
    # Split the line into parts
    parts = line.split()
    if len(parts) < 2:
        return (None, False)
    
    # Check for directory entries
    if "<DIR>" in parts[0]:
        filename = parts[1]
        is_directory = True
    else:
        # Try to parse filename and extension
        try:
            # Split the filename and extension by dot
            filename, ext = parts[1].split('.', 1)
        except ValueError:
            # No extension, return filename as is
            filename = parts[1]
            ext = ""
        is_directory = False
    
    # Return the parsed filename and whether it's a directory
    return (filename, is_directory)