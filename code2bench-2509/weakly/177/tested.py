import re
import ast
from typing import List

def deduplicate(solutions: List[str]) -> List[str]:
    def strip_comments_and_docstrings(code: str) -> str:
        code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
        code = re.sub(r"'.*?'", '', code)
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        return code.strip()
    
    def get_ast_hash(code: str) -> str:
        try:
            stripped_code = strip_comments_and_docstrings(code)
            tree = ast.parse(stripped_code)
            return ast.dump(tree, annotate_fields=False)
        except (SyntaxError, MemoryError):
            return None
    
    seen = {}
    result = []
    
    for solution in solutions:
        hash_key = get_ast_hash(solution)
        if hash_key is not None and hash_key not in seen:
            seen[hash_key] = True
            result.append(solution)
    
    return result