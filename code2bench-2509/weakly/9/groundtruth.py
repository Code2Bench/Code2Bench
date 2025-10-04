
import difflib

def closest_name(input_str, options):
    input_str = input_str.lower()

    closest_match = difflib.get_close_matches(
        input_str, list(options.keys()), n=1, cutoff=0.5
    )
    assert isinstance(closest_match, list) and len(closest_match) > 0, (
        f"The value [{input_str}] is not valid!"
    )
    result = closest_match[0]

    if result != input_str:
        print(f"Automatically corrected [{input_str}] -> [{result}].")

    return result