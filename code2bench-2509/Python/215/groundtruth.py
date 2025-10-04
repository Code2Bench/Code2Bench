from typing import Dict, List

from typing import Dict, List

def _parse_existing_framework_imports(content: str) -> Dict[str, List[str]]:
    imports_by_category = {}
    framework_marker = "# ===================================================\n# SuperClaude Framework Components"
    if framework_marker not in content:
        return imports_by_category
    framework_section = content.split(framework_marker)[1] if framework_marker in content else ""
    lines = framework_section.split('\n')
    current_category = None
    for line in lines:
        line = line.strip()
        if line.startswith('# ===') or not line:
            continue
        if line.startswith('# ') and not line.startswith('# ==='):
            current_category = line[2:].strip()
            if current_category not in imports_by_category:
                imports_by_category[current_category] = []
        elif line.startswith('@') and current_category:
            import_file = line[1:].strip()
            if import_file not in imports_by_category[current_category]:
                imports_by_category[current_category].append(import_file)
    return imports_by_category