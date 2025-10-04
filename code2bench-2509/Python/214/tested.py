from typing import Dict, List

def organize_imports_by_category(files_by_category: Dict[str, List[str]]) -> str:
    result = "SuperClaude Framework Components\n"
    
    for category, files in files_by_category.items():
        if len(files) > 0:
            result += f"{category}:\n"
            result += "\t" + "\n\t".join(f"@{file}" for file in sorted(files)) + "\n\n"
    
    return result if result else ""