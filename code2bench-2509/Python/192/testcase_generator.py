from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import Dict, Any
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
def _format_platform_constraints(platform: str, platform_adaptation: Dict[str, Any]) -> str:
    content_rules = platform_adaptation.get("content_format_rules", {})
    engagement = platform_adaptation.get("engagement_patterns", {})

    constraints = []

    if content_rules.get("character_limit"):
        constraints.append(f"Character limit: {content_rules['character_limit']}")

    if content_rules.get("optimal_length"):
        constraints.append(f"Optimal length: {content_rules['optimal_length']}")

    if engagement.get("posting_frequency"):
        constraints.append(f"Frequency: {engagement['posting_frequency']}")

    if platform == "twitter":
        constraints.extend([
            "Max 3 hashtags",
            "Thread-friendly format",
            "Engagement-optimized"
        ])
    elif platform == "linkedin":
        constraints.extend([
            "Professional networking focus",
            "Thought leadership tone",
            "Business value emphasis"
        ])
    elif platform == "blog":
        constraints.extend([
            "SEO-optimized structure",
            "Scannable format",
            "Clear headings"
        ])

    return "- " + "\n- ".join(constraints) if constraints else "- Standard platform optimization"

# Strategy for generating platform strings
platform_strategy = st.one_of([
    st.just("twitter"),
    st.just("linkedin"),
    st.just("blog"),
    st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
])

# Strategy for generating platform adaptation dictionaries
def platform_adaptation_strategy():
    return st.fixed_dictionaries({
        "content_format_rules": st.fixed_dictionaries({
            "character_limit": st.one_of([st.none(), st.integers(min_value=1, max_value=1000)]),
            "optimal_length": st.one_of([st.none(), st.integers(min_value=1, max_value=1000)])
        }),
        "engagement_patterns": st.fixed_dictionaries({
            "posting_frequency": st.one_of([st.none(), st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)])
        })
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(platform=platform_strategy, platform_adaptation=platform_adaptation_strategy())
@example(platform="twitter", platform_adaptation={"content_format_rules": {"character_limit": 280}, "engagement_patterns": {"posting_frequency": "daily"}})
@example(platform="linkedin", platform_adaptation={"content_format_rules": {"optimal_length": 500}, "engagement_patterns": {"posting_frequency": "weekly"}})
@example(platform="blog", platform_adaptation={"content_format_rules": {"character_limit": None, "optimal_length": 1000}, "engagement_patterns": {"posting_frequency": None}})
@example(platform="unknown", platform_adaptation={"content_format_rules": {}, "engagement_patterns": {}})
def test_format_platform_constraints(platform: str, platform_adaptation: Dict[str, Any]):
    global stop_collecting
    if stop_collecting:
        return
    
    platform_copy = copy.deepcopy(platform)
    platform_adaptation_copy = copy.deepcopy(platform_adaptation)
    try:
        expected = _format_platform_constraints(platform_copy, platform_adaptation_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"platform": platform, "platform_adaptation": platform_adaptation},
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