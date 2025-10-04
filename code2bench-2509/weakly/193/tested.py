from typing import Iterable, Tuple
import scipy.stats
import numpy as np

def mean_confidence_interval(data: Iterable[float], confidence: float = 0.95) -> Tuple[float, float, float]:
    data = np.array(data)
    if len(data) == 0:
        raise ValueError("Input data cannot be empty.")
    mean = np.mean(data)
    std_error = np.std(data, ddof=1) / np.sqrt(len(data))
    half_interval = scipy.stats.t.ppf((1 + confidence) / 2, len(data) - 1) * std_error
    lower_bound = mean - half_interval
    upper_bound = mean + half_interval
    return (mean, lower_bound, upper_bound)