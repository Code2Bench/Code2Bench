import unicodedata
from typing import Union

def decompose(path: Union[str, bytes]) -> Union[str, bytes]:
    if isinstance(path, str):
        return unicodedata.normalize('NFD', path)
    elif isinstance(path, bytes):
        try:
            decoded = path.decode('utf-8')
            normalized = unicodedata.normalize('NFD', decoded)
            return normalized.encode('utf-8')
        except UnicodeDecodeError:
            return path
    return path