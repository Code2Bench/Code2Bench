from typing import Any, Dict, List

def format_tool_descriptions(schemas: List[Dict[str, Any]]) -> str:
    """Formats tool schemas into a user-friendly description string."""
    descriptions = []
    for schema in schemas:
        desc = [f"{schema['name']}: {schema['description']}"]

        desc.append("\nArguments:")
        for arg_name, arg_info in schema["args"].items():
            default = (
                f" (default: {arg_info['default']})" if "default" in arg_info else ""
            )
            desc.append(f"  - {arg_name}: {arg_info['description']}{default}")

        if schema["examples"]:
            desc.append("\nExamples:")
            for example in schema["examples"]:
                desc.append(f"  {example}")

        if schema["returns"]:
            desc.append(f"\nReturns: {schema['returns']}")

        descriptions.append("\n".join(desc))

    return "\n\n".join(descriptions)