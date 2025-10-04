from typing import Optional
import re
import json

def _parsing_score(grade_stdout: str) -> Optional[float]:
    for line in grade_stdout.splitlines():
        line = line.strip()
        if "score" not in line:
            continue
        m = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", line)
        if not m:
            continue
        json_str = m.group(0)
        try:
            # Priority 1: JSON parsing
            return float(json.loads(json_str)["score"])
        except:
            pass
        try:
            # Priority 2: Eval dict
            return float(eval(json_str)["score"])
        except:
            pass
        try:
            # Priority 3: Regex for the last number in the string
            return float(re.findall(r"[-+]?\d*\.\d+|\d+", json_str)[-1])
        except:
            pass
    return None