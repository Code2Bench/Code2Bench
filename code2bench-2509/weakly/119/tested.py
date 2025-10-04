import statistics

def _timeseries_stats(ts: list) -> str:
    if not ts:
        return "No data points"
    
    count = len(ts)
    maximum = max(ts)
    minimum = min(ts)
    mean = statistics.mean(ts)
    median = statistics.median(ts)
    
    return f"""**Count:** {count}
**Maximum:** {maximum}
**Minimum:** {minimum}
**Mean:** {mean}
**Median:** {median}"""