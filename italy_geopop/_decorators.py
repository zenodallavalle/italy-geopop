from functools import wraps
import geopandas as gpd
import pandas as pd
from typing import Callable


def cache(fn) -> Callable:
    @wraps(fn)
    def wrapper(*args, **kwargs):
        key = str(list(args) + list(kwargs.items()))
        if key in wrapper.cache:
            return wrapper.cache.get(key)
        else:
            value = fn(*args, **kwargs)
            wrapper.cache[key] = value
            return value

    wrapper.cache = dict()
    return wrapper


def handle_return_cols(include_geometry=False) -> Callable:
    def _handle_return_cols(fn) -> Callable:
        def wrapper(*args, return_cols=None) -> pd.DataFrame | gpd.GeoDataFrame:
            return_df = fn(*args)
            if return_cols is None:
                if include_geometry:
                    return gpd.GeoDataFrame(return_df)
                else:
                    return return_df
            else:
                return_df = return_df[return_cols]
                if 'geometry' in return_cols:
                    return gpd.GeoDataFrame(return_df)
                else:
                    return return_df.copy()

        return wrapper

    return _handle_return_cols
