import difflib

def closest_name(input_str: str, options: dict) -> str:
    input_str_lower = input_str.lower()
    keys = list(options.keys())
    closest_matches = difflib.get_close_matches(input_str_lower, keys, n=1, cutoff=0.6)
    
    if not closest_matches:
        raise AssertionError("No valid match found for the input string.")
    
    closest_match = closest_matches[0]
    if closest_match != input_str_lower:
        print(f"Did you mean '{closest_match}'?")
    
    return closest_match