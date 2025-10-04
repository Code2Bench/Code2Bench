from typing import List, Tuple

def parse_generator(string: str) -> Tuple[List[str], List[str], bool]:
    commands = []
    quoted = []
    quote_status = False
    i = 0
    
    while i < len(string):
        if string[i] == '"':
            quote_status = not quote_status
            if quote_status:
                quoted.append(string[i])
                i += 1
            else:
                # Handle single quoted word with spaces
                if i + 1 < len(string) and string[i+1] == '"':
                    quoted.append(string[i:i+2])
                    i += 2
                else:
                    # Handle single quoted word without spaces
                    quoted.append(string[i])
                    i += 1
        elif string[i] == ' ':
            # Skip space
            i += 1
        else:
            # Extract command
            command = ""
            while i < len(string) and string[i] != '"':
                command += string[i]
                i += 1
            commands.append(command)
            if quote_status:
                quoted.append(command)
            else:
                quoted.append("")
            i += 1
    
    # Check if the string ends with an open quote
    if quote_status:
        return commands, quoted, True
    else:
        return commands, quoted, False