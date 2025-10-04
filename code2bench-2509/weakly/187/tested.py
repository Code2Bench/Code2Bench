from typing import List
import pandas as pd

def double_columns(df: pd.DataFrame, shifts: List[int]) -> pd.DataFrame:
    if not shifts:
        return df
    shifted_dfs = []
    for shift in shifts:
        shifted_df = df.shift(shift)
        shifted_dfs.append(shifted_df)
    shifted_df = pd.concat(shifted_dfs, axis=1)
    result_df = pd.concat([df, shifted_df], axis=1)
    return result_df