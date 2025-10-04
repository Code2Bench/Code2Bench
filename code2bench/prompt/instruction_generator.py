JAVA_INSTRUCTION_EDITOR_PROMPT = """
You are an automated document editor. Your task is to precisely refine a set of structured editing instructions to a given code documentation to produce a corrected version. Based on the feedback provided in the JSON, refine the original documentation. But do not simiplify the documentation, cause the documentation is used to evaluate the code generation capabilities of a model, so accuracy and clarity are paramount.

**Given Code:**
{ground_truth_code}

**Original Documentation:**
```code
/**
 * {original_documentation}
 */
```

**Editing Instructions (JSON format):**
```json
{review_feedback_json}
```

**Note:**
- Don't lose any important information or details from the original documentation and the 
- Output only the complete, final documentation, including any required opening/closing markers. Do not add any other text or explanation.
"""

JAVA_INSTRUCTION_REVIEWER_PROMPT = """
You are a meticulous Quality Assurance (QA) architect and senior Software Engineer, specializing in validating technical documentation against source code. Your task is to review generated specifications for given methods (used to evaluate other models' code generation capabilities) and provide structured, actionable feedback for improvement.

## Input Format:
**Ground-Truth Method:**
```code
{ground_truth_code}
```

**Generated Specification to Review:**
```code
/**
 * {generated_specification}
 */
```

## Your Task:
Carefully compare the specification of the ground-truth code. For each of the following checklist items, determine if the specification is accurate and complete.
► DO NOT suggest stylistic improvements, rephrasings, or optional additions.
► DO NOT hallucinate exceptions, parameters, or behaviors not in the code.
► DO report if the specification:
   - Misdescribes the core functionality
   - Omits critical boundary conditions (null, empty, limits, magic numbers)
   - Leaks internal implementation (e.g., variable names, algorithm steps)
   - Has hallucinated details not present in the code

► For each issue found, output an object with:
   - "category": one of [
        "functional_correctness",
        "boundary_conditions",
        "exception_handling",
        "parameter_and_return",
        "implementation_leakage",
        "critical_constants_and_rules",
        "hallucination"
     ]
   - "feedback": a clear, concise explanation of the issue and what the correct text should be.

► If no issues found, output an empty "issues" array.

## Output Format:
Output ONLY a JSON object in this exact format. No explanations. No extra fields.
If there are no issues, output an empty array in the values field.
```json
{
  "issues": [
    { "category": "...", "feedback": "..." },
    ...
  ]
}
```
"""

JAVA_INSTRUCTION_REVIEWER_PROMPT_V0 = """
You are a meticulous Quality Assurance (QA) architect and senior Software Engineer, specializing in validating technical documentation against source code. Your task is to review generated specifications for given methods (used to evaluate other models' code generation capabilities) and provide structured, actionable feedback for improvement.

**Ground-Truth Method:**
```java
{ground_truth_code}
```

**Generated Specification to Review:**
```java
/**
 * {generated_specification}
 */
```

**Your Task:**
Carefully compare the specification of the ground-truth code. For each of the following checklist items, determine if the specification is accurate and complete.
- If an item is perfect, set its "status" to "OK".
- If there is an issue, set its "status" to "ISSUE" and provide a **clear, concise "feedback"** explaining what is wrong and **what the corrected text should be**.

**Output your final review as a single JSON object.** Only add feedback if status is ISSUE.

**JSON Output Format:**
```json
{
  "functional_correctness": {
    "status": "[OK or ISSUE]"
  },
  "boundary_conditions": {
    "status": "[OK or ISSUE]"
  },
  "exception_handling": {
    "status": "[OK or ISSUE]"
  },
  "parameter_and_return": {
    "status": "[OK or ISSUE]",
  },
  "critical_constants_and_rules": {
    "status": "[OK or ISSUE]",
    "feedback": ""
  },
  "implementation_leakage": {
    "status": "[OK or ISSUE]",
    "feedback": "..."
  }
}
```
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_JAVA = """
You are an expert Java architect and technical writer, specializing in creating high-quality, professional Javadoc documentation. Your task is to generate a precise and informative Javadoc for a given Java method, enabling another senior Java developer to re-implement it accurately within a complete, self-contained `Tested.java` file.

## Core Objective
The generated Javadoc and method signature must serve as a perfect "specification" for the provided ground-truth method.

## Requirements
1. Core Description Fidelity: The Javadoc must accurately reflect the method's behavior, including the precise sequence of checks, conditions, and resulting actions within the code.
2. Edge Cases: Detail how the method handles edge cases, such as null, empty, or special/magic values.
3. Data Structures: Accurately describe parameters and return values using standard Java types.
4. Javadoc Refinement: If the method already has a Javadoc, your primary goal is to refine and enhance it to meet these high standards. Integrate existing accurate information with your new insights. Do not discard valuable details from the original author.
5. Example Handling:
    * If the original Javadoc contains an example (e.g., in a `<pre>{@code ...}</pre>` block): Preserve the original example verbatim.
    * If not: Omit any example section entirely.

## Input Structure
```java
{ground_truth_java_method_code}
```

## Output Structure
Return a single `<signature>` tag containing a complete, self-contained, and runnable `Tested.java` file content. The content must be enclosed in a ```java` code block and include all necessary imports, the generated Javadoc, the `public class Tested`, and the public static method signature with a `// TODO: implement this method` comment.

<signature>
```java
// All necessary imports (e.g., java.util.*) should be here.
import java.util.List;
import java.util.Map;

public class Tested {
    /**
     * High-quality, Google-style Javadoc goes here.
     *
     * param parameterName Description, including nullability and constraints.
     * return Description of the return value.
     * throws SpecificExceptionType if a specific error occurs.
     */
    public static ReturnType methodName(ParameterType parameterName) {
        // TODO: implement this method
    }
}
```
</signature>

## Final Instructions
- Ensure the method signature in the `<signature>` tag perfectly matches the ground truth, including visibility (`public static`), return type, method name, and parameter types.
- Don't add implementation details.
- Include all necessary imports based on the types used in the signature.
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_JAVA_V0 = """
You are a programming documentation architect specializing in creating precise, implementation-agnostic specifications for Java methods. Your task is to generate a **complete, self-contained Java class file** named `Tested`. This class will contain a detailed Javadoc comment and a method signature, enabling accurate reimplementation in any programming language. This output will be used to evaluate the code generation capabilities of a model.

## Requirements
1.  **Core Description Fidelity**: The Javadoc must accurately reflect the method's behavior and describe the task it solves. **Pay close attention to the sequence of checks, conditions, and resulting actions within the code.**
2.  Highlight any **special rules** that affect the model's correct understanding of the method's behavior, such as:
    *   Recursive behavior
    *   Edge cases or type-specific handling (e.g., null checks, empty collections, index out of bounds)
    *   Magic numbers or constants (e.g., indentation of `2` or `8` spaces).
    *   Specific keywords or patterns the logic depends on (e.g., `"def "`, `":"`, `","`).
3.  **Language-Agnostic Terminology**: Use universal concepts for types and logic in the Javadoc.
    *   Describe parameters and return values using **conceptual types** (e.g., "a list of text strings", "an integer") instead of Java-specific types (`List<String>`, `int`).
    *   Describe operations conceptually (e.g., "checks if the line ends with a specific character", "iterates backward through the list") rather than Java-specific calls (`previousLine.trim().endsWith(",")`, `for (int i = lineIndex - 1; i >= 0; i--)`).
4.  **Javadoc Refinement**: If the method already has a Javadoc comment, integrate and refine its content to meet these requirements. Do not discard existing accurate information.
5.  **Conditional Example Handling**:
    *   **If the original Javadoc contains an example** (e.g., in a `<pre>{@code ...}</pre>` block or as plain text):
        *   Preserve the original example **verbatim** in the final Javadoc.
    *   **If the original Javadoc has no examples**:
        *   **Omit any example section entirely**.

## **Input Structure**
```java
{ground_truth_java_method_code}
```

## **Output Structure**
Only return a single `<signature>` tag. Inside this tag, provide a complete, self-contained Java class named `Tested`. The class must contain all necessary imports, the generated Javadoc, and the method signature with a `// TODO: implement this method` comment in its body. The entire content must be enclosed in a ```java` code block.

### Example output:
<signature>
```java
import java.util.List;
// Other necessary imports...

public class Tested {
    /**
     * Javadoc in Google Style goes here.
     *
     * @param parameterName Description of the parameter.
     * @return Description of the return value.
     */
    public static ReturnType methodName(ParameterType parameterName) {
        // TODO: implement this method
    }
}
```
</signature>

### Example Input
<Function>
```java
import java.util.List;

public class StringUtils {
    /**
     * Joins a list of strings with a separator.
     * @param parts The strings to join.
     * @param separator The separator to use between parts.
     * @return The resulting string.
     */
    public static String join(List<String> parts, String separator) {
        if (parts == null || parts.isEmpty()) {
            return "";
        }

        StringBuilder result = new StringBuilder();
        for (int i = 0; i < parts.size(); i++) {
            result.append(parts.get(i));
            if (i < parts.size() - 1) {
                result.append(separator);
            }
        }
        return result.toString();
    }
}
```
</Function>
### Example Output
<signature>
```java
import java.util.List;

public class Tested {
    /**
     * Concatenates a sequence of text strings using a specified separator.
     *
     * This method handles edge cases by first checking if the input list is null or empty.
     * If it is, an empty string is returned immediately. Otherwise, it iterates through
     * the list, appending each string to the result. The separator is inserted between
     * elements, but not after the final element.
     *
     * @param parts A list of text strings to be joined. Can be null or empty.
     * @param separator The text string to use as a separator between the parts.
     * @return A single text string consisting of the joined parts, or an empty string
     *         if the input list is null or empty.
     */
    public static String join(List<String> parts, String separator) {
        // TODO: implement this method
    }
}
```
</signature>

## Note:
- Ensure all necessary imports, based on the method's parameters and return types, are included at the top of the Java code block, before the `public class Tested` declaration.
- Function should be public and static.
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_JAVA_V0 = """
You are a programming documentation architect specializing in creating precise, implementation-agnostic specifications for Java methods. Generate a docstring comment that enables accurate reimplementation in any programming language. This docstring will be used to evaluate the code generation capabilities of a model.

## Requirements
1.  **Core Description Fidelity**: The docstring must accurately reflect the method's behavior and describe the task this method solves. **Pay close attention to the sequence of checks, conditions, and resulting actions within the code.**
2.  Highlight any **special rules** that affect the model's correct understanding of the method's behavior, such as:
    *   Recursive behavior
    *   Edge cases or type-specific handling (e.g., null checks, empty collections)
    *   Magic numbers or constants
    *   Special settings that may affect the difficulty for others to correctly implement methods based on Javadocs. e.g., the Ground Truth method may add some special string at the end of the result, so the docstring should mention this case, otherwise, the model may not be able to implement the method correctly.
3.  **Language-Agnostic Terminology**: Use universal concepts for types and logic.
    *   Describe parameters and return values using **conceptual types** (e.g., "a list of text strings", "an integer", "a boolean value") instead of language-specific type hints (`List<String>`, `int`, `boolean`).
    *   Describe operations conceptually (e.g., "iterates over the elements", "checks if the collection is empty", "appends a string to a builder") rather than Java-specific calls (`for (String s : parts)`, `parts.isEmpty()`, `sb.append(separator)`).
4.  **docstring Refinement**: If the method already has a docstring comment, integrate and refine its content to meet these requirements. Do not discard existing accurate information.
5.  **Conditional Example Handling**:
    *   **If the original docstring contains an example** (e.g., in a `<pre>{@code ...}</pre>` block):
        *   Preserve the original example **verbatim** in the final docstring.
        *   Format it clearly.
    *   **If the original docstring has no examples**:
        *   **Omit any example section entirely**. You must infer the method's behavior solely from the provided source code.

## **Input Structure**
```java
{ground_truth_java_method_code}
```

## **Output:**
Only return the docstring content in `<docstring>` tags and the method signature in the `<signature>` tags. The docstring should be enclosed in a standard docstring block (`/** ... */`). The method signature should be formatted in a ```java` code block with the method name and a TODO comment indicating where the implementation should go.

### Example output:
<docstring>
/**
 * docstring in Google Style goes here.
 *
 * @param parameterName Description of the parameter.
 * @return Description of the return value.
 */
</docstring>
<signature>
```java
public static ReturnType methodName(ParameterType parameterName) {
    // TODO: implement this method
}
```
</signature>

### Example Input
<Function>
```java
import java.util.List;

public class StringUtils {
    /**
     * Joins a list of strings with a separator.
     * @param parts The strings to join.
     * @param separator The separator to use between parts.
     * @return The resulting string.
     */
    public static String join(List<String> parts, String separator) {
        if (parts == null || parts.isEmpty()) {
            return "";
        }

        StringBuilder result = new StringBuilder();
        for (int i = 0; i < parts.size(); i++) {
            result.append(parts.get(i));
            if (i < parts.size() - 1) {
                result.append(separator);
            }
        }
        return result.toString();
    }
}
```
</Function>
### Example Output
<docstring>
/**
 * Concatenates a sequence of text strings using a specified separator.
 *
 * This method handles edge cases by first checking if the input list is null or empty.
 * If it is, an empty string is returned immediately. Otherwise, it iterates through
 * the list, appending each string to the result. The separator is inserted between
 * elements, but not after the final element.
 *
 * @param parts A list of text strings to be joined. Can be null or empty.
 * @param separator The text string to use as a separator between the parts.
 * @return A single text string consisting of the joined parts, or an empty string
 *         if the input list is null or empty.
 */
</docstring>
<signature>
```java
import java.util.List;

public static String join(List<String> parts, String separator) {
    // TODO: implement this method
}
```
</signature>

## Note:
- Only add examples in the docstring when the original method already has an example section in its docstring.
- If the method signature includes imports, ensure they are present in the final signature block.
"""


JAVA_INSTRUCTION_GENERATOR_PROMPT = """
You are a senior Java developer and technical interviewer. Your task is to:
1. Convert the provided Python function into an idiomatic Java static method within a public class named Tested.
2. Generate a complete and clear problem description in Markdown.
3. Select the most representative test cases from provided examples

### Requirements

1. **Function Conversion**:
   - Create a public static method in a public class Tested that mimics the behavior of the Python function
   - Use appropriate Java types such as List<Map<String, Object>>, Map<String, Object>, etc.
   - Add a placeholder implementation using // TODO: Implement this
   - Ensure the method name matches the original Python function name
   - The method should be callable as Tested.function_name(...)

2. **Problem Description**:
   - Write a clear and concise Markdown description of what the method should do
   - Include input/output specifications
   - Describe logic and any edge cases to consider
   - Keep it clear and developer-friendly, as if it's for a technical interview or coding assessment

3. **Test Case Selection**:
   - From the provided examples, select the most useful and illustrative ones
   - Prioritize:
       - Normal cases
       - Edge cases (e.g., empty lists, null values)
       - Validation or corner logic
   - Eliminate redundant or overly similar test cases

---

### Output Format
```json
{
  "Function": "Complete Java method with TODOs inside a public class Tested",
  "Function Name": "Function name (same as the original Python one)",
  "Instruction": "Problem description in Markdown format",
  "Examples": ["Selected input/output examples"]
}

## Example
### Input Python Function:
```python
def _change_metrics_format_for_payload(metrics):
    formatted_metrics = []
    for metric in metrics:
        if any(m["name"] == metric.get("displayName") or m['name'] == metric.get("name") for m in formatted_metrics):
            continue
        metric_display_name = metric["name"]
        if metric.get("displayName"):
            metric_display_name = metric['displayName']
        formatted_metrics.append({
            "name": metric_display_name,
            "displayName": metric_display_name,
            "config": {"source": "user"},
        })
    return formatted_metrics
```

### Available Test Cases:
{{inputs_outputs}}

### Expected Output:
```json
{
  "Function": "public class Tested {\n    public static List<Map<String, Object>> _change_metrics_format_for_payload(List<Map<String, Object>> metrics) {\n        // TODO: Implement this function\n        return new ArrayList<>();\n    }\n}",
  "Function Name": "_change_metrics_format_for_payload",
  "Instruction": "### Problem Description\n\nImplement a method `_change_metrics_format_for_payload` in Java that processes a list of metric maps and returns a standardized format.\n\n#### Input:\n- `metrics`: A list of maps. Each map may contain a `name` and optionally a `displayName` field.\n\n#### Output:\n- A list of formatted metric maps. Each map should include:\n  - `name`: derived from `displayName` if present, otherwise from `name`\n  - `displayName`: same as the final name\n  - `config`: a map with `{ \"source\": \"user\" }`\n\n#### Requirements:\n- Remove duplicates based on `name` or `displayName` match\n- Preserve the order of the first unique appearance\n- Handle missing `displayName` values gracefully\n- Return an empty list if the input is empty\n\n#### Edge Cases:\n- Empty input\n- Items with only `name`\n- Duplicate names or displayNames",
  "Examples": [
    {
      "Description": "Normal case with unique metrics",
      "Input": [
        {"name": "cpu_usage", "displayName": "CPU Usage"},
        {"name": "mem_usage", "displayName": "Memory Usage"}
      ],
      "Output": [
        {"name": "CPU Usage", "displayName": "CPU Usage", "config": {"source": "user"}},
        {"name": "Memory Usage", "displayName": "Memory Usage", "config": {"source": "user"}}
      ]
    },
    {
      "Description": "Edge case - empty input",
      "Input": [],
      "Output": []
    },
    {
      "Description": "Duplicate handling",
      "Input": [
        {"name": "cpu", "displayName": "Processor"},
        {"name": "cpu", "displayName": "CPU"}
      ],
      "Output": [
        {"name": "Processor", "displayName": "Processor", "config": {"source": "user"}}
      ]
    }
  ]
}
```
"""

TS_INSTRUCTION_GENERATOR_PROMPT = """
You are a senior TypeScript developer and technical interviewer. Your task is to:
1. Convert the provided Python function into an idiomatic TypeScript function template with TODOs for implementation.
2. Generate a complete and clear problem description in Markdown.
3. Select the most representative test cases from provided examples.

### Requirements

1. **Function Conversion**:
   - Create a TypeScript function signature that mimics the behavior of the Python function
   - Use appropriate TypeScript types and interfaces (e.g., `Record<string, any>`, `unknown[]`, `string | undefined`)
   - Add placeholder implementation with `// TODO: Implement this`
   - Include necessary imports or helper types (if applicable)
   - Export the function using export so it can be used in other modules.

2. **Problem Description**:
   - Write a clear and concise Markdown description of what the function should do
   - Include input/output specifications
   - Describe logic and any edge cases to consider
   - Keep it clear and developer-friendly, as if it's for a technical exercise

3. **Test Case Selection**:
   - From the provided examples, select the most useful and illustrative ones
   - Prioritize:
     * Normal cases
     * Edge cases (e.g. empty arrays, null values)
     * Validation or corner logic
   - Eliminate redundant or similar test cases

---

### Output Format
```json
{
    "Function": "Complete TypeScript function signature with TODOs",
    "Function Name": "Function name (same as the original Python one)",
    "Instruction": "Problem description in Markdown format",
    "Examples": ["Selected input/output examples"]
}

## Example
### Input Python Function:
```python
def _change_metrics_format_for_payload(metrics):
    formatted_metrics = []
    for metric in metrics:
        if any(m["name"] == metric.get("displayName") or m['name'] == metric.get("name") for m in formatted_metrics):
            continue
        metric_display_name = metric["name"]
        if metric.get("displayName"):
            metric_display_name = metric['displayName']
        formatted_metrics.append({
            "name": metric_display_name,
            "displayName": metric_display_name,
            "config": {"source": "user"},
        })
    return formatted_metrics
```

### Available Test Cases:
{{inputs_outputs}}

### Expected Output:
```json
{
    "Function": "export function _change_metrics_format_for_payload(metrics: Array<Record<string, any>>): Array<Record<string, any>> {\n    // TODO: Implement this function\n    return [];\n}",
    "Function Name": "_change_metrics_format_for_payload",
    "Instruction": "### Problem Description\n\nImplement a function `_change_metrics_format_for_payload` in TypeScript that processes an array of metric objects and returns a standardized format.\n\n#### Input:\n- `metrics`: An array of objects. Each object may have `name` and optionally `displayName` fields.\n\n#### Output:\n- An array of formatted metric objects. Each object should include:\n  - `name`: derived from `displayName` if present, otherwise `name`\n  - `displayName`: same as the final name\n  - `config`: an object with `{ source: 'user' }`\n\n#### Requirements:\n- Remove duplicates based on `name` or `displayName` matches\n- Preserve the order of the first unique appearance\n- Handle missing `displayName` gracefully\n- Return an empty array if input is empty\n\n#### Edge Cases:\n- Empty input\n- Items with only `name` but no `displayName`\n- Multiple items with duplicate `name` or `displayName` values",
    "Examples": [
        {
            "Description": "Normal case with unique metrics",
            "Input": [
                {"name": "cpu_usage", "displayName": "CPU Usage"},
                {"name": "mem_usage", "displayName": "Memory Usage"}
            ],
            "Output": [
                {"name": "CPU Usage", "displayName": "CPU Usage", "config": {"source": "user"}},
                {"name": "Memory Usage", "displayName": "Memory Usage", "config": {"source": "user"}}
            ]
        },
        {
            "Description": "Edge case - empty input",
            "Input": [],
            "Output": []
        },
        {
            "Description": "Duplicate handling",
            "Input": [
                {"name": "cpu", "displayName": "Processor"},
                {"name": "cpu", "displayName": "CPU"}
            ],
            "Output": [
                {"name": "Processor", "displayName": "Processor", "config": {"source": "user"}}
            ]
        }
    ]
}
```

### Notes:
- Keep function names unchanged from Python (even if it starts with an underscore).
- Do not implement the function; only provide a valid TS signature with a TODO.
- Make sure to return valid JSON (especially escaping newlines properly).
- Ensure the problem description is Markdown-ready and suitable for coding platforms or interviews.
"""

GO_INSTRUCTION_GENERATOR_PROMPT = """
You are a senior Go language expert and technical interviewer. Your task is to:
1. Convert the provided Python function into an idiomatic Go function template with TODOs for implementation.
2. Generate a complete problem description
3. Select the most representative test cases from provided examples

### Requirements
1. **Function Conversion**:
   - Create a Go function signature that matches the Python function's behavior
   - Use appropriate Go conventions (type assertions, error handling, etc.)
   - Mark incomplete sections with `// TODO: Implement this`
   - Include necessary package imports

2. **Problem Description**:
   - Clearly explain the function's purpose in Markdown format
   - Specify input/output requirements
   - List any edge cases or special considerations

3. **Test Case Selection**:
   - Choose representative examples from those provided
   - Prioritize cases that demonstrate:
     * Normal operation
     * Edge cases
     * Input validation
   - Exclude redundant or less illustrative examples

### Output Format
```json
{
    "Function": "Complete Go function signature with TODOs",
    "Funcion Name": "Function name",
    "Instruction": "Clear problem description in Markdown",
    "Examples": ["Selected input/output examples"]
}

## Example
### Input Python Function:
```python
def _change_metrics_format_for_payload(metrics):
    formatted_metrics = []
    for metric in metrics:
        if any(m["name"] == metric.get("displayName") or m['name'] == metric.get("name") for m in formatted_metrics):
            continue
        metric_display_name = metric["name"]
        if metric.get("displayName"):
            metric_display_name = metric['displayName']
        formatted_metrics.append({
            "name": metric_display_name,
            "displayName": metric_display_name,
            "config": {"source": "user"},
        })
    return formatted_metrics
```
### Available Test Cases:
{{inputs_outputs}}

### Expected Output:
```json
{
    "Function": "func _change_metrics_format_for_payload(metrics []map[string]interfac{}) []map[string]interface{} {
        // TODO: Implement the function logic
    }",
    "Funcion Name": "_change_metrics_format_for_payload",
    "Instruction": "Please implement a function _change_metrics_format_for_payload, which processes raw metrics into standardized format:\n\n1. **Input**: Slice of metric maps with optional 'name' and 'displayName'\n2. **Output**: Slice of formatted metrics with:\n   - Unified 'name' and 'displayName' fields\n   - Added 'config' with source=\"user\"\n3. **Requirements**:\n   - Skip duplicates (match by either name or displayName)\n   - Use displayName if present, fallback to name\n   - Preserve original order\n4. **Edge Cases**:\n   - Handle empty input\n   - Process metrics missing displayName",
    "Examples": [
        {
            "Description": "Normal case with unique metrics",
            "Input": [
                {"name": "cpu_usage", "displayName": "CPU Usage"},
                {"name": "mem_usage", "displayName": "Memory Usage"}
            ],
            "Output": [
                {"name": "CPU Usage", "displayName": "CPU Usage", "config": {"source": "user"}},
                {"name": "Memory Usage", "displayName": "Memory Usage", "config": {"source": "user"}}
            ]
        },
        {
            "Description": "Edge case - empty input",
            "Input": [],
            "Output": []
        },
        {
            "Description": "Duplicate handling",
            "Input": [
                {"name": "cpu", "displayName": "Processor"},
                {"name": "cpu", "displayName": "CPU"}
            ],
            "Output": [
                {"name": "Processor", "displayName": "Processor", "config": {"source": "user"}}
            ]
        }
    ]
}
```
## Note: 
- Don't modify the function name, the function name should be the same as the original Python function.
- Don't implement the function in Go, just provide the function signature and TODOs.
- Ensure the generated JSON is valid.
"""

DOCSTRING_INSTRUCTION_GENERATOR_PROMPT = """
## Task Description
You are an expert in code understanding and task specification. You will be given:
1. A Python function implementation.
2. Several example usages that describe **what the function does** in specific scenarios.

Your task is to generate a **comprehensive docstring** for this function that captures its purpose, inputs, outputs, special rules, and a representative example, which can be used for testing.

### Docstring Requirements
The generated docstring should:
- Start with a concise **one-sentence summary** of the function’s purpose.
- Include:
  - **Parameters**: Names and expected types.
  - **Returns**: Description of return value and its type.
  - **Behavior rules**: Recursive logic, merge strategies, edge cases, or transformation details.
- End with a **representative usage example** (using `>>>` style).
- Be suitable for insertion directly into the function as a Python docstring.

### Input Format
You will be given:
- <Function>Python function implementation</Function>
- <Example Usage>[{{"Description": "...", "Inputs": {{...}}}}, ...]</Example Usage>

### Output Format
Return a single valid Python function signature with a docstring that meets the above requirements in <signature> tag.

### Example
#### Input
<Function>
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
</Function>

<Example Usage>
[
    {
        "Description": "Merge two simple dictionaries",
        "Inputs": {
            "base": {"a": 1, "b": 2},
            "update": {"b": 3, "c": 4}
        }
    },
    {
        "Description": "Merge two nested dictionaries",
        "Inputs": {
            "base": {"a": {"b": 1, "c": 2}},
            "update": {"a": {"c": 3, "d": 4}, "e": 5}
        }
    },
    {
        "Description": "Merge two lists",
        "Inputs": {
            "base": [1, 2, 3],
            "update": [4, 5, 6]
        }
    }
]
</Example Usage>

#### Output
<signature>
```python
def merge_json_recursive(base, update):
    \"\"\"
    Recursively merge two hierarchical data structures (dictionaries, lists, or primitives).

    This function takes two structured data inputs and merges them recursively:
    - If both inputs are dictionaries, their keys are merged recursively.
    - If both inputs are lists, they are concatenated.
    - If inputs are other types, the second input overwrites the first.

    Parameters:
        base (dict | list | any): The original structured object.
        update (dict | list | any): The object to merge into the base.

    Returns:
        The merged object, maintaining structure and applying the above merging rules.

    Example:
    >>> base = {"a": {"b": 1, "c": 2}, "x": [1, 2]}
    >>> update = {"a": {"c": 3, "d": 4}, "x": [3, 4], "e": 5}
    >>> merge_json_recursive(base, update)
    {'a': {'b': 1, 'c': 3, 'd': 4}, 'x': [1, 2, 3, 4], 'e': 5}
    \"\"\"
    pass
```
</signature>
"""

WEAKLY_SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT = """
You are a python programming expert who is refining docstrings in existing programs. You will be given a python function in a python file with an existing (possibly underspecified) docstring with corresponding some input-output examples extracted. Your goal is to refine the associated docstring by making it more informative, precise and complete without adding verbosity or detailed programming logic to the docstring. When there is a docstring, the docstring is used to evaluate the code generation capabilities of a model.

The docstring should particularly describe the format and types of the expected inputs and output as well as the behavior of the function. Do not guess outputs for functions. Finally, do not throw away existing details from the docstrings and only insert content you are sure about. Do NOT have repeated content in the docstring and ONLY describe the high-level function behavior without going into implementation details.

## Requirements
1. **Core Description Fidelity**: The docstring must accurately reflect the function's behavior and describes the task this function solves. **Pay close attention to the sequence of checks, conditions, and resulting actions within the code.
2. ** Highlight any **special rules** that affect the model's correct understanding of the function's behavior, such as:
  - Recursive behavior
  - Merging, flattening, filtering, transformation logic
  - Edge cases or type-specific handling
  - Magic numbers or constants
3.  **Docstring Refinement**: If the function already has a docstring, integrate and refine its content to meet these requirements. Do not discard existing accurate information.
4.  **Conditional Example Handling**:
You should judge whether to include examples based on the original docstring's content:
  - **If the original docstring contains an `Examples` section**:
    - Preserve all original examples **verbatim** in the final docstring's `Examples` section.
    - Format them clearly in Language-Agnostic(e.g., showing input and expected output).
    - Do **not** add or modify examples from the `Example Usages` data.
  - **If the original docstring has no `Examples` section**:
    - **Omit the Examples section entirely**, even if `Example Usages` data is provided. The `Example Usages` data should be used *internally* by you to understand the code's behavior for description purposes, but not included in the final docstring's `Examples` section.

## Input
```python
{ground_truth_function_code}
```

### Output Format
- Return the docstring in <docstring> tags following the Google-style format.
- Include the function signature in <signature> tags, with a TODO placeholder for the implementation.
#### Example output:
<docstring>
\"\"\" Docstring content here. \"\"\"
</docstring>
<signature>
```python
import numpy as np

def example_function(param1: int, param2: np.ndarray) -> np.ndarray:
    # TODO: Implement this function
    pass
</signature>

## Note
- Only add examples in Docstring when the function already has an `Examples` section in the docstring. Do not add examples from the `Example Usages` data if the original docstring does not contain `Examples`.
- If the signature has type hints, import nessesary types from the standard library (e.g., `from typing import List, Dict`) in signature.
"""

WEAKLY_SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v0 = """
## Task Description
You are an expert in code understanding and problem formulation. Your task is to generate a Python-specific instruction that describes the core functionality of a given Python function (`func0`), which depends only on standard libraries or specific external libraries (e.g., NumPy, re) and no other custom modules. The instruction will be used to evaluate a model's ability to understand Python requirements and generate equivalent code.

### Instruction Format
The instruction must:
- Clearly describe the **main functionality** of `func0` in a concise manner, tailored for Python.
- Specify the **input types** (e.g., integers, NumPy arrays, strings) and **output type**, using Python type names (e.g., `numpy.ndarray`, `List[str]`).
- Be **Python-specific**: Use Python terminology for types and behaviors, but avoid implementation details or specific syntax beyond type names.
- Be **precise and general-purpose**, guiding implementation in Python while capturing all critical behavior.

### Input Format
- **Function**: Python function code for `func0`, including docstring (if available) and any import statements for external libraries (e.g., `import numpy as np`, `import re`).
- Example structure:
```python
import numpy as np
def func0(param1: int, param2: np.ndarray) -> np.ndarray:
    # Function implementation
```
### Output Format
- Instruction: A Python-specific description of func0’s functionality, including inputs, outputs, and special rules, in <instruction> tags.
- Function Signature: The Python function signature with import statements for all used external libraries, type annotations, and a TODO placeholder, in <signature> tags.

## Example
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
#### Output
<instruction>
Implement a Python function that extracts unique domain names from email addresses within a text string.

- **Input**: A string containing zero or more email addresses, mixed with arbitrary text.
- **Output**: A sorted `list[str]` of unique domain names extracted from valid email addresses.
- **Special Rules**:
  - An email address consists of a username followed by '@' and a domain name (e.g., "user@domain.com").
  - A valid domain name includes alphanumeric characters, dots, and hyphens, ending with a top-level domain (at least two characters).
  - Extract only the domain part (e.g., "domain.com" from "user@domain.com") using regular expression matching.
  - Remove duplicates and sort the domains alphabetically.
  - Handle edge cases: empty strings, text without email addresses, or invalid email formats (e.g., "user@invalid").
</instruction>
<signature>
```python
import re

def extract_email_domains(text: str) -> list[str]:
    # TODO: Implement this function
    pass
```
</signature>

Input:
```python
import numpy as np

def chain_pair_pde( num_tokens: int, asym_ids: np.ndarray, full_pde: np.ndarray ) -> tuple[np.ndarray, np.ndarray]: 
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
#### Output
<instruction>
Implement a Python function that computes the average and minimum predicted distance errors for pairs of chains based on token assignments, using NumPy arrays.

- **Inputs**:
  - An integer specifying the number of tokens.
  - A `numpy.ndarray` of shape (num_tokens,) containing integer chain identifiers.
  - A `numpy.ndarray` of shape (num_samples, num_tokens, num_tokens) containing predicted distance errors.
- **Output**: A tuple of two `numpy.ndarray` objects, each of shape (num_samples, num_chains, num_chains), where:
  - The first array contains the average distance error for each pair of chains.
  - The second array contains the minimum distance error for each pair of chains.
- **Special Rules**:
  - Use only the first `num_tokens` elements of the chain identifiers array and the first `num_tokens` rows and columns of the distance error array.
  - Identify unique chain identifiers to determine the number of chains.
  - For each pair of chains, compute the average and minimum over the distance errors corresponding to tokens assigned to those chains.
  - Handle edge cases: zero tokens, single token, or single chain.
</instruction>
<signature>
```python
import numpy as np

def chain_pair_pde(num_tokens: int, asym_ids: np.ndarray, full_pde: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # TODO: Implement this function
    pass
```
</signature>
## Note
- The function name must match the original func0 name.
- Do not implement the function; provide only the instruction and function signature.
- Include import statements for all external libraries used by func0 (e.g., import numpy as np, import re) in the signature.
- Derive input constraints, output types, and special rules from the function’s code, docstring, and logic.
- Only return the instruction and function signature in the specified XML tag format.
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v12 = """
You are a programming documentation architect specializing in creating precise, implementation-agnostic specifications. Generate a docstring that enables accurate reimplementation in any programming language. When there is a docstring, the docstring is used to evaluate the code generation capabilities of a model.

## Requirements
1. **Core Description Fidelity**: The docstring must accurately reflect the function's behavior and describes the task this function solves. **Pay close attention to the sequence of checks, conditions, and resulting actions within the code.
2. ** Highlight any **special rules** that affect the model's correct understanding of the function's behavior, such as:
  - Recursive behavior
  - Merging, flattening, filtering, transformation logic
  - Edge cases or type-specific handling
  - Magic numbers or constants
2. **Language-Agnostic Terminology**: Use universal concepts for types and logic.
  - Describe parameters and return values using **conceptual types** (e.g., "an integer", "a boolean value", "a sequence of numbers", "a text string") instead of language-specific type hints (`int`, `bool`, `list`, `str`).
  - Describe operations conceptually (e.g., "checks if X contains Y", "iterates over the elements", "applies a function to each element") rather than Python built-ins (`s1.find("'")`, `s1.replace`).
3.  **Docstring Refinement**: If the function already has a docstring, integrate and refine its content to meet these requirements. Do not discard existing accurate information.
4.  Include **between 1 and 3 representative example usages** at the end of the docstring, formatted as `Input: ...\nOutput: ...` pairs. These examples must be derived **strictly from the provided Example Usages data** and formatted clearly. Select examples that best illustrate different aspects of the function's behavior.

## **Input Structure**
```python
{ground_truth_function_code}
```
### Example Usages:
{example_usage_data}
(Note: Example Usages will be provided in a format like input/output pairs.)

## **Output:**
Only return the docstring content in <docstring> tags and the function signature in the <signature> tags. The docstring should be enclosed in triple double quotes (`\"\"\"Docstring goes here\"\"\"`). The function signature should be formatted in ```python` code block with the function name and a TODO comment indicating where the implementation should go.

### Example output:
<docstring>
\"\"\"Google Style Docstring goes here\"\"\"
</docstring>
<signature>
```python
def function_name(arguments):
    # TODO: implement this function
    pass
```
</signature>

### Example Input
<Function>
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
</Function>
<Example Usage>
[
    {
        "Description": "Merge two simple dictionaries",
        "Inputs": {
            "base": {"a": 1, "b": 2},
            "update": {"b": 3, "c": 4}
        }
    },
    {
        "Description": "Merge two nested dictionaries",
        "Inputs": {
            "base": {"a": {"b": 1, "c": 2}},
            "update": {"a": {"c": 3, "d": 4}, "e": 5}
        }
    },
    {
        "Description": "Merge two lists",
        "Inputs": {
            "base": [1, 2, 3],
            "update": [4, 5, 6]
        }
    }
]
</Example Usage>
### Example Output
<docstring>
\"\"\"Recursively merge two JSON-like objects.

The function merges nested structures with the following rules:
- If both inputs are dictionaries, recursively merge them.
- If both inputs are lists, concatenate them.
- For all other cases, the update value overwrites the base value.
- The base object is left unmodified; a new merged object is returned.
Args:
    base: Base JSON-like object (dictionary, list, or primitive value).
    update: Update JSON-like object to merge into base.

Returns:
    A new JSON-like object containing merged content from base and update.

Examples:
    Input: base = {"a": 1, "b": 2}, update = {"b": 3, "c": 4}
    Output: {"a": 1, "b": 3, "c": 4}
\"\"\"
</docstring>
<signature>
```python
# There may be type annotations imported from the typing module, so we need to import it first when necessary. But when the function does not have type annotations, we don't need to import it.

def merge_json_recursive(base, update):
    # TODO: Implement this function
    pass
```
</signature>

## Note:
- If the signature has type hints, import nessesary types from the standard library (e.g., `from typing import List, Dict`) in signature.
"""

PYTHON_SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT = """
You are an expert Python programmer and technical writer, specializing in creating high-quality, PEP 257 compliant docstrings. Your task is to generate a precise and informative docstring for a given Python function, enabling another expert Python developer to re-implement it accurately.

## Core Objective
The generated docstring should be a perfect "specification" of the provided ground-truth function. It must capture not only the function's logic but also its engineering best practices, performance considerations, and idiomatic Python patterns.

## Requirements
1. Core Description Fidelity: The docstring must accurately reflect the function's behavior, including the precise sequence of checks, conditions, and resulting actions within the code.
2. Highlight "Pythonic" Nuances & Special Rules: Pay extremely close attention to and describe:
    * Idiomatic Patterns: Does the code use a particularly Pythonic and efficient pattern (e.g., list comprehensions, generator expressions, `collections.Counter`) instead of a naive loop? Describe the expected behavior, which might imply such an implementation.
    * Performance Considerations: If the code is clearly optimized for performance (e.g., avoiding string concatenation in a loop, using efficient data structures), the description should reflect the expectation of an efficient implementation.
    * Edge Cases & Error Handling: Detail how the function handles edge cases (e.g., empty lists, `None` inputs) or specific error conditions.
    * Data Structures: Accurately describe the expected data structures for parameters and return values, using standard Python type hints (e.g., `List[int]`, `Dict[str, Any]`).
3. Docstring Refinement: If the function already has a docstring, your primary goal is to refine and enhance it to meet these high standards. Integrate existing accurate information with your new insights. Do not discard valuable details from the original author.
4. Example Handling:
    * If the original docstring contains an `Examples` section: Preserve all original examples verbatim.
    * If the original docstring has no `Examples` section: Omit the Examples section entirely. The provided `Example Usages` are for your understanding only and should not be copied into the final docstring.

## Input Structure
```python
{ground_truth_function_code}
```
### Example Usages (for your understanding):
{example_usage_data}
(Note: Example Usages will be provided in a format like input/output pairs.)

## Output Format
Return the docstring and function signature in separate XML tags. The docstring should follow the Google Python Style Guide. The signature should be a complete, runnable stub.

<docstring>
\"\"\"Google Style Docstring goes here.

This docstring should be detailed, clear, and reflect Python best practices.
\"\"\"
</docstring>
<signature>
```python
# Necessary imports from typing should be included here if type hints are used.
from typing import List, Dict, Any # Example

def function_name(arg1: str, arg2: int) -> bool:
    # TODO: Implement this function based on the docstring.
    pass
```
</signature>

## Final Instructions
- Ensure the function signature in the `<signature>` tag perfectly matches the ground truth, including type hints, parameter names, and default values.
- Include necessary imports from the `typing` module in the signature if type hints are present.
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT = """
You are a programming documentation architect specializing in creating precise, implementation-agnostic specifications. Generate a docstring that enables accurate reimplementation in any programming language. When there is a docstring, the docstring is used to evaluate the code generation capabilities of a model.

## Requirements
1. **Core Description Fidelity**: The docstring must accurately reflect the function's behavior and describes the task this function solves. **Pay close attention to the sequence of checks, conditions, and resulting actions within the code.
2. Highlight any **special rules** that affect the model's correct understanding of the function's behavior, such as:
  - Recursive behavior
  - Edge cases or type-specific handling
  - Magic numbers or constants
  - Special settings that may affect the difficulty for others to correctly implement functions based on docstrings. e.g., the Ground Truth function may add some special string at the end of the result, so the docstring should mention this case, otherwise, the model may not be able to implement the function correctly.
2. **Language-Agnostic Terminology**: Use universal concepts for types and logic.
  - Describe parameters and return values using **conceptual types** (e.g., "an integer", "a boolean value", "a sequence of numbers", "a text string") instead of language-specific type hints (`int`, `bool`, `list`, `str`).
  - Describe operations conceptually (e.g., "checks if X contains Y", "iterates over the elements", "applies a function to each element") rather than Python built-ins (`s1.find("'")`, `s1.replace`).
3. **Docstring Refinement**: If the function already has a docstring, integrate and refine its content to meet these requirements. Do not discard existing accurate information.
4. **Conditional Example Handling**:
  - **If the original docstring contains an `Examples` section**:
    - Preserve all original examples **verbatim** in the final docstring's `Examples` section.
    - Format them clearly in Language-Agnostic(e.g., showing input and expected output).
    - Do **not** add or modify examples from the `Example Usages` data.
  - **If the original docstring has no `Examples` section**:
    - **Omit the Examples section entirely**, even if `Example Usages` data is provided. The `Example Usages` data should be used *internally* by you to understand the code's behavior for description purposes, but not included in the final docstring's `Examples` section.

## **Input Structure**
```python
{ground_truth_function_code}
```
### Example Usages:
{example_usage_data}
(Note: Example Usages will be provided in a format like input/output pairs.)

## **Output:**
Only return the docstring content in <docstring> tags and the function signature in the <signature> tags. The docstring should be enclosed in triple double quotes (`\"\"\"Docstring goes here\"\"\"`). The function signature should be formatted in ```python` code block with the function name and a TODO comment indicating where the implementation should go.

### Example output:
<docstring>
\"\"\"Google Style Docstring goes here\"\"\"
</docstring>
<signature>
```python
def function_name(arguments):
    # TODO: implement this function
    pass
```
</signature>

### Example Input
<Function>
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
</Function>
<Example Usage>
[
    {
        "Description": "Merge two simple dictionaries",
        "Inputs": {
            "base": {"a": 1, "b": 2},
            "update": {"b": 3, "c": 4}
        }
    },
    {
        "Description": "Merge two nested dictionaries",
        "Inputs": {
            "base": {"a": {"b": 1, "c": 2}},
            "update": {"a": {"c": 3, "d": 4}, "e": 5}
        }
    },
    {
        "Description": "Merge two lists",
        "Inputs": {
            "base": [1, 2, 3],
            "update": [4, 5, 6]
        }
    }
]
</Example Usage>
### Example Output
<docstring>
\"\"\"Recursively merge two JSON-like objects.

The function merges nested structures with the following rules:
- If both inputs are dictionaries, recursively merge them.
- If both inputs are lists, concatenate them.
- For all other cases, the update value overwrites the base value.
- The base object is left unmodified; a new merged object is returned.
Args:
    base: Base JSON-like object (dictionary, list, or primitive value).
    update: Update JSON-like object to merge into base.

Returns:
    A new JSON-like object containing merged content from base and update.
</docstring>
<signature>
```python
# There may be type annotations imported from the typing module, so we need to import it first when necessary. But when the function does not have type annotations, we don't need to import it.

def merge_json_recursive(base, update):
    # TODO: Implement this function
    pass
```
</signature>

## Note:
- Only add examples in Docstring when the function already has an `Examples` section in the docstring. Do not add examples from the `Example Usages` data if the original docstring does not contain `Examples`.
- If the signature has type hints, import nessesary types from the standard library (e.g., `from typing import List, Dict`) in signature.
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v11 = """
You are a highly skilled programming expert and technical writer specializing in creating clear, concise, and docstring for programming functions. Your primary task is to generate a detailed and accurate docstring for a given Python function, ensuring it serves as a specification for implementing the function in any language.

## **Constraints:**
1.  **Core Description Fidelity**: The docstring must accurately reflect the function's behavior and describes the task this function solves. **Pay close attention to the sequence of checks, conditions, and resulting actions within the code.**
2.  **Language-Agnostic Terminology**: Use universal concepts for types and logic.
    *   Describe parameters and return values using **conceptual types** (e.g., "an integer", "a boolean value", "a sequence of numbers", "a text string") instead of language-specific type hints (`int`, `bool`, `list`, `str`).
    *   Describe operations conceptually (e.g., "checks if X contains Y", "iterates over the elements", "applies a function to each element") rather than Python built-ins (`s1.find("'")`, `s1.replace`).
3.  **Docstring Refinement**: If the function already has a docstring, integrate and refine its content to meet these requirements. Do not discard existing accurate information.
4.  **Conditional Example Handling**:
    -   **If the original docstring contains an `Examples` section**:
        -   Preserve all original examples **verbatim** in the final docstring's `Examples` section.
        -   Format them clearly in Language-Agnostic(e.g., showing input and expected output).
        -   Do **not** add or modify examples from the `Example Usages` data.
    -   **If the original docstring has no `Examples` section**:
        -   **Omit the Examples section entirely**, even if `Example Usages` data is provided. The `Example Usages` data should be used *internally* by you to understand the code's behavior for description purposes, but not included in the final docstring's `Examples` section.

## **Input:**
### Python Function Code:
```python
{ground_truth_function_code}
```
### Example Usages:
{example_usage_data}
(Note: Example Usages will be provided in a format like input/output pairs.)

## **Output:**
Only return the docstring content in <docstring> tags and the function signature in the <signature> tags. The docstring should be enclosed in triple double quotes (`\"\"\"Docstring goes here\"\"\"`). The function signature should be formatted in ```python` code block with the function name and a TODO comment indicating where the implementation should go.

### Example output:
<docstring>
\"\"\"Google Style Docstring goes here\"\"\"
</docstring>
<signature>
```python
def function_name(arguments):
    # TODO: implement this function
    pass
```
</signature>

### Example Input
<Function>
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
</Function>
<Example Usage>
[
    {
        "Description": "Merge two simple dictionaries",
        "Inputs": {
            "base": {"a": 1, "b": 2},
            "update": {"b": 3, "c": 4}
        }
    },
    {
        "Description": "Merge two nested dictionaries",
        "Inputs": {
            "base": {"a": {"b": 1, "c": 2}},
            "update": {"a": {"c": 3, "d": 4}, "e": 5}
        }
    },
    {
        "Description": "Merge two lists",
        "Inputs": {
            "base": [1, 2, 3],
            "update": [4, 5, 6]
        }
    }
]
</Example Usage>
### Example Output
<docstring>
\"\"\"Recursively merge two JSON-like objects.

The function merges nested structures with the following rules:
- If both inputs are dictionaries, recursively merge them.
- If both inputs are lists, concatenate them.
- For all other cases, the update value overwrites the base value.
- The base object is left unmodified; a new merged object is returned.
Args:
    base: Base JSON-like object (dictionary, list, or primitive value).
    update: Update JSON-like object to merge into base.

Returns:
    A new JSON-like object containing merged content from base and update.
</docstring>
<signature>
```python
# There may be type annotations imported from the typing module, so we need to import it first when necessary. But when the function does not have type annotations, we don't need to import it.

def merge_json_recursive(base, update):
    # TODO: Implement this function
    pass
```
</signature>

## Note:
- Only add examples when the function already has an `Examples` section in the docstring. Do not add examples from the `Example Usages` data if the original docstring does not contain `Examples`.
- If the signature has type hints, import nessesary types from the standard library (e.g., `from typing import List, Dict`) in signature.
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v10 = """
You are a highly skilled programming expert and technical writer specializing in creating clear, concise, and **universally understandable** documentation for programming functions. Your goal is to refine the associated docstring by making it more informative, precise and complete without adding verbosity or detailed programming logic to the docstring. 

This function is designed around core programming concepts and basic data types, making its fundamental logic implementable in various programming languages. The docstrings must be formatted in the google docstring format and examples should be added if they clarify the function and look helpful without being very long. Do not guess outputs for functions but only copy the expected outputs as provided. Finally, do not throw away existing details from the docstrings and only insert content you are sure about. Do NOT have repeated content in the docstring and ONLY describe the high-level function behavior without going into implementation details.

## **Constraints:**
1.  The docstring must be **language-agnostic** in its terminology for types and general concepts. When describing the function's logic, focus on the **criteria and patterns it uses to determine the output**, describing these in a concise and conceptual manner where possible.
    *   Avoid Python-specific terminology where a universal concept can be used.
    *   Describe parameters and return values using **conceptual types** (e.g., "an integer", "a boolean value", "a sequence of numbers") rather than language-specific type hints (`int`, `bool`, `list`).
2.  If the function already has a docstring, refine and optimize it to meet these requirements.
3.  **Conditional Example Handling**:
    -   **If the original docstring contains an `Examples` section**:
        -   Preserve all original examples **verbatim** in the final docstring.
        -   Format them as `Input: ...\nOutput: ...` pairs.
        -   Do **not** add or modify examples from test cases or other sources.
    -   **If the original docstring has no `Examples` section**:
        -   **Omit the Examples section entirely**, even if `Example Usages` data is provided.

## **Input:**
### Python Function Code:
```python
{ground_truth_function_code}
```
### Example Usages:
{example_usage_data}
(Note: Example Usages will be provided in a format like input/output pairs.)

## **Output:**
Only return the docstring content in <docstring> tags and the function signature in the <signature> tags. The docstring should be enclosed in triple double quotes (`\"\"\"Docstring goes here\"\"\"`). The function signature should be formatted in ```python` code block with the function name and a TODO comment indicating where the implementation should go.

### Example output:
<docstring>
\"\"\"Docstring goes here\"\"\"
</docstring>
<signature>
```python
def function_name(arguments):
    # TODO: implement this function
    pass
```
</signature>

### Example Input
<Function>
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
</Function>
<Example Usage>
[
    {
        "Description": "Merge two simple dictionaries",
        "Inputs": {
            "base": {"a": 1, "b": 2},
            "update": {"b": 3, "c": 4}
        }
    },
    {
        "Description": "Merge two nested dictionaries",
        "Inputs": {
            "base": {"a": {"b": 1, "c": 2}},
            "update": {"a": {"c": 3, "d": 4}, "e": 5}
        }
    },
    {
        "Description": "Merge two lists",
        "Inputs": {
            "base": [1, 2, 3],
            "update": [4, 5, 6]
        }
    }
]
</Example Usage>
### Example Output
<docstring>
\"\"\"Recursively merge two JSON-like objects.


</docstring>
<signature>
```python
def merge_json_recursive(base, update):
    # TODO: Implement this function
    pass
```
</signature>

## Note:
- Only add examples when the function already has an `Examples` section in the docstring. Do not add examples from the `Example Usages` data if the original docstring does not contain `Examples`.
- If the signature has type hints, import nessesary types from the standard library (e.g., `from typing import List, Dict`) in signature.
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v9 = """
You are a highly skilled programming expert and technical writer specializing in creating clear, concise, and **universally understandable** documentation for programming functions. Your task is to write a docstring for a given Python function.

This function is designed around core programming concepts and basic data types, making its fundamental logic implementable in various programming languages.

Your goal is to write **ONE** comprehensive docstring that accurately and **universally** describes the function's purpose, arguments, and return value(s). This docstring should also include representative examples to illustrate its behavior, formatted as simple input/output pairs at the end.

## **Constraints:**
1.  The docstring should be **universally understandable**:
    *   Describe the function's purpose, arguments, and return values using **conceptual terms** (e.g., "an integer", "a sequence of numbers", "a key-value map") instead of language-specific type hints (`int`, `bool`, `list`, `dict`) in the main sections (Purpose, Args, Returns).
    *   Include example usages at the end, formatted as clear `Input: ...\nOutput: ...` pairs. These examples should use **easy-to-understand representations** for data, prioritizing clarity over language-specific syntax.
2.  If the function already has a docstring, refine and optimize it to meet these requirements.
4.  The docstring should be **concise** but **comprehensive**, capturing the essence of the function's behavior and how its output is determined by the inputs.
5.  Include **between 1 and 3 representative example usages** at the end of the docstring, formatted as `Input: ...\nOutput: ...` pairs. These examples must be derived **strictly from the provided Example Usages data** and formatted clearly. Select examples that best illustrate different aspects of the function's behavior.
6.  Your output must **ONLY** consist of the generated docstring content, including the surrounding triple double-quotes (`\"\"\"Docstring goes here\"\"\"`). Do not include any other text, tags, or the function signature.

## **Input:**
### Python Function Code:
```python
{ground_truth_function_code}
```
### Example Usages:
{example_usage_data}
(Note: Example Usages will be provided in a format like input/output pairs or function call examples based on test cases.)

## **Output:**
Only return the docstring content in <docstring> tags and the function signature in the <signature> tags. The docstring should be enclosed in triple double quotes (`\"\"\"Docstring goes here\"\"\"`). The function signature should be formatted in ```python` code block with the function name and a TODO comment indicating where the implementation should go.

### Example output:
<docstring>
\"\"\"Docstring goes here\"\"\"
</docstring>
<signature>
```python
def function_name(arguments):
    # TODO: implement this function
    pass
```
</signature>
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v8 = """
You are a highly skilled programming expert and technical writer specializing in creating clear, concise, and **language-agnostic** documentation for core programming concepts. Your task is to write a docstring for a given Python function.

This function is guaranteed to be **self-contained**, meaning it operates solely on basic data types (like integers, floats, strings, booleans, lists, dictionaries, tuples containing only basic types, etc.) and does not rely on any external libraries or custom classes beyond the standard language primitives. Because its logic is built only from these universal building blocks, the function's purpose and behavior can be described in a way that is understandable regardless of the programming language used for implementation.

Your goal is to write **ONE** docstring that accurately and **universally** describes the function's purpose, arguments, and return value(s). This docstring should serve as a specification that could be used to implement the same function in *any* programming language. The docstring content should be directly enclosed within triple double-quotes.

## **Constraints:**
1.  The docstring must be **language-agnostic** in its terminology for types and general concepts. When describing the function's logic, focus on the **criteria and patterns it uses to determine the output**, describing these in a concise and conceptual manner where possible.
    *   Avoid Python-specific terminology where a universal concept can be used.
    *   Describe parameters and return values using **conceptual types** (e.g., "an integer", "a boolean value", "a sequence of numbers") rather than language-specific type hints (`int`, `bool`, `list`).
    *   **The provided example usages (`## Input: ### Example Usages:`) are for your reference to understand the function's behavior and the patterns it reacts to, but they should NOT be included in the generated docstring.**
2.  Use a standard docstring format including sections for **Purpose**, **Arguments**, and **Return Value(s)**. **DO NOT include an "Examples" section in the generated docstring content.**
3.  If the function already has a docstring, modify and optimize it to meet these requirements.
4.  The docstring should be **concise** but **comprehensive**, capturing the essence of the function's behavior. By describing **what the output is and under what specific conditions or patterns this determination is made**, based on the function's logic. Avoid unnecessary implementation details.
5.  Your output must **ONLY** consist of the generated docstring content, including the surrounding triple double-quotes. Do not include any other text, tags, or the function signature.

## **Input:**
### Python Function Code:
```python
{ground_truth_function_code}
```
### Example Usages:
{example_usage_data}
(Note: Example Usages will be provided in a format like input/output pairs or function call examples based on test cases.)

## **Output:**
Only return the docstring content in <docstring> tags and the function signature in the <signature> tags. The docstring should be enclosed in triple double quotes (`\"\"\"Docstring goes here\"\"\"`) and should include sections for Args, Returns. The function signature should be formatted in ```python` code block with the function name and a TODO comment indicating where the implementation should go.

### example output:
<docstring>
\"\"\"Docstring goes here\"\"\"
</docstring>
<signature>
```python
def function_name(arguments):
    # TODO: implement this function
    pass
```
</signature>
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v7 = """
You are a highly skilled programming expert and technical writer specializing in creating clear, concise, and **language-agnostic** documentation for core programming concepts. Your task is to write a docstring for a given Python function.

This function is guaranteed to be **self-contained**, meaning it operates solely on basic data types (like integers, floats, strings, booleans, lists, dictionaries, tuples containing only basic types, etc.) and does not rely on any external libraries or custom classes beyond the standard language primitives. Because its logic is built only from these universal building blocks, the function's purpose and behavior can be described in a way that is understandable regardless of the programming language used for implementation.

Your goal is to write **ONE** docstring that accurately and **universally** describes the function's purpose, arguments, and return value(s). This docstring should serve as a specification that could be used to implement the same function in *any* programming language. The docstring content should be directly enclosed within triple double-quotes.

## **Constraints:**
1.  The docstring must be **language-agnostic** in its terminology for types and general concepts. However, when describing *how* the indentation level is determined, you may describe the **specific patterns or criteria the function checks for** based on the provided code and examples.
    *   Avoid Python-specific terminology where a universal concept can be used (e.g., use "sequence", "ordered collection" instead of "list"; "key-value map" instead of "dict").
    *   Describe parameters and return values using **conceptual types** (e.g., "an integer", "a boolean value", "a sequence of numbers") rather than language-specific type hints (`int`, `bool`, `list`).
    *   The provided example usages (`## Input: ### Example Usages:`) are for your reference to understand the function's behavior, but they should NOT be included in the generated docstring.
2.  Use a standard docstring format including sections for **Purpose**, **Arguments**, and **Return Value(s)**. **DO NOT include an "Examples" section in the generated docstring content.**
3.  If the function already has a docstring, modify and optimize it to meet these language-agnostic requirements.
4.  The docstring should be **concise** but **comprehensive**, capturing the essence of the function's behavior by describing **what indentation is returned and under what specific conditions or patterns this determination is made**, based on the function's logic. Avoid unnecessary implementation details.
5.  Your output must **ONLY** consist of the generated docstring content, including the surrounding triple double-quotes. Do not include any other text, tags, or the function signature.

## **Input:**
### Python Function Code:
```python
{ground_truth_function_code}
```
### Example Usages:
{example_usage_data}
(Note: Example Usages will be provided in a format like input/output pairs or function call examples based on test cases.)

## **Output:**
Only return the docstring content in <docstring> tags and the function signature in the <signature> tags. The docstring should be enclosed in triple double quotes (`\"\"\"Docstring goes here\"\"\"`) and should include sections for Args, Returns. The function signature should be formatted in ```python` code block with the function name and a TODO comment indicating where the implementation should go.

### example output:
<docstring>
\"\"\"Docstring goes here\"\"\"
</docstring>
<signature>
```python
def function_name(arguments):
    # TODO: implement this function
    pass
```
</signature>
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v6 = """
You are a highly skilled programming expert and technical writer specializing in creating clear, concise, and **language-agnostic** documentation for core programming concepts. Your task is to write a docstring for a given Python function.

This function is guaranteed to be **self-contained**, meaning it operates solely on basic data types (like integers, floats, strings, booleans, lists, dictionaries, tuples containing only basic types, etc.) and does not rely on any external libraries or custom classes beyond the standard language primitives. Because its logic is built only from these universal building blocks, the function's purpose and behavior can be described in a way that is understandable regardless of the programming language used for implementation.

Your goal is to write **ONE** docstring that accurately and **universally** describes the function's purpose, arguments, and return value(s). This docstring should serve as a specification that could be used to implement the same function in *any* programming language. The docstring content should be directly enclosed within triple double-quotes.

## **Constraints:**
1.  The docstring must be **language-agnostic**:
    *   Avoid Python-specific terminology where a universal concept can be used (e.g., use "sequence", "ordered collection" instead of "list"; "key-value map" instead of "dict").
    *   Describe parameters and return values using **conceptual types** (e.g., "an integer", "a boolean value", "a sequence of numbers") rather than language-specific type hints (`int`, `bool`, `list`).
    *   **The provided example usages (`## Input: ### Example Usages:`) are for your reference to understand the function's behavior, but they should NOT be included in the generated docstring.**
2.  Use a standard docstring format including sections for **Purpose**, **Arguments**, and **Return Value(s)**. **DO NOT include an "Examples" section in the generated docstring content.**
3.  If the function already has a docstring, modify and optimize it to meet these language-agnostic requirements.
4.  The docstring should be **concise** but **comprehensive**, capturing the essence of the function's behavior without unnecessary implementation details. Describe **what** the function does, not **how**.
5.  Your output must **ONLY** consist of the generated docstring content, including the surrounding triple double-quotes. Do not include any other text, tags, or the function signature.

## **Input:**
### Python Function Code:
```python
{ground_truth_function_code}
```
### Example Usages:
{example_usage_data}
(Note: Example Usages will be provided in a format like input/output pairs or function call examples based on test cases.)

## **Output:**
Only return the docstring content in <docstring> tags and the function signature in the <signature> tags. The docstring should be enclosed in triple double quotes (`\"\"\"Docstring goes here\"\"\"`) and should include sections for Args, Returns. The function signature should be formatted in ```python` code block with the function name and a TODO comment indicating where the implementation should go.

### example output:
<docstring>
\"\"\"Docstring goes here\"\"\"
</docstring>
<signature>
```python
def function_name(arguments):
    # TODO: implement this function
    pass
```
</signature>
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v5 = """
You are a highly skilled programming expert and technical writer specializing in creating clear, concise, and **language-agnostic** documentation for core programming concepts. Your task is to write a docstring for a given Python function.

This function is guaranteed to be **self-contained**, meaning it operates solely on basic data types (like integers, floats, strings, booleans, lists, dictionaries, tuples containing only basic types, etc.) and does not rely on any external libraries or custom classes beyond the standard language primitives. Because its logic is built only from these universal building blocks, the function's purpose and behavior can be described in a way that is understandable regardless of the programming language used for implementation.

Your goal is to write a docstring that accurately and universally describes the function's purpose, arguments, and return value(s).

## **Constraints:**
1. The docstring must be **language-agnostic**: Avoid Python-specific terminology where a universal concept can be used. 
2. Use a standard docstring format including sections for Args, Returns, and Examples.
3. If the function already has a docstring, you can modify and optimize the existing docstring to ensure it meets the language-agnostic requirements.
4. The docstring should be **concise** but **comprehensive**, capturing the essence of the function's behavior without unnecessary detail. Only describe what needs to be implemented, not how to implement it.
5. Include an appropriate number representative example usages** in the "Examples" section, formatted clearly (e.g., showing input and expected output). Select examples that best illustrate the function's behavior.

## **Input:**
### Python Function Code:
```python
{ground_truth_function_code}
```
### Example Usages:
{example_usage_data}
(Note: Example Usages will be provided in a format like input/output pairs or function call examples based on test cases.)

## **Output:**
Only return the docstring content in <docstring> tags and the function signature in the <signature> tags. The docstring should be enclosed in triple double quotes (`\"\"\"Docstring goes here\"\"\"`) and should include sections for Args, Returns, and Examples. The function signature should be formatted in ```python` code block with the function name and a TODO comment indicating where the implementation should go.

### example output:
<docstring>
\"\"\"Docstring goes here\"\"\"
</docstring>
<signature>
```python
def function_name(arguments):
    # TODO: implement this function
    pass
```
</signature>
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v4 = """
## Task Description
You are an expert in code understanding and problem formulation. Your task is to generate a **language-agnostic instruction** that describes the core functionality of a given Python function, based on its implementation and example usages. The instruction will be used to evaluate a model's ability to understand natural language requirements and generate code in any programming language.

### Instruction Format
The instruction must:
- Clearly describe the **main functionality** of the function in a concise, abstract manner.
- Specify the **input types** (e.g., dictionaries, lists, primitives) and **output type** the function handles.
- Highlight **special rules**, including:
  - Recursive behavior, if applicable.
  - Merging, concatenation, filtering, or transformation logic.
  - Handling of edge cases or type-specific behavior.
- Be **language-agnostic**: Avoid references to programming languages, specific syntax, or libraries.
- Be **precise and general-purpose**, guiding implementation in any language while capturing all critical behavior.

### Input Format
- **Function**: Python function code, including docstring (if available), provided in `<Function>` tags.
- **Example Usage**: A list of JSON objects describing specific scenarios, provided in `<Example Usage>` tags. Each object contains:
  - `"Description"`: A brief explanation of the scenario.
  - `"Inputs"`: A dictionary of input arguments and their values.
  - `"Expected"`: The expected output.

### Output Format
Instruction: A language-agnostic description of the function's functionality, including inputs and outputs description in <instruction> tags.
Function Signature: The function signature with a TODO placeholder, in <signature> tags.

### Example

#### Input
<Function>
def merge_json_recursive(base, update):
    \"\"\"Recursively merge two JSON-like objects.
    - Dictionaries are merged recursively
    - Lists are concatenated
    - Other types are overwritten by the update value
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
</Function>
<Example Usage>
[
    {
        "Description": "Merge two empty dictionaries",
        "Inputs": {
            "base": {},
            "update": {}
        },
        "Expected": {}
    },
    {
        "Description": "Merge dictionaries with overlapping keys",
        "Inputs": {
            "base": {
                "a": 1
            },
            "update": {
                "a": 2
            }
        },
        "Expected": {
            "a": 2
        }
    },
    {
        "Description": "Merge two lists",
        "Inputs": {
            "base": [
                1,
                2
            ],
            "update": [
                3,
                4
            ]
        },
        "Expected": [
            1,
            2,
            3,
            4
        ]
    },
    {
        "Description": "Merge nested dictionaries",
        "Inputs": {
            "base": {
                "a": {
                    "b": 1
                }
            },
            "update": {
                "a": {
                    "c": 2
                }
            }
        },
        "Expected": {
            "a": {
                "b": 1,
                "c": 2
            }
        }
    },
    {
        "Description": "Merge dictionaries with lists as values",
        "Inputs": {
            "base": {
                "a": [
                    1
                ]
            },
            "update": {
                "a": [
                    2
                ]
            }
        },
        "Expected": {
            "a": [
                1,
                2
            ]
        }
    }
]
</Example Usage>

#### Output
<instruction>
Implement a function that recursively merges two hierarchical data structures. The structures may consist of nested dictionaries, lists, or primitive values.

- **Input**: Two hierarchical objects. Each object can be a dictionary, list, or primitive value.
- **Output**: A merged object that combines both inputs according to the following rules:
  1. If both inputs are dictionaries, merge them recursively by key.
  2. If both inputs are lists, concatenate them.
  3. If inputs are of other types, return the second input.

The function must support nested combinations of these types and ensure all values from the second object are included in the final result.
</instruction>
<signature>
```python
def merge_json_recursive(base, update):
    # TODO: Implement this function
    pass
```
</signature>

## Note
- The function name should be the same as the original Python function.
- Don't implement the function; just provide the function signature and TODOs.
- import types from the standard library if needed in the signature.
- Only return the instruction and function signature in the xml tag format.
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v3 = """
## Task Description
You are an expert in code understanding and problem formulation. You will be given:
1. A Python function implementation.
2. Several example usages that describe **what the function does** in specific scenarios.

Your task is to generate a **language-agnostic instruction** that describes the core functionality of the function. This instruction will be used to evaluate a model's ability to understand natural language requirements and generate code in any language.

### Instruction Format
The instruction must:
- Clearly describe the **main functionality** of the function.
- Include the **input types and output types** the function handles.
- Highlight any **special rules**, such as:
  - Recursive behavior
  - Merging, flattening, filtering, transformation logic
  - Edge cases or type-specific handling
- Provide **at least one representative example usage**, based on the given examples, to help clarify expectations.
- Avoid any references to programming languages, syntax, or specific libraries.
- Be abstract and general-purpose, but **precise enough to guide implementation** in any language.

### Input Format
You will be given:
- <Function>Python function code</Function>
- <Example Usage>[{{"Description": "...", "Inputs": {{...}}}}, ...]</Example Usage>

### Output Format
Return the **instruction** in an <instruction> tag, and the **function signature** in a <signature> tag.

### Example

#### Input
<Function>
def merge_json_recursive(base, update):
    \"\"\"Recursively merge two JSON-like objects.
    - Dictionaries are merged recursively
    - Lists are concatenated
    - Other types are overwritten by the update value
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
</Function>
<Example Usage>
[
    {
        "Description": "Merge two simple dictionaries",
        "Inputs": {
            "base": {"a": 1, "b": 2},
            "update": {"b": 3, "c": 4}
        }
    },
    {
        "Description": "Merge two nested dictionaries",
        "Inputs": {
            "base": {"a": {"b": 1, "c": 2}},
            "update": {"a": {"c": 3, "d": 4}, "e": 5}
        }
    },
    {
        "Description": "Merge two lists",
        "Inputs": {
            "base": [1, 2, 3],
            "update": [4, 5, 6]
        }
    }
]
</Example Usage>

#### Output
<instruction>
Implement a function that recursively merges two hierarchical data structures. The structures may consist of nested dictionaries, lists, or primitive values.

- **Input**: Two hierarchical objects. Each object can be a dictionary, list, or primitive value.
- **Output**: A merged object that combines both inputs according to the following rules:
  1. If both inputs are dictionaries, merge them recursively by key.
  2. If both inputs are lists, concatenate them.
  3. If inputs are of other types, return the second input.

The function must support nested combinations of these types and ensure all values from the second object are included in the final result.

### Example Usage
**Input**:
base = {"a": {"b": 1, "c": 2}, "x": [1, 2]} update = {"a": {"c": 3, "d": 4}, "x": [3, 4], "e": 5}
**Output**:
{ "a": {"b": 1, "c": 3, "d": 4}, "x": [1, 2, 3, 4], "e": 5 }
</instruction>
<signature>
```python
def merge_json_recursive(base, update):
    # TODO: Implement this function
    pass
```
</signature>
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v2 = """
## Task Description
You are an expert in code understanding and problem formulation. You will be given:
1. A Python function implementation.
2. Several example usages that describe **what the function does** in specific scenarios.

Your task is to generate a **language-agnostic instruction** that describes the core functionality of the function. This instruction will be used to evaluate a model's ability to understand natural language requirements and generate code in any language.

### Instruction Format
The instruction must:
- Clearly describe the **main functionality** of the function.
- Include the **input types and output types** the function handles.
- Highlight any **special rules**, such as:
  - Recursive behavior
  - Merging, flattening, filtering, transformation logic
  - Edge cases or type-specific handling
- Avoid any references to programming languages, syntax, or specific libraries.
- Be abstract and general-purpose, but **precise enough to guide implementation** in any language.

### Input Format
You will be given:
- <Function>Python function code</Function>
- <Example Usage>[{{"Description": "...", "Inputs": {{...}}}}, ...]</Example Usage>

### Output Format
Return the **instruction** in an <instruction> tag, and the **function signature** in a <signature> tag.

### Example

#### Input
<Function>
def merge_json_recursive(base, update):
    \"\"\"Recursively merge two JSON-like objects.
    - Dictionaries are merged recursively
    - Lists are concatenated
    - Other types are overwritten by the update value
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
</Function>
<Example Usage>
[
    {
        "Description": "Merge two simple dictionaries",
        "Inputs": {
            "base": {"a": 1, "b": 2},
            "update": {"b": 3, "c": 4}
        }
    },
    {
        "Description": "Merge two nested dictionaries",
        "Inputs": {
            "base": {"a": {"b": 1, "c": 2}},
            "update": {"a": {"c": 3, "d": 4}, "e": 5}
        }
    },
    {
        "Description": "Merge two lists",
        "Inputs": {
            "base": [1, 2, 3],
            "update": [4, 5, 6]
        }
    }
]
</Example Usage>

#### Output
<instruction>
Implement a function that recursively merges two hierarchical data structures. The structures may consist of nested dictionaries, lists, or primitive values.

- **Input**: Two JSON-like structures (can be dictionaries, lists, or primitive values).
- **Output**: A merged structure that respects the following rules:
  1. If both inputs are dictionaries, merge them recursively by key.
  2. If both inputs are lists, concatenate them.
  3. If inputs are of other types, the second input value overrides the first.

The function must support nested combinations of these types and preserve all updated or added content from the second input.
</instruction>
<signature>
```python
def merge_json_recursive(base, update):
    # TODO: Implement this function
    pass
</signature>
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v1 = """
## Task Description
You are an expert in code understanding and problem formulation. You will be given:
1. A function implementation (in Python).
2. Several example usages that describe **what the function does** in specific scenarios.

Your job is to generate a **language-agnostic instruction** in markdown that describes the task this function solves. This instruction will be used to evaluate a model's ability to **understand natural language requirements** and generate the correct code in any programming language.

### Instruction Format
The instruction should:
- Describe the **core functionality** of the function.
- Mention the **types of data** being handled (e.g., dictionaries, lists, structured objects).
- Clarify any **recursive behavior, merging logic, or rules** if applicable.
- Avoid mentioning programming language, syntax, or specific libraries.
- Be abstract enough to apply to other languages, but precise enough to guide code generation.

### Input Format
You will be given:
- "Function": "<Python function implementation>",
- "Example Usage": [
    {
      "Description": "...",
      "Inputs": {...}
    },
    ...
  ]
}

### Output Format
Return the instruction in <instruction> tag, and the function signature in <signature> tag.

## Example
### Example Input
<Function>
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
</Function>
<Example Usage>
[
    {
        "Description": "Merge two simple dictionaries",
        "Inputs": {
            "base": {"a": 1, "b": 2},
            "update": {"b": 3, "c": 4}
        }
    },
    {
        "Description": "Merge two nested dictionaries",
        "Inputs": {
            "base": {"a": {"b": 1, "c": 2}},
            "update": {"a": {"c": 3, "d": 4}, "e": 5}
        }
    },
    {
        "Description": "Merge two lists",
        "Inputs": {
            "base": [1, 2, 3],
            "update": [4, 5, 6]
        }
    }
]
</Example Usage>
### Example Output
<instruction>
Implement a function that recursively merges two JSON-like objects. The merging rules are as follows: 
1. If both objects are dictionaries, merge them recursively.
2. If both objects are lists, concatenate them.
3. For other types, the value from the 'update' object overwrites the value in the 'base' object. 
The function should handle nested structures and ensure that all keys from the 'update' object are included in the final merged object.
- Input:

</instruction>
<signature>
```python
# There may be type annotations imported from the typing module, so we need to import it first when necessary. But when the function does not have type annotations, we don't need to import it.

def merge_json_recursive(base, update):
    # TODO: Implement this function
    pass
```
</signature>
"""

SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT_v0 = """
## Task Description
You are an expert in the field of coding, helping users generate corresponding questions based on the provided answers.
The user provides you with a self-contained Python function as the ground truth (answer), and you generate a programming language-independent instruction (question) based on this function.
You need to generate a corresponding question description based on the function's functionality, alongwith the function's difficulty level and domain.

## Question Description
Consider the following:
- Functionality: Clearly define the core purpose of the function.
- Inputs and Outputs: Describe the function's parameters with type and return values with type.
- Possible Domain Knowledge: Generate questions based on the domain background and application scenarios if it is needed.
- Error Handling and Edge Cases: Consider how the function handles exceptions and extreme cases.

## When to say "Can't Do"
- If the function's parameters are not a combination of basic types, such as when the parameter is an instance of a custom class, or if we do not know the type of the parameter and the function uses methods or attributes of this parameter, then we cannot generate an instruction.
- If the function does not provide a meaningful test of the model's capabilities, for example, if the function is very long but the logic is very simple, then it is not suitable for generating questions.
- If the function imports other modules or has side effects, we cannot generate an instruction.
- Sometimes the function is implemented for specific types such as Tensor or DataFrame. Although it is not explicitly stated in the function declaration, we can understand it through the semantics of the function. In this case, we should not generate instructions.
- The function is too easy, it is just simple business logic.
- The function can't be constructed by property-based testing.

## Output Format
If the function can be generate corresponding questions according to our rules. Return:
```json
{
    "Instruction": "Your instruction text in markdown format",
    "Signature": "The signature of the function", 
    "Difficulty": "Easy/Medium/Hard"
}
```
If you "Can't Do", return:
```json
{
    "Reason": "The reason why you can't generate an instruction",
}

## How to judge difficulty
### Example of Medium Difficulty
```python
def find_closest_aspect_ratio(
    aspect_ratio: float,
    target_ratios: list[tuple[int, int]],
    *,
    width: int,
    height: int,
    image_size: int,
) -> tuple[int, int]:
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio
```
### Example of Easy Difficulty
```python
def parse_message(message: str) -> str:
    if message is None:
        return ""

    message = message.strip().lower()

    # run-slow: model_1, model_2
    if not message.startswith(("run-slow", "run_slow", "run slow")):
        return ""
    message = message[len("run slow") :]
    # remove leading `:`
    while message.strip().startswith(":"):
        message = message.strip()[1:]

    return message
```
### Example of too simple which is not suitable for generating questions
```python
def get_webhook_component_in_flow(flow_data: dict):
    # Get webhook component in flow data.
    if "nodes" in flow_data:
        for node in flow_data.get("nodes", []):
            if "Webhook" in node.get("id"):
                return node
    return None
```
Note that even if the function above looks not easy, its logic is very simple, so it is of easy difficulty.

## Example of normal input and output
### Input
```python


## Note
- Do not lose the original function details, including parameter types, return types, function name, etc.
- Do not lose the context within the function, such as other variables defined in the function.
- Don't generate Example Usage in the instrution.
"""

LEVEL_SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT = """
## Task Description
You are an expert in the field of coding, helping users generate corresponding questions based on the provided answers.
The user provides you with a function A as the ground truth (answer), the function A calls a self-contained function B. You generate an instruction of function A (question) and an instruction of function B.
You need to generate a corresponding question description based on the function's functionality, alongwith the function's difficulty level and domain.

## Question Description
Consider the following:
- Functionality: Clearly define the core purpose of the function.
- Inputs and Outputs: Describe the function's parameters and return values.
- Possible Domain Knowledge: Generate questions based on the domain background and application scenarios if it is needed.
- Error Handling and Edge Cases: Consider how the function handles exceptions and extreme cases.

## When to say "Can't Do"
- If the function's parameters can't be constructed by property-based testing, such as when the parameter is an instance of a user-defined class.
- If the function does not provide a meaningful test of the model's capabilities, for example, if the function is very long but the logic is very simple, then it is not suitable for generating questions.
- If the function imports other modules or other functions(besides self-contained function B) or has side effects, we cannot generate an instruction.
- Sometimes the function is implemented for specific types such as Tensor or DataFrame. Although it is not explicitly stated in the function declaration, we can understand it through the semantics of the function. In this case, we should not generate instructions.
- The function is too easy, it is just simple business logic.

## Output Format
```json
{
    "Instruction": "Your instruction text in markdown format",
    "Difficulty": "Easy/Medium/Hard"
}
```
If you "Can't Do", return:
```json
{
    "Reason": "The reason why you can't generate an instruction",
}

## Examples
### Example of Medium Difficulty
<Example>
<function A>
```python
def find_closest_aspect_ratio(
    aspect_ratio: float,
    target_ratios: list[tuple[int, int]],
    *,
    width: int,
    height: int,
    image_size: int,
) -> tuple[int, int]:
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff <function best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    updated_ratio = update_ratio(best_ratio)
    return updated_ratio
```
</function A>
<function B>
```python
def update_ratio(ratio: tuple[int, int]) -> tuple[int, int]:
    if ratio[0] == 0:
        return (1, ratio[1])
    return ratio
```
</function B>
<Instruction>
The function you need to implement:
Generate a function named `find_closest_aspect_ratio` that takes a float `aspect_ratio`, a list of tuples `target_ratios`, and three integers `width`, `height`, and `image_size` as input. The function should find the ratio in `target_ratios` that is closest to `aspect_ratio` and return it. If there are multiple ratios with the same difference, the function should return the one with the larger area. Before returning the ratio, the function should call another function `update_ratio` with the best ratio as an argument and return the result of `update_ratio`. The `update_ratio` function takes a tuple of two integers and returns a new tuple where the first element is 1 if the original first element is 0, otherwise it returns the original tuple. The function should return the updated ratio.

The function you must use: 
`def update_ratio(ratio: tuple[int, int]) -> tuple[int, int]`
Don't implement the `update_ratio` function, just use it in the `find_closest_aspect_ratio` function.
</Instruction>
</Example>

## Note
- Do not lose the original function details, including parameter types, return types, function name, etc.
- Do not lose the context within the function, such as other variables defined in the function.
"""