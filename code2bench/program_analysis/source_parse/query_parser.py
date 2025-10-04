from tree_sitter_languages import get_language, get_parser
from typing import Dict, List, Tuple

def build_query_pattern(func_names: List[str]) -> str:
    """动态构建包含多个函数名的查询模式"""
    if not func_names:
        return ""
    
    # 生成any-of谓词的条件部分
    conditions = "\n    ".join(f'"{name}"' for name in func_names)
    return f"""
(call
  (identifier) @call.identifier
  (#any-of? @call.identifier
    {conditions}
  )
  (argument_list) @call.argument_list
)
"""

def extract_function_calls(source_code: str, target_funcs: List[str]) -> Tuple[List[str], List[int]]:
    """提取目标函数的调用信息
    
    Args:
        source_code: 需要分析的源代码
        target_funcs: 目标函数名列表
        
    Returns:
        Tuple[List[str], List[int]]: 
            匹配的函数名列表，对应的参数数量列表
    """
    language = get_language("python")
    parser = get_parser("python")
    
    # 构建动态查询
    query_pattern = build_query_pattern(target_funcs)
    if not query_pattern:
        return [], []
    
    # 解析代码
    tree = parser.parse(bytes(source_code, "utf-8"))
    query = language.query(query_pattern)
    captures = query.captures(tree.root_node)
    
    # 处理捕获结果
    func_calls = []
    arg_counts = []
    
    current_func = None
    for node, tag in captures:
        if tag == "call.identifier":
            current_func = node.text.decode("utf-8")
        elif tag == "call.argument_list" and current_func:
            # 计算参数数量
            arg_count = node.named_child_count
            func_calls.append(current_func)
            arg_counts.append(arg_count)
            current_func = None  # Reset for next capture
    
    return func_calls, arg_counts

def check_function_calls(functions: List[str], arg_counts: List[int], target_functions: Dict[str, int]) -> List[Dict[str, int]]:
    """检查提取的函数调用是否符合目标函数的参数数量
    
    Args:
        functions: 提取的函数名列表
        arg_counts: 提取的参数数量列表
        target_functions: 目标函数及其参数数量的字典
        
    Returns:
        List[Dict[str, int]]: 符合条件的函数及其参数数量的列表
    """
    res = []
    for func, count in zip(functions, arg_counts):
        if target_functions.get(func) == count:
            res.append({"function": func, "arguments": count})
    return res


# 使用示例
if __name__ == "__main__":
    sample_code = """
def test():
    _flattenize_inputs(data)
    list(items)
    _flattenize_inputs2(more_data)
    isinstance(obj, (str, int))
    """
    
    # function_name: number_of_arguments
    target_functions = {
        "_flattenize_inputs": 1,
        "_flattenize_inputs2": 1,
        "isinstance": 2,
        "list": 1
    }
    functions, arg_counts = extract_function_calls(sample_code, target_functions.keys())
    res = check_function_calls(functions, arg_counts, target_functions)
    print(res)