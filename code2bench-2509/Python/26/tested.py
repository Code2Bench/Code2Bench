from typing import List, Dict

def extract_locs_for_files(locs: List[str], file_names: List[str], keep_old_order: bool = False) -> Dict[str, List[str]]:
    result = {}
    for loc in locs:
        parts = loc.split('\n')
        for part in parts:
            if part.startswith('file'):
                file_name = part.split('file')[1].strip()
                if file_name in file_names:
                    result[file_name].append(part)
    return result if keep_old_order else dict(sorted(result.items()))