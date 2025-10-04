from typing import Optional, Tuple

def validate_input_media(width: int, height: int, with_frame_conditioning: bool, num_frames_in: Optional[int] = None) -> Tuple[bool, Optional[str]]:
    # Check if width and height are divisible by 8
    if width % 8 != 0 or height % 8 != 0:
        return False, "Width and height must be divisible by 8."

    # Check if num_frames_in is provided and divisible by 16
    if num_frames_in is not None and num_frames_in % 16 != 0:
        return False, "Number of frames must be divisible by 16 if provided."

    # Check frame conditioning conditions
    if with_frame_conditioning:
        if (width * height) % 8192 != 0:
            return False, "Product of width and height must be divisible by 8192 when frame conditioning is enabled."
    else:
        if num_frames_in is not None and num_frames_in % 32 != 0:
            return False, "Number of frames must be divisible by 32 when frame conditioning is disabled."

    return True, None