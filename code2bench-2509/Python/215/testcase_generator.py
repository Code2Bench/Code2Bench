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
def _parse_existing_framework_imports(content: str) -> Dict[str, List[str]]:
    imports_by_category = {}
    framework_marker = "# ===================================================\n# SuperClaude Framework Components"
    if framework_marker not in content:
        return imports_by_category
    framework_section = content.split(framework_marker)[1] if framework_marker in content else ""
    lines = framework_section.split('\n')
    current_category = None
    for line in lines:
        line = line.strip()
        if line.startswith('# ===') or not line:
            continue
        if line.startswith('# ') and not line.startswith('# ==='):
            current_category = line[2:].strip()
            if current_category not in imports_by_category:
                imports_by_category[current_category] = []
        elif line.startswith('@') and current_category:
            import_file = line[1:].strip()
            if import_file not in imports_by_category[current_category]:
                imports_by_category[current_category].append(import_file)
    return imports_by_category

# Strategy for generating content with framework marker
def content_strategy():
    framework_marker = "# ===================================================\n# SuperClaude Framework Components"
    category_strategy = st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
    import_strategy = st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
    
    def build_framework_section(categories):
        section = []
        for category in categories:
            section.append(f"# {category}")
            imports = st.lists(import_strategy, min_size=1, max_size=5).example()
            for imp in imports:
                section.append(f"@{imp}")
        return '\n'.join(section)
    
    return st.one_of([
        st.just(framework_marker + "\n" + build_framework_section(st.lists(category_strategy, min_size=1, max_size=5).example())),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=1000)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(content=content_strategy())
@example(content="# ===================================================\n# SuperClaude Framework Components\n# Category1\n@import1\n@import2\n# Category2\n@import3")
@example(content="# ===================================================\n# SuperClaude Framework Components\n# Category1\n@import1\n# ===\n# Category2\n@import2")
@example(content="Random content without framework marker")
@example(content="# ===================================================\n# SuperClaude Framework Components\n# Category1\n@import1\n@import1")
@example(content="# ===================================================\n# SuperClaude Framework Components\n# Category1\n@import1\n\n# Category2\n@import2")
def test_parse_existing_framework_imports(content: str):
    global stop_collecting
    if stop_collecting:
        return
    
    content_copy = copy.deepcopy(content)
    try:
        expected = _parse_existing_framework_imports(content_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if "# ===================================================\n# SuperClaude Framework Components" in content:
        generated_cases.append({
            "Inputs": {"content": content},
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