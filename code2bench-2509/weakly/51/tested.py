from itertools import starmap

def s2_authors_match(authors: list[str], data: dict) -> bool:
    if "authors" not in data:
        return False
    data_authors = data["authors"]
    min_length = AUTHOR_NAME_MIN_LENGTH
    processed_authors = [name for name in authors if len(name) >= min_length]
    processed_data_authors = [name for name in data_authors if len(name) >= min_length]
    return any(starmap(lambda x, y: x in y or y in x, zip(processed_authors, processed_data_authors))) or any(starmap(lambda x, y: x in y or y in x, zip(processed_data_authors, processed_authors)))