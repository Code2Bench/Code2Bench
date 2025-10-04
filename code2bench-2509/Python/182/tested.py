from typing import List, Tuple, Optional

def get_displacement(before: List[List[int]], after: List[List[int]]) -> Optional[Tuple[int, int]]:
    if len(before) != len(after):
        return None
    
    if not before:
        return None
    
    # Get the displacement for the first piece
    delta_row = after[0][0] - before[0][0]
    delta_col = after[0][1] - before[0][1]
    
    # Check if all pieces have the same displacement
    for i in range(1, len(before)):
        if after[i][0] - before[i][0] != delta_row or after[i][1] - before[i][1] != delta_col:
            return None
    
    return (delta_row, delta_col)