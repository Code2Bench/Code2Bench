from typing import List, Union

def syndrome_booleans(syndrome: List[Union[int, bool]], measurements: List[Union[int, bool]]) -> Union[int, bool]:
    if not syndrome or not measurements:
        return False
    
    # Process the first element of syndrome and measurements
    result = measurements[0]
    if syndrome[0] == 0 or syndrome[0] == False:
        result = not result
    
    # Apply logical AND operation for the remaining elements
    for i in range(1, len(syndrome)):
        if syndrome[i] == 0 or syndrome[i] == False:
            measurement = not measurements[i]
        else:
            measurement = measurements[i]
        result = result and measurement
    
    return result