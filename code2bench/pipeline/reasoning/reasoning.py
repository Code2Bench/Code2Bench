import json
import os
import re
from typing import Dict, List, Tuple, Union
from code2bench.data_model import FuncType
from code2bench.llm.llm_caller import call_llm
from code2bench.prompt.reasoning_generator import (
    REASONING_RUNNER_GENERATION_PROMPT,
    REASONING_TESTCASE_GENERATION_PROMPT,
    REASONING_CLASSIFICATION_PROMPT,
    WEAKLY_SELF_CONTAINED_REASONING_TESTCASE_GENERATION_PROMPT,
) 
from code2bench.test_runner.dry_run import run_pytest, run_python_driver
from code2bench.utils.json_utils import clean_response_content, get_python_response, load_json, save_json
from code2bench import config, logger, llm_client
from code2bench.utils.python import extract_function_name
from code2bench.utils.file_utils import copy_file


class ReasoningGenerator:
    
    def __init__(self, llm=None):
        self.llm = llm
        
    def route(self, ground_truth: str):
        system_prompt = REASONING_CLASSIFICATION_PROMPT
        
        try:
            response = call_llm(self.llm, system_message=system_prompt, user_message=ground_truth)
            cleaned_response = clean_response_content(response)
            res = json.loads(cleaned_response)
            return res['is_suitable']
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(f"ReasoningGenerator generate failed: {e}")
            # return GeneratedDriver(error=str(e))
            
    def generate_weakly_self_contained_example_usage(self, testcase_generator: str, last_res: str = "", error_msg: str = ""):
        system_prompt = WEAKLY_SELF_CONTAINED_REASONING_TESTCASE_GENERATION_PROMPT
        error_prompt = f"""
## Previous Error Information
The previously generated driver code:
{last_res}

The previously generated code resulted in the following error during execution:
{error_msg}

Please analyze the error, correct the code, and provide the updated code.
""" if last_res else ""
        try:
            response = call_llm(self.llm, system_message=system_prompt, user_message=testcase_generator + error_prompt, clean=False)
            python_code = get_python_response(response)
            return python_code, ""
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(f"ReasoningGenerator generate failed: {e}")
            return None, str(e)
            
    def generate_reasoning_testcases(self, ground_truth: str, inputs_hint: str = "", last_testcases: str = "", error_msg: str = ""):
        system_prompt = REASONING_TESTCASE_GENERATION_PROMPT
        error_prompt = f"""
## Previous Error Information
The previously generated driver code:
{last_testcases}

The previously generated driver code resulted in the following error during execution:
{error_msg}

Please analyze the error, correct the driver code, and provide the updated driver code.
""" if last_testcases else ""
        inputs_hint = f"""
Here are some examples of inputs(may not be exhaustive):
<Inputs>
{inputs_hint}
</Inputs>        
"""
        user_prompt = "<Function>\n" + ground_truth + "\n</Function>\n" + inputs_hint + error_prompt + " Note that examples of inputs may not readable, but you need to generate readable inputs.\n"
        try:
            response = call_llm(self.llm, system_message=system_prompt, user_message=user_prompt)
            cleaned_response = clean_response_content(response)
            try:
                res = json.loads(cleaned_response)
            except json.JSONDecodeError:
                logger.error(f"JSON decode error: {cleaned_response}")
                return None, "JSON decode error"
            return res, None
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(f"ReasoningGenerator generate failed: {e}")
            return None, str(e)
            
    def generate_reasoning_testcases_runner(self, normal_runner: str, last_error: str = "", last_runner: str = ""):
        system_prompt = REASONING_RUNNER_GENERATION_PROMPT
        error_msg = f"""
Last generation error message:
{last_error}

Last generation code:
{last_runner}
Please analyze the error, correct the previous generated code, and provide the updated code.
""" if last_error else ""
        user_message = f"""
<NormalRunner>
{normal_runner}
</NormalRunner>
""" + error_msg
        try:
            response = call_llm(self.llm, system_message=system_prompt, user_message=user_message)
            cleaned_response = clean_response_content(response)
            res = json.loads(cleaned_response)
            return res["Runner"]
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(f"ReasoningGenerator generate failed: {e}")
    
    def execute_prediction(self, function_definition: str, input_str: str, cot_mode=False):
        # 零样本模式Prompt（直接预测）
        system_prompt_zero_shot = """
You are a Python execution simulator. Given a function and inputs, predict ONLY the output in strict JSON format.
Follow these rules ABSOLUTELY:

1. OUTPUT FORMAT (MUST be valid JSON):
{
    "output": <EXACT_OUTPUT> or "Error"
}

2. RULES:
- SUCCESS: Return the exact Python object if execution succeeds
  - List: Return full list (e.g., ["apple", "banana"])
  - Dict: Return full dict (e.g., {"key": "value"})
  - Tuple: Return full tuple (e.g., (1, 2))
  - Primitive: Return as-is (e.g., 42, "hello", True)
- FAILURE: Return "Error" (exact string) for ANY exception including:
  * Invalid inputs
  * Type errors
  * Infinite loops
  * Runtime exceptions
  * Syntax errors
  * Timeouts

3. PROHIBITED:
- No tracebacks/error details
- No explanations/comments
- No partial outputs
- No JSON formatting errors

4. EXAMPLES:
Correct Output: {"output": [1, 2, 3]}
Error Output: {"output": "Error"}

5. Note:
- Only return json with "output" key.
"""

        # 思维链模式Prompt（分步推理）
        system_prompt_cot = """
You are a Python code analyzer. Given a function and inputs, predict ONLY the output in strict JSON format following COT (Chain-of-Thought) analysis.

1. OUTPUT FORMAT (MUST be valid JSON):
{
    "output": <EXACT_OUTPUT> or "Error"
}

2. EXECUTION STEPS (INTERNAL REASONING):
1. Parameter Analysis: Check input types and required parameters
2. Logic Simulation: Trace possible execution paths
3. Validation:
   - Success Path: Verify return value computable
   - Error Paths: Identify all possible exceptions
4. Decision: Finalize output or error

3. RULES:
- SUCCESS: Return exact Python object
  - Collections: Full structure (lists/dicts/tuples)
  - Primitives: Raw values (int/str/bool/etc)
- FAILURE: Return "Error" (exact string) for:
  * TypeError/ValueError/AttributeError
  * Syntax errors (even if not executed)
  * Recursion/Timeout possibilities
  * Any undefined behavior

4. OUTPUT CONSTRAINTS:
- JSON must contain ONLY "output" key
- No error details/tracebacks
- No explanatory text
- No partial outputs
- No metadata (e.g., execution time)

5. EXAMPLES:
Correct COT Process:
Input: def get_len(x): return len(x)
Inputs: {"x": "abc"}
Thought: 1. Valid str input → 2. len() computable → 3. No error paths
Output: {"output": 3}

Error COT Process:
Input: def sqrt(x): return x**0.5
Inputs: {"x": -1}
Thought: 1. Valid input → 2. Math error possible → 3. ValueError expected
Output: {"output": "Error"}
"""

        user_prompt = f"""
<Function>
{function_definition}
</Function>

<Input>
{input_str}
</Input>

Return ONLY:
- The exact output object if successful, OR
- The string "Error" if any error occurs
    """

        try:
            # 根据配置选择Prompt模式
            system_prompt = system_prompt_cot if cot_mode else system_prompt_zero_shot
            
            response = call_llm(
                self.llm,
                system_message=system_prompt,
                user_message=user_prompt,
            )
            cleaned = clean_response_content(response)
                
            # # 尝试解析为Python字面量
            # try:
            #     return eval(cleaned) if cleaned else "Error"
            # except:
            #     return "Error"
            
            parsed = json.loads(cleaned)
            return parsed.get("output", "Error")          
        except Exception:
            return "Error"
        
    def run_once_execute_prediction(self, ground_truth_path: str, test_cases_path: str):
        # read ground truth
        with open(ground_truth_path, "r") as f:
            function_definition = f.read()

        test_cases = load_json(test_cases_path)
        if test_cases is None:
            return False
        
        res = []
        for case in test_cases:
            inputs = case["Inputs"]
            expected = case["Expected"]
            llm_answer = self.execute_prediction(function_definition, inputs)
            res.append({
                "Inputs": inputs,
                "Expected": expected,
                "Actual": llm_answer,
                "IsCorrect": llm_answer == expected
            })
            
        return res
        
def batch_execute_prediction():
    pass
    
    
def route_driver(ground_truth: str, llm):
    driver_router = ReasoningGenerator(llm=llm)
    return driver_router.route(ground_truth)

def batch_route_driver():
    index_dict: Dict[str, List[str]] = {
        "success": [],
        "failed": []
    }
    reasoning_index_path = config.BENCMARK_REASONING_INDEX_PATH
    if os.path.exists(reasoning_index_path):
        index_dict = load_json(reasoning_index_path)

    cnt = 0
    for idx in sorted(os.listdir(config.BENCHMARK_PATH)):
        if idx in index_dict["success"] or idx in index_dict["failed"]:
            continue
        
        ground_truth = os.path.join(config.BENCHMARK_PATH, idx, "groundtruth.py")
        with open(ground_truth, "r") as f:
            ground_truth = f.read()
        
        logger.info(f"Processing {idx}")
        status = route_driver(ground_truth=ground_truth, llm=llm_client)
        if status:
            index_dict["success"].append(idx)
        else:
            index_dict["failed"].append(idx)
            
        # cnt += 1
        # if cnt == 10:
        #     break
        
        save_json(reasoning_index_path, index_dict)
        
def generate_weakly_example_usage(idx: str, llm) -> Tuple[Union[bool, List[Dict]], str]:
    assert config.MODE == FuncType.WEAKLY_SELF_CONTAINED, "Only support WEAKLY_SELF_CONTAINED mode in generate_weakly_example_usage"
    ground_truth_path = os.path.join(config.BENCHMARK_PATH, idx, "groundtruth.py")
    with open(ground_truth_path, "r") as f:
        ground_truth = f.read()
    
    func_name = extract_function_name(ground_truth)
    if func_name is None:
        raise ValueError(f"Function name not found in {ground_truth_path}")

    with open(ground_truth_path.replace("groundtruth.py", "testcase_generator.py"), "r") as f:
        testcase_generator = f.read()
    
    example_usage_generator_path = ground_truth_path.replace("groundtruth.py", "example_usages.py")
    
    generator = ReasoningGenerator(llm=llm)
    cnt = 0
    max_retries = 3
    last_error = None
    last_testcases = None
    while cnt < max_retries:
        example_usage_generator, last_error = generator.generate_weakly_self_contained_example_usage(testcase_generator, last_res=last_testcases, error_msg=last_error)
        
        cnt += 1
        if last_error:
            logger.error(f"Generate reasoning testcases failed: {last_error}")    
            last_testcases = example_usage_generator
            continue
        
        with open(example_usage_generator_path, "w") as f:
            f.write(example_usage_generator)
        
        try:
            run_pytest(driver_path=example_usage_generator_path)
            example_usage_path = os.path.join(config.BENCHMARK_PATH, idx, "test_cases/example_usages.json")    
            testcases = load_json(example_usage_path)
            normal_cases = testcases.get("Normal cases", [])
            if not normal_cases:
                logger.error(f"Generate reasoning testcases failed, no `Normal cases` found: {testcases}")
                last_error = f"Generate reasoning testcases failed, no `Normal cases` found"
                cnt += 1
                continue
            break
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(f"Run reasoning runner failed: {e}")
            last_error = str(e)
    
    if last_error:
        logger.error(f"Generate reasoning testcases failed: {last_error}")
        return False, last_error

    all_testcases = {
        "Test cases": []
    }
    all_testcases["Test cases"].extend(testcases.get("Normal cases", []))
    all_testcases["Test cases"].extend(testcases.get("Others", []))
    reasoning_testcases_path = ground_truth_path.replace("groundtruth.py", "test_cases/reasoning_testcases.json")
    if not os.path.exists(os.path.dirname(reasoning_testcases_path)):
        os.makedirs(os.path.dirname(reasoning_testcases_path))
    save_json(file_path=reasoning_testcases_path, data=all_testcases)
    logger.info(f"Save reasoning testcases to {reasoning_testcases_path}")
    return testcases["Normal cases"], ""
        
def generate_reasoning_testcases(idx: str, llm) -> Tuple[Union[bool, List[Dict]], str]:
    ground_truth_path = os.path.join(config.BENCHMARK_PATH, idx, "groundtruth.py")
    with open(ground_truth_path, "r") as f:
        ground_truth = f.read()
    
    func_name = extract_function_name(ground_truth)
    if func_name is None:
        raise ValueError(f"Function name not found in {ground_truth_path}")

    driver_testcases = load_json(ground_truth_path.replace("groundtruth.py", f"test_cases/test_cases.json"))
    driver_testcases = driver_testcases[:10]
    driver_testcases = json.dumps(driver_testcases)
    
    generator = ReasoningGenerator(llm=llm)
    cnt = 0
    max_retries = 3
    last_error = None
    last_testcases = None
    while cnt < max_retries:
        testcases, last_error = generator.generate_reasoning_testcases(ground_truth, inputs_hint=driver_testcases, last_testcases=last_testcases, error_msg=last_error)
        
        if last_error:
            logger.error(f"Generate reasoning testcases failed: {last_error}")
            cnt += 1
            continue
        
        if "Normal cases" not in testcases:
            logger.error(f"Generate reasoning testcases failed, no `Normal cases` found: {testcases}")
            last_error = f"Generate reasoning testcases failed, no `Normal cases` found"
            cnt += 1
            continue

        if testcases:
            break
    
    if last_error:
        logger.error(f"Generate reasoning testcases failed: {last_error}")
        return False, last_error
    
    ground_truth_path = ground_truth_path.replace("Python", "reasoning")
    example_usage_path = ground_truth_path.replace("groundtruth.py", "test_cases/example_usages.json")
    if not os.path.exists(os.path.dirname(example_usage_path)):
        os.makedirs(os.path.dirname(example_usage_path))        
    save_json(file_path=example_usage_path, data=testcases)
    logger.info(f"Save example usage to {example_usage_path}")
    
    status, reason = generate_reasoning_testcases_outputs(idx=idx, func_name=func_name)
    if not status:
        logger.error(f"Generate reasoning testcases outputs failed: {reason}")
        return False, reason
    # 生成的测试用例可能包含 Normal cases 和 Edge cases
    # 这里将它们合并成一个列表
    testcases = load_json(example_usage_path)

    all_testcases = {
        "Test cases": []
    }
    all_testcases["Test cases"].extend(testcases["Normal cases"])
    all_testcases["Test cases"].extend(testcases.get("Others", []))
    reasoning_testcases_path = ground_truth_path.replace("groundtruth.py", "test_cases/reasoning_testcases.json")
    if not os.path.exists(os.path.dirname(reasoning_testcases_path)):
        os.makedirs(os.path.dirname(reasoning_testcases_path))
    save_json(file_path=reasoning_testcases_path, data=all_testcases)
    logger.info(f"Save reasoning testcases to {reasoning_testcases_path}")
    return testcases["Normal cases"], ""

def batch_generate_reasoning_testcases():
    pass

def generate_reasoning_testcases_outputs(idx: str, func_name: str) -> Tuple[bool, str]:
    """Use the previous generated runner to get the output of the reasoning testcases"""
    # copy the runner.py as "reasoning_runner.py"
    reasoning_dir = os.path.join(config.BENCHMARK_PATH, idx).replace("Python", "reasoning")
    src = os.path.join(config.BENCHMARK_PATH, idx, "runner.py")
    reasoning_runner_path = os.path.join(reasoning_dir, "reasoning_runner.py")
    
    if not os.path.exists(os.path.dirname(reasoning_runner_path)):
        os.makedirs(os.path.dirname(reasoning_runner_path))

    # if not copy_file(src=src, dst=reasoning_runner_path):
    #     logger.error(f"Copy file failed: {src} -> {reasoning_runner_path}")
    #     return False, f"Copy file failed: {src} -> {reasoning_runner_path}"
    # logger.info(f"Copy file {src} -> {reasoning_runner_path}")
    
    src = os.path.join(config.BENCHMARK_PATH, idx, "groundtruth.py")
    dst = os.path.join(reasoning_dir, "groundtruth.py")
    if not copy_file(src=src, dst=dst):
        logger.error(f"Copy file failed: {src} -> {dst}")
        return False, f"Copy file failed: {src} -> {dst}"
    logger.info(f"Copy file {src} -> {dst}")
    
    # modify it to support the reasoning testcases
    with open(config.REASONING_RUNNER_TEMPLATE_PATH, "r") as f:
        runner_template = f.read()

    runner_template = runner_template.replace("fast_format_html", func_name)
    with open(reasoning_runner_path, "w") as f:
        f.write(runner_template)
    
    try:
        run_python_driver(driver_path=reasoning_runner_path)
        return True, ""
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.exception(f"Run reasoning runner failed: {e}")
        return False, str(e)
    
    
    # # 把driver文件中的"from tested"改成"from ground_truth"
    # runner = runner.replace("from tested", "from groundtruth")
    # runner = re.sub(r"(test_cases)/[^/\"']+", r"\1", runner)
    
    # # generate the reasoning_runner.py
    # generator = ReasoningGenerator(llm=llm_client)
    
    # cnt = 0
    # max_retries = 3
    # last_error = ""
    # last_runner = ""
    # while cnt < max_retries:
    #     reasoning_runner = generator.generate_reasoning_testcases_runner(runner, last_error, last_error=last_error, last_runner=last_runner)
    #     reasoning_runner = reasoning_runner.replace("test_cases.json", "reasoning_testcases.json") # replace the test_cases.json to reasoning_testcases.json because the llm may not generate the correct path
    #     with open(reasoning_runner_path, "w") as f:
    #         f.write(reasoning_runner)
    #     logger.info(f"Write reasoning runner to {reasoning_runner_path}")
        
    #     last_runner = reasoning_runner
    #     # run the reasoning_runner.py
    #     error_type, error_msg = run_python_driver(driver_path=reasoning_runner_path)
    #     if error_msg:
    #         logger.error(f"Run reasoning runner failed: {error_type} - {error_msg}")
    #         last_error = error_msg
    #     else:
    #         logger.info(f"Run reasoning runner success")
    #         # 运行成功，退出循环
    #         break
    #     cnt += 1
    
    # if last_error:
    #     logger.error(f"Generate reasoning testcases outputs failed: {last_error}")
    #     return False, last_error
    # return True, ""


if __name__ == "__main__":
    
    config.BENCHMARK_NAME = "Python"
    generate_reasoning_testcases(idx="1", llm=llm_client)
    # generate_reasoning_testcases_outputs(idx="1")