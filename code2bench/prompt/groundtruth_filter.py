WEAKLY_SELF_CONTAINED_DIFFICULTY_ASSESSMENT_PROMPT = """
## Task Description
You are an expert code analyst tasked with assessing the difficulty level of a weakly self-contained Python function. A weakly self-contained function depends only on Python standard libraries or specific external libraries (e.g., NumPy, pandas, re) and no custom modules. Assume the function is valid and suitable for analysis. Assign a difficulty level of "Easy", "Medium", or "Hard" based on the complexity of its logic, structure, required concepts, and cognitive load to understand.

## Criteria for Difficulty Assessment

### Easy Difficulty
- **Logic**: Very simple, minimal or no branching, single loop or direct parameter use.
- **Structure**: Short, linear, immediately clear control flow.
- **Concepts**: Basic Python constructs (variables, operators, lists, strings) or simple library calls (e.g., Counter from collections, basic re matching, pandas filtering).
- **Cognitive Load**: Minimal; purpose and execution are obvious at a glance.
- **Example**:
```python
from collections import Counter

def count_word_frequencies(text: str) -> dict[str, int]:
    \"\"\"Count the frequency of each word in a text string.

    Args:
        text: Input string containing words.

    Returns:
        Dictionary mapping words to their frequency.
    \"\"\"
    words = text.lower().split()
    return dict(Counter(words))
```

### Medium Difficulty
- Logic: Moderate complexity, with loops, conditions, or data transformations (e.g., - filtering, sorting, deduplication).
- Structure: Traceable control flow, possibly nested loops or multiple steps, moderate length.
- Example:
```python
import re
from typing import List

def extract_email_domains(text: str) -> List[str]:
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
Hard Difficulty
- Logic: Complex, with nested loops, intricate transformations, non-trivial algorithms (e.g., multi-dim aggregation, complex grouping), or subtle edge cases.
- Structure: Dense or multi-step control flow, significant state management.
Example:
```python
import re

def _custom_replace(key: str, substrings: List[str]) -> str:
    # Replaces the "."s with "_"s upto the `substrings`.
    # Example:
    # lora_unet.foo.bar.lora_A.weight -> lora_unet_foo_bar.lora_A.weight
    pattern = "(" + "|".join(re.escape(sub) for sub in substrings) + ")"

    match = re.search(pattern, key)
    if match:
        start_sub = match.start()
        if start_sub > 0 and key[start_sub - 1] == ".":
            boundary = start_sub - 1
        else:
            boundary = start_sub
        left = key[:boundary].replace(".", "_")
        right = key[boundary:]
        return left + right
    else:
        return key.replace(".", "_")
```
## Output Format
Return ONLY a JSON object containing the assessed difficulty level:
```json
{
    "Difficulty": "Easy/Medium/Hard"
}
```

## Note
- weakly self-contained function depends only on Python standard libraries or specific external libraries (e.g., NumPy, pandas, re) and no custom modules.
- Focus on logic and structure, not the library’s complexity (e.g., simple Counter usage is Easy, complex NumPy array ops are Hard).
- Analyze the function’s code, docstring, and logic thoroughly.
- Only return the JSON output in the specified format.
"""


DIFFICULTY_ASSESSMENT_PROMPT = """
## Task Description
You are an expert code analyst. Your task is to assess the difficulty level of the provided Python function. Assume the function is generally valid and suitable for analysis. Assign a difficulty level of "Easy", "Medium", or "Hard" based on the complexity of its logic, structure, required concepts, and cognitive load to understand.

## Criteria for Difficulty Assessment
### Easy Difficulty
- Logic: Straightforward, minimal branching (simple if/else), possibly a single simple loop. Direct use of parameters.
- Structure: Typically short, linear control flow. Easy to follow step-by-step.
- Concepts: Relies on fundamental programming constructs (variables, basic operators, standard data types, simple function calls).
- Cognitive Load: Low; the function's purpose and execution are immediately apparent.
- Example:
```python
def parse_message(message: str) -> str:
    if message is None:
        return ""
    message = message.strip().lower()
    # Simple string checks and manipulations
    if not message.startswith(("run-slow", "run_slow", "run slow")):
        return ""
    message = message[len("run slow") :]
    while message.strip().startswith(":"):
        message = message.strip()[1:]
    return message
```
### Hard Difficulty
- Logic: Moderate complexity. May involve nested loops, multiple non-trivial conditions, manipulation of data structures (e.g., iterating through lists/dicts with transformations), implementing a common simple algorithm, or tracking state across iterations.
- Structure: Control flow is more involved but still reasonably traceable. Function length might be moderate.
- Example:
```python
def qa_pairs_to_qna_to_avg_scores(qa_pairs: list[dict]) -> dict[str, float]:
    qna_to_scores: dict[str, list[float]] = {}
    for qa_pair in qa_pairs:
        qna_file = qa_pair["qna_file"]
        score = qa_pair["score"]
        scores = qna_to_scores.get(qna_file)
        if scores is None:
            qna_to_scores[qna_file] = [score]
        else:
            scores.append(score)
    qna_to_avg_scores = {}
    for qna, scores in qna_to_scores.items():
        qna_to_avg_scores[qna] = sum(scores) / len(scores)
    return qna_to_avg_scores
```
### Hard Difficulty
- Logic: Complex logic. Might involve recursion, implementing non-trivial algorithms.
- Structure: Can have nested structures, complex control flow, significant state management, or rely on clever interactions between code parts. May not be long but could be dense.
- Example:
```python
def find_closest_aspect_ratio(
    aspect_ratio: float,
    target_ratios: list[tuple[int, int]],
    *,
    width: int, # Although present, these args aren't heavily used in core logic below
    height: int,
    image_size: int,
) -> tuple[int, int]:
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    # area = width * height # Calculation commented out or removed for simplicity focus
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        # Logic to find minimum difference, with a tie-breaking condition
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            # Simple tie-breaking placeholder or simplified logic
            # Example: prefer smaller denominator in case of tie
            if ratio[1] < best_ratio[1]:
               best_ratio = ratio
    return best_ratio
```
## Output Format
Return ONLY a JSON object containing the assessed difficulty level:
{
    "Difficulty": "Easy/Medium/Hard"
}
"""

WEAKLY_GROUND_TRUTH_FILTER_AND_REWRITE_PROMPT = """
You are an expert in Python coding, tasked with two responsibilities:
1. Determine whether a given Python **class method** (with `self` as first parameter) meets benchmark suitability criteria (weakly self-contained).
2. If suitable AND **fully self-contained** (no `self.xxx` access), rewrite it as a top-level global function (remove `self`, add necessary imports).

---

## 🚫 Criteria for Suitability (ALL must be met)

### 1. Function Parameters
- **Basic and Library Types**: Parameters must be:
  - Basic types: `int`, `float`, `str`, `list`, `dict`, `tuple`, `bool`, `None`
  - Standard/external library types: `numpy.ndarray`, `pandas.DataFrame`, `re.Pattern`, `pathlib.Path`, etc.
  - ✅ Type hints can be missing — infer from usage.
  - ❌ Custom class types (e.g., `MyModel`, `custom_module.X`) → Not suitable.
  - ❌ Relies on unknown object methods/attributes → Not suitable.
  - ✅ Uses `typing.List[np.ndarray]` → Suitable.

### 2. Function Complexity
- **Meaningful Logic**: Should test non-trivial reasoning or transformation.
  - ❌ Trivial logic (e.g., `.suffix`, simple getter) → Not suitable.
  - ❌ Too long but shallow → Not suitable.
  - ✅ Moderate-to-complex logic with clear purpose → Suitable.

### 3. Domain Knowledge
- **General Applicability**: Should not require niche or proprietary knowledge.
  - ❌ Tied to internal system, custom framework → Not suitable.
  - ✅ Uses `numpy` for math, `re` for text → Suitable.

### 4. Property-Based Testing
- **Constructible Inputs**: Must be testable with generated/random inputs.
  - ❌ Depends on external state (time, random seed without control, hardware) → Not suitable.
  - ❌ Non-deterministic behavior → Not suitable.
  - ✅ Pure function with constructible inputs → Suitable.

---

## ✅ Rewrite Rules (ONLY if Suitable == true)

### Step 1: Check for `self.` usage
- If function body contains ANY `self.` (e.g., `self.attr`, `self.method()`, `self["key"]`, `getattr(self,...)`):
  - Keep `Suitable: true` (if it passed all above),
  - Set `RewrittenCode: null`
  - Append to Reason: "Function is suitable but not self-contained (uses self.xxx), cannot rewrite."

### Step 2: If NO `self.` usage → Rewrite!
- Remove first parameter `self`
- Keep all other parameters, type hints, body, return annotation
- **Automatically add missing imports** if used:
  - If `re.findall` → add `import re`
  - If `np.array` → add `import numpy as np`
  - If `pd.DataFrame` → add `import pandas as pd`
  - If `pathlib.Path` → add `import pathlib`
  - If `List`, `Dict`, `Optional` from `typing` → add `from typing import List, Dict, Optional, ...`
- Output clean, runnable top-level function as string in `RewrittenCode`
- Escape newlines as `\\n` for valid JSON

---

## 🧾 Output Format (STRICT JSON ONLY)

```json
{
    "Suitable": true,
    "Reason": "The function meets all criteria and is self-contained.",
    "RewrittenCode": "import re\\nfrom typing import List\\n\\ndef extract_email_domains(text: str) -> List[str]: ..."
}
```

OR

```json
{
    "Suitable": true,
    "Reason": "Function is suitable but not self-contained (uses self.xxx), cannot rewrite.",
    "RewrittenCode": null
}
```

OR

```json
{
    "Suitable": false,
    "Reason": "The function depends on a custom module.",
    "RewrittenCode": null
}
```

---

## 📚 Examples

### Example 1: Not Suitable (Trivial Logic)

```python
import pathlib

def get_file_extension(self, file_path: pathlib.Path) -> str:
    return file_path.suffix
```

Output:
```json
{
    "Suitable": false,
    "Reason": "The function is too simple, lacking meaningful complexity to test the model's capabilities.",
    "RewrittenCode": null
}
```

---

### Example 2: Suitable + Uses numpy → Auto import

```python
def chain_pair_pde(self, num_tokens: int, asym_ids: np.ndarray, full_pde: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
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

Output:
```json
{
    "Suitable": true,
    "Reason": "The function has meaningful complexity, uses well-defined library types (numpy), and is self-contained.",
    "RewrittenCode": "import numpy as np\\nfrom typing import Tuple\\n\\ndef chain_pair_pde(num_tokens: int, asym_ids: np.ndarray, full_pde: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:\\n    full_pde = full_pde[:, :num_tokens, :num_tokens]\\n    asym_ids = asym_ids[:num_tokens]\\n    unique_asym_ids = np.unique(asym_ids)\\n    num_chains = len(unique_asym_ids)\\n    num_samples = full_pde.shape[0]\\n    chain_pair_pred_err_mean = np.zeros((num_samples, num_chains, num_chains))\\n    chain_pair_pred_err_min = np.zeros((num_samples, num_chains, num_chains))\\n\\n    for idx1, asym_id_1 in enumerate(unique_asym_ids):\\n        subset = full_pde[:, asym_ids == asym_id_1, :]\\n        for idx2, asym_id_2 in enumerate(unique_asym_ids):\\n            subsubset = subset[:, :, asym_ids == asym_id_2]\\n            chain_pair_pred_err_mean[:, idx1, idx2] = np.mean(subsubset, axis=(1, 2))\\n            chain_pair_pred_err_min[:, idx1, idx2] = np.min(subsubset, axis=(1, 2))\\n    return chain_pair_pred_err_mean, chain_pair_pred_err_min"
}
```

---

### Example 3: Not Suitable (Custom Dependency)

```python
import custom_module

def process_data(self, data: custom_module.DataType) -> int:
    return data.compute_value()
```

Output:
```json
{
    "Suitable": false,
    "Reason": "The function depends on a custom module (custom_module) and uses an unknown type (DataType), making it not suitable for a benchmark.",
    "RewrittenCode": null
}
```

---

## ⚠️ Important Notes

- ALWAYS output valid JSON.
- NEVER output explanations, markdown, or extra text.
- Escape newlines in `RewrittenCode` as `\\n` for valid JSON string.
- Auto-import only for: `re`, `numpy`, `pandas`, `pathlib`, `typing` (and their common aliases like `np`, `pd`)
- If `self.` appears → `RewrittenCode = null`, even if otherwise suitable.
- If import is already present in input → keep it in output.
- If function uses `random` → ❌ Not suitable (non-deterministic unless seeded and controlled — too risky for benchmark).
"""

WEAKLY_GROUNG_TRUTH_FILTER_PROMPT = """
You are an expert in Python coding, tasked with determining whether a given Python function meets the requirements below for generating a benchmark. The function is weakly self-contained, meaning it depends only on Python standard libraries or specific external libraries (e.g., numpy, re, pandas) and no custom modules. You will analyze the function based on its characteristics, functionality, and adherence to specific criteria. If the function meets the criteria, it is deemed suitable; otherwise, it is not.

## Criteria for Suitability
To determine whether a function is suitable, consider the following criteria:
### 1. Function Parameters
- **Basic and Library Types**: Parameters must be basic Python types (e.g., `int`, `float`, `str`, `list`, `dict`) or types from standard/external libraries (e.g., `numpy.ndarray`, `re.Pattern`).
  - If the parameters' type is missing, but you can infer it from the code, it is **suitable**.
  - If the function relies on methods or attributes of unknown objects, it is **not suitable**. But if the function uses lib types (e.g., `numpy.ndarray`, `pandas.DataFrame`), it is **suitable**.

### 2. Function Complexity
- **Meaningful Complexity**: The function should provide a meaningful test of the model's capabilities, with clear logic and purpose.
  - If the function is overly long but trivial (e.g., repetitive assignments), it is **not suitable**.
  - If the function is too simple (e.g., basic getter/setter), it is **not suitable**.

### 3. Domain Knowledge
- **General Applicability**: The function should not require highly specialized domain knowledge to understand or implement.
  - If the function is tied to a specific, non-generalizable application (e.g., proprietary system logic), it is **not suitable**.

### 4. Property-Based Testing
- **Constructible Inputs**: The function should allow generating random inputs for property-based testing to verify its behavior.
  - The function exhibits non-deterministic behavior, such as unpredictable results from concurrent thread scheduling, or dependencies on external states (like random numbers, etc.), it is **not suitable**.
  - If inputs cannot be constructed or tested (e.g., requires specific hardware), it is **not suitable**.

## Output Format
If the function is **suitable**, return:
```json
{
    "Suitable": true,
    "Reason": "The reason why the function meets all criteria for generating a benchmark."
}
If the function is not suitable, return:
```json
{
    "Suitable": false,
    "Reason": "The reason why the function is not suitable for generating a benchmark."
}
```
## Examples
### Example 1: Not Suitable (Trivial Logic)
```python
import pathlib

def get_file_extension(file_path: pathlib.Path) -> str:
    \"\"\"Get the file extension from a path.\"\"\"
    return file_path.suffix
```
Output:
```json
{
    "Suitable": false,
    "Reason": "The function is too simple, lacking meaningful complexity to test the model's capabilities."
}
```
Example 2: Suitable (Meaningful Logic)
```python
def extract_email_domains(text: str) -> List[str]:
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
```json
{
    "Suitable": true,
    "Reason": "The function has meaningful logic, and can be tested with property-based testing, making it suitable for a benchmark."
}
```
Example 3: Suitable (Complex Logic)
```python
def chain_pair_pde(
    num_tokens: int, asym_ids: np.ndarray, full_pde: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
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
Output:
```json
{
    "Suitable": true,
    "Reason": "The function has meaningful complexity, uses well-defined library types, and supports property-based testing, making it suitable for a benchmark instruction."
}
```
Example 4: Not Suitable (Custom Dependency)
```python
import custom_module

def process_data(data: custom_module.DataType) -> int:
    \"\"\"Process custom data type.\"\"\"
    return data.compute_value()
```
Output:
```json
{
    "Suitable": false,
    "Reason": "The function depends on a custom module (custom_module) and uses an unknown type (DataType), making it not suitable for a benchmark."
}
```
## Note
- Provide clear and concise reasoning for the decision.
- If the function meets our standards but is missing imports, it is still suitable.
- If the function only uses `typing` for type hints, it is not suitable.
- Only return the JSON output in the specified format.
"""

GROUNG_TRUTH_FILTER_AND_REWRITE_PROMPT = """
## Task Description
You are an expert in the field of coding, tasked with two responsibilities:
1. Determine whether a given Python **class method** (with `self` as first parameter) is suitable for generating an instruction (question) for testing a code generation model.
2. If suitable AND **fully self-contained** (no `self.xxx` access), rewrite it as a top-level global function (remove `self`, add necessary imports).

The function will be analyzed based on its characteristics, functionality, and adherence to specific criteria.

---

## 🚫 Criteria for Suitability (ALL must be met)

### 1. Function Parameters
- **Basic Types Only**: Parameters must be basic types (e.g., `int`, `float`, `str`, `list`, `dict`, `tuple`, `bool`, `None`, or from `typing` like `List[str]`, `Optional[Dict]`).
  - ❌ Custom classes or unknown types → Not suitable.
  - ❌ Relies on methods/attributes of unknown objects → Not suitable.

### 2. Function Complexity
- **Meaningful Logic**: Should test non-trivial reasoning or transformation.
  - ❌ Trivial logic (e.g., simple string split, basic assignment) → Not suitable.
  - ❌ Too long but shallow → Not suitable.
  - ❌ No clear purpose → Not suitable.

### 3. Side Effects and Dependencies
- **No Side Effects**: Must not modify globals, write files, print, call APIs, etc.
- **No External Imports**: Must not import modules (e.g., `import os`, `from sklearn...`).
  - ❌ Uses `Tensor`, `DataFrame`, etc. without clear type hints → Not suitable.

### 4. Error Handling and Edge Cases
- ✅ Clear error handling is a plus, but not mandatory.
- ⚠️ If completely ignores edge cases, note it in Reason — but doesn't auto-reject.

### 5. Domain Knowledge
- **General Applicability**: Should not require niche domain knowledge.
  - ❌ Tied to internal framework, proprietary types → Not suitable.

### 6. Property-Based Testing
- **Constructible Inputs**: Must be testable with random or generated inputs.
  - ❌ Requires complex setup or external state → Not suitable.

---

## ✅ Additional Rewrite Rule (ONLY if Suitable == true)

- **Check for `self.` usage**: If function body contains ANY `self.` (e.g., `self.attr`, `self.method()`, `self["key"]`, `getattr(self,...)`), then:
  - `Suitable` remains `true` (if it passed all above),
  - But `RewrittenCode` must be `null` — because it's not safe to extract.
  - Add to Reason: "Function is suitable but not self-contained (uses self.xxx), cannot rewrite."

- **If NO `self.` usage**:
  - Remove first parameter `self`
  - Keep all other parameters, type hints, body, return annotation
  - Add necessary `from typing import ...` if `List`, `Dict`, etc. are used
  - Output clean, runnable top-level function in `RewrittenCode`

---

## 🧾 Output Format (STRICT JSON ONLY)
```json
{
    "Suitable": true,
    "Reason": "The function meets all criteria and is self-contained.",
    "RewrittenCode": "from typing import List, Dict\\n\\ndef my_func(param: List[Dict]) -> str: ..."
}
```

OR
```json
{
    "Suitable": true,
    "Reason": "Function is suitable but not self-contained (uses self.xxx), cannot rewrite.",
    "RewrittenCode": null
}
```

OR
```json
{
    "Suitable": false,
    "Reason": "The function uses external imports or custom types.",
    "RewrittenCode": null
}
```

---

## 📚 Examples

### Example 1: Not Suitable (Trivial Logic)
```python
def parse_resource_filter(self, resource_filter: str) -> Tuple[Optional[str], ...]:
    filters = resource_filter.split(":")
    # ... simple assignments
    return target_env, target_infra, ...
```

Output:
```json
{
    "Suitable": false,
    "Reason": "The function lacks meaningful complexity and does not provide a meaningful test of the model's capabilities.",
    "RewrittenCode": null
}
```

---

### Example 2: Suitable + Self-Contained → Rewrite!
```python
def normalize_codec(self, codec_str):
    result = str(codec_str).upper()
    parts = result.split('.')
    if len(parts) > 0:
        result = parts[0].strip()
    else:
        return None
    if 'NONE' == result:
        return None
    if str(0) in result:
        prefix = result.rstrip('0123456789')
        result = prefix + str(int(result[len(prefix):]))
    return result
```

Output:
```json
{
    "Suitable": true,
    "Reason": "The function has meaningful logic and is self-contained.",
    "RewrittenCode": "def normalize_codec(codec_str):\\n    result = str(codec_str).upper()\\n    parts = result.split('.')\\n    if len(parts) > 0:\\n        result = parts[0].strip()\\n    else:\\n        return None\\n    if 'NONE' == result:\\n        return None\\n    if str(0) in result:\\n        prefix = result.rstrip('0123456789')\\n        result = prefix + str(int(result[len(prefix):]))\\n    return result"
}
```

---

## ⚠️ Important Notes
- ALWAYS output valid JSON.
- NEVER output explanations, markdown, or extra text.
- Escape newlines in `RewrittenCode` as `\\n` for valid JSON string.
- If function uses `Optional`, `Tuple`, etc., auto-add `from typing import ...`.
- If any `self.` appears → `RewrittenCode = null`, even if otherwise suitable.
"""

GROUNG_TRUTH_FILTER_PROMPT = """
## Task Description
You are an expert in the field of coding, tasked with determining whether a given Python function is suitable for generating an instruction (question). 
The function will be analyzed based on its characteristics, functionality, and adherence to specific criteria. If the function meets the criteria, it is deemed suitable; otherwise, it is not.

## Criteria for Suitability
To determine whether a function is suitable for generating an instruction, consider the following criteria:

### 1. Function Parameters
- **Basic Types Only**: The function's parameters must be basic types (e.g., `int`, `float`, `str`, `list`, `dict`, etc.). 
  - If the parameters include custom classes or unknown types, the function is **not suitable**.
  - If the function relies on methods or attributes of unknown objects, the function is **not suitable**.

### 2. Function Complexity
- **Meaningful Complexity**: The function should provide a meaningful test of the model's capabilities. 
  - If the function is very long but its logic is trivial, it is **not suitable**.
  - If the function is too simple (e.g., basic business logic), it is **not suitable**.
  - If the function lacks clear logic or purpose, it is **not suitable**.

### 3. Side Effects and Dependencies
- **No Side Effects**: The function should not have side effects (e.g., modifying global variables, writing to files, etc.).
- **No External Imports**: The function should not import other modules or depend on external libraries.
  - If the function uses domain-specific types (e.g., `Tensor`, `DataFrame`) without explicit type hints, it is **not suitable**.

### 4. Error Handling and Edge Cases
- **Clear Error Handling**: The function should handle exceptions and edge cases explicitly. 
  - If the function lacks clear error handling or ignores edge cases, it may still be suitable, but this should be noted.

### 5. Domain Knowledge
- **General Applicability**: The function should not require highly specialized domain knowledge to understand or use. 
  - If the function is tied to a specific application or domain that is not generalizable, it is **not suitable**.

### 6. Property-Based Testing
- **Constructible Inputs**: The function should be testable using property-based testing (e.g., generating random inputs to test behavior). 
  - If the function cannot be tested in this way, it is **not suitable**.

## Output Format
If the function is **suitable**, return:
```json
{
    "Suitable": true,
    "Reason": "The function meets all criteria for generating an instruction."
}
```
If the function is not suitable , return:
```json
{
    "Suitable": false,
    "Reason": "The reason why the function is not suitable for generating an instruction."
}
```
## Examples
Example 1: Not Suitable (No Testing Meaning)
```python
def parse_resource_filter(
    resource_filter: str,
) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
    target_env: Optional[str] = None
    target_infra: Optional[str] = None
    target_group: Optional[str] = None
    target_name: Optional[str] = None
    target_type: Optional[str] = None

    filters = resource_filter.split(":")
    num_filters = len(filters)
    if num_filters >= 1:
        if filters[0] != "":
            target_env = filters[0]
    if num_filters >= 2:
        if filters[1] != "":
            target_infra = filters[1]
    if num_filters >= 3:
        if filters[2] != "":
            target_group = filters[2]
    if num_filters >= 4:
        if filters[3] != "":
            target_name = filters[3]
    if num_filters >= 5:
        if filters[4] != "":
            target_type = filters[4]

    return target_env, target_infra, target_group, target_name, target_type
```
Output:
```json
{
    "Suitable": false,
    "Reason": "The function lacks meaningful complexity and does not provide a meaningful test of the model's capabilities."
}
```
Example 2: Suitable (Meaningful Logic)
```python
def normalize_codec(codec_str):
    result = str(codec_str).upper()
    parts = result.split('.')
    if len(parts) > 0:
        result = parts[0].strip()
    else:
        return None
    if 'NONE' == result:
        return None
    if str(0) in result:
        prefix = result.rstrip('0123456789')
        result = prefix + str(int(result[len(prefix):]))
    return result
```
Output:
```json
{
    "Suitable": true,
    "Reason": "The function has meaningful logic and can be used to generate an instruction."
}
```
Example 3: Suitable (Complex Logic)
```python
def process_transcription_response(response):
    words_list = []
    # Iterate directly over the results.
    for result in response.results:
        # Ensure there is at least one alternative.
        if not result.alternatives:
            continue
        alternative = result.alternatives[0]
        # Each alternative has a repeated field "words"
        for word_info in alternative.words:
            words_list.append(word_info)

    # Build the overall transcript by joining the word strings.
    final_transcript = " ".join(word.word for word in words_list)

    # Now, segment the transcript based on punctuation.
    segments = []
    current_words = []
    segment_start = None
    segment_end = None
    punctuation_marks = {".", "?", "!"}

    for word in words_list:
        # Mark the start of a segment if not already set.
        if segment_start is None:
            segment_start = word.start_time
        segment_end = word.end_time
        current_words.append(word.word)

        # End the segment when a word ends with punctuation.
        if word.word and word.word[-1] in punctuation_marks:
            segments.append({"start": segment_start, "end": segment_end, "text": " ".join(current_words)})
            current_words = []
            segment_start = None
            segment_end = None

    # Add any remaining words as a segment.
    if current_words:
        segments.append({"start": segment_start, "end": segment_end, "text": " ".join(current_words)})

    return segments, final_transcript
```
Output:
```json
{
    "Suitable": true,
    "Reason": "The function has meaningful complexity and demonstrates clear logic, making it suitable for generating an instruction."
}
```
## Note
- Ensure that your analysis is thorough and considers all aspects of the function.
- Provide clear and concise reasoning for your decision.
- Only return the Json.
"""

GROUNG_TRUTH_FILTER_PROMPT_JAVA = """
## Task Description
You are an expert in Java programming and code analysis. Your task is to determine whether a given Java function is suitable for generating an instruction (question) or for use as a benchmark problem.  
You must analyze the function based on its characteristics, functionality, and adherence to specific criteria. If the function meets the criteria, it is deemed suitable; otherwise, it is not.

## Criteria for Suitability

### 1. Function Parameters
- **Basic Types Only**: The function's parameters must be basic Java types (e.g., `int`, `double`, `float`, `boolean`, `char`, `String`, `List`, `Map`, arrays, etc.).
  - If the parameters include custom classes or unknown types, the function is **not suitable**.
  - If the function relies on methods or fields of unknown objects, the function is **not suitable**.

### 2. Function Complexity
- **Meaningful Complexity**: The function should provide a meaningful test of the model's capabilities.
  - If the function is very long but its logic is trivial or repetitive, it is **not suitable**.
  - If the function is too simple (e.g., a basic getter/setter, or trivial business logic), it is **not suitable**.
  - If the function lacks clear logic or purpose, it is **not suitable**.

### 3. Side Effects and Dependencies
- **No Side Effects**: The function should not have side effects (e.g., modifying global/static variables, writing to files, printing to console, etc.).
- **No External Dependencies**: The function should not depend on external libraries or custom classes (except for standard Java library types).
  - If the function uses domain-specific types (e.g., `Tensor`, `DataFrame`) without explicit type hints or imports, it is **not suitable**.

### 4. Error Handling and Edge Cases
- **No Error Handling**: The function should not handle exceptions.

### 5. Domain Knowledge
- **General Applicability**: The function should not require highly specialized domain knowledge to understand or use.
  - If the function is tied to a specific application or domain that is not generalizable, it is **not suitable**.

### 6. Property-Based Testing
- **Constructible Inputs**: The function should be testable using property-based testing (e.g., generating random inputs to test behavior).
  - If the function cannot be tested in this way (e.g., requires specific hardware, or non-deterministic behavior), it is **not suitable**.

## Output Format
If the function is **suitable**, return:
```json
{
    "Suitable": true,
    "Reason": "The function meets all criteria for generating an instruction."
}
```
If the function is **not suitable**, return:
```json
{
    "Suitable": false,
    "Reason": "The reason why the function is not suitable for generating an instruction."
}
```

## Examples

### Example 1: Not Suitable (Trivial Logic)
```java
public int getValue() {
    return value;
}
```
Output:
```json
{
    "Suitable": false,
    "Reason": "The function is too simple, lacking meaningful complexity to test the model's capabilities."
}
```

### Example 2: Suitable (Meaningful Logic)
```java
public static String normalizeCodec(String codecStr) {
    String result = codecStr.toUpperCase();
    String[] parts = result.split("\\.");
    if (parts.length > 0) {
        result = parts[0].trim();
    } else {
        return null;
    }
    if ("NONE".equals(result)) {
        return null;
    }
    if (result.matches(".*\\d.*")) {
        String prefix = result.replaceAll("\\d+$", "");
        String number = result.substring(prefix.length());
        result = prefix + Integer.parseInt(number);
    }
    return result;
}
```
Output:
```json
{
    "Suitable": true,
    "Reason": "The function has meaningful logic and can be used to generate an instruction."
}
```

### Example 3: Suitable (Complex Logic)
```java
public static List<String> extractEmailDomains(String text) {
    Set<String> domains = new HashSet<>();
    Pattern emailPattern = Pattern.compile("[a-zA-Z0-9._%+-]+@([a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})");
    Matcher matcher = emailPattern.matcher(text);
    while (matcher.find()) {
        domains.add(matcher.group(1));
    }
    List<String> result = new ArrayList<>(domains);
    Collections.sort(result);
    return result;
}
```
Output:
```json
{
    "Suitable": true,
    "Reason": "The function has meaningful logic and can be tested with property-based testing, making it suitable for a benchmark."
}
```

### Example 4: Not Suitable (Custom Dependency)
```java
public int processData(CustomType data) {
    return data.computeValue();
}
```
Output:
```json
{
    "Suitable": false,
    "Reason": "The function depends on a custom type (CustomType), making it not suitable for a benchmark."
}
```

## Note
- Ensure that your analysis is thorough and considers all aspects of the function.
- Provide clear and concise reasoning for your decision.
- Only return the JSON output in the specified format.
"""