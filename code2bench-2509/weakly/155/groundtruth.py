
import re
import unicodedata

import re
import unicodedata

def normalize_name(tag_name: str) -> str:
    nfkd_form = unicodedata.normalize("NFKD", tag_name)
    nfkd_form.encode("ASCII", "ignore").decode("UTF-8")
    tag_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    tag_name = tag_name.strip().lower()
    tag_name = re.sub(r"\s+", "_", tag_name)
    tag_name = re.sub(r"[^a-zA-Z0-9_.:-]", "", tag_name)
    return tag_name