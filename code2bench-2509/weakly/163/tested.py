import re
import unicodedata

def normalize(x: str | bytes) -> str:
    if isinstance(x, bytes):
        x = x.decode("utf-8")
    x = unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8")
    x = re.sub(r"[‘’“”«»]", '"', x)
    x = re.sub(r"([–—])", "-", x)
    while True:
        new_x = re.sub(r"^(\"|\'|\`)(.*?)(\"|\'|\`)$", r"\1\2\3", x)
        new_x = re.sub(r"\([^)]*\)", "", new_x)
        new_x = re.sub(r"\b([A-Za-z]+)\.(\s+|$)", r"\1\2", new_x)
        if new_x == x:
            break
        x = new_x
    x = re.sub(r"\.\s*$", "", x)
    x = re.sub(r"\s+", " ", x).strip()
    return x.lower()