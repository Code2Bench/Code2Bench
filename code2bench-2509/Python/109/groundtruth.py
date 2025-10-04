

def validate_input_media(width, height, with_frame_conditioning, num_frames_in=None):
    # inference validation
    # T = num_frames
    # in all cases, the following must be true: T divisible by 16 and H,W by 8. in addition...
    # with image conditioning: H*W must be divisible by 8192
    # without image conditioning: T divisible by 32
    if num_frames_in and not num_frames_in % 16 == 0:
        return False, ("The input video total frame count must be divisible by 16!")

    if height % 8 != 0 or width % 8 != 0:
        return False, (
            f"Height ({height}) and width ({width}) must be " "divisible by 8"
        )

    if with_frame_conditioning:
        if (height * width) % 8192 != 0:
            return False, (
                f"Height * width ({height * width}) must be "
                "divisible by 8192 for frame conditioning"
            )
    else:
        if num_frames_in and not num_frames_in % 32 == 0:
            return False, ("The input video total frame count must be divisible by 32!")