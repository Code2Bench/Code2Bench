from typing import List, Union

def get_predicates(conds: Union[str, List]) -> List[str]:
    if not isinstance(conds, list):
        return []
    
    predicates = []
    for item in conds:
        if isinstance(item, list):
            predicates.extend(get_predicates(item))
        elif isinstance(item, str):
            predicates.append(item)
    
    return predicates