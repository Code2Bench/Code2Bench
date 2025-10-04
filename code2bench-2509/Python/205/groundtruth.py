

def _strip_existing_semantic_index(content: str) -> str:
    lines = content.split('\n')
    result_lines = []
    in_semantic_index = False

    for line in lines:
        if line.strip().startswith('## SEMANTIC INDEX'):
            in_semantic_index = True
            continue
        elif in_semantic_index and line.strip().startswith('##') and not line.strip().startswith('## SEMANTIC INDEX'):
            in_semantic_index = False
            result_lines.append(line)
        elif not in_semantic_index:
            result_lines.append(line)

    return '\n'.join(result_lines)