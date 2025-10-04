import statistics
from typing import List

def calculate_fcf_volatility(fcf_history: List[float]) -> float:
    positive_fcf = [x for x in fcf_history if x > 0]
    if len(positive_fcf) < 3:
        return 0.5
    if sum(positive_fcf) / len(positive_fcf) <= 0:
        return 0.8
    std_dev = statistics.stdev(positive_fcf)
    mean = statistics.mean(positive_fcf)
    volatility = std_dev / mean
    return min(volatility, 1.0)