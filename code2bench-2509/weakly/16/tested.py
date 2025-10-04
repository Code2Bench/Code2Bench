from collections import defaultdict
import re

def extract_error_files(output: str) -> defaultdict[str, list[str]]:
    error_dict = defaultdict(list)
    lines = output.splitlines()
    pattern = r'error: (.+?)\s*:\s*(.+)'
    for line in lines:
        match = re.search(pattern, line)
        if match:
            file_path = match.group(1)
            error_message = match.group(2)
            error_dict[file_path].append(error_message)
    return error_dict