import pandas as pd
from typing import Iterable

def _is_categorical(values: Iterable) -> bool:
    df = pd.DataFrame([values])
    inferred_type = df.convert_dtypes().dtypes[0]
    return inferred_type in ["category", "string", "boolean"]