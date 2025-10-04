def _strip_existing_semantic_index(content: str) -> str:
    lines = content.splitlines()
    result = []
    in_semantic_index = False
    
    for line in lines:
        if line.startswith('## SEMANTIC INDEX'):
            in_semantic_index = True
        elif in_semantic_index and line.startswith('##'):
            in_semantic_index = False
        elif in_semantic_index:
            continue
        else:
            result.append(line)
    
    return '\n'.join(result)