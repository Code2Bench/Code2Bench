import json
import os

from code2bench import logger
from code2bench.prompt.runner_generator import JAVA_RUNNER_GENERATOR_PROMPT, TS_RUNNER_GENERATOR_PROMPT
from code2bench.data_model import GeneratedDriver
from code2bench.llm.llm_caller import call_llm
from code2bench.utils.json_utils import clean_response_content
from code2bench.data_model import GeneratedDriver

class TestcaseGenerator:
    def __init__(self, func_name: str, gt_example: dict, tested_file_path: str):
        self.func_name = func_name
        self.gt_example = gt_example
        self.tested_file_path = tested_file_path
    
    def generate(self) -> GeneratedDriver:
        return GeneratedDriver()
    

class TSGenerator(TestcaseGenerator):
    def __init__(self, func_name: str, gt_example: dict, tested_file_path: str, idx: str, llm):
        super().__init__(func_name, gt_example, tested_file_path)
        self.llm = llm
        self.idx = idx

    def build_code(self, def_string: str, call_string: str) -> str:
        return f"""import fs from 'fs';
import path from 'path';
import {{ {self.func_name} as func }} from '{self.tested_file_path}';
    
function loadTestCases(filePath: string): any[] {{
    const rawData = fs.readFileSync(filePath, 'utf-8');
    const testCases = JSON.parse(rawData);
    return testCases;
}}
    
describe('mergeJsonRecursive', () => {{
    const testCases = loadTestCases('./{self.idx}/test_cases/test_cases.json');
    
    testCases.forEach((tc, index) => {{
        test(`Case {{index}}`, () => {{
{def_string}
{call_string}

            expect(deepCompare(result, tc.Expected)).toEqual(true);
        }});
    }});
}});

function isClose(a: number, b: number, tolerance: number = 1e-6): boolean {{
    return Math.abs(a - b) <= tolerance;
}}

function deepCompare(a: any, b: any, tolerance: number = 1e-6): boolean {{
    if (typeof a === "number" && typeof b === "number") {{
        return isClose(a, b, tolerance);
    }} else if (Array.isArray(a) && Array.isArray(b)) {{
        if (a.length !== b.length) return false;
        return a.every((ai, index) => deepCompare(ai, b[index], tolerance));
    }} else if (
        a !== null && typeof a === "object" &&
        b !== null && typeof b === "object"
    ) {{
        const aKeys = Object.keys(a);
        const bKeys = Object.keys(b);
        if (aKeys.length !== bKeys.length) return false;
        return aKeys.every(k => k in b && deepCompare(a[k], b[k], tolerance));
    }} else {{
        return a === b;
    }}
}}
"""
    
    def generate_template(self, python_runner: str, testcases_str: str):
        system_prompt = TS_RUNNER_GENERATOR_PROMPT
        system_prompt = system_prompt.replace("{", "{{").replace("}", "}}")
        user_message = python_runner
        try:
            response = call_llm(self.llm, system_message=system_prompt, user_message=user_message)
            signature = self.parse_llm_response(response)
            # res = json.loads(cleaned_response)
            # driver = res["JSONLoader"]
            return GeneratedDriver(driver=self.generate()), signature
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(f"Generating driver failed: {e}")
            return GeneratedDriver(error=str(e)), ""
        
    def parse_llm_response(self, response: str):
        def clean_code_block(block: str) -> str:
            if block.startswith("```ts"):
                block = block[len("```ts"):].strip()
            if block.endswith("```"):
                block = block[:-len("```")].strip()
            return block

        # Extract code and signature parts
        signature_start = response.find("<signature>") + len("<signature>")
        signature_end = response.find("</signature>")

        # Validate the response format
        if signature_start == -1 or signature_end == -1:
            raise ValueError("Invalid response format. Missing code or signature tags.")

        # Extract and clean the code and signature
        signature = response[signature_start:signature_end].strip()

        # Remove ```go markers
        signature = clean_code_block(signature)

        return signature

    def generate(self):
        blank = " " * 12
        def_string = ""
        args = []
        input_example = self.gt_example["Inputs"]
        sigs = []
        for key, value in input_example.items():
            def_string += blank + f'let {key}_1: any = tc.Inputs.{key};\n'
            args.append(f"{key}_1")
            sigs.append(f"{key}: any")
        call_string = f"{blank}const result = func({', '.join(args)})"
        code = self.build_code(def_string, call_string)
        return code
    
class JSGenerator(TestcaseGenerator):
    def __init__(self, func_name: str, gt_example: dict, tested_file_path: str, idx: str):
        super().__init__(func_name, gt_example, tested_file_path)
        self.idx = idx

    def build_code(self, def_string: str, call_string: str) -> str:
        return f"""import fs from 'fs';
import path from 'path';
import {{ {self.func_name} as func }} from '{self.tested_file_path}';
    
function loadTestCases(filePath) {{
    const rawData = fs.readFileSync(filePath, 'utf-8');
    const testCases = JSON.parse(rawData);
    return testCases;
}}
    
describe('mergeJsonRecursive', () => {{
    const testCases = loadTestCases('./{self.idx}/test_cases/test_cases.json');
    
    testCases.forEach((tc, index) => {{
        test(`Case {{index}}`, () => {{
{def_string}
{call_string}

            expect(deepCompare(result, tc.Expected)).toEqual(true);
        }});
    }});
}});

function isClose(a, b, tolerance = 1e-6) {{
    return Math.abs(a - b) <= tolerance;
}}

function deepCompare(a, b, tolerance = 1e-6) {{
    if (typeof a === "number" && typeof b === "number") {{
        return isClose(a, b, tolerance);
    }} else if (Array.isArray(a) && Array.isArray(b)) {{
        if (a.length !== b.length) return false;
        return a.every((ai, index) => deepCompare(ai, b[index], tolerance));
    }} else if (
        a !== null && typeof a === "object" &&
        b !== null && typeof b === "object"
    ) {{
        const aKeys = Object.keys(a);
        const bKeys = Object.keys(b);
        if (aKeys.length !== bKeys.length) return false;
        return aKeys.every(k => k in b && deepCompare(a[k], b[k], tolerance));
    }} else {{
        return a === b;
    }}
}}
"""

    def generate(self):
        blank = " " * 12
        def_string = ""
        args = []
        input_example = self.gt_example["Inputs"]
        sigs = []
        for key, value in input_example.items():
            def_string += blank + f'let {key}_1 = tc.Inputs.{key};\n'
            args.append(f"{key}_1")
            sigs.append(f"{key}")
        call_string = f"{blank}const result = func({', '.join(args)})"
        code = self.build_code(def_string, call_string)
        return GeneratedDriver(code), f"\nexport function {self.func_name}({', '.join(sigs)}) {{ \n    // TODO: Implement\n}}"

class PyGenerator(TestcaseGenerator):
    def __init__(self, func_name: str, gt_example: dict, tested_file_path: str, llm):
        super().__init__(func_name, gt_example, tested_file_path)
        self.llm = llm

    def build_code(self, def_string: str, call_string: str) -> str:
        return f"""from benchmark import {self.func_name} as func
import json
import pytest


def load_test_cases(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


test_cases = load_test_cases('./test.json')

@pytest.mark.parametrize("tc", test_cases)
def test_merge_json_recursive(tc):
{def_string}
{call_string}
    assert result == tc['Expected']
"""

    def generate(self):
        blank = " " * 4
        def_string = ""
        args = []
        input_example = self.gt_example["Inputs"]
        for key, value in input_example.items():
            def_string += blank + f"{key}_1 = tc['Inputs']['{key}']\n"
            args.append(f"{key}_1")

        call_string = f"{blank}result = func({', '.join(args)})"
        code = self.build_code(def_string, call_string)

        return GeneratedDriver(code)

# TS示例调用
# generator: TSGenerator = TSGenerator("add", "/mnt/c/Users/34203/Desktop/code2bench/benchmark/TS", "./test", "/mnt/c/Users/34203/Desktop/code2bench/benchmark/TS/runner.test.ts")
# generator.generate()

# py示例调用
# generator: PyGenerator = PyGenerator("add", "/mnt/c/Users/34203/Desktop/code2bench/benchmark/TS", "./test", "/mnt/c/Users/34203/Desktop/code2bench/benchmark/TS/runner_test.py")
# generator.generate()

class JavaGenerator(TestcaseGenerator):
    def __init__(self, func_name: str, gt_example: dict, tested_file_path: str, llm):
        super().__init__(func_name, gt_example, tested_file_path)
        self.llm = llm

    def generate(self, python_runner: str, testcases_str: str, last_runner=None, error_msg=None):
        system_prompt = JAVA_RUNNER_GENERATOR_PROMPT
        error_prompt = f"""
## Previous Error Information
The previously generated runner code:
{last_runner.driver}

The previously generated runner code resulted in the following error during execution:
{error_msg}

Please analyze the error, correct the runner code, and provide the updated runner code.
""" if last_runner else ""
        system_prompt = system_prompt.replace("{", "{{").replace("}", "}}")
        # system_prompt = system_prompt.replace("benchmark/Java/test_data.json", f"{self.gt_file_dir}/test_data.json")
        # TODO: give the right path
        system_prompt = system_prompt.format(testcases_str=testcases_str)
        user_message = python_runner + error_prompt
        try:
            response = call_llm(self.llm, system_message=system_prompt, user_message=user_message)
            cleaned_response = clean_response_content(response)
            res = json.loads(cleaned_response)
            driver = res["JSONLoader"]
            return GeneratedDriver(driver=driver)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(f"Generating driver failed: {e}")
            return GeneratedDriver(error=str(e))

