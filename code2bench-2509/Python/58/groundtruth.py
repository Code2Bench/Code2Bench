

def insert_lines_into_block(block_bbox, line_height, page_w, page_h):

    x0, y0, x1, y1 = block_bbox

    block_height = y1 - y0
    block_weight = x1 - x0


    if line_height * 2 < block_height:
        if (
            block_height > page_h * 0.25 and page_w * 0.5 > block_weight > page_w * 0.25
        ):
            lines = int(block_height / line_height) + 1
        else:

            if block_weight > page_w * 0.4:
                lines = 3
                line_height = (y1 - y0) / lines
            elif block_weight > page_w * 0.25:
                lines = int(block_height / line_height) + 1
            else:
                if block_height / block_weight > 1.2:
                    return [[x0, y0, x1, y1]]
                else:
                    lines = 2
                    line_height = (y1 - y0) / lines


        current_y = y0


        lines_positions = []

        for i in range(lines):
            lines_positions.append([x0, current_y, x1, current_y + line_height])
            current_y += line_height
        return lines_positions

    else:
        return [[x0, y0, x1, y1]]