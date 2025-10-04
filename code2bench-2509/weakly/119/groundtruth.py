
import statistics

def _timeseries_stats(ts):
    """Calculate and format summary statistics for a time series.

    Args:
        ts (list): List of numeric values representing a time series

    Returns:
        str: Markdown formatted string containing summary statistics
    """
    if len(ts) == 0:
        return "No data points"

    count = len(ts)
    max_val = max(ts)
    min_val = min(ts)
    mean_val = sum(ts) / count if count > 0 else float("nan")
    median_val = statistics.median(ts)

    markdown_summary = f"""
Time Series Statistics
- Number of Data Points: {count}
- Maximum Value: {max_val}
- Minimum Value: {min_val}
- Mean Value: {mean_val:.2f}
- Median Value: {median_val}
"""
    return markdown_summary