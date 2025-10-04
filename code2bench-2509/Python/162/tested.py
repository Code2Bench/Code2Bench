from typing import Dict, Any

def parse_prompt_line(line: str) -> Dict[str, Any]:
    # Split the line into parts
    parts = line.split()
    
    # Extract the main prompt
    prompt = parts[0]
    
    # Initialize a dictionary to store the arguments
    args = {
        'prompt': prompt
    }
    
    # Process the remaining parts for arguments
    for part in parts[1:]:
        if part.startswith('--'):
            # Extract the argument name and value
            arg_name = part[2:]
            arg_value = None
            
            # Check if there's a value after the argument
            if ' ' in part:
                arg_value = part.split(' ', 1)[1]
            
            # Add the argument to the dictionary
            args[arg_name] = arg_value
    
    return args