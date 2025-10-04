
import csv

import csv

def load_benchmark_data(benchmark_file):
    """Load question-answer pairs from benchmark CSV"""
    benchmark_data = {}

    with open(benchmark_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            question = row['question'].strip()
            answer = row['answer'].strip()
            benchmark_data[question] = answer

    return benchmark_data