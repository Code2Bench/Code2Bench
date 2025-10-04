
from itertools import starmap

def s2_authors_match(authors: list[str], data: dict) -> bool:
    """Check if the authors in the data match the authors in the paper."""
    AUTHOR_NAME_MIN_LENGTH = 2
    s2_authors_noinit = [
        " ".join([w for w in a["name"].split() if len(w) > AUTHOR_NAME_MIN_LENGTH])
        for a in data["authors"]
    ]
    authors_noinit = [
        " ".join([w for w in a.split() if len(w) > AUTHOR_NAME_MIN_LENGTH])
        for a in authors
    ]
    # Note: we expect the number of authors to be possibly different
    return any(
        starmap(
            lambda x, y: x in y or y in x,
            zip(s2_authors_noinit, authors_noinit, strict=False),
        )
    )