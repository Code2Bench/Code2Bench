from typing import Dict, Any

def _set_all_properties_required(schema: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(schema, dict):
        return schema
    
    if "properties" in schema:
        schema["required"] = list(schema["properties"].keys())
    
    for value in schema.values():
        if isinstance(value, dict):
            _set_all_properties_required(value)
    
    return schema