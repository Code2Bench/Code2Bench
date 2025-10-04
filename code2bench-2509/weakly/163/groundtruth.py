
import unicodedata
import re

import re
import unicodedata

def normalize(x):
    if not isinstance(x, str):
        x = x.decode('utf8', errors='ignore')
    # Remove diacritics
    x = ''.join(
        c for c in unicodedata.normalize('NFKD', x) if unicodedata.category(c) != 'Mn'
    )
    # Normalize quotes and dashes
    x = re.sub(r'[‘’´`]', "'", x)
    x = re.sub(r'[“”]', '"', x)
    x = re.sub(r'[‐‑‒–—−]', '-', x)
    while True:
        old_x = x
        # Remove citations
        x = re.sub(r'((?<!^)\[[^\]]*\]|\[\d+\]|[•♦†‡*#+])*$', '', x.strip())
        # Remove details in parenthesis
        x = re.sub(r'(?<!^)( \([^)]*\))*$', '', x.strip())
        # Remove outermost quotation mark
        x = re.sub(r'^"([^"]*)"$', r'\1', x.strip())
        if x == old_x:
            break
    # Remove final '.'
    if x and x[-1] == '.':
        x = x[:-1]
    # Collapse whitespaces and convert to lower case
    x = re.sub(r'\s+', ' ', x, flags=re.U).lower().strip()
    return x