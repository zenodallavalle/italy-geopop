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
def municipality_names() -> pd.Series:
    """
    Returns a pd.Series with some valid municipality names. This function ensures that returned municipalities are unique in Italy municipalities.
    """
    return pd.Series(
        [
            'Ronzo-Chienis',
            'Castelvisconti',
            'Scafati',
            'Gandosso',
            'Vasto',
            'Vigolo',
            'Giffone',
            'Mezzana Rabattone',
            'Tissi',
            'Boara Pisani',
        ]
    )


@pytest.fixture
def municipality_codes() -> pd.Series:
    """
    Returns a pd.Series with some valid municipalities codes.
    """
    return pd.Series(
        [70070, 88007, 60018, 4001, 16131, 17097, 4071, 29026, 26084, 6015]
    )


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
def province_names_short() -> pd.Series:
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


def test_pandas_extension_from_municipality_return_df_with_same_index_as_input(
    dummy_series,
):
    with pandas_activate_context(include_geometry=False):
        output = dummy_series.italy_geopop.from_municipality()
    diffs = output.index.to_series() != dummy_series.index.to_series()
    assert diffs.sum() == 0


def test_pandas_extension_from_municipality_returns_all_columns_if_not_differently_specified(
    dummy_series,
):
    with pandas_activate_context(include_geometry=False):
        output = dummy_series.italy_geopop.from_municipality()
    for c in (
        _municipality_columns
        + _province_columns
        + _region_columns
        + _population_columns
    ):
        pytest.assume(c in output.columns)


def test_pandas_extension_from_municipality_return_df_with_same_index_as_input(
    dummy_series,
):
    with pandas_activate_context(include_geometry=False):
        output = dummy_series.italy_geopop.from_municipality()
    diffs = output.index.to_series() != dummy_series.index.to_series()
    assert diffs.sum() == 0


def test_pandas_extension_from_municipality_returns_all_columns_if_not_differently_specified(
    dummy_series,
):
    with pandas_activate_context(include_geometry=False):
        output = dummy_series.italy_geopop.from_municipality()
    for c in (
        _municipality_columns
        + _province_columns
        + _region_columns
        + _population_columns
    ):
        pytest.assume(c in output.columns)


def test_pandas_extension_from_province_return_df_with_same_index_as_input(
    dummy_series,
):
    with pandas_activate_context(include_geometry=False):
        output = dummy_series.italy_geopop.from_province()
    diffs = output.index.to_series() != dummy_series.index.to_series()
    assert diffs.sum() == 0


def test_pandas_extension_from_province_returns_all_columns_if_not_differently_specified(
    dummy_series,
):
    with pandas_activate_context(include_geometry=False):
        output = dummy_series.italy_geopop.from_province()
    for c in _province_columns + _region_columns + _population_columns:
        pytest.assume(c in output.columns)
    for c in _municipality_columns:
        pytest.assume(c not in output.columns)


def test_pandas_extension_from_region_return_df_with_same_index_as_input(
    dummy_series,
):
    with pandas_activate_context(include_geometry=False):
        output = dummy_series.italy_geopop.from_region()
    diffs = output.index.to_series() != dummy_series.index.to_series()
    assert diffs.sum() == 0


def test_pandas_extension_from_region_returns_all_columns_if_not_differently_specified(
    dummy_series,
):
    with pandas_activate_context(include_geometry=False):
        output = dummy_series.italy_geopop.from_region()
    for c in _region_columns + _population_columns:
        pytest.assume(c in output.columns)
    for c in _municipality_columns + _province_columns:
        pytest.assume(c not in output.columns)


def test_pandas_extension_find_correct_municipality_information_from_names(
    geopop_df, municipality_names
):
    with pandas_activate_context(include_geometry=False):
        expected = (
            geopop_df.set_index('municipality')
            .loc[municipality_names.to_list()]
            .reset_index()
        )

        output = municipality_names.italy_geopop.from_municipality()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_municipality_information_from_codes(
    geopop_df, municipality_codes
):
    with pandas_activate_context(include_geometry=False):
        expected = (
            geopop_df.set_index('municipality_code')
            .loc[municipality_codes.to_list()]
            .reset_index()
        )

        output = municipality_codes.italy_geopop.from_municipality()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_municipality_information_from_mixed_names_and_codes(
    geopop_df, municipality_codes, municipality_names
):
    with pandas_activate_context(include_geometry=False):
        expected_names = (
            geopop_df.set_index('municipality')
            .loc[municipality_names.to_list()]
            .reset_index()
        )

        expected_codes = (
            geopop_df.set_index('municipality_code')
            .loc[municipality_codes.to_list()]
            .reset_index()
        )
        expected = pd.concat([expected_names, expected_codes], ignore_index=True)

        input = pd.concat([municipality_names, municipality_codes], ignore_index=True)

        output = input.italy_geopop.from_municipality()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_names(
    geopop_df, province_names
):
    with pandas_activate_context(include_geometry=False):
        expected = (
            geopop_df.aggregate_province()
            .set_index('province')
            .loc[province_names.to_list()]
            .reset_index()
        )

        output = province_names.italy_geopop.from_province()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_codes(
    geopop_df, province_codes
):
    with pandas_activate_context(include_geometry=False):
        expected = (
            geopop_df.aggregate_province()
            .set_index('province_code')
            .loc[province_codes.to_list()]
            .reset_index()
        )

        output = province_codes.italy_geopop.from_province()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_names_short(
    geopop_df, province_names_short
):
    with pandas_activate_context(include_geometry=False):
        expected = (
            geopop_df.aggregate_province()
            .set_index('province_short')
            .loc[province_names_short.to_list()]
            .reset_index()
        )

        output = province_names_short.italy_geopop.from_province()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_mixed_names_and_codes_and_names_short(
    geopop_df, province_names, province_codes, province_names_short
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
            .loc[province_names_short.to_list()]
            .reset_index()
        )

        expected = pd.concat(
            [expected_names, expected_codes, expected_names_short], ignore_index=True
        )

        input = pd.concat(
            [province_names, province_codes, province_names_short], ignore_index=True
        )

        output = input.italy_geopop.from_province()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_region_information_from_names(
    geopop_df, region_names
):
    with pandas_activate_context(include_geometry=False):
        expected = (
            geopop_df.aggregate_region()
            .set_index('region')
            .loc[region_names.to_list()]
            .reset_index()
        )

        output = region_names.italy_geopop.from_region()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_region_information_from_codes(
    geopop_df, region_codes
):
    with pandas_activate_context(include_geometry=False):
        expected = (
            geopop_df.aggregate_region()
            .set_index('region_code')
            .loc[region_codes.to_list()]
            .reset_index()
        )

        output = region_codes.italy_geopop.from_region()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_region_information_from_mixed_names_and_codes(
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

        input = pd.concat([region_names, region_codes], ignore_index=True)

        output = input.italy_geopop.from_region()
    output = output[expected.columns]

    assert (output != expected).sum().sum() == 0


def test_pandas_extension_find_correct_province_information_from_complex_province_name(
    province_name_complex, province_name_complex_to_simple
):
    with pandas_activate_context(include_geometry=False):
        expected = province_name_complex_to_simple.italy_geopop.from_province()
        output = province_name_complex.italy_geopop.smart_from_province()
    assert (output != expected).sum().sum() == 0


def test_pandas_extension_return_nan_for_non_unequivocal_province_name(
    not_unequivocal_province_name_complex,
):
    with pandas_activate_context(include_geometry=False):
        output = (
            not_unequivocal_province_name_complex.italy_geopop.smart_from_province()
        )
    assert output.isna().all().all()


def test_pandas_extension_find_correct_region_information_from_complex_region_name(
    region_name_complex, region_name_complex_to_simple
):
    with pandas_activate_context(include_geometry=False):
        expected = region_name_complex_to_simple.italy_geopop.from_region()
        output = region_name_complex.italy_geopop.smart_from_region()
    assert (output != expected).sum().sum() == 0


def test_pandas_extension_return_nan_for_non_unequivocal_province_name(
    not_unequivocal_region_name_complex,
):
    with pandas_activate_context(include_geometry=False):
        output = not_unequivocal_region_name_complex.italy_geopop.smart_from_region()
    assert output.isna().all().all()
