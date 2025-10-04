from typing import List, Tuple, Dict, Any

def conditioning_set_values(conditioning: List[Tuple[str, Dict[str, Any]]], values: Dict[str, Any] = {}, append: bool = False) -> List[Tuple[str, Dict[str, Any]]]:
    new_conditioning = []
    for key, dict_entry in conditioning:
        if append:
            dict_entry.update(values)
        else:
            dict_entry.clear()
            dict_entry.update(values)
        new_conditioning.append((key, dict_entry))
    return new_conditioning