

def compare_numerical_ans(ans_p, ans_l):
    if ans_p is None:
        return False
    ans_p = ans_p.replace(",", "").replace("$", "")
    ans_l = ans_l.replace(",", "").replace("$", "")
    try:
        if ans_p.endswith("%"):
            ans_p = float(ans_p.rstrip("%")) / 100
        if isinstance(ans_p, str):
            ans_p = float(ans_p)
        if isinstance(ans_l, str):
            ans_l = float(ans_l)
    except Exception as e:
        return False
    return abs(ans_p - float(ans_l)) < 1e-3