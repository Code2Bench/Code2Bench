from datetime import datetime
import json
import re
from pathlib import Path
from typing import Tuple

from code2bench import config, logger
from code2bench.llm.llm_caller import call_llm
from code2bench.data_model import FuncToGenerate, FuncType, GeneratedInstruction
from code2bench.prompt.groundtruth_filter import DIFFICULTY_ASSESSMENT_PROMPT, WEAKLY_SELF_CONTAINED_DIFFICULTY_ASSESSMENT_PROMPT
from code2bench.prompt.instruction_generator import LEVEL_SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT, SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT, WEAKLY_SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT
from code2bench.utils.json_utils import clean_response_content, load_json
from code2bench.utils.python import add_docstring_to_signature
from code2bench import llm_client


class InstructionGenerator:
    def __init__(self, llm):
        self.llm = llm
        
    def assess_difficulty(self, func: FuncToGenerate) -> str:
        if func.func_type == FuncType.SELF_CONTAINED:
            system_prompt = DIFFICULTY_ASSESSMENT_PROMPT
        elif func.func_type == FuncType.WEAKLY_SELF_CONTAINED:
            system_prompt = WEAKLY_SELF_CONTAINED_DIFFICULTY_ASSESSMENT_PROMPT
        else:
            raise ValueError(f"Unsupported function type: {func.func_type} in assess_difficulty")
        user_message = func.original_str
        try:
            response = call_llm(self.llm, system_message=system_prompt, user_message=user_message)
            cleaned_response = clean_response_content(response)
            res = json.loads(cleaned_response)
            difficulty = res.get("Difficulty")

            assert difficulty in ["Easy", "Medium", "Hard"]
            return difficulty
        except Exception as e:
            logger.exception(f"Error generating instruction: {e}")
            return str(e)

    def generate_instruction(self, func: FuncToGenerate, last_res, last_error, example_usages) -> Tuple[GeneratedInstruction, str]:
        if func.func_type == FuncType.SELF_CONTAINED:
            return self.generate_self_contained_instruction(func, last_res=last_res, last_error=last_error, example_usages=example_usages)
        elif func.func_type == FuncType.WEAKLY_SELF_CONTAINED:
            return self.generate_self_contained_instruction(func, last_res=last_res, last_error=last_error)
        # elif func.func_type == FuncType.LEVEL_SELF_CONTAINED:
        #     return self.generate_level_self_contained_instruction(func)
        else:
            raise ValueError("Unsupported function type")
    
    def generate_self_contained_instruction(self, func: FuncToGenerate, last_res=None, last_error=None, example_usages: str=None) -> Tuple[GeneratedInstruction, str]:
        level0_prompt = SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT

        level1_prompt = LEVEL_SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT  
        
        weakly_self_contained_prompt = WEAKLY_SELF_CONTAINED_INSTRUCTION_GENERATOR_PROMPT
        
        error_prompt = (
            f"Please check the last result: {last_res} and provide a suitable answer. "
            f"Error response: {last_error}."
        ) if last_res and last_error else ""

        try:
            if func.func_type == FuncType.SELF_CONTAINED:
                prompt = level0_prompt
                # user_message = func.original_str
                user_message = f"""
<function>
{func.original_str}
</function>
<example usages>
{example_usages}
</example usages>
"""
            elif func.func_type == FuncType.LEVEL_SELF_CONTAINED:
                prompt = level1_prompt
                user_message = f"""
<function A>
{func.original_str}
</function A>
<function B>
{func.contains[0].original_str}
</function B>
"""
            elif func.func_type == FuncType.WEAKLY_SELF_CONTAINED:
                prompt = weakly_self_contained_prompt
                user_message = f"""
<function>
{func.original_str}
</function>
Function Calls lib: {','.join(func.call_libs)}.   
"""
            
            user_message = user_message + error_prompt
            response = call_llm(self.llm, system_message=prompt, user_message=user_message)
            if func.func_type == FuncType.SELF_CONTAINED:
                docstring, python_signature = self.parse_docstring_and_signature(response=response)
                return GeneratedInstruction(instruction=docstring), python_signature
            elif func.func_type == FuncType.WEAKLY_SELF_CONTAINED:
                docstring, python_signature = self.parse_docstring_and_signature(response=response)

                # instruction, python_signature = self.parse_llm_response(response)
                
            # cleaned_response = clean_response_content(response)
            # cleaned_response = cleaned_response.replace(r'\n', r'\\n').replace(r'\t', r'\\t')
            # res = json.loads(cleaned_response)
            # instruction = res.get("Instruction")
            # python_signature = res.get("Python Signature")
            # if reason:
            #     return GeneratedInstruction(reason=reason)
            # difficulty = res.get("Difficulty")
            # assert difficulty in ["Easy", "Medium", "Hard"]
                return GeneratedInstruction(instruction=docstring), python_signature
            else:
                raise ValueError("Invalid response format. Missing instruction or signature tags.")
        except Exception as e:
            logger.exception(f"Error generating instruction: {e}")
            return GeneratedInstruction(error=str(e)), ""
        
    def parse_docstring_and_signature(self, response: str):
        """
        Parses the LLM response to extract the docstring and Python Signature parts.

        LLM response format:
        <docstring>
        The docstring
        </docstring>
        <signature>
        ```python
        def function_name():
            # Your code here
        ```
        </signature>

        Returns:
        - docstring: The extracted docstring text.
        - python_signature: The extracted Python function signature without the ```python markers.
        """
        def clean_code_block(block: str) -> str:
            """Removes ```python markers from the code block."""
            if block.startswith("```python"):
                block = block[len("```python"):].strip()
            if block.endswith("```"):
                block = block[:-len("```")].strip()
            return block

        # Extract docstring and signature parts
        docstring_start = response.find("<docstring>") + len("<docstring>")
        docstring_end = response.find("</docstring>")
        signature_start = response.find("<signature>") + len("<signature>")
        signature_end = response.find("</signature>")

        # Validate the response format
        if docstring_start == -1 or docstring_end == -1 or signature_start == -1 or signature_end == -1:
            raise ValueError("Invalid response format. Missing docstring or signature tags.")

        # Extract and clean the docstring and signature
        docstring = response[docstring_start:docstring_end].strip()
        python_signature = response[signature_start:signature_end].strip()

        # Remove ```python markers from the signature
        python_signature = clean_code_block(python_signature)

        return docstring, python_signature
    
    def parse_llm_response(self, response: str):
        """
        Parses the LLM response to extract the Instruction and Python Signature parts.

        LLM response format:
        <instruction>
        The instruction
        </instruction>
        <signature>
        ```python
        def function_name():
            # Your code here
        ```
        </signature>

        Returns:
        - instruction: The extracted instruction text.
        - python_signature: The extracted Python function signature without the ```python markers.
        """
        def clean_code_block(block: str) -> str:
            """Removes ```python markers from the code block."""
            if block.startswith("```python"):
                block = block[len("```python"):].strip()
            if block.endswith("```"):
                block = block[:-len("```")].strip()
            return block

        # Extract instruction and signature parts
        instruction_start = response.find("<instruction>") + len("<instruction>")
        instruction_end = response.find("</instruction>")
        signature_start = response.find("<signature>") + len("<signature>")
        signature_end = response.find("</signature>")

        # Validate the response format
        if instruction_start == -1 or instruction_end == -1 or signature_start == -1 or signature_end == -1:
            raise ValueError("Invalid response format. Missing instruction or signature tags.")

        # Extract and clean the instruction and signature
        instruction = response[instruction_start:instruction_end].strip()
        python_signature = response[signature_start:signature_end].strip()

        # Remove ```python markers from the signature
        python_signature = clean_code_block(python_signature)

        return instruction, python_signature
        

    def generate_weakly_self_contained_instruction(self, func: FuncToGenerate) -> Tuple[str, str]:
        pass

    def judge_input_output(self, func: FuncToGenerate):
        """
        判断输入和输出是不是基本类型，基本类型比较容易搞定，输入和输出不需要考虑项目相关的context，因为基本类型是通用的：
        Self-contained function: (Cyclomatic Complexity: 5)
        ['vllm.model_executor.model_loader.openvino._flattenize_inputs']
        def _flattenize_inputs(inputs):
            # Helper function for making nested inputs flattens
            flatten_inputs = []
            for input_data in inputs:
                if input_data is None:
                    continue
                if isinstance(input_data, (list, tuple)):
                    flatten_inputs.extend(_flattenize_inputs(input_data))
                elif isinstance(input_data, dict):
                    flatten_inputs.extend(_flattenize_inputs(list(
                        input_data.values())))
                else:
                    flatten_inputs.append(input_data)
            return flatten_inputs
        
        但是，如果不是基本类型的话，就需要考虑context了，比如下面这个例子：
        Self-contained function: (Cyclomatic Complexity: 1)
        ['tests.core.utils.get_sequence_groups']
        def get_sequence_groups(scheduler_output):
            return [s.seq_group for s in scheduler_output.scheduled_seq_groups]
        出题的时候要把会用到的自定义类型的方法或者属性也补充进去呀！这是context of parameter
        """
        pass

def generate_one_instruction(func: FuncToGenerate, llm, last_res, last_error, example_usages: str) -> Tuple[GeneratedInstruction, str]:
    ig = InstructionGenerator(llm)
    return ig.generate_instruction(func, last_res=last_res, last_error=last_error, example_usages=example_usages)

def assess_difficulty(func: FuncToGenerate, llm) -> str:
    ig = InstructionGenerator(llm)
    return ig.assess_difficulty(func)

def generate_instruction_with_retry(idx, func: FuncToGenerate, llm_client, max_retries=3, example_usages: str=None) -> Tuple[bool, str, str, str]:
    """
    Generate an instruction for a function with retry logic.
    
    Args:
        idx (str): Index of the function
        func (FuncToGenerate): Function to generate instruction for
        llm_client: LLM client to use for generation
        max_retries (int): Maximum number of retries
        
    Returns:
        tuple: (success, message, instruction, python_signature)
    """
    assert config.PROJECT_NAME in ("Python", "weakly"), "Your project is not Python, please check your project name in config.py"
    
    retry_count = 0
    last_error = None
    last_res = None
    
    while retry_count < max_retries:
        # Generate instruction with previous results/errors
        generated_instruction, python_signature = generate_one_instruction(func, llm_client, last_res=last_res, last_error=last_error, example_usages=example_usages)
        if generated_instruction.error:
            logger.info(f"Failed to generate instruction for function {idx}: {func.name} Due to error: {generated_instruction.error}")
            last_error = generated_instruction.error
        last_res = generated_instruction.instruction
        if generated_instruction.instruction:
            break
        retry_count += 1
    
    instruction = generated_instruction.instruction
    if not instruction:
        return False, "Failed to generate instruction" + "###" + (generated_instruction.error or ""), None, None
    
    if func.func_type == FuncType.SELF_CONTAINED:
        # Write pure instruction first
        pure_instruction_path = Path(config.BENCHMARK_PATH) / idx / "pure_instruction.txt"
        with open(pure_instruction_path, "w", encoding="utf-8") as f:
            f.write(instruction)
        python_instruction = add_docstring_to_signature(docstring=instruction, signature=python_signature)
    elif func.func_type == FuncType.WEAKLY_SELF_CONTAINED:
        python_instruction = add_docstring_to_signature(docstring=instruction, signature=python_signature)
    

    # Write python instruction to file
    instruction_path = Path(config.BENCHMARK_PATH) / idx / "instruction.txt"
    # python_instruction = (
    #     f"{instruction}\n"
    #     f"You should write code starting with:\n{python_signature}\n\n"
    # )
    with open(instruction_path, "w", encoding="utf-8") as f:
        f.write(python_instruction)

    logger.info(f"Generated instruction for function {idx}.")
    
    return True, "", instruction, python_signature

def batch_generate_instruction():
    """
    批量生成指令。
    
    遍历Python基准目录下的所有数字命名文件夹，
    读取每个文件夹中的groundtruth.py文件和example_usages.json文件，
    然后调用generate_instruction_with_retry生成指令。
    
    结果会被记录到一个日志文件中。
    """
    assert config.PROJECT_NAME in ("Python", "weakly"), "Your PROJECT_NAME is not Python, please check your project name in config.py"
    
    base_path = Path(config.BENCHMARK_PATH)
    
    # 创建日志文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = Path(config.CURRENT_PROJECT_PATH) / Path(f"instruction_generation_{timestamp}.txt")
    log_file.parent.mkdir(exist_ok=True, parents=True)
    
    # 记录开始时间
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(f"Instruction Generation Log - Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
    
    # 统计信息
    total_folders = 0
    success_count = 0
    fail_count = 0
    success_list = []
    fail_list = []
    
    # 获取所有数字命名的文件夹
    folders = [f for f in base_path.iterdir() if f.is_dir() and f.name.isdigit()]
    folders.sort(key=lambda x: int(x.name))  # 按数字顺序排序
    
    logger.info(f"Found {len(folders)} numeric folders to process")
    
    # 更新日志文件
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"Found {len(folders)} numeric folders to process\n\n")
    
    for folder in folders:
        idx = folder.name
        total_folders += 1
        logger.info(f"Processing folder {idx} ({total_folders}/{len(folders)})")
        
        # 读取 groundtruth.py 文件
        groundtruth_path = folder / "groundtruth.py"
        if not groundtruth_path.exists():
            error_msg = f"No groundtruth.py found in folder {idx}, skipping."
            logger.warning(error_msg)
            fail_count += 1
            fail_list.append((idx, error_msg))
            
            # 更新日志文件
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[FAIL] Folder {idx}: {error_msg}\n")
            
            continue
        
        with open(groundtruth_path, 'r', encoding='utf-8') as f:
            groundtruth_content = f.read()
        
        # 提取函数定义（假设每个groundtruth.py只包含一个函数）
        func_match = re.search(r'def\s+(\w+)', groundtruth_content)
        if not func_match:
            error_msg = f"Could not find function definition in {groundtruth_path}, skipping."
            logger.warning(error_msg)
            fail_count += 1
            fail_list.append((idx, error_msg))
            
            # 更新日志文件
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[FAIL] Folder {idx}: {error_msg}\n")
            
            continue
        
        func_name = func_match.group(1)
        
        # 读取example_usages.json文件
        example_usages_path = folder / "test_cases" / "example_usages.json"
        example_usages_str = None
        
        if example_usages_path.exists():
            try:
                with open(example_usages_path, 'r', encoding='utf-8') as f:
                    example_usages_data = json.load(f)
                
                # 提取Normal cases部分
                normal_cases = example_usages_data.get('Normal cases', [])
                if normal_cases:
                    example_usages_str = json.dumps(normal_cases, indent=2)
                    logger.info(f"Loaded {len(normal_cases)} normal cases from {example_usages_path}")
            except Exception as e:
                warning_msg = f"Error reading or parsing {example_usages_path}: {e}"
                logger.warning(warning_msg)
                
                # 更新日志文件
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[WARNING] Folder {idx}: {warning_msg}\n")
        
        if config.MODE == FuncType.SELF_CONTAINED:
            # 构造函数对象
            func = FuncToGenerate(
                name=func_name,
                original_str=groundtruth_content,
                func_type=FuncType.SELF_CONTAINED
            )
        elif config.MODE == FuncType.WEAKLY_SELF_CONTAINED:
            metainfo_path = folder / "metainfo.json"
            metainfo = load_json(metainfo_path)
            # 构造函数对象
            func = FuncToGenerate(
                name=func_name,
                original_str=groundtruth_content,
                func_type=FuncType.WEAKLY_SELF_CONTAINED,
                call_libs=metainfo['call_libs']  # 示例调用的库
            )
        
        # 调用生成函数
        try:
            success, message, instruction, signature = generate_instruction_with_retry(
                idx=idx,
                func=func,
                llm_client=llm_client,
                example_usages=example_usages_str
            )
            
            if success:
                success_msg = f"Successfully generated instruction for function {func_name}"
                logger.info(success_msg)
                success_count += 1
                success_list.append(idx)
                
                # 更新日志文件
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[SUCCESS] Folder {idx}: Generated instruction for function '{func_name}'\n")
            else:
                error_msg = f"Failed to generate instruction: {message}"
                logger.warning(error_msg)
                fail_count += 1
                fail_list.append((idx, error_msg))
                
                # 更新日志文件
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(f"[FAIL] Folder {idx}: {error_msg}\n")
                
        except Exception as e:
            error_msg = f"Exception while generating instruction: {e}"
            logger.exception(error_msg)
            fail_count += 1
            fail_list.append((idx, error_msg))
            
            # 更新日志文件
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[ERROR] Folder {idx}: {error_msg}\n")
    
    # 记录总结信息
    summary = f"Batch generation complete. Processed {total_folders} folders. Success: {success_count}, Failed: {fail_count}"
    logger.info(summary)
    
    # # 更新日志文件
    # with open(log_file, 'a', encoding='utf-8') as f:
    #     f.write("\n" + "=" * 80 + "\n")
    #     f.write(f"SUMMARY - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    #     f.write("-" * 80 + "\n")
    #     f.write(f"Total folders processed: {total_folders}\n")
    #     f.write(f"Successful generations: {success_count}\n")
    #     f.write(f"Failed generations: {fail_count}\n\n")
        
    #     f.write("Successful folders:\n")
    #     for idx in success_list:
    #         f.write(f"- {idx}\n")
        
    #     f.write("\nFailed folders:\n")
    #     for idx, reason in fail_list:
    #         f.write(f"- {idx}: {reason}\n")
    
    # logger.info(f"Log saved to: {log_file}")
    return success_count, fail_count, total_folders


if __name__ == '__main__':
#     from autocodebench import llm_client
#     ig = InstructionGenerator(llm_client)
#     func = FuncToGenerate(original_str="""
# def _flattenize_inputs(inputs):
#     # Helper function for making nested inputs flattens
#     flatten_inputs = []
#     for input_data in inputs.data:
#         if input_data is None:
#             continue
#         if isinstance(input_data, (list, tuple)):
#             flatten_inputs.extend(_flattenize_inputs(input_data))
#         elif isinstance(input_data, dict):
#             flatten_inputs.extend(_flattenize_inputs(list(
#                 input_data.values())))
#         else:
#             flatten_inputs.append(input_data)
#     return flatten_inputs
# """, func_type=FuncType.SELF_CONTAINED)
#     status, instruction = ig.generate_instruction(func)
#     print(instruction)
# """
# ```json
# {
#     "Reason": "The function's parameter 'inputs' is not a combination of basic types, and it uses the attribute 'data' of this parameter. Since we do not know the type of 'inputs' and it uses methods or attributes of this parameter, we cannot generate an instruction."
# }
# ```
# """
# """
# Write a Python function named `_flattenize_inputs` that takes a single parameter `inputs`, which can be a nested structure containing lists, tuples, dictionaries, or other data types. The function should recursively traverse the nested structure and return a flat list containing all the non-None elements. If an element is a list or tuple, it should be further flattened. If an element is a dictionary, only its values should be considered for flattening. The function should skip any elements that are `None`.
# """

    config.PROJECT_NAME = "Python"
    config.MODE = FuncType.SELF_CONTAINED
    config.BENCHMARK_PATH = Path(config.CURRENT_PROJECT_PATH) / "benchmark" / config.PROJECT_NAME
    print(config.BENCHMARK_PATH)
    
    # config.PROJECT_NAME = "weakly"
    # config.MODE = FuncType.WEAKLY_SELF_CONTAINED
    # config.BENCHMARK_PATH = Path(config.CURRENT_PROJECT_PATH) / "benchmark" / config.PROJECT_NAME
    # print(config.BENCHMARK_PATH)

    success_count, fail_count, total_folders = batch_generate_instruction()
    print(f"Success: {success_count}, Failed: {fail_count}, Total: {total_folders}")