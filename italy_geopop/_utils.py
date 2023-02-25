import pandas as pd


def handle_return_cols(return_df, return_cols) -> pd.DataFrame:
    if return_cols is None:
        return return_df
    else:
        return_df = return_df[return_cols]
        return return_df.copy()
