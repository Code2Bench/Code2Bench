
import statistics

def calculate_stats(times: list[float]) -> dict[str, float]:
    """Calculate timing statistics.

    Args:
        times: List of execution times.

    Returns:
        dict[str, float]: Dictionary with statistical measures.

    Examples:
        >>> times = [1.0, 2.0, 3.0, 4.0, 5.0]
        >>> stats = calculate_stats(times)
        >>> stats['mean']
        3.0
        >>> stats['median']
        3.0
    """
    if not times:
        return {"mean": 0, "median": 0, "std_dev": 0, "min": 0, "max": 0}

    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
        "min": min(times),
        "max": max(times),
    }