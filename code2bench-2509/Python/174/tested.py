def fit_res(w: int, h: int, max_w: int, max_h: int) -> tuple[int, int]:
    # Check if dimensions are already within limits
    if w <= max_w and h <= max_h:
        return (w, h)
    
    # Calculate the aspect ratio
    aspect_ratio = w / h
    
    # Adjust dimensions to fit within max limits while maintaining aspect ratio
    new_w = int(max_w * aspect_ratio)
    new_h = int(max_h * aspect_ratio)
    
    # Ensure dimensions are even numbers
    new_w = new_w - (new_w % 2)
    new_h = new_h - (new_h % 2)
    
    return (new_w, new_h)