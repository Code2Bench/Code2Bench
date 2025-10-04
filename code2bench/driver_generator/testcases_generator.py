import os
from pathlib import Path
from typing import Dict, List, Tuple

from code2bench import config, logger
from code2bench.runner_generator.go_runner_generator import GoRunnerGenerator
from code2bench.llm.llm_caller import call_llm
from code2bench.data_model import FuncToGenerate, FuncType, GeneratedDriver
from code2bench.prompt.testcases_generator import RECURSIVE_NOTE, TESTCASES_GENERATOR_PROMPT, WEAKLY_SELF_CONTAINED_TESTCASES_GENERATOR_PROMPT
from code2bench.prompt.runner_generator import RUNNER_GENERATOR_PROMPT
from code2bench.runner_generator.runner_generator import generate_one_runner
from code2bench.utils.json_utils import clean_response_content, get_python_response, load_json, save_json
from code2bench import llm_client
from code2bench.utils.python import extract_function_name, extract_imported_function
from code2bench.test_runner.dry_run import dry_run, dry_run_runner
from code2bench.utils.file_utils import load_testcases
from code2bench.utils.helper import is_recursive_function


class TestcasesGenerator:

    def __init__(self, llm=None):
        self.llm = llm
    
    def load_driver(self, driver_path: str) -> str:
        with open(driver_path, "r") as f:
            return f.read()

    def load_runner_prompt(self, language: str="Python") -> str:
        python_runner_prompt = RUNNER_GENERATOR_PROMPT
        if language == "Python":
            return python_runner_prompt
        elif language == "Java":
            pass
        else:
            raise ValueError(f"Unsupported language: {language} for generating runner prompt.")

    def generate_testcase_generator(self, groundtruth: str, last_driver=None, error_msg=None) -> GeneratedDriver:
        if config.MODE == FuncType.SELF_CONTAINED: 
            base_prompt = TESTCASES_GENERATOR_PROMPT
        elif config.MODE == FuncType.WEAKLY_SELF_CONTAINED:
            base_prompt = WEAKLY_SELF_CONTAINED_TESTCASES_GENERATOR_PROMPT

        error_prompt = f"""
## Previous Error Information
The previously generated driver code:
{last_driver.driver}

The previously generated driver code resulted in the following error during execution:
{error_msg}

Please analyze the error, correct the driver code, and provide the updated driver code.
""" if last_driver else ""
        
        func_name = extract_function_name(groundtruth)
        is_recursive = is_recursive_function(function_definition=groundtruth, function_name=func_name)
        if is_recursive:
            base_prompt = base_prompt + RECURSIVE_NOTE
        # full_prompt = base_prompt + (error_prompt if error_msg else "")
        full_prompt = base_prompt
        user_message = groundtruth + error_prompt
        # key = "TestcaseGenerator"

        try:
            response = call_llm(self.llm, system_message=full_prompt, user_message=user_message, clean=False)
            python_code = get_python_response(response)
            # res = json.loads(cleaned_response)
            # driver = res[key]
            
            if 'atexit' not in python_code:
                error_msg = "The generated code does not include the atexit to save the test cases. You need to add it. for example: atexit.register(save_test_cases) at the end of the code."
                return GeneratedDriver(error=error_msg)
            return GeneratedDriver(driver=python_code)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(f"Generating testcase generator failed: {e}")
            return GeneratedDriver(error=str(e))


def generate_one_testcases(groundtruth: str, llm, last_driver=None, error_msg=None) -> GeneratedDriver:
    generator = TestcasesGenerator(llm)
    return generator.generate_testcase_generator(groundtruth, last_driver, error_msg=error_msg)

def run_once_testcase_generation(
    idx: str, 
    from_path: str = "groundtruth.py", 
    to_path: str = "testcase_generator.py",
    # item_path: str = None,
) -> Tuple[bool, str]:
    item_path = os.path.join(config.BENCHMARK_PATH, idx)
    item_path = Path(item_path) / from_path
    # item_path = str(item_path).replace(language, "default")
    if not os.path.exists(item_path):
        logger.error(f"Failed to find groundtruth file for function {idx}.")
        raise FileNotFoundError(f"Failed to find groundtruth file for function {idx}.")

    with open(item_path, "r") as f:
        func_str = f.read()
    
    # func_name = extract_imported_function(func_str) or extract_function_name(func_str)
    func_name = extract_function_name(func_str)
    
    # # 把driver输出到对应的文件中
    # driver_path = Path(config.BENCHMARK_PATH) / idx / to_path
    # if not os.path.exists(driver_path.parent):
    #     os.makedirs(driver_path.parent)
    
    testcase_generator_path = Path(config.BENCHMARK_PATH) / idx / to_path
    if not os.path.exists(testcase_generator_path.parent):
        os.makedirs(testcase_generator_path.parent)
    
    max_retries = 3
    retry_count = 0
    last_error = None
    driver = None
    while retry_count < max_retries:
        driver = generate_one_testcases(groundtruth=func_str, llm=llm_client, last_driver=driver, error_msg=last_error)
        print(f"Testcase generation for function {idx}:")
        # print(driver.driver)

        # 如果max_examples=100，更换成 max_examples=10000
        driver.driver = driver.driver.replace("max_examples=100,", "max_examples=10000,")
        driver.driver = driver.driver.replace("max_examples=1000,", "max_examples=10000,")

        if driver.error:
            last_error = driver.error
            retry_count += 1
            continue

        with open(testcase_generator_path, "w") as f:
            f.write(driver.driver)
        logger.info(f"Generated testcase generator for function {idx}.")
        
        # Dry run
        error_type, error_msg = dry_run(testcase_generator_path, func_name=func_name)
        if not error_type:
            return True, ""
        if error_type == "TimeoutError":
            logger.error(f"Timeout error for function {idx}.")
            return False, "Dry run timeout."
        last_error = error_msg
        retry_count += 1
    
    logger.error(f"Failed to generate testcases for function {idx}.")
    return False, last_error


def batch_run_testcases(specified_idx: str=None):
    index_dict: Dict[str, List[str]] = {
        "success": [],
        "failed": []
    }
    testcases_index_path = config.BENCHMARK_TESTCASES_INDEX_PATH
    if os.path.exists(testcases_index_path):
        index_dict = load_json(testcases_index_path)

    cnt = 0
    benchmarks = sorted(os.listdir(config.BENCHMARK_PATH))
    # Filter out files that are not directories
    benchmarks = [b for b in benchmarks if os.path.isdir(os.path.join(config.BENCHMARK_PATH, b))]
    
    for idx in benchmarks:
        if (
            (idx in index_dict["success"] or idx in index_dict["failed"])
            and specified_idx is None
        ):
            continue
        
        # if cnt == 20:
        #     break
        
        if specified_idx and idx != specified_idx:
            continue

        status = run_once_testcase_generation(idx, generate_one_testcases, from_path="driver.py", to_path="testcase_generator.py")
        cnt += 1
 
        if status is True:
            index_dict["success"].append(idx)
            save_json(testcases_index_path, index_dict)
        else:
            index_dict["failed"].append(idx)
            save_json(testcases_index_path, index_dict)
            
            if os.path.exists(str(Path(config.BENCHMARK_PATH) / idx / "testcase_generator.py")):
                # 删除
                os.remove(str(Path(config.BENCHMARK_PATH) / idx / "testcase_generator.py"))

def batch_run_runers(language: str="Python", specified_idx: str=None):
    benchmarks = sorted(os.listdir(config.BENCHMARK_PATH))
    if language == "Python":
        from_path = "testcase_generator.py"
        to_path = "runner.py"
        testcases_index_path = config.BENCHMARK_TESTCASES_INDEX_PATH
        testcases_index_dict = load_json(testcases_index_path)
        testcases_set = set(testcases_index_dict["success"] + testcases_index_dict["failed"])
    elif language == "Java":
        pass
    elif language == "Go":
        config.BENCHMARK_NAME = "Go"
        from_path = "testcase_generator.py"
        to_path = "runner_test.go"
    
    index_dict: Dict[str, List[str]] = {
        "success": [],
        "failed": []
    }
    index_path = config.BENCHMARK_RUNNERS_INDEX_PATH
    if os.path.exists(index_path):
        index_dict = load_json(index_path)
    
    cnt = 0
    for idx in benchmarks:
        if (
            language == "Python" and idx not in testcases_set and 
            specified_idx and idx != specified_idx
        ):
            continue
        
        if (
            (idx in index_dict["success"] or idx in index_dict["failed"])
            and specified_idx and idx != specified_idx
        ):
            continue
        
        if specified_idx and idx != specified_idx:
            continue

        # if cnt == 3:
        #     break
        if language == "Go":
            # 创建tested.go文件
            tested_path = Path(config.BENCHMARK_PATH) / idx / "tested.go"
            if not os.path.exists(tested_path.parent):
                os.makedirs(tested_path.parent)
            # 写入func_name占位，这部分比较难搞啊，可能需要调用LLM了。
            with open(tested_path, "w") as f:
                pass

        status = run_once_testcase_generation(idx, generate_one_runner, dry_run_func=dry_run_runner, from_path=from_path, to_path=to_path, language=language)
        cnt += 1
 
        if status is True:
            index_dict["success"].append(idx)
            save_json(index_path, index_dict)
        else:
            index_dict["failed"].append(idx)
            save_json(index_path, index_dict)
            
            
            runner_path = Path(config.BENCHMARK_PATH) / idx / to_path
            if runner_path.exists():
                os.remove(runner_path)
            else:
                logger.warning(f"File {runner_path} does not exist.")


if __name__ == "__main__":
    batch_run_testcases()
    # batch_run_testcases(specified_idx="115")
    # batch_run_runers(language="Go", specified_idx="1")
    # batch_run_runers(language="Go")
    # batch_run_runers(language="Python", specified_idx="136")