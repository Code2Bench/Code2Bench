

def separate_lora_AB(parameters, B_patterns=None):
    parameters_normal = {}
    parameters_B = {}

    if B_patterns is None:
        B_patterns = ['.lora_B.', '__zero__']

    for k, v in parameters.items():
        if any(B_pattern in k for B_pattern in B_patterns):
            parameters_B[k] = v
        else:
            parameters_normal[k] = v

    return parameters_normal, parameters_B