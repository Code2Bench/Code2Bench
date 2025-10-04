from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
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
def SubstituteTemplate(template, values_base):
    values = copy.deepcopy(values_base)
    if values.get("KernelSchedule") is not None and "Auto" in values["KernelSchedule"]:
        values["KernelSchedule"] = "collective::" + values["KernelSchedule"]
    if values.get("EpilogueSchedule") is not None and "Auto" in values["EpilogueSchedule"]:
        values["EpilogueSchedule"] = "collective::" + values["EpilogueSchedule"]
    text = template
    changed = True
    while changed:
        changed = False
        for key, value in values.items():
            regex = f"\\{{{key}\\}}"
            newtext = re.sub(regex, value, text)
            if newtext != text:
                changed = True
            text = newtext
    return text

# Strategies for generating inputs
def template_strategy():
    return st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), whitelist_characters='{}'),
        min_size=0, max_size=100
    )

def values_base_strategy():
    return st.dictionaries(
        keys=st.text(
            alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='_'),
            min_size=1, max_size=10
        ),
        values=st.one_of(
            st.text(
                alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), whitelist_characters='_'),
                min_size=0, max_size=20
            ),
            st.text(
                alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'), whitelist_characters='_'),
                min_size=0, max_size=20
            ).map(lambda x: "Auto" + x)
        ),
        min_size=1, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    template=template_strategy(),
    values_base=values_base_strategy()
)
@example(
    template="",
    values_base={}
)
@example(
    template="{KernelSchedule}",
    values_base={"KernelSchedule": "AutoSchedule"}
)
@example(
    template="{EpilogueSchedule}",
    values_base={"EpilogueSchedule": "AutoSchedule"}
)
@example(
    template="{KernelSchedule} {EpilogueSchedule}",
    values_base={"KernelSchedule": "AutoSchedule", "EpilogueSchedule": "AutoSchedule"}
)
@example(
    template="{Key1} {Key2}",
    values_base={"Key1": "Value1", "Key2": "Value2"}
)
def test_SubstituteTemplate(template, values_base):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    template_copy = copy.deepcopy(template)
    values_base_copy = copy.deepcopy(values_base)

    # Call func0 to verify input validity
    try:
        expected = SubstituteTemplate(template_copy, values_base_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "template": template_copy,
            "values_base": values_base_copy
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