from typing import List

def find_import_section_end(lines: List[str]) -> int:
    import_section_end = 0
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from ') or line.startswith('sys.path.') or line.startswith('load_dotenv('):
            import_section_end = i
        elif line.strip() == '':
            continue
        else:
            break
    return import_section_end