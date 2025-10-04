from typing import Dict

def calculate_avg_pass_at_3(query_results: Dict[str, Dict[str, str]]) -> float:
    # Count the number of correct answers for each round
    correct_round1 = 0
    correct_round2 = 0
    correct_round3 = 0

    # Iterate through each query in the results
    for query in query_results:
        results = query_results[query]
        # Check each round
        if results['round1'] == 'Correct':
            correct_round1 += 1
        if results['round2'] == 'Correct':
            correct_round2 += 1
        if results['round3'] == 'Correct':
            correct_round3 += 1

    # Calculate the total correct answers
    total_correct = correct_round1 + correct_round2 + correct_round3

    # Calculate the average correctness for each round
    avg_round1 = correct_round1 / len(query_results)
    avg_round2 = correct_round2 / len(query_results)
    avg_round3 = correct_round3 / len(query_results)

    # Calculate the overall average correctness
    overall_avg = (avg_round1 + avg_round2 + avg_round3) / 3

    # Round to two decimal places
    return round(overall_avg, 2)