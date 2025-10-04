

def parse_interval(interval):
	"""
	Parse interval string or integer into seconds.

	Args:
	    interval: Can be:
	        - Integer: seconds (e.g., 3600)
	        - String: number + unit (e.g., "1h", "30m", "7d")

	Returns:
	    int: Total seconds

	Examples:
	    parse_interval(3600) -> 3600
	    parse_interval("1h") -> 3600
	    parse_interval("30m") -> 1800
	    parse_interval("7d") -> 604800
	"""
	if interval is None:
		return None

	# If already an integer, return as-is (assuming seconds)
	if isinstance(interval, int):
		return interval

	# Parse string format
	interval = str(interval).strip().lower()

	# Extract number and unit
	if interval[-1].isdigit():
		# No unit specified, assume seconds
		return int(interval)

	unit = interval[-1]
	try:
		number = int(interval[:-1])
	except ValueError:
		raise ValueError(f"Invalid interval format: {interval}")

	# Convert to seconds
	multipliers = {
		"s": 1,  # seconds
		"m": 60,  # minutes
		"h": 3600,  # hours
		"d": 86400,  # days
		"w": 604800,  # weeks
		"y": 31536000,  # years
	}

	if unit not in multipliers:
		raise ValueError(f"Invalid time unit '{unit}'. Use: s, m, h, d, w, y")

	return number * multipliers[unit]