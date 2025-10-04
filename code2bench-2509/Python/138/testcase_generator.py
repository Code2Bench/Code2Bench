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
def _compact_signals(signals_by_ticker: dict[str, dict]) -> dict[str, dict]:
    """Keep only {agent: {sig, conf}} and drop empty agents."""
    out = {}
    for t, agents in signals_by_ticker.items():
        if not agents:
            out[t] = {}
            continue
        compact = {}
        for agent, payload in agents.items():
            sig = payload.get("sig") or payload.get("signal")
            conf = payload.get("conf") if "conf" in payload else payload.get("confidence")
            if sig is not None and conf is not None:
                compact[agent] = {"sig": sig, "conf": conf}
        out[t] = compact
    return out

# Strategy for generating agent payloads
def payload_strategy():
    return st.fixed_dictionaries({
        "sig": st.one_of([st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.none()]),
        "signal": st.one_of([st.integers(), st.floats(allow_nan=False, allow_infinity=False), st.none()]),
        "conf": st.one_of([st.floats(allow_nan=False, allow_infinity=False), st.none()]),
        "confidence": st.one_of([st.floats(allow_nan=False, allow_infinity=False), st.none()])
    })

# Strategy for generating signals_by_ticker
def signals_by_ticker_strategy():
    return st.dictionaries(
        keys=st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5),
        values=st.one_of([
            st.dictionaries(
                keys=st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1, max_size=5),
                values=payload_strategy(),
                min_size=0, max_size=5
            ),
            st.just({})
        ]),
        min_size=1, max_size=5
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(signals_by_ticker=signals_by_ticker_strategy())
@example(signals_by_ticker={})
@example(signals_by_ticker={"ticker1": {}})
@example(signals_by_ticker={"ticker1": {"agent1": {"sig": 1, "conf": 0.5}}})
@example(signals_by_ticker={"ticker1": {"agent1": {"signal": 1, "confidence": 0.5}}})
@example(signals_by_ticker={"ticker1": {"agent1": {"sig": 1, "confidence": 0.5}}})
@example(signals_by_ticker={"ticker1": {"agent1": {"signal": 1, "conf": 0.5}}})
@example(signals_by_ticker={"ticker1": {"agent1": {"sig": None, "conf": 0.5}}})
@example(signals_by_ticker={"ticker1": {"agent1": {"signal": 1, "confidence": None}}})
def test_compact_signals(signals_by_ticker: dict[str, dict]):
    global stop_collecting
    if stop_collecting:
        return
    
    signals_by_ticker_copy = copy.deepcopy(signals_by_ticker)
    try:
        expected = _compact_signals(signals_by_ticker_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"signals_by_ticker": signals_by_ticker},
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