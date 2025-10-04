from collections import Counter

def majority_vote_move(moves_list: list, prev_move=None) -> str:
    if not moves_list:
        return None
    counter = Counter(moves_list)
    max_count = max(counter.values())
    candidates = [move for move, count in counter.items() if count == max_count]
    if prev_move in candidates:
        return prev_move
    else:
        return candidates[0]