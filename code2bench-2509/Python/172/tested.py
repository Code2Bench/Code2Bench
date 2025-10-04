from typing import List, Tuple

def _parse_n_check_triples(triples_str: str) -> List[Tuple[str, str, str]]:
    # Remove surrounding parentheses and single quotes
    triples_str = triples_str.strip()
    triples_str = triples_str.replace('(', '').replace(')', '').replace("'", '')
    
    # Split by newline or space to get individual triples
    triples = triples_str.split('\n') if '\n' in triples_str else triples_str.split()
    
    valid_triples = []
    
    for triple in triples:
        # Check if the triple is empty
        if not triple:
            continue
        
        # Split the triple into components
        try:
            components = triple.split(',')
            if len(components) != 3:
                continue
            
            # Trim whitespace from each component
            entity, relation, entity = [comp.strip() for comp in components]
            
            # Convert to lowercase if they end with a space
            if entity.endswith(' '):
                entity = entity[:-1].lower()
            if relation.endswith(' '):
                relation = relation[:-1].lower()
            
            # Check if the first component contains 'note:'
            if 'note:' in entity:
                continue
                
            # Validate that all components are non-empty strings
            if not all(component for component in [entity, relation, entity]):
                continue
                
            valid_triples.append((entity, relation, entity))
        except Exception:
            continue
    
    return valid_triples