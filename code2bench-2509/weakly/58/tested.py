import re
import json
from typing import Optional

def _parsing_score(grade_stdout: str) -> Optional[float]:
    for line in grade_stdout.splitlines():
        if "score" in line:
            try:
                # Try JSON parsing
                score_dict = json.loads(line)
                return float(score_dict.get("score", 0))
            except json.JSONDecodeError:
                pass
            try:
                # Try evaluating as a dictionary
                exec(f"score_dict = {line}")
                return float(score_dict.get("score", 0))
            except (SyntaxError, NameError, KeyError):
                pass
            # Try regex to extract the last number
            match = re.search(r"(\d+\.\d+|\d+)$", line)
            if match:
                return float(match.group(1))
    return None