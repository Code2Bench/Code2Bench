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
def format_transcript(transcript: list) -> str:
    """Format debate transcript for display."""
    if not transcript:
        return "(empty)"
    lines = []
    for turn in transcript:
        agent = turn.get("agent_id")
        rd = turn.get("round")
        role = turn.get("role")
        arg = (turn.get("argument") or "").strip()
        ans = (turn.get("answer") or "").strip()
        if ans:
            lines.append(f"[Round {rd}] Agent#{agent} ({role})\nArgument: {arg}\nAnswer: {ans}\n")
        else:
            lines.append(f"[Round {rd}] Agent#{agent} ({role})\nArgument: {arg}\n")
    return "\n".join(lines)

# Strategy for generating transcript entries
def transcript_strategy():
    return st.lists(
        st.dictionaries(
            keys=st.sampled_from(["agent_id", "round", "role", "argument", "answer"]),
            values=st.one_of([
                st.integers(min_value=0, max_value=100),
                st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), max_size=50),
                st.none()
            ]),
            min_size=3,  # Ensure at least agent_id, round, and role are present
            max_size=5
        ),
        min_size=0, max_size=10
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(transcript=transcript_strategy())
@example(transcript=[])
@example(transcript=[{"agent_id": 1, "round": 1, "role": "Proposer", "argument": "Let's do X.", "answer": "Agreed."}])
@example(transcript=[{"agent_id": 2, "round": 2, "role": "Opposer", "argument": "Let's not do X.", "answer": None}])
@example(transcript=[{"agent_id": 3, "round": 3, "role": "Moderator", "argument": None, "answer": "Let's move on."}])
def test_format_transcript(transcript: list):
    global stop_collecting
    if stop_collecting:
        return
    
    transcript_copy = copy.deepcopy(transcript)
    try:
        expected = format_transcript(transcript_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to ensure meaningful test cases
    if any(turn.get("agent_id") is not None and turn.get("round") is not None and turn.get("role") is not None for turn in transcript):
        generated_cases.append({
            "Inputs": {"transcript": transcript},
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