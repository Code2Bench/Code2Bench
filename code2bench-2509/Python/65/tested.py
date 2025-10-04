from typing import List, Tuple

def parse_evolve_blocks(code: str) -> List[Tuple[int, int, str]]:
    blocks = []
    lines = code.splitlines()
    line_num = 0
    
    for line in lines:
        line_num += 1
        if '# EVOLVE-BLOCK-START' in line:
            start_line = line_num
            # Find the corresponding end line
            end_line = line_num
            while end_line < len(lines) and '#' not in lines[end_line]:
                end_line += 1
            if end_line < len(lines) and lines[end_line].startswith('# EVOLVE-BLOCK-END'):
                end_line += 1
            blocks.append((start_line, end_line - 1, '\n'.join(lines[start_line - 1:end_line])))
    
    return blocks