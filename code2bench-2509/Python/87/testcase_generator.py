import hypothesis
import hypothesis.strategies as st
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
def enquote_executable(executable):
    if ' ' in executable:
        # make sure we quote only the executable in case of env
        # for example /usr/bin/env "/dir with spaces/bin/jython"
        # instead of "/usr/bin/env /dir with spaces/bin/jython"
        # otherwise whole
        if executable.startswith('/usr/bin/env '):
            env, _executable = executable.split(' ', 1)
            if ' ' in _executable and not _executable.startswith('"'):
                executable = '%s "%s"' % (env, _executable)
        else:
            if not executable.startswith('"'):
                executable = '"%s"' % executable
    return executable

# Strategy for generating executable paths
def executable_strategy():
    return st.one_of([
        # Executables with spaces
        st.tuples(
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1)
        ).map(lambda x: '/'.join(x)),
        # Executables with /usr/bin/env prefix
        st.tuples(
            st.just('/usr/bin/env'),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1),
            st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1)
        ).map(lambda x: ' '.join(x)),
        # Simple executables without spaces
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1)
    ])

# Hypothesis test configuration
@hypothesis.settings(max_examples=10000, verbosity=hypothesis.Verbosity.verbose, print_blob=True)
@hypothesis.given(executable=executable_strategy())
@hypothesis.example(executable="/usr/bin/env python")
@hypothesis.example(executable="/usr/bin/env python script")
@hypothesis.example(executable="/usr/bin/env python script with spaces")
@hypothesis.example(executable="/usr/bin/env python script with spaces and quotes")
@hypothesis.example(executable="/usr/bin/env python script with spaces and quotes")
def test_enquote_executable(executable):
    global stop_collecting
    if stop_collecting:
        return
    
    executable_copy = copy.deepcopy(executable)
    try:
        expected = enquote_executable(executable_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    generated_cases.append({
        "Inputs": {"executable": executable},
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