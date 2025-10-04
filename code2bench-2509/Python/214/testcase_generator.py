from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Dict, List
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
def organize_imports_by_category(files_by_category: Dict[str, List[str]]) -> str:
    if not files_by_category:
        return ""

    sections = []

    # Framework imports section header
    sections.append("# ===================================================")
    sections.append("# SuperClaude Framework Components")
    sections.append("# ===================================================")
    sections.append("")

    # Add each category
    for category, files in files_by_category.items():
        if files:
            sections.append(f"# {category}")
            for file in sorted(files):
                sections.append(f"@{file}")
            sections.append("")

    return "\n".join(sections)

# Strategy for generating files_by_category
def files_by_category_strategy():
    return st.dictionaries(
        keys=st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20),
        values=st.lists(st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20), min_size=0, max_size=5),
        min_size=0, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(files_by_category=files_by_category_strategy())
@example(files_by_category={})
@example(files_by_category={"category1": ["file1", "file2"]})
@example(files_by_category={"category1": [], "category2": ["file3"]})
@example(files_by_category={"category1": ["file2", "file1"], "category2": ["file3", "file4"]})
def test_organize_imports_by_category(files_by_category: Dict[str, List[str]]):
    global stop_collecting
    if stop_collecting:
        return
    
    files_by_category_copy = copy.deepcopy(files_by_category)
    try:
        expected = organize_imports_by_category(files_by_category_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if files_by_category or any(files for files in files_by_category.values()):
        generated_cases.append({
            "Inputs": {"files_by_category": files_by_category},
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