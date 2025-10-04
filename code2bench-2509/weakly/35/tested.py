from collections import defaultdict
import re

def get_changed_lines_from_file(diff_txt_path: str) -> defaultdict:
    changed_lines = defaultdict(set)
    with open(diff_txt_path, 'r') as file:
        lines = file.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('diff --git'):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('---'):
                i += 1
            if i < len(lines):
                file_name = lines[i].strip().split(' ')[-1]
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('@@'):
                    i += 1
                if i < len(lines):
                    match = re.search(r'@@ -(\\d+)(,\\d+)? \\+(\\d+)(,\\d+)? @@', lines[i])
                    if match:
                        start_line = int(match.group(3))
                        num_lines = int(match.group(4)) if match.group(4) else 1
                        for j in range(num_lines):
                            changed_lines[file_name].add(start_line + j)
                        i += 1
    return changed_lines