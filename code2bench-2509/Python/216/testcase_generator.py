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
def _format_community_content(base_text: str, entities: list[str], keywords: list[str]) -> str:
    if not entities and not keywords:
        return base_text

    content_parts = [base_text, "\n  Contains:"]

    if entities:
        shown = entities[:3]
        entities_text = f"\n    Entities: {', '.join(shown)}"
        if len(entities) > 3:
            entities_text += f" and {len(entities) - 3} more"
        content_parts.append(entities_text)

    if keywords:
        shown = keywords[:3]
        keywords_text = f"\n    Keywords: {', '.join(shown)}"
        if len(keywords) > 3:
            keywords_text += f" and {len(keywords) - 3} more"
        content_parts.append(keywords_text)

    return "".join(content_parts)

# Strategy for generating base text
def base_text_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)

# Strategy for generating entities and keywords
def entity_keyword_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    base_text=base_text_strategy(),
    entities=st.lists(entity_keyword_strategy(), max_size=10),
    keywords=st.lists(entity_keyword_strategy(), max_size=10)
)
@example(base_text="Sample text", entities=[], keywords=[])
@example(base_text="Sample text", entities=["entity1"], keywords=[])
@example(base_text="Sample text", entities=[], keywords=["keyword1"])
@example(base_text="Sample text", entities=["entity1", "entity2", "entity3", "entity4"], keywords=["keyword1", "keyword2", "keyword3", "keyword4"])
@example(base_text="Sample text", entities=["entity1"], keywords=["keyword1"])
@example(base_text="Sample text", entities=["entity1", "entity2"], keywords=["keyword1", "keyword2"])
def test_format_community_content(base_text: str, entities: list[str], keywords: list[str]):
    global stop_collecting
    if stop_collecting:
        return
    
    base_text_copy = copy.deepcopy(base_text)
    entities_copy = copy.deepcopy(entities)
    keywords_copy = copy.deepcopy(keywords)
    try:
        expected = _format_community_content(base_text_copy, entities_copy, keywords_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if (len(entities) > 0 or len(keywords) > 0) or (len(entities) == 0 and len(keywords) == 0):
        generated_cases.append({
            "Inputs": {"base_text": base_text, "entities": entities, "keywords": keywords},
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