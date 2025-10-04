from typing import List

def get_parenthetical_substrings(text: str) -> List[str]:
    stack = []
    result = []
    i = 0
    while i < len(text):
        if text[i] == '(':
            stack.append(i)
            i += 1
        elif text[i] == ')':
            if stack:
                start = stack.pop()
                substring = text[start:i+1]
                result.append(substring)
                i += 1
            else:
                i += 1
        else:
            i += 1
    return result