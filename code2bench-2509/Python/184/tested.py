from typing import Dict, List

def build_immediate_ancestor_map(ancestor_dict: Dict[str, List[int]], adj_list: List[int]) -> Dict[str, int]:
    result = {}
    for node in ancestor_dict:
        ancestors = ancestor_dict[node]
        if not ancestors:
            continue
        # Check if the node is present in the adjacency list
        if node in adj_list:
            # The immediate ancestor is the first element in the list
            result[node] = ancestors[0]
    return result