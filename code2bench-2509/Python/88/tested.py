from typing import List, Tuple

def merge_overlapping_spans(spans: List[Tuple[int, int, int, int]]) -> List[Tuple[int, int, int, int]]:
    if not spans:
        return []

    # Sort spans by their starting x-coordinate
    spans.sort(key=lambda span: span[0])

    merged = [spans[0]]

    for current in spans[1:]:
        last = merged[-1]
        # Check if current span overlaps with the last merged span
        if current[0] <= last[2]:
            # Merge the spans
            new_span = (
                min(last[0], current[0]),
                min(last[1], current[1]),
                max(last[2], current[2]),
                max(last[3], current[3])
            )
            merged[-1] = new_span
        else:
            merged.append(current)

    return merged