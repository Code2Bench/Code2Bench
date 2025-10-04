

def check_valid(s: str):
    cnt = 0
    for ch in s:
        if ch == "(":
            cnt += 1
        elif ch == ")":
            cnt -= 1
        else:
            return False
        if cnt < 0:
            return False
    return cnt == 0