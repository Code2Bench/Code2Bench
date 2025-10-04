

def preprocess_operands(operand):
    """
    Interprets a string operand as an appropriate type.

    Args:
        operand (str): the string operand to interpret.

    Returns:
        The interpreted operand as an appropriate type.
    """
    if isinstance(operand, str):
        if operand.isdigit():
            operand = int(operand)
        elif operand.replace(".", "").isnumeric():
            operand = float(operand)
    return operand