from typing import Any

def display_desc_to_display_path(display_desc: dict[str, Any]) -> str:
    uri = ""
    path = display_desc.get("path")
    if path:
        uri += path
    display = display_desc.get("display")
    if display:
        if path:
            uri += "#"
        uri += display.lstrip(":")
    options_str = display_desc.get("options_str")
    if options_str:
        uri += f"?{options_str}"
    return uri