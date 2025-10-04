from typing import Optional

def extract_examples_section(docstring: Optional[str]) -> Optional[str]:
    if not docstring:
        return None
    
    examples = []
    in_examples = False
    
    for line in docstring.split('\n'):
        if line.strip() == 'Examples:':
            in_examples = True
        elif in_examples and line.strip() != '':
            examples.append(line)
        elif in_examples and line.strip() == '':
            in_examples = False
    
    return '\n'.join(examples) if in_examples else None