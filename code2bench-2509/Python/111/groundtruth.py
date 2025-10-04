

def calculate_best_pass_at_1(query_results):  
    round_correct = {round_name: 0 for round_name in ["round1", "round2", "round3"]}

    for query, results in query_results.items():
        for round_name in ["round1", "round2", "round3"]: 
            if results[round_name] == "Correct":  
                round_correct[round_name] += 1 

    overall_best = max(
        round_correct[round_name] / len(query_results)
        for round_name in ["round1", "round2", "round3"]
    )

    return round(overall_best * 100, 2)