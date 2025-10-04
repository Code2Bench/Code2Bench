from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def extract_duration_from_data(movie_data):
    """Extract duration in seconds from movie data"""
    duration_secs = None

    # Try to extract duration from various possible fields
    if movie_data.get('duration_secs'):
        duration_secs = int(movie_data.get('duration_secs'))
    elif movie_data.get('duration'):
        # Handle duration that might be in different formats
        duration_str = str(movie_data.get('duration'))
        if duration_str.isdigit():
            duration_secs = int(duration_str) * 60  # Assume minutes if just a number
        else:
            # Try to parse time format like "01:30:00"
            try:
                time_parts = duration_str.split(':')
                if len(time_parts) == 3:
                    hours, minutes, seconds = map(int, time_parts)
                    duration_secs = (hours * 3600) + (minutes * 60) + seconds
                elif len(time_parts) == 2:
                    minutes, seconds = map(int, time_parts)
                    duration_secs = minutes * 60 + seconds
            except (ValueError, AttributeError):
                pass

    return duration_secs

# Strategy for generating movie data
def movie_data_strategy():
    return st.fixed_dictionaries({
        'duration_secs': st.one_of([st.none(), st.integers(min_value=0, max_value=86400)]),
        'duration': st.one_of([
            st.none(),
            st.integers(min_value=0, max_value=1440),
            st.text(st.characters(whitelist_categories=('Nd', 'P'), min_codepoint=48, max_codepoint=58), min_size=1, max_size=8),
            st.tuples(st.integers(min_value=0, max_value=23), st.integers(min_value=0, max_value=59), st.integers(min_value=0, max_value=59)).map(lambda x: f"{x[0]:02}:{x[1]:02}:{x[2]:02}"),
            st.tuples(st.integers(min_value=0, max_value=59), st.integers(min_value=0, max_value=59)).map(lambda x: f"{x[0]:02}:{x[1]:02}")
        ])
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(movie_data=movie_data_strategy())
@example(movie_data={'duration_secs': 3600})
@example(movie_data={'duration': '120'})
@example(movie_data={'duration': '01:30:00'})
@example(movie_data={'duration': '30:00'})
@example(movie_data={'duration': 'invalid'})
@example(movie_data={'duration': None})
@example(movie_data={'duration_secs': None})
def test_extract_duration_from_data(movie_data):
    global stop_collecting
    if stop_collecting:
        return
    
    movie_data_copy = copy.deepcopy(movie_data)
    try:
        expected = extract_duration_from_data(movie_data_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if 'duration_secs' in movie_data or 'duration' in movie_data:
        generated_cases.append({
            "Inputs": {"movie_data": movie_data},
            "Expected": expected
        })
        if len(generated_cases) >= 500:
            stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)