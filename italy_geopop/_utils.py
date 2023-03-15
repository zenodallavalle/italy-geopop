from functools import wraps
from itertools import pairwise
import pandas as pd
import numpy as np
from typing import Any, Callable, Iterable
from warnings import warn
import re


def handle_return_cols(
    return_df, return_cols: list | str | re.Pattern | None, regex=False
) -> pd.DataFrame:
    if return_cols is None:
        return return_df
    elif isinstance(return_cols, re.Pattern) or (
        isinstance(return_cols, str) and regex
    ):
        if not isinstance(return_cols, re.Pattern):
            return_cols = re.compile(return_cols)

        def filter_fn(col):
            """Returns True if col has to be kept, False otherwise."""
            return return_cols.fullmatch(col) is not None

        return_cols = list(filter(filter_fn, return_df.columns))

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


def cache(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args, **kwargs) -> Any:
        key = str(args) + str(tuple(kwargs.items()))
        if key in wrapper.cache:
            return wrapper.cache[key]
        else:
            value = fn(*args, **kwargs)
            wrapper.cache[key] = value
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


def aggregate_province_pop(pop_df: pd.DataFrame, geo_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(
        geo_df[['province_code']], pop_df, how='left', left_index=True, right_index=True
    )
    return df.groupby('province_code').sum()


def aggregate_region_pop(pop_df: pd.DataFrame, geo_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(
        geo_df[['region_code']], pop_df, how='left', left_index=True, right_index=True
    )
    return df.groupby('region_code').sum()


def prepare_limits(population_limits):
    """Prepare population limits for age groups. Adds 0 and np.inf to the limits and sorts them after converting them to int."""
    slices = [0]
    for limit in sorted(set(map(int, population_limits))):
        if limit > 100:
            warn(f'age above 100 are not supported, {limit} will be ignored')
        elif limit <= 0:
            warn(f'age ≤ 0 are not supported, {limit} will be ignored')
        else:
            slices.append(limit)
    slices.append(np.inf)
    return slices


def generate_labels_for_age_cutoffs(age_cutoffs):
    groups = list(pairwise(age_cutoffs))
    return [
        '<{}'.format(upper)
        if i == 0
        else '>={}'.format(lower)
        if (i + 1) == len(groups)
        else '{}-{}'.format(lower, upper)
        for i, [lower, upper] in enumerate(groups)
    ]
