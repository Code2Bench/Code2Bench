

def git_submodules_under_thirdparty(ls_stage_lines: list[str]) -> list[str]:
    """
    Use `git ls-files --stage` (mode 160000) and keep only those under thirdparty/.
    """
    names = []
    for line in ls_stage_lines:
        parts = line.split()
        if len(parts) >= 4 and parts[0] == "160000":
            path = parts[3]  # repo-relative
            if path.startswith("thirdparty/"):
                rel = path[len("thirdparty/") :]
                first = rel.split("/", 1)[0]
                if first:
                    names.append(first)
    return sorted(set(names))