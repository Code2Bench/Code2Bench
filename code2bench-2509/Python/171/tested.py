from typing import List

def git_submodules_under_thirdparty(ls_stage_lines: List[str]) -> List[str]:
    submodule_names = set()
    for line in ls_stage_lines:
        if line.startswith('160000'):
            path = line.split()[1]
            if path.startswith('thirdparty/'):
                submodule_name = path.split('/')[1]
                submodule_names.add(submodule_name)
    return sorted(submodule_names)