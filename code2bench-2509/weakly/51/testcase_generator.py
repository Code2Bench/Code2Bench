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
def s2_authors_match(authors: list[str], data: dict) -> bool:
    """Check if the authors in the data match the authors in the paper."""
    AUTHOR_NAME_MIN_LENGTH = 2
    s2_authors_noinit = [
        " ".join([w for w in a["name"].split() if len(w) > AUTHOR_NAME_MIN_LENGTH])
        for a in data["authors"]
    ]
    authors_noinit = [
        " ".join([w for w in a.split() if len(w) > AUTHOR_NAME_MIN_LENGTH])
        for a in authors
    ]
    # Note: we expect the number of authors to be possibly different
    return any(
        starmap(
            lambda x, y: x in y or y in x,
            zip(s2_authors_noinit, authors_noinit, strict=False),
        )
    )

# Strategies for generating inputs
def author_name_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'Z'), min_codepoint=32, max_codepoint=126),
        min_size=1, max_size=20
    )

def authors_strategy():
    return st.lists(author_name_strategy(), min_size=0, max_size=10)

def data_strategy():
    return st.dictionaries(
        keys=st.just("authors"),
        values=st.lists(
            st.dictionaries(
                keys=st.just("name"),
                values=author_name_strategy()
            ),
            min_size=0, max_size=10
        )
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    authors=authors_strategy(),
    data=data_strategy()
)
@example(
    authors=[],
    data={"authors": []}
)
@example(
    authors=["John Doe"],
    data={"authors": [{"name": "John Doe"}]}
)
@example(
    authors=["John Doe"],
    data={"authors": [{"name": "Doe John"}]}
)
@example(
    authors=["John Doe"],
    data={"authors": [{"name": "John"}]}
)
@example(
    authors=["John Doe"],
    data={"authors": [{"name": "Doe"}]}
)
@example(
    authors=["John Doe"],
    data={"authors": [{"name": "Jane Doe"}]}
)
def test_s2_authors_match(authors: list[str], data: dict):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    authors_copy = copy.deepcopy(authors)
    data_copy = copy.deepcopy(data)

    # Call func0 to verify input validity
    try:
        expected = s2_authors_match(authors_copy, data_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "authors": authors_copy,
            "data": data_copy
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