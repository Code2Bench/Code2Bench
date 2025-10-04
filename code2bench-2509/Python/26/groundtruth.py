

def extract_locs_for_files(locs, file_names, keep_old_order=False):
    if keep_old_order:
        results = {fn: [] for fn in file_names}
    else:
        results = {}  # dict is insertion ordered
    current_file_name = None
    for loc in locs:
        for line in loc.splitlines():
            if line.strip().endswith('.py'):
                current_file_name = line.strip()
            elif line.strip() and any(
                line.startswith(w) for w in ['line:', 'function:', 'class:', 'variable:']
            ):
                if current_file_name in file_names:
                    if current_file_name not in results:
                        results[current_file_name] = []
                    results[current_file_name].append(line)
                else:
                    pass

    for file_name in file_names:
        if file_name not in results:  # guard for new order case
            results[file_name] = []

    return {fn: ['\n'.join(results[fn])] for fn in results.keys()}