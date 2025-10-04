from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import codecs
import json
import os
import atexit
import copy
from typing import Any

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def _clean_text_value(value: Any) -> Any:
    """Fix common text encoding issues and decode escaped sequences.

    - Fix UTF-8 displayed as Windows-1252/latin-1 (e.g., â -> ’)
    - Decode backslash-escaped unicode sequences when present
    - Leave non-strings unchanged
    """
    if not isinstance(value, str):
        return value

    text = value

    # Attempt to fix mojibake: bytes intended as UTF-8 shown as latin-1
    # Trigger only if typical mojibake markers present
    if any(mark in text for mark in ("â€", "Ã", "Â")):
        try:
            text = text.encode("latin-1", errors="ignore").decode(
                "utf-8", errors="ignore"
            )
        except Exception:
            pass

    # Decode literal escape sequences like \u2019 -> ’ if present
    if "\\u" in text or "\\x" in text:
        try:
            text = codecs.decode(text.encode("utf-8"), "unicode_escape")
        except Exception:
            pass

    return text

# Strategies for generating inputs
def value_strategy():
    return st.one_of(
        st.text(
            alphabet=st.characters(
                whitelist_categories=("L", "N", "P", "S", "Z"),
                whitelist_characters="â€ÃÂ\\ux",
            ),
            min_size=0,
            max_size=50,
        ),
        st.integers(min_value=-100, max_value=100),
        st.floats(allow_nan=False, allow_infinity=False),
        st.booleans(),
        st.none(),
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(value=value_strategy())
@example(value="â€")
@example(value="Ã")
@example(value="Â")
@example(value="\\u2019")
@example(value="\\x41")
@example(value=42)
@example(value=3.14)
@example(value=True)
@example(value=None)
def test_clean_text_value(value: Any):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    value_copy = copy.deepcopy(value)

    # Call func0 to verify input validity
    try:
        expected = _clean_text_value(value_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "value": value_copy if not isinstance(value_copy, str) else value_copy
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