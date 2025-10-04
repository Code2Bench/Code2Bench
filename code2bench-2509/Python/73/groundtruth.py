

def filter_contained_bboxes(bboxes):
    """
    Filters a list of bounding boxes by removing any box that is fully contained within another.

    Args:
        bboxes (list of dict): A list of bounding boxes. Each bbox is expected to be a
                               dictionary with 'column_min', 'row_min', 'column_max', 'row_max'.

    Returns:
        list of dict: A new list of bounding boxes with the smaller, contained boxes removed.
    """
    # A set to store the indices of bboxes to be removed.
    # Using a set avoids duplicates and provides fast membership checking.
    indices_to_remove = set()

    # Compare every bbox with every other bbox.
    for i in range(len(bboxes)):
        for j in range(len(bboxes)):
            # Don't compare a bbox to itself.
            if i == j:
                continue

            bbox_a = bboxes[i]
            bbox_b = bboxes[j]

            # Check if bbox_a contains bbox_b
            # This is true if bbox_b's corners are all within bbox_a's corners.
            # Note: If they are identical, one will contain the other.
            is_contained = (bbox_a['column_min'] <= bbox_b['column_min'] and
                            bbox_a['row_min'] <= bbox_b['row_min'] and
                            bbox_a['column_max'] >= bbox_b['column_max'] and
                            bbox_a['row_max'] >= bbox_b['row_max'])

            if is_contained:
                # If bbox_a and bbox_b are identical, this logic will flag one for removal
                # based on its index, which is acceptable for de-duplication.
                # If bbox_a is strictly larger, bbox_b is the smaller one and should be removed.
                indices_to_remove.add(j)

    # Create a new list containing only the bboxes that were not marked for removal.
    filtered_bboxes = [bbox for i, bbox in enumerate(bboxes) if i not in indices_to_remove]

    return filtered_bboxes