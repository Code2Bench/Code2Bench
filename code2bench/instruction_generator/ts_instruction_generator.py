
from datetime import datetime
import json
import os

import shutil
from typing import Dict, List
from code2bench.llm.llm_caller import call_llm
from code2bench.prompt.instruction_generator import TS_INSTRUCTION_GENERATOR_PROMPT
from code2bench.utils.ts import replace_ts_function_name
from code2bench.utils.json_utils import clean_response_content, save_json
from code2bench import llm_client, logger
from code2bench.config import config
from code2bench.utils.python import extract_function_name


class TSInstructionGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate_instruction(self, groundtruth: str, inputs_outputs: str, last_res: str=None, error_msg: str=None):
        system_prompt = TS_INSTRUCTION_GENERATOR_PROMPT
        error_msg = f"""
Last generation error message:
{last_res}

Last generation code:
{error_msg}
You can use this information to improve the generated code.
""" if last_res else ""

        user_message = f"""
<Python Function>
{groundtruth}
</Python Function>
<Inputs_Outputs>
{inputs_outputs}
</Inputs_Outputs>
"""
        user_message = user_message + error_msg
        try:
            response = call_llm(self.llm, system_message=system_prompt, user_message=user_message)
            cleaned_response = clean_response_content(response)
            try:
                res = json.loads(cleaned_response)
                # function = res.get("Function")
                # instruction = res.get("Instruction")
                # examples = res.get("Examples")
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON response: {cleaned_response}")
                return None, "JSON decode error"
            return res, None
        except Exception as e:
            print(f"Error generating instruction: {e}")
            return None, str(e)
        
def generate_instruction_for_ts(idx: str):

    groundtruth_path = os.path.join(config.BENCHMARK_PATH.replace("TS", "default"), idx, "groundtruth.py")
    with open(groundtruth_path, "r") as f:
        groundtruth = f.read()
        
    # python_instrution_path = os.path.join(config.BENCHMARK_PATH.replace("Go", "default"), idx, "instruction.txt")
    # with open(python_instrution_path, "r") as f:
    #     python_instrution = f.read()
        
    func_name = extract_function_name(groundtruth)

    # TODO: get inputs and outputs from the test cases
    # reasoning_testcases_path = os.path.join(config.BENCHMARK_PATH.replace("default", "reasoning"), idx, "test_cases", "reasoning_testcases.json")
    # if not os.path.exists(reasoning_testcases_path):
    #     print(f"Reasoning test cases file not found: {reasoning_testcases_path}")
    #     return False
    # with open(reasoning_testcases_path, "r") as f:
    #     inputs_outputs = f.read()
        
    inputs_outputs = ""
    
    # inputs_outputs = os.path.join(config.BENCHMARK_PATH.replace("Go", "default"), idx, "test_cases", "test_cases.json")
    # if not os.path.exists(inputs_outputs):
    #     print(f"Reasoning test cases file not found: {inputs_outputs}")
    #     return False

    generator = TSInstructionGenerator(llm_client)
    
    cnt = 0
    max_retries = 5
    last_error = None
    last_res = None
    success = False
    while cnt < max_retries:
        cnt += 1
        if last_error:
            res, last_error = generator.generate_instruction(groundtruth, inputs_outputs, last_res=last_res, error_msg=last_error)
        else:
            res, last_error = generator.generate_instruction(groundtruth, inputs_outputs)
        
        if res:
            function = res.get("Function") or ""
            ts_func_name = res.get("Function Name") or ""
            instruction = res.get("Instruction")
            examples: List[Dict] = res.get("Examples")
            
            # 这里还是不好控制。。还是修改runner文件？
            if func_name not in function:
                logger.error(f"Function name mismatch: {func_name} not found in generated function.")
                function = replace_ts_function_name(function, func_name)
                # last_error = "Function name mismatch, you need to change the function name as {func_name}."
                # continue
            if func_name not in instruction:
                pass
            
            if function and instruction and examples:
                success = True
                break
        else:
            logger.error(f"Error generating instruction: {last_error}")
            last_res = res
    
    if not success:
        logger.error(f"Failed to generate Go instruction for {idx} after {max_retries} attempts.")
        return False
    
    # Save the generated funtion to 'tested.ts'
    ts_benchmark_path = config.BENCHMARK_PATH.replace("default", "TS")
    tested_go_path = os.path.join(ts_benchmark_path, idx, "tested.ts")
    if not os.path.exists(os.path.dirname(tested_go_path)):
        os.makedirs(os.path.dirname(tested_go_path))
    with open(tested_go_path, "w") as f:
        f.write(function)
        
    # Save the metainfo
    metainfo_path = os.path.join(ts_benchmark_path, idx, "metainfo.json")
    python_metainfo_path = os.path.join(config.BENCHMARK_PATH.replace("TS", "default"), idx, "metainfo.json")
    if not os.path.exists(python_metainfo_path):
        raise FileNotFoundError(f"Failed to find metainfo file for function {idx}. You need to generate it first.")
    with open(python_metainfo_path, "r") as f:
        metainfo = json.load(f)
    metainfo["original_func_name"] = metainfo.get("func_name", func_name)
    metainfo["func_name"] = ts_func_name if ts_func_name != "" else func_name
    metainfo["created_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_json(metainfo_path, metainfo)

    # Save the generated instruction to 'instruction.txt'
    instruction_path = os.path.join(ts_benchmark_path, idx, "instruction.txt")
    content = instruction + "\n\n### Examples:\n" + "\n".join(
        [f"#### {example['Description']}\nInput: {json.dumps(example['Input'], indent=2, ensure_ascii=False)}\nOutput: {json.dumps(example['Output'], indent=2, ensure_ascii=False)}" for example in examples]
    )
    with open(instruction_path, "w") as f:
        f.write(content)
        
    # Copy the testcases
    testcases_path = os.path.join(ts_benchmark_path, idx, "test_cases", "test_cases.json")
    if not os.path.exists(os.path.dirname(testcases_path)):
        os.makedirs(os.path.dirname(testcases_path))
    python_testcases_path = os.path.join(config.BENCHMARK_PATH.replace("TS", "default"), idx, "test_cases", "test_cases.json")
    if not os.path.exists(python_testcases_path):
        raise FileNotFoundError(f"Failed to find testcases file for function {idx}. You need to generate it first.")
    shutil.copyfile(python_testcases_path, testcases_path)
    return True


if __name__ == "__main__":
    # Example usage
    idx = "1"  # Replace with the actual index you want to process
    generate_instruction_for_ts(idx)