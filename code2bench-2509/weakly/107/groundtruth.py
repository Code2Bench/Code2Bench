
import csv
import json

def load_dataset(dataset_file, eval_type):
    questions = [] #list of questions: {question: str, answers: dict, solution: str}
    if eval_type == "seceval":
        with open(dataset_file, 'r') as f:
            data = json.load(f)
            for question in data:
                questions.append({
                    "Question": question["question"],
                    "Choices": "\n".join(question["choices"]),
                    "Solution": question["answer"]
                })

    elif eval_type == "cybermetric":
        with open(dataset_file, 'r') as f:
            data = json.load(f)
            for question in data.get("questions", []):
                questions.append({
                    "Question": question.get("question", ""),
                    "Choices": "\n".join([f"{k}: {v}" for k, v in question.get("answers", {}).items()]),
                    "Solution": question.get("solution", "")
                })
    elif eval_type == "cti_bench":
        with open(dataset_file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            header = next(reader, None)
            for row in reader:
                # Handle three possible formats:
                # Format 1: [URL, Question, Option A, Option B, Option C, Option D, Prompt, GT] (8 columns)
                # Format 2: [URL, Platform, Description, Prompt, GT] (5 columns)
                # Format 3: [URL, Description, Prompt, GT] (4 columns)

                if len(row) == 8:
                    # MCQ format
                    questions.append({
                        "Question": row[1],
                        "Choices": f"A: {row[2]}\nB: {row[3]}\nC: {row[4]}\nD: {row[5]}",
                        "Solution": row[7]
                    })
                elif len(row) == 5:
                    # ATE format (no choices, just open-ended)
                    questions.append({
                        "Question": row[2] + row[3],  # Description + Prompt
                        "Choices": "",       # No choices for ATE
                        "Solution": row[4]   # GT
                    })
                elif len(row) == 4:
                    # RCM format: [URL, Description, Prompt, GT]
                    questions.append({
                        "Question": row[1] + row[2],  # Description + Prompt
                        "Choices": "",       # No choices for RCM
                        "Solution": row[3]   # GT
                    })

    return questions