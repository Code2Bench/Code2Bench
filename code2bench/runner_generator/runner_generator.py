import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

from code2bench.data_model import FuncType, GeneratedDriver
from code2bench.instruction_generator.go_instruction_generator import generate_instruction_for_go
from code2bench.instruction_generator.ts_instruction_generator import generate_instruction_for_ts
from code2bench.instruction_generator.java_instruction_generator import generate_instruction_for_java
from code2bench.runner_generator.go_runner_generator import GoRunnerGenerator
from code2bench.runner_generator.java_runner_generator import JavaRunnerGenerator
from code2bench.llm.llm_caller import call_llm
from code2bench.prompt.runner_generator import RUNNER_GENERATOR_PROMPT, WEAKLY_SELF_CONTAINED_RUNNER_GENERATOR_PROMPT
from code2bench.prompt.testcases_generator import RECURSIVE_NOTE
from code2bench.test_runner.dry_run import dry_run_python_runner, dry_run_runner
from code2bench.utils.file_utils import copy_file, load_reasoning_testcases, load_testcases
from code2bench.utils.helper import is_recursive_function
from code2bench.utils.js import convert_python_docstring_to_js_doc
from code2bench.utils.json_utils import clean_response_content, get_python_response, load_json, save_json
from code2bench.utils.python import modify_runner
from code2bench.utils.go import convert_python_docstring_to_go_comment, extract_function_name as go_extract_function_name
from code2bench import config, logger, llm_client
from code2bench.runner_generator.testcase_generator import TSGenerator, JSGenerator
from code2bench.utils.java import add_package, extract_java_method_name, convert_python_docstring_to_java_doc
from code2bench.utils.ts import convert_python_docstring_to_ts_doc


class RunnerGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate_runner(self, driver_str: str, last_runner=None, error_msg: str=None):
        assert config.MODE == FuncType.WEAKLY_SELF_CONTAINED, "Only WEAKLY_SELF_CONTAINED mode is supported for now."
        system_prompt = WEAKLY_SELF_CONTAINED_RUNNER_GENERATOR_PROMPT
        error_prompt = f"""
## Previous Error Information
The previously generated driver code:
{last_runner.driver}

The previously generated driver code resulted in the following error during execution:
{error_msg}

Please analyze the error, correct the driver code, and provide the updated driver code.
""" if last_runner else ""

        # func_name = extract_function_name(driver_str)
        user_message = "<Testcase Generator>" + driver_str + "</Testcase Generator" + error_prompt
        try:
            response = call_llm(self.llm, system_message=system_prompt, user_message=user_message, clean=False)
            python_code = get_python_response(response)
            # res = json.loads(cleaned_response)
            # runner = res.get("JSONLoader")
            return GeneratedDriver(driver=python_code)
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception(f"Generating runner failed: {e}")
            return GeneratedDriver(error=str(e))
        
def generate_one_runner(idx: str, llm, language: str="Python", last_runner=None, error_msg=None) -> GeneratedDriver:
    if language == "Python":
        raise NotImplementedError("Python runner generation is not implemented yet.")
    elif language == "Go":
        python_runner_path = str(Path(config.BENCHMARK_PATH) / idx / "groundtruth.py")
        # if not os.path.exists(python_runner_path):
        #     original_python_runner_path = str(Path(config.BENCHMARK_PATH.replace("Go", "Python")) / idx / "groundtruth.py")
        #     if not copy_file(src=original_python_runner_path, dst=python_runner_path):
        #         logger.error(f"Failed to copy {original_python_runner_path} to {python_runner_path}.")
        #         return "", f"Failed to copy {original_python_runner_path} to {python_runner_path}."
        
        generator = GoRunnerGenerator(llm)
        with open(python_runner_path) as f:
            python_runner = f.read()
        
        # Copy the testcases.json to the runner path
        testcases_path = python_runner_path.replace("groundtruth.py", "test_cases/test_cases.json")
        dst_path = python_runner_path.replace("Python", "Go").replace("groundtruth.py", "test_cases/test_cases.json")
        if not copy_file(src=testcases_path, dst=dst_path):
            logger.error(f"Failed to copy test_cases.json to {dst_path}.")
            return "", f"Failed to copy test_cases.json to {dst_path}."

        # Copy the metainfo.json to the runner path
        metainfo_path = python_runner_path.replace("groundtruth.py", "metainfo.json")
        dst_path = python_runner_path.replace("Python", "Go").replace("groundtruth.py", "metainfo.json")
        if not copy_file(src=metainfo_path, dst=dst_path):
            logger.error(f"Failed to copy metainfo.json to {dst_path}.")
            return "", f"Failed to copy metainfo.json to {dst_path}."
        
        # Copy the go helper to the runner path
        dst_path = python_runner_path.replace("Python", "Go").replace("groundtruth.py", "helper.go")
        if not copy_file(src=config.GO_RUNNER_HELPER_PATH, dst=dst_path):
            logger.error(f"Failed to copy helper.go to {dst_path}.")
            return "", f"Failed to copy helper.go to {dst_path}."
        
        # Run "go mod init" in the directory
        os.chdir(os.path.dirname(python_runner_path.replace("Python", "Go")))
        os.system(f"go mod init benchmark/Go/{idx}")
        logger.info(f"Generated instruction and function for {idx} in Go.")

        testcases = load_reasoning_testcases(python_runner_path)
        testcases_str = json.dumps(testcases["Test cases"][:3], indent=2, ensure_ascii=False)
        runner, signature = generator.generate_runner(python_runner=python_runner, testcases_str=testcases_str, last_runner=last_runner, error_msg=error_msg)
        return runner, signature
    elif language == "TS":
        python_runner_path = str(Path(config.BENCHMARK_PATH) / idx / "groundtruth.py")
        with open(python_runner_path) as f:
            python_runner = f.read()
        testcases_path = python_runner_path.replace("groundtruth.py", "test_cases/test_cases.json")
        dst_path = python_runner_path.replace("Python", "TS").replace("groundtruth.py", "test_cases/test_cases.json")
        if not copy_file(src=testcases_path, dst=dst_path):
            logger.error(f"Failed to copy test_cases.json to {dst_path}.")
            return "", f"Failed to copy test_cases.json to {dst_path}."
        
        metainfo_path = python_runner_path.replace("groundtruth.py", "metainfo.json")
        dst_path = python_runner_path.replace("Python", "TS").replace("groundtruth.py", "metainfo.json")
        if not copy_file(src=metainfo_path, dst=dst_path):
            logger.error(f"Failed to copy metainfo.json to {dst_path}.")
            return "", f"Failed to copy metainfo.json to {dst_path}."
        
        metainfo = load_json(metainfo_path)
        true_func_name = metainfo.get("func_name")

        reasoning_testcases = load_reasoning_testcases(python_runner_path)
        testcases = load_testcases(python_runner_path)
        testcases_str = json.dumps(reasoning_testcases["Test cases"][:3], indent=2, ensure_ascii=False)
        generator = TSGenerator(func_name=true_func_name, gt_example=testcases[0], tested_file_path="./tested", idx=idx, llm=llm)
        return generator.generate_template(python_runner=python_runner, testcases_str=testcases_str)
    elif language == "JS":
        python_runner_path = str(Path(config.BENCHMARK_PATH) / idx / "runner.py")
        with open(python_runner_path) as f:
            python_runner = f.read()
        testcases_path = python_runner_path.replace("runner.py", "test_cases/test_cases.json")
        dst_path = python_runner_path.replace("Python", "JS").replace("runner.py", "test_cases/test_cases.json")
        if not copy_file(src=testcases_path, dst=dst_path):
            logger.error(f"Failed to copy test_cases.json to {dst_path}.")
            return "", f"Failed to copy test_cases.json to {dst_path}."
        
        metainfo_path = python_runner_path.replace("runner.py", "metainfo.json")
        dst_path = python_runner_path.replace("Python", "JS").replace("runner.py", "metainfo.json")
        if not copy_file(src=metainfo_path, dst=dst_path):
            logger.error(f"Failed to copy metainfo.json to {dst_path}.")
            return "", f"Failed to copy metainfo.json to {dst_path}."
        
        metainfo = load_json(metainfo_path)
        true_func_name = metainfo.get("func_name")

        testcases = load_testcases(python_runner_path)
        generator = JSGenerator(func_name=true_func_name, gt_example=testcases[0], tested_file_path="./tested", idx=idx)
        return generator.generate()
    elif language == "Java":
        python_runner_path = str(Path(config.BENCHMARK_PATH) / idx.lstrip("p") / "groundtruth.py")
        java_base_path = str(Path(config.BENCHMARK_PATH.replace("Python", "Java")) / idx )
        generator = JavaRunnerGenerator(llm)
        with open(python_runner_path) as f:
            python_runner = f.read()
        
        # Copy the testcases.json to the runner path
        testcases_path = python_runner_path.replace("groundtruth.py", "test_cases/test_cases.json")
        dst_path = str(Path(java_base_path) / "src" / "test" / "java" / "test_cases" / "test_cases.json")
        if not copy_file(src=testcases_path, dst=dst_path):
            logger.error(f"Failed to copy test_cases.json to {dst_path}.")
            return "", f"Failed to copy test_cases.json to {dst_path}."
    
        # Copy the metainfo.json to the runner path
        metainfo_path = python_runner_path.replace("groundtruth.py", "metainfo.json")
        dst_path = str(Path(java_base_path) / "metainfo.json")
        if not copy_file(src=metainfo_path, dst=dst_path):
            logger.error(f"Failed to copy metainfo.json to {dst_path}.")
            return "", f"Failed to copy metainfo.json to {dst_path}."

        # Copy the Java helper to the runner path
        dst_path = str(Path(java_base_path) / "src" / "main" / "java" / idx / "Helper.java")
        if not copy_file(src=config.JAVA_RUNNER_HELPER_PATH, dst=dst_path):
            logger.error(f"Failed to copy Helper.java to {dst_path}.")
            return "", f"Failed to copy Helper.java to {dst_path}."
        
        with open(dst_path, 'r') as f:
            helper = f.read()
        if not helper.startswith("package p"):
            helper = f"package {idx};\n" + helper
        with open(dst_path, "w") as f:
            f.write(helper)
        
        # Copy pom to the runner path
        pom_path = config.JAVA_POM_TEMPLATE_PATH
        dst_path = str(Path(java_base_path) / "pom.xml")
        if not copy_file(src=pom_path, dst=dst_path):
            logger.error(f"Failed to copy pom.xml to {dst_path}.")
            return "", f"Failed to copy pom.xml to {dst_path}."
        
        testcases = load_reasoning_testcases(python_runner_path)
        testcases_str = json.dumps(testcases["Test cases"][:3], indent=2, ensure_ascii=False)
        runner, signature = generator.generate_runner(python_runner=python_runner, testcases_str=testcases_str, last_runner=last_runner, error_msg=error_msg)

        return runner, signature

        # testcases = load_testcases(python_runner_path)
        # testcases_str = json.dumps(testcases[:3], indent=2, ensure_ascii=False)
        # return generator.generate_runner(python_runner=python_runner, testcases_str=testcases_str, last_runner=last_runner, error_msg=error_msg)

def generate_runner_for_weakly(idx: str, func_name: str):
    testcase_generator_path = str(Path(config.BENCHMARK_PATH) / idx / "testcase_generator.py")
    with open(testcase_generator_path) as f:
        testcase_generator_str = f.read()
    runner_path = str(Path(config.BENCHMARK_PATH) / idx / "runner.py")
    
    # 添加deep compare函数, copy helper to runner path
    if not copy_file(src=config.PYTHON_RUNNER_HELPER_PATH, dst=str(runner_path).replace("runner.py", "helper.py")):
        logger.error(f"Failed to copy helper.py to {runner_path}.")
        return False, f"Failed to copy helper.py to {runner_path}."
    
    generator = RunnerGenerator(llm_client)
    
    last_runner = None
    error_msg = None
    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        runner = generator.generate_runner(driver_str=testcase_generator_str, last_runner=last_runner, error_msg=error_msg)

        if runner.error:
            last_runner = runner
            error_msg = runner.error
            retry_count += 1
            continue

        with open(runner_path, "w") as f:
            f.write(runner.driver)

        # dry run
        error_type, error_msg = dry_run_python_runner(runner_path=runner_path, func_name=func_name)
        if not error_type:
            break
        
        if error_type == "TimeoutError":
            logger.error(f"Timeout error for function {idx}.")
            return False, error_msg
        
        if error_type:
            last_runner = runner
            error_msg = error_msg
            retry_count += 1

    logger.info(f"Generated runner for function {idx}.")

    # 添加deep compare函数, copy helper to runner path
    if not copy_file(src=config.PYTHON_RUNNER_HELPER_PATH, dst=str(runner_path).replace("runner.py", "helper.py")):
        logger.error(f"Failed to copy helper.py to {runner_path}.")
        return False, f"Failed to copy helper.py to {runner_path}."
    return True, ""


def generate_runner_without_llm(idx: str, func_name, language: str="Python"):
    if language == "Python":
        with open(config.TESTCASE_RUNNER_TEMPLATE_PATH) as f:
            runner = f.read()
        runner = runner.replace("move_y", func_name)
        runner_path = Path(config.BENCHMARK_PATH) / idx / "runner.py"
        with open(runner_path, "w") as f:
            f.write(runner)
        logger.info(f"Generated runner for function {idx}.")

        # 添加deep compare函数, copy helper to runner path
        if not copy_file(src=config.PYTHON_RUNNER_HELPER_PATH, dst=str(runner_path).replace("runner.py", "helper.py")):
            logger.error(f"Failed to copy helper.py to {runner_path}.")
            return False, f"Failed to copy helper.py to {runner_path}."
        return True, ""
    elif language == "Java":
        java_base_path = str(Path(config.BENCHMARK_PATH.replace("Python", "Java")) / idx )
        python_runner_path = str(Path(config.BENCHMARK_PATH) / idx.lstrip("p") / "runner.py")
        
        # Copy the instruction.txt to the runner path
        pure_instruction_path = str(Path(config.BENCHMARK_PATH) / idx.lstrip("p") / "pure_instruction.txt")
        with open(pure_instruction_path, "r") as f:
            pure_instruction = f.read()
            
        
        # Copy the testcases.json to the runner path
        testcases_path = python_runner_path.replace("runner.py", "test_cases/test_cases.json")
        dst_path = str(Path(java_base_path) / idx / "src" / "test" / "java" / "test_cases" / "test_cases.json")
        if not copy_file(src=testcases_path, dst=dst_path):
            logger.error(f"Failed to copy test_cases.json to {dst_path}.")
            return "", f"Failed to copy test_cases.json to {dst_path}."
    
        # Copy the metainfo.json to the runner path
        metainfo_path = python_runner_path.replace("runner.py", "metainfo.json")
        dst_path = str(Path(java_base_path) / idx / "src" / "main" / "java" / idx / "metainfo.json")
        if not copy_file(src=metainfo_path, dst=dst_path):
            logger.error(f"Failed to copy metainfo.json to {dst_path}.")
            return "", f"Failed to copy metainfo.json to {dst_path}."

        # Copy the Java helper to the runner path
        dst_path = str(Path(java_base_path) / idx / "src" / "main" / "java" / idx / "Helper.java")
        if not copy_file(src=config.JAVA_RUNNER_HELPER_PATH, dst=dst_path):
            logger.error(f"Failed to copy Helper.java to {dst_path}.")
            return "", f"Failed to copy Helper.java to {dst_path}."
        
        # We don't need to copy the Java Tested.java to the runner path, since we can directly use the Java Tester.java
        # # Copy the Java Tested.java to the runner path
        # tested_path = config.JAVA_TESTED_TEMPLATE_PATH
        
        # Copy the Java Tester.java to the runner path
        with open(config.JAVA_RUNNER_TEMPLATE_PATH) as f:
            runner = f.read()
        runner = runner.replace("package p0;", f"package {idx};")
        runner = runner.replace("_get_correct_indent_level", func_name)
        runner_path = Path(config.BENCHMARK_PATH) / idx / "src" / "test" / "java" / idx / "Tester.java"
        with open(runner_path, "w") as f:
            f.write(runner)
        logger.info(f"Generated Java runner for function {idx}.")

        # Copy pom to the runner path
        pom_path = config.JAVA_POM_TEMPLATE_PATH
        dst_path = str(Path(java_base_path) / idx / "pom.xml")
        if not copy_file(src=pom_path, dst=dst_path):
            logger.error(f"Failed to copy pom.xml to {dst_path}.")
            return "", f"Failed to copy pom.xml to {dst_path}."
    elif language == "TypeScript":
        pass
    elif language == "JavaScript":
        pass
    else:
        raise ValueError(f"Unsupported language: {language} in generate_runner_without_llm.")

def generate_runner_with_llm(
    idx: str, 
    language: str = "Go",
    func_name: str = None,
    dry_run: bool = False
) -> Tuple[bool, str]:
    # item_path = os.path.join(config.BENCHMARK_PATH, idx)
    # item_path = Path(item_path) / from_path
    # item_path = str(item_path).replace(language, "default")
    # if not os.path.exists(item_path):
    #     logger.error(f"Failed to find driver file for function {idx}.")
    #     return False
    
    base_dir_path = Path(config.BENCHMARK_PATH.replace("Python", language))
    metainfo_path = base_dir_path / idx / "metainfo.json"
    # 把driver输出到对应的文件中
    if language == "Java":
        idx = 'p' + idx # Java的idx是p0,p1,p2...，而不是0,1,2...
        to_path = "Tester.java"
        runner_path = base_dir_path / idx / "src" / "test" / "java" / to_path
        metainfo_path = base_dir_path / idx / "metainfo.json"
    elif language == "Go":
        to_path = "runner_test.go"
        runner_path = base_dir_path / idx / to_path
    elif language == "TS":
        to_path = "runner.test.ts"
        runner_path = base_dir_path / idx / to_path
    elif language == "JS":
        to_path = "runner.test.js"
        runner_path = base_dir_path / idx / to_path

    if not os.path.exists(runner_path.parent):
        os.makedirs(runner_path.parent)
        
    max_retries = 3
    retry_count = 0
    last_error = None
    runner = None
    error_msg = None
    while retry_count < max_retries:
        runner, signature = generate_one_runner(idx=idx, llm=llm_client, language=language, last_runner=runner, error_msg=last_error)
        
        if not runner:
            logger.error(f"Failed to generate runner for function {idx}.")
            return False, signature
        
        # print(runner.driver)
        
        if runner.error:
            last_error = runner.error
            retry_count += 1
            continue

        if language == "Python":
            # 如果max_examples=100，更换成 max_examples=1000
            # driver.driver = driver.driver.replace("max_examples=100", "max_examples=1000")
            raise NotImplementedError("Python runner generation is not implemented yet.")
        elif language == "Go":
            tested_path = base_dir_path / idx / "tested.go"
            # Insert `Package main` at the beginning of the file
            if not signature.startswith("package main"):
                signature = "package main\n" + signature
            
            with open(tested_path, "w") as f:
                f.write(signature)
            
            true_func_name = go_extract_function_name(runner.driver)
            metainfo = load_json(metainfo_path)
            metainfo['func_name'] = true_func_name
            metainfo['original_func_name'] = func_name
            save_json(metainfo_path, metainfo)
            
            # Copy the instruction.txt to the runner path
            pure_instruction_path = str(Path(config.BENCHMARK_PATH) / idx / "pure_instruction.txt")
            with open(pure_instruction_path, "r") as f:
                pure_instruction = f.read()
            if not pure_instruction:
                logger.error(f"Failed to find pure_instruction.txt file for function {idx}.")
                raise FileNotFoundError(f"Failed to find pure_instruction.txt file for function {idx}. You need to generate it first.")
            
            instruction_path = str(Path(config.BENCHMARK_PATH) / idx / "instruction.txt").replace("Python", "Go")
            # with open(instruction_path, "w") as f:
            #     go_instruction = pure_instruction + "\nYou should write code starting with:\n" + signature 
            #     f.write(go_instruction)
            docstring = convert_python_docstring_to_go_comment(pure_instruction)
            func_index = signature.find("func ")
            if func_index != -1:
                # 找到func前面的换行符位置
                newline_before_func = signature.rfind("\n", 0, func_index)
                if newline_before_func == -1:  # 如果func在第一行
                    newline_before_func = 0
                
                # 确保package声明保持在最前面
                if signature.startswith("package main"):
                    modified_signature = signature[:newline_before_func] + "\n" + docstring + signature[newline_before_func:]
                else:
                    # 如果没有package声明，添加一个并放在最前面
                    modified_signature = "package main\n\n" + docstring + "\n" + signature.lstrip("package main\n")
            else:
                return False, "Failed to find function definition in the signature."
            with open(instruction_path, "w") as f:
                f.write(modified_signature)
            
            logger.info(f"Generated Go runner for function {idx}.")
        # TS/JS don't need any additional operations
        elif language == "TS":
            pure_instruction_path = str(Path(config.BENCHMARK_PATH) / idx / "pure_instruction.txt")
            with open(pure_instruction_path, "r") as f:
                pure_instruction = f.read()
            if not pure_instruction:
                logger.error(f"Failed to find pure_instruction.txt file for function {idx}.")
                raise FileNotFoundError(f"Failed to find pure_instruction.txt file for function {idx}. You need to generate it first.")
            
            tested_path = base_dir_path / idx / "tested.ts"
            with open(tested_path, "w") as f:
                f.write(signature)
            
            instruction_path = str(Path(config.BENCHMARK_PATH) / idx / "instruction.txt").replace("Python", "TS")
            ts_docstring = convert_python_docstring_to_ts_doc(pure_instruction)
            with open(instruction_path, "w") as f:
                # go_instruction = pure_instruction + "\nYou should write code starting with:\n" + signature 
                instruction = ts_docstring + "\n" + signature
                f.write(instruction)
            logger.info(f"Generated TS runner for function {idx}.")
        elif language == "JS":
            pure_instruction_path = str(Path(config.BENCHMARK_PATH) / idx / "pure_instruction.txt")
            with open(pure_instruction_path, "r") as f:
                pure_instruction = f.read()
            if not pure_instruction:
                logger.error(f"Failed to find pure_instruction.txt file for function {idx}.")
                raise FileNotFoundError(f"Failed to find pure_instruction.txt file for function {idx}. You need to generate it first.")
            
            tested_path = base_dir_path / idx / "tested.js"
            with open(tested_path, "w") as f:
                f.write(signature)
            
            instruction_path = str(Path(config.BENCHMARK_PATH) / idx / "instruction.txt").replace("Python", "JS")
            js_docstring = convert_python_docstring_to_js_doc(pure_instruction)
            with open(instruction_path, "w") as f:
                # instruction = js_docstring + "\nYou should write code starting with:\n" + signature 
                instruction = js_docstring + "\n" + signature
                f.write(instruction)
            logger.info(f"Generated JS runner for function {idx}.")
        elif language == "Java":
            runner.driver = add_package(runner.driver, idx)
            signature = add_package(signature, idx)
            # runner.driver = runner.replace("benchmark/Java/test_data.json", f"benchmark/Java/tests/{idx}/test_cases/test_data.json")

            tested_path = base_dir_path / idx / "src" / "main" / "java" / idx / "Tested.java"
            with open(tested_path, "w") as f:
                f.write(signature)
                
            true_func_name = extract_java_method_name(signature)
            metainfo = load_json(metainfo_path)
            metainfo['func_name'] = true_func_name
            metainfo['original_func_name'] = func_name
            save_json(metainfo_path, metainfo)
            
            # Copy the instruction.txt to the runner path
            pure_instruction_path = str(Path(config.BENCHMARK_PATH) / idx.lstrip("p") / "pure_instruction.txt")
            with open(pure_instruction_path, "r") as f:
                pure_instruction = f.read()
            if not pure_instruction:
                logger.error(f"Failed to find pure_instruction.txt file for function {idx}.")
                raise FileNotFoundError(f"Failed to find pure_instruction.txt file for function {idx}. You need to generate it first.")
                        
            java_docstring = convert_python_docstring_to_java_doc(pure_instruction)
            instruction_path = str(Path(config.BENCHMARK_PATH) / idx / "instruction.txt").replace("Python", "Java")
            with open(instruction_path, "w") as f:
                # java_instruction = pure_instruction + "\nYou should write code starting with:\n" + signature 
                # java_instruction = java_docstring + "\n" + signature
                java_instruction = signature.replace("public class Tested", (
                    java_docstring + "\n" + "public class Tested"
                ))                    

                f.write(java_instruction)
            logger.info(f"Generated Java instruction for function {idx}.")

        with open(runner_path, "w") as f:
            f.write(runner.driver)
        logger.info(f"Generated {language} runner for function {idx}.")
        
        # Go don't need to dry run. We use LLM to generate the tested.go file after that to run the runner
        if language == "Go" or language == "TS" or language == "Java" or language == "JS":
            return True, ""
        
        # Dry run
        if dry_run:
            error_type, error_msg = dry_run_runner(idx=idx, llm=llm_client, func_name=func_name, language=language)
            if not error_type:
                return True
            if error_type == "TimeoutError":
                logger.error(f"Timeout error for function {idx}.")
                return False
        
        # Use LLM to generate the tested file to dry run the runner

        last_error = error_msg
        retry_count += 1
    
    logger.error(f"Failed to generate testcases for function {idx}.")
    return False, "Failed to generate runner."

def batch_generate_runner_with_llm():
    config.BENCHMARK_NAME = "Python"
    # config.BENCHMARK_PATH = str(Path(config.BENCHMARK_PATH)).replace("Python", "Go")
    python_path = str(Path(config.BENCHMARK_PATH)).replace("Go", "Python") 
    
        # 获取并过滤出纯数字命名的文件夹
    all_items = os.listdir(config.BENCHMARK_PATH)
    benchmarks = []
    for item in all_items:
        if item.isdigit() and os.path.isdir(os.path.join(config.BENCHMARK_PATH, item)):
            benchmarks.append(item)
    
    # 按数字排序（而不是字符串排序）
    benchmarks = sorted(benchmarks, key=int)
    
    # benchmarks = sorted(os.listdir(config.BENCHMARK_PATH))
    status_list = []
    for idx in benchmarks:
        # if int(idx) <= 160:
        #     continue
        
        # if int(idx) not in [13, 56, 64, 87, 125, 176, 186]:
        if int(idx) not in [9, 10, 21, 22, 37, 49, 52, 53, 59, 67, 121, 125, 137, 164, 193]:
            continue

        python_metainfo_path = str(Path(python_path) / idx / "metainfo.json")
        if not os.path.exists(python_metainfo_path):
            raise FileNotFoundError(f"Failed to find metainfo.json file for function {idx}.")
        metainfo = load_json(python_metainfo_path)
        func_name = metainfo.get("func_name")
        
        status, _ = generate_runner_with_llm(idx, language="Go", func_name=func_name)
        # status, _ = generate_runner_with_llm(idx, language="Java", func_name=func_name)
        if status is True:
            logger.info(f"Generated runner for function {idx}.")
            status_list.append(status)
        else:
            logger.error(f"Failed to generate runner for function {idx}.")
            status_list.append(status)
            continue
    with open('status_list.json', 'w') as f:
        json.dump(status_list, f, indent=2)
        
def generate_runner_for_js(idx: str):
    pass
        
def bathc_generate_runner_for_js():
    pass

def batch_run_runers(language: str="Python", specified_idx: str=None):
    benchmarks = sorted(os.listdir(config.BENCHMARK_PATH))
    if language == "Python":
        from_path = "testcase_generator.py"
        to_path = "runner.py"
        dry_run = True
        testcases_index_path = config.BENCHMARK_TESTCASES_INDEX_PATH
        testcases_index_dict = load_json(testcases_index_path)
        testcases_set = set(testcases_index_dict["success"] + testcases_index_dict["failed"])
        pass
    elif language == "Java":
        config.BENCHMARK_NAME = "Java"
        from_path = "testcase_generator.py"
        to_path = "Tester.java"
        dry_run = False
    elif language == "Go":
        config.BENCHMARK_NAME = "Go"
        from_path = "testcase_generator.py"
        to_path = "runner_test.go"
        dry_run = False
    elif language == "TS":
        config.BENCHMARK_NAME = "TS"
        from_path = "testcase_generator.py" 
        to_path = "runner.test.ts"
        dry_run = False
        
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
        
        runner_path = Path(config.BENCHMARK_PATH) / idx / to_path
        if language == "Java":
            runner_path = Path(config.BENCHMARK_PATH) / "tests" / idx / to_path

        if cnt == 3:
            break
        
        if language == "Go":
            # Need to generate the instruction first
            if generate_instruction_for_go(idx) is False:
                index_dict["failed"].append(idx)
                save_json(index_path, index_dict)
                continue
        elif language == "TS":
            if generate_instruction_for_ts(idx) is False:
                index_dict["failed"].append(idx)
                save_json(index_path, index_dict)
                continue
        elif language == "Java":
            if generate_instruction_for_java(idx) is False:
                index_dict["failed"].append(idx)
                save_json(index_path, index_dict)
                continue

        if idx == '0':
            continue
        status = generate_runner_with_llm(idx, language=language, dry_run=dry_run)
        cnt += 1
 
        if status is True:
            index_dict["success"].append(idx)
            save_json(index_path, index_dict)
        else:
            index_dict["failed"].append(idx)
            save_json(index_path, index_dict)
            if runner_path.exists():
                os.remove(runner_path)
            else:
                logger.warning(f"File {runner_path} does not exist.")
                

if __name__ == "__main__":
    # batch_run_runers(language="Python", specified_idx="testcase_1")
    # config.BENCHMARK_NAME = "Python"
    # generate_runner_with_llm("2", "TS", "")
    # pass    
    
    batch_generate_runner_with_llm()