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
def replace_symbols(text, lang="en"):
    """Replace symbols based on the lenguage tag.

    Args:
      text:
       Input text.
      lang:
        Lenguage identifier. ex: "en", "fr", "pt", "ca".

    Returns:
      The modified text
      example:
        input args:
            text: "si l'avi cau, diguem-ho"
            lang: "ca"
        Output:
            text: "si lavi cau, diguemho"
    """
    text = text.replace(";", ",")
    text = text.replace("-", " ") if lang != "ca" else text.replace("-", "")
    text = text.replace(":", ",")
    if lang == "en":
        text = text.replace("&", " and ")
    elif lang == "fr":
        text = text.replace("&", " et ")
    elif lang == "pt":
        text = text.replace("&", " e ")
    elif lang == "ca":
        text = text.replace("&", " i ")
        text = text.replace("'", "")
    elif lang == "es":
        text = text.replace("&", "y")
        text = text.replace("'", "")
    return text

# Strategy for generating text with symbols
def text_with_symbols():
    return st.text(
        st.characters(
            whitelist_categories=('L', 'N', 'P', 'S', 'Z'),
            whitelist_characters=";&-:'"
        ),
        min_size=1,
        max_size=50
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    text=text_with_symbols(),
    lang=st.sampled_from(["en", "fr", "pt", "ca", "es"])
)
@example(text="si l'avi cau, diguem-ho", lang="ca")
@example(text="bread & butter", lang="en")
@example(text="pain & beurre", lang="fr")
@example(text="pão & manteiga", lang="pt")
@example(text="pan & mantega", lang="ca")
@example(text="pan & mantequilla", lang="es")
@example(text="example;text", lang="en")
@example(text="example-text", lang="en")
@example(text="example:text", lang="en")
@example(text="example-text", lang="ca")
def test_replace_symbols(text, lang):
    global stop_collecting
    if stop_collecting:
        return
    
    text_copy = copy.deepcopy(text)
    try:
        expected = replace_symbols(text_copy, lang)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(symbol in text for symbol in ";&-:'"):
        generated_cases.append({
            "Inputs": {"text": text, "lang": lang},
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