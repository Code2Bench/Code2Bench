
import pandas as pd

def _is_categorical(values):
    """
    Infer whether input values are categorical on best effort.
    Return True represent they are categorical, return False represent we cannot determine result.
    """
    dtype_name = pd.Series(values).convert_dtypes().dtype.name.lower()
    return dtype_name in ["category", "string", "boolean"]