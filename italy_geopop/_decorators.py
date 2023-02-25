from functools import wraps
import pandas as pd
from typing import Any, Callable


def dumb_cache(fn: Callable) -> Callable:
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


def args_kwargs_cache(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args, **kwargs) -> Any:
        key = str(list(args) + list(kwargs.items()))
        if key in wrapper.cache:
            return wrapper.cache.get(key)
        else:
            value = fn(*args, **kwargs)
            wrapper.cache[key] = value
            return value

    wrapper.cache = dict()
    return wrapper
