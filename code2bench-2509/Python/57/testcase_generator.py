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
def parse_hp_string(hp_string):
    result = {}
    for pair in hp_string.split(','):
        if not pair:
            continue
        key, value = pair.split('=')
        try:
            # 自动转换为 int / float / str
            ori_value = value
            value = float(value)
            if '.' not in str(ori_value):
                value = int(value)
        except ValueError:
            pass

        if value in ['true', 'True']:
            value = True
        if value in ['false', 'False']:
            value = False
        if '.' in key:
            keys = key.split('.')
            keys = keys
            current = result
            for key in keys[:-1]:
                if key not in current or not isinstance(current[key], dict):
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = value
        else:
            result[key.strip()] = value
    return result

# Strategy for generating valid key-value pairs
def key_strategy():
    return st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=10)

def value_strategy():
    return st.one_of([
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S')), min_size=1, max_size=10),
        st.booleans()
    ])

def pair_strategy():
    return st.tuples(key_strategy(), value_strategy()).map(lambda x: f"{x[0]}={x[1]}")

# Strategy for generating hp_string
def hp_string_strategy():
    return st.lists(pair_strategy(), min_size=1, max_size=5).map(lambda x: ",".join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(hp_string=hp_string_strategy())
@example(hp_string="key1=value1,key2=value2")
@example(hp_string="key1=123,key2=456.789")
@example(hp_string="key1=true,key2=false")
@example(hp_string="key1=value1,key2=value2,key3=value3")
@example(hp_string="key1=value1,key2=value2,key3=value3,key4=value4")
@example(hp_string="key1=value1,key2=value2,key3=value3,key4=value4,key5=value5")
@example(hp_string="key1=value1,key2=value2,key3=value3,key4=value4,key5=value5,key6=value6")
@example(hp_string="key1=value1,key2=value2,key3=value3,key4=value4,key5=value5,key6=value6,key7=value7")
@example(hp_string="key1=value1,key2=value2,key3=value3,key4=value4,key5=value5,key6=value6,key7=value7,key8=value8")
@example(hp_string="key1=value1,key2=value2,key3=value3,key4=value4,key5=value5,key6=value6,key7=value7,key8=value8,key9=value9")
@example(hp_string="key1=value1,key2=value2,key3=value3,key4=value4,key5=value5,key6=value6,key7=value7,key8=value8,key9=value9,key10=value10")
def test_parse_hp_string(hp_string):
    global stop_collecting
    if stop_collecting:
        return
    
    hp_string_copy = copy.deepcopy(hp_string)
    try:
        expected = parse_hp_string(hp_string_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"hp_string": hp_string},
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