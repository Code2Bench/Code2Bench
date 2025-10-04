import statistics
from typing import List, Dict

def calculate_stats(times: List[float]) -> Dict[str, float]:
    if not times:
        return {'mean': 0.0, 'median': 0.0, 'std_dev': 0.0, 'min': 0.0, 'max': 0.0}
    
    mean = statistics.mean(times)
    median = statistics.median(times)
    min_val = min(times)
    max_val = max(times)
    
    if len(times) < 2:
        std_dev = 0.0
    else:
        std_dev = statistics.stdev(times)
    
    return {'mean': mean, 'median': median, 'std_dev': std_dev, 'min': min_val, 'max': max_val}