PURE_JAVA_RUNNER_GENERATOR_PROMPT = """
## Task Description

You are an expert Java developer specializing in automated test case execution and property-based testing. Your task is to generate a **complete, executable Java test file** for a given Java function (provided as a class with package declaration). The test file should:

1. **Match the package** of the function under test.
2. **Define a `Tester` class** that loads test cases from `src/test/java/test_cases/test_cases.json`.
3. **Define a `TestCase` inner class** (with nested `Inputs` class if needed) that matches the expected JSON structure for test cases, with fields corresponding to the function’s parameters and expected output.
4. **Use JUnit 5 parameterized testing** (`@ParameterizedTest` and `@MethodSource`) to run each test case as a subtest.
5. **Call the function under test** (e.g., `Tested.func0(tc.Inputs.x, tc.Inputs.y)`).
6. **Assert the result** using `Helper.deepCompare`, with detailed error messages showing input, expected, and actual values.
7. **Only output Java code**—no explanations or comments outside the code.
8. **Ensure the package name matches the function under test.**

---

## Input

A Java function (with class and package declaration), for example:

```java
package template;

public class GroundTruth {
    public static int func0(int x, int y) {
        if (x > 0 && y > 0) {
            return x + y;
        } else if (x < 0 && y < 0) {
            return x - y;
        } else {
            return x * y;
        }
    }
}
```

## Output Example

```java
package template;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;
import p1.Helper;
import p1.Tested;

public class Tester {

    static class TestCase {
        public Inputs Inputs;
        public int Expected;

        static class Inputs {
            public int x;
            public int y;
        }
    }

    private static List<TestCase> loadTestCases(String filePath) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        File file = new File(filePath);
        try {
            return mapper.readValue(file, new TypeReference<List<TestCase>>() {});
        } catch (IOException e) {
            throw new IOException("Failed to load test cases from " + filePath + ": " + e.getMessage(), e);
        }
    }

    private static Stream<TestCase> testCases() throws IOException {
        return loadTestCases("src/test/java/test_cases/test_cases.json").stream();
    }

    @ParameterizedTest(name = "TestCase{index}")
    @MethodSource("testCases")
    void testFunc0(TestCase tc) {
        int actual = Tested.func0(tc.Inputs.x, tc.Inputs.y);
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: x=%d, y=%d%nExpected: %s%nActual: %s",
                tc.Inputs.x, tc.Inputs.y, tc.Expected, actual
            )
        );
    }
}
```

## Notes

- Only output Java code.
- The `TestCase` and `Inputs` classes must match the expected test case JSON structure for the function under test.
- The test method should call the function under test with the correct arguments and assert the result using `Helper.deepCompare`.
- The package name and "import template.Helper", "import template.Tested" should match the function's package.
"""

JAVA_RUNNER_GENERATOR_PROMPT = """
## Task Description
As an expert Java developer specializing in test case generation and function signature translation, your task is to generate a Java test file and function signature based on a Python function and its test cases. The test file will load test cases from a JSON file and execute tests using a provided `Helper.deepCompare` method.

### Requirements
1. **Java Test File**:
   - Generate a complete, executable Java test file in the `p0` package.
   - Include:
     - Necessary imports (`com.fasterxml.jackson.databind.ObjectMapper`, `com.fasterxml.jackson.core.type.TypeReference`, `org.junit.jupiter.*`, `java.io.*`, `java.util.*`).
     - A `TestCase` class matching the JSON structure, with nested `Inputs` class for input fields.
     - A `loadTestCases` method to read and parse the JSON file, throwing `IOException`.
     - A test method `test<FunctionName>` using `@ParameterizedTest` and `@MethodSource` to run sub-tests for each test case.
     - Error reporting with input, expected, and actual values.
   - Follow Java best practices:
     - Type-safe JSON parsing (use `List<String>`, `int`, `String`, avoid `Map` or `Object`).
     - Clear comments explaining key sections (e.g., `TestCase`, `loadTestCases`).
     - Separate JSON loading from test logic.
     - Use JUnit 5 with `@ParameterizedTest` for sub-test naming (e.g., `TestCase{index}`).
     - Handle exceptions (e.g., `IOException`) with descriptive messages.
   - Output in `<code>` tags.

2. **Function Signature**:
   - Provide only the function signature in the `p0.Tested` class.
   - Match the Python function’s input and output types (e.g., `List[str]` → `List<String>`, `str` → `String`).
   - Use `public static` methods, include a `// TODO: Implement this function` comment.
   - Import necessary types (e.g., `java.util.List`).
   - **Declare potential exceptions in the function signature**, even if they are not tested in the test file.
   - Output in `<signature>` tags.

3. **Special Considerations**:
   - **Type Safety**:
     - Ensure `TestCase` fields exactly match JSON keys and types (e.g., `lines` → `List<String>`, `line_index` → `int`).
     - Avoid using generic types like `Object` or `Map` unless absolutely necessary.
     - Handle complex inputs (e.g., lists, multiple parameters) accurately.
   - **Exception Handling**:
     - Use `assertTrue` to validate test results.
     - Do not use `assertThrows` in the test file even if the function signature declares exceptions, as the test cases do not include invalid inputs.
   - Assume `Helper.deepCompare(expected, actual, tolerance)` is defined elsewhere, with `tolerance` set to `0` for non-floating-point types (e.g., `String`) and `1e-6` for floating-point types.
   - Return only `<code>` and `<signature>` sections, without additional explanations.
   - Do not implement the function in the test file.
   
4. **Type Definition Rules**
- Follow these rules to determine where to define types:
  | Usage Scenario                | Location         | Example                  |
  |-------------------------------|------------------|--------------------------|
  | Used in function signature    | `tested.java`      | `public static class TagInfo {}`  |
  | Only in test JSON structure   | Inline in TestCase | `static class Inputs { public List<String> lines; }` |
  | Used in both                  | `tested.java`      | Shared types always in implementation |

## Input Format
- **Test Cases JSON**: A JSON array of test cases, provided as `{testcases_str}`.
- **Python Function**: A Python function to be tested, including its signature and implementation, provided as code.

## Output Format
```plaintext
<code>
[Java test file]
</code>
<signature>
[Java function signature]
</signature>

## Examples
### Example 1: normal case with no error handling
#### Input
Test Cases JSON:
```json
[
    {
        "Inputs": {
            "lines": ["    def func():"],
            "line_index": 0
        },
        "Expected": ""
    },
    {
        "Inputs": {
            "lines": ["class MyClass:", "    pass"],
            "line_index": 1
        },
        "Expected": "    "
    }
]
```
Python Function:
```python
from typing import List

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
#### Output
<code>
```java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class Tester {

    // TestCase represents the structure of our test cases
    static class TestCase {
        public Inputs Inputs;
        public String Expected;

        static class Inputs {
            public List<String> lines;
            public int line_index;
        }
    }

    // loadTestCases reads and parses test cases from a JSON file
    private static List<TestCase> loadTestCases(String filePath) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        File file = new File(filePath);
        try {
            return mapper.readValue(file, new TypeReference<List<TestCase>>() {});
        } catch (IOException e) {
            throw new IOException("Failed to load test cases from " + filePath + ": " + e.getMessage(), e);
        }
    }

    // Provide test cases as a stream for parameterized testing
    private static Stream<TestCase> testCases() throws IOException {
        return loadTestCases("src/test/java/test_cases/test_cases.json").stream();
    }

    @ParameterizedTest(name = "TestCase{index}")
    @MethodSource("testCases")
    void testGetCorrectIndentLevel(TestCase tc) {
        // Call the function under test
        String actual = Tested._get_correct_indent_level(tc.Inputs.lines, tc.Inputs.line_index);

        // Compare with expected result using Helper.deepCompare
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: lines=%s, line_index=%d%nExpected: %s%nActual: %s",
                tc.Inputs.lines, tc.Inputs.line_index, tc.Expected, actual
            )
        );
    }
}
```
<signature>
```java
import java.util.List;

public class Tested {
    public static String _get_correct_indent_level(List<String> lines, int lineIndex) {
        // TODO: Implement this function
    }
}
```
</signature>

### Example 2: Type definition used in both test and function signature
#### Input
Test Cases JSON:
```json
[
    {
      "Description": "Valid response structure with default tags",
      "Inputs": {
        "processed_str": "<think>thought</think><answer>answer</answer>"
      },
      "Expected": true
    }
]
```
Python Function:
```python
from typing import Dict

def validate_response_structure(processed_str: str, tags: Dict = None) -> bool:
    validation_passed = True
    # Check required tags
    if tags is None:
        tags = {
            "think_start": {"text": "<think>", "num_occur": 1},
            "think_end": {"text": "</think>", "num_occur": 1},
            "answer_start": {"text": "<answer>", "num_occur": 1},
            "answer_end": {"text": "</answer>", "num_occur": 1},
        }
    positions = {}
    for tag_name, tag_info in tags.items():
        tag_str = tag_info["text"]
        expected_count = tag_info["num_occur"]
        count = processed_str.count(tag_str)
        positions[tag_name] = pos = processed_str.find(tag_str)
        if count != expected_count:
            validation_passed = False
    # Verify tag order
    if (
        positions["think_start"] > positions["think_end"]
        or positions["think_end"] > positions["answer_start"]
        or positions["answer_start"] > positions["answer_end"]
    ):
        validation_passed = False
    if len(processed_str) - positions["answer_end"] != len(tags["answer_end"]["text"]):
        validation_passed = False
    return validation_passed
```
### Output
<code>
```java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class Tester {

    // TestCase represents the structure of our test cases
    static class TestCase {
        public Inputs Inputs;
        public boolean Expected;

        static class Inputs {
            public String processed_str;
            public Map<String, TagInfo> tags;
        }
    }

    // loadTestCases reads and parses test cases from a JSON file
    private static List<TestCase> loadTestCases(String filePath) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        File file = new File(filePath);
        try {
            return mapper.readValue(file, new TypeReference<List<TestCase>>() {
            });
        } catch (IOException e) {
            throw new IOException("Failed to load test cases from " + filePath + ": " + e.getMessage(), e);
        }
    }

    // Provide test cases as a stream for parameterized testing
    private static Stream<TestCase> testCases() throws IOException {
        return loadTestCases("src/test/java/test_cases/test_cases.json").stream();
    }

    @ParameterizedTest(name = "TestCase{index}")
    @MethodSource("testCases")
    void testValidateResponseStructure(TestCase tc) {
        // Call the function under test
        boolean actual = Tested.validate_response_structure(tc.Inputs.processed_str, tc.Inputs.tags);

        // Compare with expected result using Helper.deepCompare
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: processed_str=%s, tags=%s%nExpected: %s%nActual: %s",
                tc.Inputs.processed_str, tc.Inputs.tags, tc.Expected, actual
            )
        );
    }
}
```
</code>
<signature>
```java
import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;

public class Tested {
    public static boolean validate_response_structure(String processedStr, Map<String, TagInfo> tags) {
        // TODO: Implement this function
    }

    // TagInfo represents the structure of tag information
    static class TagInfo {
        public String text;
        public int num_occur;
    }
}
```
</signature>

### Example 3: Function with Potential Errors
Python Function:
```python
def parse_config(config: dict) -> str:
    if not config:
        raise ValueError("Empty config")
    return config["version"]
```
Test Cases JSON:
```json
[
    {
        "Inputs": {
            "config": {
                "version": "1.0.0",
                "debug": true
            }
        },
        "Expected": "1.0.0"
    },
    {
        "Inputs": {
            "config": {
                "version": "2.1.3"
            }
        },
        "Expected": "2.1.3"
    }
]
```
#### Output
<code>
```java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.*;

public class Tester {

    static class TestCase {
        public Inputs Inputs;
        public String Expected;

        static class Inputs {
            public Map<String, Object> config;
        }
    }

    private static List<TestCase> loadTestCases(String filePath) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(new File(filePath), new TypeReference<List<TestCase>>() {});
    }

    private static Stream<TestCase> testCases() throws IOException {
        return loadTestCases("test_cases/test_cases.json").stream();
    }

    @ParameterizedTest(name = "TestCase{index}")
    @MethodSource("testCases")
    void testParseConfig(TestCase tc) throws Exception {
        // Call function under test
        String actual = Tested.parse_config(tc.Inputs.config);

        // Verify output
        assertTrue(
                Helper.deepCompare(tc.Expected, actual, 0),
                String.format(
                        "Test case failed:%nInput: %s%nExpected: %s%nActual: %s",
                        tc.Inputs.config, tc.Expected, actual
                )
        );
    }
}
```
</code>
<signature>
```java
import java.util.Map;

public class Tested {
    public static String parse_config(Map<String, Object> config) throws Exception {
        // TODO: Implement this function
    }
}
```
</signature>

## Note
- Ensure the generated Java test file is complete and executable.
- The function signature should be a valid Java function signature that matches the Python function's behavior.
- Only return the Java test file in `<code>` and the function signature in `<signature>` tags.
"""

JAVA_RUNNER_GENERATOR_PROMPT_v2 = """
## Task Description
As an expert Java developer specializing in test case generation and function signature translation, your task is to generate a Java test file and function signature based on a Python function and its test cases. The test file will load test cases from a JSON file and execute tests using a provided `Helper.deepCompare` method.

### Requirements
1. **Java Test File**:
   - Generate a complete, executable Java test file in the `p0` package.
   - Include:
     - Necessary imports (`com.fasterxml.jackson.databind.ObjectMapper`, `com.fasterxml.jackson.core.type.TypeReference`, `org.junit.jupiter.*`, `java.io.*`, `java.util.*`).
     - A `TestCase` class matching the JSON structure, with nested `Inputs` class for input fields.
     - A `loadTestCases` method to read and parse the JSON file, throwing `IOException`.
     - A test method `test<FunctionName>` using `@ParameterizedTest` and `@MethodSource` to run sub-tests for each test case.
     - Error reporting with input, expected, and actual values.
   - Follow Java best practices:
     - Type-safe JSON parsing (use `List<String>`, `int`, `String`, avoid `Map` or `Object`).
     - Clear comments explaining key sections (e.g., `TestCase`, `loadTestCases`).
     - Separate JSON loading from test logic.
     - Use JUnit 5 with `@ParameterizedTest` for sub-test naming (e.g., `TestCase{index}`).
     - Handle exceptions (e.g., `IOException`) with descriptive messages.
   - Output in `<code>` tags.

2. **Function Signature**:
   - Provide only the function signature in the `p0.Tested` class.
   - Match the Python function’s input and output types (e.g., `List[str]` → `List<String>`, `str` → `String`).
   - Use `public static` methods, include a `// TODO: Implement` comment.
   - Import necessary types (e.g., `java.util.List`).
   - Output in `<signature>` tags.

3. **Special Considerations**:
   - Ensure `TestCase` fields exactly match JSON keys and types (e.g., `lines` → `List<String>`, `line_index` → `int`).
   - Use specific Java types to reflect JSON data, avoiding `Map` or `Object` for type safety.
   - Handle complex inputs (e.g., lists, multiple parameters) accurately.
   - Do not implement the function in the test file.
   - Assume `Helper.deepCompare(expected, actual, tolerance)` is defined elsewhere, with `tolerance` set to `0` for non-floating-point types (e.g., `String`) and `1e-6` for floating-point types.
   - Return only `<code>` and `<signature>` sections, without additional explanations.

## Input Format
- **Test Cases JSON**: A JSON array of test cases, provided as `{testcases_str}`.
- **Python Function**: A Python function to be tested, including its signature and implementation, provided as code.

## Output Format
```plaintext
<code>
[Java test file]
</code>
<signature>
[Java function signature]
</signature>

## Examples
### Example 1: fast_format_html
#### Input
Test Cases JSON:
```json
[
    {
        "Inputs": {
            "html_string": "<div><p>Hello</p></div>"
        },
        "Expected": "<div>\n  <p>\n    Hello\n  </p>\n</div>"
    },
    {
        "Inputs": {
            "html_string": "<br/>"
        },
        "Expected": "<br/>"
    }
]
```
Python Function:
```python
def fast_format_html(html_string):
    indent = 0
    indent_str = "  "
    formatted = []
    parts = html_string.replace(">", ">\n").replace("<", "\n<").split("\n")
    for part in parts:
        if not part.strip():
            continue
        if part.startswith("</"):
            indent -= 1
            formatted.append(indent_str * indent + part)
        elif part.startswith("<") and part.endswith("/>"):
            formatted.append(indent_str * indent + part)
        elif part.startswith("<"):
            formatted.append(indent_str * indent + part)
            indent += 1
        else:
            content = part.strip()
            if content:
                formatted.append(indent_str * indent + content)
    return "\n".join(formatted)
```
### Output
<code>
```java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class Tester {

    // TestCase represents the structure of our test cases
    static class TestCase {
        public Inputs Inputs;
        public String Expected;

        static class Inputs {
            public String html_string;
        }
    }

    // loadTestCases reads and parses test cases from a JSON file
    private static List<TestCase> loadTestCases(String filePath) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        File file = new File(filePath);
        try {
            return mapper.readValue(file, new TypeReference<List<TestCase>>() {});
        } catch (IOException e) {
            throw new IOException("Failed to load test cases from " + filePath + ": " + e.getMessage(), e);
        }
    }

    // Provide test cases as a stream for parameterized testing
    private static Stream<TestCase> testCases() throws IOException {
        return loadTestCases("src/test/java/test_cases/test_cases.json").stream();
    }

    @ParameterizedTest(name = "TestCase{index}")
    @MethodSource("testCases")
    void testFastFormatHTML(TestCase tc) {
        // Call the function under test
        String actual = Tested.fast_format_html(tc.Inputs.html_string);
        // Compare with expected result using Helper.deepCompare
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 1e06),
            String.format(
                "Test case failed:%nInputs: html_string=%s%nExpected: %s%nActual: %s",
                tc.Inputs.html_string, tc.Expected, actual
            )
        );
    }
}
```
</code>
<signature>
```java
public class Tested {
    public static String fast_format_html(String htmlString) {
        // TODO: Implement this function
    }
}
```
</signature>
### Example 2: _get_correct_indent_level
#### Input
Test Cases JSON:
```json
[
    {
        "Inputs": {
            "lines": ["    def func():"],
            "line_index": 0
        },
        "Expected": ""
    },
    {
        "Inputs": {
            "lines": ["class MyClass:", "    pass"],
            "line_index": 1
        },
        "Expected": "    "
    }
]
```
Python Function:
```python
from typing import List

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
#### Output
<code>
```java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.stream.Stream;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class Tester {

    // TestCase represents the structure of our test cases
    static class TestCase {
        public Inputs Inputs;
        public String Expected;

        static class Inputs {
            public List<String> lines;
            public int line_index;
        }
    }

    // loadTestCases reads and parses test cases from a JSON file
    private static List<TestCase> loadTestCases(String filePath) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        File file = new File(filePath);
        try {
            return mapper.readValue(file, new TypeReference<List<TestCase>>() {});
        } catch (IOException e) {
            throw new IOException("Failed to load test cases from " + filePath + ": " + e.getMessage(), e);
        }
    }

    // Provide test cases as a stream for parameterized testing
    private static Stream<TestCase> testCases() throws IOException {
        return loadTestCases("src/test/java/test_cases/test_cases.json").stream();
    }

    @ParameterizedTest(name = "TestCase{index}")
    @MethodSource("testCases")
    void testGetCorrectIndentLevel(TestCase tc) {
        // Call the function under test
        String actual = Tested._get_correct_indent_level(tc.Inputs.lines, tc.Inputs.line_index);

        // Compare with expected result using Helper.deepCompare
        assertTrue(
            Helper.deepCompare(tc.Expected, actual, 0),
            String.format(
                "Test case failed:%nInputs: lines=%s, line_index=%d%nExpected: %s%nActual: %s",
                tc.Inputs.lines, tc.Inputs.line_index, tc.Expected, actual
            )
        );
    }
}
```
<signature>
```java
import java.util.List;

public class Tested {
    public static String _get_correct_indent_level(List<String> lines, int lineIndex) {
        // TODO: Implement this function
    }
}
```
</signature>

## Note
- Ensure the generated Java test file is complete and executable.
- The function signature should be a valid Java function signature that matches the Python function's behavior.
- Only return the Java test file in `<code>` and the function signature in `<signature>` tags.
"""

JAVA_RUNNER_GENERATOR_PROMPT_v1 = """
You are an expert Java developer specializing in test case generation and function signature translation. Your task is to:

1. Generate a complete and executable Java test file that:
   - Loads test cases from JSON using Jackson
   - Uses direct Map<String, Object> inputs
   - Employs DeepCompare for verification
   - Provides detailed error reporting

2. For the function implementation:
   - Only provide the function signature
   - Include a "TODO: Implement" comment
   - Match the Python function's behavior

3. Test file requirements:
   - JUnit 5 with proper assertions
   - Clear test case structure
   - Separate JSON loading
   - Detailed failure messages

4. Special considerations:
   - Maintain type safety with Jackson
   - Follow Java testing best practices
   - Include descriptive comments

## Input and Output
The input will include a Python test case runner and a JSON file containing test cases. The output should be a Go test file and a function signature.

## Input Example
The test cases JSON file has the following structure:
```json
{testcases_str}
```
The python test case runner containes a Python function to be tested:
```python
def fast_format_html(html_string):
    # Initialize variables
    indent = 0
    indent_str = "  "  # Two spaces for indentation
    formatted = []
    # in_content = False

    # Split by < and > to separate tags and content
    parts = html_string.replace(">", ">\n").replace("<", "\n<").split("\n")

    for part in parts:
        if not part.strip():
            continue

        # Handle closing tags
        if part.startswith("</"):
            indent -= 1
            formatted.append(indent_str * indent + part)

        # Handle self-closing tags
        elif part.startswith("<") and part.endswith("/>"):
            formatted.append(indent_str * indent + part)

        # Handle opening tags
        elif part.startswith("<"):
            formatted.append(indent_str * indent + part)
            indent += 1

        # Handle content between tags
        else:
            content = part.strip()
            if content:
                formatted.append(indent_str * indent + content)

    return "\n".join(formatted)
```
## Output Example
<code>
```java
package p0;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import java.io.File;
import java.util.List;
import java.util.Map;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class Tester {

	static class TestCase {
		public Map<String, Object> Inputs;
		public Object Expected;
	}

	@Test
	public void testFromJson() throws Exception {
		ObjectMapper mapper = new ObjectMapper();
		List<TestCase> cases = mapper.readValue(
				new File("src/test/java/test_cases/test_cases.json"),
				new TypeReference<List<TestCase>>() {
				});

		for (int i = 0; i < cases.size(); i++) {
			TestCase tc = cases.get(i);
			Object actual = Tested._get_pipelines_disabled(tc.Inputs);

			assertTrue(
					Helper.deepCompare(tc.Expected, actual, 1e-6),
					String.format("Test case %d failed%nInputs: %s%nExpected: %s%nActual: %s",
							i, tc.Inputs, tc.Expected, actual));
		}
	}
}
```
</code>
<signature>
```java
package p0;

"""

JAVA_RUNNER_GENERATOR_PROMPT_v0 = """
You are an expert Java developer specializing in test case generation and verification. Your task is to generate a complete and executable Java test file that:
- Loads test cases from a JSON file generated by a Python test case generator
- Re-runs the logic under test using the loaded test cases
- Verifies the behavior of the function under test against the expected outputs

## Requirements
The generated Java test file must include:
1. **Imports**:
    - Jackson for JSON deserialization (ObjectMapper, TypeReference)
    - JUnit 5 (org.junit.jupiter.api.Test, org.junit.jupiter.api.Assertions)
    - Java standard libraries (File, List, Map)
2. **Test Case Structure**:
    - Define a static inner class TestCase that matches the structure of the JSON file
    - Nested structures must use appropriate Java types (e.g. Map<String, String>, List<...>)
3. **JSON Loading**:
    - Use Jackson's ObjectMapper to read the test case JSON from a file
    - Deserialize the content into a list of TestCase objects using TypeReference
4. **Test Method**:
    - Use a @Test method to loop through each test case
    - For each test case, call the function under test (e.g., Solution.processInput(...))
    - Compare actual output with expected output using assertEquals(...)
    - Provide a descriptive error message with the case index if the test fails
5. **Test File Location**:
    - Use relative path like "benchmark/Java/test_data.json" to locate the JSON file
6. **Naming**:
    - The generated Java class must be named Tester

## Input Example
The test case JSON file follows this structure:
```json
{testcases_str}
```

## Output Example

```json
{
    "JSONLoader": "import com.fasterxml.jackson.core.type.TypeReference;\nimport com.fasterxml.jackson.databind.ObjectMapper;\nimport org.junit.jupiter.api.Test;\n\nimport java.io.File;\nimport java.util.List;\nimport java.util.Map;\n\nimport static org.junit.jupiter.api.Assertions.assertEquals;\n\npublic class Tester {\n\n\tstatic class TestCase {\n\t\tpublic Map<String, Map<String, String>> Inputs;\n\t\tpublic Map<String, String> Expected;\n\t}\n\n\t@Test\n\tpublic void testFromJson() throws Exception {\n\t\tObjectMapper mapper = new ObjectMapper();\n\n\t\tList<TestCase> cases = mapper.readValue(\n\t\t\tnew File(\"benchmark/Java/test_data.json\"),\n\t\t\tnew TypeReference<List<TestCase>>() {}\n\t\t);\n\n\t\tfor (int i = 0; i < cases.size(); i++) {\n\t\t\tTestCase testCase = cases.get(i);\n\n\t\t\tMap<String, String> actual = Tested.processInput(testCase.Inputs);\n\n\t\t\tassertEquals(\n\t\t\t\ttestCase.Expected,\n\t\t\t\tactual,\n\t\t\t\t\"Test case \" + i + \" failed\"\n\t\t\t);\n\t\t}\n\t}\n}"
}
```

## Special Considerations for Java
- Object Mapping: Ensure that Java types align exactly with the JSON structure
- Static Inner Class: Use a nested TestCase class to simplify deserialization
- Readability: Ensure clear and structured test output on failure
- Encapsulation: Place all test logic in a single test class
- Error Messages: Include case index in failure messages for easier debugging

## Output Format
Generate a JSON object with a single key "JSONLoader" whose value is the complete Java test file code that:
- Matches the JSON structure
- Calls the correct method from the Solution class
- Handles all edge cases
- Is ready to compile and run with JUnit
"""

GO_RUNNER_GENERATOR_PROMPT = """
## Task Description
As an expert Go developer, generate two files from Python function definitions and JSON test cases:
1. `runner_test.go` - Test execution logic only
2. `tested.go` - Implementation signature with all required types

### Strict Requirements
1. **File Separation Rules**:
   - `runner_test.go` MUST contain:
     - TestCase struct (inline JSON structure only)
     - Test execution logic
     - NO implementation types
   - `tested.go` MUST contain:
     - Function signature
     - ALL types used in signature (even if also used in tests)
     - `// TODO: Implement` comment
     - NO test-related code

2. **Error Handling Rules**:
   - If Python function can raise exceptions:
     → Go function MUST return `(resultType, error)`
     → Test MUST verify no error occurs (since test cases are all valid inputs)
   - If Python has no error cases:
     → Go function returns only `resultType`

3. **Type Definition Rules**:
   | Usage Scenario                | Location         | Example                  |
   |-------------------------------|------------------|--------------------------|
   | Used in function signature    | `tested.go`      | `type TagInfo struct{}`  |
   | Only in test JSON structure   | Inline in TestCase | `Inputs struct{ Temp float64 }` |
   | Used in both                  | `tested.go`      | Shared types always in implementation |

4. **Test Validation Logic**:
   - For functions returning `(result, error)`:
     ```go
     actual, err := targetFunc(inputs)
     if err != nil {  // Should NEVER happen for provided test cases
         t.Errorf("Unexpected error for valid input: %v", err)
         return
     }
     // Proceed with value comparison
     ```
   - For functions returning `result` only:
     ```go
     actual := targetFunc(inputs)
     // Direct comparison
     ```

### Output Format
```plaintext
<code>
// runner_test.go
[Complete test file content]
</code>
<signature>
// tested.go
[Complete implementation file content]
</signature>

## Examples
### Example 1: Type definition used in both test and function signature
#### Input
Test Cases JSON:
```json
[
    {
      "Description": "Valid response structure with default tags",
      "Inputs": {
        "processed_str": "<think>thought</think><answer>answer</answer>"
      },
      "Expected": true
    }
]
```
Python Function:
```python
from typing import Dict

def validate_response_structure(processed_str: str, tags: Dict = None) -> bool:
    validation_passed = True
    # Check required tags
    if tags is None:
        tags = {
            "think_start": {"text": "<think>", "num_occur": 1},
            "think_end": {"text": "</think>", "num_occur": 1},
            "answer_start": {"text": "<answer>", "num_occur": 1},
            "answer_end": {"text": "</answer>", "num_occur": 1},
        }
    positions = {}
    for tag_name, tag_info in tags.items():
        tag_str = tag_info["text"]
        expected_count = tag_info["num_occur"]
        count = processed_str.count(tag_str)
        positions[tag_name] = pos = processed_str.find(tag_str)
        if count != expected_count:
            validation_passed = False
    # Verify tag order
    if (
        positions["think_start"] > positions["think_end"]
        or positions["think_end"] > positions["answer_start"]
        or positions["answer_start"] > positions["answer_end"]
    ):
        validation_passed = False
    if len(processed_str) - positions["answer_end"] != len(tags["answer_end"]["text"]):
        validation_passed = False
    return validation_passed
```
### Output
<code>
```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
    "testing"
)

// TestCase represents the structure of our test cases
type TestCase struct {
    Inputs struct {
        ProcessedStr string            `json:"processed_str"`
        Tags         map[string]TagInfo `json:"tags"`
    } `json:"Inputs"`
    Expected bool `json:"Expected"`
}

// loadTestCases reads and parses test cases from a JSON file
func loadTestCases(filePath string) ([]TestCase, error) {
    // Read the test cases file
    file, err := os.ReadFile(filePath)
    if err != nil {
        return nil, fmt.Errorf("failed to read test cases: %v", err)
    }

    // Parse the JSON content into a slice of TestCase
    var testCases []TestCase
    if err := json.Unmarshal(file, &testCases); err != nil {
        return nil, fmt.Errorf("failed to parse test cases: %v", err)
    }

    return testCases, nil
}

// TestValidateResponseStructure runs test cases for the validate_response_structure function
func TestValidateResponseStructure(t *testing.T) {
    // Load test cases from the JSON file
    testCases, err := loadTestCases("test_cases/test_cases.json")
    if err != nil {
        t.Fatalf("Failed to load test cases: %v", err)
    }

    // Iterate through each test case
    for i, tc := range testCases {
        t.Run(fmt.Sprintf("Case%d", i), func(t *testing.T) {
            // Call the function under test
            actual := validate_response_structure(tc.Inputs.ProcessedStr, tc.Inputs.Tags)

            // Compare the actual output with the expected result
            if !DeepCompare(actual, tc.Expected, 0) {
                t.Errorf(
                    `Test case %d failed:
Input:    %v
Expected: %v
Actual:   %v`,
                    i, tc.Inputs, tc.Expected, actual,
                )
            }
        })
    }
}
```
</code>
<signature>
```go
package main

// TagInfo represents the structure of tag information
type TagInfo struct {
    Text      string `json:"text"`
    NumOccur  int    `json:"num_occur"`
}

func validate_response_structure(processedStr string, tags map[string]TagInfo) bool {
	// TODO: Implement
}
```
</signature>
### Example 2: normal case with no error handling
#### Input
Test Cases JSON:
```json
[
    {
        "Inputs": {
            "lines": ["    def func():"],
            "line_index": 0
        },
        "Expected": ""
    },
    {
        "Inputs": {
            "lines": ["class MyClass:", "    pass"],
            "line_index": 1
        },
        "Expected": "    "
    }
]
```
Python Function:
```python
from typing import List

def _get_correct_indent_level(lines: List[str], line_index: int) -> str:
    \"\"\"Determine correct indentation level by looking at surrounding structure.\"\"\"
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
#### Output
<code>
```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
    "testing"
)

// TestCase represents the structure of our test cases
type TestCase struct {
    Inputs struct {
        Lines     []string `json:"lines"`
        LineIndex int      `json:"line_index"`
    } `json:"Inputs"`
    Expected string `json:"Expected"`
}

// loadTestCases reads and parses test cases from a JSON file
func loadTestCases(filePath string) ([]TestCase, error) {
    // Read the test cases file
    file, err := os.ReadFile(filePath)
    if err != nil {
        return nil, fmt.Errorf("failed to read test cases: %v", err)
    }

    // Parse the JSON content into a slice of TestCase
    var testCases []TestCase
    if err := json.Unmarshal(file, &testCases); err != nil {
        return nil, fmt.Errorf("failed to parse test cases: %v", err)
    }

    return testCases, nil
}

// TestGetCorrectIndentLevel runs test cases for the _get_correct_indent_level function
func TestGetCorrectIndentLevel(t *testing.T) {
    // Load test cases from the JSON file
    testCases, err := loadTestCases("test_cases/test_cases.json")
    if err != nil {
        t.Fatalf("Failed to load test cases: %v", err)
    }

    // Iterate through each test case
    for i, tc := range testCases {
        t.Run(fmt.Sprintf("Case%d", i), func(t *testing.T) {
            // Call the function under test
            actual := _get_correct_indent_level(tc.Inputs.Lines, tc.Inputs.LineIndex)

            // Compare the actual output with the expected result
            if !DeepCompare(actual, tc.Expected, 0) {
                t.Errorf(
                    `Test case %d failed:
Input:    %v
Expected: %q
Actual:   %q`,
                    i, tc.Inputs, tc.Expected, actual,
                )
            }
        })
    }
}
```
</code>
<signature>
```go
package main

func _get_correct_indent_level(lines []string, lineIndex int) string {
    // TODO: Implement
}
```
</signature>

### Example 3: Function with Potential Errors
Python Function:
```python
def parse_config(config: dict) -> str:
    if not config:
        raise ValueError("Empty config")
    return config["version"]
```
Test Cases JSON:
```json
[
    {
        "Inputs": {
            "config": {
                "version": "1.0.0",
                "debug": true
            }
        },
        "Expected": "1.0.0"
    },
    {
        "Inputs": {
            "config": {
                "version": "2.1.3"
            }
        },
        "Expected": "2.1.3"
    }
]
```
#### Output
<code>
```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
    "testing"
)

// TestCase represents the structure of our test cases
type TestCase struct {
    Inputs struct {
        Config map[string]interface{} `json:"config"`
    } `json:"Inputs"`
    Expected string `json:"Expected"`
}

// loadTestCases reads and parses test cases from a JSON file
func loadTestCases(filePath string) ([]TestCase, error) {
    file, err := os.ReadFile(filePath)
    if err != nil {
        return nil, fmt.Errorf("failed to read test cases: %v", err)
    }

    var testCases []TestCase
    if err := json.Unmarshal(file, &testCases); err != nil {
        return nil, fmt.Errorf("failed to parse test cases: %v", err)
    }
    return testCases, nil
}

// TestParseConfig runs test cases for the parse_config function
func TestParseConfig(t *testing.T) {
    testCases, err := loadTestCases("test_cases/test_cases.json")
    if err != nil {
        t.Fatalf("Failed to load test cases: %v", err)
    }

    for i, tc := range testCases {
        t.Run(fmt.Sprintf("Case%d", i), func(t *testing.T) {
            // Call the function under test
            actual, err := parse_config(tc.Inputs.Config)

            // Critical error check: Valid input should not return an error
            if err != nil {
                t.Errorf(`
[Invalid Error] Valid input should not return an error!
Input: %v
Error: %v`, tc.Inputs, err)
                return
            }

            // Result comparison
            if !DeepCompare(actual, tc.Expected, 0) {
                t.Errorf(`
[Result Mismatch]
Input: %v
Expected: %q
Actual: %q`, tc.Inputs, tc.Expected, actual)
            }
        })
    }
}
```
</code>
<signature>
```go
package main

func parse_config(config map[string]interface{}) (string, error) {
	// TODO: Implement
}
```
</signature>

## Note
- Ensure the generated runner_test.go file is complete and executable.
- The function signature should be a valid Go function signature that matches the Python function's behavior.
- Only return the runner_test.go file in `<code>` and the tested.go in `<signature>` tags.
"""

GO_RUNNER_GENERATOR_PROMPT_v4 = """
## Task Description
As an expert Go developer specializing in test case generation and function signature translation, your task is to generate two files:
1. A Go test file (`runner_test.go`) containing only test-related code
2. A Go implementation file (`tested.go`) containing the function signature and any required type definitions

### Requirements
1. **Go Test File (`runner_test.go`)**:
   - Generate a complete, executable Go test file in the `main` package
   - Include:
     - Necessary imports (`encoding/json`, `fmt`, `os`, `testing`)
     - A `TestCase` struct matching the JSON structure (only for test cases)
     - A `loadTestCases` function to read and parse the JSON file
     - A test function (e.g., `Test<FunctionName>`) with test execution logic
   - Do NOT include any types that will be used by the actual implementation

2. **Go Implementation File (`tested.go`)**:
   - Provide the function signature in the `main` package
   - Include ALL type definitions required by the function signature
   - Add a `// TODO: Implement` comment
   - Ensure the file is self-contained (can be used independently)

3. **Special Rules for Type Definitions**:
   - If a type is used in BOTH test cases and function signature:
    → Define it in `tested.go`
   - If a type is ONLY used in test cases:
    → Define it in `runner_test.go`
   - For nested JSON structures used in test cases:
    → Define them inline in the `TestCase` struct

4. **Output Format**:
```plaintext
<code>
// runner_test.go
[Complete test file content]
</code>
<signature>
// tested.go
[file content]
</signature>

## Examples
### Example 1: validate_response_structure
#### Input
Test Cases JSON:
```json
[
    {
      "Description": "Valid response structure with default tags",
      "Inputs": {
        "processed_str": "<think>thought</think><answer>answer</answer>"
      },
      "Expected": true
    }
]
```
Python Function:
```python
from typing import Dict

def validate_response_structure(processed_str: str, tags: Dict = None) -> bool:
    validation_passed = True
    # Check required tags
    if tags is None:
        tags = {
            "think_start": {"text": "<think>", "num_occur": 1},
            "think_end": {"text": "</think>", "num_occur": 1},
            "answer_start": {"text": "<answer>", "num_occur": 1},
            "answer_end": {"text": "</answer>", "num_occur": 1},
        }
    positions = {}
    for tag_name, tag_info in tags.items():
        tag_str = tag_info["text"]
        expected_count = tag_info["num_occur"]
        count = processed_str.count(tag_str)
        positions[tag_name] = pos = processed_str.find(tag_str)
        if count != expected_count:
            validation_passed = False
    # Verify tag order
    if (
        positions["think_start"] > positions["think_end"]
        or positions["think_end"] > positions["answer_start"]
        or positions["answer_start"] > positions["answer_end"]
    ):
        validation_passed = False
    if len(processed_str) - positions["answer_end"] != len(tags["answer_end"]["text"]):
        validation_passed = False
    return validation_passed
```
### Output
<code>
```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
    "testing"
)

// TestCase represents the structure of our test cases
type TestCase struct {
    Inputs struct {
        ProcessedStr string            `json:"processed_str"`
        Tags         map[string]TagInfo `json:"tags"`
    } `json:"Inputs"`
    Expected bool `json:"Expected"`
}

// loadTestCases reads and parses test cases from a JSON file
func loadTestCases(filePath string) ([]TestCase, error) {
    // Read the test cases file
    file, err := os.ReadFile(filePath)
    if err != nil {
        return nil, fmt.Errorf("failed to read test cases: %v", err)
    }

    // Parse the JSON content into a slice of TestCase
    var testCases []TestCase
    if err := json.Unmarshal(file, &testCases); err != nil {
        return nil, fmt.Errorf("failed to parse test cases: %v", err)
    }

    return testCases, nil
}

// TestValidateResponseStructure runs test cases for the validate_response_structure function
func TestValidateResponseStructure(t *testing.T) {
    // Load test cases from the JSON file
    testCases, err := loadTestCases("test_cases/test_cases.json")
    if err != nil {
        t.Fatalf("Failed to load test cases: %v", err)
    }

    // Iterate through each test case
    for i, tc := range testCases {
        t.Run(fmt.Sprintf("Case%d", i), func(t *testing.T) {
            // Call the function under test
            actual := validate_response_structure(tc.Inputs.ProcessedStr, tc.Inputs.Tags)

            // Compare the actual output with the expected result
            if !DeepCompare(actual, tc.Expected, 0) {
                t.Errorf(
                    `Test case %d failed:
Input:    %v
Expected: %v
Actual:   %v`,
                    i, tc.Inputs, tc.Expected, actual,
                )
            }
        })
    }
}
```
</code>
<signature>
```go
package main

// TagInfo represents the structure of tag information
type TagInfo struct {
    Text      string `json:"text"`
    NumOccur  int    `json:"num_occur"`
}

func validate_response_structure(processedStr string, tags map[string]TagInfo) bool {
	// TODO: Implement
}
```
</signature>
### Example 2: _get_correct_indent_level
#### Input
Test Cases JSON:
```json
[
    {
        "Inputs": {
            "lines": ["    def func():"],
            "line_index": 0
        },
        "Expected": ""
    },
    {
        "Inputs": {
            "lines": ["class MyClass:", "    pass"],
            "line_index": 1
        },
        "Expected": "    "
    }
]
```
Python Function:
```python
from typing import List

def _get_correct_indent_level(lines: List[str], line_index: int) -> str:
    \"\"\"Determine correct indentation level by looking at surrounding structure.\"\"\"
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
#### Output
<code>
```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
    "testing"
)

// TestCase represents the structure of our test cases
type TestCase struct {
    Inputs struct {
        Lines     []string `json:"lines"`
        LineIndex int      `json:"line_index"`
    } `json:"Inputs"`
    Expected string `json:"Expected"`
}

// loadTestCases reads and parses test cases from a JSON file
func loadTestCases(filePath string) ([]TestCase, error) {
    // Read the test cases file
    file, err := os.ReadFile(filePath)
    if err != nil {
        return nil, fmt.Errorf("failed to read test cases: %v", err)
    }

    // Parse the JSON content into a slice of TestCase
    var testCases []TestCase
    if err := json.Unmarshal(file, &testCases); err != nil {
        return nil, fmt.Errorf("failed to parse test cases: %v", err)
    }

    return testCases, nil
}

// TestGetCorrectIndentLevel runs test cases for the _get_correct_indent_level function
func TestGetCorrectIndentLevel(t *testing.T) {
    // Load test cases from the JSON file
    testCases, err := loadTestCases("test_cases/test_cases.json")
    if err != nil {
        t.Fatalf("Failed to load test cases: %v", err)
    }

    // Iterate through each test case
    for i, tc := range testCases {
        t.Run(fmt.Sprintf("Case%d", i), func(t *testing.T) {
            // Call the function under test
            actual := _get_correct_indent_level(tc.Inputs.Lines, tc.Inputs.LineIndex)

            // Compare the actual output with the expected result
            if !DeepCompare(actual, tc.Expected, 0) {
                t.Errorf(
                    `Test case %d failed:
Input:    %v
Expected: %q
Actual:   %q`,
                    i, tc.Inputs, tc.Expected, actual,
                )
            }
        })
    }
}
```
</code>
<signature>
```go
package main

func _get_correct_indent_level(lines []string, lineIndex int) string {
    // TODO: Implement
}
```
</signature>

### Example 3: Function with Potential Errors
Python Function:
```python
def parse_config(config: dict) -> str:
    if not config:
        raise ValueError("Empty config")
    return config["version"]
```
Test Cases JSON:
```json
[
    {
        "Inputs": {
            "config": {
                "version": "1.0.0",
                "debug": true
            }
        },
        "Expected": "1.0.0"
    },
    {
        "Inputs": {
            "config": {
                "version": "2.1.3"
            }
        },
        "Expected": "2.1.3"
    }
]
```
#### Output
<code>
```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
    "testing"
)

// TestCase represents the structure of our test cases
type TestCase struct {
    Inputs struct {
        Config map[string]interface{} `json:"config"`
    } `json:"Inputs"`
    Expected string `json:"Expected"`
}

// loadTestCases reads and parses test cases from a JSON file
func loadTestCases(filePath string) ([]TestCase, error) {
    file, err := os.ReadFile(filePath)
    if err != nil {
        return nil, fmt.Errorf("failed to read test cases: %v", err)
    }

    var testCases []TestCase
    if err := json.Unmarshal(file, &testCases); err != nil {
        return nil, fmt.Errorf("failed to parse test cases: %v", err)
    }
    return testCases, nil
}

// TestParseConfig runs test cases for the parse_config function
func TestParseConfig(t *testing.T) {
    testCases, err := loadTestCases("test_cases/test_cases.json")
    if err != nil {
        t.Fatalf("Failed to load test cases: %v", err)
    }

    for i, tc := range testCases {
        t.Run(fmt.Sprintf("Case%d", i), func(t *testing.T) {
            // Call the function under test
            actual, err := parse_config(tc.Inputs.Config)

            // Critical error check: Valid input should not return an error
            if err != nil {
                t.Errorf(`
[Invalid Error] Valid input should not return an error!
Input: %v
Error: %v`, tc.Inputs, err)
                return
            }

            // Result comparison
            if !DeepCompare(actual, tc.Expected, 0) {
                t.Errorf(`
[Result Mismatch]
Input: %v
Expected: %q
Actual: %q`, tc.Inputs, tc.Expected, actual)
            }
        })
    }
}
```
</code>
<signature>
```go
package main

func parse_config(config map[string]interface{}) (string, error) {
	// TODO: Implement
}
```
</signature>

## Note
- Ensure the generated runner_test.go file is complete and executable.
- The function signature should be a valid Go function signature that matches the Python function's behavior.
- Only return the runner_test.go file in `<code>` and the tested.go in `<signature>` tags.
"""

GO_RUNNER_GENERATOR_PROMPT_v3 = """
## Task Description
As an expert Go developer specializing in test case generation and function signature translation, your task is to generate a Go test file and function signature based on a Python function and its test cases. The test file will load test cases from a JSON file and execute tests using a provided `DeepCompare` helper function.

### Requirements
1. **Go Test File**:
   - Generate a complete, executable Go test file in the `main` package.
   - Include:
     - Necessary imports (`encoding/json`, `fmt`, `os`, `testing`).
     - A `TestCase` struct matching the JSON structure.
     - A `loadTestCases` function to read and parse the JSON file.
     - A test function (e.g., `Test<FunctionName>`) that:
       - Loads test cases.
       - Executes the function under test for each case.
       - Uses `DeepCompare` for output comparison.
       - Reports errors clearly with input, expected, and actual values.
   - Follow Go best practices:
     - Type-safe JSON parsing (avoid `interface{}` unless necessary).
     - Clear comments explaining key sections.
     - Separate JSON loading from test logic.
     - Use `t.Run` for individual test cases.
   - Output in `<code>` tags.

2. **Function Signature**:
   - Provide only the function signature in the `main` package.
   - Match the Python function’s input and output types (e.g., `List[str]` → `[]string`, `str` → `string`).
   - Include a `// TODO: Implement` comment.
   - Output in `<signature>` tags.

3. **Special Considerations**:
   - Ensure `TestCase` struct fields exactly match JSON keys and types.
   - Use specific Go types (e.g., `string`, `int`, `[]string`) to reflect JSON data.
   - Handle complex inputs (e.g., arrays, nested structures) accurately.
   - Do not implement the function in the test file.
   - Assume `DeepCompare(actual, expected, tolerance)` is defined elsewhere, with `tolerance` set to `1e-6` for floating-point comparisons (use `0` for non-floating-point types).
   - Return only `<code>` and `<signature>` sections, without additional explanations.

## Input Format
- **Test Cases JSON**: A JSON array of test cases, provided as `{testcases_str}`.
- **Python Function**: A Python function to be tested, including its signature and implementation, provided as code.

## Output Format
```plaintext
<code>
[Go test file]
</code>
<signature>
[Go function signature]
</signature>

## Examples
### Example 1: fast_format_html
#### Input
Test Cases JSON:
```json
[
    {
        "Inputs": {
            "html_string": "<div><p>Hello</p></div>"
        },
        "Expected": "<div>\n  <p>\n    Hello\n  </p>\n</div>"
    },
    {
        "Inputs": {
            "html_string": "<br/>"
        },
        "Expected": "<br/>"
    }
]
```
Python Function:
```python
def fast_format_html(html_string):
    indent = 0
    indent_str = "  "
    formatted = []
    parts = html_string.replace(">", ">\n").replace("<", "\n<").split("\n")
    for part in parts:
        if not part.strip():
            continue
        if part.startswith("</"):
            indent -= 1
            formatted.append(indent_str * indent + part)
        elif part.startswith("<") and part.endswith("/>"):
            formatted.append(indent_str * indent + part)
        elif part.startswith("<"):
            formatted.append(indent_str * indent + part)
            indent += 1
        else:
            content = part.strip()
            if content:
                formatted.append(indent_str * indent + content)
    return "\n".join(formatted)
```
### Output
<code>
```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
    "testing"
)

// TestCase represents the structure of our test cases
type TestCase struct {
    Inputs struct {
        HTMLString string `json:"html_string"`
    } `json:"Inputs"`
    Expected string `json:"Expected"`
}

// loadTestCases reads and parses test cases from a JSON file
func loadTestCases(filePath string) ([]TestCase, error) {
    // Read the test cases file
    file, err := os.ReadFile(filePath)
    if err != nil {
        return nil, fmt.Errorf("failed to read test cases: %v", err)
    }

    // Parse the JSON content into a slice of TestCase
    var testCases []TestCase
    if err := json.Unmarshal(file, &testCases); err != nil {
        return nil, fmt.Errorf("failed to parse test cases: %v", err)
    }

    return testCases, nil
}

// TestFastFormatHTML runs test cases for the fast_format_html function
func TestFastFormatHTML(t *testing.T) {
    // Load test cases from the JSON file
    testCases, err := loadTestCases("test_cases/test_cases.json")
    if err != nil {
        t.Fatalf("Failed to load test cases: %v", err)
    }

    // Iterate through each test case
    for i, tc := range testCases {
        t.Run(fmt.Sprintf("Case%d", i), func(t *testing.T) {
            // Call the function under test
            actual := fast_format_html(tc.Inputs.HTMLString)

            // Compare the actual output with the expected result
            if !DeepCompare(actual, tc.Expected, 0) {
                t.Errorf(
                    `Test case %d failed:
Input:    %q
Expected: %q
Actual:   %q`,
                    i, tc.Inputs.HTMLString, tc.Expected, actual,
                )
            }
        })
    }
}
```
</code>
<signature>
```go
package main

func fast_format_html(htmlString string) string {
    // TODO: Implement
}
```
</signature>
### Example 2: _get_correct_indent_level
#### Input
Test Cases JSON:
```json
[
    {
        "Inputs": {
            "lines": ["    def func():"],
            "line_index": 0
        },
        "Expected": ""
    },
    {
        "Inputs": {
            "lines": ["class MyClass:", "    pass"],
            "line_index": 1
        },
        "Expected": "    "
    }
]
```
Python Function:
```python
from typing import List

def _get_correct_indent_level(lines: List[str], line_index: int) -> str:
    \"\"\"Determine correct indentation level by looking at surrounding structure.\"\"\"
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
#### Output
<code>
```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
    "testing"
)

// TestCase represents the structure of our test cases
type TestCase struct {
    Inputs struct {
        Lines     []string `json:"lines"`
        LineIndex int      `json:"line_index"`
    } `json:"Inputs"`
    Expected string `json:"Expected"`
}

// loadTestCases reads and parses test cases from a JSON file
func loadTestCases(filePath string) ([]TestCase, error) {
    // Read the test cases file
    file, err := os.ReadFile(filePath)
    if err != nil {
        return nil, fmt.Errorf("failed to read test cases: %v", err)
    }

    // Parse the JSON content into a slice of TestCase
    var testCases []TestCase
    if err := json.Unmarshal(file, &testCases); err != nil {
        return nil, fmt.Errorf("failed to parse test cases: %v", err)
    }

    return testCases, nil
}

// TestGetCorrectIndentLevel runs test cases for the _get_correct_indent_level function
func TestGetCorrectIndentLevel(t *testing.T) {
    // Load test cases from the JSON file
    testCases, err := loadTestCases("test_cases/test_cases.json")
    if err != nil {
        t.Fatalf("Failed to load test cases: %v", err)
    }

    // Iterate through each test case
    for i, tc := range testCases {
        t.Run(fmt.Sprintf("Case%d", i), func(t *testing.T) {
            // Call the function under test
            actual := _get_correct_indent_level(tc.Inputs.Lines, tc.Inputs.LineIndex)

            // Compare the actual output with the expected result
            if !DeepCompare(actual, tc.Expected, 0) {
                t.Errorf(
                    `Test case %d failed:
Input:    %v
Expected: %q
Actual:   %q`,
                    i, tc.Inputs, tc.Expected, actual,
                )
            }
        })
    }
}
```
</code>
<signature>
```go
package main

func _get_correct_indent_level(lines []string, lineIndex int) string {
    // TODO: Implement
}
```
</signature>

## Note
- Ensure the generated Go test file is complete and executable.
- The function signature should be a valid Go function signature that matches the Python function's behavior.
- Only return the Go test file in `<code>` and the function signature in `<signature>` tags.
"""

GO_RUNNER_GENERATOR_PROMPT_v2 = """
You are an expert Go developer specializing in test case generation and function signature translation. Your task is to:

1. Generate a complete and executable Go test file that:
   - Loads test cases from a JSON file
   - Use DeepCompare for comparison which is a helper function has been defined in other files
   - Implements test execution logic

2. For the function implementation:
   - Only provide the function signature
   - Include a "TODO: Implement" comment
   - Match the Python function's input/output types

3. Test file requirements:
   - Package declaration and necessary imports
   - Test case structure matching JSON
   - Test loading and execution logic
   - Clear error reporting

4. Special considerations:
   - Include helpful comments
   - Follow Go best practices
   - Keep JSON loading separate from test logic
   
## Input and Output
The input will include a Python test case runner and a JSON file containing test cases. The output should be a Go test file and a function signature.

## Input Example
The test cases JSON file has the following structure:
```json
{testcases_str}
```
The python test case runner containes a Python function to be tested:
```python
def fast_format_html(html_string):
    # Initialize variables
    indent = 0
    indent_str = "  "  # Two spaces for indentation
    formatted = []
    # in_content = False

    # Split by < and > to separate tags and content
    parts = html_string.replace(">", ">\n").replace("<", "\n<").split("\n")

    for part in parts:
        if not part.strip():
            continue

        # Handle closing tags
        if part.startswith("</"):
            indent -= 1
            formatted.append(indent_str * indent + part)

        # Handle self-closing tags
        elif part.startswith("<") and part.endswith("/>"):
            formatted.append(indent_str * indent + part)

        # Handle opening tags
        elif part.startswith("<"):
            formatted.append(indent_str * indent + part)
            indent += 1

        # Handle content between tags
        else:
            content = part.strip()
            if content:
                formatted.append(indent_str * indent + content)

    return "\n".join(formatted)
```
## Output Example
<code>
```go
package main

import (
	"encoding/json"
	"fmt"
	"os"
	"testing"
)

// TestCase represents the structure of our test cases
type TestCase struct {
	Inputs struct {
		HTMLString string `json:"html_string"`
	} `json:"Inputs"`
	Expected string `json:"Expected"`
}

func loadTestCases(filePath string) ([]TestCase, error) {
	file, err := os.ReadFile(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to read test cases: %v", err)
	}

	var testCases []TestCase
	if err := json.Unmarshal(file, &testCases); err != nil {
		return nil, fmt.Errorf("failed to parse test cases: %v", err)
	}

	return testCases, nil
}

func TestFastFormatHTML(t *testing.T) {
	testCases, err := loadTestCases("test_cases/test_cases.json")
	if err != nil {
		t.Fatalf("Failed to load test cases: %v", err)
	}

	for i, tc := range testCases {
		t.Run(fmt.Sprintf("Case%d", i), func(t *testing.T) {
			// Call the function under test
			actual := fast_format_html(tc.Inputs.HTMLString)

			// Compare with expected result using DeepCompare
			if !DeepCompare(actual, tc.Expected, 1e-6) {
				t.Errorf(
`Test case %d failed:
Input:    %v
Expected: %v
Actual:   %v
`, i, tc.Inputs.HTMLString, tc.Expected, actual)
			}
		})
	}
}
```
</code>
<signature>
```go
package main

func fast_format_html(htmlString string) string {
    // TODO: Implement
}
```
</signature>

## Special Considerations for Go
- Type Safety: Ensure proper type conversion from JSON
- The parameter types in the signature should be as specific as possible to reflect the actual input types, avoiding the use of interface{} unless absolutely necessary
- Use DeepCompare for complex types
- Define TestCase struct to match JSON structure
- Don't implement the function in the test file
- Only return the Go test file in <code> and the function signature in <signature> tags
"""

GO_RUNNER_GENERATOR_PROMPT_v1 = """
You are an expert Go developer specializing in test case generation and function signature translation. Your task is to:

1. Generate a complete and executable Go test file that:
   - Loads test cases from a JSON file
   - Use DeepCompare for comparison which is a helper function has been defined in other files
   - Implements test execution logic

2. For the function implementation:
   - Only provide the function signature
   - Include a "TODO: Implement" comment
   - Match the Python function's input/output types

3. Test file requirements:
   - Package declaration and necessary imports
   - Test case structure matching JSON
   - Test loading and execution logic
   - Clear error reporting

4. Special considerations:
   - Include helpful comments
   - Follow Go best practices
   - Keep JSON loading separate from test logic
   
## Input and Output
The input will include a Python test case runner and a JSON file containing test cases. The output should be a Go test file and a function signature with appropriate imports from the official Go libraries. This is necessary because certain operations supported by basic types in Python may not be directly supported in Go, requiring the use of Go's standard libraries. Therefore, when Go's standard libraries are needed, the corresponding imports should be included in the function signature.

## Input Example
The test cases JSON file has the following structure:
```json
{testcases_str}
```
The python test case runner containes a Python function to be tested:
```python
def fast_format_html(html_string):
    # Initialize variables
    indent = 0
    indent_str = "  "  # Two spaces for indentation
    formatted = []
    # in_content = False

    # Split by < and > to separate tags and content
    parts = html_string.replace(">", ">\n").replace("<", "\n<").split("\n")

    for part in parts:
        if not part.strip():
            continue

        # Handle closing tags
        if part.startswith("</"):
            indent -= 1
            formatted.append(indent_str * indent + part)

        # Handle self-closing tags
        elif part.startswith("<") and part.endswith("/>"):
            formatted.append(indent_str * indent + part)

        # Handle opening tags
        elif part.startswith("<"):
            formatted.append(indent_str * indent + part)
            indent += 1

        # Handle content between tags
        else:
            content = part.strip()
            if content:
                formatted.append(indent_str * indent + content)

    return "\n".join(formatted)
```
## Output Example
<code>
```go
package main

import (
	"encoding/json"
	"fmt"
	"os"
	"testing"
)

// TestCase represents the structure of our test cases
type TestCase struct {
	Inputs struct {
		HTMLString string `json:"html_string"`
	} `json:"Inputs"`
	Expected string `json:"Expected"`
}

func loadTestCases(filePath string) ([]TestCase, error) {
	file, err := os.ReadFile(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to read test cases: %v", err)
	}

	var testCases []TestCase
	if err := json.Unmarshal(file, &testCases); err != nil {
		return nil, fmt.Errorf("failed to parse test cases: %v", err)
	}

	return testCases, nil
}

func TestFastFormatHTML(t *testing.T) {
	testCases, err := loadTestCases("test_cases/test_cases.json")
	if err != nil {
		t.Fatalf("Failed to load test cases: %v", err)
	}

	for i, tc := range testCases {
		t.Run(fmt.Sprintf("Case%d", i), func(t *testing.T) {
			// Call the function under test
			actual := fast_format_html(tc.Inputs.HTMLString)

			// Compare with expected result using DeepCompare
			if !DeepCompare(actual, tc.Expected, 1e-6) {
				t.Errorf(
`Test case %d failed:
Input:    %v
Expected: %v
Actual:   %v
`, i, tc.Inputs.HTMLString, tc.Expected, actual)
			}
		})
	}
}
```
</code>
<signature>
```go
package main

import strings // fast_format_html needs this package for string manipulation because Go does not support string operations like Python

func fast_format_html(htmlString string) string {
    // TODO: Implement
}
```
</signature>

## Special Considerations for Go
- Type Safety: Ensure proper type conversion from JSON
- Use DeepCompare for complex types
- Define TestCase struct to match JSON structure when it is needed
- Don't implement the function in the test file
- Import necessary Go standard libraries when needed
- Only return the Go test file in <code> and the function signature in <signature> tags
"""

GO_RUNNER_GENERATOR_PROMPT_v0 = """
You are an expert Go developer specializing in test case generation and verification. Your task is to generate a **complete and executable Go test file** that:
1. Loads test cases from a JSON file generated by the Python test case generator
2. Re-runs the test logic using the loaded test cases
3. Verifies the behavior of the function under test against the expected outputs

## Requirements
The generated Go test file must include:
1. **Package Declaration**: `package main`
2. **Imports**:
   - Required packages (`encoding/json`, `os`, `testing`, `fmt`, etc.)
   - The package containing the function under test
3. **Test Case Structure**:
   - Define a struct to represent test cases matching the JSON structure
4. **Test Loading**:
   - Implement a function to load test cases from JSON
5. **Test Execution**:
   - Implement table-driven tests using `testing.T`
   - Compare actual outputs with expected outputs
6. **Error Handling**:
   - Properly handle file loading errors
   - Provide detailed failure messages

## Input Example
The test cases JSON file has the following structure:
```json
{testcases_str}
## Output Example
```json
{
    "JSONLoader": "package main\n\nimport (\n\t\"encoding/json\"\n\t\"fmt\"\n\t\"os\"\n\t\"testing\"\n)\n\n// TestCase represents the structure of our test cases\ntype TestCase struct {\n\tInputs struct {\n\t\tMatrix [][]string `json:\"matrix_g\"`\n\t\tSize   int        `json:\"size\"`\n\t} `json:\"Inputs\"`\n\tExpected [][]string `json:\"Expected\"`\n}\n\nfunc loadTestCases(filePath string) ([]TestCase, error) {\n\tfile, err := os.ReadFile(filePath)\n\tif err != nil {\n\t\treturn nil, fmt.Errorf(\"failed to read test cases: %v\", err)\n\t}\n\n\tvar testCases []TestCase\n\tif err := json.Unmarshal(file, &testCases); err != nil {\n\t\treturn nil, fmt.Errorf(\"failed to parse test cases: %v\", err)\n\t}\n\n\treturn testCases, nil\n}\n\nfunc TestFunctionWithLoadedCases(t *testing.T) {\n\ttestCases, err := loadTestCases(\"test_cases/test_cases.json\")\n\tif err != nil {\n\t\tt.Fatalf(\"Failed to load test cases: %v\", err)\n\t}\n\n\tfor i, tc := range testCases {\n\t\tt.Run(fmt.Sprintf(\"Case%d\", i), func(t *testing.T) {\n\t\t\t// Make a copy of input to prevent modification\n\t\t\tinput := make([][]string, len(tc.Inputs.Matrix))\n\t\t\tfor i := range tc.Inputs.Matrix {\n\t\t\t\tinput[i] = make([]string, len(tc.Inputs.Matrix[i]))\n\t\t\t\tcopy(input[i], tc.Inputs.Matrix[i])\n\t\t\t}\n\n\t\t\t// Call the function under test\n\t\t\tactual := {Func1}(input, tc.Inputs.Size)\n\n\t\t\t// Compare with expected result\n\t\t\tif !compareMatrix(actual, tc.Expected) {\n\t\t\t\tt.Errorf(`\nTest case %d failed:\nInput:    %v\nExpected: %v\nActual:   %v\n`, i, tc.Inputs, tc.Expected, actual)\n\t\t\t}\n\t\t})\n\t}\n}\n\n// compareMatrix compares two 2D string slices\nfunc compareMatrix(a, b [][]string) bool {\n\tif len(a) != len(b) {\n\t\treturn false\n\t}\n\tfor i := range a {\n\t\tif len(a[i]) != len(b[i]) {\n\t\t\treturn false\n\t\t}\n\t\tfor j := range a[i] {\n\t\t\tif a[i][j] != b[i][j] {\n\t\t\t\treturn false\n\t\t\t}\n\t\t}\n\t}\n\treturn true\n}"
}
```
## Special Considerations for Go
- Type Safety: Ensure proper type conversion from JSON
- Input Copying: Make copies of input data to prevent modification
- Table Tests: Use Go's table-driven test pattern
- Error Messages: Provide detailed failure messages
- Comparison: Implement proper deep comparison for complex types
- File Path: Use absolute paths for test case files

## Output Format
Generate a JSON response containing a single key "JSONLoader". The value should be the complete Go test file code that:
- Matches the structure of the input test cases
- Properly tests the function under test
- Handles all edge cases
- Is ready to compile and run with go test
"""

WEAKLY_SELF_CONTAINED_RUNNER_GENERATOR_PROMPT = """
## Role
You are an expert Python developer specializing in property-based testing. Generate a **complete, executable Python script** that:
- Loads test cases from `test_cases.json` (generated by Hypothesis).
- Re-tests `func1` (from `tested` module) against ground truth `func0`.
- Outputs a **structured JSON diagnostic block** for automated parsing.

## Core Requirements

✅ MUST import:  
```python
from helper import deep_compare, load_test_cases_from_json
from tested import <function_name> as func1
```

✅ MUST define `ground truth` (copy from input, aka func0) to compute `expected_output` — **do not read "Expected" from JSON**.
```python
# Ground truth function (func0), keep its original implementation and name
```

✅ MUST use this diagnostic runner structure:
```python
def run_tests_with_loaded_cases_diagnostic(test_cases):
    passed_count = 0
    failed_count = 0
    failures = []
    execution_error = None

    try:
        for i, case in enumerate(test_cases):
            inputs = copy.deepcopy(case["Inputs"])
            # ← Type conversion here if needed (e.g., list → np.array)

            try:
                expected_output = ground_truth(...)  # ← Compute dynamically
                actual_output = func1(...)

                if compare_outputs(expected_output, actual_output):
                    passed_count += 1
                else:
                    failed_count += 1
                    failures.append({
                        "case_id": i+1,
                        "type": "TestFailure",
                        "inputs": inputs,
                        "expected": ...,  # serialize if it can be serialized
                        "actual": ...
                    })
            except Exception as e:
                failed_count += 1
                failures.append({
                    "case_id": i+1,
                    "type": "ExecutionError",
                    "inputs": inputs,
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                })

    except Exception as e:
        execution_error = {
            "type": "CriticalExecutionError",
            "error_type": type(e).__name__,
            "error_message": str(e)
        }

    summary = {
        "passed": passed_count,
        "failed": failed_count,
        "total": len(test_cases),
        "failures": failures[:10],
        "execution_error": execution_error
    }

    print("\\n---DIAGNOSTIC_SUMMARY_START---")
    print(json.dumps(summary, indent=2))
    print("---DIAGNOSTIC_SUMMARY_END---")
```

✅ MUST handle type conversion for inputs (e.g., JSON list → `np.ndarray`, tuple, etc.) before calling `func0`/`func1`.

✅ MUST define `compare_outputs(expected, actual)`:
- For basic types: `return deep_compare(expected, actual, tolerance=1e-6)`
- For NumPy: `np.allclose`
- For tuples: recursively compare elements

✅ MUST main block:
```python
if __name__ == "__main__":
    test_cases = load_test_cases_from_json()
    run_tests_with_loaded_cases_diagnostic(test_cases)
```

---

## 🎯 Input Format

You will receive a Testcase Generator script in `<Testcase Generator>` tags. It contains:
- `func0` (ground truth)
- Hypothesis test logic
- Saves test cases with ONLY `"Inputs"` (no `"Expected"`)

---

## 🧩 Output Format

Generate a single ```python``` block that:
1. Imports (including `func1`, `helper` utilities, and `func0`’s dependencies)
2. Defines `func0` (copied from input)
3. Defines `compare_outputs`
4. Defines `run_tests_with_loaded_cases_diagnostic` (use template above)
5. Includes main guard with fallback for empty test cases

---

## 💡 Examples (Abbreviated — Show Pattern, Not Full Code)

### Example 1: String → List (re module)
- `func0`: `extract_email_domains(text: str) → list[str]`
- Input conversion: none (str is JSON-native)
- Compare: `deep_compare`

### Example 2: NumPy Arrays → Tuple[np.ndarray, np.ndarray]
- `func0`: `chain_pair_pde(num_tokens, asym_ids, full_pde)`
- Input conversion:
  ```python
  asym_ids = np.array(inputs["asym_ids"], dtype=np.int32)
  full_pde = np.array(inputs["full_pde"], dtype=np.float32)
  ```
- Compare: `np.allclose` for arrays, recursive for tuple

### Example 3: List[Dict] → Dict[List]
- `func0`: `list_of_flat_dict_to_dict_of_list(list_of_dict)`
- Input conversion: none (dict/list are JSON-native)
- Compare: `deep_compare`

> 💡 In all cases: **compute expected_output by calling ground truth function (func0)**, never assume it’s in JSON.

---

## ⚠️ Critical Notes

- DO NOT redefine `load_test_cases_from_json` — import from `helper`.
- DO NOT skip deep copying mutable inputs.
- DO serialize non-JSON-safe types in failure reports (e.g., `ndarray.tolist()`, `str(obj)`).
- DO catch per-case exceptions — don’t let one failure stop the whole suite.
- DO wrap final summary in `---DIAGNOSTIC_SUMMARY_START---` / `END` tags.

Generate the script now.
"""

WEAKLY_SELF_CONTAINED_RUNNER_GENERATOR_PROMPT_V0 = """
## Task Description
You are an expert Python developer specializing in property-based testing and test case execution. Your task is to generate a **complete and executable Python script** that loads test cases from a JSON file generated by a Hypothesis-based Testcase Generator and re-runs the test logic to verify the behavior of a function under test (`func1`) against a ground truth function (`func0`). The functions depend only on standard libraries or specific external libraries (e.g., NumPy, re) and no other custom modules. The script will:
1. Load test cases from the JSON file (`test_cases.json`) containing 500 test cases, each with a `"Inputs"` dictionary mapping `func0`’s argument names to JSON-serializable values.
2. Re-run the test logic by calling `func0` (ground truth) and `func1` (under test) with the loaded inputs, comparing their outputs via differential testing.
3. Compare outputs using:
   - For basic types and their combinations (`int`, `float`, `str`, `list`, `dict`, etc.), use `deep_compare` from the `helper` module.
   - For third-party library types (e.g., `numpy.ndarray`, `tuple` of `numpy.ndarray`), use library-provided comparison functions (e.g., `np.allclose`) or custom logic if none is provided.
4. Report test results, indicating whether each test case passes or fails, with detailed failure information (inputs, expected output, actual output).

## Input
The input is a Python Testcase Generator script that includes:
1. The ground truth function `func0`, its dependencies (e.g., `numpy`, `re`), and implementation.
2. Hypothesis strategies and `@example` decorators defining input generation logic.
3. A test function (`test_<function_name>`) that generates and saves 500 test cases to `test_cases.json`, each containing only `"Inputs"`.
Provided in `<Testcase Generator>` tags.

## Output
Generate a complete, executable Python script that:
1. **Includes Necessary Imports**:
- Import `json`, `os`, and `copy` for file handling and deep copying.
- Import `helper` for `deep_compare` to compare basic types and combinations.
- Import external libraries used by `func0` (e.g., `numpy as np`, `re`).
- Import `func1` as the function under test (e.g., `from tested import chain_pair_pde as func1`).
2. **Defines `func0`**:
- Copy the ground truth function `func0` from the Testcase Generator to compute expected outputs.
3. **Loads Test Cases**:
- Define a `load_test_cases_from_json` function to read `test_cases.json` from `TEST_CASE_DIR`.
- Return an empty list if the file is missing, printing a warning.
4. **Compares Outputs**:
Basic types and their combinations (e.g., `int`, `float`, `str`, `list`, `dict`, and their nesting): use `deep_compare(a, b, tolerance=1e-6)` from `helper`.
Third-party library-related types (e.g., `np.ndarray`, `tuple[np.ndarray]`):  
- Prefer using the comparison functions provided by the library (e.g., `np.allclose` for NumPy).
- If the library does not provide a dedicated comparison function, implement custom logic to compare the outputs.
5. **Runs Tests**:
- Define a `run_tests_with_loaded_cases` function that:
- Iterates over test cases.
- Converts JSON inputs to `func0`’s expected types (e.g., `list` to `np.ndarray` for NumPy arrays).
- Makes deep copies of mutable inputs (e.g., arrays, lists) to avoid modification.
- Calls `func0` and `func1` with the inputs.
- Compares outputs using `compare_outputs`.
- Prints pass/fail status for each test case.
- For failures, prints the case number, inputs, expected output, and actual output.
6. **Main Execution**:
- Loads test cases and runs tests under `if __name__ == "__main__":`.
7. **Handles Complex Types**:
- Converts JSON-serialized inputs (e.g., `list` for `np.ndarray`) back to `func0`’s expected types (e.g., `np.array(inputs["asym_ids"], dtype=np.int32)`).
- Supports tuple outputs (e.g., `tuple[np.ndarray, np.ndarray]`) by comparing each element.
8. **Executable and Minimal**:
- Ensures the script is self-contained, executable, and includes only necessary logic.
- Uses the same `TEST_CASE_DIR` as the Testcase Generator (`os.path.abspath("test_cases")`).

Output the script in ```python``` tags.

## Example

#### Input
<Testcase Generator>
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
    \"\"\"Extract unique email domains from a text string.

    Args:
        text: A string containing potential email addresses.

    Returns:
        A sorted list of unique email domains (e.g., ['gmail.com', 'yahoo.com']).
    \"\"\"
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
</Testcase Generator>
Output:
```python
import json
import os
import copy
import re
from helper import deep_compare
from tested import extract_email_domains as func1

# Configure save path
TEST_CASE_DIR = os.path.abspath("test_cases")
TEST_CASE_JSON_PATH = os.path.join(TEST_CASE_DIR, "test_cases.json")

# Ground truth function
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

def load_test_cases_from_json():
    if not os.path.exists(TEST_CASE_JSON_PATH):
        print(f"JSON file not found: {TEST_CASE_JSON_PATH}")
        return []
    with open(TEST_CASE_JSON_PATH, "r") as f:
        test_cases = json.load(f)
    return test_cases

def run_tests_with_loaded_cases(test_cases):
    for i, case in enumerate(test_cases):
        inputs = copy.deepcopy(case["Inputs"])
        text = inputs["text"]

        # Run ground truth and function under test
        expected_output = extract_email_domains(text)
        actual_output = func1(text)

        # Compare outputs
        if compare_outputs(expected_output, actual_output):
            print(f"Test case {i + 1} passed.")
        else:
            print(f"Test case {i + 1} failed:")
            print(f"  Inputs: {inputs}")
            print(f"  Expected: {expected_output}")
            print(f"  Actual: {actual_output}")

if __name__ == "__main__":
    test_cases = load_test_cases_from_json()
    run_tests_with_loaded_cases(test_cases)
```
Input:
<Testcase Generator>
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

# Strategies for generating inputs
def num_tokens_strategy():
    return st.integers(min_value=0, max_value=10)

def asym_ids_strategy(num_tokens):
    return hnp.arrays(
        dtype=np.int32,
        shape=(num_tokens,),
        elements=st.integers(min_value=0, max_value=5),
    )

def full_pde_strategy(num_tokens):
    return hnp.arrays(
        dtype=np.float32,
        shape=st.tuples(
            st.integers(min_value=1, max_value=3),
            st.just(num_tokens),
            st.just(num_tokens),
        ),
        elements=st.floats(
            min_value=-10.0, max_value=10.0, allow_nan=False, allow_infinity=False
        ),
    )

# Hypothesis test configuration
@settings(max_examples=10000, verbosity=Verbosity.verbose, print_blob=True)
@given(
    num_tokens=num_tokens_strategy(),
    asym_ids=st.builds(lambda n: asym_ids_strategy(n), num_tokens_strategy()),
    full_pde=st.builds(lambda n: full_pde_strategy(n), num_tokens_strategy()),
)
@example(
    num_tokens=0,
    asym_ids=np.array([]),
    full_pde=np.array([[]]),
)
@example(
    num_tokens=1,
    asym_ids=np.array([0]),
    full_pde=np.array([[[0.0]]]),
)
@example(
    num_tokens=3,
    asym_ids=np.array([0, 0, 1]),
    full_pde=np.array(
        [
            [
                [1.0, 2.0, 3.0],
                [2.0, 1.0, 4.0],
                [3.0, 4.0, 1.0],
            ]
        ]
    ),
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
        expected_mean, expected_min = chain_pair_pde(
            num_tokens_copy, asym_ids_copy, full_pde_copy
        )
    except Exception:
        return

    generated_cases.append(
        {
            "Inputs": {
                "num_tokens": num_tokens_copy,
                "asym_ids": asym_ids_copy.tolist(),
                "full_pde": full_pde_copy.tolist(),
            }
        }
    )

    if len(generated_cases) >= 500:
        stop_collecting = True

# Save test cases
def save_test_cases():
    with open(TEST_CASE_FILE, "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(generated_cases)} test cases to {TEST_CASE_FILE}")

atexit.register(save_test_cases)
```
</Testcase Generator>
Output:
```python
import json
import os
import copy
import numpy as np
from helper import deep_compare
from tested import chain_pair_pde as func1

# Configure save path
TEST_CASE_DIR = os.path.abspath("test_cases")
TEST_CASE_JSON_PATH = os.path.join(TEST_CASE_DIR, "test_cases.json")

# Ground truth function
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

def load_test_cases_from_json():
    if not os.path.exists(TEST_CASE_JSON_PATH):
        print(f"JSON file not found: {TEST_CASE_JSON_PATH}")
        return []
    with open(TEST_CASE_JSON_PATH, "r") as f:
        test_cases = json.load(f)
    return test_cases

def compare_outputs(expected, actual):
    # Handle third-party library types (e.g., NumPy arrays)
    if isinstance(expected, np.ndarray) and isinstance(actual, np.ndarray):
        return np.allclose(expected, actual, rtol=1e-05, atol=1e-08)
    elif isinstance(expected, tuple) and isinstance(actual, tuple):
        if len(expected) != len(actual):
            return False
        return all(compare_outputs(exp, act) for exp, act in zip(expected, actual))
    # Handle basic types and combinations (int, float, str, list, dict, etc.)
    return deep_compare(expected, actual, tolerance=1e-6)

def run_tests_with_loaded_cases(test_cases):
    for i, case in enumerate(test_cases):
        inputs = copy.deepcopy(case["Inputs"])
        num_tokens = inputs["num_tokens"]
        asym_ids = np.array(inputs["asym_ids"], dtype=np.int32)
        full_pde = np.array(inputs["full_pde"], dtype=np.float32)

        # Run ground truth and function under test
        expected_output = chain_pair_pde(num_tokens, asym_ids, full_pde)
        actual_output = func1(num_tokens, asym_ids, full_pde)

        # Compare outputs
        if compare_outputs(expected_output, actual_output):
            print(f"Test case {i + 1} passed.")
        else:
            print(f"Test case {i + 1} failed:")
            print(f"  Inputs: {inputs}")
            print(f"  Expected: {expected_output}")
            print(f"  Actual: {actual_output}")


if __name__ == "__main__":
    test_cases = load_test_cases_from_json()
    run_tests_with_loaded_cases(test_cases)
```

## Note
- Focus on Loading and Re-testing: Load test cases from test_cases.json and verify func1 against func0 using differential testing.
- Preserve Input Format: Ensure inputs match func0’s signature, converting JSON-serialized inputs (e.g., list to np.ndarray) as needed.
- Output Comparison:
- Use deep_compare from helper for basic types and combinations (int, float, str, list, dict, etc.).
- Use library-provided comparisons (e.g., np.allclose for numpy.ndarray) for third-party library types, or custom logic if none is provided.
- Executable Code: The script must be complete, self-contained, and executable.
- Differential Testing: Since test cases contain only inputs, compute expected outputs by calling func0 and compare with func1’s outputs.
- External Libraries: Include imports for func0’s dependencies (e.g., numpy, re) and handle their data types (e.g., np.ndarray).
"""

RUNNER_GENERATOR_PROMPT = """
## Task Description
You are an expert Python developer specializing in property-based testing with the `hypothesis` library and test case generation. Your task is to generate a **complete and executable Python script** that loads test cases from a JSON file and re-runs the test logic using the loaded test cases.

The input code provided will include:
1. A Hypothesis-based test function (`test_<function_name>`) that generates test cases and saves them to a JSON file.
2. The reference implementation of the function being tested (e.g., `move_y`).

Your output should be a new Python script that:
1. **Loads test cases from the JSON file** generated by the input code.
2. **Re-runs the test logic** using the loaded test cases to verify the behavior of the function under test (`func1`).
3. Ensures the output is a complete, self-contained Python script that can be executed directly.

## Input
The input is a Python code snippet that includes a Hypothesis test function and a reference implementation. You need to generate a new Python script that loads test cases from a JSON file and re-runs the test logic in output.

## Example
The Python code for generating test cases is provided below:
```python
from hypothesis import settings, given, Verbosity
from hypothesis import strategies as st
from tested import move_y as func1
import json
import os

TEST_CASE_DIR = os.path.abspath("test_cases")
os.makedirs(TEST_CASE_DIR, exist_ok=True)

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

generated_cases = []

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
        min_size=1, max_size=10  # Number of rows between 1 and 10
    ),
    size=st.integers(min_value=1, max_value=10)  # Matrix size limited to 1-10
)
def test_move_y(matrix_g: list[list[str]], size: int):
    # Ensure matrix dimensions match the specified size
    if len(matrix_g) != size or any(len(row) != size for row in matrix_g):
        return

    # Calculate expected output using reference implementation
    expected_output = move_y([row[:] for row in matrix_g], size)  # Copy matrix to avoid in-place modification

    # Calculate actual output using function under test
    actual_output = func1([row[:] for row in matrix_g], size)  # Also copy matrix

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
    
    # Save test cases to JSON file (note this should be inside test function)
    with open(os.path.join(TEST_CASE_DIR, "test_cases.json"), "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(generated_cases)} test cases to {TEST_CASE_DIR}")
```
## Output
```python
import json
import os
from tested import move_y as func1
from helper import deep_compare

# Configure save path
TEST_CASE_DIR = os.path.abspath("test_cases")
TEST_CASE_JSON_PATH = os.path.join(TEST_CASE_DIR, "test_cases.json")

def load_test_cases_from_json():
    if not os.path.exists(TEST_CASE_JSON_PATH):
        print(f"JSON file not found: {TEST_CASE_JSON_PATH}")
        return []

    # Read JSON file
    with open(TEST_CASE_JSON_PATH, "r") as f:
        test_cases = json.load(f)

    return test_cases

def run_tests_with_loaded_cases(test_cases):
    for i, case in enumerate(test_cases):
        inputs = case["Inputs"]
        expected_output = case["Expected"]

        # Run function under test
        actual_output = func1(**inputs)  # Copy matrix to avoid in-place modification

        # Check if results match using deep_compare
        if not deep_compare(actual_output, expected_output, tolerance=1e-6):
            print(f"Test case {i + 1} failed:")
            print(f"  Inputs: {inputs}")
            print(f"  Expected: {expected_output}")
            print(f"  Actual: {actual_output}")
        else:
            print(f"Test case {i + 1} passed.")

if __name__ == "__main__":
    test_cases = load_test_cases_from_json()
    run_tests_with_loaded_cases(test_cases)
```
## Note
- **Focus on Loading and Re-testing**: The primary goal is to load test cases from the JSON file and re-run the test logic to verify the behavior of the function under test.
- **Preserve Original Input Format**: Ensure the input format (e.g., `matrix_g`, `size`) matches the original Hypothesis test code.
- **Executable Code**: The generated code must be a complete, self-contained Python script that can be executed directly.
- **Deep Comparison**: Use a helper function to compare complex data structures, especially for floating-point numbers, to avoid precision issues.
- Only return the code in ```python` tags.
"""

RUNNER_GENERATOR_PROMPT_v0 = """
## Task Description
You are an expert Python developer specializing in property-based testing with the `hypothesis` library and test case generation. Your task is to generate a **complete and executable Python script** that loads test cases from a JSON file and re-runs the test logic using the loaded test cases.

The input code provided will include:
1. A Hypothesis-based test function (`test_<function_name>`) that generates test cases and saves them to a JSON file.
2. The reference implementation of the function being tested (e.g., `move_y`).

Your output should be a new Python script that:
1. **Loads test cases from the JSON file** generated by the input code.
2. **Re-runs the test logic** using the loaded test cases to verify the behavior of the function under test (`func1`).
3. Ensures the output is a complete, self-contained Python script that can be executed directly.

## Input
The Python code for generating test cases and saving them to a JSON file is provided below:
```python
from hypothesis import settings, given, Verbosity
from hypothesis import strategies as st
from tested import move_y as func1
import json
import os

TEST_CASE_DIR = os.path.abspath("test_cases/move_y")
os.makedirs(TEST_CASE_DIR, exist_ok=True)

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

generated_cases = []

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
        min_size=1, max_size=10  # Number of rows between 1 and 10
    ),
    size=st.integers(min_value=1, max_value=10)  # Matrix size limited to 1-10
)
def test_move_y(matrix_g: list[list[str]], size: int):
    # Ensure matrix dimensions match the specified size
    if len(matrix_g) != size or any(len(row) != size for row in matrix_g):
        return

    # Calculate expected output using reference implementation
    expected_output = move_y([row[:] for row in matrix_g], size)  # Copy matrix to avoid in-place modification

    # Calculate actual output using function under test
    actual_output = func1([row[:] for row in matrix_g], size)  # Also copy matrix

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
    
    # Save test cases to JSON file (note this should be inside test function)
    with open(os.path.join(TEST_CASE_DIR, "test_cases.json"), "w") as f:
        json.dump(generated_cases, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(generated_cases)} test cases to {TEST_CASE_DIR}")
```
## Output
Generate a JSON response containing a single key "JSONLoader". The value of "JSONLoader" should be a string containing the complete Python code for loading test cases from the JSON file and re-running the test logic. The generated code must include:
1. **Import Statements**:
   - Import necessary libraries (`json`, `os`, etc.).
   - Import the function under test (`func1`) from the tested module.
2. **Configuration**:
   - Define the directory path (`TEST_CASE_DIR`) where the JSON file is saved.
   - Define the JSON file path (`TEST_CASE_JSON_PATH`).
3. **Load Test Cases**:
   - Implement a function (`load_test_cases_from_json`) to load test cases from the JSON file.
4. **Run Tests**:
   - Implement a function (`run_tests_with_loaded_cases`) to re-run the test logic using the loaded test cases.
5. **Main Program Logic**:
   - Load test cases and run tests when the script is executed.

The generated code must be ready to be executed.

## Example
For the input Hypothesis test driver code:
```python
from hypothesis import settings, given, Verbosity
from hypothesis import strategies as st
from tested import move_y as func1
import json
import os

# Configure save path
TEST_CASE_DIR = os.path.abspath("test_cases/move_y")
os.makedirs(TEST_CASE_DIR, exist_ok=True)

# Reference implementation
def move_y(matrix_g: list[list[str]], size: int) -> list[list[str]]:
    ...
```

The generated JSON loader might look like:
```python
import json
import os
from tested import move_y as func1

# Configure save path
TEST_CASE_DIR = os.path.abspath("test_cases/move_y")
TEST_CASE_JSON_PATH = os.path.join(TEST_CASE_DIR, "test_cases.json")

def load_test_cases_from_json():
    if not os.path.exists(TEST_CASE_JSON_PATH):
        print(f"JSON file not found: {TEST_CASE_JSON_PATH}")
        return []

    # Read JSON file
    with open(TEST_CASE_JSON_PATH, "r") as f:
        test_cases = json.load(f)

    return test_cases

def run_tests_with_loaded_cases(test_cases):
    for i, case in enumerate(test_cases):
        inputs = case["Inputs"]
        expected_output = case["Expected"]

        # Extract input parameters
        matrix_g = inputs["matrix_g"]
        size = inputs["size"]

        # Run function under test
        actual_output = func1([row[:] for row in matrix_g], size)  # Copy matrix to avoid in-place modification

        # Check if results match
        if actual_output != expected_output:
            print(f"Test case {i + 1} failed:")
            print(f"  Inputs: {inputs}")
            print(f"  Expected: {expected_output}")
            print(f"  Actual: {actual_output}")
        else:
            print(f"Test case {i + 1} passed.")

if __name__ == "__main__":
    test_cases = load_test_cases_from_json()
    run_tests_with_loaded_cases(test_cases)
```
## Note
- **Focus on Loading and Re-testing**: The primary goal is to load test cases from the JSON file and re-run the test logic to verify the behavior of the function under test.
- **Preserve Original Input Format**: Ensure the input format (e.g., `matrix_g`, `size`) matches the original Hypothesis test code.
- **Handle Missing Files Gracefully**: If the JSON file does not exist, print an appropriate message and exit gracefully.
- **Executable Code**: The generated code must be a complete, self-contained Python script that can be executed directly.
"""


TS_RUNNER_GENERATOR_PROMPT = """
## Task Description
As an expert TypeScript developer specializing in test case generation and function signature translation, your task is to generate a function signature based on a Python function and its test cases.

### Requirements
1. **Function Signature**:
   - Match the Python function’s input and output types (e.g., List[str] → string[], str → string).
   - Use export function declarations, include a // TODO: Implement comment inside the function.
   - Output in `<signature>` tags.

2. **Special Considerations**:
   - Use explicit and specific TypeScript types, avoiding any or object for type safety.
   - Handle complex inputs (e.g., arrays, tuples, nested structures) precisely.
   - Return only `<signature>` sections, without additional explanations.

## Input Format
- **Python Function**: A Python function to be tested, including its signature and implementation, provided as code.

## Output Format
```plaintext
<signature>
[TypeScript function signature]
</signature>

## Examples
### Example 1: fast_format_html
#### Input
Python Function:
```python
def fast_format_html(html_string):
    indent = 0
    indent_str = "  "
    formatted = []
    parts = html_string.replace(">", ">\n").replace("<", "\n<").split("\n")
    for part in parts:
        if not part.strip():
            continue
        if part.startswith("</"):
            indent -= 1
            formatted.append(indent_str * indent + part)
        elif part.startswith("<") and part.endswith("/>"):
            formatted.append(indent_str * indent + part)
        elif part.startswith("<"):
            formatted.append(indent_str * indent + part)
            indent += 1
        else:
            content = part.strip()
            if content:
                formatted.append(indent_str * indent + content)
    return "\n".join(formatted)
```
### Output
<signature> 
```ts 
export function fast_format_html(htmlString: string): string { 
    // TODO: Implement
} 
``` 
</signature>
### Example 2: _get_correct_indent_level
#### Input
Python Function:
```python
from typing import List

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
#### Output
<signature> 
```ts 
export function _get_correct_indent_level(lines: string[], lineIndex: number): string { 
    // TODO: Implement 
}
``` 
</signature>
"""
