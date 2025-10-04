import numpy as np

def nms(boxes: np.ndarray, scores: np.ndarray, nms_thr: float) -> list[int]:
    if boxes.shape[0] == 0:
        return []
    
    indices = np.argsort(scores)[::-1]
    keep = []
    while len(indices) > 0:
        best = indices[0]
        keep.append(best)
        ious = calculate_iou(boxes[best], boxes[indices[1:]])
        indices = indices[(ious <= nms_thr)]
    return keep

def calculate_iou(box1, boxes):
    x1, y1, x2, y2 = box1
    areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    inter_x1 = np.maximum(x1, boxes[:, 0])
    inter_y1 = np.maximum(y1, boxes[:, 1])
    inter_x2 = np.minimum(x2, boxes[:, 2])
    inter_y2 = np.minimum(y2, boxes[:, 3])
    inter_area = np.maximum(0, inter_x2 - inter_x1) * np.maximum(0, inter_y2 - inter_y1)
    ious = inter_area / (areas + 1e-16)
    return ious