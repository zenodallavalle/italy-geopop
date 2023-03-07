from functools import wraps
import pandas as pd
from typing import Any, Callable, Iterable
import re


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


def match_single_word(words: Iterable[str], text: str) -> str | None:
    """return the word, taken from a list of words, that is found in text only if it's the only match. Word is searched as "exact word match".

    :param words: a list or iterable of words to be searched into text.
    :type words: Iterable[str]
    :param text: the source text into words are searched.
    :type text: str
    :return: the word, taken from a list of words, that is found in text only if it's the only match.
    :rtype: str | None
    """
    n_matches = 0
    match = None
    for word in words:
        if re.search(r'\b{}\b'.format(word), text):
            n_matches += 1
            match = word
    if n_matches == 1:
        return match
