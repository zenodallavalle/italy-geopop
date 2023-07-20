from functools import wraps
from itertools import pairwise
import os
import pandas as pd
import numpy as np
from typing import Any, Callable, Iterable, Optional, List
from warnings import warn
import re


def get_available_years(data_directory: os.PathLike | str) -> List[int]:
    """Return a list of data available years."""
    years = []
    for file in os.listdir(data_directory):
        if re.match(r"\d{4}_", file):
            try:
                years.append(int(file[:4]))
            except ValueError:
                pass
    return sorted(years)


def get_latest_available_year(data_directory: os.PathLike | str) -> int:
    """Return the latest data available year."""
    return max(get_available_years(data_directory))


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
        if "_cached" in wrapper.cache:
            return wrapper.cache["_cached"]
        else:
            value = fn(*args, **kwargs)
            wrapper.cache["_cached"] = value
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


def _match_every_word(words: Iterable[str], text: str) -> bool:
    """return True if every word in words is found in text, False otherwise. Word is searched as "exact word match" and with "case-insensitive" flag.

    :param words: a list or iterable of words to be searched into text.
    :type words: Iterable[str]
    :param text: the source text into words are searched.
    :type text: str
    :return: True if every word in words is found in text, False otherwise.
    :rtype: bool
    """
    for word in words:
        if not re.search(r"\b{}\b".format(word), text, flags=re.IGNORECASE):
            return False
    return True


def match_single_key(
    keys: Iterable[str],
    text: str,
    _split_key: bool = False,
    _return_values: Optional[Iterable[str]] = None,
) -> str | None:
    """return the key, taken from a list of keys, that is found in text only if it's the only match.
    Key is searched as "exact key match" and with "case-insensitive" flag.

    If no matches are found every key is splitted into:
    - sinonims using '/' as separator and then search for every sinonim in text if '/' is found in key.
    - words using '\W' regex as separator and then search for every word whose length is > 2 in text. If every word is found, the original key is returned.

    :param keys: a list or iterable of keys to be searched into text.
    :type keys: Iterable[str]
    :param text: the source text into keys are searched.
    :type text: str

    :return: the key, taken from a list of keys, that is found in text only if it's the only match.
    :rtype: str | None
    """
    if _return_values is None:
        return_values = keys
    else:
        return_values = _return_values
    return_dict = dict(zip(keys, return_values))
    n_matches = 0
    match = None
    extended_keys = []
    extended_values = []
    if not _split_key:
        for key in keys:
            if re.search(r"\b{}\b".format(key), text, flags=re.IGNORECASE):
                n_matches += 1
                match = key
        if not n_matches:
            for key in keys:
                if "/" not in key:
                    continue
                for sinonim in key.split("/"):
                    sinonim = sinonim.strip()
                    if len(sinonim) < 3:
                        continue
                    extended_keys.append(sinonim)
                    extended_values.append(key)
                    if re.search(r"\b{}\b".format(sinonim), text, flags=re.IGNORECASE):
                        n_matches += 1
                        match = key

    else:
        for key in keys:
            words = [x.strip() for x in re.split("\W", key) if len(x.strip()) >= 2]
            if len(words) < 2:
                continue
            if _match_every_word(words, text):
                n_matches += 1
                match = key

    if n_matches == 1:
        return return_dict[match]
    elif not n_matches and not _split_key:
        return match_single_key(
            ([*keys] + extended_keys),
            text,
            _split_key=True,
            _return_values=([*return_values] + extended_values),
        )


def aggregate_province_pop(pop_df: pd.DataFrame, geo_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(
        geo_df[["province_code"]], pop_df, how="left", left_index=True, right_index=True
    )
    return df.groupby("province_code").sum()


def aggregate_region_pop(pop_df: pd.DataFrame, geo_df: pd.DataFrame) -> pd.DataFrame:
    df = pd.merge(
        geo_df[["region_code"]], pop_df, how="left", left_index=True, right_index=True
    )
    return df.groupby("region_code").sum()


def prepare_limits(population_limits):
    """Prepare population limits for age groups. Adds 0 and np.inf to the limits and sorts them after converting them to int."""
    slices = [0]
    for limit in sorted(set(map(int, population_limits))):
        if limit > 100:
            warn(f"age above 100 are not supported, {limit} will be ignored")
        elif limit <= 0:
            warn(f"age ≤ 0 are not supported, {limit} will be ignored")
        else:
            slices.append(limit)
    slices.append(np.inf)
    return slices


def generate_labels_for_age_cutoffs(age_cutoffs):
    groups = list(pairwise(age_cutoffs))
    return [
        "<{}".format(upper)
        if i == 0
        else ">={}".format(lower)
        if (i + 1) == len(groups)
        else "{}-{}".format(lower, upper)
        for i, [lower, upper] in enumerate(groups)
    ]
