import os
import re
from typing import Dict
from code2bench.config import config
from code2bench.data_model import FuncType
from code2bench.utils.json_utils import load_json

def get_index_dicts() -> tuple:
    if config.MODE == FuncType.SELF_CONTAINED:
        benchmark_index_path = config.BENCHMARK_INDEX_PATH
        benchmark_skip_path = config.BENCHMARK_SKIP_PATH
    elif config.MODE == FuncType.LEVEL_SELF_CONTAINED:
        benchmark_index_path = config.BENCHMARK_LEVEL_INDEX_PATH
        benchmark_skip_path = config.BENCHMARK_LEVEL_SKIP_PATH
    elif config.MODE == FuncType.WEAKLY_SELF_CONTAINED:
        benchmark_index_path = config.BENCHMARK_WEAKLY_INDEX_PATH
        benchmark_skip_path = config.BENCHMARK_WEAKLY_SKIP_PATH
    else:
        raise ValueError(f"Unsupported mode: {config.MODE}")
    
    return benchmark_index_path, benchmark_skip_path

def get_func_list():
    if config.MODE == FuncType.SELF_CONTAINED:
        if os.path.exists(config.FILTERED_SELF_COTAINED_PATH):
            func_list = load_json(config.FILTERED_SELF_COTAINED_PATH)
        else:
            func_list = []
    elif config.MODE == FuncType.LEVEL_SELF_CONTAINED:
        if os.path.exists(config.ONE_LEVEL_SELF_CONTAINED_PATH):
            func_list = load_json(config.ONE_LEVEL_SELF_CONTAINED_PATH)
        else:
            func_list = []
    elif config.MODE == FuncType.WEAKLY_SELF_CONTAINED:
        if os.path.exists(config.WEAKLY_SELF_COTAINED_PATH):
            func_list = load_json(config.WEAKLY_SELF_COTAINED_PATH)
        else:
            func_list = []
    else:
        raise ValueError(f"Unsupported mode: {config.MODE}")
    return func_list or []
    
def get_statistic_path():
    if config.MODE == FuncType.SELF_CONTAINED:
        return config.BENCHMARK_STATISTICS_PATH
    elif config.MODE == FuncType.LEVEL_SELF_CONTAINED:
        return config.BENCHMARK_LEVEL_STATISTICS_PATH
    elif config.MODE == FuncType.WEAKLY_SELF_CONTAINED:
        return config.BENCHMARK_WEAKLY_STATISTICS_PATH
    else:
        raise ValueError(f"Unsupported mode: {config.MODE}")
    
def get_running_status_path():
    if config.MODE == FuncType.SELF_CONTAINED:
        return config.BENCHMARK_RUNNING_STATUS_PATH
    elif config.MODE == FuncType.LEVEL_SELF_CONTAINED:
        return config.BENCHMARK_LEVEL_RUNNING_STATUS_PATH
    elif config.MODE == FuncType.WEAKLY_SELF_CONTAINED:
        return config.BENCHMARK_WEAKLY_RUNNING_STATUS_PATH
    else:
        raise ValueError(f"Unsupported mode: {config.MODE}")
    
def is_recursive_function(function_definition: str, function_name: str) -> bool:
    """
    判断一个函数是否是递归函数。

    Parameters:
    - function_definition (str): 函数的完整定义（包括函数体）。
    - function_name (str): 函数的名称。

    Returns:
    - bool: 如果是递归函数，返回 True；否则返回 False。
    """
    # 使用正则表达式匹配函数体中对自身函数名的调用
    pattern = rf'\b{re.escape(function_name)}\b\s*\('
    return re.search(pattern, function_definition) is not None

def deduplicate_dict_values(input_dict):
    """
    对字典的值进行去重，保留第一个出现的键值对。

    Parameters:
    - input_dict (dict): 输入的字典。

    Returns:
    - dict: 去重后的字典。
    """
    seen_values = set()
    deduplicated_dict = {}

    for key, value in input_dict.items():
        # 将不可哈希的值（如 list）转换为 tuple
        hashable_value = tuple(value) if isinstance(value, list) else value
        if hashable_value not in seen_values:
            deduplicated_dict[key] = value
            seen_values.add(hashable_value)

    return deduplicated_dict

def get_existing_func_name_list(func_to_idx: Dict):
    return [func.split('.')[-2] for func in func_to_idx.keys()]