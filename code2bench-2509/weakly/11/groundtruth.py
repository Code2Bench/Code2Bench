from typing import List
import statistics

def calculate_algotune_score(speedups: List[float]) -> float:
    """
    Calculate AlgoTune Score as harmonic mean of speedups.

    Args:
        speedups: List of speedup values

    Returns:
        Harmonic mean of speedups
    """
    if not speedups:
        return 0.0

    # Filter out None and invalid values
    valid_speedups = [s for s in speedups if s is not None and s > 0]

    if not valid_speedups:
        return 0.0

    return statistics.harmonic_mean(valid_speedups)