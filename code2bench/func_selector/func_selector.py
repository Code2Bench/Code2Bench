import ast
import textwrap
from typing import Dict, List, Set, Union
import json

from code2bench.config import config
from code2bench.program_analysis.cfg.cfg_builder import check_non_none_non_constant_return
from code2bench.program_analysis.cyclomatic_complexity.cyclomatic_complexity_analyzer import analyze_cyclomatic_complexity
from code2bench.program_analysis.scope_graph import get_unresolved_refs
from code2bench.program_analysis.git.analyse_commit_time import analyze_commit_changes
from code2bench.program_analysis.source_parse.query_parser import extract_function_calls
from code2bench.utils.json_utils import load_json, save_json
from code2bench import logger

class FunctionSelector:
    def __init__(self, method_metainfo: List[Dict], allowed_libraries: Set[str] = None,
                 file_metainfo: List[Dict] = None):
        """
        初始化FunctionSelector。
        :param method_metainfo: 方法元信息列表，每个方法是一个字典。
        :param allowed_libraries: 允许的外部库集合，用于判断弱自包含函数。
        """
        self.method_metainfo = method_metainfo
        self.file_metainfo = file_metainfo
        self.allowed_libraries = allowed_libraries
        self.allowed_modules_dict = config.ALLOWED_MODULES
        self.allowed_modules = set(self.allowed_modules_dict.keys())
        self.self_contained_functions = set()
        self.modified_methods = set()

    def check_function_containment(self, func: str, file_path: str, file_info: Dict = None) -> Union[bool, Set[str]]:
        """
        判断函数是完全自包含、弱自包含还是非自包含，并返回相应信息。
        :param func: 函数的源代码字符串。
        :return: 如果是完全自包含，返回 True；如果是弱自包含，返回未解析的引用集合；如果都不是，返回空集合。
        """
        unresolved_refs = set(get_unresolved_refs(code=func))
        # 完全自包含的情况
        if not unresolved_refs:
            return True

        # 弱自包含的情况
        if unresolved_refs.issubset(self.allowed_libraries):
            return unresolved_refs
        cnt = 0
        truly_imports = set()
        if file_info is not None:
            for ref in unresolved_refs:
                _imports = file_info["_import"]
                _import_froms = file_info["_import_from"]
                _imports = _imports + _import_froms
                for item in _imports:
                    if len(list(item.values())[0]) == 0:
                        continue
                    
                    _dict = list(item.values())[0][0]
                    if "alias" in _dict:
                        alias = _dict['alias']
                        if ref == alias:
                            _from = _dict['from'].split(".")[0]
                            if _from in self.allowed_libraries:
                                truly_imports.add(list(item.keys())[0])
                                cnt += 1
                    else:
                        what = _dict['what']
                        if ref == what:
                            _from = _dict['from'].split(".")[0]
                            if _from in self.allowed_libraries:
                                truly_imports.add(list(item.keys())[0])
                                cnt += 1
        
        if cnt == len(unresolved_refs):
            return truly_imports
        return set()

    def is_instance_method(self, method: Dict) -> bool:
        return method["params"] and (method["params"][0] == "self" or method["params"][0] == "cls")

    def get_modified_methods(self, start_time: str, end_time: str) -> List[str]:
        """
        Input Format:
            start_date = '2024-9-30'
            end_date = '2024-12-02'
        Output:
            changed_uris = ['class_name.method_name', ...]
        """
        modified_methods = analyze_commit_changes(config.REPO_PATH, start_time, end_time, config.ALL_METAINFO_PATH)
        self.modified_methods: List[str] = modified_methods
        # dump modified methods to a file
        save_json(config.MODIFIED_METHODS_PATH, {"modified_methods": modified_methods})
        logger.info("Modified methods saved.")

    def run(self, output_to_file: bool, 
            self_contained_file: str,
            self_contained_class_method_file: str,
            weakly_self_contained_file: str,
            txt_output: bool = False):
        """
        筛选出self-contained和weakly self-contained的函数，并根据是否是类的方法区分输出。
        :param output_to_file: 是否输出到文件，默认为 False。
        :param self_contained_file: 非类方法的自包含函数输出文件。
        :param self_contained_class_method_file: 类方法的自包含函数输出文件。
        :param weakly_self_contained_file: 弱自包含函数输出文件。
        """
        self_contained_output = []
        self_contained_class_method_output = []
        weakly_self_contained_output = []

        for method in self.method_metainfo:
            original_string = method["original_string"]
            uris = method["uris"]
            
            if uris not in self.modified_methods:
                continue
            
            if has_non_basic_type_hint(original_string):
                continue
            
            file_info = None
            for file in self.file_metainfo:
                if file["file_path"] == method['file']:
                    file_info = file
                    break

            containment_result = self.check_function_containment(
                original_string, method['file'], file_info=file_info)

            if containment_result is True:
                if self.is_instance_method(method):
                    self_contained_class_method_output.append({
                        "type": "class_method",
                        "uris": uris,
                        "arg_nums": method["arg_nums"],
                        "code": original_string
                    })
                else:
                    self_contained_output.append({
                        "type": "function",
                        "uris": uris,
                        "arg_nums": method["arg_nums"],
                        "code": original_string
                    })
            elif containment_result:
                if self.is_instance_method(method):
                    continue

                weakly_self_contained_output.append({
                    "type": "weakly_self_contained",
                    "uris": uris,
                    "arg_nums": method["arg_nums"],
                    "allowed_libraries": list(containment_result),
                    "code": original_string
                })

        # 如果需要输出到文件
        if output_to_file:
            save_json(self_contained_file, self_contained_output)
            save_json(self_contained_class_method_file, self_contained_class_method_output)
            save_json(weakly_self_contained_file, weakly_self_contained_output)
        else:
            print("Self-contained functions:")
            print(json.dumps(self_contained_output, indent=4))
            print("Self-contained class methods:")
            print(json.dumps(self_contained_class_method_output, indent=4))
            print("Weakly self-contained functions:")
            print(json.dumps(weakly_self_contained_output, indent=4))
        
        if txt_output:
            with open(config.SELF_COTAINED_PATH.replace(".json", ".txt"), "w") as f:
                for func in self_contained_output:
                    f.write(func["type"] + ": " + func["uris"] + "\n")
                    f.write(func["code"] + "\n\n")
            with open(config.SELF_COTAINED_CLASS_METHOD_PATH.replace(".json", ".txt"), "w") as f:
                for func in self_contained_class_method_output:
                    f.write(func["type"] + ": " + func["uris"] + "\n")
                    f.write(func["code"] + "\n\n")
            with open(config.WEAKLY_SELF_COTAINED_PATH.replace(".json", ".txt"), "w") as f:
                for func in weakly_self_contained_output:
                    f.write(func["type"] + ": " + func["uris"] + "\n")
                    f.write(', '.join(func["allowed_libraries"]) + "\n")
                    f.write(func["code"] + "\n\n")
            
        logger.info("Function selection completed.")

    def check_one_level_containment(
        self, 
        method_metainfo: List[Dict],
        self_contained_functions: List[Dict],
        level: int = 1,
        level_self_contained_path: str = "",
        level_self_contained_class_method_path: str = "",
        level_weakly_self_contained_path: str = "",
        txt_output: bool = False,
    ):
        """
        筛选具有一层函数调用的函数是否为自包含，比如一个函数调用了另一个自包含的函数，
        那么这个函数也可以认为是自包含的。
        :param func: 函数的源代码字符串。
        :return: 如果是自包含或弱自包含，返回 True；否则返回 False。
        """
        self.self_contained_functions = self_contained_functions
        target_functions = {f["code"].split('(')[0].split()[-1]: f["arg_nums"] for f in self_contained_functions}
        target_func_name_to_func = {f["code"].split('(')[0].split()[-1]: f for f in self_contained_functions}
        one_level_self_contained_class_method_output = []
        one_level_self_contained_output = []
        one_level_weakly_self_contained_output = []
        
        for method in method_metainfo:
            if method['uris'] not in self.modified_methods:
                continue

            original_string = method["original_string"]
            if has_non_basic_type_hint(original_string):
                continue

            func_calls, arg_counts = extract_function_calls(source_code=original_string, target_funcs=target_functions.keys())
            if func_calls and arg_counts:
                unresolved_refs = get_unresolved_refs(code=original_string)
                    
                if set(unresolved_refs) - set(target_functions) - self.allowed_libraries:
                    # 如果除了target_functions和allowed_libraries还有别人，就continue
                    continue
                
                allowed_lib_intersetction = set(unresolved_refs) & self.allowed_libraries
                target_func_intersection = set(unresolved_refs) & set(target_functions)
                # 如果只有target_functions，没有allowed_libraries:
                if (
                    (not (allowed_lib_intersetction)) and
                    target_func_intersection
                ):
                    for func_call, arg_count in zip(func_calls, arg_counts):
                        if func_call in target_functions and arg_count == target_functions[func_call]:
                            if self.is_instance_method(method):
                                one_level_self_contained_class_method_output.append({
                                    "type": "class_method",
                                    "uris": method['uris'],
                                    "level": level,
                                    "arg_nums": method["arg_nums"],
                                    "func_call": target_func_name_to_func[func_call],
                                    "code": original_string
                                })
                            else:
                                one_level_self_contained_output.append({
                                    "type": "function",
                                    "uris": method['uris'],
                                    "level": level,
                                    "arg_nums": method["arg_nums"],
                                    "func_call": target_func_name_to_func[func_call],
                                    "code": original_string
                                })
                # 如果又有target_functions，又有allowed_libraries:
                if (
                    allowed_lib_intersetction and
                    target_func_intersection
                ):
                    for func_call, arg_count in zip(func_calls, arg_counts):
                        if func_call in target_functions and arg_count == target_functions[func_call]:
                            if self.is_instance_method(method):
                                # one_level_self_contained_class_method_output.append({
                                #     "type": "class_method",
                                #     "uris": method['uris'],
                                #     "arg_nums": method["arg_nums"],
                                #     "allowed_libraries": list(allowed_lib_intersetction),
                                #     "func_call": target_func_name_to_func[func_call],
                                #     "code": original_string
                                # })
                                pass
                            else:
                                one_level_weakly_self_contained_output.append({
                                    "type": "function",
                                    "uris": method['uris'],
                                    "level": level,
                                    "arg_nums": method["arg_nums"],
                                    "allowed_libraries": list(allowed_lib_intersetction),
                                    "func_call": target_func_name_to_func[func_call],
                                    "code": original_string
                                })
        
        save_json(level_self_contained_path, one_level_self_contained_output)
        logger.info(f"level {level} self-contained functions saved.")
        save_json(level_self_contained_class_method_path, one_level_self_contained_class_method_output)
        logger.info(f"level {level} self-contained class methods saved.")
        save_json(level_weakly_self_contained_path, one_level_weakly_self_contained_output)
        logger.info(f"level {level} weakly self-contained functions saved.")
        if txt_output:
            with open(level_self_contained_path.replace(".json", ".txt"), "w") as f:
                for func in one_level_self_contained_output:
                    f.write(func["type"] + ": " + func["uris"] + "\n")
                    f.write(func["func_call"]["code"] + "\n")
                    f.write(func["code"] + "\n\n")
            with open(level_self_contained_class_method_path.replace(".json", ".txt"), "w") as f:
                for func in one_level_self_contained_class_method_output:
                    f.write(func["type"] + ": " + func["uris"] + "\n")
                    f.write(func["func_call"]["code"] + "\n")
                    f.write(func["code"] + "\n\n")
            with open(level_weakly_self_contained_path.replace(".json", ".txt"), "w") as f:
                for func in one_level_weakly_self_contained_output:
                    f.write(func["type"] + ": " + func["uris"] + "\n")
                    f.write(func["func_call"]["code"] + "\n")
                    f.write(', '.join(func["allowed_libraries"]) + "\n")
                    f.write(func["code"] + "\n\n")

        logger.info(f"level {level} containment check completed.")



import re
from typing import Tuple, Optional, List, Dict  # 引入一些常见的 Type Hint，方便后续判断

def _is_non_basic_type(type_hint_str: str, basic_types: set) -> bool:
    """
    递归检查类型提示字符串是否包含非基本类型。

    Args:
        type_hint_str: 类型提示字符串，例如 "Tuple[int, DataFrame]"
        basic_types: 基本类型集合

    Returns:
        bool: 如果类型提示字符串中包含非基本类型，则返回 True，否则返回 False。
    """
    type_hint_str = type_hint_str.strip()
    if not type_hint_str:
        return False

    if '[' in type_hint_str and ']' in type_hint_str: # 泛型类型
        base_type = type_hint_str.split('[')[0].strip()
        if base_type not in basic_types and base_type not in ["List", "Tuple", "Optional", "Dict", "Iterable"]: #  添加 "Iterable"
            return True

        inner_type_str = type_hint_str[len(base_type)+1:-1]
        inner_types = []
        bracket_level = 0
        current_type = ''
        for char in inner_type_str:
            if char == '[':
                bracket_level += 1
                current_type += char
            elif char == ']':
                bracket_level -= 1
                current_type += char
            elif char == ',' and bracket_level == 0: # 只在顶层逗号分割
                inner_types.append(current_type.strip())
                current_type = ''
            else:
                current_type += char
        inner_types.append(current_type.strip())

        for inner_type in inner_types:
            if _is_non_basic_type(inner_type, basic_types):
                return True
        return False

    else: # 基本类型或类型参数
        base_type = type_hint_str.split('.')[0].strip()
        # 修改：如果类型名以 _ 开头，也认为是 Non-basic type (TypeVar)
        if base_type.startswith('_'):
            return True
        return base_type not in basic_types

def has_non_basic_type_hint(func_str: str) -> bool:
    return contains_any_non_basic_type_hint(func_str)

import ast
from typing import List, Dict, Union, Any # Import necessary types for the example

def extract_all_type_hints(func_str: str) -> List[str]:
    """
    Extracts all type hints from a Python function's source code string,
    including parameters, return type, and variable annotations within the body.

    Args:
        func_str: A string containing the source code of a Python function.

    Returns:
        A list of strings, where each string is a type hint found in the function.
    """
    type_hints: List[str] = []

    try:
        # Remove extra indentation
        func_str = textwrap.dedent(func_str)
        # Parse the function string into an AST node
        tree = ast.parse(func_str)
    except SyntaxError as e:
        print(f"Error parsing function string: {e}")
        return []

    # Find the function definition node. We assume the string contains exactly one.
    func_def = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_def = node
            break
        # Also check for async function definitions
        if isinstance(node, ast.AsyncFunctionDef):
            func_def = node
            break


    if func_def is None:
        print("No function definition found in the string.")
        return []

    # --- Extract type hints from the function signature ---

    # Parameters
    for arg in func_def.args.args:
        if arg.annotation:
            # ast.unparse converts the AST node back to source code string (Python 3.9+)
            # For older Python, you'd need to manually reconstruct the string
            try:
                 type_hints.append(ast.unparse(arg.annotation).strip())
            except AttributeError: # Fallback for older Python versions
                 type_hints.append(ast.dump(arg.annotation).strip()) # This is less readable, just for demonstration

    # Keyword-only arguments
    for arg in func_def.args.kwonlyargs:
        if arg.annotation:
             try:
                 type_hints.append(ast.unparse(arg.annotation).strip())
             except AttributeError:
                 type_hints.append(ast.dump(arg.annotation).strip())

    # Position-only arguments (Python 3.8+)
    if hasattr(func_def.args, 'posonlyargs'):
        for arg in func_def.args.posonlyargs:
            if arg.annotation:
                 try:
                    type_hints.append(ast.unparse(arg.annotation).strip())
                 except AttributeError:
                    type_hints.append(ast.dump(arg.annotation).strip())


    # Return type
    if func_def.returns:
         try:
            type_hints.append(ast.unparse(func_def.returns).strip())
         except AttributeError:
            type_hints.append(ast.dump(func_def.returns).strip())

    # --- Extract type hints from variable annotations within the function body ---

    # Walk through all nodes in the function body
    for node in ast.walk(func_def):
        # Look for AnnAssign nodes (like `var: Type = value` or `var: Type`)
        if isinstance(node, ast.AnnAssign):
            if node.annotation:
                 try:
                    type_hints.append(ast.unparse(node.annotation).strip())
                 except AttributeError:
                    type_hints.append(ast.dump(node.annotation).strip())

    # Use a set to get unique hints, then convert back to list
    unique_hints = list(set(type_hints))

    return unique_hints

def contains_any_non_basic_type_hint(func_str: str) -> bool:
    """
    检查函数字符串中（签名或体内部）是否包含任何非基本类型提示。
    使用 AST 进行提取，并使用 _is_non_basic_type 进行分类。
    """
    all_type_hints = extract_all_type_hints(func_str)

    basic_types = {
        "int", "str", "bool", "float", "List", "Tuple", "Optional", "Dict", "None", "Iterable",
        "list", "tuple", "optional", "dict", "iterable",
        "typing.List", "typing.Tuple", "typing.Optional", "typing.Dict", "typing.Union", "typing.Iterable",
        "Any", "typing.Any", # 添加 Any，通常也算作某种“基本”或通配类型
    } # 你可以根据需要完善这个基本类型集合

    for hint in all_type_hints:
        # 确保提示字符串不为空，有时候 ast.unparse 可能会产生空字符串或其他意外
        if hint and _is_non_basic_type(hint, basic_types):
            return True

    return False

# filter装饰器, 过滤掉有@classmethod, @staticmethod 装饰器的函数    
def filter_decorators(source_code):
    """
    找出带有 @classmethod 和 @staticmethod 装饰器的函数。
    :param source_code: 源代码字符串。
    :return: 带有指定装饰器的函数名列表。
    """
    class DecoratorFinder(ast.NodeVisitor):
        def __init__(self):
            self.decorated_functions = []

        def visit_FunctionDef(self, node):
            # 检查函数是否有 @classmethod 或 @staticmethod 装饰器
            if any(isinstance(decorator, ast.Name) and decorator.id in {"classmethod", "staticmethod"} for decorator in node.decorator_list):
                self.decorated_functions.append(node.name)
            self.generic_visit(node)

    source_code = textwrap.dedent(source_code)
    try:
        tree = ast.parse(source_code)
    except Exception as e:
        return True
    finder = DecoratorFinder()
    finder.visit(tree)
    return finder.decorated_functions


def filter_return(file_path, output_file_path):
    """
    进一步筛选文件中的函数，只保留返回值不为 None 的函数，并将结果保存为 JSON 格式。
    :param file_path: 输入文件路径（JSON 格式）。
    :param output_file_path: 输出文件路径（JSON 格式）。
    """
    # 从 JSON 文件中加载数据
    functions = load_json(file_path)
    # if not functions:
    #     print(f"No data loaded from {file_path}")
    #     return

    valid_functions = []
    for func in functions:
        source_code = func.get("code", "")

        # 过滤掉带有 @classmethod 和 @staticmethod 装饰器的函数
        if filter_decorators(source_code):
            continue
        
        # 检查返回值是否为非 None 且非常量
        if check_non_none_non_constant_return(source_code):
            # 计算圈复杂度
            cyclomatic_complexity = analyze_cyclomatic_complexity(source_code)
            
            # 构造函数信息字典
            function_info = {
                **func,
                "cyclomatic_complexity": cyclomatic_complexity,
            }
            # 添加到有效函数列表
            valid_functions.append(function_info)

    # 将筛选后的函数信息保存为 JSON 文件
    save_json(output_file_path, valid_functions)
    with open(output_file_path.replace(".json", ".txt"), "w") as f:
        for func in valid_functions:
            f.write(str(func["type"]) + ": " + str(func["uris"]) + "\n")
            f.write("Cyclomatic complexity: " + str(func["cyclomatic_complexity"]) + "\n")
            if "func_call" in func:
                f.write("Function call: \n" + str(func["func_call"]) + "\n")
            f.write(func["code"] + "\n\n")
    logger.info(f"Function return filtering completed for {output_file_path}")

def select_function(start_time: str = "", end_time: str = ""):
    """
    主函数，加载方法元信息并运行筛选器。
    """
    # 加载方法元信息
    method_metainfo = load_json(config.METHOD_METAINFO_PATH)
    file_metainfo = load_json(config.FILE_METAINFO_PATH)
    # 定义允许的外部库
    # allowed_libraries = {"math", "numpy", "json"}  # 可根据需求扩展
    allowed_libraries = config.ALLOWED_LIBRARIES
    # 初始化筛选器
    fc = FunctionSelector(method_metainfo, allowed_libraries, file_metainfo)

    if start_time and end_time:
        # 获取指定时间范围内的修改方法
        fc.get_modified_methods(start_time=start_time, end_time=end_time)

    # 运行筛选器
    fc.run(output_to_file=True, self_contained_file=config.SELF_COTAINED_PATH,
           self_contained_class_method_file=config.SELF_COTAINED_CLASS_METHOD_PATH,
           weakly_self_contained_file=config.WEAKLY_SELF_COTAINED_PATH,
           txt_output=True)
    filter_return(config.SELF_COTAINED_PATH, config.FILTERED_SELF_COTAINED_PATH)
    filter_return(config.WEAKLY_SELF_COTAINED_PATH, config.WEAKLY_SELF_COTAINED_PATH)
    
    self_contained_functions = load_json(config.FILTERED_SELF_COTAINED_PATH)
    fc.check_one_level_containment(
        method_metainfo, self_contained_functions, level=1,
        level_self_contained_path=config.ONE_LEVEL_SELF_CONTAINED_PATH,
        level_self_contained_class_method_path=config.ONE_LEVEL_SELF_CONTAINED_CLASS_METHOD_PATH,
        level_weakly_self_contained_path=config.ONE_LEVEL_WEAKLY_SELF_CONTAINED_PATH,
        txt_output=True)
    filter_return(config.ONE_LEVEL_SELF_CONTAINED_PATH, config.ONE_LEVEL_SELF_CONTAINED_PATH)
    filter_return(config.ONE_LEVEL_WEAKLY_SELF_CONTAINED_PATH, config.ONE_LEVEL_WEAKLY_SELF_CONTAINED_PATH)
    
    one_level_self_contained_functions = load_json(config.ONE_LEVEL_SELF_CONTAINED_PATH)
    fc.check_one_level_containment(
        method_metainfo, one_level_self_contained_functions, level=2, 
        level_self_contained_path=config.TWO_LEVEL_SELF_CONTAINED_PATH, 
        level_self_contained_class_method_path=config.TWO_LEVEL_SELF_CONTAINED_CLASS_METHOD_PATH, 
        level_weakly_self_contained_path=config.TWO_LEVEL_WEAKLY_SELF_CONTAINED_PATH, 
        txt_output=True
    )
    filter_return(config.TWO_LEVEL_SELF_CONTAINED_PATH, config.TWO_LEVEL_SELF_CONTAINED_PATH)
    filter_return(config.TWO_LEVEL_WEAKLY_SELF_CONTAINED_PATH, config.TWO_LEVEL_WEAKLY_SELF_CONTAINED_PATH)

if __name__ == "__main__":
    # select_function()
    # process_loaded_data()
    
    func_str = """
def _get_correct_indent_level(lines: List[str], line_index: int) -> str:
    # Look at previous line's indentation first
    if line_index > 0:
        prev_line = lines[line_index - 1].rstrip()
        if prev_line and not prev_line.endswith(","):  # Ignore continuation lines
            return prev_line[: len(prev_line) - len(prev_line.lstrip())]

    # Look backward for containing blocks
    for i in range(line_index - 1, -1, -1):
        line = lines[i].rstrip()
        if not line:  # Skip empty lines
            continue
        # Get the indentation of this line
        curr_indent: Dict[str, Dict[str, Union[int, bool]]] = line[: len(line) - len(line.lstrip())]
        # If the line starts with 8+ spaces, it was probably properly nested
        if len(line) - len(line.lstrip()) >= 8:
            return line[: len(line) - len(line.lstrip())]
        # If we find a class or function definition, use its base indentation
        if line.lstrip().startswith(("def ", "class ", "async def ")):
            return curr_indent + "  "  # One level deeper than definition

        # If line ends with colon, use its indentation level
        if line.endswith(":"):
            return curr_indent + "  "  # One level deeper than block starter

    # Default to base level if we couldn't determine
    return ""
"""
    
    # type_hints = extract_all_type_hints(func_str=func_str)
    # print(type_hints)
    
    config.PROJECT_NAME = "BentoML"
    select_function(
        start_time='2024-08-01', end_time='2025-05-30'
    )
    