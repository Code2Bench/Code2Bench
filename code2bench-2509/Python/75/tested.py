from typing import Dict, Any

def trim_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    # Remove 'title' key if present
    if 'title' in schema:
        del schema['title']
    
    # Remove 'default' key if its value is None
    if 'default' in schema and schema['default'] is None:
        del schema['default']
    
    # Convert 'anyOf' to 'type' and combine types
    if 'anyOf' in schema:
        types = []
        for item in schema['anyOf']:
            if 'type' in item:
                types.extend(item['type'])
        # Remove 'null' type
        types = [t for t in types if t != 'null']
        schema['type'] = types
    
    # Recursively process nested 'properties'
    if 'properties' in schema:
        for prop, details in schema['properties'].items():
            if 'type' in details:
                schema[prop] = trim_schema(details)
    
    return schema