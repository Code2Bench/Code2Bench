
import os
from pathlib import Path
from typing import Dict, List

from code2bench.utils.json_utils import load_json

def copy_file(src: str, dst: str):
    try:
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        import shutil
        shutil.copyfile(src, dst)
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False
    
def load_testcases(driver_path: str) -> List[Dict]:
    testcases_path = Path(driver_path).parent / "test_cases" / "test_cases.json"
    return load_json(testcases_path)

def load_reasoning_testcases(driver_path: str) -> List[Dict]:
    # path = driver_path.replace("Python", "reasoning")
    reasoning_testcases_path = Path(driver_path).parent / "test_cases" / "reasoning_testcases.json"
    return load_json(reasoning_testcases_path)

def get_benchmark_num_of_functions(benchmark_path: str) -> int:
    """
    Get the number of functions in the benchmark.
    :param benchmark_path: The path to the benchmark.
    :return: The number of functions in the benchmark.
    """
    return len([name for name in os.listdir(benchmark_path) if os.path.isdir(os.path.join(benchmark_path, name))])

def get_benchmark_max_function_num(benchmark_path: str) -> int:
    """
    Get the maximum function number in the benchmark.
    :param benchmark_path: The path to the benchmark.
    :return: The maximum function number in the benchmark.
    """
    return max([int(name) for name in os.listdir(benchmark_path) if os.path.isdir(os.path.join(benchmark_path, name))])

def get_missing_branch_code(missing_branches: list, file_path: str) -> dict:
    """
    根据未覆盖的分支信息和文件路径，返回对应的代码行。
    
    :param missing_branches: 未覆盖的分支信息，例如 [[44, 49]]
    :param file_path: 文件路径
    :return: 包含未覆盖分支代码的字典，键为分支范围，值为对应的代码行
    """
    missing_code = {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for branch in missing_branches:
            start_line, end_line = branch
            if start_line < 1 or end_line > len(lines):
                raise ValueError(f"Invalid line range: {start_line}-{end_line}")

            code_lines = [line.rstrip("\n") for line in lines[start_line - 1:end_line]]
            missing_code[f"{start_line}-{end_line}"] = code_lines

    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return missing_code

def format_missing_code_to_string(missing_code: dict) -> str:
    """
    将未覆盖分支的代码字典格式化为字符串。
    
    :param missing_code: 包含未覆盖分支代码的字典，键为分支范围，值为对应的代码行列表
    :return: 格式化后的字符串
    """
    result_string = ""

    for range_key, code_lines in missing_code.items():
        result_string += f"Branch Range: {range_key}\n"
        result_string += "Code:\n"
        result_string += "\n".join(code_lines) + "\n\n"

    return result_string.strip()