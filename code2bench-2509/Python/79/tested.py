def find_matching_parenthesis(expression: str, opening_index: int) -> int:
    stack = []
    for i, char in enumerate(expression):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                stack.pop()
    if not stack:
        raise ValueError("No matching closing parenthesis found")
    return stack[0]