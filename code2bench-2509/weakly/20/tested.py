from math import ceil

def get_resize_factor(original_shape: tuple[int, int], pixels_range: tuple[int, int], shape_multiplier: int = 14) -> tuple[float, tuple[int, int]]:
    original_height, original_width = original_shape
    min_pixels, max_pixels = pixels_range
    
    # Calculate the target pixel count within the range
    target_pixels = (min_pixels + max_pixels) // 2
    
    # Calculate the resize factor based on the target pixels
    resize_factor = target_pixels / original_height
    
    # Calculate new dimensions
    new_height = round(original_height * resize_factor)
    new_width = round(original_width * resize_factor)
    
    # Adjust new dimensions to be multiples of shape_multiplier
    new_height = ((new_height + shape_multiplier - 1) // shape_multiplier) * shape_multiplier
    new_width = ((new_width + shape_multiplier - 1) // shape_multiplier) * shape_multiplier
    
    return resize_factor, (new_height, new_width)