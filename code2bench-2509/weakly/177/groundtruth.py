from typing import List
import ast
import re

import re
import ast
from typing import List

def deduplicate(solutions: List[str]) -> List[str]:
    asts = set()
    deduplicated = []
    for solution in solutions:
        solution = re.sub(r"#[^\n]*", "", solution)
        solution = re.sub(r'"""[^"]*"""', "", solution)
        solution = re.sub(r"'''[^']*'''", "", solution)
        try:
            ast_string = ast.dump(ast.parse(solution))
        except SyntaxError:
            continue
        except MemoryError:
            continue
        if ast_string not in asts:
            asts.add(ast_string)
            deduplicated.append(solution)
    return list(deduplicated)