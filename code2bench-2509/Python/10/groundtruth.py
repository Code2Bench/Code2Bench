

def extract_boxed_answer(text: str):
    """Extract the last boxed{…} string from a LaTeX-like answer."""
    answers = []
    for piece in text.split("boxed{")[1:]:
        n = 0
        for i, ch in enumerate(piece):
            if ch == "{":
                n += 1
            elif ch == "}":
                n -= 1
                if n < 0:
                    answers.append(piece[: i] if (i + 1 == len(piece) or piece[i + 1] != "%") else piece[: i + 1])
                    break
    return answers[-1] if answers else None