

def find_matching_parenthesis(expression, opening_index):
    if expression[opening_index] != "(":
        raise ValueError("The character at the provided index is not '('.")

    stack = 0

    for index in range(opening_index + 1, len(expression)):
        char = expression[index]
        if char == "(":
            stack += 1
        elif char == ")":
            if stack == 0:
                return index
            stack -= 1

    raise ValueError("No matching ')' found for '(' at index {}.".format(opening_index))