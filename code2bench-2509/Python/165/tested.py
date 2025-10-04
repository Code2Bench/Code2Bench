from typing import Dict, Optional

def build_csp_header(csp_config: Dict[str, str]) -> Optional[str]:
    result = []
    for directive, value in csp_config.items():
        if value:
            # If the value is empty, include the directive without a value
            if not value:
                result.append(directive)
            else:
                # Format the directive with the value
                result.append(f"{directive} {value}")
    return "; ".join(result) if result else None