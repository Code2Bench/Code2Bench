from typing import List, Dict, Any

def format_tool_descriptions(schemas: List[Dict[str, Any]]) -> str:
    result = []
    for schema in schemas:
        # Extract tool name and description
        name = schema['name']
        description = schema['description']
        
        # Extract arguments
        args = schema['args']
        argument_list = []
        for arg_name, arg in args.items():
            argument_list.append(f"{arg_name}: {arg['description']} ({arg.get('default', 'no default')})")
        
        # Extract examples
        examples = schema.get('examples', [])
        
        # Extract return description
        returns = schema.get('returns', '')
        
        # Build the tool description string
        tool_description = f"{name}\n{description}\n{'\n'.join(argument_list)}\n{'\n'.join(examples)}\n{returns}"
        
        result.append(tool_description)
    
    return '\n\n'.join(result)