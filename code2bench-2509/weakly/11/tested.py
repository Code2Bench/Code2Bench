from typing import List
import statistics

def calculate_algotune_score(speedups: List[float]) -> float:
    valid_speedups = [s for s in speedups if s is not None and s > 0]
    if not valid_speedups:
        return 0.0
    return statistics.harmonic_mean(valid_speedups)