import re

def replace_function_name(code, new_name):
    # 定义正则表达式，匹配函数名
    pattern = r"(func\s+)(\w+)(\s*\(.*\)\s*\w+\s*\{.*)"
    
    # 使用 re.sub 替换函数名
    replaced_code = re.sub(pattern, rf"\1{new_name}\3", code)
    
    return replaced_code

def extract_function_name(code):
    # 定义正则表达式，匹配函数名
    pattern = r"func\s+(\w+)\s*\(.*\)\s*\w+\s*\{.*"
    
    # 使用 re.search 查找匹配
    match = re.search(pattern, code)
    
    if match:
        # 提取捕获组中的函数名
        return match.group(1)
    else:
        # 如果未匹配到，返回 None
        return None

def convert_python_docstring_to_go_comment(docstring):
    """
    将 Python 文档字符串转换为 Go 格式的注释（全部使用 // 单行注释）
    
    Args:
        docstring: Python 文档字符串
    
    Returns:
        转换后的 Go 注释
    """
    # 移除开头和结尾的三引号
    docstring = docstring.strip()
    if docstring.startswith('"""') and docstring.endswith('"""'):
        docstring = docstring[3:-3].strip()
    
    # 处理参数部分
    docstring = re.sub(r'Args:', 'Parameters:', docstring)
    
    # 处理返回值部分
    docstring = re.sub(r'Returns:', 'Returns:', docstring)
    
    # 将每一行转换为 Go 注释格式
    lines = docstring.split('\n')
    go_comment_lines = []
    
    # 处理每一行
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:
            # 对非空行添加 // 前缀
            go_comment_lines.append(f"// {stripped_line}")
        else:
            # 对空行也保留 //，表示注释中的空行
            go_comment_lines.append("//")
    
    return "\n".join(go_comment_lines)

def rename_duplicate_types(file1_content: str, file2_content: str) -> str:
    """
    检测 file1 和 file2 中重复的类型定义，并对 file1 中的重复类型进行重命名。
    重命名时会更新 file1 中所有对该类型的引用。
    
    参数:
        file1_content: 文件1的内容 (字符串)
        file2_content: 文件2的内容 (字符串)
    
    返回:
        修改后的文件1内容 (字符串)
    """
    # 正则表达式匹配类型定义
    type_pattern = re.compile(r"type\s+(\w+)\s+struct\s*\{")
    
    # 提取两个文件中的类型定义
    types_in_file1 = set(type_pattern.findall(file1_content))
    types_in_file2 = set(type_pattern.findall(file2_content))
    
    # 找到重复的类型名称
    duplicate_types = types_in_file1.intersection(types_in_file2)
    
    # 如果没有重复类型，直接返回原始内容
    if not duplicate_types:
        return file1_content
    
    # 遍历重复类型，重命名并在 file1 中更新所有引用
    for duplicate_type in duplicate_types:
        # 构造新的类型名称
        new_type_name = f"Renamed_{duplicate_type}"
        
        # 替换类型定义
        file1_content = re.sub(
            rf"type\s+{re.escape(duplicate_type)}\s+struct\s*\{{",
            f"type {new_type_name} struct {{",
            file1_content
        )
        
        # 替换所有对该类型的引用
        file1_content = re.sub(
            rf"\b{re.escape(duplicate_type)}\b",
            new_type_name,
            file1_content
        )
    
    return file1_content

import re

def parse_go_test_results(test_output, total_tests=None):
    """
    解析Go语言测试输出并提取测试结果统计信息
    
    Args:
        test_output (str): Go测试运行的输出字符串
        total_tests (int, optional): 测试用例总数，如果为None则从输出中计算
    
    Returns:
        dict: 包含以下键值对的字典：
            - 'failed_count': 失败的测试用例数量(int)
            - 'failed_cases': 失败的测试用例详情列表(list)
            - 'passed_count': 通过的测试用例数量(int)
            - 'total_tests': 总测试用例数量(int)
            - 'pass_rate': 通过率(float，0到1之间)
            - 'pass_percentage': 通过率的百分比表示(str，带百分号)
    """
    # 初始化结果字典
    result = {
        'failed_count': 0,
        'failed_cases': [],
        'passed_count': 0,
        'total_tests': 0,
        'pass_rate': 0,
        'pass_percentage': '0.00%'
    }
    
    # 查找所有测试结果行
    test_lines = re.findall(r'--- (PASS|FAIL): ([\w/]+) \(([\d.]+)s\)', test_output)
    
    # 统计通过和失败的测试用例
    passed_tests = []
    failed_tests = []
    
    for status, test_name, duration in test_lines:
        if status == 'PASS':
            passed_tests.append({
                'test_name': test_name,
                'duration': duration
            })
        else:  # status == 'FAIL'
            failed_tests.append({
                'test_name': test_name,
                'duration': duration
            })
    
    # 设置计数
    result['passed_count'] = len(passed_tests)
    result['failed_count'] = len(failed_tests)
    
    # 如果未提供总测试数，则从找到的测试数计算
    if total_tests is None:
        result['total_tests'] = result['passed_count'] + result['failed_count']
    else:
        result['total_tests'] = total_tests
    
    # 详细记录失败的测试用例
    for test in failed_tests:
        # 尝试从测试名称中提取测试用例编号
        case_match = re.search(r'Case(\d+)', test['test_name'])
        case_number = case_match.group(1) if case_match else "Unknown"
        
        result['failed_cases'].append({
            'test_name': test['test_name'],
            'case_number': case_number,
            'duration': test['duration'],
            'full_details': f"--- FAIL: {test['test_name']} ({test['duration']}s)"
        })
    
    # 计算通过率
    if result['total_tests'] > 0:
        result['pass_rate'] = result['passed_count'] / result['total_tests']
        result['pass_percentage'] = f"{result['pass_rate'] * 100:.2f}%"
    
    return result

# 示例用法
if __name__ == "__main__":
    test_output = """--- FAIL: TestProcessJSON/Case475 (0.00s)
--- PASS: TestProcessJSON/Case476 (0.00s)
--- FAIL: TestProcessJSON/Case477 (0.00s)
--- PASS: TestProcessJSON/Case478 (0.00s)
--- PASS: TestProcessJSON/Case479 (0.00s)
--- FAIL: TestProcessJSON/Case480 (0.00s)
--- FAIL: TestProcessJSON/Case481 (0.00s)
--- FAIL: TestProcessJSON/Case482 (0.00s)
--- FAIL: TestProcessJSON/Case483 (0.00s)
--- FAIL: TestProcessJSON/Case484 (0.00s)
--- FAIL: TestProcessJSON/Case485 (0.00s)
--- FAIL: TestProcessJSON/Case486 (0.00s)
--- FAIL: TestProcessJSON/Case487 (0.00s)
--- PASS: TestProcessJSON/Case488 (0.00s)
--- PASS: TestProcessJSON/Case489 (0.00s)
--- FAIL: TestProcessJSON/Case490 (0.00s)
--- FAIL: TestProcessJSON/Case491 (0.00s)
--- FAIL: TestProcessJSON/Case492 (0.00s)
--- PASS: TestProcessJSON/Case493 (0.00s)
--- FAIL: TestProcessJSON/Case494 (0.00s)
--- FAIL: TestProcessJSON/Case495 (0.00s)
--- PASS: TestProcessJSON/Case496 (0.00s)
--- FAIL: TestProcessJSON/Case497 (0.00s)
--- PASS: TestProcessJSON/Case498 (0.00s)
--- PASS: TestProcessJSON/Case499 (0.00s)"""
    
    result = parse_go_test_results(test_output)
    
    print(f"失败的测试用例数量: {result['failed_count']}")
    print(f"通过的测试用例数量: {result['passed_count']}")
    print(f"测试用例总数: {result['total_tests']}")
    print(f"通过率: {result['pass_rate']}")
    print(f"通过率百分比: {result['pass_percentage']}")
    
    print("\n失败的测试用例:")
    for i, case in enumerate(result['failed_cases'], 1):
        print(f"{i}. 测试名称: {case['test_name']} (用例编号: {case['case_number']})")

