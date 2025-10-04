WEAKLY_SELF_CONTAINED_TESTCASES_GENERATOR_PROMPT = """
## Task Description
You are an expert Python developer specializing in property-based testing with the `hypothesis` library. Your task is to generate a **complete and executable Python test case generator script** for a given weakly self-contained Python function (`func0`, provided in the "Input" section). A weakly self-contained function depends only on standard libraries or specific external libraries (e.g., NumPy) and no other custom modules. The script will use `hypothesis` to:
1. Generate **high-quality, diverse test cases** that achieve **100% branch coverage** of `func0`, ensuring all code paths (including conditional branches, loops, and edge cases) are exercised.
2. Collect **exactly 500 test cases** that pass filtering conditions, using a global flag to stop collection once the target is reached.
3. Call `func0` with generated inputs to validate their effectiveness (e.g., no exceptions, triggers meaningful branches), but **only store input parameters** in test cases, omitting expected outputs, as correctness will be verified via differential testing (comparing `func0` outputs with a tested implementation during testing).
4. Save all collected test cases into a single JSON file upon script completion using the `atexit` module.

The generated script must include the following components:
1. **Import Statements**:
- Import required libraries: `hypothesis`, `hypothesis.strategies as st`, `hypothesis.extra.numpy` (for NumPy arrays), `numpy as np`, `json`, `os`, `atexit`, and `copy` for deep copying mutable inputs.
- Include only libraries necessary for `func0`’s dependencies (e.g., `numpy` for array operations).
2. **Ground Truth Function Definition**:
- Include the provided `func0` code directly in the script to validate inputs by computing outputs during generation.
3. **Configuration**:
- Define a directory path (`TEST_CASE_DIR`) for saving the output file, ensuring it exists using `os.makedirs(..., exist_ok=True)`.
- Define the output JSON filename (`test_cases.json`).
- Initialize a global list (`generated_cases`) to store test cases and a global flag (`stop_collecting`) to control case collection.
4. **Test Case Collection**:
- Each test case is a dictionary with a single key `"Inputs"` (a dictionary mapping argument names to JSON-serializable values, e.g., `int`, `list[int]`, `list[list[list[float]]]` for NumPy arrays).
- Collect **exactly 500 test cases** by checking the length of `generated_cases` after appending each case and setting `stop_collecting = True` when 500 is reached.
- Call `func0` with generated inputs to verify their validity (e.g., no exceptions, triggers target branches), but do not store the output in the test case.
5. **Input Strategy Generation**:
- Analyze `func0`’s signature, type hints, and function body to design **targeted hypothesis strategies** that:
    - Cover all branches, including edge cases (e.g., empty arrays, boundary values, invalid inputs handled by the function).
    - Are tailored to the function’s logic (e.g., for a function processing NumPy arrays, generate `np.ndarray` with appropriate shapes and dtypes).
    - Ensure JSON-serializability (e.g., use `st.floats(allow_nan=False, allow_infinity=False)`, convert `np.ndarray` to `list` via `.tolist()`).
    - Avoid generating irrelevant inputs by constraining strategies to meaningful ranges or patterns based on `func0`’s behavior.
- For NumPy arrays, use `hypothesis.extra.numpy.arrays` with appropriate `dtype` (e.g., `np.int32`, `np.float32`) and shapes derived from `func0`’s requirements.
- For dynamic shapes (e.g., arrays dependent on an integer argument), use `st.builds` to bind strategies to other inputs.
- **Maximize Branch Coverage**: Design strategies to achieve 100% branch coverage without relying on manual test cases, unless specific branches are exceptionally difficult to cover.
6. **Hypothesis Test Function (`@given(...)`)**:
- Define a test function decorated with `@given(...)`, mapping strategies to `func0`’s arguments.
- Use `@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)` to ensure enough attempts to collect 500 valid cases after filtering.
- Inside the test function:
    - Check `stop_collecting` at the start; if `True`, return to skip further collection.
    - Handle input modification by making deep copies of mutable inputs (e.g., NumPy arrays, lists) using `copy.deepcopy` to preserve original inputs.
    - Validate input constraints (e.g., array shapes match expected dimensions); skip invalid inputs using `return`.
    - Call `func0` with copied inputs to verify validity (e.g., no exceptions, triggers meaningful branches); if invalid (e.g., raises expected exceptions), skip using `return`.
    - Append `{"Inputs": {...}}` to `generated_cases`, converting non-serializable types (e.g., `np.ndarray`) to JSON-serializable forms (e.g., `array.tolist()`).
    - After appending, check if `len(generated_cases) >= 500`; if so, set `stop_collecting = True`.
- Add `@example` decorators for critical edge cases derived from `func0`’s logic (e.g., empty arrays, single-element arrays, multi-dimensional arrays) to ensure coverage of key scenarios.
7. **Manual Test Cases (Conditional)**:
- **Omit `manual_cases` if Hypothesis strategies achieve 100% branch coverage**, as verified by tools like `pytest-cov`.
- Only include `manual_cases` if specific branches are difficult to cover with random strategies (e.g., rare edge cases, complex array shapes). In such cases:
    - Provide a list of manual test cases (as dictionaries) covering these branches.
    - Append them to `generated_cases` after Hypothesis runs.
    - Ensure manual cases are executed via `@example` to guarantee coverage.
    - Include a comment explaining why `manual_cases` are necessary (e.g., `# Manual cases for rare array shapes not easily covered by Hypothesis`).
8. **Saving Test Cases**:
- Define a `save_test_cases` function that writes `generated_cases` to the JSON file using `json.dump(..., indent=2, ensure_ascii=False)`.
- Register it with `atexit.register(save_test_cases)` to save test cases once after all tests complete.
9. **Branch Coverage Guarantee**:
- Design strategies and optional `manual_cases` to ensure **100% branch coverage**, verifiable with `pytest-cov`. Analyze `func0`’s control flow (e.g., conditionals, loops, array indexing) to generate inputs that trigger each branch.
- Call `func0` to confirm inputs trigger specific branches; filter out inputs that do not contribute to coverage.
- For example, if `func0` processes NumPy arrays, include strategies generating empty, single-element, and multi-dimensional arrays.
10. **Complete and Executable Script**:
- Output a single, executable Python script that can be saved as a `.py` file and run directly.
- Ensure the script is minimal, avoiding unnecessary imports or logic, while being robust and maintainable.
11. **Differential Testing Support**:
- Since only inputs are stored, the test cases support differential testing, where inputs are passed to both `func0` (ground truth) and a tested implementation, and outputs are compared (e.g., using `np.allclose` for NumPy arrays with floating-point values).
- Calling `func0` during generation ensures inputs are valid and cover all branches, enhancing test case quality.

## Input
The Python code for the ground truth function `func0` is provided below:
```python
{func_code}

## Output
Generate a complete, executable Python code string for the test case generator script. For example:
```python
from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import json
import os
import atexit
import copy
# ... rest of the script ...

## Examples
Example 1: Chain Pair PDE Function
Input:
```python
import numpy as np

def chain_pair_pde(
    num_tokens: int, asym_ids: np.ndarray, full_pde: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    \"\"\"Compute predicted distance errors for all pairs of chains.

    Args:
      num_tokens: The number of tokens (not including padding).
      asym_ids: The asym_ids (array of shape num_tokens).
      full_pde: A [num_samples, num_tokens, num_tokens] matrix of predicted
        distance errors.

    Returns:
      chain_pair_pred_err_mean - a [num_samples, num_chains, num_chains] matrix with average
        per chain-pair predicted distance error.
      chain_pair_pred_err_min - a [num_samples, num_chains, num_chains] matrix with min
        per chain-pair predicted distance error.
    \"\"\"
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
```
Ouput:
```python
from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import hypothesis.extra.numpy as hnp
import numpy as np
import json
import os
import atexit
import copy
# Possiblely other imports based on func0's dependencies, e.g., typing

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

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
            st.integers(min_value=1, max_value=3),  # num_samples
            st.just(num_tokens),                     # num_tokens
            st.just(num_tokens)                      # num_tokens
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

    # Validate input shapes
    if len(asym_ids) != num_tokens or full_pde.shape[1:] != (num_tokens, num_tokens):
        return

    # Deep copy inputs to avoid modification
    num_tokens_copy = num_tokens
    asym_ids_copy = copy.deepcopy(asym_ids)
    full_pde_copy = copy.deepcopy(full_pde)

    # Call func0 to verify input validity
    try:
        expected_mean, expected_min = chain_pair_pde(num_tokens_copy, asym_ids_copy, full_pde_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "num_tokens": num_tokens_copy,
            "asym_ids": asym_ids_copy.tolist(),
            "full_pde": full_pde_copy.tolist()
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
```
Example 2: Extract Email Domains Function
Input:
```python
import re

def extract_email_domains(text: str) -> list[str]:
    \"\"\"Extract unique email domains from a text string.

    Args:
        text: A string containing potential email addresses.

    Returns:
        A sorted list of unique email domains (e.g., ['gmail.com', 'yahoo.com']).
    \"\"\"
    email_pattern = r'[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    matches = re.findall(email_pattern, text)
    return sorted(list(set(matches)))
```
Output:
```python
from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
import re
import json
import os
import atexit
import copy
# Possiblely other imports based on func0's dependencies, e.g., typing

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []
stop_collecting = False  # Global flag to control case collection

# Ground truth function
def extract_email_domains(text: str) -> list[str]:
    email_pattern = r'[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    matches = re.findall(email_pattern, text)
    return sorted(list(set(matches)))

# Strategy for generating text with potential email addresses
def text_strategy():
    # Generate domains (e.g., gmail.com, sub.domain.org)
    domain = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='.'),
        min_size=3, max_size=15
    ).map(lambda s: s + '.' + st.sampled_from(['com', 'org', 'net', 'edu']).example())
    
    # Generate usernames (e.g., user123, name.surname)
    username = st.text(
        alphabet=st.characters(whitelist_categories=('L', 'N'), whitelist_characters='._%+-'),
        min_size=1, max_size=10
    )
    
    # Combine into email addresses or random text
    email = st.builds(
        lambda u, d: f"{u}@{d}",
        username, domain
    )
    
    # Mix emails with random text
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

    # Deep copy input to avoid modification
    text_copy = copy.deepcopy(text)

    # Call func0 to verify input validity
    try:
        expected = extract_email_domains(text_copy)
    except Exception:
        return  # Skip inputs that cause exceptions

    # Store inputs only
    generated_cases.append({
        "Inputs": {
            "text": text_copy
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
```
## Note
- Exactly 500 Test Cases: Use a global stop_collecting flag to ensure exactly 500 test cases are collected, stopping further collection without throwing exceptions to avoid pytest failures.
- High-Quality Test Cases: Call func0 to validate inputs, filtering out those that cause exceptions or do not trigger meaningful branches, ensuring high-quality test cases.
- 100% Branch Coverage: Design strategies to achieve 100% branch coverage, verifiable with pytest-cov. Only include manual_cases if specific branches are difficult to cover, with a comment explaining their necessity.
- Targeted Strategies: Design strategies based on func0’s logic, using hypothesis.extra.numpy for NumPy arrays with appropriate dtype and shapes.
- Executable Code: Ensure the script is complete, executable, and minimal.
- max_examples=10000: Use 10000 examples to ensure enough attempts to collect 500 valid cases after filtering.
- JSON Output: Save test cases in a structured JSON format with only "Inputs", using atexit.
- Differential Testing: Test cases support differential testing by providing inputs to both func0 and a tested implementation, comparing outputs (e.g., with np.allclose for NumPy arrays).
- Weakly Self-Contained: Support functions depending on standard libraries or specific external libraries (e.g., NumPy), with no other dependencies.
- Input Validation: Call func0 during generation to ensure inputs are valid and cover all branches, but only store inputs in JSON for differential testing.
- Don't Forget: Import any necessary libraries, e.g., `typing` for type hints if used in func0.
- Only Return Code: Output only the Python code string, without explanations or additional comments.
"""

TESTCASES_GENERATOR_PROMPT_JAVA = """
## Task Description

You are an expert Java developer specializing in property-based testing and automated test case generation. Your task is to generate a **complete and executable Java test case generator script** for a given Java function (`func0`). This function is located in an external class `p_n.Tested` and will be provided in the "Input" section. The script will use the **jqwik** property-based testing framework to:

1.  Generate **high-quality, diverse test cases** that aim for **100% branch coverage** of `func0`, ensuring all code paths (including conditional branches, loops, and edge cases) are exercised.
2.  Collect **exactly 500 test cases** that pass any necessary filtering conditions. A global counter must be used to stop collection once this target is reached.
3.  Execute the external `GroundTruth.func0()` with the generated inputs to determine the expected output.
4.  Save all collected test cases into a single JSON file in a standardized test directory upon script completion.

The generated script must adhere to the following structure and requirements:

### 1. Import Statements
- Import required libraries:
  - jqwik (`net.jqwik.api.*`, `net.jqwik.api.lifecycle.*`)
  - JSON serialization (`com.google.gson.*`)
  - Standard Java utilities (`java.io.*`, `java.util.*`, `java.util.concurrent.atomic.*`)
  - **Crucially, import the `GroundTruth` class from its package (e.g., `p1.GroundTruth`, `p_n.GroundTruth`).** The specific package `p_n` will be contextually derived from the input.

### 2. External Ground Truth Function
- The ground truth function `func0` is **NOT** to be defined within the test class.
- It is located in a separate, pre-existing class named `GroundTruth`.
- The test script must call this function statically: `GroundTruth.func0(...)`.

### 3. Configuration
- Define the output directory path as `src/test/java/test_cases`, ensuring it is created if it doesn't exist.
- Define the output filename as `test_cases.json`.
- Initialize a global list to store test cases and a global `AtomicInteger` counter to control case collection up to `MAX_CASES = 500`.

### 4. Test Case Data Structure
- Use a simple inner class `TestCase` to structure each test case, containing an `Inputs` map and an `Expected` object.

### 5. Input Strategy Generation (`@Provide`)
- Analyze `func0`'s signature and logic to design **targeted jqwik `Arbitrary` generators**.
- These generators must be robust enough to cover all branches and edge cases (e.g., nulls, empty collections, boundary values).
- **Enforce cross-language numeric safety**:
  - Integers: Default to the 32-bit signed range (`-2147483648` to `2147483647`).
  - Floats: Use 32-bit float values, avoiding NaN/Infinity unless specifically required.
- For complex inputs (e.g., nested structures), use recursive generators or combinators.
- **Access Modifier**: Use package-private access for `@Provide` methods (e.g., `Arbitrary<Integer> int32()`).

### 6. Property-Based Test Method (`@Property`)
- Define a property-based test method that maps the provided arbitraries to `func0`'s arguments.
- Set a high number of `tries` (e.g., 10000) to ensure enough valid cases can be found.
- **For functions with strong semantic constraints or branches that are hard to cover with random generation, you MUST add explicit `@Example` annotations to guarantee coverage.**  
  - Each `@Example` should provide concrete arguments that trigger specific branches or edge cases.
  - The combination of property-based and example-based tests must guarantee 100% branch coverage.
- Inside the test method:
  - Immediately return if the collection target (`MAX_CASES`) has been met.
  - Wrap the call to `GroundTruth.func0()` in a `try-catch` block to handle potential exceptions gracefully.
  - **Optionally**, add filtering logic to only store test cases that cover distinct, meaningful branches.
  - If a valid case is generated, store it in the global list and increment the counter.
- **Access Modifier**: Use package-private access for the `@Property` method (e.g., `void generateTestCases(...)`).

### 7. Saving Test Cases (`@AfterContainer`)
- Define a static, package-private method annotated with `@AfterContainer` to handle file writing.
- This method will serialize the list of collected test cases to the specified JSON file (`src/test/java/test_cases/test_cases.json`) using the Gson library.
- Ensure the output JSON is pretty-printed for readability.

### 8. Complete and Executable Script
- The final output must be a single, complete, and executable Java file that can be run as a jqwik test.
- The script should be minimal, robust, and follow modern Java conventions.
- **Manual test cases (`@Example`) are required only if random generation is insufficient for full coverage.**

---

## Input
The Java code for the ground truth function `func0` is provided below. Assume this code resides in `p_n/src/main/java/p_n/GroundTruth.java`.
```java
public static int func0(int x, int y) {
    if (x > 0 && y > 0) {
        return x + y;
    } else if (x < 0 && y < 0) {
        return x - y;
    } else {
        return x * y;
    }
}
```

## Output Example
```java
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import net.jqwik.api.*;
import net.jqwik.api.lifecycle.AfterContainer;
import p1.GroundTruth;

public class TestCaseGenerator {

    static class TestCase {
        Map<String, Object> Inputs;
        Object Expected;
        TestCase(Map<String, Object> inputs, Object expected) {
            this.Inputs = inputs;
            this.Expected = expected;
        }
    }

    static List<TestCase> generatedCases = new ArrayList<>();
    static AtomicInteger caseCount = new AtomicInteger(0);
    static final int MAX_CASES = 500;

    @Property(tries = 10000)
    @Example(1, 1)
    @Example(-2, -3)
    @Example(0, 0)
    void generateTestCases(@ForAll("int32") int x, @ForAll("int32") int y) {
        if (caseCount.get() >= MAX_CASES) {
            return;
        }

        int result;
        try {
            result = GroundTruth.func0(x, y);
        } catch (Exception e) {
            return;
        }

        boolean isPositiveBranch = x > 0 && y > 0;
        boolean isNegativeBranch = x < 0 && y < 0;
        boolean isElseBranch = !isPositiveBranch && !isNegativeBranch;
        if (!isPositiveBranch && !isNegativeBranch && !isElseBranch) {
            return;
        }

        Map<String, Object> inputs = new LinkedHashMap<>();
        inputs.put("x", x);
        inputs.put("y", y);
        generatedCases.add(new TestCase(inputs, result));
        caseCount.incrementAndGet();
    }

    @Provide
    Arbitrary<Integer> int32() {
        return Arbitraries.integers().between(-2147483648, 2147483647);
    }

    @AfterContainer
    static void saveTestCases() throws IOException {
        if (generatedCases.isEmpty()) {
            return;
        }
        String dirPath = "src/test/java/test_cases";
        File dir = new File(dirPath);
        if (!dir.exists()) {
            dir.mkdirs();
        }
        String filePath = dirPath + "/test_cases.json";
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        try (Writer writer = new FileWriter(filePath)) {
            gson.toJson(generatedCases, writer);
        }
        System.out.println("✅ Saved " + generatedCases.size() + " test cases to " + filePath);
    }
}
```

# Note
- Only return the Java code string without explanations or additional comments.
- Don't forget to include the necessary imports and ensure the script is executable as a jqwik test.
- **If the function under test contains branches that are hard to cover with random generation, you MUST add explicit `@Example` annotations to guarantee full branch coverage.**
"""

TESTCASES_GENERATOR_PROMPT_JAVA_V1 = """## Task Description
You are an expert Java developer specializing in property-based testing and automated test case generation. Your task is to generate a **complete and executable Java test case generator script** for a given Java function (`func0`). This function is located in an external class `p_n.Tested` and will be provided in the "Input" section. The script will use the **jqwik** property-based testing framework to:

1.  Generate **high-quality, diverse test cases** that aim for **100% branch coverage** of `func0`, ensuring all code paths (including conditional branches, loops, and edge cases) are exercised.
2.  Collect **exactly 500 test cases** that pass any necessary filtering conditions. A global counter must be used to stop collection once this target is reached.
3.  Execute the external `GroundTruth.func0()` with the generated inputs to determine the expected output.
4.  Save all collected test cases into a single JSON file in a standardized test directory upon script completion.

The generated script must adhere to the following structure and requirements:

### 1. Import Statements
- Import required libraries:
  - jqwik (`net.jqwik.api.*`, `net.jqwik.api.lifecycle.*`)
  - JSON serialization (`com.google.gson.*`)
  - Standard Java utilities (`java.io.*`, `java.util.*`, `java.util.concurrent.atomic.*`)
  - **Crucially, import the `GroundTruth` class from its package (e.g., `p1.GroundTruth`, `p_n.GroundTruth`).** The specific package `p_n` will be contextually derived from the input.

### 2. External Ground Truth Function
- The ground truth function `func0` is **NOT** to be defined within the test class.
- It is located in a separate, pre-existing class named `GroundTruth`.
- The test script must call this function statically: `GroundTruth.func0(...)`.

### 3. Configuration
- Define the output directory path as `src/test/java/test_cases`, ensuring it is created if it doesn't exist.
- Define the output filename as `test_cases.json`.
- Initialize a global list to store test cases and a global `AtomicInteger` counter to control case collection up to `MAX_CASES = 500`.

### 4. Test Case Data Structure
- Use a simple inner class `TestCase` to structure each test case, containing an `Inputs` map and an `Expected` object.

### 5. Input Strategy Generation (`@Provide`)
- Analyze `func0`'s signature and logic to design **targeted jqwik `Arbitrary` generators**.
- These generators must be robust enough to cover all branches and edge cases (e.g., nulls, empty collections, boundary values).
- **Enforce cross-language numeric safety**:
  - Integers: Default to the 32-bit signed range (`-2147483648` to `2147483647`).
  - Floats: Use 32-bit float values, avoiding NaN/Infinity unless specifically required.
- For complex inputs (e.g., nested structures), use recursive generators or combinators.
- **Access Modifier**: Use package-private access for `@Provide` methods (e.g., `Arbitrary<Integer> int32()`).

### 6. Property-Based Test Method (`@Property`)
- Define a property-based test method that maps the provided arbitraries to `func0`'s arguments.
- Set a high number of `tries` (e.g., 10000) to ensure enough valid cases can be found.
- Inside the test method:
  - Immediately return if the collection target (`MAX_CASES`) has been met.
  - Wrap the call to `GroundTruth.func0()` in a `try-catch` block to handle potential exceptions gracefully.
  - **Optionally**, add filtering logic to only store test cases that cover distinct, meaningful branches.
  - If a valid case is generated, store it in the global list and increment the counter.
- **Access Modifier**: Use package-private access for the `@Property` method (e.g., `void generateTestCases(...)`).

### 7. Saving Test Cases (`@AfterContainer`)
- Define a static, package-private method annotated with `@AfterContainer` to handle file writing.
- This method will serialize the list of collected test cases to the specified JSON file (`src/test/java/test_cases/test_cases.json`) using the Gson library.
- Ensure the output JSON is pretty-printed for readability.

### 8. Complete and Executable Script
- The final output must be a single, complete, and executable Java file that can be run as a jqwik test.
- The script should be minimal, robust, and follow modern Java conventions. Omit manual test cases (`@Example`) unless random generation is insufficient for full coverage.

---

## Input
The Java code for the ground truth function `func0` is provided below. Assume this code resides in `p_n/src/main/java/p_n/GroundTruth.java`.
```java
public static int func0(int x, int y) {
    if (x > 0 && y > 0) {
        return x + y;
    } else if (x < 0 && y < 0) {
        return x - y;
    } else {
        return x * y;
    }
}
```

## Output Example
```java
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import net.jqwik.api.*;
import net.jqwik.api.lifecycle.AfterContainer;
// The package 'p1' is used here as an example for 'p_n'.
import p1.GroundTruth;

public class TestCaseGenerator {

    static class TestCase {
        Map<String, Object> Inputs;
        Object Expected;
        TestCase(Map<String, Object> inputs, Object expected) {
            this.Inputs = inputs;
            this.Expected = expected;
        }
    }

    static List<TestCase> generatedCases = new ArrayList<>();
    static AtomicInteger caseCount = new AtomicInteger(0);
    static final int MAX_CASES = 500;

    @Property(tries = 10000)
    void generateTestCases(@ForAll("int32") int x, @ForAll("int32") int y) {
        if (caseCount.get() >= MAX_CASES) {
            return;
        }

        int result;
        try {
            result = GroundTruth.func0(x, y);
        } catch (Exception e) {
            // Skip cases that throw an exception, as they are not the target for generation.
            return;
        }

        // Optional: Filter to collect only cases that cover distinct branches.
        boolean isPositiveBranch = x > 0 && y > 0;
        boolean isNegativeBranch = x < 0 && y < 0;
        boolean isElseBranch = !isPositiveBranch && !isNegativeBranch;
        if (!isPositiveBranch && !isNegativeBranch && !isElseBranch) {
             // This condition should not be met, but acts as a safeguard.
             return;
        }

        Map<String, Object> inputs = new LinkedHashMap<>();
        inputs.put("x", x);
        inputs.put("y", y);
        generatedCases.add(new TestCase(inputs, result));
        caseCount.incrementAndGet();
    }

    @Provide
    Arbitrary<Integer> int32() {
        return Arbitraries.integers().between(-2147483648, 2147483647);
    }

    @AfterContainer
    static void saveTestCases() throws IOException {
        if (generatedCases.isEmpty()) {
            return;
        }
        String dirPath = "src/test/java/test_cases";
        File dir = new File(dirPath);
        if (!dir.exists()) {
            dir.mkdirs();
        }
        String filePath = dirPath + "/test_cases.json";
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        try (Writer writer = new FileWriter(filePath)) {
            gson.toJson(generatedCases, writer);
        }
        System.out.println("✅ Saved " + generatedCases.size() + " test cases to " + filePath);
    }
}
```
# Note
- Only return the Java code string without explanations or additional comments.
- Don't forget to include the necessary imports and ensure the script is executable as a jqwik test.
"""

TESTCASES_GENERATOR_PROMPT_JAVA_V0 = """## Task Description
You are an expert Java developer specializing in property-based testing and automated test case generation. Your task is to generate a **complete and executable Java test case generator script** for a given Java function (`func0`, provided in the "Input" section). The script will use the **jqwik** property-based testing framework to:

1. Generate **high-quality, diverse test cases** that achieve **100% branch coverage** of `func0`, ensuring all code paths (including conditional branches, loops, and edge cases) are exercised.
2. Collect **exactly 500 test cases** that pass filtering conditions, using a global flag or counter to stop collection once the target is reached.
3. Execute `func0` with the generated inputs to determine the expected output.
4. Save all collected test cases into a single JSON file upon script completion.

The generated script must include the following components:

### 1. Import Statements
- Import required libraries:  
  - jqwik (`net.jqwik.api.*`, `net.jqwik.api.lifecycle.*`)
  - JSON serialization (e.g., `com.google.gson.*`)
  - File I/O (`java.io.*`)
  - Collections (`java.util.*`)
  - Any others needed by `func0`

### 2. Ground Truth Function Definition
- Include the provided `func0` code directly in the script to compute expected outputs.

### 3. Configuration
- Define a directory path for saving the output file, ensuring it exists.
- Define the output JSON filename (e.g., `test_cases.json`).
- Initialize a global list to store test cases and a global flag/counter to control case collection.

### 4. Test Case Collection
- Each test case is a JSON object with keys `"Inputs"` (a map of argument names to values) and `"Expected"` (the output from `func0`).
- Collect **exactly 500 test cases** by checking the length of the list after appending each case and stopping further collection when 500 is reached.

### 5. Input Strategy Generation
- Analyze `func0`'s signature, type hints, and function body to design **targeted jqwik generators** that:
  - Cover all branches, including edge cases (e.g., empty inputs, boundary values, invalid inputs handled by the function).
  - Are tailored to the function’s logic (e.g., for a function merging JSON-like objects, generate nested maps and lists; for a function handling code indentation, generate strings mimicking Java code).
  - Ensure JSON-serializability (e.g., use only types that can be serialized to JSON).
  - Avoid generating irrelevant inputs by constraining generators to meaningful ranges or patterns based on `func0`’s behavior.
  - **Enforce cross-language numeric safety**:
    - Integers: Use range **-2147483648 to 2147483647** (32-bit signed) unless function explicitly requires larger values.
    - Floats: Use 32-bit float values, avoiding NaN and Infinity unless required.
  - For complex inputs (e.g., nested maps or lists), use recursive generators or combinators to generate specific patterns.
  - **Maximize Branch Coverage**: Design generators to achieve 100% branch coverage without relying on manual test cases, unless specific branches are exceptionally difficult to cover.

### 6. Property-Based Test Function
- Define a property-based test function using jqwik, mapping generators to `func0`’s arguments.
- Configure the test to run enough examples to collect 500 valid cases after filtering.
- Inside the test function:
  - Check the global flag/counter at the start; if the target is reached, skip further collection.
  - Call `func0` with the generated inputs and store the result as `expected_output`.
  - Append `{"Inputs": {...}, "Expected": expected_output}` to the list if the case passes filtering conditions (e.g., triggers meaningful branches).
  - After appending, check if the target is reached; if so, set the flag/counter.
  - Optionally include basic type checks on `expected_output` to ensure validity.
- Add explicit edge case examples if needed to ensure coverage of key scenarios.

### 7. Manual Test Cases (Conditional)
- **Omit manual cases if generators achieve 100% branch coverage**, as verified by tools like JaCoCo.
- Only include manual cases if specific branches are difficult to cover with random generators.

### 8. Saving Test Cases
- Define a function that writes the collected test cases to the JSON file using a JSON library.
- Ensure the file is saved once after all tests complete (e.g., using `@AfterContainer`).

### 9. Branch Coverage Guarantee
- Design generators and optional manual cases to ensure **100% branch coverage**, verifiable with JaCoCo or similar tools.

### 10. Complete and Executable Script
- Output a single, executable Java file (JUnit/jqwik test class) that can be run directly.
- Ensure the script is minimal, robust, and maintainable.

---

## Input
The Java code for the ground truth function `func0` is provided below:
```java
public static int func0(int x, int y) {
    if (x > 0 && y > 0) {
        return x + y;
    } else if (x < 0 && y < 0) {
        return x - y;
    } else {
        return x * y;
    }
}
```

## Output Example

```java
import net.jqwik.api.*;
import net.jqwik.api.lifecycle.*;
import com.google.gson.*;
import java.io.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger

public class TestCaseGenerator {

    static class TestCase {
        Map<String, Object> Inputs;
        Object Expected;
        TestCase(Map<String, Object> inputs, Object expected) {
            this.Inputs = inputs;
            this.Expected = expected;
        }
    }

    static List<TestCase> generatedCases = new ArrayList<>();
    static AtomicInteger caseCount = new AtomicInteger(0);
    static final int MAX_CASES = 500;

    // Ground truth function
    public static int func0(int x, int y) {
        if (x > 0 && y > 0) {
            return x + y;
        } else if (x < 0 && y < 0) {
            return x - y;
        } else {
            return x * y;
        }
    }

    @Property(tries = 10000)
    public void generateTestCases(@ForAll("int32") int x, @ForAll("int32") int y) {
        if (caseCount.get() >= MAX_CASES) return;
        int result;
        try {
            result = func0(x, y);
        } catch (Exception e) {
            return;
        }
        // Only collect meaningful branch-coverage cases
        boolean meaningful = (x > 0 && y > 0) || (x < 0 && y < 0) || (x * y == result);
        if (!meaningful) return;

        Map<String, Object> inputs = new LinkedHashMap<>();
        inputs.put("x", x);
        inputs.put("y", y);
        generatedCases.add(new TestCase(inputs, result));
        caseCount.incrementAndGet();
    }

    @Provide
    public Arbitrary<Integer> int32() {
        return Arbitraries.integers().between(-2147483648, 2147483647);
    }

    @AfterContainer
    public static void saveTestCases() throws IOException {
        if (generatedCases.isEmpty()) return;
        String dir = "test_cases";
        new File(dir).mkdirs();
        String file = dir + "/test_cases.json";
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        try (Writer writer = new FileWriter(file)) {
            gson.toJson(generatedCases, writer);
        }
        System.out.println("✅ Saved " + generatedCases.size() + " test cases to " + file);
    }
}
```"""

TESTCASES_GENERATOR_PROMPT = """
## Task Description
You are an expert Python developer specializing in property-based testing with the `hypothesis` library. Your task is to generate a **complete and executable Python test case generator script** for a given Python function (`func0`, provided in the "Input" section). The script will use `hypothesis` to:
1. Generate **high-quality, diverse test cases** that achieve **100% branch coverage** of `func0`, ensuring all code paths (including conditional branches, loops, and edge cases) are exercised.
2. Collect **exactly 500 test cases** that pass filtering conditions, using a global flag to stop collection once the target is reached.
3. Execute `func0` with the generated inputs to determine the expected output.
4. Save all collected test cases into a single JSON file upon script completion using the `atexit` module.

The generated script must include the following components:
1. **Import Statements**:
   - Import required libraries: `hypothesis`, `hypothesis.strategies as st`, `json`, `os`, `atexit`, and optionally `typing`, `copy`, or others needed by `func0`.
2. **Ground Truth Function Definition**:
   - Include the provided `func0` code directly in the script to compute expected outputs.
3. **Configuration**:
   - Define a directory path (`TEST_CASE_DIR`) for saving the output file, ensuring it exists using `os.makedirs(..., exist_ok=True)`.
   - Define the output JSON filename (`test_cases.json`).
   - Initialize a global list (`generated_cases`) to store test cases and a global flag (`stop_collecting`) to control case collection.
4. **Test Case Collection**:
   - Each test case is a dictionary with keys `"Inputs"` (a dictionary mapping argument names to values) and `"Expected"` (the output from `func0`).
   - Collect **exactly 500 test cases** by checking the length of `generated_cases` after appending each case and setting `stop_collecting = True` when 500 is reached.
5. **Input Strategy Generation**:
   - Analyze `func0`'s signature, type hints, and function body to design **targeted hypothesis strategies** that:
     - Cover all branches, including edge cases (e.g., empty inputs, boundary values, invalid inputs handled by the function).
     - Are tailored to the function’s logic (e.g., for a function merging JSON-like objects, generate nested dictionaries and lists; for a function handling code indentation, generate strings mimicking Python code).
     - Ensure JSON-serializability (e.g., use `st.floats(allow_nan=False, allow_infinity=False)`, printable strings via `st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')))`).
     - Avoid generating irrelevant inputs by constraining strategies to meaningful ranges or patterns based on `func0`’s behavior.
   - **Enforce cross-language numeric safety**:
     - Integers: Use range **-2147483648 to 2147483647** (32-bit signed) unless function explicitly requires larger values
     - Floats: Use `st.floats(allow_nan=False, allow_infinity=False, width=32)` for 32-bit compatibility
   - For complex inputs (e.g., nested dictionaries or lists), use recursive strategies (e.g., `st.recursive`) or `st.one_of` to generate specific patterns.
   - **Maximize Branch Coverage**: Design strategies to achieve 100% branch coverage without relying on manual test cases, unless specific branches are exceptionally difficult to cover.
6. **Hypothesis Test Function (`@given(...)`)**:
   - Define a test function decorated with `@given(...)`, mapping strategies to `func0`’s arguments.
   - Use `@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)` to ensure enough attempts to collect 500 valid cases after filtering.
   - Inside the test function:
     - Check `stop_collecting` at the start; if `True`, return to skip further collection.
     - Handle input modification by making deep copies of mutable inputs (e.g., lists, dicts) using `copy.deepcopy` (import `copy` if needed) to preserve original inputs.
     - Call `func0` with the copied inputs and store the result as `expected_output`.
     - Append `{"Inputs": {...}, "Expected": expected_output}` to `generated_cases` if the case passes filtering conditions (e.g., triggers meaningful branches).
     - After appending, check if `len(generated_cases) >= 500`; if so, set `stop_collecting = True`.
     - Optionally include basic type checks on `expected_output` to ensure validity.
   - Add `@example` decorators for critical edge cases derived from `func0`’s logic (e.g., empty dictionaries, single-element lists) to ensure coverage of key scenarios.
7. **Manual Test Cases (Conditional)**:
   - **Omit `manual_cases` if Hypothesis strategies achieve 100% branch coverage**, as verified by tools like `pytest-cov`.
   - Only include `manual_cases` if specific branches are difficult to cover with random strategies (e.g., rare edge cases, complex nested conditions). In such cases:
     - Provide a list of manual test cases (as dictionaries) covering these branches.
     - Append them to `generated_cases` after Hypothesis runs.
     - Ensure manual cases are executed via `@example` to guarantee coverage.
     - Include a comment explaining why `manual_cases` are necessary (e.g., `# Manual cases for rare edge case not easily covered by Hypothesis`).
8. **Saving Test Cases**:
   - Define a `save_test_cases` function that writes `generated_cases` to the JSON file using `json.dump(..., indent=2, ensure_ascii=False)`.
   - Register it with `atexit.register(save_test_cases)` to save test cases once after all tests complete.
9. **Branch Coverage Guarantee**:
   - Design strategies and optional `manual_cases` to ensure **100% branch coverage**, verifiable with `pytest-cov`. Analyze `func0`’s control flow (e.g., conditionals, loops) to generate inputs that trigger each branch.
   - For example, if `func0` processes nested dictionaries, include strategies generating empty, single-key, and deeply nested dictionaries.
10. **Complete and Executable Script**:
    - Output a single, executable Python script that can be saved as a `.py` file and run directly.
    - Ensure the script is minimal, avoiding unnecessary imports or logic, while being robust and maintainable.

## Input
The Python code for the ground truth function `func0` is provided below:
```python
{func_code}

## Output
Generate a complete, executable Python code string for the test case generator script. For example:
```python
import hypothesis
import hypothesis.strategies as st
import json
# ... rest of the script ...
```
## Examples
### Example 1: Code Indentation Function
For an input function like:
```python
def _get_correct_indent_level(lines: List[str], line_index: int) -> str:
    if line_index > 0:
        prev_line = lines[line_index - 1].rstrip()
        if prev_line and not prev_line.endswith(","):
            return prev_line[: len(prev_line) - len(prev_line.lstrip())]
    for i in range(line_index - 1, -1, -1):
        line = lines[i].rstrip()
        if not line:
            continue
        curr_indent = line[: len(line) - len(line.lstrip())]
        if len(line) - len(line.lstrip()) >= 8:
            return line[: len(line) - len(line.lstrip())]
        if line.lstrip().startswith(("def ", "class ", "async def ")):
            return curr_indent + "  "
        if line.endswith(":"):
            return curr_indent + "  "
    return ""
```
The generated script might look like:
```python
from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []

# Ground truth function
def _get_correct_indent_level(lines: List[str], line_index: int) -> str:
    if line_index > 0:
        prev_line = lines[line_index - 1].rstrip()
        if prev_line and not prev_line.endswith(","):
            return prev_line[: len(prev_line) - len(prev_line.lstrip())]
    for i in range(line_index - 1, -1, -1):
        line = lines[i].rstrip()
        if not line:
            continue
        curr_indent = line[: len(line) - len(line.lstrip())]
        if len(line) - len(line.lstrip()) >= 8:
            return line[: len(line) - len(line.lstrip())]
        if line.lstrip().startswith(("def ", "class ", "async def ")):
            return curr_indent + "  "
        if line.endswith(":"):
            return curr_indent + "  "
    return ""

# Strategy for generating code-like lines
def line_strategy():
    return st.one_of([
        # Lines starting with def/class/async def
        st.tuples(
            st.text(st.characters(whitelist_categories=('Zs',)), max_size=16),
            st.one_of([st.just("def "), st.just("class "), st.just("async def ")]),
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1),
            st.one_of([st.just(":"), st.just(""), st.just(" # comment")])
        ).map(lambda x: "".join(x)),
        # Lines ending with colon
        st.tuples(
            st.text(st.characters(whitelist_categories=('Zs',)), max_size=16),
            st.text(st.characters(min_codepoint=33, max_codepoint=126), min_size=1),
            st.just(":")
        ).map(lambda x: "".join(x)),
        # Lines with 8+ spaces
        st.text(st.characters(whitelist_categories=('Zs',)), min_size=8, max_size=16),
        # Lines ending with comma
        st.tuples(
            st.text(st.characters(whitelist_categories=('Zs',)), max_size=16),
            st.text(st.characters(min_codepoint=33, max_codepoint=126), min_size=1),
            st.just(",")
        ).map(lambda x: "".join(x)),
        # Empty lines
        st.just(""),
        # Generic code lines
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    lines=st.lists(line_strategy(), min_size=1, max_size=20, unique=True),
    line_index=st.integers(min_value=0)
)
@example(lines=["    def func():"], line_index=0)
@example(lines=["class MyClass:", "    pass"], line_index=1)
@example(lines=["if condition:", "    value = 1"], line_index=1)
@example(lines=["    previous_line", "next_line"], line_index=1)
@example(lines=["previous_line,", "next_line"], line_index=1)
@example(lines=["        value = 1"], line_index=0)
@example(lines=["random_line"], line_index=0)
def test_get_correct_indent_level(lines: List[str], line_index: int):
    if line_index >= len(lines):
        line_index = len(lines) - 1
    
    lines_copy = copy.deepcopy(lines)
    try:
        expected = _get_correct_indent_level(lines_copy, line_index)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if len(lines) > 1 or any(
        line.lstrip().startswith(("def ", "class ", "async def ")) or
        line.endswith(":") or
        line.endswith(",") or
        len(line) - len(line.lstrip()) >= 8
        for line in lines
    ):
        generated_cases.append({
            "Inputs": {"lines": lines, "line_index": line_index},
            "Expected": expected
        })

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)
```
### Example 2: JSON Merge Function
For an input function like:
```python
def merge_json_recursive(base, update):
    \"\"\"Recursively merge two JSON-like objects.
    - Dictionaries are merged recursively
    - Lists are concatenated
    - Other types are overwritten by the update value

    Args:
        base: Base JSON-like object
        update: Update JSON-like object to merge into base

    Returns:
        Merged JSON-like object
    \"\"\"
    if not isinstance(base, dict) or not isinstance(update, dict):
        if isinstance(base, list) and isinstance(update, list):
            return base + update
        return update

    merged = base.copy()
    for key, value in update.items():
        if key in merged:
            merged[key] = merge_json_recursive(merged[key], value)
        else:
            merged[key] = value

    return merged
```
The generated script might look like:
```python
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
def merge_json_recursive(base, update):
    if not isinstance(base, dict) or not isinstance(update, dict):
        if isinstance(base, list) and isinstance(update, list):
            return base + update
        return update

    merged = base.copy()
    for key, value in update.items():
        if key in merged:
            merged[key] = merge_json_recursive(merged[key], value)
        else:
            merged[key] = value

    return merged

# Strategy for JSON-like objects
json_strategy = st.recursive(
    st.one_of([
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'))),
        st.booleans()
    ]),
    lambda children: st.one_of(
        st.lists(children, max_size=5),
        st.dictionaries(st.text(st.characters(whitelist_categories=('L', 'N')), max_size=5), children, max_size=5)
    ),
    max_leaves=5
)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(base=json_strategy, update=json_strategy)
@example(base={}, update={})
@example(base={"a": 1}, update={"a": 2})
@example(base=[1, 2], update=[3, 4])
@example(base={"a": {"b": 1}}, update={"a": {"c": 2}})
@example(base="string", update=42)
@example(base={"a": [1]}, update={"a": [2]})
def test_merge_json_recursive(base, update):
    global stop_collecting
    if stop_collecting:
        return
    
    base_copy = copy.deepcopy(base)
    update_copy = copy.deepcopy(update)
    try:
        expected = merge_json_recursive(base_copy, update_copy)
    except Exception:
        return  # Skip inputs that cause exceptions
    
    if isinstance(base, (dict, list)) or isinstance(update, (dict, list)):
        generated_cases.append({
            "Inputs": {"base": base, "update": update},
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
```
## Note
- Exactly 500 Test Cases: Use a global stop_collecting flag to ensure exactly 500 test cases are collected, stopping further collection without throwing exceptions to avoid pytest failures.
- High-Quality Test Cases: Filter test cases to prioritize those that exercise meaningful branches, avoiding redundant or irrelevant inputs.
- 100% Branch Coverage: Design strategies to achieve 100% branch coverage, verifiable with pytest-cov. Only include manual_cases if specific branches are difficult to cover, with a comment explaining their necessity.
- Targeted Strategies: Design strategies based on func0’s logic, not generic defaults.
- Executable Code: Ensure the script is complete, executable, and minimal.
- max_examples=10000: Use 10000 examples to ensure enough attempts to collect 500 valid cases after filtering.
- JSON Output: Save test cases in a structured JSON format using atexit.
- Only Return Code: Output only the Python code string, without explanations or additional comments.
"""

TESTCASES_GENERATOR_PROMPT_v3 = """
## Task Description
You are an expert Python developer specializing in property-based testing with the `hypothesis` library. Your task is to generate a **complete and executable Python test case generator script** for a given Python function (`func0`, provided in the "Input" section). The script will use `hypothesis` to:
1. Generate **high-quality, diverse test cases** that achieve **100% branch coverage** of `func0`, ensuring all code paths (including conditional branches, loops, and edge cases) are exercised.
2. Collect **exactly 500 test cases** that pass filtering conditions, using a global flag to stop collection once the target is reached.
3. Execute `func0` with the generated inputs to determine the expected output.
4. Save all collected test cases into a single JSON file upon script completion using the `atexit` module.

The generated script must include the following components:
1. **Import Statements**:
   - Import required libraries: `hypothesis`, `hypothesis.strategies as st`, `json`, `os`, `atexit`, and optionally `typing`, `copy`, or others needed by `func0`.
2. **Ground Truth Function Definition**:
   - Include the provided `func0` code directly in the script to compute expected outputs.
3. **Configuration**:
   - Define a directory path (`TEST_CASE_DIR`) for saving the output file, ensuring it exists using `os.makedirs(..., exist_ok=True)`.
   - Define the output JSON filename (`test_cases.json`).
   - Initialize a global list (`generated_cases`) to store test cases and a global flag (`stop_collecting`) to control case collection.
4. **Test Case Collection**:
   - Each test case is a dictionary with keys `"Inputs"` (a dictionary mapping argument names to values) and `"Expected"` (the output from `func0`).
   - Collect **exactly 500 test cases** by checking the length of `generated_cases` after appending each case and setting `stop_collecting = True` when 500 is reached.
5. **Input Strategy Generation**:
   - Analyze `func0`'s signature, type hints, and function body to design **targeted hypothesis strategies** that:
     - Cover all branches, including edge cases (e.g., empty inputs, boundary values, invalid inputs handled by the function).
     - Are tailored to the function’s logic (e.g., for a function merging JSON-like objects, generate nested dictionaries and lists; for a function handling code indentation, generate strings mimicking Python code).
     - Ensure JSON-serializability (e.g., use `st.floats(allow_nan=False, allow_infinity=False)`, printable strings via `st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')))`).
     - Avoid generating irrelevant inputs by constraining strategies to meaningful ranges or patterns based on `func0`’s behavior.
   - For complex inputs (e.g., nested dictionaries or lists), use recursive strategies (e.g., `st.recursive`) or `st.one_of` to generate specific patterns.
   - **Maximize Branch Coverage**: Design strategies to achieve 100% branch coverage without relying on manual test cases, unless specific branches are exceptionally difficult to cover.
6. **Hypothesis Test Function (`@given(...)`)**:
   - Define a test function decorated with `@given(...)`, mapping strategies to `func0`’s arguments.
   - Use `@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)` to ensure enough attempts to collect 500 valid cases after filtering.
   - Inside the test function:
     - Check `stop_collecting` at the start; if `True`, return to skip further collection.
     - Handle input modification by making deep copies of mutable inputs (e.g., lists, dicts) using `copy.deepcopy` (import `copy` if needed) to preserve original inputs.
     - Call `func0` with the copied inputs and store the result as `expected_output`.
     - Append `{"Inputs": {...}, "Expected": expected_output}` to `generated_cases` if the case passes filtering conditions (e.g., triggers meaningful branches).
     - After appending, check if `len(generated_cases) >= 500`; if so, set `stop_collecting = True`.
     - Optionally include basic type checks on `expected_output` to ensure validity.
   - Add `@example` decorators for critical edge cases derived from `func0`’s logic (e.g., empty dictionaries, single-element lists) to ensure coverage of key scenarios.
7. **Manual Test Cases (Conditional)**:
   - **Omit `manual_cases` if Hypothesis strategies achieve 100% branch coverage**, as verified by tools like `pytest-cov`.
   - Only include `manual_cases` if specific branches are difficult to cover with random strategies (e.g., rare edge cases, complex nested conditions). In such cases:
     - Provide a list of manual test cases (as dictionaries) covering these branches.
     - Append them to `generated_cases` after Hypothesis runs.
     - Ensure manual cases are executed via `@example` to guarantee coverage.
     - Include a comment explaining why `manual_cases` are necessary (e.g., `# Manual cases for rare edge case not easily covered by Hypothesis`).
8. **Saving Test Cases**:
   - Define a `save_test_cases` function that writes `generated_cases` to the JSON file using `json.dump(..., indent=2, ensure_ascii=False)`.
   - Register it with `atexit.register(save_test_cases)` to save test cases once after all tests complete.
9. **Branch Coverage Guarantee**:
   - Design strategies and optional `manual_cases` to ensure **100% branch coverage**, verifiable with `pytest-cov`. Analyze `func0`’s control flow (e.g., conditionals, loops) to generate inputs that trigger each branch.
   - For example, if `func0` processes nested dictionaries, include strategies generating empty, single-key, and deeply nested dictionaries.
10. **Complete and Executable Script**:
    - Output a single, executable Python script that can be saved as a `.py` file and run directly.
    - Ensure the script is minimal, avoiding unnecessary imports or logic, while being robust and maintainable.

## Input
The Python code for the ground truth function `func0` is provided below:
```python
{func_code}

## Output
Generate a complete, executable Python code string for the test case generator script. For example:
```python
import hypothesis
import hypothesis.strategies as st
import json
# ... rest of the script ...
```
## Examples
### Example 1: Code Indentation Function
For an input function like:
```python
def _get_correct_indent_level(lines: List[str], line_index: int) -> str:
    if line_index > 0:
        prev_line = lines[line_index - 1].rstrip()
        if prev_line and not prev_line.endswith(","):
            return prev_line[: len(prev_line) - len(prev_line.lstrip())]
    for i in range(line_index - 1, -1, -1):
        line = lines[i].rstrip()
        if not line:
            continue
        curr_indent = line[: len(line) - len(line.lstrip())]
        if len(line) - len(line.lstrip()) >= 8:
            return line[: len(line) - len(line.lstrip())]
        if line.lstrip().startswith(("def ", "class ", "async def ")):
            return curr_indent + "  "
        if line.endswith(":"):
            return curr_indent + "  "
    return ""
```
The generated script might look like:
```python
from hypothesis import settings, given, Verbosity, example
from hypothesis import strategies as st
from typing import List
import json
import os
import atexit
import copy

# Configuration
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")
generated_cases = []

# Ground truth function
def _get_correct_indent_level(lines: List[str], line_index: int) -> str:
    if line_index > 0:
        prev_line = lines[line_index - 1].rstrip()
        if prev_line and not prev_line.endswith(","):
            return prev_line[: len(prev_line) - len(prev_line.lstrip())]
    for i in range(line_index - 1, -1, -1):
        line = lines[i].rstrip()
        if not line:
            continue
        curr_indent = line[: len(line) - len(line.lstrip())]
        if len(line) - len(line.lstrip()) >= 8:
            return line[: len(line) - len(line.lstrip())]
        if line.lstrip().startswith(("def ", "class ", "async def ")):
            return curr_indent + "  "
        if line.endswith(":"):
            return curr_indent + "  "
    return ""

# Strategy for generating code-like lines
def line_strategy():
    return st.one_of([
        # Lines starting with def/class/async def
        st.tuples(
            st.text(st.characters(whitelist_categories=('Zs',)), max_size=16),
            st.one_of([st.just("def "), st.just("class "), st.just("async def ")]),
            st.text(st.characters(whitelist_categories=('L', 'N')), min_size=1),
            st.one_of([st.just(":"), st.just(""), st.just(" # comment")])
        ).map(lambda x: "".join(x)),
        # Lines ending with colon
        st.tuples(
            st.text(st.characters(whitelist_categories=('Zs',)), max_size=16),
            st.text(st.characters(min_codepoint=33, max_codepoint=126), min_size=1),
            st.just(":")
        ).map(lambda x: "".join(x)),
        # Lines with 8+ spaces
        st.text(st.characters(whitelist_categories=('Zs',)), min_size=8, max_size=16),
        # Lines ending with comma
        st.tuples(
            st.text(st.characters(whitelist_categories=('Zs',)), max_size=16),
            st.text(st.characters(min_codepoint=33, max_codepoint=126), min_size=1),
            st.just(",")
        ).map(lambda x: "".join(x)),
        # Empty lines
        st.just(""),
        # Generic code lines
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z')), min_size=1, max_size=50)
    ])

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    lines=st.lists(line_strategy(), min_size=1, max_size=20, unique=True),
    line_index=st.integers(min_value=0)
)
@example(lines=["    def func():"], line_index=0)
@example(lines=["class MyClass:", "    pass"], line_index=1)
@example(lines=["if condition:", "    value = 1"], line_index=1)
@example(lines=["    previous_line", "next_line"], line_index=1)
@example(lines=["previous_line,", "next_line"], line_index=1)
@example(lines=["        value = 1"], line_index=0)
@example(lines=["random_line"], line_index=0)
def test_get_correct_indent_level(lines: List[str], line_index: int):
    if line_index >= len(lines):
        line_index = len(lines) - 1
    
    lines_copy = copy.deepcopy(lines)
    expected = _get_correct_indent_level(lines_copy, line_index)
    
    if len(lines) > 1 or any(
        line.lstrip().startswith(("def ", "class ", "async def ")) or
        line.endswith(":") or
        line.endswith(",") or
        len(line) - len(line.lstrip()) >= 8
        for line in lines
    ):
        generated_cases.append({
            "Inputs": {"lines": lines, "line_index": line_index},
            "Expected": expected
        })

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)
```
### Example 2: JSON Merge Function
For an input function like:
```python
def merge_json_recursive(base, update):
    \"\"\"Recursively merge two JSON-like objects.
    - Dictionaries are merged recursively
    - Lists are concatenated
    - Other types are overwritten by the update value

    Args:
        base: Base JSON-like object
        update: Update JSON-like object to merge into base

    Returns:
        Merged JSON-like object
    \"\"\"
    if not isinstance(base, dict) or not isinstance(update, dict):
        if isinstance(base, list) and isinstance(update, list):
            return base + update
        return update

    merged = base.copy()
    for key, value in update.items():
        if key in merged:
            merged[key] = merge_json_recursive(merged[key], value)
        else:
            merged[key] = value

    return merged
```
The generated script might look like:
```python
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
def merge_json_recursive(base, update):
    if not isinstance(base, dict) or not isinstance(update, dict):
        if isinstance(base, list) and isinstance(update, list):
            return base + update
        return update

    merged = base.copy()
    for key, value in update.items():
        if key in merged:
            merged[key] = merge_json_recursive(merged[key], value)
        else:
            merged[key] = value

    return merged

# Strategy for JSON-like objects
json_strategy = st.recursive(
    st.one_of([
        st.integers(),
        st.floats(allow_nan=False, allow_infinity=False),
        st.text(st.characters(whitelist_categories=('L', 'N', 'P', 'S', 'Z'))),
        st.booleans()
    ]),
    lambda children: st.one_of(
        st.lists(children, max_size=5),
        st.dictionaries(st.text(st.characters(whitelist_categories=('L', 'N')), max_size=5), children, max_size=5)
    ),
    max_leaves=5
)

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(base=json_strategy, update=json_strategy)
@example(base={}, update={})
@example(base={"a": 1}, update={"a": 2})
@example(base=[1, 2], update=[3, 4])
@example(base={"a": {"b": 1}}, update={"a": {"c": 2}})
@example(base="string", update=42)
@example(base={"a": [1]}, update={"a": [2]})
def test_merge_json_recursive(base, update):
    global stop_collecting
    if stop_collecting:
        return
    
    base_copy = copy.deepcopy(base)
    update_copy = copy.deepcopy(update)
    expected = merge_json_recursive(base_copy, update_copy)
    
    if isinstance(base, (dict, list)) or isinstance(update, (dict, list)):
        generated_cases.append({
            "Inputs": {"base": base, "update": update},
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
```
## Note
- Exactly 500 Test Cases: Use a global stop_collecting flag to ensure exactly 500 test cases are collected, stopping further collection without throwing exceptions to avoid pytest failures.
- High-Quality Test Cases: Filter test cases to prioritize those that exercise meaningful branches, avoiding redundant or irrelevant inputs.
- 100% Branch Coverage: Design strategies to achieve 100% branch coverage, verifiable with pytest-cov. Only include manual_cases if specific branches are difficult to cover, with a comment explaining their necessity.
- Targeted Strategies: Design strategies based on func0’s logic, not generic defaults.
- Executable Code: Ensure the script is complete, executable, and minimal.
- max_examples=10000: Use 10000 examples to ensure enough attempts to collect 500 valid cases after filtering.
- JSON Output: Save test cases in a structured JSON format using atexit.
- Only Return Code: Output only the Python code string, without explanations or additional comments.
"""

TESTCASES_GENERATOR_PROMPT_v2 = """
## Task Description
You are an expert Python developer specializing in property-based testing with the `hypothesis` library and test case generation. Your task is to generate a **complete and executable Python test case generator script** for a given Python function (`func0`, provided in the "Input" section). This script will use `hypothesis` to:
1.Generate diverse input values based on `func0`'s signature.
2.Execute `func0` with the generated inputs to determine the expected output.
3.Collect these input/output pairs as test cases.
4.Save all collected test cases into a single JSON file upon script completion using the `atexit` module.

The generated script must include all necessary components for functionality:
1.**Import Statements**:
  * Import required libraries: `hypothesis`, `hypothesis.strategies as st`, `json`, `os`,`atexit`, potentially `typing` or others needed by `func0`.
2.**Ground Truth Function Definition**:
  * **Crucially, the provided `func0` code must be included directly within the generatedscript** so it can be called to produce expected outputs.
3.**Configuration**:
  * Define a directory path (e.g., `TEST_CASE_DIR`) for saving the output file.
  * Ensure this directory exists using `os.makedirs(..., exist_ok=True)`.
  * Define the output JSON filename (e.g., `test_cases.json`).
4.**Test Case Collection**:
  * Initialize an empty list (e.g., `generated_cases`) to store collected test cases globally.
  * Each test case stored in the list should be a dictionary with keys like `"Inputs"`(containing a dictionary of input arguments and their values) and `"Expected"` (containing theoutput from `func0`).
5.**Input Strategy Generation**:
  * Analyze `func0`'s signature (type hints, argument names, function body context) to inferappropriate `hypothesis.strategies`.
  * Define strategies for each input argument, ensuring generated values are suitable for`func0`.
  * **JSON Compatibility**: Ensure generated values are JSON-serializable:
    * Use `st.floats(allow_nan=False, allow_infinity=False)`.
    * Generate printable strings, e.g., `st.text().filter(lambda s: s.isprintable())` or `stcharacters(whitelist_categories=('L', 'N', 'P', 'S', 'Z', 'M'))`. Avoid raw binary dataunless the function specifically handles it and a JSON-safe representation (like base64) isused during storage.
    * Be mindful of complex types; convert sets/tuples to lists before storing if necessary(though Hypothesis often generates lists directly).
6.**Hypothesis Test Function (`@given(...)`)**:
* Define a test function decorated with `@given(...)`, mapping the generated strategies to `func0`'s arguments.
* Apply `hypothesis.settings`, specifically setting `max_examples=1000`. You can also set `verbosity=Verbosity.verbose` and `print_blob=True` for debugging, but `max_examples=1000` is mandatory.
* Inside the test function:
  * **Handle potential input modification**: If `func0` might modify its inputs (e.g., lists, dicts) in place, make deep copies of the inputs before passing them to `func0` to ensure the *original* inputs are saved. Standard libraries like `copy.deepcopy` might be needed (import `copy`).
  * Call `func0` with the (potentially copied) generated inputs and store the result as `expected_output`.
  * Append a dictionary `{"Inputs": {...}, "Expected": expected_output}` to the global `generated_cases` list. Ensure the structure matches the requirements (Inputs as a dict mapping arg names to values).
  * **No assertions are strictly required here**, as the goal is generation, not validation within *this* script. However, basic type checks on the `expected_output` could be added if helpful.
7. **Saving Test Cases**:
  * Define a function (e.g., `save_test_cases`) that opens the target JSON file and uses `json.dump()` to write the `generated_cases` list. Use `indent=2` for readability.
  * Register this saving function using `atexit.register(save_test_cases)` to ensure it runs automatically when the script finishes (either normally or via exception after Hypothesis finishes its run).
8. **Complete and Executable Script**:
  * The final output must be a single string containing the full Python code, ready to be saved as a `.py` file and executed.

## Input
The Python code for the ground truth function `func0` is provided below:
```python
{func_code}
```
## Output
Generate a complete, executable Python code for the test case generator script as described above. For example:
```python
import hypothesis
import hypothesis.strategies as st
import json
# ... rest of the script ...
```

## Example
For an input function like:
```python
def move_y(matrix_g: list[list[str]], size: int) -> list[list[str]]:
    # Move empty columns ('-' filled) to the right side of the matrix
    empty_columns = []

    # Identify empty columns (all '-')
    for column in range(size - 1, -1, -1):
        if all(matrix_g[row][column] == "-" for row in range(size)):
            empty_columns.append(column)

    # Shift columns left to fill empty spaces
    for column in empty_columns:
        for col in range(column + 1, size):
            for row in range(size):
                matrix_g[row][col - 1] = matrix_g[row][col]
        # Fill rightmost column with '-'
        for row in range(size):
            matrix_g[row][-1] = "-"

    return matrix_g
```
The generated test case generator might look like:
```python
from hypothesis import settings, given, Verbosity
from hypothesis import strategies as st
from tested import move_y as func1
import json
import os
import atexit

# Configuration for saving test cases
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")

# Ground truth implementation
def move_y(matrix_g: list[list[str]], size: int) -> list[list[str]]:
    # Move empty columns ('-' filled) to the right side of the matrix
    empty_columns = []

    # Identify empty columns (all '-')
    for column in range(size - 1, -1, -1):
        if all(matrix_g[row][column] == "-" for row in range(size)):
            empty_columns.append(column)

    # Shift columns left to fill empty spaces
    for column in empty_columns:
        for col in range(column + 1, size):
            for row in range(size):
                matrix_g[row][col - 1] = matrix_g[row][col]
        # Fill rightmost column with '-'
        for row in range(size):
            matrix_g[row][-1] = "-"

    return matrix_g

# Global list to store generated test cases
generated_cases = []

# Hypothesis test configuration
@settings(
    max_examples=1000,
    verbosity=Verbosity.verbose,
    print_blob=True
)
@given(
    matrix_g=st.lists(
        st.lists(
            st.sampled_from(['-', 'A', 'B', 'C']),  # Matrix elements can only be '-', 'A', 'B', 'C'
            min_size=1, max_size=10  # Row length between 1 and 10
        ),
        min_size=1, max_size=10  # Matrix row count between 1 and 10
    ),
    size=st.integers(min_value=1, max_value=10)  # Matrix size limited to 1-10
)
def test_move_y(matrix_g: list[list[str]], size: int):
    # Ensure matrix dimensions match the specified size
    if len(matrix_g) != size or any(len(row) != size for row in matrix_g):
        return

    # Calculate expected output using reference implementation
    expected_output = move_y([row[:] for row in matrix_g], size)  # Copy matrix to avoid in-place modification

    # Calculate actual output using the function under test
    actual_output = func1([row[:] for row in matrix_g], size)  # Also copy the matrix

    # Collect test parameters
    generated_cases.append({
        "Inputs": {
            "matrix_g": matrix_g,
            "size": size,
        },
        "Expected": expected_output,
    })

    # Assert that outputs match
    assert expected_output == actual_output, (
        f"Test failed for inputs:\n"
        f"matrix_g={matrix_g}\n"
        f"size={size}\n"
        f"Expected: {expected_output}\n"
        f"Actual: {actual_output}"
    )

# Save test cases to JSON file when pytest exits
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)  # Ensure data is saved when tests complete
```
## Note
- **Focus on Test Case Generation**: The primary goal is to generate and save test cases for later use. The generator should facilitate this by collecting inputs and expected outputs during the Hypothesis tests.
- **Preserve Original Input Strategies**: Use the same `hypothesis.strategies` as defined in the input driver code to ensure consistency.
- **Save Test Cases to JSON**: Ensure the generated test cases are saved to a JSON file in a structured format for easy reuse.
- **Executable Code**: The generated code must be a complete that can be executed directly.
- **max_examples**: must be set to 1000.
- **Save the test cases**: Don't forget to use `atexit` to save the test cases in json format only once after all tests are completed.
- **Only return the code**: Don't include any additional explanations or comments in the output.
"""

TESTCASES_GENERATOR_PROMPT_v1 = """
## Task Description
You are an expert Python developer specializing in property-based testing with the `hypothesis` library and test case generation. Your task is to generate a **complete and executable Python test case generator** from a given Hypothesis test driver code. This generator will:
1. Use the same input strategies as defined in the Hypothesis driver.
2. Generate and collect test cases during the execution of the Hypothesis tests.
3. Save the collected test cases to a JSON file for later use with the `atexit` module.

The generated test case generator must include all necessary components for functionality:
1. **Import Statements**:
   - Import required libraries (`hypothesis`, `json`, `os`, `atexit` etc.).
   - Import the ground truth function (`func0`) and the tested function (`func1`) from the provided modules.
2. **Configuration**:
   - Define a directory path (e.g., `TEST_CASE_DIR`) where the generated test cases will be saved.
   - Ensure the directory exists using `os.makedirs`.
3. **Test Case Collection**:
   - Maintain a list (`generated_cases`) to store all generated test cases.
   - Each test case should include:
     - The inputs used for the test.
     - The expected output from the ground truth function (`func0`).
4. **Hypothesis Test Function**:
   - Modify the original Hypothesis test function to:
     - Call the ground truth function (`func0`) to compute the expected output.
     - Call the tested function (`func1`) to compute the actual output.
     - Collect the inputs and expected output into the `generated_cases` list.
     - Assert that the outputs of `func0` and `func1` are identical.
5. **Saving Test Cases**:
   - After running the Hypothesis tests, save the collected test cases (`generated_cases`) to a JSON file in the specified directory, and use `atexit` to save the test cases.
6. **Complete and Executable Code**:
   - Ensure the generated code is a **complete, self-contained, and executable Python script** that defines the test case generator. It should be ready to run assuming `func0` and `func1` are defined in the same environment.
7. **Ensure JSON compatibility**  
   - Ensure that all data types used in the test cases are JSON-compatible.
   - Convert non-serializable types to JSON-compatible formats (`list`, `str`, `int`, etc.).
   - Example: Convert `set()` to `list()`, `tuple()` to `list()`, etc.
   - Use `st.floats(allow_nan=False, allow_infinity=False)` to prevent JSON serialization errors.
   - Strings must be valid UTF-8. Avoid unprintable control characters. Example: safe_strings = st.text(min_size=1).filter(lambda s: s.isprintable())

## Input
The Python code for the Hypothesis test driver is provided below:
```python
{python code}
```
## Output
Generate a JSON response containing a single key "TestcaseGenerator". The value of "TestcaseGenerator" should be a string containing the complete Python code for the test case generator, including:
- Import statements.
- Configuration for saving test cases.
- Modified Hypothesis test function to collect test cases.
- Logic to save the collected test cases to a JSON file.
- Save the generated test cases to a JSON file with `atexit`

The generated code must be ready to be executed.
## Example
For the input Hypothesis test driver code:
```python
from tested import move_y as func1
from hypothesis import settings
import hypothesis.strategies as st
from hypothesis import given

# Define the ground truth function
def move_y(matrix_g: list[list[str]], size: int) -> list[list[str]]:
    empty_columns = []

    for column in range(size - 1, -1, -1):
        if all(matrix_g[row][column] == "-" for row in range(size)):
            empty_columns.append(column)

    for column in empty_columns:
        for col in range(column + 1, size):
            for row in range(size):
                matrix_g[row][col - 1] = matrix_g[row][col]
        for row in range(size):
            matrix_g[row][-1] = "-"

    return matrix_g

# Define the test function
@settings(max_examples=1000)
@given(matrix_g=st.lists(st.lists(st.sampled_from(['-', 'A', 'B', 'C']), min_size=1, max_size=10), min_size=1, max_size=10), size=st.integers(min_value=1, max_value=10))
def test_move_y(matrix_g: list[list[str]], size: int):
    # Ensure the matrix_g has the correct size
    if len(matrix_g) != size or any(len(row) != size for row in matrix_g):
        return

    expected_output = move_y(matrix_g, size)
    actual_output = func1(matrix_g, size)
    assert expected_output == actual_output, (
        f"Mismatch in outputs for inputs: {matrix_g}, {size}.\n"
        f"Expected: {expected_output}\n"
        f"Actual: {actual_output}"
    )
```

The generated test case generator might look like:
```python
from hypothesis import settings, given, Verbosity
from hypothesis import strategies as st
from tested import move_y as func1
import json
import os
import atexit

# Configuration for saving test cases
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")

# Ground truth implementation
def move_y(matrix_g: list[list[str]], size: int) -> list[list[str]]:
    # Move empty columns ('-' filled) to the right side of the matrix
    empty_columns = []

    # Identify empty columns (all '-')
    for column in range(size - 1, -1, -1):
        if all(matrix_g[row][column] == "-" for row in range(size)):
            empty_columns.append(column)

    # Shift columns left to fill empty spaces
    for column in empty_columns:
        for col in range(column + 1, size):
            for row in range(size):
                matrix_g[row][col - 1] = matrix_g[row][col]
        # Fill rightmost column with '-'
        for row in range(size):
            matrix_g[row][-1] = "-"

    return matrix_g

# Global list to store generated test cases
generated_cases = []

# Hypothesis test configuration
@settings(
    max_examples=1000,
    verbosity=Verbosity.verbose,
    print_blob=True
)
@given(
    matrix_g=st.lists(
        st.lists(
            st.sampled_from(['-', 'A', 'B', 'C']),  # Matrix elements can only be '-', 'A', 'B', 'C'
            min_size=1, max_size=10  # Row length between 1 and 10
        ),
        min_size=1, max_size=10  # Matrix row count between 1 and 10
    ),
    size=st.integers(min_value=1, max_value=10)  # Matrix size limited to 1-10
)
def test_move_y(matrix_g: list[list[str]], size: int):
    # Ensure matrix dimensions match the specified size
    if len(matrix_g) != size or any(len(row) != size for row in matrix_g):
        return

    # Calculate expected output using reference implementation
    expected_output = move_y([row[:] for row in matrix_g], size)  # Copy matrix to avoid in-place modification

    # Calculate actual output using the function under test
    actual_output = func1([row[:] for row in matrix_g], size)  # Also copy the matrix

    # Collect test parameters
    generated_cases.append({
        "Inputs": {
            "matrix_g": matrix_g,
            "size": size,
        },
        "Expected": expected_output,
    })

    # Assert that outputs match
    assert expected_output == actual_output, (
        f"Test failed for inputs:\n"
        f"matrix_g={matrix_g}\n"
        f"size={size}\n"
        f"Expected: {expected_output}\n"
        f"Actual: {actual_output}"
    )

# Save test cases to JSON file when pytest exits
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)  # Ensure data is saved when tests complete
```

## Note
- **Focus on Test Case Generation**: The primary goal is to generate and save test cases for later use. The generator should facilitate this by collecting inputs and expected outputs during the Hypothesis tests.
- **Preserve Original Input Strategies**: Use the same `hypothesis.strategies` as defined in the input driver code to ensure consistency.
- **Save Test Cases to JSON**: Ensure the generated test cases are saved to a JSON file in a structured format for easy reuse.
- **Executable Code**: The generated code must be a complete that can be executed directly.
- **max_examples**: must be set to 1000.
- **Save the test cases**: Don't forget to use `atexit` to save the test cases in json format only once after all tests are completed.
"""

TESTCASES_GENERATOR_PROMPT_V0 = """
## Task Description
You are an expert Python developer specializing in property-based testing with the `hypothesis` library and test case generation. Your task is to generate a **complete and executable Python test case generator** from a given Hypothesis test driver code. This generator will:
1. Use the same input strategies as defined in the Hypothesis driver.
2. Generate and collect test cases during the execution of the Hypothesis tests.
3. Save the collected test cases to a JSON file for later use with the `atexit` module.

The generated test case generator must include all necessary components for functionality:
1. **Import Statements**:
   - Import required libraries (`hypothesis`, `json`, `os`, `atexit` etc.).
   - Import the ground truth function (`func0`) and the tested function (`func1`) from the provided modules.
2. **Configuration**:
   - Define a directory path (e.g., `TEST_CASE_DIR`) where the generated test cases will be saved.
   - Ensure the directory exists using `os.makedirs`.
3. **Test Case Collection**:
   - Maintain a list (`generated_cases`) to store all generated test cases.
   - Each test case should include:
     - The inputs used for the test.
     - The expected output from the ground truth function (`func0`).
4. **Hypothesis Test Function**:
   - Modify the original Hypothesis test function to:
     - Call the ground truth function (`func0`) to compute the expected output.
     - Call the tested function (`func1`) to compute the actual output.
     - Collect the inputs and expected output into the `generated_cases` list.
     - Assert that the outputs of `func0` and `func1` are identical.
5. **Saving Test Cases**:
   - After running the Hypothesis tests, save the collected test cases (`generated_cases`) to a JSON file in the specified directory, and use `atexit` to save the test cases.
6. **Complete and Executable Code**:
   - Ensure the generated code is a **complete, self-contained, and executable Python script** that defines the test case generator. It should be ready to run assuming `func0` and `func1` are defined in the same environment.

## Input
The Python code for the Hypothesis test driver is provided below:
```python
{python code}
```
## Output
Generate a JSON response containing a single key "TestcaseGenerator". The value of "TestcaseGenerator" should be a string containing the complete Python code for the test case generator, including:
- Import statements.
- Configuration for saving test cases.
- Modified Hypothesis test function to collect test cases.
- Logic to save the collected test cases to a JSON file.
- Save the generated test cases to a JSON file with `atexit`

The generated code must be ready to be executed.
## Example
For the input Hypothesis test driver code:
```python
from tested import move_y as func1
from hypothesis import settings
import hypothesis.strategies as st
from hypothesis import given

# Define the ground truth function
def move_y(matrix_g: list[list[str]], size: int) -> list[list[str]]:
    empty_columns = []

    for column in range(size - 1, -1, -1):
        if all(matrix_g[row][column] == "-" for row in range(size)):
            empty_columns.append(column)

    for column in empty_columns:
        for col in range(column + 1, size):
            for row in range(size):
                matrix_g[row][col - 1] = matrix_g[row][col]
        for row in range(size):
            matrix_g[row][-1] = "-"

    return matrix_g

# Define the test function
@settings(max_examples=1000)
@given(matrix_g=st.lists(st.lists(st.sampled_from(['-', 'A', 'B', 'C']), min_size=1, max_size=10), min_size=1, max_size=10), size=st.integers(min_value=1, max_value=10))
def test_move_y(matrix_g: list[list[str]], size: int):
    # Ensure the matrix_g has the correct size
    if len(matrix_g) != size or any(len(row) != size for row in matrix_g):
        return

    expected_output = move_y(matrix_g, size)
    actual_output = func1(matrix_g, size)
    assert expected_output == actual_output, (
        f"Mismatch in outputs for inputs: {matrix_g}, {size}.\n"
        f"Expected: {expected_output}\n"
        f"Actual: {actual_output}"
    )
```

The generated test case generator might look like:
```python
from hypothesis import settings, given, Verbosity
from hypothesis import strategies as st
from tested import move_y as func1
import json
import os
import atexit

# Configuration for saving test cases
TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)
TEST_CASE_FILE = os.path.join(TEST_CASE_DIR, "test_cases.json")

# Ground truth implementation
def move_y(matrix_g: list[list[str]], size: int) -> list[list[str]]:
    # Move empty columns ('-' filled) to the right side of the matrix
    empty_columns = []

    # Identify empty columns (all '-')
    for column in range(size - 1, -1, -1):
        if all(matrix_g[row][column] == "-" for row in range(size)):
            empty_columns.append(column)

    # Shift columns left to fill empty spaces
    for column in empty_columns:
        for col in range(column + 1, size):
            for row in range(size):
                matrix_g[row][col - 1] = matrix_g[row][col]
        # Fill rightmost column with '-'
        for row in range(size):
            matrix_g[row][-1] = "-"

    return matrix_g

# Global list to store generated test cases
generated_cases = []

# Hypothesis test configuration
@settings(
    max_examples=1000,
    verbosity=Verbosity.verbose,
    print_blob=True
)
@given(
    matrix_g=st.lists(
        st.lists(
            st.sampled_from(['-', 'A', 'B', 'C']),  # Matrix elements can only be '-', 'A', 'B', 'C'
            min_size=1, max_size=10  # Row length between 1 and 10
        ),
        min_size=1, max_size=10  # Matrix row count between 1 and 10
    ),
    size=st.integers(min_value=1, max_value=10)  # Matrix size limited to 1-10
)
def test_move_y(matrix_g: list[list[str]], size: int):
    # Ensure matrix dimensions match the specified size
    if len(matrix_g) != size or any(len(row) != size for row in matrix_g):
        return

    # Calculate expected output using reference implementation
    expected_output = move_y([row[:] for row in matrix_g], size)  # Copy matrix to avoid in-place modification

    # Calculate actual output using the function under test
    actual_output = func1([row[:] for row in matrix_g], size)  # Also copy the matrix

    # Collect test parameters
    generated_cases.append({
        "Inputs": {
            "matrix_g": matrix_g,
            "size": size,
        },
        "Expected": expected_output,
    })

    # Assert that outputs match
    assert expected_output == actual_output, (
        f"Test failed for inputs:\n"
        f"matrix_g={matrix_g}\n"
        f"size={size}\n"
        f"Expected: {expected_output}\n"
        f"Actual: {actual_output}"
    )

# Save test cases to JSON file when pytest exits
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)  # Ensure data is saved when tests complete
```

## Note
- **Focus on Test Case Generation**: The primary goal is to generate and save test cases for later use. The generator should facilitate this by collecting inputs and expected outputs during the Hypothesis tests.
- **Preserve Original Input Strategies**: Use the same `hypothesis.strategies` as defined in the input driver code to ensure consistency.
- **Save Test Cases to JSON**: Ensure the generated test cases are saved to a JSON file in a structured format for easy reuse.
- **Executable Code**: The generated code must be a complete that can be executed directly.
- **max_examples**: must be set to 1000.
- **Save the test cases**: Don't forget to use `atexit` to save the test cases in json format only once after all tests are completed.
"""


RECURSIVE_NOTE = """
## Special Handling for Recursive Functions
If the provided Hypothesis test driver contains a **recursive function**, your implementation must:
- **Limit the recursion depth** to prevent infinite recursion.
- **Ensure JSON compatibility** of the generated test cases.
- **Detect and handle base cases** correctly.
- **Track recursion depth** and store it as `"recursion_depth"` in the JSON output.

### **How to handle recursion**
1. **Restrict recursion depth**  
   - Use `hypothesis.strategies.recursive()` with `max_leaves=5` to restrict recursion depth.

### Example
Use the following structure when defining recursive test cases:
```python
from hypothesis import strategies as st

base_strategy = st.integers(min_value=0, max_value=100)
recursive_strategy = st.recursive(
    base_strategy,
    lambda children: st.lists(children, min_size=1, max_size=3),
    max_leaves=5  # Restrict recursive depth
)
```
"""