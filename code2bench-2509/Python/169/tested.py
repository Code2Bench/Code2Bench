from typing import Union

def preprocess_operands(operand: str) -> Union[int, float, str]:
    try:
        return int(operand)
    except ValueError:
        try:
            return float(operand)
        except ValueError:
            return operand