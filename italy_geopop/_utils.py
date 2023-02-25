from functools import wraps
import pandas as pd
from typing import Any, Callable


def handle_return_cols(return_df, return_cols) -> pd.DataFrame:
    if return_cols is None:
        return return_df
    else:
        return_df = return_df[return_cols]
        return return_df.copy()


def simple_cache(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args, **kwargs) -> Any:
        if '_cached' in wrapper.cache:
            return wrapper.cache['_cached']
        else:
            value = fn(*args, **kwargs)
            wrapper.cache['_cached'] = value
            return value

    wrapper.cache = dict()
    return wrapper
