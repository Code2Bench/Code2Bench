from typing import Union

def count_todos(obj: Union[dict, list, str]) -> int:
    count = 0
    if isinstance(obj, (dict, list)):
        if isinstance(obj, dict):
            for key, value in obj.items():
                count += count_todos(value)
        else:
            for item in obj:
                count += count_todos(item)
    elif isinstance(obj, str):
        if obj.strip() == 'TODO: translate':
            count += 1
    return count