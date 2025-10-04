import re

def count_valid_tags(text: str, tag: str) -> int:
    # Find all occurrences of the tag and its closing counterpart
    tags = re.findall(r'<{}>'.format(tag), text)
    # Count valid pairs by checking if each opening tag has a corresponding closing tag
    count = 0
    i = 0
    while i < len(tags):
        if i + 1 < len(tags) and tags[i] == tags[i + 1].replace('</', ''):
            count += 1
            i += 2
        else:
            i += 1
    return count