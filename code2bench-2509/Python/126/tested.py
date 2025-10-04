from typing import List, Union

def combine_nums(a: Union[int, str], b: Union[int, str]) -> List[List[Union[int, str]]]:
    # Convert inputs to integers
    a_int = int(a)
    b_int = int(b)
    
    # Define operations
    operations = [
        ("addition", a_int + b_int),
        ("multiplication", a_int * b_int),
        ("subtraction", a_int - b_int)
    ]
    
    # Check for division and include it if conditions are met
    if b_int != 0 and a_int % b_int == 0:
        division_result = a_int // b_int
        division_equation = f"{a_int} ÷ {b_int} = {division_result}"
        operations.append(("division", division_result))
    
    # Return the results with their equations
    return [operation for operation in operations]