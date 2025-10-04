import re
import ast
from typing import Dict, List


def add_docstring_to_signature(docstring: str, signature: str) -> str:
    """
    将文档字符串(docstring)添加到函数签名中，放在函数参数之后，函数体之前。
    
    Args:
        docstring (str): 函数的文档字符串，可以包含或不包含三引号
        signature (str): 函数的签名，包括函数名和参数
        
    Returns:
        str: 组合后的函数定义，包含签名和文档字符串
    
    Example:
        >>> doc = '\"\"\"This is a docstring\"\"\"'
        >>> sig = 'def example_func(a, b):'
        >>> add_docstring_to_signature(doc, sig)
        'def example_func(a, b):\\n    \"\"\"This is a docstring\"\"\"\\n    pass'
    """
    # 清理docstring，确保它是一个适当的三引号文档字符串
    docstring = docstring.strip()
    
    # 确保docstring有三引号
    if not docstring.startswith('"""'):
        docstring = f'"""{docstring}'
    if not docstring.endswith('"""'):
        docstring = f'{docstring}"""'
    
    # 将docstring分行并适当缩进
    docstring_lines = docstring.split('\n')
    
    # 第一行保持不变，其余行缩进4个空格
    indented_docstring = docstring_lines[0]
    for i in range(1, len(docstring_lines)):
        line = docstring_lines[i]
        # 如果行不为空，添加4个空格缩进
        if line.strip():
            indented_docstring += f'\n    {line}'
        # 如果是空行，保留空行
        else:
            indented_docstring += '\n'
    
    # 处理签名
    sig_lines = signature.strip().split('\n')
    
    # 分离导入语句和函数定义
    imports = []
    function_def_idx = -1
    
    for i, line in enumerate(sig_lines):
        stripped_line = line.strip()
        if stripped_line.startswith('def '):
            function_def_idx = i
            break
        imports.append(line)
    
    # 如果没有找到函数定义，则使用第一行作为函数定义
    if function_def_idx == -1:
        function_def_idx = 0
        imports = []
    
    function_def = sig_lines[function_def_idx].strip()
    
    # 确保函数定义以冒号结尾
    if not function_def.endswith(':'):
        function_def += ':'
    
    # 构建结果，首先添加导入语句
    result = '\n'.join(imports)
    if imports:
        result += '\n'  # 在导入和函数定义之间添加空行
    
    # 添加函数定义和文档字符串
    result += f"{function_def}\n    {indented_docstring}"
    
    # 处理函数体
    if len(sig_lines) > function_def_idx + 1:
        # 提取函数体（函数定义之后的所有内容）
        body = '\n'.join(sig_lines[function_def_idx + 1:])
        
        # 检查是否有TODO注释
        if "# TODO:" in body or "# TODO" in body:
            # 保留原始格式的TODO注释和pass
            todo_lines = []
            for line in sig_lines[function_def_idx + 1:]:
                if line.strip():  # 只添加非空行
                    todo_lines.append(line)
            
            # 添加函数体到结果
            if todo_lines:
                result += '\n' + '\n'.join(todo_lines)
            else:
                result += '\n    pass'
        else:
            # 如果没有TODO注释，添加其他函数体内容
            body_lines = [line for line in sig_lines[function_def_idx + 1:] if line.strip()]
            if body_lines:
                result += '\n    ' + '\n    '.join(body_lines)
            else:
                result += '\n    pass'
    else:
        # 如果只有函数定义，添加pass
        result += '\n    pass'
    
    return result

def parse_python_test_failures(error_message, total_tests=500):
    """
    解析Python测试错误信息，提取失败的测试用例数量和计算通过率
    
    Args:
        error_message (str): 测试错误信息字符串
        total_tests (int, optional): 测试用例总数，默认为500
    
    Returns:
        dict: 包含以下键值对的字典：
            - 'failed_count': 失败的测试用例数量(int)
            - 'failed_cases': 失败的测试用例ID列表(list of int)
            - 'passed_count': 通过的测试用例数量(int)
            - 'total_tests': 测试用例总数(int)
            - 'pass_rate': 通过率(float，0到1之间)
            - 'pass_percentage': 通过率的百分比表示(str，带百分号)
    """
    # 使用正则表达式匹配"Test case X failed:"格式的字符串
    # 这里假设测试用例ID是整数
    failed_case_pattern = re.compile(r'Test case (\d+) failed:', re.IGNORECASE)
    
    # 找出所有失败的测试用例ID
    failed_cases = [int(match.group(1)) for match in failed_case_pattern.finditer(error_message)]
    
    # 计算失败和通过的测试用例数量
    failed_count = len(failed_cases)
    passed_count = total_tests - failed_count
    
    # 计算通过率
    pass_rate = passed_count / total_tests if total_tests > 0 else 0
    pass_percentage = f"{pass_rate * 100:.2f}%"
    
    return {
        'failed_count': failed_count,
        # 'failed_cases': failed_cases,
        'passed_count': passed_count,
        'total_tests': total_tests,
        'pass_rate': pass_rate,
        # 'pass_percentage': pass_percentage
    }

def modify_runner(func_name, runner):
    """
    Inserts "func1={func_name}" before the line containing "def load_test_cases_from_json"
    and returns the modified runner.

    Args:
        func_name (str): The name of the function to assign to func1.
        runner (str): The original runner code as a string.

    Returns:
        str: The modified runner code with the new assignment inserted.
    """
    lines = runner.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("def load_test_cases_from_json"):
            # Insert the new line before the target function definition
            lines.insert(i, f"func1={func_name}")
            break
    return "\n".join(lines)

def detect_other_imports(content: str):
    # Define the known imports
    known_imports = [
        r'^from tested import .+ as .+$',
        'from hypothesis import settings',
        'import hypothesis.strategies as st',
        'from hypothesis import given'
    ]

    # Find all import statements
    import_statements = re.findall(r'^\s*(import .+|from .+ import .+)', content, re.MULTILINE)

    # Check for unknown imports
    unknown_imports = []
    for imp in import_statements:
        if not any(re.match(pattern, imp) for pattern in known_imports):
            unknown_imports.append(imp)

    return unknown_imports

def extract_imported_function(import_statement):
    # """
    # Extracts the imported function name from a 'from ... import ... as ...' statement.

    # Parameters:
    # import_statement (str): The import statement.

    # Returns:
    # str: The imported function name.
    # """
    # match = re.match(r'^from\s+\S+\s+import\s+([\w\.]+)\s+as\s+\w+', import_statement)
    # if match:
    #     return match.group(1)
    # return None
    match = re.search(
        r'from\s+tested\s+import\s+(\w+)\s+as\s+\w+',
        import_statement
    )
    if match:
        return match.group(1)  # merge_json_recursive
    match = re.search(
        r'from\s+groundtruth\s+import\s+(\w+)\s+as\s+\w+',
        import_statement
    )
    if match:
        return match.group(1)
    return None

def extract_function_name(function_definition):
    """
    Extracts the function name from a function definition.

    Parameters:
    function_definition (str): The function definition.

    Returns:
    str: The function name.
    """
    # match = re.match(r'^\s*def\s+(\w+)\s*\(.*\):', function_definition)
    # if match:
    #     return match.group(1)
    # return None
    return function_definition.split('(')[0].split()[-1]

def get_func_name(tested_path: str) -> str:
    with open(tested_path, "r") as f:
        for line in f:
            if line.startswith("def "):
                return line.split("def ")[1].split("(")[0]
    return None

def get_method_canonical_uri(relative_path, class_name=None, method_name=None):
    path = relative_path.strip('.py').replace('/', '.')
    if class_name:
        return f'{path}.{class_name}.{method_name}'
    return f'{path}.{method_name}'

def resolve_relative_import(current_module, relative_import):
    current_module_path = current_module.strip('.py').replace('/', '.')
    relative_parts = relative_import.split('.')
    depth = len([part for part in relative_parts if part == ''])
    
    # 计算绝对路径
    base_module = '.'.join(current_module_path.split('.')[:-depth])
    resolved_path = f'{base_module}.' + '.'.join([part for part in relative_parts if part != ''])
    
    return resolved_path

def get_method_alias_uris(relative_path, class_name=None, method_name=None, import_path=None):
    path = relative_path.strip('.py').replace('/', '.')
    aliases = []
    
    if import_path:
        # 如果方法通过__init__.py或其他模块导入
        import_module = import_path.strip('.py').replace('/', '.')
        if class_name:
            aliases.append(f'{import_module}.{class_name}.{method_name}')
        else:
            aliases.append(f'{import_module}.{method_name}')
    
    # 处理 __init__.py 特例
    if path.endswith('.__init__'):
        package_path = path.rstrip('.__init__')
        if class_name:
            aliases.append(f'{package_path}.{class_name}.{method_name}')
        else:
            aliases.append(f'{package_path}.{method_name}')
    
    return aliases

def get_python_method_uris(relative_path, method: Dict = None, class_name='global'):
    if class_name is None:
        class_name = 'global'
    return f"{relative_path}.{class_name}.{method['name']}.{method['args_nums']}"

def get_method_uris(relative_path, class_name=None, method_name=None, import_path=None, current_module=None, relative_import=None):
    """
    生成给定方法或函数的 URI，包括 Canonical URI 和 Alias URIs。

    参数：
    ----------
    
    relative_path : str
        方法或函数所在文件的相对路径（相对于仓库根目录）。用于生成 Canonical URI 的模块路径部分。
    
    class_name : str, 可选
        如果方法属于某个类，则为类的名称。
    
    method_name : str, 可选
        方法或函数的名称。用于生成 URI 的方法或函数名部分。
    
    import_path : str, 可选
        导入路径，表示该方法或函数可能被导入到的其他模块路径。用于生成 Alias URI。
    
    current_module : str, 可选
        当前模块的相对路径（相对于仓库根目录），用于解析相对引用。
    
    relative_import : str, 可选
        相对导入路径，通常以 `.` 或 `..` 开头。用于解析并生成绝对导入路径的 Alias URI。
    
    返回值：
    ----------
    tuple
        包含 Canonical URI 和 Alias URIs 的元组。
        - Canonical URI (str): 方法或函数的标准 URI。
        - Alias URIs (list): 方法或函数可能的其他 URI 别名列表。
    
    示例：
    ----------
    >>> get_method_uris(
            is_in_class=False, 
            relative_path='source_parser/some_module.py', 
            method_name='load_zip_json',
            import_path='source_parser/__init__.py'
        )
    ('source_parser.some_module.load_zip_json', 
     ['source_parser.load_zip_json'])
    
    逻辑：
    ----------
    1. Canonical URI:
       使用 `relative_path`、`class_name` 和 `method_name` 生成唯一的 Canonical URI。
    
    2. Alias URIs:
       使用 `import_path` 生成导入路径对应的 Alias URI。
    
    3. 相对引用解析:
       如果提供了 `relative_import` 和 `current_module`，解析相对导入路径，并添加解析后的路径作为 Alias URI。
    """
    
    # 生成Canonical URI
    canonical_uri = get_method_canonical_uri(relative_path, class_name, method_name)
    
    # 生成Alias URIs
    alias_uris = get_method_alias_uris(relative_path, class_name, method_name, import_path)
    
    # 解析相对引用
    if relative_import and current_module:
        resolved_import = resolve_relative_import(current_module, relative_import)
        alias_uris.append(f'{resolved_import}.{method_name}')
    
    return [canonical_uri] + alias_uris
    # return canonical_uri, alias_uris

def get_class_canonical_uri(relative_path, class_name):
    path = relative_path.strip('.py').replace('/', '.')
    return f'{path}.{class_name}'

def get_class_uris(relative_path, class_name, import_path=None, current_module=None, relative_import=None):
    """
    生成给定类的 URI，包括 Canonical URI 和 Alias URIs。

    参数：
    ----------
    relative_path : str
        类所在文件的相对路径（相对于仓库根目录）。用于生成 Canonical URI 的模块路径部分。

    class_name : str
        类的名称。

    import_path : str, 可选
        导入路径，表示该类可能被导入到的其他模块路径。用于生成 Alias URI。

    current_module : str, 可选
        当前模块的相对路径（相对于仓库根目录），用于解析相对引用。

    relative_import : str, 可选
        相对导入路径，通常以 `.` 或 `..` 开头。用于解析并生成绝对导入路径的 Alias URI。

    返回值：
    ----------
    tuple
        包含 Canonical URI 和 Alias URIs 的元组。
        - Canonical URI (str): 类的标准 URI。
        - Alias URIs (list): 类可能的其他 URI 别名列表。

    示例：
    ----------
    >>> get_class_uris(
            relative_path='source_parser/some_module.py',
            class_name='DataProcessor',
            import_path='source_parser/__init__.py'
        )
    ('source_parser.some_module#DataProcessor', 
     ['source_parser#DataProcessor'])
    """
    
    # 生成Canonical URI
    canonical_uri = get_class_canonical_uri(relative_path, class_name)

    # 生成Alias URIs
    alias_uris = []
    if import_path:
        import_module = import_path.strip('.py').replace('/', '.')
        alias_uris.append(f'{import_module}.{class_name}')
    
    # 处理 __init__.py 特例
    if relative_path.endswith('__init__.py'):
        package_path = relative_path.rstrip('.__init__.py').replace('/', '.')
        alias_uris.append(f'{package_path}.{class_name}')
    
    # 解析相对引用
    if relative_import and current_module:
        resolved_import = resolve_relative_import(current_module, relative_import)
        alias_uris.append(f'{resolved_import}.{class_name}')

    return [canonical_uri] + alias_uris

def extract_typing_imports(type_hints: List[str]) -> str:
    # 定义 typing 模块中的常用类型
    typing_types = {
        "List", "Dict", "Union", "Optional", "Tuple", "Set", "FrozenSet",
        "Callable", "Type", "Any", "Sequence", "Iterable", "Mapping", "Generator"
    }
    
    # 用于存储需要导入的类型
    imports_needed = set()
    
    # 遍历 typing_types，检查是否在 type_hints 中出现
    for typing_type in typing_types:
        if any(typing_type in hint for hint in type_hints):
            imports_needed.add(typing_type)
    
    # 生成 from typing import ... 的导入语句
    if imports_needed:
        return f"from typing import {', '.join(sorted(imports_needed))}"
    return ""

import ast
import textwrap

def extract_python_signature_line(source_code: str) -> str | None:
    """
    Extracts the first line of the function signature (the line starting with 'def')
    from a Python function's source code string using the AST module.

    This function handles leading/trailing whitespace and dedents the code
    to correctly parse snippets that might have inherited indentation.
    It returns the exact line from the source code where the function definition starts,
    which typically includes 'def function_name(...)'.

    Args:
        source_code: A string containing the Python function definition source code.
                     It's assumed to contain at least one top-level function definition.

    Returns:
        The first line of the function signature as a string (including leading
        whitespace from that line in the original snippet) if a top-level
        function definition is found and parsed successfully.
        Returns None if no top-level function definition is found or parsing fails.
    """
    try:
        # Use textwrap.dedent to handle potential indentation in the input snippet
        # and strip leading/trailing whitespace from the overall snippet.
        cleaned_code = textwrap.dedent(source_code).strip()

        # If the cleaned code is empty, there's nothing to parse
        if not cleaned_code:
            return None

        # Parse the cleaned source code into an Abstract Syntax Tree
        tree = ast.parse(cleaned_code)

        # Iterate through the top-level nodes in the AST to find a function definition
        # We look for the first ast.FunctionDef node at the module's body level.
        sig_line = None
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                # Found a function definition. Get its starting line number (1-based).
                start_lineno = node.lineno

                # Get all lines from the cleaned source code
                lines = cleaned_code.splitlines()

                # Extract the specific line corresponding to the start of the function definition
                # AST lineno is 1-based, Python list index is 0-based.
                if 1 <= start_lineno <= len(lines):
                    sig_line = lines[start_lineno - 1]
                    # Optional: Further trim trailing whitespace if desired
                    # sig_line = sig_line.rstrip()
                    return sig_line
                else:
                    # This case should ideally not happen if ast.parse is successful and lineno is valid
                    # but includes a safeguard.
                    print(f"Warning: AST lineno {start_lineno} out of range for {len(lines)} lines in code:\n{cleaned_code[:100]}...")
                    return None

            # Stop after finding the first top-level function definition, as the snippet
            # is expected to represent a single function for the benchmark.
            # Remove 'break' if you needed to find *all* top-level functions, but for this task, first is enough.
            break

        # No top-level function definition found in the code snippet
        return None

    except SyntaxError as e:
        # Handle cases where the input string is not valid Python code
        # print(f"Error parsing Python code for signature extraction: {e}") # Avoid printing in a utility
        return None
    except Exception as e:
        # Catch any other unexpected errors during AST processing
        # print(f"An unexpected error occurred during signature extraction: {e}") # Avoid printing
        return None


if __name__ == '__main__':
    # # 定义在 __init__.py 中的函数：
    # uris = get_method_uris(
    #     relative_path='source_parser/__init__.py',
    #     method_name='load_zip_json'
    # )

    # # 从其他模块导入的函数：
    # canonical_uri, alias_uris = get_method_uris(
    #     is_in_class=False,
    #     relative_path='source_parser/some_module.py',
    #     method_name='load_zip_json',
    #     import_path='source_parser/__init__.py'
    # )

    # # 处理相对引用：
    # canonical_uri, alias_uris = get_method_uris(
    #     is_in_class=False,
    #     relative_path='utils/helper.py',
    #     method_name='calculate_checksum',
    #     current_module='utils/helper.py',
    #     relative_import='.submodule'
    # )
    
    # uris = get_class_uris(
    #     relative_path='source_parser/some_module.py',
    #     class_name='DataProcessor',
    #     import_path='source_parser/__init__.py',
    #     current_module='source_parser/some_module.py',
    #     relative_import='..helpers'
    # )

    # print(uris)
    
    # type_hints = ['int', 'Dict[str, Dict[str, Union[int, bool]]]', 'str', 'List[str]']
    # import_statement = extract_typing_imports(type_hints)
    # print(import_statement)
    
    
    # --- Example Usage ---
    code_snippet1 = """
    def my_simple_function(x, y):
        \"\"\"A simple function.\"\"\"
        return x + y
    """

    code_snippet2 = """
    @decorator
    def another_function(
        arg1: int, # first argument
        arg2: str = "default" # second argument
    ) -> str:
        \"\"\"Multi-line signature with decorators.\"\"\"
        # Some implementation
        pass
    """ # AST reports the line number where 'def another_function' is located.

    code_snippet3 = """
        # Some comment before
        def single_line(): return True # Implementation on same line
    """ # dedent handles leading whitespace. AST finds the line with 'def'.

    code_snippet4 = """
    # Just a comment
    """ # No function definition.

    code_snippet5 = """
    class MyClass:
        def method(self):
            pass
    """ # Nested function definition (a method), not a top-level function in the module body.

    print("--- Testing Python Signature Line Extraction ---")
    print(f"Snippet 1 Signature: '{extract_python_signature_line(code_snippet1)}'")
    print(f"Snippet 2 Signature: '{extract_python_signature_line(code_snippet2)}'")
    print(f"Snippet 3 Signature: '{extract_python_signature_line(code_snippet3)}'")
    print(f"Snippet 4 Signature: '{extract_python_signature_line(code_snippet4)}'")
    print(f"Snippet 5 Signature: '{extract_python_signature_line(code_snippet5)}'") # Should return None
