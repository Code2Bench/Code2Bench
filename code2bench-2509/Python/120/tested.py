def get_optimal_patched_size_with_sp(patched_h: int, patched_w: int, sp_size: int) -> tuple[int, int]:
    assert sp_size > 0, "sp_size must be a positive integer"
    assert (sp_size & (sp_size - 1)) == 0, "sp_size must be a power of 2"

    # Function to check if a number is a power of two
    def is_power_of_two(n: int) -> bool:
        return n != 0 and (n & (n - 1)) == 0

    # Calculate the optimal height and width
    optimal_h = patched_h
    optimal_w = patched_w

    # Reduce the larger dimension when both are odd
    if patched_h % 2 == 1 and patched_w % 2 == 1:
        optimal_h = (patched_h // 2) * 2 + 1
        optimal_w = (patched_w // 2) * 2 + 1

    # Reduce the dimension based on sp_size
    while optimal_h > sp_size or optimal_w > sp_size:
        if optimal_h > optimal_w:
            optimal_h -= 1
        else:
            optimal_w -= 1

    return (optimal_h, optimal_w)