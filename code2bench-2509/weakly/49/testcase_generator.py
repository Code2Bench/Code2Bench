from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import os
import atexit
import copy
from typing import Optional, Tuple
from urllib.parse import urlparse

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def normalize_run_path(target: str, entity: Optional[str], project: Optional[str]) -> Tuple[str, str, str]:
    if target.startswith(("http://", "https://")):
        parsed = urlparse(target)
        parts = [p for p in parsed.path.split("/") if p]
        if len(parts) < 3:
            raise ValueError(f"Could not parse run information from URL: {target}")
        entity = parts[0]
        project = parts[1]
        if parts[2] == "runs" and len(parts) >= 4:
            run_id = parts[3]
        else:
            run_id = parts[2]
        return entity, project, run_id

    parts = [p for p in target.split("/") if p]
    if len(parts) == 1:
        if not entity or not project:
            raise ValueError("Bare run ids require --entity and --project.")
        return entity, project, parts[0]

    if len(parts) >= 3:
        entity = parts[0]
        project = parts[1]
        if parts[2] == "runs" and len(parts) >= 4:
            run_id = parts[3]
        else:
            run_id = parts[2]
        return entity, project, run_id

    raise ValueError(f"Unrecognized run target: {target}")

# Strategies for generating inputs
def target_strategy():
    return st.one_of(
        st.builds(
            lambda scheme, netloc, path: f"{scheme}://{netloc}/{path}",
            st.sampled_from(["http", "https"]),
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            st.lists(
                st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
                min_size=3, max_size=5
            ).map(lambda parts: "/".join(parts))
        ),
        st.lists(
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10),
            min_size=1, max_size=5
        ).map(lambda parts: "/".join(parts))
    )

def entity_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10)

def project_strategy():
    return st.text(alphabet=st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=10)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    target=target_strategy(),
    entity=st.one_of(st.none(), entity_strategy()),
    project=st.one_of(st.none(), project_strategy())
)
@example(
    target="http://example.com/entity/project/runs/run_id",
    entity=None,
    project=None
)
@example(
    target="https://example.com/entity/project/run_id",
    entity=None,
    project=None
)
@example(
    target="run_id",
    entity="entity",
    project="project"
)
@example(
    target="entity/project/run_id",
    entity=None,
    project=None
)
@example(
    target="entity/project/runs/run_id",
    entity=None,
    project=None
)
def test_normalize_run_path(target: str, entity: Optional[str], project: Optional[str]):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy inputs to avoid modification
    target_copy = copy.deepcopy(target)
    entity_copy = copy.deepcopy(entity)
    project_copy = copy.deepcopy(project)

    # Call func0 to verify input validity
    try:
        expected = normalize_run_path(target_copy, entity_copy, project_copy)
    except ValueError:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "target": target_copy,
            "entity": entity_copy,
            "project": project_copy
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