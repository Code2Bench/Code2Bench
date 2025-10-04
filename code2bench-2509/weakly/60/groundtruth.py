
import ast
import re

def extract_first_section_name_from_code(source_code):
    """
    Extract the first section name from the source code.
    """
    parsed = ast.parse(source_code)
    for node in ast.walk(parsed):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            if getattr(call.func, "id", None) == "print" and call.args:
                arg0 = call.args[0]
                if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                    # Match "Section: ..." pattern
                    m = re.match(r"Section:\s*(.+)", arg0.value)
                    if m:
                        return m.group(1).strip()
    return None