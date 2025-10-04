import csv

def load_benchmark_data(benchmark_file: str) -> dict:
    data = {}
    with open(benchmark_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            question = row['question'].strip()
            answer = row['answer'].strip()
            data[question] = answer
    return data