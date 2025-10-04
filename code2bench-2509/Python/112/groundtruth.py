

def calculate_avg_pass_at_3(query_results): 
    round_names = ["round1", "round2", "round3"]
    total_correct = {round_name: 0 for round_name in round_names}

    for query, results in query_results.items():  
        for round_name in round_names:  
            if results[round_name] == "Correct":
                total_correct[round_name] += 1 

    avg_overall = sum(total_correct[r] / len(query_results) for r in round_names) / len(round_names)

    return round(avg_overall * 100, 2)