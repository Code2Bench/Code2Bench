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
def _parse_ethtool_unprefixed_queue_num(stat_name):
    """
    Extract the queue and the metric name from ethtool stat name:
    tx0_bytes -> (queue:0, tx_bytes)
    rx1_packets -> (queue:1, rx_packets)
    """
    if 'rx' not in stat_name and 'tx' not in stat_name:
        return None, None
    parts = stat_name.split('_')
    queue_num = None
    queue_index = None
    for i, part in enumerate(parts):
        if not part.startswith('tx') and not part.startswith('rx'):
            continue
        if part[2:].isdigit():
            queue_num = part[2:]
            queue_index = i
            break
    if queue_num is None or not queue_num.isdigit():
        return None, None
    parts[queue_index] = parts[queue_index][:2]
    return 'queue:{}'.format(queue_num), '_'.join(parts)

# Strategy for generating ethtool stat names
def ethtool_stat_name_strategy():
    return st.one_of([
        st.tuples(
            st.one_of([st.just("tx"), st.just("rx")]),
            st.integers(min_value=0, max_value=999),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=10)
        ).map(lambda x: f"{x[0]}{x[1]}_{x[2]}"),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=20)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(stat_name=ethtool_stat_name_strategy())
@example(stat_name="tx0_bytes")
@example(stat_name="rx1_packets")
@example(stat_name="tx_bytes")
@example(stat_name="rx_packets")
@example(stat_name="tx0")
@example(stat_name="rx1")
@example(stat_name="invalid_stat")
def test_parse_ethtool_unprefixed_queue_num(stat_name):
    global stop_collecting
    if stop_collecting:
        return
    
    stat_name_copy = copy.deepcopy(stat_name)
    try:
        expected = _parse_ethtool_unprefixed_queue_num(stat_name_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if 'rx' in stat_name or 'tx' in stat_name:
        generated_cases.append({
            "Inputs": {"stat_name": stat_name},
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