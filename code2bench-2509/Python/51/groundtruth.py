

def generate_crop_size_list(base_size=256, patch_size=32, max_ratio=4.0):
    """generate crop size list

    Args:
        base_size (int, optional): the base size for generate bucket. Defaults to 256.
        patch_size (int, optional): the stride to generate bucket. Defaults to 32.
        max_ratio (float, optional): th max ratio for h or w based on base_size . Defaults to 4.0.

    Returns:
        list: generate crop size list
    """
    num_patches = round((base_size / patch_size) ** 2)
    assert max_ratio >= 1.0
    crop_size_list = []
    wp, hp = num_patches, 1
    while wp > 0:
        if max(wp, hp) / min(wp, hp) <= max_ratio:
            crop_size_list.append((wp * patch_size, hp * patch_size))
        if (hp + 1) * wp <= num_patches:
            hp += 1
        else:
            wp -= 1
    return crop_size_list