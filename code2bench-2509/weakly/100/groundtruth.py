
import re
import ast

def safe_literal_eval(s):
    s = s.strip()
    try:
        return ast.literal_eval(s)
    except:
        pass
    if not s.startswith("{"):
        s = "{" + s
    if not s.endswith("}"):
        s = s + "}"
    s = re.sub(r'([{,]\s*)([^"\{\}\:\,\s]+)\s*:', r'\1"\2":', s)
    try:
        return ast.literal_eval(s)
    except:
        return None