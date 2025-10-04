from typing import Dict

def calculate_best_pass_at_1(query_results: Dict[str, Dict[str, str]]) -> float:
    round_correct = {'round1': 0, 'round2': 0, 'round3': 0}
    
    for query in query_results:
        for round_name, result in query_results[query].items():
            if result == "Correct":
                round_correct[round_name] += 1
    
    total_queries = len(query_results)
    pass_rates = {
        'round1': (round_correct['round1'] / total_queries) * 100,
        'round2': (round_correct['round2'] / total_queries) * 100,
        'round3': (round_correct['round3'] / total_queries) * 100
    }
    
    return round(max(pass_rates.values()), 2)