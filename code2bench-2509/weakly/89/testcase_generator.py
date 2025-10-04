from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import json
import urllib.parse
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
def parse_rtc_config(data):
    ice_servers = json.loads(data)['iceServers']
    stun_uris = []
    turn_uris = []
    for ice_server in ice_servers:
        for url in ice_server.get("urls", []):
            if url.startswith("stun:"):
                stun_host = url.split(":")[1]
                stun_port = url.split(":")[2].split("?")[0]
                stun_uri = "stun://%s:%s" % (
                    stun_host,
                    stun_port
                )
                stun_uris.append(stun_uri)
            elif url.startswith("turn:"):
                turn_host = url.split(':')[1]
                turn_port = url.split(':')[2].split('?')[[0]]
                turn_user = ice_server['username']
                turn_password = ice_server['credential']
                turn_uri = "turn://%s:%s@%s:%s" % (
                    urllib.parse.quote(turn_user, safe=""),
                    urllib.parse.quote(turn_password, safe=""),
                    turn_host,
                    turn_port
                )
                turn_uris.append(turn_uri)
            elif url.startswith("turns:"):
                turn_host = url.split(':')[1]
                turn_port = url.split(':')[2].split('?')[0]
                turn_user = ice_server['username']
                turn_password = ice_server['credential']
                turn_uri = "turns://%s:%s@%s:%s" % (
                    urllib.parse.quote(turn_user, safe=""),
                    urllib.parse.quote(turn_password, safe=""),
                    turn_host,
                    turn_port
                )
                turn_uris.append(turn_uri)
    return stun_uris, turn_uris, data

# Strategies for generating inputs
def url_strategy(prefix):
    return st.builds(
        lambda host, port: f"{prefix}:{host}:{port}",
        st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P')), min_size=1, max_size=10),
        st.integers(min_value=1, max_value=65535)
    )

def ice_server_strategy():
    return st.fixed_dictionaries({
        "urls": st.lists(
            st.one_of(
                url_strategy("stun"),
                url_strategy("turn"),
                url_strategy("turns")
            ),
            min_size=1, max_size=3
        ),
        "username": st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P')), min_size=1, max_size=10),
        "credential": st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P')), min_size=1, max_size=10)
    })

def data_strategy():
    return st.builds(
        lambda ice_servers: json.dumps({"iceServers": ice_servers}),
        st.lists(ice_server_strategy(), min_size=1, max_size=3)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(data=data_strategy())
@example(data=json.dumps({"iceServers": [{"urls": ["stun:example.com:3478"], "username": "user", "credential": "pass"}]}))
@example(data=json.dumps({"iceServers": [{"urls": ["turn:example.com:3478"], "username": "user", "credential": "pass"}]}))
@example(data=json.dumps({"iceServers": [{"urls": ["turns:example.com:3478"], "username": "user", "credential": "pass"}]}))
@example(data=json.dumps({"iceServers": [{"urls": ["stun:example.com:3478", "turn:example.com:3478"], "username": "user", "credential": "pass"}]}))
@example(data=json.dumps({"iceServers": [{"urls": ["stun:example.com:3478"], "username": "user", "credential": "pass"}, {"urls": ["turn:example.com:3478"], "username": "user2", "credential": "pass2"}]}))
def test_parse_rtc_config(data: str):
    global stop_collecting
    if stop_collecting:
        return

    # Deep copy input to avoid modification
    data_copy = copy.deepcopy(data)

    # Call func0 to verify input validity
    try:
        expected_stun_uris, expected_turn_uris, expected_data = parse_rtc_config(data_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "data": data_copy
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