
import json
import os
import time
from abc import ABC, abstractmethod
from typing import Tuple, Optional

from code2bench.config import config
from code2bench.llm.llm_caller import call_llm
from code2bench.llm.qwen_llm import QwenLLM
from code2bench.prompt.benchmark_runner import DEFAULT_PROMPT, GO_PROMPT, TS_PROMPT, JS_PROMPT, JAVA_PROMPT, WEAKLY_PROMPT
from code2bench.test_runner.dry_run import (
    run_go_runner, run_pytest, run_python_runner, run_js_runner, run_java_runner
)
from code2bench.utils.go import extract_function_name, parse_go_test_results, rename_duplicate_types
from code2bench.utils.ts import extract_ts_function_name, parse_ts_jest_test_results
from code2bench.utils.java import parse_java_test_failures
from code2bench.utils.helper import get_statistic_path, get_running_status_path
from code2bench.utils.json_utils import clean_response_content, load_json, save_json
from code2bench import logger
from code2bench.utils.python import get_func_name, parse_python_test_failures


class BaseBenchmarkRunner(ABC):
    def __init__(self, llm, benchmark_path: str):
        self.llm = llm
        self.benchmark_path = benchmark_path
    
    def run_item(self, item_path: str, **kwargs) -> Tuple[bool, Optional[str], Optional[str]]:
        try:
            system_message, user_message = self.prepare_llm_input(item_path)
            
            llm_output = call_llm(self.llm, system_message=system_message, user_message=user_message)
            if not self.validate_response(item_path=item_path, llm_output=llm_output):
                return False, "ValidationError", "Response validation failed"
            
            test_result = self.evaluate_llm_output(llm_output, item_path)
            if test_result[0] is True:
                return True, None, None
            return test_result
            
        except Exception as e:
            import traceback
            logger.error(f"Exception in run_item {item_path}: {traceback.format_exc()}")
            logger.warning(f"Error in run_item {item_path}: {e}")
            return False, "RuntimeError", str(e)
    
    @abstractmethod
    def prepare_llm_input(self, item_path: str) -> Tuple[str, str]:
        """准备给LLM的输入"""
        pass
    
    @abstractmethod
    def validate_response(self, llm_output: str, item_path: str) -> bool:
        """验证LLM的响应是否符合要求（格式/基础检查）"""
        pass
    
    @abstractmethod
    def evaluate_llm_output(self, llm_output: str, item_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """评估LLM输出是否正确（实际测试逻辑）"""
        pass
    

class CodeGenerationRunner(BaseBenchmarkRunner):
    def __init__(self, llm, benchmark_path: str):
        super().__init__(llm, benchmark_path)

    def prepare_llm_input(self, item_path: str) -> str:
        with open(os.path.join(item_path, "instruction.txt"), "r") as f:
            user_message = f.read()
        return DEFAULT_PROMPT, user_message
    
    def validate_response(self, llm_output: str, item_path: str) -> bool:
        return "def " in llm_output and "\n" in llm_output
    
    def evaluate_llm_output(self, llm_output: str, item_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
        tested_path = os.path.join(item_path, "tested.py")
        llm_output = clean_response_content(llm_output)
        with open(tested_path, "w") as f:
            f.write(llm_output)
        
        runner_path = os.path.join(item_path, "runner.py")

        error_type, error_msg, passed = run_python_runner(runner_path)
        if passed is True:
            print("所有测试通过了！")
        elif passed is None:
            print("测试结果不明确")
        else:
            print(f"测试失败。错误类型: {error_type}, 错误信息: {error_msg}")
        return passed, error_type, error_msg
    

class GoCodeGenerationRunner(CodeGenerationRunner):
    def __init__(self, llm, benchmark_path: str):
        super().__init__(llm, benchmark_path)
    
    def prepare_llm_input(self, item_path: str) -> str:
        """从instruction.txt读取问题描述"""
        with open(os.path.join(item_path, "instruction.txt"), "r") as f:
            user_message = f.read()
        return GO_PROMPT, user_message
    
    def validate_response(self, llm_output: str, item_path: str) -> bool:
        """验证是否生成了有效的Go代码"""
        return True
        
    def evaluate_llm_output(self, llm_output: str, item_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """针对Go代码的评估逻辑"""
        
        runner_path = os.path.join(item_path, "runner_test.go")
        with open(runner_path, "r") as f:
            runner_content = f.read()
        
        # 保存生成的代码
        tested_path = os.path.join(item_path, "tested.go")
        with open(tested_path, "w") as f:
            f.write(llm_output)
        
        # 运行测试
        func_name = extract_function_name(llm_output)
        error_type, error_msg, passed = run_go_runner(runner_path, func_name=func_name)
        # 检查结果
        if passed is True:
            print("所有测试通过了！")
        elif passed is None:
            print("测试结果不明确")
        else:
            print(f"测试失败。错误类型: {error_type}, 错误信息: {error_msg}")
        return passed, error_type, error_msg

class JavaCodeGenerationRunner(CodeGenerationRunner):
    def __init__(self, llm, benchmark_path: str):
        super().__init__(llm, benchmark_path)
    
    def prepare_llm_input(self, item_path: str) -> str:
        """从instruction.txt读取问题描述"""
        with open(os.path.join(item_path, "instruction.txt"), "r") as f:
            user_message = f.read()
        return JAVA_PROMPT, user_message
    
    def validate_response(self, llm_output: str, item_path: str) -> bool:
        """验证是否生成了有效的Java代码"""
        return True
        
    def evaluate_llm_output(self, llm_output: str, item_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """针对Java代码的评估逻辑"""
        # 保存生成的代码
        idx = os.path.basename(item_path)
        tested_path = os.path.join(item_path, f"src/main/java/{idx}/Tested.java")
        with open(tested_path, "w") as f:
            f.write(llm_output)
        
        # 运行测试
        # runner_path = os.path.join(item_path, f"src/test/java/Tester.java")
        error_type, error_msg, passed = run_java_runner(item_path)
        # 检查结果
        if passed is True:
            print("所有测试通过了！")
        elif passed is None:
            print("测试结果不明确")
        else:
            print(f"测试失败。错误类型: {error_type}, 错误信息: {error_msg}")
        return passed, error_type, error_msg
    
    
class TSCodeGenerationRunner(CodeGenerationRunner):
    def __init__(self, llm, benchmark_path: str):
        super().__init__(llm, benchmark_path)
    
    def prepare_llm_input(self, item_path: str) -> str:
        """从instruction.txt读取问题描述"""
        with open(os.path.join(item_path, "instruction.txt"), "r") as f:
            user_message = f.read()
        return TS_PROMPT, user_message
    
    def validate_response(self, llm_output: str, item_path: str) -> bool:
        """验证是否生成了有效的TS代码"""
        return True
        
    def evaluate_llm_output(self, llm_output: str, item_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """针对TS代码的评估逻辑"""
        # 保存生成的代码
        tested_path = os.path.join(item_path, "tested.ts")
        with open(tested_path, "w") as f:
            f.write(llm_output)
        
        # 运行测试
        func_name = extract_ts_function_name(llm_output)
        # idx = os.path.basename(item_path)
        # runner_path = os.path.dirname(item_path)
        # error_type, error_msg = run_ts_driver(runner_path, func_name, idx)
        # return (not bool(error_type)), error_type, error_msg
        # idx = os.path.basename(item_path)
        # runner_path = os.path.dirname(item_path)
        runner_path = os.path.join(item_path, "runner.test.ts")
        error_type, error_msg, passed = run_js_runner(runner_path, func_name=func_name)
        # 检查结果
        if passed is True:
            print("所有测试通过了！")
        elif passed is None:
            print("测试结果不明确")
        else:
            print(f"测试失败。错误类型: {error_type}, 错误信息: {error_msg}")
        return passed, error_type, error_msg
    

class JSCodeGenerationRunner(CodeGenerationRunner):
    def __init__(self, llm, benchmark_path: str):
        super().__init__(llm, benchmark_path)
    
    def prepare_llm_input(self, item_path: str) -> str:
        """从instruction.txt读取问题描述"""
        with open(os.path.join(item_path, "instruction.txt"), "r") as f:
            user_message = f.read()
        return JS_PROMPT, user_message
    
    def validate_response(self, llm_output: str, item_path: str) -> bool:
        """验证是否生成了有效的JS代码"""
        return True
        
    def evaluate_llm_output(self, llm_output: str, item_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """针对JS代码的评估逻辑"""
        # 保存生成的代码
        tested_path = os.path.join(item_path, "tested.js")
        with open(tested_path, "w") as f:
            f.write(llm_output)
        
        # 运行测试
        func_name = extract_ts_function_name(llm_output)
        # idx = os.path.basename(item_path)
        # runner_path = os.path.dirname(item_path)
        runner_path = os.path.join(item_path, "runner.test.js")
        error_type, error_msg, passed = run_js_runner(runner_path, func_name=func_name)
        # 检查结果
        if passed is True:
            print("所有测试通过了！")
        elif passed is None:
            print("测试结果不明确")
        else:
            print(f"测试失败。错误类型: {error_type}, 错误信息: {error_msg}")
        return passed, error_type, error_msg


class WeaklyTypedCodeRunner(CodeGenerationRunner):
    def prepare_llm_input(self, item_path: str) -> Tuple[str, str]:
        """针对 weakly 类型的输入准备逻辑"""
        with open(os.path.join(item_path, "instruction.txt"), "r") as f:
            instruction = f.read()
        system_message = WEAKLY_PROMPT
        return system_message, instruction

def get_runner_class() -> BaseBenchmarkRunner:
    if config.BENCHMARK_NAME == "Python":
        return CodeGenerationRunner
    elif config.BENCHMARK_NAME == "weakly":
        # return WeaklyTypedCodeRunner
        return CodeGenerationRunner
    elif config.BENCHMARK_NAME == "Go":
        return GoCodeGenerationRunner
    elif config.BENCHMARK_NAME == "TS":
        return TSCodeGenerationRunner
    elif config.BENCHMARK_NAME == "JS":
        return JSCodeGenerationRunner
    elif config.BENCHMARK_NAME == "Java":
        return JavaCodeGenerationRunner
    else:
        raise ValueError(f"Unsupported benchmark type")

def generate_tested(llm, instruction: str, tested_path: str):
    """Call the LLM to generate the tested.py file.
    """
    prompt = DEFAULT_PROMPT
    response = call_llm(llm, system_message=prompt, user_message=instruction)
    
    try:
        code = clean_response_content(response)
        with open(tested_path, "w") as f:
            f.write(code)
        logger.info(f"Generated tested.py file: {tested_path}")
        # tested_path: /path/to/benchmark/default/1/tested.py
        # logging it，记录到/path/to/benchmark/test/default/{llm}/1/tested.py
        llm_tested_path = tested_path.replace("benchmark", f"benchmark/test/{llm}")
        if not os.path.exists(os.path.dirname(llm_tested_path)):
            os.makedirs(os.path.dirname(llm_tested_path))
        with open(llm_tested_path, "w") as f:
            f.write(code)
        logger.info(f"Generated tested.py file for {llm}: {llm_tested_path}")
    except Exception as e:
        logger.exception(f"Error cleaning response content: {e}")
        
def utc_time_to_beijing_time():
    """
    将当前UTC时间转换为北京时间并返回格式化后的时间字符串
    """
    utc_time_stamp = time.time()
    # beijing_struct_time = time.localtime(utc_time_stamp + 8 * 3600)
    beijing_struct_time = time.localtime(utc_time_stamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", beijing_struct_time)
        
def run_item(llm, item_path: str) -> Tuple[bool, Optional[str], Optional[str]]:
    # Load the benchmark data
    # item_path = "benchmark/default/1"

    groundtruth_path = os.path.join(item_path, "groundtruth.py")
    instruction_path = os.path.join(item_path, "instruction.txt")
    tested_path = os.path.join(item_path, "tested.py")
    logger.info(f"Running benchmark in {item_path} for {llm}")

    # Load the instruction
    with open(instruction_path, "r") as f:
        instruction = f.read()
    
    # Generate the tested.py file
    generate_tested(llm, instruction, tested_path)
    
    # Get the function name
    func_name = get_func_name(tested_path)
    if func_name is None:
        logger.error("Cannot find the function name in the tested.py file.")
        return False, "FunctionNameError", "Cannot find the function name in the tested.py file."
    
    # Run the benchmark
    driver_path = os.path.join(item_path, "driver.py")
    error_type, error_msg = run_pytest(driver_path)
    
    error_msg = error_msg[-300:] if error_msg else None # Truncate the error message to avoid too long messages
    if error_type:
        logger.error(f"Error type: {error_type}, Error message: {error_msg}")
        return False, error_type, error_msg
    else:
        logger.info("Benchmark passed successfully.")
        return True, None, None

def run_benchmark(llm, benchmark_path: str, limited: float = 0, use_ckpt: bool = True):
    """Run the benchmark for the given LLM and benchmark path."""
    
    statistics_path = os.path.join(benchmark_path, "statistics.json")
    # 确保LLM目录存在
    llm_dir = os.path.join(benchmark_path, str(llm))
    os.makedirs(llm_dir, exist_ok=True)
    running_status_path = os.path.join(llm_dir, "running_status.json")
    
    runner_cls = get_runner_class()
    runner = runner_cls(llm=llm, benchmark_path=benchmark_path)
    
    # 预先筛选出纯数字命名的目录，并按数字大小排序
    items = []
    for item in os.listdir(benchmark_path):
        if config.BENCHMARK_NAME == "Java":
            if item.startswith("p") and item[1:].isdigit() and os.path.isdir(os.path.join(benchmark_path, item)):
                items.append(item)
        else:
            # 其他语言的目录名是纯数字
            if item.isdigit() and os.path.isdir(os.path.join(benchmark_path, item)):
                items.append(item)

    # 按照数字值排序，而不是字符串排序
    if config.BENCHMARK_NAME == "Java":
        items = sorted(items, key=lambda x: int(x[1:]))
    else:
        items = sorted(items, key=int)
    
    tot = 0
    error = 0
    success = 0
    running_status = {}
    
    # 初始化或加载现有状态
    if os.path.exists(running_status_path) and use_ckpt:
        running_status_data = load_json(file_path=running_status_path)
        if str(llm) in running_status_data and running_status_data[str(llm)]:
            # 获取最新的运行状态
            running_status = running_status_data[str(llm)][-1]
    else:
        running_status_data = {str(llm): []}
    
    # 获取已完成的项目集合
    completed_items = set(running_status.keys())
    
    is_first_run = True
    is_first_run_statistic = True
    for item in items:
        # 如果这个测试项已经完成，跳过
        if item in completed_items:
            logger.info(f"Item {item} already completed, skipping...")
            # 更新统计数据
            if running_status[item].get("Status") is True:
                success += 1
            else:
                error += 1
            tot += 1
            continue
            
        if limited:
            time.sleep(limited)
            
        item_path = os.path.join(benchmark_path, item)
        tot += 1
        logger.info(f"Running item {item} ({tot}/{len(items)})...")
        
        # 运行测试项
        status, error_type, error_msg = runner.run_item(item_path)
        if status is False:
            error += 1
        else:
            success += 1
        
        if config.BENCHMARK_NAME == "Python":
            if error_msg:
                failures_status = parse_python_test_failures(error_msg)
                running_status[item] = {
                    "Status": status,
                    "Error Type": error_type,
                    "Error Message": error_msg[-300:] if error_msg else None,
                    "Failures": failures_status
                }
            else:
                running_status[item] = {
                    "Status": status,
                    "Error Type": error_type,
                    "Error Message": error_msg[-300:] if error_msg else None,
                }
        elif config.BENCHMARK_NAME == "Java":
            if error_msg:
                failures_status = parse_java_test_failures(error_msg)
                running_status[item] = {
                    "Status": status,
                    "Error Type": error_type,
                    "Error Message": error_msg[-1000:] if error_msg else None,
                    "Failures": failures_status
                }
            else:
                running_status[item] = {
                    "Status": status,
                    "Error Type": error_type,
                    "Error Message": error_msg[-1000:] if error_msg else None,
                }
        elif config.BENCHMARK_NAME == "Go":
            if error_msg:
                failures_status = parse_go_test_results(error_msg)
                running_status[item] = {
                    "Status": status,
                    "Error Type": error_type,
                    "Error Message": error_msg[-300:] if error_msg else None,
                    "Failures": failures_status
                }
            else:
                running_status[item] = {
                    "Status": status,
                    "Error Type": error_type,
                    "Error Message": error_msg[-300:] if error_msg else None,
                }
        elif config.BENCHMARK_NAME == "TS" or config.BENCHMARK_NAME == "JS":
            if error_msg:
                failures_status = parse_ts_jest_test_results(error_msg)
                running_status[item] = {
                    "Status": status,
                    "Error Type": error_type,
                    "Error Message": error_msg[-300:] if error_msg else None,
                    "Failures": failures_status
                }
            else:
                running_status[item] = {
                    "Status": status,
                    "Error Type": error_type,
                    "Error Message": error_msg[-300:] if error_msg else None,
                }
        else:
            # 更新运行状态
            running_status[item] = {
                "Status": status,
                "Error Type": error_type,
                "Error Message": error_msg[-300:] if error_msg else None,
            }
        
        # 每次运行完一个测试项就保存一次状态
        if str(llm) not in running_status_data:
            running_status_data[str(llm)] = []

        # 如果第一次运行或没有状态，添加新状态
        if not running_status_data[str(llm)]:
            running_status_data[str(llm)].append(running_status)
        else:
            # 否则更新最新的状态
            running_status_data[str(llm)][-1] = running_status
        save_json(running_status_path, running_status_data)
        logger.info(f"Updated running status after item {item}")
        
        # 同时更新统计数据
        current_statistics = {
            "Total": tot,
            "Success": success,
            "Error": error,
            "Success Rate": success / tot if tot > 0 else 0,
            "Time": utc_time_to_beijing_time(),
            "Completed": len(running_status)
        }
        
        if os.path.exists(statistics_path):
            statistics = load_json(file_path=statistics_path)
            if "Statistics" not in statistics:
                statistics["Statistics"] = [{}]
            if str(llm) not in statistics["Statistics"][0]:
                statistics["Statistics"][0][str(llm)] = []
            
            # 更新最新的统计
            if statistics["Statistics"][0][str(llm)]:
                # 如果是第一次运行, 也需要append
                if is_first_run_statistic:
                    statistics["Statistics"][0][str(llm)].append(current_statistics)
                    is_first_run_statistic = False
                else:
                    # 更新最新的统计
                    statistics["Statistics"][0][str(llm)][-1] = current_statistics
            else:
                statistics["Statistics"][0][str(llm)].append(current_statistics)
        else:
            statistics = {
                "Statistics": [
                    {str(llm): [current_statistics]}
                ]
            }
            
        save_json(statistics_path, statistics)
        logger.info(f"Updated statistics after item {item}: Total={tot}, Success={success}, Error={error}")
            
    # 最终日志记录
    logger.info(f"{config.BENCHMARK_NAME} Benchmark complete! Total: {tot}, Success: {success}, Error: {error} for {llm}")
    
def batch_run_runners(benchmark_path: str, llm, limited: bool = False):
    statistics_path = get_statistic_path()
    running_status_path = get_running_status_path()
    
    statistics_path = os.path.join(benchmark_path, "statistics.json")
    running_status_path = os.path.join(benchmark_path, "running_status.json")
    
    runner_cls = get_runner_class()
    runner = runner_cls(llm=llm, benchmark_path=benchmark_path)
    
    tot = 0
    error = 0
    success = 0
    running_status = {}
    items = sorted(os.listdir(benchmark_path))
    for item in items:
        if limited:
            time.sleep(0.5)
        item_path = os.path.join(benchmark_path, item)
        if os.path.isdir(item_path):
            tot += 1
            status, error_type, error_msg = run_python_runner(item_path)
            if status is True:
                success += 1
            else:
                error += 1
            if error_type and error_msg:
                running_status[item] = {
                    "Status": status,
                    "Error Type": error_type,
                    "Error Message": error_msg[-300:] if error_msg else None
                }
            
    logger.info(f"Total: {tot}, Success: {success}, Error: {error} for {llm}")

    if not os.path.exists(statistics_path):
        statistics = {
            "Total": tot,
            "Success": success,
            "Error": error,
            "Success Rate": success / tot,
            # "Time": time.time()
            "Time": utc_time_to_beijing_time()
        }
        save_json(statistics_path, {
            "Statistics": [
                {f"{llm}": [statistics]}
            ]
        })
    else:
        statistics = load_json(file_path=statistics_path)
        if str(llm) not in statistics["Statistics"][0]:
            statistics["Statistics"][0][f"{str(llm)}"] = []
        statistics["Statistics"][0][f"{str(llm)}"].append({
            "Total": tot,
            "Success": success,
            "Error": error,
            "Success Rate": success / tot,
            # "Time": time.time()
            "Time": utc_time_to_beijing_time()
        })
        save_json(statistics_path, statistics)
    logger.info(f"Statistics saved successfully.")
    
    if os.path.exists(running_status_path):
        running_status_data = load_json(file_path=running_status_path)
        if str(llm) not in running_status_data:
            running_status_data[str(llm)] = []
        running_status_data[str(llm)].append(running_status)
    else:
        running_status_data = {
            str(llm): [running_status]
        }
    save_json(running_status_path, running_status_data)
    logger.info(f"Running status saved successfully.")
    
if __name__ == "__main__":
    
    # config.BENCHMARK_NAME = "weakly"
    # config.BENCHMARK_NAME = "Python"
    # config.BENCHMARK_NAME = "Go"
    # config.BENCHMARK_NAME = "JS"
    config.BENCHMARK_NAME = "TS"
    # config.BENCHMARK_NAME = "Java"
    
    print("Config benchmark name:", config.BENCHMARK_NAME)

    llm_client = QwenLLM()
    run_benchmark(llm=llm_client, benchmark_path=config.BENCHMARK_PATH, use_ckpt=False)



