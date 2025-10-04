from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import unicodedata
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
def detect_unicode_homographs(text: str) -> tuple[bool, str]:
    """
    Detect and normalize Unicode homograph characters used to bypass security checks.
    Returns (has_homographs, normalized_text)
    """
    # Common homograph replacements
    homograph_map = {
        # Cyrillic to Latin mappings
        '\u0430': 'a',  # Cyrillic а
        '\u0435': 'e',  # Cyrillic е  
        '\u043e': 'o',  # Cyrillic о
        '\u0440': 'p',  # Cyrillic р
        '\u0441': 'c',  # Cyrillic с
        '\u0443': 'y',  # Cyrillic у
        '\u0445': 'x',  # Cyrillic х
        '\u0410': 'A',  # Cyrillic А
        '\u0415': 'E',  # Cyrillic Е
        '\u041e': 'O',  # Cyrillic О
        '\u0420': 'P',  # Cyrillic Р
        '\u0421': 'C',  # Cyrillic С
        '\u0425': 'X',  # Cyrillic Х
        # Greek to Latin mappings
        '\u03b1': 'a',  # Greek α
        '\u03bf': 'o',  # Greek ο
        '\u03c1': 'p',  # Greek ρ
        '\u03c5': 'u',  # Greek υ
        '\u03c7': 'x',  # Greek χ
        '\u0391': 'A',  # Greek Α
        '\u039f': 'O',  # Greek Ο
        '\u03a1': 'P',  # Greek Ρ
    }

    # Check if text contains any homographs
    has_homographs = any(char in text for char in homograph_map)

    # Normalize the text
    normalized = text
    for homograph, replacement in homograph_map.items():
        normalized = normalized.replace(homograph, replacement)

    # Also normalize using Unicode NFKD
    normalized = unicodedata.normalize('NFKD', normalized)

    return (has_homographs, normalized)

# Strategy for generating text with potential homographs
def text_strategy():
    # Generate homograph characters
    homographs = st.sampled_from([
        '\u0430', '\u0435', '\u043e', '\u0440', '\u0441', '\u0443', '\u0445',
        '\u0410', '\u0415', '\u041e', '\u0420', '\u0421', '\u0425',
        '\u03b1', '\u03bf', '\u03c1', '\u03c5', '\u03c7',
        '\u0391', '\u039f', '\u03a1'
    ])
    
    # Generate regular ASCII characters
    ascii_chars = st.characters(min_codepoint=32, max_codepoint=126)
    
    # Mix homographs with ASCII characters
    return st.lists(
        st.one_of(homographs, ascii_chars),
        min_size=0, max_size=20
    ).map(lambda x: ''.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="")
@example(text="hello")
@example(text="\u0430\u0435\u043e")  # Cyrillic аео
@example(text="\u03b1\u03bf\u03c1")  # Greek αορ
@example(text="mix\u0430\u03b1ed")  # Mixed ASCII and homographs
def test_detect_unicode_homographs(text: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    text_copy = copy.deepcopy(text)

    # Call func0 to verify input validity
    try:
        has_homographs, normalized = detect_unicode_homographs(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "text": text_copy
        }
    })

    # Stop collecting after 500 cases
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)