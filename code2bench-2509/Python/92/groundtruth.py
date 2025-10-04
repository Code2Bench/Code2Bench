

def format_index_ranges(indices):
    """Format a list of indices into range strings like '0-1,3-6'."""
    if not indices:
        return ""

    ranges = []
    start = end = indices[0]

    for i in range(1, len(indices)):
        if indices[i] == end + 1:
            end = indices[i]
        else:
            ranges.append(str(start) if start == end else f"{start}-{end}")
            start = end = indices[i]

    # Add the last range
    ranges.append(str(start) if start == end else f"{start}-{end}")
    return ",".join(ranges)