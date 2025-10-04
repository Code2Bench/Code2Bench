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
def normalize_unicode_homographs(text: str) -> str:
    homograph_map = {
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
        '\u03b1': 'a',  # Greek α
        '\u03bf': 'o',  # Greek ο
        '\u03c1': 'p',  # Greek ρ
        '\u03c5': 'u',  # Greek υ
        '\u03c7': 'x',  # Greek χ
        '\u0391': 'A',  # Greek Α
        '\u039f': 'O',  # Greek Ο
        '\u03a1': 'P',  # Greek Ρ
        '\u2010': '-',  # Hyphen
        '\u2011': '-',  # Non-breaking hyphen
        '\u2212': '-',  # Minus sign
        '\uff0d': '-',  # Fullwidth hyphen-minus
    }
    normalized = text
    for homograph, replacement in homograph_map.items():
        normalized = normalized.replace(homograph, replacement)
    normalized = unicodedata.normalize('NFKD', normalized)
    return normalized

# Strategy for generating text with potential homographs
def text_strategy():
    # Generate homographs from the map
    homograph_map = {
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
        '\u03b1': 'a',  # Greek α
        '\u03bf': 'o',  # Greek ο
        '\u03c1': 'p',  # Greek ρ
        '\u03c5': 'u',  # Greek υ
        '\u03c7': 'x',  # Greek χ
        '\u0391': 'A',  # Greek Α
        '\u039f': 'O',  # Greek Ο
        '\u03a1': 'P',  # Greek Ρ
        '\u2010': '-',  # Hyphen
        '\u2011': '-',  # Non-breaking hyphen
        '\u2212': '-',  # Minus sign
        '\uff0d': '-',  # Fullwidth hyphen-minus
    }
    homographs = st.sampled_from(list(homograph_map.keys()))
    # Generate random text
    random_text = st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)
    # Combine homographs and random text
    return st.lists(
        st.one_of(homographs, random_text),
        min_size=0, max_size=10
    ).map(lambda x: ''.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="")
@example(text="с")  # Cyrillic с
@example(text="а")  # Cyrillic а
@example(text="α")  # Greek α
@example(text="\u2010")  # Hyphen
@example(text="\u2212")  # Minus sign
@example(text="\uff0d")  # Fullwidth hyphen-minus
@example(text="с\u0430α\u2010")  # Mixed homographs
def test_normalize_unicode_homographs(text: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    text_copy = copy.deepcopy(text)

    # Call func0 to verify input validity
    try:
        expected = normalize_unicode_homographs(text_copy)
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