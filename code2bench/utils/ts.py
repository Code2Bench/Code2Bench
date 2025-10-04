import re

def replace_ts_function_name(code, new_name):
    """
    替换 TypeScript 函数的名称为 new_name

    示例匹配：
    function oldName(param: string): number {
        // ...
    }
    """
    # 匹配 TypeScript 的函数定义
    pattern = r"(function\s+)(\w+)(\s*\([^)]*\)\s*:\s*[^ \n{]+\s*\{)"
    
    # 替换函数名
    replaced_code = re.sub(pattern, rf"\1{new_name}\3", code)
    
    return replaced_code


def extract_ts_function_name(code):
    """
    从 TypeScript 函数定义中提取函数名称。
    支持有无类型注解的函数定义。
    """
    pattern = r"function\s+(\w+)\s*\([^)]*\)\s*(?::\s*[^ \n{]+)?\s*\{"
    
    match = re.search(pattern, code)
    
    if match:
        return match.group(1)
    else:
        return None
    
import re

from code2bench.llm.llm_caller import call_llm
from code2bench import llm_client

def convert_python_docstring_to_ts_doc(docstring):
    prompt = """
请严格按照以下规则将Python docstring转换为TypeScript文档格式，保持原始内容不变：

# 转换规则
1. 整体结构：
   - 输入内容直接包裹在/** 和 */之间
   - 每行前缀添加" * "
   - 保留原始空行（转换为" *"）

2. 标签转换：
   | Python标签 | TypeScript标签 | 转换规则                                                                    |
   |-----------|--------------|------------------------------------------------------------------------------|
   | Args:     | @param       | 转换为TypeScript参数语法（例：`base: 描述...` → `@param base - 描述...`）      |
   | Returns:  | @returns     | 保持返回值描述原样                                                            |
   | Raises:   | @throws      | 保持异常描述原样（例：`ValueError: 描述` → `@throws {Error} 描述`）           |

3. 特别处理：
   - 保留所有原始换行和缩进
   - 不修改任何描述内容（包括标点符号、换行符、特殊字符）
   - 非标准段落（如"Special rules:"）直接保留为注释
   - 与JSDoc不同，TypeScript通常不在@param中指定类型，因为它通过函数签名定义
   - 所有Error类型默认转换为标准TypeScript的Error类型

# 输入示例
\"\"\"Recursively merge two JSON-like objects.

Args:
    base: A JSON-like object (can be dict/list)
    update: Update structure

Returns:
    New merged object

Raises:
    ValueError: If types incompatible

Special rules:
    - Dictionary merge
    - List concat
\"\"\"

# 期望输出
/**
 * Recursively merge two JSON-like objects.
 * 
 * @param base - A JSON-like object (can be dict/list)
 * @param update - Update structure
 * @returns New merged object
 * @throws {Error} If types incompatible
 * 
 * Special rules:
 * - Dictionary merge
 * - List concat
 */    
"""
    res = call_llm(llm=llm_client, system_message=prompt, user_message=docstring)
    return res

import re

def parse_ts_jest_test_results(test_output, total_tests=None):
    """
    解析TypeScript/Jest测试输出并提取测试结果统计信息，
    返回格式与Java测试结果解析函数一致
    
    Args:
        test_output (str): Jest测试运行的输出字符串
        total_tests (int, optional): 测试用例总数，如果为None则从输出中提取
    
    Returns:
        dict: 包含以下键值对的字典：
            - 'failed_count': 失败的测试用例数量(int)
            - 'failed_cases': 失败的测试用例详情列表(list)
            - 'passed_count': 通过的测试用例数量(int)
            - 'total_tests': 总测试用例数量(int)
            - 'pass_rate': 通过率(float，0到1之间)
            - 'pass_percentage': 通过率的百分比表示(str，带百分号)
    """
    # 初始化结果字典，使用与Java解析函数一致的键
    result = {
        'failed_count': 0,
        'failed_cases': [],
        'passed_count': 0,
        'total_tests': 0,
        'pass_rate': 0,
        'pass_percentage': '0.00%'
    }
    
    # 解析测试用例统计
    tests_match = re.search(r'Tests:\s+(\d+)\s+failed,\s+(\d+)\s+passed,\s+(\d+)\s+total', test_output)
    if tests_match:
        result['failed_count'] = int(tests_match.group(1))
        result['passed_count'] = int(tests_match.group(2))
        result['total_tests'] = int(tests_match.group(3))
    else:
        # 如果没有找到具体的测试统计，但提供了总测试数
        if total_tests is not None:
            result['total_tests'] = total_tests
            
            # 检查是否有失败信息
            if "FAIL" in test_output:
                # 无法确定具体失败数，假设至少有1个失败
                result['failed_count'] = 1
                result['passed_count'] = total_tests - 1
            else:
                # 假设全部通过
                result['passed_count'] = total_tests
    
    # 尝试提取失败的测试用例详情
    # 例如： FAIL src/test.ts:123 Test Description
    failure_details = re.findall(r'FAIL\s+([^\s]+):(\d+)\s+(.*?)(?=\n|$)', test_output)
    
    for file_path, line_number, description in failure_details:
        result['failed_cases'].append({
            'test_name': description.strip(),
            'file_path': file_path.strip(),
            'line_number': line_number,
            'full_details': f"FAIL {file_path}:{line_number} {description.strip()}"
        })
    
    # 计算通过率
    if result['total_tests'] > 0:
        result['pass_rate'] = result['passed_count'] / result['total_tests']
        result['pass_percentage'] = f"{result['pass_rate'] * 100:.2f}%"
    
    return result

# 示例用法
if __name__ == "__main__":
    test_output = """
Test Suites: 1 failed, 1 total
Tests:       2 failed, 498 passed, 500 total
Snapshots:   0 total
Time:        8.771 s, estimated 9 s
Ran all test suites matching /.\/2\/runner.test.ts/i.
"""
    
    result = parse_ts_jest_test_results(test_output)
    
    print(f"失败的测试用例数量: {result['failed_count']}")
    print(f"通过的测试用例数量: {result['passed_count']}")
    print(f"测试用例总数: {result['total_tests']}")
    print(f"通过率: {result['pass_rate']}")
    print(f"通过率百分比: {result['pass_percentage']}")
    
    if result['failed_cases']:
        print("\n失败的测试用例详情:")
        for i, case in enumerate(result['failed_cases'], 1):
            print(f"失败 #{i}:")
            print(f"  测试名称: {case['test_name']}")
            print(f"  文件路径: {case['file_path']}")
            print(f"  行号: {case['line_number']}")
            print(f"  详情: {case['full_details']}")
    else:
        print("\n无法提取失败测试用例的详细信息")

# def test_ts_function_parser():
#     code1 = """
# function getUserInfo(id: number): string {
#     // TODO
# }
# """
#     code2 = """
# function getUserInfo(id): string {
#     // TODO
# }
# """
#     code3 = """
# function getUserInfo(id: number) {
#     // TODO
# }
# """
#     code4 = """
# function getUserInfo(id) {
#     // TODO
# }
# """
#     func_name = "getUserInfo"
#     assert extract_ts_function_name(code1) == func_name
#     assert extract_ts_function_name(code2) == func_name
#     assert extract_ts_function_name(code3) == func_name
#     assert extract_ts_function_name(code4) == func_name

# test_ts_function_parser()
