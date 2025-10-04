import os
import re
import subprocess
import sys
import traceback
from typing import Optional, Tuple

from code2bench import logger
from code2bench.config import config
from code2bench.test_runner.go_tested_generator import GoTestedGenerator
from code2bench.test_runner.java_tested_generator import JavaTestedGenerator
from code2bench.utils.coverage import get_coverage_report, is_function_fully_covered


def run_pytest(driver_path: str) -> Tuple[Optional[str], Optional[str]]:
    """运行pytest并解析测试结果"""
    original_dir = os.getcwd()
    try:
        # 切换到driver所在目录
        work_dir = os.path.dirname(os.path.abspath(driver_path))
        os.chdir(work_dir)
        
        command = [
            sys.executable, "-m", "pytest",
            "--disable-warnings",
            "--verbose",
            "--capture=no",  # 禁止输入捕获
            os.path.basename(driver_path)
        ]
        
        logger.info(f"Running pytest in {work_dir} with command: {' '.join(command)}")
        
        timeout_time = 480 # 之前设置120秒，结果第二个item直接超时了，花了121秒。运行了一个花了204秒
        # 捕获完整输出
        result = subprocess.run(
            command,
            # stdout=sys.stdout,  # 直接输出到终端
            # stderr=sys.stderr,
            text=True,
            timeout=timeout_time,
            capture_output=True,
            # text=True,
            # timeout=timeout_time  # 增加超时时间
        )
        
        # 解析输出
        if result.returncode == 0:
            logger.info("Run succeeded")
            return None, None
        else:
            # error_type, error_msg = parse_pytest_output(result.stdout, result.stderr)
            error_type, error_msg = "ExecutionError", result.stdout.strip().replace(" ", "")
            logger.error(f"Pytest failed with {error_type}: {error_msg}")
            return error_type, error_msg
            # 下面这个不能用，因为上面开了stdout=sys.stdout之后，result.stderr就是None了，下轮生成的时候没有报错信息的指示了。
            # logger.error(f"Pytest failed with{result.returncode}: {result.stderr}")
            # return "ExecutionError", result.stderr[-500:]  # 返回最后500字符防止信息过长
    except subprocess.TimeoutExpired:
        logger.error("Pytest execution timed out")
        return "TimeoutError", f"Test execution exceeded {timeout_time} seconds"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "ExecutionError", str(e)
    finally:
        os.chdir(original_dir)  # 恢复原始工作目录

def parse_pytest_output(stdout: str, stderr: str) -> Tuple[str, str]:
    """解析pytest的输出"""
    # 优先检查标准错误
    if stderr:
        if "SyntaxError" in stderr:
            return "SyntaxError", stderr.split("SyntaxError: ")[-1].split("\n")[0]
        if "ImportError" in stderr:
            return "DependencyError", stderr.split("ImportError: ")[-1].split("\n")[0]
    
    # 解析标准输出中的失败信息
    failure_patterns = {
        "AssertionError": (r"AssertionError: (.*)", "Assertion Failure"),
        "HypothesisError": (r"hypothesis.errors.(\w+Error): (.*)", "Property Test Failure"),
        "RuntimeError": (r"RuntimeError: (.*)", "Runtime Error"),
        "Timeout": (r"Timeout: (.*)", "Test Timeout")
    }
    
    for line in reversed(stdout.split("\n")):  # 从最后开始检查
        for err_type, (pattern, desc) in failure_patterns.items():
            match = re.search(pattern, line)
            if match:
                return err_type, f"{desc}: {match.group(1)}"
    
    # 默认返回第一个失败信息
    fail_sections = [s for s in stdout.split("\n\n") if "FAILED" in s]
    if fail_sections:
        first_fail = fail_sections[0].split("_ ", 1)[-1]
        return "TestFailure", first_fail.split("\n")[0]
    
    return "UnknownError", stdout[-500:]  # 返回最后500字符防止信息过长

def add_settings_decorator(driver_path: str, max_examples: int = 1000):
    """
    在每个 @given 装饰器对应的函数定义前添加 @settings(max_examples=max_examples)，
    并在文件开头添加相应的 import 语句。
    
    :param driver_path: 驱动文件路径。
    :param max_examples: 设置的最大示例数。
    """
    # 定义要插入的 settings 装饰器和 import 语句
    settings_decorator = f'@settings(max_examples={max_examples})\n'
    import_statement = 'from hypothesis import settings\n'

    # 读取文件内容
    with open(driver_path, "r") as f:
        content = f.read()

    # 检查并添加 import 语句
    if 'from hypothesis import settings' not in content:
        content = import_statement + content

    # 匹配所有 @given 装饰器及其对应的 def 函数定义
    given_pattern = r'(@given\(.*?\))[\s\S]*?(def\s+\w+\s*\(.*?\):)'
    matches = list(re.finditer(given_pattern, content, re.DOTALL))

    if not matches:
        print("No @given decorators found in the driver code.")
        return

    # 构造新的内容
    modified_content = content
    offset = 0  # 用于跟踪插入导致的偏移量

    for match in matches:
        # 获取 @given 装饰器和 def 函数定义的位置
        given_start_index = match.start()
        def_start_index = match.end() - len(match.group(2)) + offset

        # 检查是否已经存在 @settings 装饰器
        prev_lines = modified_content[:given_start_index].strip().split("\n")
        if any(line.strip().startswith('@settings') for line in prev_lines[-2:]):
            continue  # 已经有 @settings，跳过

        # 插入 @settings 装饰器
        modified_content = (
            modified_content[:given_start_index] +
            settings_decorator +
            modified_content[given_start_index:]
        )
        # 更新偏移量
        offset += len(settings_decorator)

    # 将修改后的内容写回文件
    with open(driver_path, "w") as f:
        f.write(modified_content)

    print(f"Added @settings(max_examples={max_examples}) to all @given decorators in {driver_path}")

def add_func_assignment(
    driver: str, 
    func_name: str, 
    given_pattern: str = r'@settings'
) -> str:
    """
    在最后一个 @settings 装饰器的上面添加 func1 = func0 语句。

    :param driver: 原始代码字符串。
    :param func_name: 函数名。
    :return: 修改后的代码字符串。
    """
    # 找到最后一个 @settings 装饰器的位置
    # given_pattern = r'@settings'
    matches = list(re.finditer(given_pattern, driver))
    if not matches:
        # raise ValueError("No @settings decorator found in the driver code.")
        return 0
    
    last_given_match = matches[-1]
    given_start_index = last_given_match.start()

    # 在最后一个 @settings 装饰器的上面添加 func1 = func0
    modified_driver = driver[:given_start_index] + f'func1 = {func_name}\n' + driver[given_start_index:]
    return modified_driver

def recover(driver_path: str, func_name: str):
    """
    恢复 add_func_assignment 函数所做的修改，即删除 func1 = func_name 的行。
    :param driver_path: 驱动文件路径。
    :param func_name: 函数名。
    """
    # 定义要删除的行的模式
    line_to_remove = f'func1 = {func_name}\n'

    # 读取文件内容
    with open(driver_path, "r") as f:
        lines = f.readlines()

    # 查找并删除指定的行
    modified_lines = [line for line in lines if line != line_to_remove]

    # 如果没有找到要删除的行，记录警告
    if len(modified_lines) == len(lines):
        logger.warning(f"Line '{line_to_remove.strip()}' not found in {driver_path}. No changes made.")
        return

    # 将修改后的内容写回文件
    with open(driver_path, "w") as f:
        f.writelines(modified_lines)
    logger.info(f"Recovered driver.py by removing 'func1 = {func_name}'")

def add_import_statement(driver_path, func_name):
    with open(driver_path, "r") as f:
        driver = f.read()
    import_statement = f"from tested import {func_name} as func1\n"
    if import_statement not in driver:
        driver = import_statement + driver
    with open(driver_path, "w") as f:
        f.write(driver)
    logger.info(f"Added import statement to driver.py")

def dry_run(driver_path: str, func_name: str, language: str="Python") -> Tuple[Optional[str], Optional[str]]:
    # # 需要先把ground_truth放到tested里面
    # # 在最后一个 @settings 装饰器的上面添加 func1 = func0
    # with open(driver_path, "r") as f:
    #     driver = f.read()
    # modified_driver = add_func_assignment(driver, func_name)
    # if modified_driver == 0:
    #     logger.error("No @settings decorator found in the driver code.")
    #     return "NoSettingsError", "No @settings decorator found in the driver code."

    # # 将修改后的内容写回文件
    # with open(driver_path, "w") as f:
    #     f.write(modified_driver)
    # logger.info(f"Edited driver.py to add func1 = {func_name}")
    
    # # When use the coverage.py, there is no need to run pytest, because the coverage.py will run pytest automatically.
    # # Call the new function in the dry_run function
    # error_type, error_msg = run_pytest(driver_path)
    # if error_type is not None:
    #     logger.error(f"Error type: {error_type}, Error message: {error_msg}")
    #     return error_type, error_msg
    
    # # recover driver.py
    # # 恢复 add_func_assignment 函数所做的修改，即删除 func1 = func_name 的行。
    # recover(driver_path, func_name)
    
    # # 添加from tested import {func_name} as func1
    # add_import_statement(driver_path, func_name)
    
    # 测试覆盖率
    status, message = is_function_fully_covered(driver_path, func_name=func_name)
    if status is not True:
        logger.error(f"Error: {status}, Message: {message}")
        return status, message 
 
    return None, None

def dry_run_python_runner(runner_path: str, func_name: str) -> Tuple[Optional[str], Optional[str]]:
    with open(runner_path, "r") as f:
        driver = f.read()
    # 把driver文件中的"from tested"改成"from ground_truth"
    driver = driver.replace("from tested", "from groundtruth")
    with open(runner_path, "w") as f:
        f.write(driver)
    logger.info(f"change 'from tested' to 'from groundtruth'")
    
    error_type, error_msg = run_python_driver(runner_path, func_name)
    
    # 恢复driver文件
    driver = driver.replace("from groundtruth", "from tested")
    with open(runner_path, "w") as f:
        f.write(driver)
    logger.info(f"Recovered by changing 'from groundtruth' to 'from tested'")
    
    return error_type, error_msg

def dry_run_go_runner(idx: str, llm, func_name: str):
    intruction_path = config.BENCHMARK_PATH.replace("Python", "Go") + f"/{idx}/instruction.txt"
    # 读取instruction.txt文件内容
    with open(intruction_path, "r") as f:
        instruction = f.read()
    
    generator = GoTestedGenerator(llm=llm)
    tested = generator.generate_tested(instruction=instruction)
    
    # with open(config.GO_TESTED_TEMPLATE_PATH, "r") as f:
    #     tested_template = f.read()
    # tested = tested_template.replace("_get_correct_indent_level", func_name)
    
    # 将生成的代码写入文件
    tested_path = config.BENCHMARK_PATH.replace("Python", "Go") + f"/{idx}/tested.go"
    with open(tested_path, "w") as f:
        f.write(tested)

    runner_path = config.BENCHMARK_PATH.replace("Python", "Go") + f"/{idx}/runner_test.go"
    error_type, error_msg = run_go_driver(runner_path, func_name)
    return error_type, error_msg

def dry_run_java_runner(idx: str, llm, func_name: str):
    intruction_path = config.BENCHMARK_PATH.replace("Python", "Java") + f"/p{idx}/instruction.txt"
    # 读取instruction.txt文件内容
    with open(intruction_path, "r") as f:
        instruction = f.read()
    
    generator = JavaTestedGenerator(llm=llm)
    tested = generator.generate_tested(instruction=instruction)
    
    # with open(config.GO_TESTED_TEMPLATE_PATH, "r") as f:
    #     tested_template = f.read()
    # tested = tested_template.replace("_get_correct_indent_level", func_name)
    
    # 将生成的代码写入文件
    tested_path = config.BENCHMARK_PATH.replace("Python", "Java") + f"/p{idx}/src/main/java/p{idx}/Tested.java"
    with open(tested_path, "w") as f:
        f.write(tested)

    runner_path = config.BENCHMARK_PATH.replace("Python", "Java") + f"/p{idx}"
    error_type, error_msg = run_java_driver(runner_path, func_name)
    return error_type, error_msg

def dry_run_ts_runner(idx: str, func_name: str):
    with open(config.TS_TESTED_TEMPLATE_PATH, "r") as f:
        tested_template = f.read()
    tested = tested_template.replace("getPipelinesDisabled", func_name)
    
    # 将生成的代码写入文件
    tested_path = config.BENCHMARK_PATH.replace("Python", "TS") + f"/{idx}/tested.ts"
    with open(tested_path, "w") as f:
        f.write(tested)

    runner_path = config.BENCHMARK_PATH.replace("Python", "TS") + f"/{idx}/runner.test.ts"
    error_type, error_msg = run_ts_driver(runner_path, func_name, idx)
    return error_type, error_msg

def dry_run_js_runner(idx: str, func_name: str):
    with open(config.JS_TESTED_TEMPLATE_PATH, "r") as f:
        tested_template = f.read()
    tested = tested_template.replace("getPipelinesDisabled", func_name)
    
    # 将生成的代码写入文件
    tested_path = config.BENCHMARK_PATH.replace("Python", "JS") + f"/{idx}/tested.js"
    with open(tested_path, "w") as f:
        f.write(tested)

    runner_path = config.BENCHMARK_PATH.replace("Python", "JS") + f"/{idx}/runner.test.js"
    error_type, error_msg = run_js_driver(runner_path, func_name, idx)
    return error_type, error_msg

def dry_run_runner(idx: str, llm, func_name: str, language: str="Python"):
    if language == "Python":
        # return dry_run_python_runner(idx, func_name)
        pass
    elif language == "Java":
        return dry_run_java_runner(idx, llm, func_name)
    elif language == "Go":
        return dry_run_go_runner(idx, llm, func_name)
    elif language == "TS":
        return dry_run_ts_runner(idx, func_name)
    elif language == "JS":
        return dry_run_js_runner(idx, func_name)
    
def run_python_runner(driver_path: str, func_name: str = "") -> Tuple[Optional[str], Optional[str], bool]:
    """
    运行python driver.py并解析测试结果
    
    返回:
        error_type: 错误类型（如有）
        error_msg: 错误信息（如有）
        passed: 是否所有测试都通过
    """
    original_dir = os.getcwd()
    try:
        # 切换到driver所在目录
        work_dir = os.path.dirname(os.path.abspath(driver_path))
        os.chdir(work_dir)
        
        command = [
            sys.executable, 
            os.path.basename(driver_path)
        ]
        
        logger.info(f"Running in {work_dir} with command: {' '.join(command)}")
        
        timeout_time = 300  # 增加到5分钟
        # 捕获完整输出
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_time
        )
        
        # 分析输出来判断测试是否通过
        output = result.stdout + result.stderr
        
        # 检查是否有失败的测试用例
        failed_tests = re.findall(r"Test case \d+ failed:", output)
        all_tests_passed = len(failed_tests) == 0
        
        # 检查是否运行了测试但没有输出结果（可能是格式问题）
        if not re.search(r"Test case \d+ (passed|failed)", output) and result.returncode == 0:
            logger.warning("No test results found in output, but process completed successfully")
            all_tests_passed = None  # 无法确定是否通过
        
        # 解析输出
        if result.returncode == 0 and all_tests_passed:
            logger.info("All tests passed successfully")
            return None, None, True
        elif result.returncode == 0 and all_tests_passed is None:
            logger.info("Process completed but test results unclear")
            return None, None, None
        else:
            error_summary = f"Failed tests: {len(failed_tests)}" if failed_tests else "Execution error"
            logger.error(f"{func_name} failed: {error_summary}")
            # 提取失败测试的详细信息
            error_details = "\n".join(re.findall(r"Test case \d+ failed:.*?Actual:.*?$", output, re.DOTALL | re.MULTILINE))
            if not error_details and result.stderr:
                error_details = result.stderr.strip()[-1000:]  # 增加到最后1000字符
            
            return "TestFailure" if failed_tests else "ExecutionError", error_details, False
    except subprocess.TimeoutExpired:
        logger.error("Execution timed out")
        return "TimeoutError", f"Test execution exceeded {timeout_time} seconds", False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "ExecutionError", str(e), False
    finally:
        os.chdir(original_dir)  # 恢复原始工作目录

def run_python_driver(driver_path: str, func_name: str = "") -> Tuple[Optional[str], Optional[str]]:
    # 执行python driver.py
    """运行python driver.py并解析测试结果"""
    original_dir = os.getcwd()
    try:
        # 切换到driver所在目录
        work_dir = os.path.dirname(os.path.abspath(driver_path))
        os.chdir(work_dir)
        
        command = [
            sys.executable, 
            os.path.basename(driver_path)
        ]
        
        logger.info(f"Running in {work_dir} with command: {' '.join(command)}")
        
        timeout_time = 120 # 之前设置120秒，结果第二个item直接超时了，花了121秒。运行了一个花了204秒
        # 捕获完整输出
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_time  # 增加超时时间
        )
        
        # 解析输出
        if result.returncode == 0:
            logger.info("Run succeeded")
            return None, None
        else:
            # error_type, error_msg = parse_error_output(result.stderr)
            # logger.error(f"{func_name} failed with {error_type}: {error_msg}")
            # return error_type, error_msg
            return "ExecutionError", result.stderr.strip()[-500:]  # 返回最后500字符防止信息过长
    except subprocess.TimeoutExpired:
        logger.error("execution timed out")
        return "TimeoutError", f"Test execution exceeded {timeout_time} seconds"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "ExecutionError", str(e)
    finally:
        os.chdir(original_dir)  # 恢复原始工作目录

def run_go_runner(driver_path: str, func_name: str = "") -> Tuple[Optional[str], Optional[str], bool]:
    """
    运行Go测试文件并解析测试结果
    
    返回:
        error_type: 错误类型（如有）
        error_msg: 错误信息（如有）
        passed: 是否所有测试都通过
    """
    original_dir = os.getcwd()
    try:
        # 切换到driver所在目录
        work_dir = os.path.dirname(os.path.abspath(driver_path))
        os.chdir(work_dir)
        
        # 构建Go测试命令
        command = [
            "go", "test", "-v"
        ]
        
        # if func_name:
        #     command.extend(["-run", f"^{func_name}$"])  # 只运行特定测试函数
        
        logger.info(f"Running Go test in {work_dir} with command: {' '.join(command)}")
        
        timeout_time = 120  # 外部进程超时时间
        env = os.environ.copy()
        env["GO111MODULE"] = "auto"  # 自动检测Go模块
        
        # 捕获完整输出
        result = subprocess.run(
            command,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_time
        )
        
        # 分析输出来判断测试是否通过
        output = result.stdout + result.stderr
        
        # 检查是否有失败的测试用例
        failed_tests = re.findall(r"Test case \d+ failed:", output)
        
        # 检查测试总结信息
        # test_summary_failed = re.search(r"FAIL*", output, re.MULTILINE)
        # test_summary_passed = re.search(r"PASS*", output, re.MULTILINE)
        
        # 判断是否所有测试通过
        if "exit status 1" not in output and result.returncode == 0:
            logger.info("All tests passed successfully")
            return None, None, True
        elif failed_tests or result.returncode != 0:
            error_summary = f"Failed tests: {len(failed_tests)}" if failed_tests else "Execution error"
            logger.error(f"{func_name} failed: {error_summary}")
            # 提取失败测试的详细信息
            error_details = "\n".join(re.findall(r"Test case \d+ failed:.*?Actual:.*?$", output, re.DOTALL | re.MULTILINE))
            if not error_details and result.stderr:
                error_details = result.stderr.strip()[-500:]  # 增加到最后1000字符
            
            return "TestFailure" if failed_tests else "ExecutionError", error_details, False
        else:
            logger.warning("No clear test results found in output")
            return None, None, None
    except subprocess.TimeoutExpired:
        logger.error("Execution timed out")
        return "TimeoutError", f"Test execution exceeded {timeout_time} seconds", False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "ExecutionError", str(e), False
    finally:
        os.chdir(original_dir)  # 恢复原始工作目录

def run_go_driver(driver_path: str, func_name: str) -> Tuple[Optional[str], Optional[str]]:
    """运行Go测试文件并解析测试结果"""
    original_dir = os.getcwd()
    try:
        # 切换到driver所在目录
        work_dir = os.path.dirname(os.path.abspath(driver_path))
        os.chdir(work_dir)
        
        # 构建Go测试命令
        # command = [
        #     "go", "test",
        #     "-v",  # 显示详细输出
        #     "-run", f"^{func_name}$",  # 只运行特定测试函数
        #     "-timeout", "60s",  # 设置Go测试超时
        #     os.path.basename(driver_path)
        # ]
        
        command = [
            "go", "test", "-v"
        ]
        
        logger.info(f"Running Go test in {work_dir} with command: {' '.join(command)}")
        
        timeout_time = 120  # 外部进程超时时间
        env = os.environ.copy()
        env["GO111MODULE"] = "auto"  # 自动检测Go模块
        
        # 捕获完整输出
        result = subprocess.run(
            command,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_time
        )
        
        # 解析输出
        if result.returncode == 0:
            logger.info("Go test succeeded")
            return None, None
        else:
            # error_type, error_msg = parse_go_test_output(result.stdout, result.stderr)
            # logger.error(f"Go test {func_name} failed with {error_type}: {error_msg}")
            # return error_type, error_msg
            logger.error(f"Go run failed with{result.returncode}: {result.stderr}")
            return "ExecutionError", result.stderr[-500:]  # 返回最后500字符防止信息过长
    except subprocess.TimeoutExpired:
        logger.error("Go test execution timed out")
        return "TimeoutError", f"Test execution exceeded {timeout_time} seconds"
    except Exception as e:
        logger.error(f"Unexpected error in Go test: {str(e)}")
        return "ExecutionError", str(e)
    finally:
        os.chdir(original_dir)  # 恢复原始工作目录
        
def run_java_runner(package_path: str, func_name: str = "") -> Tuple[Optional[str], Optional[str], bool]:
    """
    运行Java测试并解析测试结果
    
    返回:
        error_type: 错误类型（如有）
        error_msg: 错误信息（如有）
        passed: 是否所有测试都通过
    """
    original_dir = os.getcwd()
    try:
        # 切换到driver所在目录
        work_dir = package_path
        os.chdir(work_dir)
        
        command = ["mvn", "test"]
        
        logger.info(f"Running Java test in {work_dir} with command: {' '.join(command)}")
        
        timeout_time = 300  # 5分钟超时
        env = os.environ.copy()
        
        # 捕获完整输出
        result = subprocess.run(
            command,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_time
        )
        
        output = result.stdout + result.stderr
        
        # 检查编译错误
        if "[ERROR] COMPILATION ERROR" in output:
            logger.error("Java compilation failed")
            # 提取编译错误信息
            error_match = re.search(r"\[ERROR\] COMPILATION ERROR :\s*(.*?)\[INFO\]", output, re.DOTALL)
            error_msg = error_match.group(1).strip() if error_match else "Unknown compilation error"
            return "COMPILATION ERROR", error_msg[:-1000], False
        
        # 检查测试结果
        tests_passed = None
        test_summary = re.search(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+)", output)
        
        if test_summary:
            total = int(test_summary.group(1))
            failures = int(test_summary.group(2))
            errors = int(test_summary.group(3))
            tests_passed = (failures == 0) and (errors == 0)
            
            if not tests_passed:
                # 提取具体的测试错误信息，排除无用的Maven错误提示
                # 首先尝试提取具体的测试失败信息
                failure_details = re.search(r"Failed tests:(.*?)(?=\[INFO\]|$)", output, re.DOTALL)
                if failure_details:
                    error_msg = failure_details.group(1).strip()
                else:
                    # 查找失败的测试类和方法
                    test_failures = re.search(r"Tests in error:(.*?)(?=\[INFO\]|$)", output, re.DOTALL)
                    if test_failures:
                        error_msg = test_failures.group(1).strip()
                    else:
                        # 如果上面的都没找到，尝试查找最有意义的错误信息部分
                        error_section = re.search(r"Running .*?\n(.*?)(?=\[INFO\] Total time|$)", output, re.DOTALL)
                        if error_section:
                            error_msg = error_section.group(1).strip()
                        else:
                            # 最后的备用方案：过滤掉Maven相关的通用错误信息
                            error_lines = []
                            capture = False
                            for line in output.split('\n'):
                                # 开始捕获有意义内容
                                if "Results :" in line or "Running " in line:
                                    capture = True
                                    continue
                                
                                # 结束捕获无意义内容
                                if "[INFO] Total time:" in line or "[ERROR] Failed to execute" in line:
                                    capture = False
                                
                                # 只保留有意义的错误信息
                                if capture and line.strip() and not line.startswith("[INFO]") and not line.startswith("[ERROR] Please refer"):
                                    error_lines.append(line.strip())
                            
                            error_msg = "\n".join(error_lines) if error_lines else "Test failure without specific details"
                
                return "TEST FAILURE", error_msg[:-1000], False
        
        # 如果mvn test成功但没有测试结果输出
        if result.returncode == 0 and tests_passed is None:
            logger.warning("Process completed but no test results found")
            return None, None, None
        
        # 如果mvn test成功且测试通过
        if result.returncode == 0 and tests_passed:
            logger.info("All Java tests passed successfully")
            return None, None, True
        
        # 其他执行错误，过滤掉Maven标准错误消息
        logger.error(f"Java execution failed with return code {result.returncode}")
        
        # 过滤掉标准Maven错误消息
        error_lines = []
        for line in result.stderr.strip().split('\n'):
            if (line.startswith("[ERROR]") and 
                not any(skip in line for skip in [
                    "Failed to execute goal", 
                    "Please refer to", 
                    "To see the full stack trace", 
                    "Re-run Maven", 
                    "For more information",
                    "Help"
                ])):
                error_lines.append(line)
        
        error_msg = "\n".join(error_lines) if error_lines else "Execution failed without specific details"
        return "EXECUTION ERROR", error_msg[:-1000], False
        
    except subprocess.TimeoutExpired:
        logger.error("Java test execution timed out")
        return "TIMEOUT ERROR", f"Test execution exceeded {timeout_time} seconds", False
    except Exception as e:
        logger.error(f"Unexpected error in Java test: {str(e)}")
        return "EXECUTION ERROR", str(e), False
    finally:
        os.chdir(original_dir)  # 恢复原始工作目录

def run_java_driver(driver_path: str, func_name: str) -> Tuple[Optional[str], Optional[str]]:
    """运行Java测试文件并解析测试结果"""
    original_dir = os.getcwd()
    try:
        # 切换到driver所在目录
        work_dir = os.path.abspath(driver_path)
        os.chdir(work_dir)
        
        # 构建Go测试命令
        # command = [
        #     "go", "test",
        #     "-v",  # 显示详细输出
        #     "-run", f"^{func_name}$",  # 只运行特定测试函数
        #     "-timeout", "60s",  # 设置Go测试超时
        #     os.path.basename(driver_path)
        # ]
        
        command = [
            "mvn", "test"
        ]
        
        logger.info(f"Running Java test in {work_dir} with command: {' '.join(command)}")
        
        timeout_time = 120  # 外部进程超时时间
        env = os.environ.copy()
        env["GO111MODULE"] = "auto"  # 自动检测Go模块
        
        # 捕获完整输出
        result = subprocess.run(
            command,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_time
        )
        
        # 解析输出
        if result.returncode == 0:
            logger.info("Java test succeeded")
            return None, None
        else:
            # error_type, error_msg = parse_go_test_output(result.stdout, result.stderr)
            # logger.error(f"Go test {func_name} failed with {error_type}: {error_msg}")
            # return error_type, error_msg
            logger.error(f"Java run failed with{result.returncode}: {result.stderr}")
            return "ExecutionError", result.stderr[-500:]  # 返回最后500字符防止信息过长
    except subprocess.TimeoutExpired:
        logger.error("Java test execution timed out")
        return "TimeoutError", f"Test execution exceeded {timeout_time} seconds"
    except Exception as e:
        logger.error(f"Unexpected error in Go test: {str(e)}")
        return "ExecutionError", str(e)
    finally:
        os.chdir(original_dir)  # 恢复原始工作目录

def run_ts_driver(driver_path: str, func_name, idx: str) -> Tuple[Optional[str], Optional[str]]:
    original_dir = os.getcwd()
    try:
        # 切换到driver所在目录
        work_dir = os.path.abspath(driver_path)
        os.chdir(work_dir)

        print(work_dir)
        
        command = [
            "npx", "jest", f"./TS/{idx}/"
        ]
        
        logger.info(f"Running TS test in {work_dir} with command: {' '.join(command)}")
        
        timeout_time = 120  # 外部进程超时时间
        env = os.environ.copy()
        
        # 捕获完整输出
        result = subprocess.run(
            command,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_time
        )
        
        # 解析输出
        if result.returncode == 0:
            logger.info("TS test succeeded")
            return None, None
        else:
            # error_type, error_msg = parse_go_test_output(result.stdout, result.stderr)
            # logger.error(f"Go test {func_name} failed with {error_type}: {error_msg}")
            # return error_type, error_msg
            logger.error(f"TS run failed with{result.returncode}: {result.stderr}")
            return "ExecutionError", result.stderr[-500:]  # 返回最后500字符防止信息过长
    except subprocess.TimeoutExpired:
        logger.error("TS test execution timed out")
        return "TimeoutError", f"Test execution exceeded {timeout_time} seconds"
    except Exception as e:
        logger.error(f"Unexpected error in TS test: {str(e)}")
        return "ExecutionError", str(e)
    finally:
        os.chdir(original_dir)  # 恢复原始工作目录
        
def run_js_runner(driver_path: str, func_name: str = "") -> Tuple[Optional[str], Optional[str], bool]:
    """
    Runs JavaScript tests using Jest and parses the test results.
    
    Args:
        driver_path: Full path to the test file (e.g., '/data/.../JS/3/runner.test.js')
        func_name: Name of the function being tested (for logging)
    
    Returns:
        Tuple containing:
        - error_type: None if success, or error type string
        - error_msg: None if success, or error message
        - passed: Boolean indicating if all tests passed
    """
    original_dir = os.getcwd()
    try:
        # Extract directory and test file path components
        full_path = os.path.abspath(driver_path)
        test_dir = os.path.dirname(os.path.dirname(full_path))  # Gets the JS directory
        test_file = os.path.basename(full_path)
        test_subdir = os.path.basename(os.path.dirname(full_path))  # Gets the '3' part
        
        # Switch to the JS directory (parent of test file's directory)
        os.chdir(test_dir)
        
        command = [
            "npx",
            "jest",
            f"./{test_subdir}/{test_file}"  # e.g., ./3/runner.test.js
        ]
        
        logger.info(f"Running JS tests in {test_dir} with command: {' '.join(command)}")
        
        timeout_time = 120  # 2 minutes timeout
        env = os.environ.copy()
        
        # Capture full output
        result = subprocess.run(
            command,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_time
        )
        
        output = result.stdout + result.stderr
        
        # 解析测试结果
        if result.returncode == 0:
            # 检查输出中是否包含明确的成功信息
            if re.search(r"Test Suites: \d+ passed", output):
                logger.info("All tests passed successfully")
                return None, None, True
                
            # 成功执行但未找到测试结果（可能格式异常）
            if not re.search(r"Test Suites: \d+ (passed|failed)", output):
                logger.warning("No test results found in output, but process completed successfully")
                return None, None, None
                
        else:
            # 检查是否有具体的测试失败信息
            failed_test_blocks = re.findall(
                r"(● [^\n]+\n[\s\S]*?)(?=\n● |\nTest Suites|$)", 
                output
            )

            if failed_test_blocks:
                logger.error(f"Found {len(failed_test_blocks)} failed tests")
                
            #     # 提取关键错误信息并格式化
            #     error_details = []
            #     for block in failed_test_blocks[:3]:  # 最多显示前3个失败用例
            #         # 提取核心错误信息
            #         match = re.search(
            #             r"(Expected: [^\n]+)\n(Received: [^\n]+)\n\s+at (.+)", 
            #             block, 
            #             re.DOTALL
            #         )
            #         if match:
            #             error_summary = f"{match.group(1)}\n{match.group(2)}\nError location: {match.group(3)}"
            #         else:
            #             error_summary = block[:300]  # 截断显示前300字符
                        
            #         # 添加分隔标记
            #         error_details.append(f"▼ Failed Test ▼\n{error_summary}\n▲▲")
                
            #     # 组合错误信息（总长度控制在1000字符内）
            #     full_error = "\n\n".join(error_details)
            #     full_error += f"\n\n[Last 500 characters of output]\n{output[-250:]}"
                full_error = output.strip()
                return "TestFailure", full_error, False
            
            # 执行错误
            error_details = result.stderr.strip()[-500:] if result.stderr else output[-500:]
            logger.error(f"Execution error: {error_details}")
            return "ExecutionError", error_details, False
            
        return None, None, True
                
    except subprocess.TimeoutExpired:
        logger.error("JS test execution timed out")
        return "TimeoutError", f"Test execution exceeded {timeout_time} seconds", False
    except Exception as e:
        logger.error(f"Unexpected error in JS test: {str(e)}")
        return "ExecutionError", str(e), False
    finally:
        os.chdir(original_dir)

def run_js_driver(driver_path: str, func_name, idx: str) -> Tuple[Optional[str], Optional[str]]:
    original_dir = os.getcwd()
    try:
        # 切换到driver所在目录
        work_dir = os.path.abspath(driver_path)
        os.chdir(work_dir)

        print(work_dir)
        
        command = [
            "npx", "jest", f"./JS/{idx}/"
        ]
        
        logger.info(f"Running JS test in {work_dir} with command: {' '.join(command)}")
        
        timeout_time = 120  # 外部进程超时时间
        env = os.environ.copy()
        
        # 捕获完整输出
        result = subprocess.run(
            command,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_time
        )
        
        # 解析输出
        if result.returncode == 0:
            logger.info("JS test succeeded")
            return None, None
        else:
            # error_type, error_msg = parse_go_test_output(result.stdout, result.stderr)
            # logger.error(f"Go test {func_name} failed with {error_type}: {error_msg}")
            # return error_type, error_msg
            logger.error(f"JS run failed with{result.returncode}: {result.stderr}")
            return "ExecutionError", result.stderr[-500:]  # 返回最后500字符防止信息过长
    except subprocess.TimeoutExpired:
        logger.error("JS test execution timed out")
        return "TimeoutError", f"Test execution exceeded {timeout_time} seconds"
    except Exception as e:
        logger.error(f"Unexpected error in JS test: {str(e)}")
        return "ExecutionError", str(e)
    finally:
        os.chdir(original_dir)  # 恢复原始工作目录

def parse_go_test_output(stdout: str, stderr: str) -> Tuple[str, str]:
    """解析Go测试输出"""
    if "--- FAIL" in stdout:
        # 提取失败的测试信息
        fail_lines = [line for line in stdout.splitlines() if line.startswith("--- FAIL")]
        error_msg = "\n".join(fail_lines)
        return "TestFailure", error_msg
    
    if "panic: " in stderr:
        # 处理panic情况
        panic_msg = stderr.split("panic: ")[1].split("\n")[0]
        return "PanicError", f"panic: {panic_msg}"
    
    if "build failed" in stderr:
        # 编译错误
        build_errors = "\n".join([line for line in stderr.splitlines() if "error:" in line])
        return "CompileError", build_errors
    
    # 默认返回原始错误输出
    return "UnknownError", stderr if stderr else stdout  
        
def parse_error_output(stderr: str) -> Tuple[str, str]:
    """
    解析错误输出，提取错误类型和错误信息。
    
    :param stderr: 标准错误输出
    :return: 错误类型和错误信息
    """
    # 定义常见的错误模式
    error_patterns = {
        "SyntaxError": r"SyntaxError: (.*)",
        "ImportError": r"ImportError: (.*)",
        "AssertionError": r"AssertionError: (.*)",
        "TypeError": r"TypeError: (.*)",
        "ValueError": r"ValueError: (.*)",
        "AttributeError": r"AttributeError: (.*)",
        "NameError": r"NameError: (.*)",
        "ModuleNotFoundError": r"ModuleNotFoundError: (.*)",
        "IndexError": r"IndexError: (.*)",
        "KeyError": r"KeyError: (.*)",
        "ZeroDivisionError": r"ZeroDivisionError: (.*)",
        "IndentationError": r"IndentationError: (.*)",
    }
    
    if not stderr:
        return "UnknownError", "No error message found"
    
    # 按行解析错误输出
    for line in reversed(stderr.split("\n")):  # 从最后一行开始检查
        for err_type, pattern in error_patterns.items():
            match = re.search(pattern, line)
            if match:
                return err_type, match.group(1).strip()
    
    # 如果没有匹配到已知错误类型，返回未知错误
    return "UnknownError", stderr.strip() or "No specific error message found"
 

if __name__ == "__main__":
    pass
    