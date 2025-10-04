import ast

def scrape_python_blocks(source_code: str, file_path_for_logging: str) -> list:
    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return []
    
    blocks = []
    
    def visit(node):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.If, ast.Try)):
            block_start = ""
            if isinstance(node, ast.ClassDef):
                block_start += f"class {node.name}:\n"
            elif isinstance(node, ast.FunctionDef):
                block_start += f"def {node.name}(\n"
            elif isinstance(node, ast.If):
                block_start += "if "
                block_start += " ".join(ast.get_source_segment(source_code, node.test))
                block_start += ":\n"
            elif isinstance(node, ast.Try):
                block_start += "try:\n"
            
            block_content = ""
            for child in ast.walk(node):
                if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.If, ast.Try)):
                    continue
                if isinstance(child, ast.Expr):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Assign):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.AnnAssign):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.For):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.While):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.With):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Assert):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Delete):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Pass):
                    block_content += "    pass\n"
                elif isinstance(child, ast.Break):
                    block_content += "    break\n"
                elif isinstance(child, ast.Continue):
                    block_content += "    continue\n"
                elif isinstance(child, ast.Raise):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Return):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Yield):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.YieldFrom):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Global):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Nonlocal):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Import):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ImportFrom):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Expression):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Compare):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.BoolOp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.UnaryOp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.BinOp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ExtSlice):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Slice):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Subscript):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Attribute):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Name):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Num):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Str):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Bytes):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Ellipsis):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.FormattedValue):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.JoinedStr):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Constant):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Arg):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.keyword):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.alias):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.comprehension):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.arguments):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.arg):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.withitem):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.excepthandler):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ExceptHandler):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.IfExp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ListComp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.SetComp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.DictComp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.GeneratorExp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Dict):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Set):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Tuple):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.List):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.NameConstant):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Lambda):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Call):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Repr):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Slice):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ExtSlice):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.UnaryOp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.BinOp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Compare):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.BoolOp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.operator):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.cmpop):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.expr):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.stmt):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.annassign):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.alias):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.comprehension):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.arguments):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.arg):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.withitem):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.excepthandler):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ExceptHandler):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.IfExp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ListComp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.SetComp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.DictComp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.GeneratorExp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Dict):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Set):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Tuple):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.List):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.NameConstant):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Lambda):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Call):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Repr):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Slice):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ExtSlice):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.UnaryOp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.BinOp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Compare):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.BoolOp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.operator):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.cmpop):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.expr):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.stmt):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.annassign):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.alias):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.comprehension):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.arguments):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.arg):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.withitem):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.excepthandler):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ExceptHandler):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.IfExp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ListComp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.SetComp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.DictComp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.GeneratorExp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Dict):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Set):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Tuple):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.List):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.NameConstant):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Lambda):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Call):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Repr):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Slice):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ExtSlice):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.UnaryOp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.BinOp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Compare):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.BoolOp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.operator):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.cmpop):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.expr):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.stmt):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.annassign):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.alias):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.comprehension):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.arguments):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.arg):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.withitem):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.excepthandler):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ExceptHandler):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.IfExp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.ListComp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.SetComp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.DictComp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.GeneratorExp):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Dict):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Set):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Tuple):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.List):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.NameConstant):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Lambda):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Call):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif isinstance(child, ast.Repr):
                    block_content += "    " + ast.unparse(child) + "\n"
                elif