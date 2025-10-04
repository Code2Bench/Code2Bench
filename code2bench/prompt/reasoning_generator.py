WEAKLY_SELF_CONTAINED_REASONING_TESTCASE_GENERATION_PROMPT = """
You are an expert Python developer specializing in generating example usage inputs and outputs for weakly self-contained Python functions. A weakly self-contained function depends only on standard libraries or specific external libraries (e.g., NumPy, re) and no other custom modules. Your task is to modify the provided Testcase Generator to generate 5-10 example usage cases for the function `func0`, using its Hypothesis strategies and `@example` cases. The output will be a JSON object containing input parameters and, where applicable, expected outputs or usage instructions, supporting differential testing (passing inputs to both `func0` and a tested implementation to compare outputs).

Follow these guidelines:
1. **Input Provided**:
- A complete Testcase Generator script, including:
 - The ground truth function `func0` (e.g., `chain_pair_pde`, `extract_email_domains`).
 - Hypothesis strategies (e.g., `num_tokens_strategy`, `text_strategy`) defining input ranges and types.
 - `@example` decorators specifying critical edge cases.
 - Validation logic (e.g., shape checks, exception handling).
- Example Testcase Generator structure:
```python
from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import json
import os
import atexit
import copy
# ... Configuration, func0, strategies, test function ...
```

2. **Modification Requirements**:
- Modify the Testcase Generator to:
 - Generate exactly 5-10 test cases (2-4 Normal, 3-6 Others) instead of 500.
 - Use existing Hypothesis strategies and `@example` cases to produce inputs.
 - Call `func0` to validate inputs and obtain outputs.
 - For **basic output types** (`int`, `float`, `str`, `bool`, `list[str]`, `list[int]`, etc.), include the output in the `Expected` field.
 - For **complex output types** (e.g., `np.ndarray`, `tuple`, nested structures), omit `Expected` and include a `Usage` field with Python code showing:
 - How to construct the inputs (e.g., `np.array([...])`).
 - How to call `func0` (e.g., `result = func0(...)`).
 - Output a JSON file with `"Normal cases"` and `"Others"` instead of `test_cases.json`.
 - Retain validation logic (e.g., shape checks, exception handling) to ensure input validity.

3. **Test Case Structure**:
- Each test case includes:
 - **Description**: A brief string explaining the test case (e.g., "Multiple chains", "Empty input").
 - **Inputs**: A dictionary mapping `func0`’s parameter names to JSON-serializable values (e.g., `int`, `list[int]`, `list[list[list[float]]]`, `str`).
 - **Expected** (optional): The output of `func0` if it is a basic type (e.g., `["gmail.com", "yahoo.com"]`).
 - **Usage** (optional): For complex outputs, a string containing Python code to construct inputs and call `func0`.
- Inputs must match `func0`’s signature and be compatible with the Hypothesis strategies and `@example` cases.
- NumPy arrays must be converted to `list` (e.g., `np.array([1, 2]).tolist() -> [1, 2]`).
- Strings must be valid per the strategy (e.g., email patterns for re-based functions).

4. **Coverage Requirements**:
- Generate 5-10 test cases covering:
 - **Normal cases** (2-4): Typical inputs triggering `func0`’s main logic (e.g., multiple email domains, multi-chain PDE arrays).
 - **Others** (3-6):
 - **Edge cases**: Empty or minimal/maximal inputs (e.g., empty string, zero tokens, large arrays).
 - **Duplicate detection**: Inputs with duplicates, if applicable (e.g., repeated email domains, identical `asym_ids`).
 - **Type boundary cases**: Inputs at type or value boundaries (e.g., max integer, complex regex patterns).
 - **Error handling cases**: Inputs that may trigger exceptions, if `func0` handles errors explicitly (otherwise, omit).
 - Use the Testcase Generator’s strategies and `@example` cases to guide input generation, ensuring coverage of all branches.

5. **Output Format (JSON)**:
- Structure the output as:
```json
{
    "Normal cases": [
        {
            "Description": "string",
            "Inputs": {
                "param1": value,
                "param2": value,
                ...
            },
            "Expected": value | null,
            "Usage": "string" | null
        },
        ...
    ],
    "Others": [
        {
            "Description": "string",
            "Inputs": {
                "param1": value,
                "param2": value,
                ...
            },
            "Expected": value | null,
            "Usage": "string" | null
        },
        ...
    ]
}
```
- Include `Expected` for basic output types; set to `null` if it is lib-specific.
- Include `Usage`.
- Ensure all inputs are JSON-serializable (e.g., NumPy arrays as `list`, no `np.ndarray` objects).

6. **Generation Guidelines**:
- Analyze `func0`’s signature, docstring, and logic to understand input requirements.
- Use Hypothesis strategies (e.g., `st.integers(min_value=0, max_value=10)`, `text_strategy`) to generate valid inputs.
- Include at least one input from each `@example` case to ensure critical scenarios.
- Call `func0` to validate inputs (no exceptions, triggers branches) and obtain outputs.
- For complex outputs, generate `Usage` as a multi-line Python code string, including:
    - Import statements (e.g., `import numpy as np`).
    - Input construction (e.g., `asym_ids = np.array([0, 0, 1])`).
    - Function call (e.g., `mean, min = chain_pair_pde(num_tokens, asym_ids, full_pde)`).
- Ensure inputs trigger all branches of `func0`, as defined in the Testcase Generator.

7. **Note**:
- Generate exactly 5-10 test cases (2-4 Normal, 3-6 Others) to balance coverage and conciseness.
- Ensure inputs support differential testing (valid for both `func0` and tested implementation).
- Modify the Testcase Generator minimally, reusing its strategies, validation, and `@example` cases.
- Output only the modified Python script, with no additional explanations or comments.

8. **Examples**:
#### Input Testcase Generator:
```python
from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False

# Ground truth function
def extract_email_domains(text: str) -> list[str]:
    email_pattern = r'[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    matches = re.findall(email_pattern, text)
    return sorted(list(set(matches)))

# Strategy for generating text with potential email addresses
def text_strategy():
    domain = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.'),
        min_size=3, max_size=15
    ).map(lambda s: s + '.' + st.sampled_from(['com', 'org', 'net', 'edu']).example())
    username = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='._%+-'),
        min_size=1, max_size=10
    )
    email = st.builds(
        lambda u, d: f"{u}@{d}",
        username, domain
    )
    return st.lists(
        st.one_of(
            email,
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)
        ),
        min_size=0, max_size=10
    ).map(lambda x: ' '.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="")
@example(text="user@gmail.com")
@example(text="alice@yahoo.com bob@gmail.com")
@example(text="no.emails@invalid user@domain.com")
@example(text="user.name@sub.domain.org other@domain.net")
@example(text="random text without emails")
def test_extract_email_domains(text: str):
    global stop_collecting
    if stop_collecting:
        return
    text_copy = copy.deepcopy(text)
    try:
        expected = extract_email_domains(text_copy)
    except Exception:
        return
    generated_cases.append({
        "Inputs": {
            "text": text_copy
        }
    })
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)
```
#### Output Modified Generator:
```python
from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

# Ground truth function
def extract_email_domains(text: str) -> list[str]:
    email_pattern = r'[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    matches = re.findall(email_pattern, text)
    return sorted(list(set(matches)))

# Strategy for generating text with potential email addresses
def text_strategy():
    domain = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.'),
        min_size=3, max_size=15
    ).map(lambda s: s + '.' + st.sampled_from(['com', 'org', 'net', 'edu']).example())
    username = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='._%+-'),
        min_size=1, max_size=10
    )
    email = st.builds(
        lambda u, d: f"{u}@{d}",
        username, domain
    )
    return st.lists(
        st.one_of(
            email,
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)
        ),
        min_size=0, max_size=10
    ).map(lambda x: ' '.join(x))

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="")
@example(text="user@gmail.com")
@example(text="alice@yahoo.com bob@gmail.com")
@example(text="no.emails@invalid user@domain.com")
@example(text="user.name@sub.domain.org other@domain.net")
@example(text="random text without emails")
def test_extract_email_domains(text: str):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return
    text_copy = copy.deepcopy(text)
    try:
        expected = extract_email_domains(text_copy)
    except Exception:
        return

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Multiple unique email domains"
        elif case_count == 1:
            desc = "Single email domain"
        else:
            desc = "Mixed text with emails"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Empty string"
        elif case_count == 4:
            desc = "Duplicate email domains"
        elif case_count == 5:
            desc = "Invalid email format"
        elif case_count == 6:
            desc = "Long complex string with subdomains"
        else:
            desc = "No email addresses"

    # Store case
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {"text": text_copy},
        "Expected": expected,
        "Usage": None
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)
```
#### Input Testcase Generator:
```python
from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False

# Ground truth function
def chain_pair_pde(
    num_tokens: int, asym_ids: np.ndarray, full_pde: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    full_pde = full_pde[:, :num_tokens, :num_tokens]
    asym_ids = asym_ids[:num_tokens]
    unique_asym_ids = np.unique(asym_ids)
    num_chains = len(unique_asym_ids)
    num_samples = full_pde.shape[0]
    chain_pair_pred_err_mean = np.zeros((num_samples, num_chains, num_chains))
    chain_pair_pred_err_min = np.zeros((num_samples, num_chains, num_chains))

    for idx1, asym_id_1 in enumerate(unique_asym_ids):
        subset = full_pde[:, asym_ids == asym_id_1, :]
        for idx2, asym_id_2 in enumerate(unique_asym_ids):
            subsubset = subset[:, :, asym_ids == asym_id_2]
            chain_pair_pred_err_mean[:, idx1, idx2] = np.mean(subsubset, axis=(1, 2))
            chain_pair_pred_err_min[:, idx1, idx2] = np.min(subsubset, axis=(1, 2))
    return chain_pair_pred_err_mean, chain_pair_pred_err_min

# Strategies for generating inputs
def num_tokens_strategy():
    return st.integers(min_value=0, max_value=10)

def asym_ids_strategy(num_tokens):
    return hnp.arrays(
        dtype=np.int32,
        shape=(num_tokens,),
        elements=st.integers(min_value=0, max_value=5)
    )

def full_pde_strategy(num_tokens):
    return hnp.arrays(
        dtype=np.float32,
        shape=st.tuples(
            st.integers(min_value=1, max_value=3),
            st.just(num_tokens),
            st.just(num_tokens)
        ),
        elements=st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    num_tokens=num_tokens_strategy(),
    asym_ids=st.builds(
        lambda n: asym_ids_strategy(n),
        num_tokens_strategy()
    ),
    full_pde=st.builds(
        lambda n: full_pde_strategy(n),
        num_tokens_strategy()
    )
)
@example(
    num_tokens=0,
    asym_ids=np.array([]),
    full_pde=np.array([[]])
)
@example(
    num_tokens=1,
    asym_ids=np.array([0]),
    full_pde=np.array([[[0.0]]])
)
@example(
    num_tokens=3,
    asym_ids=np.array([0, 0, 1]),
    full_pde=np.array([[[1.0, 2.0, 3.0], [2.0, 1.0, 4.0], [3.0, 4.0, 1.0]]])
)
def test_chain_pair_pde(num_tokens: int, asym_ids: np.ndarray, full_pde: np.ndarray):
    global stop_collecting
    if stop_collecting:
        return
    if len(asym_ids) != num_tokens or full_pde.shape[1:] != (num_tokens, num_tokens):
        return
    num_tokens_copy = num_tokens
    asym_ids_copy = copy.deepcopy(asym_ids)
    full_pde_copy = copy.deepcopy(full_pde)
    try:
        expected_mean, expected_min = chain_pair_pde(num_tokens_copy, asym_ids_copy, full_pde_copy)
    except Exception:
        return
    generated_cases.append({
        "Inputs": {
            "num_tokens": num_tokens_copy,
            "asym_ids": asym_ids_copy.tolist(),
            "full_pde": full_pde_copy.tolist()
        }
    })
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)
```
#### Output Modified Generator:
```python
from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "example_usages.json")
generated_cases = {
    "Normal cases": [],
    "Others": []
}
stop_collecting = False
case_count = 0
MAX_CASES = 8

# Ground truth function
def chain_pair_pde(
    num_tokens: int, asym_ids: np.ndarray, full_pde: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    full_pde = full_pde[:, :num_tokens, :num_tokens]
    asym_ids = asym_ids[:num_tokens]
    unique_asym_ids = np.unique(asym_ids)
    num_chains = len(unique_asym_ids)
    num_samples = full_pde.shape[0]
    chain_pair_pred_err_mean = np.zeros((num_samples, num_chains, num_chains))
    chain_pair_pred_err_min = np.zeros((num_samples, num_chains, num_chains))

    for idx1, asym_id_1 in enumerate(unique_asym_ids):
        subset = full_pde[:, asym_ids == asym_id_1, :]
        for idx2, asym_id_2 in enumerate(unique_asym_ids):
            subsubset = subset[:, :, asym_ids == asym_id_2]
            chain_pair_pred_err_mean[:, idx1, idx2] = np.mean(subsubset, axis=(1, 2))
            chain_pair_pred_err_min[:, idx1, idx2] = np.min(subsubset, axis=(1, 2))
    return chain_pair_pred_err_mean, chain_pair_pred_err_min

# Strategies for generating inputs
def num_tokens_strategy():
    return st.integers(min_value=0, max_value=10)

def asym_ids_strategy(num_tokens):
    return hnp.arrays(
        dtype=np.int32,
        shape=(num_tokens,),
        elements=st.integers(min_value=0, max_value=5)
    )

def full_pde_strategy(num_tokens):
    return hnp.arrays(
        dtype=np.float32,
        shape=st.tuples(
            st.integers(min_value=1, max_value=3),
            st.just(num_tokens),
            st.just(num_tokens)
        ),
        elements=st.floats(min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False)
    )

# Hypothesis test configuration
@settings(max_examples=100, verbosity=Verbosity.verbose, print_blob=True)
@given(
    num_tokens=num_tokens_strategy(),
    asym_ids=st.builds(
        lambda n: asym_ids_strategy(n),
        num_tokens_strategy()
    ),
    full_pde=st.builds(
        lambda n: full_pde_strategy(n),
        num_tokens_strategy()
    )
)
@example(
    num_tokens=0,
    asym_ids=np.array([]),
    full_pde=np.array([[]])
)
@example(
    num_tokens=1,
    asym_ids=np.array([0]),
    full_pde=np.array([[[0.0]]])
)
@example(
    num_tokens=3,
    asym_ids=np.array([0, 0, 1]),
    full_pde=np.array([[[1.0, 2.0, 3.0], [2.0, 1.0, 4.0], [3.0, 4.0, 1.0]]])
)
def test_chain_pair_pde(num_tokens: int, asym_ids: np.ndarray, full_pde: np.ndarray):
    global stop_collecting, case_count
    if stop_collecting or case_count >= MAX_CASES:
        return
    if len(asym_ids) != num_tokens or full_pde.shape[1:] != (num_tokens, num_tokens):
        return
    num_tokens_copy = num_tokens
    asym_ids_copy = copy.deepcopy(asym_ids)
    full_pde_copy = copy.deepcopy(full_pde)
    try:
        expected_mean, expected_min = chain_pair_pde(num_tokens_copy, asym_ids_copy, full_pde_copy)
    except Exception:
        return

    # Determine case type
    if case_count < 3:
        case_type = "Normal cases"
        if case_count == 0:
            desc = "Multiple chains with multiple samples"
        elif case_count == 1:
            desc = "Single chain with single sample"
        else:
            desc = "Two chains with multiple samples"
    else:
        case_type = "Others"
        if case_count == 3:
            desc = "Empty input"
        elif case_count == 4:
            desc = "Single token with single chain"
        elif case_count == 5:
            desc = "Duplicate chain IDs"
        elif case_count == 6:
            desc = "Large number of tokens"
        else:
            desc = "Single sample with multiple chains"

    # Generate usage code
    usage = f\"\"\"import numpy as np

# Construct inputs
num_tokens = {num_tokens}
asym_ids = np.array({asym_ids_copy.tolist()})
full_pde = np.array({full_pde_copy.tolist()})

# Call function
mean, min = chain_pair_pde(num_tokens, asym_ids, full_pde)
\"\"\"

    # Store case
    # We don't include the expected output for lib-specific types
    generated_cases[case_type].append({
        "Description": desc,
        "Inputs": {
            "num_tokens": num_tokens_copy,
            "asym_ids": asym_ids_copy.tolist(),
            "full_pde": full_pde_copy.tolist()
        },
        "Expected": None,
        "Usage": usage
    })
    case_count += 1
    if case_count >= MAX_CASES:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {sum(len(cases) for cases in generated_cases.values())} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)
```
"""

WEAKLY_SELF_CONTAINED_REASONING_TESTCASE_GENERATION_PROMPT_v0 = """
You are an expert testing engineer specializing in generating reasoning-focused example usage inputs for weakly self-contained Python functions. A weakly self-contained function depends only on standard libraries or specific external libraries (e.g., NumPy, re) and no other custom modules. Your task is to generate a JSON object containing example input parameters for the function `func0` provided in the Testcase Generator, based on its signature, Hypothesis strategies, and `@example` cases. The inputs will be used for differential testing (passing to both `func0` and a tested implementation to compare outputs).

Follow these guidelines:

1. **Input Provided**:
   - A complete Testcase Generator script, including:
     - The ground truth function `func0` (e.g., `chain_pair_pde`, `extract_email_domains`).
     - Hypothesis strategies (e.g., `num_tokens_strategy`, `text_strategy`) defining input ranges and types.
     - `@example` decorators specifying critical edge cases.
   - Example Testcase Generator structure:
     ```python
     from hypothesis import settings, given, Verbosity, example
     from hypothesis import strategies as st
     import hypothesis.extra.numpy as hnp
     import numpy as np
     import json
     import os
     import atexit
     import copy
     # ... Configuration, func0, strategies, test function ...
     ```

2. **Test Case Structure**:
   - Each test case includes:
     - **Description**: A brief string explaining the test case (e.g., "Single email domain", "Empty input").
     - **Inputs**: A dictionary mapping `func0`’s parameter names to JSON-serializable values (e.g., `int`, `list[int]`, `list[list[list[float]]]`, `str`).
   - Inputs must match `func0`’s signature and be compatible with the Hypothesis strategies and `@example` cases.
   - For NumPy arrays, use `list` representation (e.g., `np.array([1, 2]).tolist() -> [1, 2]`).
   - For strings (e.g., in re-based functions), use valid string formats matching the strategy.

3. **Coverage Requirements**:
   - Generate 5-10 test cases covering:
     - **Normal cases**: Typical inputs triggering `func0`’s main logic (e.g., multiple email domains, multi-chain PDE arrays).
     - **Edge cases**: Empty or minimal/maximal inputs (e.g., empty string, zero tokens, large arrays).
     - **Duplicate detection**: Inputs with duplicates, if applicable (e.g., repeated email domains, identical `asym_ids`).
     - **Type boundary cases**: Inputs at type or value boundaries (e.g., max integer, complex regex patterns).
     - **Error handling cases**: Inputs that may trigger exceptions, if `func0` handles errors explicitly (otherwise, omit).
   - Use the Testcase Generator’s strategies and `@example` cases to guide input generation, ensuring coverage of all branches.

4. **Output Format (JSON)**:
   - Structure the output as:
     ```json
     {
         "Normal cases": [
             {
                 "Description": "string",
                 "Inputs": {
                     "param1": value,
                     "param2": value,
                     ...
                 }
             },
             ...
         ],
         "Others": [
             {
                 "Description": "string",
                 "Inputs": {
                     "param1": value,
                     "param2": value,
                     ...
                 }
             },
             ...
         ]
     }
     ```
   - Place typical inputs in `"Normal cases"` (2-4 cases).
   - Place edge cases, duplicate detection, type boundary, and error handling cases in `"Others"` (3-6 cases).
   - Ensure all inputs are JSON-serializable (e.g., NumPy arrays as `list`, no `np.ndarray` objects).

5. **Generation Guidelines**:
   - Analyze `func0`’s signature, docstring, and logic to understand input requirements.
   - Use Hypothesis strategies (e.g., `st.integers(min_value=0, max_value=10)`, `text_strategy`) to determine valid input ranges and types.
   - Reference `@example` cases to include critical scenarios (e.g., empty inputs, specific patterns).
   - Ensure inputs trigger all branches of `func0`, as defined in the Testcase Generator.
   - For NumPy-based functions, generate arrays matching strategy shapes and dtypes, converted to `list`.
   - For re-based functions, generate strings with valid/invalid patterns matching the regex.
   - Avoid generating inputs that violate `func0`’s constraints (e.g., mismatched array shapes).

6. **Note**:
   - Generate exactly 5-10 test cases (2-4 Normal, 3-6 Others) to balance coverage and conciseness.
   - Ensure inputs support differential testing (valid for both `func0` and tested implementation).
   - Only return the JSON object, with no additional explanations or comments.

7. **Example**:

#### Input Testcase Generator:
```python
from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False

# Ground truth function
def extract_email_domains(text: str) -> list[str]:
    email_pattern = r'[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    matches = re.findall(email_pattern, text)
    return sorted(list(set(matches)))

# Strategy for generating text with potential email addresses
def text_strategy():
    domain = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.'),
        min_size=3, max_size=15
    ).map(lambda s: s + '.' + st.sampled_from(['com', 'org', 'net', 'edu']).example())
    username = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='._%+-'),
        min_size=1, max_size=10
    )
    email = st.builds(
        lambda u, d: f"{u}@{d}",
        username, domain
    )
    return st.lists(
        st.one_of(
            email,
            st.text(alphabet=st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=0, max_size=20)
        ),
        min_size=0, max_size=10
    ).map(lambda x: ' '.join(x))

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(text=text_strategy())
@example(text="")
@example(text="user@gmail.com")
@example(text="alice@yahoo.com bob@gmail.com")
@example(text="no.emails@invalid user@domain.com")
@example(text="user.name@sub.domain.org other@domain.net")
@example(text="random text without emails")
def test_extract_email_domains(text: str):
    global stop_collecting
    if stop_collecting:
        return
    text_copy = copy.deepcopy(text)
    try:
        expected = extract_email_domains(text_copy)
    except Exception:
        return
    generated_cases.append({
        "Inputs": {
            "text": text_copy
        }
    })
    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)
"""


REASONING_TESTCASE_GENERATION_PROMPT = """
You are an expert testing engineer specializing in generating reasoning-focused test cases for execution prediction tasks. Follow these guidelines:

Each test case must include:
1. **Test Case Structure**:
- Each test case must include:
* Input: The exact input parameters the function accepts

2. **Coverage Requirements** (Language Agnostic):
- Must cover these key scenarios:
a) Normal cases (typical inputs)
b) Edge cases (empty/minimal/maximal values)
c) Duplicate detection (if applicable)
d) Type boundary cases
e) Error handling cases (if applicable)

4. **Output Format** (JSON):
Put normal cases in "Normal cases" and others in "Others".
Follow this structure:
```json
{
    "Normal cases": [
        {
            "Description": "",
            "Inputs": {
              "html_string": ""
            }
        },
        ...
    ],
    "Others": [ 
        {
            "Description": "",
            "Inputs": {
              "html_string": ""
            }
        },
        ...
    ]
}
```
5. Note:
- Generate appropriate test cases covering all requirement categories 
- Only return JSON

6. **Example**:
Input:
# Ground Truth Function Example:
def is_palindrome(s: str) -> bool:
    return s == s[::-1]

Output:
{
    "Normal cases": [
        {
            "description": "Simple palindrome",
            "input": [
                {"s": "racecar"}
            ]
        }
    ],
    "Others": [
        {
            "description": "Non-palindrome",
            "input": [{"s": "hello"}]
        },
        {
            "description": "Empty string",
            "input": [{"s": ""}]
        }
    ]
}
"""

REASONING_CLASSIFICATION_PROMPT = """
**Role:** You are an experienced static code analysis expert, specializing in evaluating code feasibility for AI model execution prediction. Your task is not to execute code, but to analyze its structure and characteristics.

**Task:** Analyze the provided Python function source code to determine whether it is "suitable" or "unsuitable" for reliable, deterministic execution prediction by AI models (like large language models) given specific inputs.

**Core Objective:** Identify functions whose intrinsic properties make it difficult or impossible for AI models to precisely and deterministically trace their execution flow and predict final outputs. We want to filter out these functions to focus on those where AI models are more likely to successfully predict execution results.

**Evaluation Criteria (A function is "unsuitable" if it meets any of these conditions):**

1. **Excessive Control Flow Complexity:**
   * **Loop iterations:** Contains explicit loops with extremely large iterations (e.g., `range(1000)` or more); loops where iteration count depends on input and may become very large; deeply nested loops (3+ levels) making state tracking difficult.
   * **Recursion depth/complexity:** Recursive functions where depth may exceed 5 levels, or with complex/non-intuitive recursion logic.
   * **Dynamic termination:** Loops or logic with termination conditions that are hard to predict statically (e.g., complex calculations or input-dependent `break`/`continue`).

2. **Precision-Sensitive Math Operations:** Involves extensive floating-point operations requiring high precision (beyond basic arithmetic), or uses complex math library functions (e.g., advanced scientific computing) where language models may produce errors or fail to simulate.

3. **Randomness/Non-Determinism:** Explicit use of `random` module or other non-deterministic mechanisms (time-based seeds, hardware RNG, etc.).

4. **External State/Resource Dependence:** Function output depends on external environment/state inaccessible during model inference:
   * Filesystem operations (`open()`)
   * Network communication (`requests`, `socket`)
   * Database interactions
   * System time dependence (`datetime.now()`, `time.time()`)
   * Environment variables (`os.environ`)
   * OS/process interactions

5. **Complex Regular Expressions:** Uses very long (>20 chars) or sophisticated regex patterns (nested capture groups, lookarounds, complex backreferences) that challenge AI model comprehension.

6. **Complex/Dynamic Data Structures:** Processes deeply nested (>3 levels) lists/dictionaries, or structures that change unpredictably during runtime (dynamic key additions/deletions).

7. **Concurrency/Parallelism:** Uses `threading`, `multiprocessing`, or `asyncio`, introducing non-deterministic execution order or race conditions.

8. **Dynamic Code Execution:** Employs `eval()`, `exec()`, or similar mechanisms to execute dynamically generated code.

9. **Input-Sensitive Behavior:** Execution behavior (especially computational load, memory usage, or paths) changes drastically and unpredictably based on input characteristics, even if inputs aren't inherently complex (e.g., triggering worst-case algorithm scenarios).

10. **Third-Party Library Dependence or Non-Primitive Returns:**
    * Heavy reliance on specific third-party libraries (NumPy, Pandas, etc.) with opaque internal implementations or stateful objects requiring specialized knowledge.
    * Returns non-Python primitive types (NumPy arrays, DataFrames, custom class instances, special values like `-np.inf`) that complicate value representation/comparison.

**Output Requirements:**

1. First, provide a clear verdict: "**SUITABLE**" or "**UNSUITABLE**".
2. If "UNSUITABLE", you **must** list all violating reasons. For each:
   * Reference the relevant criterion number/description
   * Briefly explain how the function demonstrates this issue

## Input
You will receive Python function definitions to evaluate.

## Output
Return a JSON object with:
- "violations": list of rule violations
- "is_suitable": boolean

## Examples

### Example 1: Suitable Function
```python
def count_vowels(text: str) -> int:
    \"\"\"Count vowels in a string (a,e,i,o,u).\"\"\"
    vowels = {'a', 'e', 'i', 'o', 'u'}
    return sum(1 for char in text.lower() if char in vowels)
Analysis:
{
    "violations": [],
    "is_suitable": true
}
### Example 2: Unsuitable Function
```python
def process_matrix(data):
    \"\"\"Process nested matrix with random sampling.\"\"\"
    import numpy as np  # Violation
    result = []
    
    for row in data:
        if np.random.rand() > 0.5:  # Violation
            new_row = []
            for item in row:
                if isinstance(item, list):  # Violation (3-level nesting)
                    new_row.extend(item)
                else:
                    new_row.append(item)
            result.append(new_row)
    
    return np.array(result)  # Violation
```
Analysis:
{
    "violations": [
        "ExternalDeps-ThirdPartyLibrary(numpy)",
        "Structure-ExcessiveNesting(3 levels)",
        "Behavior-RandomOperation(np.random)",
        "ReturnType-NonNative(numpy.ndarray)"
    ],
    "is_suitable": false
}

## Note
- Be strict with recursion and nesting limits
- Only return json with "is_suitable" and "violations" keys
"""

REASONING_RUNNER_GENERATION_PROMPT = """
## Role: You are an expert Python developer specializing in test automation frameworks. Your task is to transform a normal test case runner into a specialized version that executes test cases and captures their outputs in JSON format.

## Input Requirements:
1. You will receive a Python file containing a normal test case runner implementation
2. The runner typically loads test cases from JSON and compares actual vs expected outputs

## Transformation Requirements:
1. Core Functionality Change:
- Convert from assertion-based testing to output-capture mode
- Remove all comparison logic (no more pass/fail checks)
- Store all actual outputs as "Expected" results in the output JSON

2. Output Specification:
- Create a global `results` dictionary with "Test cases" array
- Each executed case should append:
{
    "Inputs": original_inputs,
    "Expected": actual_output
}
- Final output should overwrite the input JSON file with enriched data

3. Ensure JSON compatibility  
- Ensure that all data types are JSON-compatible.
- Convert non-serializable types to JSON-compatible formats (`list`, `str`, `int`, etc.).
- Example: Convert `set()` to `list()`, `tuple()` to `list()`, etc.
   
## Example Transformation:
Input (Normal Runner):
```python
import json
import os
from groundtruth import fast_format_html as func1

# Configuration for loading test cases
TEST_CASE_DIR = os.path.abspath('test_cases')
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, 'test_cases.json')

# Function to load test cases from JSON
def load_test_cases_from_json():
    if not os.path.exists(TEST_CASE_FILE):
        print(f'JSON file not found: {TEST_CASE_FILE}')
        return []

    # Read the JSON file
    with open(TEST_CASE_FILE, 'r') as f:
        test_cases = json.load(f)

    return test_cases

# Function to run tests with loaded cases
def run_tests_with_loaded_cases(test_cases):
    for i, case in enumerate(test_cases):
        inputs = case['Inputs']
        expected_output = case['Expected']

        # Extract input parameter
        html_string = inputs['html_string']

        # Run the function under test
        actual_output = func1(html_string)

        # Check if the outputs match
        if actual_output != expected_output:
            print(f'Test case {i + 1} failed:')
            print(f'  Input: {html_string}')
            print(f'  Expected: {expected_output}')
            print(f'  Actual: {actual_output}')
        else:
            print(f'Test case {i + 1} passed.')

if __name__ == '__main__':
    # Load test cases from JSON
    test_cases = load_test_cases_from_json()
    run_tests_with_loaded_cases(test_cases)
```
## Output (Output Capture Runner):
```python
import json
import os
from groundtruth import fast_format_html as func1  # Preserve original import

# Change testcases filepath to reasoning_testcases.json
TEST_CASE_DIR = os.path.abspath('test_cases')
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, 'reasoning_testcases.json')
results = {"Test cases": []}  # New results container

def load_cases():
    with open(TEST_CASE_FILE) as f:
        return json.load(f)

def execute_cases(cases):
    for case in cases:
        actual = func1(**case['Inputs'])
        results['Test cases'].append({
            **case,
            'Expected': actual  # Capture instead of compare
        })

if __name__ == '__main__':
    test_cases = load_cases()
    execute_cases(test_cases['Test cases'])
    
    # Overwrite with enriched data
    with open(TEST_CASE_FILE, 'w') as f:
        json.dump(results, f, indent=2)

## Note:
- Only return the generated code in JSON format with "Runner" key.
- test_cases is a dict with "Test cases" key, not a list.
- Follow the style of the exmple code provided without any extra code.
"""