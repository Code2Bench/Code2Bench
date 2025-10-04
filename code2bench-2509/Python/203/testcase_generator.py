from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List, Optional
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
def get_required_actions(step_number: int, confidence: str, findings: str, total_steps: int, request=None) -> List[str]:
    actions = []

    if step_number == 1:
        actions.extend(
            [
                "Begin systematic thinking analysis",
                "Identify key aspects and assumptions to explore",
                "Establish initial investigation approach",
            ]
        )
    elif confidence == "low":
        actions.extend(
            [
                "Continue gathering evidence and insights",
                "Test initial hypotheses",
                "Explore alternative perspectives",
            ]
        )
    elif confidence == "medium":
        actions.extend(
            [
                "Deepen analysis of promising approaches",
                "Validate key assumptions",
                "Consider implementation challenges",
            ]
        )
    elif confidence == "high":
        actions.extend(
            [
                "Refine and validate key findings",
                "Explore edge cases and limitations",
                "Document assumptions and trade-offs",
            ]
        )
    elif confidence == "very_high":
        actions.extend(
            [
                "Synthesize findings into cohesive recommendations",
                "Validate conclusions against all evidence",
                "Prepare comprehensive implementation guidance",
            ]
        )
    elif confidence == "almost_certain":
        actions.extend(
            [
                "Finalize recommendations with high confidence",
                "Document any remaining minor uncertainties",
                "Prepare for expert analysis or implementation",
            ]
        )
    else:  # certain
        actions.append("Analysis complete - ready for implementation")

    return actions

# Strategy for generating confidence levels
confidence_strategy = st.one_of([
    st.just("low"),
    st.just("medium"),
    st.just("high"),
    st.just("very_high"),
    st.just("almost_certain"),
    st.just("certain")
])

# Strategy for generating step numbers and total steps
step_strategy = st.integers(min_value=1, max_value=100)

# Strategy for generating findings
findings_strategy = st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=100)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    step_number=step_strategy,
    confidence=confidence_strategy,
    findings=findings_strategy,
    total_steps=step_strategy
)
@example(step_number=1, confidence="low", findings="Initial findings", total_steps=10)
@example(step_number=2, confidence="medium", findings="Some findings", total_steps=5)
@example(step_number=3, confidence="high", findings="Detailed findings", total_steps=20)
@example(step_number=4, confidence="very_high", findings="Comprehensive findings", total_steps=15)
@example(step_number=5, confidence="almost_certain", findings="Final findings", total_steps=25)
@example(step_number=6, confidence="certain", findings="Complete findings", total_steps=30)
def test_get_required_actions(step_number: int, confidence: str, findings: str, total_steps: int):
    global stop_collecting
    if stop_collecting:
        return

    try:
        expected = get_required_actions(step_number, confidence, findings, total_steps)
    except Exception:
        return  # Skip inputs that cause exceptions

    generated_cases.append({
        "Inputs": {
            "step_number": step_number,
            "confidence": confidence,
            "findings": findings,
            "total_steps": total_steps
        },
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