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
def grouplines(sdp: str) -> tuple[list[str], list[list[str]]]:
    session = []
    media = []
    for line in sdp.splitlines():
        if line.startswith("m="):
            media.append([line])
        elif len(media):
            media[-1].append(line)
        else:
            session.append(line)
    return session, media

# Strategy for generating SDP-like strings
def sdp_strategy():
    return st.lists(
        st.one_of([
            st.just("m=audio 49170 RTP/AVP 0"),
            st.just("m=video 51372 RTP/AVP 99"),
            st.just("a=rtpmap:99 h263-1998/90000"),
            st.just("a=sendrecv"),
            st.just("c=IN IP4 192.0.2.3"),
            st.just("s=Session SDP"),
            st.just("t=0 0"),
            st.just("o=alice 2890844526 2890844526 IN IP4 192.0.2.3"),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
        ]),
        min_size=1,
        max_size=20
    ).map(lambda x: "\n".join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(sdp=sdp_strategy())
@example(sdp="m=audio 49170 RTP/AVP 0")
@example(sdp="m=video 51372 RTP/AVP 99\na=rtpmap:99 h263-1998/90000")
@example(sdp="c=IN IP4 192.0.2.3\nm=audio 49170 RTP/AVP 0")
@example(sdp="s=Session SDP\nt=0 0\nm=audio 49170 RTP/AVP 0")
@example(sdp="o=alice 2890844526 2890844526 IN IP4 192.0.2.3\nm=audio 49170 RTP/AVP 0")
def test_grouplines(sdp: str):
    global stop_collecting
    if stop_collecting:
        return
    
    sdp_copy = copy.deepcopy(sdp)
    try:
        expected = grouplines(sdp_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if any(line.startswith("m=") for line in sdp.splitlines()):
        generated_cases.append({
            "Inputs": {"sdp": sdp},
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