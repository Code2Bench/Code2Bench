
import json
import re

def extract_answer_obj(s: str):
    if "<|begin_of_box|>" not in s or "<|end_of_box|>" not in s:
        return None
    try:
        res = s.split("<|begin_of_box|>")[1].split("<|end_of_box|>")[0].strip()

        # Processing leading zeros if any
        ptn = r"\[\[\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\]\]"
        m = re.search(ptn, res)
        if m:
            old_str = m.group(0)
            v1 = int(m.group(1))
            v2 = int(m.group(2))
            v3 = int(m.group(3))
            v4 = int(m.group(4))
            new_str = f"[[{v1},{v2},{v3},{v4}]]"
            res = res.replace(old_str, new_str)
        try:
            return json.loads(res)
        except:
            return eval(res, {"true": True, "false": False, "null": None})
    except:
        return None