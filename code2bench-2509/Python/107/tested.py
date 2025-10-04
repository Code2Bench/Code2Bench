from typing import List

def validate_and_extract_os_classifiers(classifiers: List[str]) -> List[str]:
    valid_prefixes = {"Operating System :: ", "Operating System :: Microsoft Windows", "Operating System :: POSIX Linux", "Operating System :: OS Independent"}
    result = []
    for classifier in classifiers:
        if classifier.startswith(valid_prefixes):
            result.append(classifier.split("::")[1])
    return result