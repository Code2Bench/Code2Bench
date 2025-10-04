from typing import List, Dict

def filter_contained_bboxes(bboxes: List[Dict[str, int]]) -> List[Dict[str, int]]:
    removed = set()
    for i, box in enumerate(bboxes):
        for j, other_box in enumerate(bboxes):
            if i == j:
                continue
            if is_contained(box, other_box):
                removed.add(i)
                break
    return [box for idx, box in enumerate(bboxes) if idx not in removed]

def is_contained(box1: Dict[str, int], box2: Dict[str, int]) -> bool:
    # Check if box1 is contained within box2
    if box1['column_min'] >= box2['column_min'] and \
       box1['column_max'] <= box2['column_max'] and \
       box1['row_min'] >= box2['row_min'] and \
       box1['row_max'] <= box2['row_max']:
        return True
    return False