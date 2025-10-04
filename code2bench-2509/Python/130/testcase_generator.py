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
def collect_round_candidates(transcript: list, num_agents: int, round_index: int) -> list:
    """Collect candidates from specified round (prioritizes answer, falls back to argument)."""
    candidates = []
    for agent_id in range(num_agents):
        records = [
            t for t in transcript if t.get("agent_id") == agent_id and t.get("round") == round_index
        ]
        if not records:
            continue
        rec = records[-1]
        ans = (rec.get("answer") or "").strip()
        arg = (rec.get("argument") or "").strip()
        text = ans if ans else arg
        if text:
            candidates.append({"agent_id": agent_id, "text": text})
    return candidates

# Strategy for generating transcript entries
def transcript_entry_strategy():
    return st.fixed_dictionaries({
        "agent_id": st.integers(min_value=0, max_value=10),
        "round": st.integers(min_value=0, max_value=10),
        "answer": st.one_of(st.none(), st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')))),
        "argument": st.one_of(st.none(), st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'))))
    })

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    transcript=st.lists(transcript_entry_strategy(), min_size=0, max_size=20),
    num_agents=st.integers(min_value=1, max_value=10),
    round_index=st.integers(min_value=0, max_value=10)
)
@example(transcript=[], num_agents=1, round_index=0)
@example(transcript=[{"agent_id": 0, "round": 0, "answer": "Yes", "argument": None}], num_agents=1, round_index=0)
@example(transcript=[{"agent_id": 0, "round": 0, "answer": None, "argument": "Because"}], num_agents=1, round_index=0)
@example(transcript=[{"agent_id": 0, "round": 0, "answer": "", "argument": "Because"}], num_agents=1, round_index=0)
@example(transcript=[{"agent_id": 0, "round": 1, "answer": "Yes", "argument": None}], num_agents=1, round_index=0)
@example(transcript=[{"agent_id": 0, "round": 0, "answer": "Yes", "argument": "Because"}], num_agents=1, round_index=0)
@example(transcript=[{"agent_id": 0, "round": 0, "answer": None, "argument": None}], num_agents=1, round_index=0)
def test_collect_round_candidates(transcript, num_agents, round_index):
    global stop_collecting
    if stop_collecting:
        return
    
    transcript_copy = copy.deepcopy(transcript)
    try:
        expected = collect_round_candidates(transcript_copy, num_agents, round_index)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    # Filter to prioritize meaningful cases
    if any(
        t.get("round") == round_index and (t.get("answer") or t.get("argument"))
        for t in transcript
    ):
        generated_cases.append({
            "Inputs": {"transcript": transcript, "num_agents": num_agents, "round_index": round_index},
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