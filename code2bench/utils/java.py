import re

def replace_java_method_name(code, new_name):
    """
    替换 Java 方法的名称为 new_name

    示例匹配：
    public String getUserName(int id) {
        // ...
    }
    """
    # 匹配 Java 方法定义（带可选修饰符、返回类型、方法名、参数和左大括号）
    pattern = r"((public|protected|private|static|\s)+\s+[\w<>\[\]]+\s+)(\w+)(\s*\([^)]*\)\s*\{)"
    
    # 替换方法名
    replaced_code = re.sub(pattern, rf"\1{new_name}\4", code)
    print(replaced_code)
    
    return replaced_code


def extract_java_method_name(code):
    """
    从 Java 方法定义中提取方法名称

    示例匹配：
    public int calculateSum(int a, int b) {
        // ...
    }
    """
    pattern = r"(public|protected|private|static|\s)+\s+[\w<>\[\]]+\s+(\w+)\s*\([^)]*\)\s*\{"
    
    match = re.search(pattern, code)
    
    if match:
        return match.group(2)
    else:
        return None
    
def add_package(code, idx): 
    # # if already has a package, we should move it and then add the new one
    if code.startswith("package "):
        code = code.split("\n", 1)[1]
    return f"package {idx};\n" + code

import re

from code2bench.llm.llm_caller import call_llm
from code2bench import llm_client

def convert_python_docstring_to_java_doc(docstring):
    prompt = """
请严格按照以下规则将Python docstring转换为JavaDoc格式，保持原始内容不变：

# 转换规则
1. 整体结构：
   - 输入内容直接包裹在/** 和 */之间
   - 每行前缀添加" * "
   - 保留原始空行（转换为" *"）

2. 标签转换：
   | Python标签 | JavaDoc标签  | 转换规则                                                              |
   |-----------|-------------|-----------------------------------------------------------------------|
   | Args:     | @param      | 保持参数描述原样，每行独立转换（例：`base: 描述...` → `@param base 描述...`） |
   | Returns:  | @return     | 保持返回值描述原样（注意JavaDoc使用单数形式@return而非@returns）          |
   | Raises:   | @throws     | 保持异常描述原样（例：`ValueError: 描述` → `@throws Exception 描述`）     |

3. 特别处理：
   - 保留所有原始换行和缩进
   - 不修改任何描述内容（包括标点符号、换行符、特殊字符）
   - 非标准段落（如"Special rules:"）直接保留为注释
   - 所有Python异常类型转换为Java的对应类型（如ValueError转换为IllegalArgumentException）
   - 没有完全对应的Python异常统一使用Exception类型

4. Java异常类型对应关系：
   | Python异常        | Java异常                      |
   |------------------|-------------------------------|
   | ValueError       | IllegalArgumentException     |
   | TypeError        | ClassCastException           |
   | IndexError       | IndexOutOfBoundsException    |
   | KeyError         | NoSuchElementException       |
   | FileNotFoundError| FileNotFoundException        |
   | IOError          | IOException                  |
   | ZeroDivisionError| ArithmeticException          |
   | 其他异常          | Exception                    |

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
 * @param base A JSON-like object (can be dict/list)
 * @param update Update structure
 * @return New merged object
 * @throws IllegalArgumentException If types incompatible
 *
 * Special rules:
 * - Dictionary merge
 * - List concat
 */    
"""
    res = call_llm(llm=llm_client, system_message=prompt, user_message=docstring)
    return res

import re

def parse_java_test_failures(error_output, total_tests=None):
    """
    解析Java测试失败输出，提取失败的测试用例数量、总测试用例数量和通过率
    
    Args:
        error_output (str): 测试失败输出字符串
        total_tests (int, optional): 测试用例总数，如果为None则尝试从输出中提取
    
    Returns:
        dict: 包含以下键值对的字典：
            - 'failed_count': 失败的测试用例数量(int)
            - 'failed_cases': 失败的测试用例详情列表(list of dict)
            - 'passed_count': 通过的测试用例数量(int)
            - 'total_tests': 总测试用例数量(int)
            - 'pass_rate': 通过率(float，0到1之间)
            - 'pass_percentage': 通过率的百分比表示(str，带百分号)
    """
    # 1. 识别 [ERROR] Failures: 行，确认有失败的测试
    if "[ERROR] Failures:" not in error_output:
        # 可能是其他类型的错误或全部通过
        if "[INFO] Tests run:" in error_output:
            # 尝试从maven输出中提取测试数据
            maven_pattern = re.compile(r'\[INFO\] Tests run: (\d+), Failures: (\d+), Errors: (\d+), Skipped: (\d+)')
            maven_match = maven_pattern.search(error_output)
            if maven_match:
                total = int(maven_match.group(1))
                failures = int(maven_match.group(2))
                errors = int(maven_match.group(3))
                failed_count = failures + errors
                passed_count = total - failed_count
                
                return {
                    'failed_count': failed_count,
                    'failed_cases': [],
                    'passed_count': passed_count,
                    'total_tests': total,
                    'pass_rate': passed_count / total if total > 0 else 0,
                    'pass_percentage': f"{(passed_count / total * 100) if total > 0 else 0:.2f}%"
                }
        
        if total_tests is not None:
            # 如果提供了总测试数量且没有发现失败，认为全部通过
            return {
                'failed_count': 0,
                'failed_cases': [],
                'passed_count': total_tests,
                'total_tests': total_tests,
                'pass_rate': 1.0,
                'pass_percentage': "100.00%"
            }
        
        # 无法确定测试结果
        return {
            'failed_count': None,
            'failed_cases': [],
            'passed_count': None,
            'total_tests': None,
            'pass_rate': None,
            'pass_percentage': None,
            'error': 'Unable to parse test results'
        }
    
    # 2. 提取每个测试失败的详细信息
    # 查找形如 [ERROR]   Tester.testGetCorrectIndentLevel:48 Test case failed: 的行
    test_failure_pattern = re.compile(r'\[ERROR\]\s+([^:]+):(\d+) (Test case failed:.*?)(?=\[ERROR\]|\Z)', re.DOTALL)
    
    failed_cases = []
    for match in test_failure_pattern.finditer(error_output):
        test_name = match.group(1)
        line_number = match.group(2)
        failure_details = match.group(3).strip()
        
        # 进一步解析测试失败的细节
        inputs_match = re.search(r'Inputs: (.*?)Expected:', failure_details, re.DOTALL)
        expected_match = re.search(r'Expected: (.*?)Actual:', failure_details, re.DOTALL)
        actual_match = re.search(r'Actual: (.*?)(?:==>|$)', failure_details, re.DOTALL)
        
        inputs = inputs_match.group(1).strip() if inputs_match else None
        expected = expected_match.group(1).strip() if expected_match else None
        actual = actual_match.group(1).strip() if actual_match else None
        
        failed_cases.append({
            'test_name': test_name,
            'line_number': line_number,
            'inputs': inputs,
            'expected': expected,
            'actual': actual,
            'full_details': failure_details
        })
    
    # 计算失败的测试用例数量
    failed_count = len(failed_cases)
    
    # 如果没有提供总测试数量，尝试从输出中提取
    if total_tests is None:
        # 尝试从JUnit/Maven输出中提取总测试数
        run_tests_pattern = re.compile(r'Tests run: (\d+)')
        run_tests_match = run_tests_pattern.search(error_output)
        if run_tests_match:
            total_tests = int(run_tests_match.group(1))
        else:
            # 无法确定总测试数，暂时设置为失败数
            total_tests = failed_count
    
    # 计算通过的测试用例数量和通过率
    passed_count = total_tests - failed_count
    pass_rate = passed_count / total_tests if total_tests > 0 else 0
    pass_percentage = f"{pass_rate * 100:.2f}%"
    
    return {
        'failed_count': failed_count,
        # 'failed_cases': failed_cases,
        'passed_count': passed_count,
        'total_tests': total_tests,
        # 'pass_rate': pass_rate,
        'pass_percentage': pass_percentage
    }

# 示例使用
if __name__ == "__main__":
    # 示例错误输出
    error_output = """[ERROR] Failures: 
[ERROR]   Tester.testGetCorrectIndentLevel:48 Test case failed:
Inputs: lines=[ 　      　Raz:ko,,      async def ìũ,  ;Q:, y$¬,          class ŦŬęò¼í𐾶È4䮙Č, ,         :CHUIpVo);q#si:], line_index=6
Expected:          
Actual:      ==> expected: <true> but was: <false>
[ERROR]   Tester.testGetCorrectIndentLevel:48 Test case failed:
Inputs: lines=[     async def ÒJÎ:,   6o)}X3,,        =(h6hrTXHuZ\\Pah+.:,           ], line_index=3
Expected:        
Actual:      ==> expected: <true> but was: <false>"""
    
    # 假设总测试用例数为20
    result = parse_java_test_failures(error_output, total_tests=20)
    
    print(f"失败的测试用例数量: {result['failed_count']}")
    print(f"通过的测试用例数量: {result['passed_count']}")
    print(f"测试用例总数: {result['total_tests']}")
    # print(f"通过率: {result['pass_rate']}")
    print(f"通过率百分比: {result['pass_percentage']}")
    print("\n失败的测试用例详情:")
    for i, case in enumerate(result['failed_cases'], 1):
        print(f"失败 #{i}:")
        print(f"  测试名称: {case['test_name']}")
        print(f"  行号: {case['line_number']}")
        print(f"  输入: {case['inputs']}")
        print(f"  期望: {case['expected']}")
        print(f"  实际: {case['actual']}")
        print()

# def convert_python_docstring_to_java_javadoc(docstring):
#     """
#     将 Python 文档字符串转换为 Java Javadoc 格式的注释。
    
#     Args:
#         docstring: Python 文档字符串
    
#     Returns:
#         转换后的 Java Javadoc 注释
#     """
#     # 移除开头和结尾的三引号
#     docstring = docstring.strip()
#     if docstring.startswith('"""') and docstring.endswith('"""'):
#         docstring = docstring[3:-3].strip()
    
#     # 初始化 Javadoc 内容
#     javadoc_lines = ["/**"]
    
#     # 分割文档字符串为段落
#     paragraphs = re.split(r'\n\s*\n', docstring)
    
#     for paragraph in paragraphs:
#         paragraph = paragraph.strip()
#         if not paragraph:
#             continue
        
#         # 处理普通描述
#         if not (paragraph.startswith("Args:") or 
#                 paragraph.startswith("Returns:") or 
#                 paragraph.startswith("Raises:")):
#             javadoc_lines.append(f" * {paragraph}")
#             javadoc_lines.append(" *")  # 添加空行分隔
#             continue
        
#         # 处理参数部分
#         if paragraph.startswith("Args:"):
#             lines = paragraph.split('\n')
#             for line in lines:
#                 # 跳过标题行
#                 if line.strip().lower() == "args:":
#                     continue
#                 match = re.match(r'^\s*([a-zA-Z_]\w*)\s*(\(.*?\))?:\s*(.*)', line)
#                 if match:
#                     param_name = match.group(1)
#                     param_desc = match.group(3).strip()
#                     javadoc_lines.append(f" * @param {param_name} {param_desc}")
#             javadoc_lines.append(" *")  # 添加空行分隔
        
#         # 处理返回值部分
#         elif paragraph.startswith("Returns:"):
#             lines = paragraph.split('\n')
#             for line in lines:
#                 # 跳过标题行
#                 if line.strip().lower() == "returns:":
#                     continue
#                 match = re.match(r'^\s*Returns:\s*(.*)', line, flags=re.IGNORECASE)
#                 if match:
#                     return_desc = match.group(1).strip()
#                     # 去掉类型提示（如 "int:"）
#                     return_desc = re.sub(r'^\w+:\s*', '', return_desc)
#                     javadoc_lines.append(f" * @return {return_desc}")
#             javadoc_lines.append(" *")  # 添加空行分隔
        
#         # 处理异常部分
#         elif paragraph.startswith("Raises:"):
#             lines = paragraph.split('\n')
#             for line in lines:
#                 # 跳过标题行
#                 if line.strip().lower() == "raises:":
#                     continue
#                 match = re.match(r'^\s*([a-zA-Z_]\w*):\s*(.*)', line)
#                 if match:
#                     exception_class = match.group(1)
#                     exception_desc = match.group(2).strip()
#                     javadoc_lines.append(f" * @throws {exception_class} {exception_desc}")
#             javadoc_lines.append(" *")  # 添加空行分隔
    
#     # 移除最后一个多余的空行
#     if javadoc_lines[-1] == " *":
#         javadoc_lines.pop()
    
#     # 结束 Javadoc 注释
#     javadoc_lines.append(" */")
    
#     return "\n".join(javadoc_lines)


# def test_java_method_parser():
#     code = """
# public class Tested {
#     public String getUserInfo(int id) {
#         // TODO
#     }
# }
# """
#     alias_code = """
# public class Tested {
#     public String fetchUser(int id) {
#         // TODO
#     }
# }
# """
#     method_name = "getUserInfo"
#     alias_name = "fetchUser"
#     assert extract_java_method_name(code) == method_name
#     replace_java_method_name(code, alias_name)
#     assert replace_java_method_name(code, alias_name) == alias_code

if __name__ == "__main__":
    # 示例用法
    python_docstring = '''
    """
    计算两个整数的和。

    Args:
        a (int): 第一个整数
        b (int): 第二个整数

    Returns:
        int: 两个整数的和

    Raises:
        ValueError: 如果输入参数无效
    """
    '''

    converted_javadoc = convert_python_docstring_to_java_javadoc(python_docstring)
    print(converted_javadoc)
