import textwrap
from scalpel.cfg import CFGBuilder
import ast
import astor


def add_return_none(source_code):
    """
    在函数的最后添加一个 return None
    """
    class ReturnNoneAdder(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            # 检查函数体的最后一个语句是否是 return 语句
            if not node.body or not isinstance(node.body[-1], ast.Return):
                # 如果不是 return 语句，则添加 return None
                node.body.append(ast.Return(value=ast.Constant(value=None)))
            return node

    source_code = textwrap.dedent(source_code)
    tree = ast.parse(source_code)
    tree = ReturnNoneAdder().visit(tree)
    return astor.to_source(tree)

# def check_non_none_return(source_code):
#     source_code = textwrap.dedent(source_code)
#     add_return_none(source_code)
#     cfg = CFGBuilder().build_from_src("test", source_code)

#     for (block_id, fun_name), fun_cfg in cfg.functioncfgs.items():
#         for block in fun_cfg.finalblocks:
#             has_non_none_return = False
#             for stmt in block.statements:
#                 if isinstance(stmt, ast.Return):
#                     if stmt.value is not None:
#                         if not (isinstance(stmt.value, ast.Constant) and stmt.value.value is None):
#                             if not (isinstance(stmt.value, ast.Str) and stmt.value.s):
#                                 has_non_none_return = True
#                                 break
#             if not has_non_none_return:
#                 return False
#     return True

def is_constant_expression(node):
    """
    Recursively checks if an AST node represents a constant expression.
    Handles constant literals and constant composite types (list, dict, tuple, set) recursively.
    """
    if isinstance(node, ast.Constant):
        return True
    elif isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        # Check if all elements in list/tuple/set are constant expressions
        return all(is_constant_expression(elt) for elt in node.elts)
    elif isinstance(node, ast.Dict):
        # Check if all keys and values in dict are constant expressions
        return all(is_constant_expression(key) and is_constant_expression(value)
                   for key, value in zip(node.keys, node.values) if key is not None) # Handle None keys in dict
    elif node is None: # Allow None as a constant (e.g., for default dict keys)
        return True
    else:
        return False # Not a constant expression

# def check_non_none_non_constant_return(source_code):
#     source_code = textwrap.dedent(source_code)
#     cfg = CFGBuilder().build_from_src("test", source_code)

#     for (block_id, fun_name), fun_cfg in cfg.functioncfgs.items():
#         for block in fun_cfg.finalblocks:
#             has_non_none_non_constant_return = False
#             for stmt in block.statements:
#                 if isinstance(stmt, ast.Return):
#                     if stmt.value is not None:
#                         if not is_constant_expression(stmt.value): # Use the new helper function
#                             has_non_none_non_constant_return = True
#                             break
#             if not has_non_none_non_constant_return:
#                 return False
#     return True

def check_non_none_non_constant_return(source_code):
    source_code = textwrap.dedent(source_code)
    cfg = CFGBuilder().build_from_src("test", source_code)

    for (block_id, fun_name), fun_cfg in cfg.functioncfgs.items():
        has_explicit_return = False  # 标记是否有显式 return
        for block in fun_cfg.finalblocks:
            for stmt in block.statements:
                if isinstance(stmt, ast.Return):
                    has_explicit_return = True  # 找到显式 return
                    if stmt.value is not None:
                        if not is_constant_expression(stmt.value):
                            return True # 找到非 None 非常量 return, 直接返回 True
                    break # 找到 return 语句，不需要再检查这个 block 的其他语句了
            if has_explicit_return: # 如果这个 final block 有 return, 继续检查下一个 final block
                continue

    if not has_explicit_return: # 遍历完所有 final blocks, 没有找到任何显式 return
        return False # 可以认为函数没有显式 return (或者只有隐式 None return)

    return False # 如果遍历完所有函数，都没有返回 True，则返回 False (表示没有找到非 None 非常量 return)


if __name__ == "__main__":

    source_code_valid = """
def use_cuda_graph_recommendation() -> str:
    return "of the operation"
    """

    source_code_invalid_none_return = """
    def example_invalid_none():
        return None
    """

    source_code_invalid_no_return = """
    def example_invalid_no_return(x):
        if x > 0:
            return "positive"
    """

    print(check_non_none_return(source_code_valid))  # True
    # print(check_non_none_return(source_code_invalid_none_return))  # False
    # print(check_non_none_return(source_code_invalid_no_return))  # False

    # # 测试 add_return_none 函数
    # modified_code = add_return_none(source_code_invalid_no_return)
    # print(modified_code)
    # print(check_non_none_return(modified_code))  # True