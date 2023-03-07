import geopandas as gpd
import pandas as pd
import pytest

from italy_geopop.geopop import ItalyGeopopDataFrame
from italy_geopop.pandas_extension import pandas_activate_context


_municipality_columns = [
    'municipality',
    'municipality_code',
]

_province_columns = [
    'province_code',
    'province',
    'province_short',
]


_region_columns = [
    'region',
    'region_code',
]

_population_columns = [
    'population',
    'population_M',
    'population_F',
]


@pytest.fixture
def geopop_df() -> ItalyGeopopDataFrame:
    return ItalyGeopopDataFrame()


@pytest.fixture
def dummy_series() -> pd.Series:
    """
    Returns a pd.Series with empty string values '' indexed as range(0, 500, 5).
    """
    index = list(range(0, 500, 5))
    return pd.Series(['' for _ in index], index=index)


@pytest.fixture
def province_names() -> pd.Series:
    """
    Returns a pd.Series with some valid provinces names.
    """
    return pd.Series(
        [
            'Verbano-Cusio-Ossola',
            'Viterbo',
            'La Spezia',
            'Frosinone',
            'Lodi',
            'Teramo',
            'Pordenone',
            'Genova',
            "Reggio nell'Emilia",
            'Caltanissetta',
        ]
    )


@pytest.fixture
def province_name_complex() -> pd.Series:
    """
    Returns a pd.Series with a valid complex province name.
    """
    return pd.Series(['Università degli studi di Verona'])


@pytest.fixture
def province_name_complex_to_simple() -> pd.Series:
    """
    Returns a pd.Series with a the right simple name for province_name_complex above.
    """
    return pd.Series(['verona'])


@pytest.fixture
def not_unequivocal_province_name_complex() -> pd.Series:
    """
    Returns a pd.Series with a non-unequivocal complex province name.
    """
    return pd.Series(['Verona or Milano'])


@pytest.fixture
def province_abbreviations() -> pd.Series:
    """
    Returns a pd.Series with some valid provinces abbreviations.
    """
    return pd.Series(['AG', 'RO', 'SA', 'CH', 'CN', 'SS', 'GO', 'LO', 'AQ', 'TS'])


@pytest.fixture
def province_codes() -> pd.Series:
    """
    Returns a pd.Series with some valid provinces codes.
    """
    return pd.Series([68, 26, 75, 7, 32, 74, 4, 38, 57, 47])


def test_pandas_extension_from_province_return_df_with_same_index_as_input_with_geometry(
    dummy_series,
):
    with pandas_activate_context(include_geometry=True):
        output = dummy_series.italy_geopop.from_province()
    diffs = output.index.to_series() != dummy_series.index.to_series()
    assert diffs.sum() == 0


def test_pandas_extension_from_province_returns_all_columns_if_not_differently_specified_with_geometry(
    dummy_series,
):
    with pandas_activate_context(include_geometry=True):
        output = dummy_series.italy_geopop.from_province()
    for c in _province_columns + _region_columns + _population_columns:
        pytest.assume(c in output.columns)
    for c in _municipality_columns:
        pytest.assume(c not in output.columns)


def test_pandas_extension_find_correct_province_information_from_names_with_geometry(
    geopop_df, province_names
):
    with pandas_activate_context(include_geometry=True):
        expected = (
            geopop_df.aggregate_province()
            .set_index('province')
            .loc[province_names.to_list()]
            .reset_index()
        )
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_provinces_geometry(),
            how='left',
            left_on='province_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        output = province_names.italy_geopop.from_province()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_codes_with_geometry(
    geopop_df, province_codes
):
    with pandas_activate_context(include_geometry=True):
        expected = (
            geopop_df.aggregate_province()
            .set_index('province_code')
            .loc[province_codes.to_list()]
            .reset_index()
        )
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_provinces_geometry(),
            how='left',
            left_on='province_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        output = province_codes.italy_geopop.from_province()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_names_short_with_geometry(
    geopop_df, province_abbreviations
):
    with pandas_activate_context(include_geometry=True):
        expected = (
            geopop_df.aggregate_province()
            .set_index('province_short')
            .loc[province_abbreviations.to_list()]
            .reset_index()
        )
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_provinces_geometry(),
            how='left',
            left_on='province_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        output = province_abbreviations.italy_geopop.from_province()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_mixed_names_and_codes_and_names_short_with_geometry(
    geopop_df, province_names, province_codes, province_abbreviations
):
    with pandas_activate_context(include_geometry=True):
        expected_names = (
            geopop_df.aggregate_province()
            .set_index('province')
            .loc[province_names.to_list()]
            .reset_index()
        )

        expected_codes = (
            geopop_df.aggregate_province()
            .set_index('province_code')
            .loc[province_codes.to_list()]
            .reset_index()
        )

        expected_names_short = (
            geopop_df.aggregate_province()
            .set_index('province_short')
            .loc[province_abbreviations.to_list()]
            .reset_index()
        )

        expected = pd.concat(
            [expected_names, expected_codes, expected_names_short], ignore_index=True
        )
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_provinces_geometry(),
            how='left',
            left_on='province_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        input = pd.concat(
            [province_names, province_codes, province_abbreviations], ignore_index=True
        )

        output = input.italy_geopop.from_province()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_complex_province_name_with_geometry(
    province_name_complex, province_name_complex_to_simple
):
    with pandas_activate_context(include_geometry=True):
        expected = province_name_complex_to_simple.italy_geopop.from_province()
        output = province_name_complex.italy_geopop.smart_from_province()
    assert (output != expected).sum().sum() == 0


def test_pandas_extension_return_nan_for_non_unequivocal_province_name_with_geometry(
    not_unequivocal_province_name_complex,
):
    with pandas_activate_context(include_geometry=True):
        output = (
            not_unequivocal_province_name_complex.italy_geopop.smart_from_province()
        )
    assert output.isna().all().all()


## without geometry


def test_pandas_extension_from_province_return_df_with_same_index_as_input_without_geometry(
    dummy_series,
):
    with pandas_activate_context(include_geometry=False):
        output = dummy_series.italy_geopop.from_province()
    diffs = output.index.to_series() != dummy_series.index.to_series()
    assert diffs.sum() == 0


def test_pandas_extension_from_province_returns_all_columns_if_not_differently_specified_without_geometry(
    dummy_series,
):
    with pandas_activate_context(include_geometry=False):
        output = dummy_series.italy_geopop.from_province()
    for c in _province_columns + _region_columns + _population_columns:
        pytest.assume(c in output.columns)
    for c in _municipality_columns:
        pytest.assume(c not in output.columns)


def test_pandas_extension_find_correct_province_information_from_names_without_geometry(
    geopop_df, province_names
):
    with pandas_activate_context(include_geometry=False):
        expected = (
            geopop_df.aggregate_province()
            .set_index('province')
            .loc[province_names.to_list()]
            .reset_index()
        )
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_provinces_geometry(),
            how='left',
            left_on='province_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        output = province_names.italy_geopop.from_province()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_codes_without_geometry(
    geopop_df, province_codes
):
    with pandas_activate_context(include_geometry=False):
        expected = (
            geopop_df.aggregate_province()
            .set_index('province_code')
            .loc[province_codes.to_list()]
            .reset_index()
        )
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_provinces_geometry(),
            how='left',
            left_on='province_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        output = province_codes.italy_geopop.from_province()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_names_short_without_geometry(
    geopop_df, province_abbreviations
):
    with pandas_activate_context(include_geometry=False):
        expected = (
            geopop_df.aggregate_province()
            .set_index('province_short')
            .loc[province_abbreviations.to_list()]
            .reset_index()
        )
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_provinces_geometry(),
            how='left',
            left_on='province_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        output = province_abbreviations.italy_geopop.from_province()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_mixed_names_and_codes_and_names_short_without_geometry(
    geopop_df, province_names, province_codes, province_abbreviations
):
    with pandas_activate_context(include_geometry=False):
        expected_names = (
            geopop_df.aggregate_province()
            .set_index('province')
            .loc[province_names.to_list()]
            .reset_index()
        )

        expected_codes = (
            geopop_df.aggregate_province()
            .set_index('province_code')
            .loc[province_codes.to_list()]
            .reset_index()
        )

        expected_names_short = (
            geopop_df.aggregate_province()
            .set_index('province_short')
            .loc[province_abbreviations.to_list()]
            .reset_index()
        )

        expected = pd.concat(
            [expected_names, expected_codes, expected_names_short], ignore_index=True
        )
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_provinces_geometry(),
            how='left',
            left_on='province_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        input = pd.concat(
            [province_names, province_codes, province_abbreviations], ignore_index=True
        )

        output = input.italy_geopop.from_province()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_complex_province_name_without_geometry(
    province_name_complex, province_name_complex_to_simple
):
    with pandas_activate_context(include_geometry=False):
        expected = province_name_complex_to_simple.italy_geopop.from_province()
        output = province_name_complex.italy_geopop.smart_from_province()
    assert (output != expected).sum().sum() == 0


def test_pandas_extension_return_nan_for_non_unequivocal_province_name_without_geometry(
    not_unequivocal_province_name_complex,
):
    with pandas_activate_context(include_geometry=False):
        output = (
            not_unequivocal_province_name_complex.italy_geopop.smart_from_province()
        )
    assert output.isna().all().all()
