from typing import Dict, List

def _parse_existing_framework_imports(content: str) -> Dict[str, List[str]]:
    categories = {}
    lines = content.splitlines()
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('# ==================================================='):
            continue  # Skip separator line
        
        if line.startswith('# SuperClaude Framework Components'):
            category = line.split('# ')[1].strip()
            categories[category] = []
        
        elif line.startswith('@'):
            import_name = line.split('@')[1].strip()
            categories[category].append(import_name)
    
    return categories