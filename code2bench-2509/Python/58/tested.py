from typing import List

def insert_lines_into_block(block_bbox: List[float], line_height: float, page_w: float, page_h: float) -> List[List[float]]:
    x0, y0, x1, y1 = block_bbox
    
    # Calculate block dimensions
    block_width = x1 - x0
    block_height = y1 - y0
    
    # Rule 1: If block height is less than twice the line height, return as single line
    if block_height < 2 * line_height:
        return [[x0, y0, x1, y1]]
    
    # Rule 2: If block height > 25% of page height and block width between 25% and 50% of page width
    if (block_height > 0.25 * page_h) and (block_width >= 0.25 * page_w and block_width <= 0.5 * page_w):
        lines = int((block_height / line_height) + 1)
        return [list(block_bbox[i:i+2]) for i in range(0, len(block_bbox), lines)]
    
    # Rule 3: If block width > 40% of page width, return as 3 lines
    if block_width > 0.4 * page_w:
        return [[x0, y0, x1, y1], [x0, y0 + line_height, x1, y1], [x0, y0 + 2 * line_height, x1, y1]]
    
    # Rule 4: If block width between 25% and 40% of page width, calculate lines based on block height and line height
    if 0.25 * page_w <= block_width <= 0.4 * page_w:
        lines = int((block_height / line_height) + 1)
        return [list(block_bbox[i:i+2]) for i in range(0, len(block_bbox), lines)]
    
    # Rule 5: If block width < 25% of page width and block height to width ratio > 1.2, return as single line
    if block_width < 0.25 * page_w and (block_height / block_width) > 1.2:
        return [[x0, y0, x1, y1]]
    
    # Default case: return as 2 lines
    return [[x0, y0, x1, y1], [x0, y0 + line_height, x1, y1]]