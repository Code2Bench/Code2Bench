
from collections import defaultdict
import re

def get_changed_lines_from_file(diff_txt_path):
    """Parse diff.txt to get changed lines per file"""
    file_changes = defaultdict(set)
    current_file = None

    with open(diff_txt_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("+++ b/"):
                current_file = line[6:].strip()
            elif line.startswith("@@"):
                match = re.search(r"\+(\d+)(?:,(\d+))?", line)
                if match and current_file:
                    start_line = int(match.group(1))
                    line_count = int(match.group(2) or "1")
                    for i in range(start_line, start_line + line_count):
                        file_changes[current_file].add(i)
    return file_changes