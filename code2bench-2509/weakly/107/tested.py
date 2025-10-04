import csv
import json

def load_dataset(dataset_file: str, eval_type: str) -> list:
    if eval_type == "seceval":
        with open(dataset_file, 'r') as f:
            data = json.load(f)
        questions = []
        for item in data:
            question = item.get("question", "")
            choices = item.get("choices", "")
            solution = item.get("answer", "")
            questions.append({"Question": question, "Choices": choices, "Solution": solution})
        return questions
    elif eval_type == "cybermetric":
        with open(dataset_file, 'r') as f:
            data = json.load(f)
        questions = []
        for question in data.get("questions", []):
            question_text = question.get("question", "")
            answers = question.get("answers", [])
            solution = question.get("solution", "")
            choices = "\n".join(answers) if answers else ""
            questions.append({"Question": question_text, "Choices": choices, "Solution": solution})
        return questions
    elif eval_type == "cti_bench":
        questions = []
        with open(dataset_file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                if len(row) == 8:
                    question = row[0]
                    choices = "\n".join(row[1:5])
                    solution = row[5]
                elif len(row) == 5:
                    question = row[0]
                    choices = "\n".join(row[1:4])
                    solution = row[4]
                elif len(row) == 4:
                    question = row[0]
                    choices = row[1]
                    solution = row[2]
                else:
                    continue
                questions.append({"Question": question, "Choices": choices, "Solution": solution})
        return questions
    else:
        raise ValueError(f"Unsupported evaluation type: {eval_type}")