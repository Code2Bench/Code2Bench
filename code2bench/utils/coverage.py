import os
import subprocess

from typing import Optional, Tuple, Union
from code2bench import logger
from code2bench.utils.file_utils import format_missing_code_to_string, get_missing_branch_code
from code2bench.utils.json_utils import load_json


def get_coverage(driver_path: str) -> Tuple[Optional[str], Optional[str]]:
    """运行 coverage.py 并解析测试结果"""
    original_dir = os.getcwd()
    try:
        # 切换到 driver 所在目录
        work_dir = os.path.dirname(os.path.abspath(driver_path))
        os.chdir(work_dir)
        
        # 构造 coverage 命令
        command = [
            "coverage", "run", "--branch", "-m", "pytest", os.path.basename(driver_path)
        ]
        
        logger.info(f"Running in {work_dir} with command: {' '.join(command)}")
        
        timeout_time = 600  # 设置超时时间为 120 秒
        
        # 捕获完整输出
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout_time
        )
        
        # 检查测试是否成功
        if result.returncode == 0:
            logger.info("Tests succeeded")
            
            # 生成 JSON 覆盖率报告
            coverage_command = ["coverage", "json"]
            coverage_result = subprocess.run(
                coverage_command,
                capture_output=True,
                text=True,
                timeout=30  # 覆盖率生成通常较快，设置较短超时时间
            )
            
            if coverage_result.returncode != 0:
                logger.error(f"Failed to generate coverage report: {coverage_result.stderr}")
                return "CoverageError", coverage_result.stderr.strip()[-500:]
            
            logger.info("Coverage report generated successfully")
            return None, None
        elif result.returncode == 1:
            # 测试失败，返回错误信息
            error_message = result.stdout.strip()[-500:]  # 截取最后 500 字符防止过长
            logger.error(f"Tests failed with error: {error_message}")
            return "TestFailure", error_message or result.stderr.strip()[-500:] or "Test failed."
        else:
            # 测试失败，返回错误信息
            error_message = result.stderr.strip()[-500:]  # 截取最后 500 字符防止过长
            logger.error(f"Tests failed with error: {error_message}")
            return "TestFailure", error_message or result.stdout.strip()[-500:] or "Test failed."
    except subprocess.TimeoutExpired:
        logger.error("Execution timed out")
        return "TimeoutError", f"Test execution exceeded {timeout_time} seconds"
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return "ExecutionError", str(e)
    finally:
        # 恢复原始工作目录
        os.chdir(original_dir)
        
def get_coverage_report(driver_path: str) -> Tuple[Optional[str], Optional[str]]:
    """获取覆盖率报告"""
    # 运行测试并获取结果
    error_type, error_message = get_coverage(driver_path)
    
    if error_type is not None:
        return error_type, error_message
    
    # 读取 JSON 覆盖率报告
    coverage_json_path = os.path.join(os.path.dirname(driver_path), "coverage.json")
    
    if not os.path.exists(coverage_json_path):
        logger.error(f"Coverage report not found: {coverage_json_path}")
        return "CoverageReportError", "Coverage report not found"
    
    coverage_data = load_json(coverage_json_path)
    
    return None, coverage_data

def is_function_fully_covered(driver_path: str, func_name: str) -> Tuple[Union[str, bool], str]:
    """获取指定函数的覆盖率"""
    # get_coverage_report 函数返回的覆盖率数据
    error_type, coverage_data = get_coverage_report(driver_path)
    if error_type is not None:
        return error_type, coverage_data

    # 解析 JSON 数据
    missing_branches = coverage_data['files']['testcase_generator.py']['functions'][func_name]['missing_branches']
    if missing_branches:
        logger.info(f"Function {func_name} is not fully covered: {missing_branches}")
        missing_code = format_missing_code_to_string(
            get_missing_branch_code(missing_branches=missing_branches, file_path=driver_path))
        return False, f"{func_name} is not fully covered. Missing branches: {missing_code}"
    else:
        logger.info(f"Function {func_name} is fully covered")
        return True, "Function is fully covered"
    

if __name__ == "__main__":
    # 示例用法
    driver_path = ""
    func_name = "_get_correct_indent_level"
    
    status, message = is_function_fully_covered(driver_path, func_name)
    if status is not True:
        print(f"Error: {status}, Message: {message}")
    else:
        print(f"Coverage result: {message}")