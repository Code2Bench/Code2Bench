import math

def deep_compare(a, b, tolerance=1e-6):
    if isinstance(a, float) and isinstance(b, float):
        # Compare floats with a tolerance
        return math.isclose(a, b, abs_tol=tolerance)
    elif isinstance(a, dict) and isinstance(b, dict):
        # Compare dictionaries recursively
        return all(
            k in b and deep_compare(a[k], b[k], tolerance)
            for k in a
        ) and len(a) == len(b)
    elif isinstance(a, list) and isinstance(b, list):
        # Compare lists recursively
        return len(a) == len(b) and all(
            deep_compare(ai, bi, tolerance)
            for ai, bi in zip(a, b)
        )
    else:
        # Use strict equality for other types
        return a == b