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
def region_names() -> pd.Series:
    """
    Returns a pd.Series with some valid regions names.
    """
    return pd.Series(
        [
            'Veneto',
            'Umbria',
            'Piemonte',
            'Sicilia',
            'Friuli-Venezia Giulia',
            'Emilia-Romagna',
            'Campania',
            'Puglia',
            'Lazio',
            'Abruzzo',
        ]
    )


@pytest.fixture
def region_name_complex() -> pd.Series:
    """
    Returns a pd.Series with a valid complex region name.
    """
    return pd.Series(['Regione del Veneto'])


@pytest.fixture
def region_name_complex_to_simple() -> pd.Series:
    """
    Returns a pd.Series with a the right simple name for region_name_complex above.
    """
    return pd.Series(['veneto'])


@pytest.fixture
def not_unequivocal_region_name_complex() -> pd.Series:
    """
    Returns a pd.Series with a non-unequivocal complex region name.
    """
    return pd.Series(['Piemonte o Lombardia'])


@pytest.fixture
def region_codes() -> pd.Series:
    """
    Returns a pd.Series with some valid regions codes.
    """
    return pd.Series([18, 15, 6, 1, 3, 13, 10, 14, 5, 19])


def test_pandas_extension_from_region_return_df_with_same_index_as_input_with_geometry(
    dummy_series,
):
    with pandas_activate_context(include_geometry=True):
        output = dummy_series.italy_geopop.from_region()
    diffs = output.index.to_series() != dummy_series.index.to_series()
    assert diffs.sum() == 0


def test_pandas_extension_from_region_returns_all_columns_if_not_differently_specified_with_geometry(
    dummy_series,
):
    with pandas_activate_context(include_geometry=True):
        output = dummy_series.italy_geopop.from_region()
    for c in _region_columns + _population_columns:
        pytest.assume(c in output.columns)
    for c in _municipality_columns + _province_columns:
        pytest.assume(c not in output.columns)


def test_pandas_extension_find_correct_region_information_from_names_with_geometry(
    geopop_df, region_names
):
    with pandas_activate_context(include_geometry=True):
        expected = (
            geopop_df.aggregate_region()
            .set_index('region')
            .loc[region_names.to_list()]
            .reset_index()
        )
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_regions_geometry(),
            how='left',
            left_on='region_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        output = region_names.italy_geopop.from_region()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_region_information_from_codes_with_geometry(
    geopop_df, region_codes
):
    with pandas_activate_context(include_geometry=True):
        expected = (
            geopop_df.aggregate_region()
            .set_index('region_code')
            .loc[region_codes.to_list()]
            .reset_index()
        )
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_regions_geometry(),
            how='left',
            left_on='region_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        output = region_codes.italy_geopop.from_region()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_region_information_from_mixed_names_and_codes_with_geometry(
    geopop_df, region_names, region_codes
):
    with pandas_activate_context(include_geometry=True):
        expected_names = (
            geopop_df.aggregate_region()
            .set_index('region')
            .loc[region_names.to_list()]
            .reset_index()
        )

        expected_codes = (
            geopop_df.aggregate_region()
            .set_index('region_code')
            .loc[region_codes.to_list()]
            .reset_index()
        )

        expected = pd.concat([expected_names, expected_codes], ignore_index=True)
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_regions_geometry(),
            how='left',
            left_on='region_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        input = pd.concat([region_names, region_codes], ignore_index=True)

        output = input.italy_geopop.from_region()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_region_information_from_complex_region_name_with_geometry(
    region_name_complex, region_name_complex_to_simple
):
    with pandas_activate_context(include_geometry=True):
        expected = region_name_complex_to_simple.italy_geopop.from_region()
        output = region_name_complex.italy_geopop.smart_from_region()
    assert (output != expected).sum().sum() == 0


def test_pandas_extension_return_nan_for_non_unequivocal_region_name_with_geometry(
    not_unequivocal_region_name_complex,
):
    with pandas_activate_context(include_geometry=True):
        output = not_unequivocal_region_name_complex.italy_geopop.smart_from_region()
    assert output.isna().all().all()


## without geometry


def test_pandas_extension_from_region_return_df_with_same_index_as_input_without_geometry(
    dummy_series,
):
    with pandas_activate_context(include_geometry=False):
        output = dummy_series.italy_geopop.from_region()
    diffs = output.index.to_series() != dummy_series.index.to_series()
    assert diffs.sum() == 0


def test_pandas_extension_from_region_returns_all_columns_if_not_differently_specified_without_geometry(
    dummy_series,
):
    with pandas_activate_context(include_geometry=False):
        output = dummy_series.italy_geopop.from_region()
    for c in _region_columns + _population_columns:
        pytest.assume(c in output.columns)
    for c in _municipality_columns + _province_columns:
        pytest.assume(c not in output.columns)


def test_pandas_extension_find_correct_region_information_from_names_without_geometry(
    geopop_df, region_names
):
    with pandas_activate_context(include_geometry=False):
        expected = (
            geopop_df.aggregate_region()
            .set_index('region')
            .loc[region_names.to_list()]
            .reset_index()
        )
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_regions_geometry(),
            how='left',
            left_on='region_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        output = region_names.italy_geopop.from_region()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_region_information_from_codes_without_geometry(
    geopop_df, region_codes
):
    with pandas_activate_context(include_geometry=False):
        expected = (
            geopop_df.aggregate_region()
            .set_index('region_code')
            .loc[region_codes.to_list()]
            .reset_index()
        )
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_regions_geometry(),
            how='left',
            left_on='region_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        output = region_codes.italy_geopop.from_region()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_region_information_from_mixed_names_and_codes_without_geometry(
    geopop_df, region_names, region_codes
):
    with pandas_activate_context(include_geometry=False):
        expected_names = (
            geopop_df.aggregate_region()
            .set_index('region')
            .loc[region_names.to_list()]
            .reset_index()
        )

        expected_codes = (
            geopop_df.aggregate_region()
            .set_index('region_code')
            .loc[region_codes.to_list()]
            .reset_index()
        )

        expected = pd.concat([expected_names, expected_codes], ignore_index=True)
        expected = pd.merge(
            expected,
            ItalyGeopopDataFrame.get_regions_geometry(),
            how='left',
            left_on='region_code',
            right_index=True,
        )
        expected = gpd.GeoDataFrame(expected)

        input = pd.concat([region_names, region_codes], ignore_index=True)

        output = input.italy_geopop.from_region()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_region_information_from_complex_region_name_without_geometry(
    region_name_complex, region_name_complex_to_simple
):
    with pandas_activate_context(include_geometry=False):
        expected = region_name_complex_to_simple.italy_geopop.from_region()
        output = region_name_complex.italy_geopop.smart_from_region()
    assert (output != expected).sum().sum() == 0


def test_pandas_extension_return_nan_for_non_unequivocal_region_name_without_geometry(
    not_unequivocal_region_name_complex,
):
    with pandas_activate_context(include_geometry=False):
        output = not_unequivocal_region_name_complex.italy_geopop.smart_from_region()
    assert output.isna().all().all()
