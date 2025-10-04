

def CalculateAlpha(
    distances,
    fade_end=10,
    fade_start=30,
    max_fade_start=150,
    max_fade_end=170,
    verbose=False,
):
    if not distances:
        return 0

    # Calculate the average distance
    avg_distance = sum(distances) / len(distances)

    # Determine the alpha value based on the average distance
    if avg_distance < fade_end:
        return 0
    elif fade_end <= avg_distance < fade_start:
        return 255 * (avg_distance - fade_end) / (fade_start - fade_end)
    elif fade_start <= avg_distance < max_fade_start:
        return 255
    elif max_fade_start <= avg_distance < max_fade_end:
        return 255 * (max_fade_end - avg_distance) / (max_fade_end - max_fade_start)
    else:
        return 0