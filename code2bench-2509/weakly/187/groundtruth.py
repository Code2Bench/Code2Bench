from typing import List
import pandas as pd

def double_columns(df, shifts: List[int]):
    """
    Use previous rows as features appended to this row. This allows us to move history to the current time.
    One limitation is that this function will duplicate *all* features and only using the explicitly specified list of offsets.
    """
    if not shifts:
        return df
    df_list = [df.shift(shift) for shift in shifts]
    df_list.insert(0, df)
    max_shift = max(shifts)

    # Shift and add same columns
    df_out = pd.concat(df_list, axis=1)  # keys=('A', 'B')

    return df_out