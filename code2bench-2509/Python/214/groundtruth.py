from typing import Dict, List

from typing import Dict, List

def organize_imports_by_category(files_by_category: Dict[str, List[str]]) -> str:
    if not files_by_category:
        return ""

    sections = []

    # Framework imports section header
    sections.append("# ===================================================")
    sections.append("# SuperClaude Framework Components")
    sections.append("# ===================================================")
    sections.append("")

    # Add each category
    for category, files in files_by_category.items():
        if files:
            sections.append(f"# {category}")
            for file in sorted(files):
                sections.append(f"@{file}")
            sections.append("")

    return "\n".join(sections)