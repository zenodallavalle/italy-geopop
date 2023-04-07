import geopandas as gpd
import pandas as pd
import numpy as np

import pytest

from italy_geopop._utils import generate_labels_for_age_cutoffs, prepare_limits
from italy_geopop.geopop import Geopop
from italy_geopop.pandas_extension import pandas_activate_context


_municipality_columns = [
    'municipality',
    'municipality_code',
    'cadastral_code',
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

_total_population_columns = [
    'population',
    'population_M',
    'population_F',
]

_auto_population_limits_columns = [
    '<3_F',
    '3-11_F',
    '11-19_F',
    '19-25_F',
    '25-50_F',
    '50-65_F',
    '65-75_F',
    '>=75_F',
    '<3_M',
    '3-11_M',
    '11-19_M',
    '19-25_M',
    '25-50_M',
    '50-65_M',
    '65-75_M',
    '>=75_M',
    '<3',
    '3-11',
    '11-19',
    '19-25',
    '25-50',
    '50-65',
    '65-75',
    '>=75',
]


@pytest.fixture
def dummy_series() -> pd.Series:
    """
    Returns a pd.Series with empty string values '' indexed as range(0, 500, 5).
    """
    index = list(range(0, 500, 5))
    return pd.Series(['' for _ in index], index=index)


@pytest.fixture(params=['names', 'codes', 'both'])
def municipality(request) -> pd.Series:
    """
    Returns a pd.Series with some valid municipality names if params='name' else municipality codes if params='codes' else myxed-type. This function ensures that returned municipalities are unique in Italy municipalities.
    """
    if request.param == 'names':
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

    elif request.param == 'codes':
        return pd.Series(
            [70070, 88007, 60018, 4001, 16131, 17097, 4071, 29026, 26084, 6015]
        )
    elif request.param == 'cadastral':
        return pd.Series(
            [
                'B368',
                'H838',
                'M212',
                'M194',
                'H265',
                'H432',
                'C236',
                'C879',
                'B160',
                'B551',
            ]
        )
    else:
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
                70070,
                88007,
                60018,
                4001,
                16131,
                17097,
                4071,
                29026,
                26084,
                6015,
            ]
        )


@pytest.fixture
def municipality_name_complex() -> pd.Series:
    """
    Returns a pd.Series with a valid complex municipality name.
    """
    return pd.Series(['Comune di Abano Terme'])


@pytest.fixture
def municipality_name_complex_to_simple() -> pd.Series:
    """
    Returns a pd.Series with a the right simple name for municipality_name_complex above.
    """
    return pd.Series(['abano terme'])


@pytest.fixture
def not_unequivocal_municipality_name_complex() -> pd.Series:
    """
    Returns a pd.Series with a non-unequivocal complex municipality name.
    """
    return pd.Series(['Verona or Milano'])


@pytest.fixture(params=['names', 'codes', 'abbreviation', 'mixed'])
def province(request) -> pd.Series:
    """
    Returns a pd.Series with some valid provinces names if type='names', provinces codes if type='codes', province abbreviations if type='abbreviation' else mixed-type list.
    """
    if request.param == 'names':
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
    elif request.param == 'codes':
        return pd.Series([68, 26, 75, 7, 32, 74, 4, 38, 57, 47])
    elif request.param == 'abbreviations':
        return pd.Series(['AG', 'RO', 'SA', 'CH', 'CN', 'SS', 'GO', 'LO', 'AQ', 'TS'])
    else:
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
                68,
                26,
                75,
                7,
                32,
                74,
                4,
                38,
                57,
                4,
                'AG',
                'RO',
                'SA',
                'CH',
                'CN',
                'SS',
                'GO',
                'LO',
                'AQ',
                'TS',
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


@pytest.fixture(params=['names', 'codes', 'both'])
def region(request) -> pd.Series:
    """
    Returns a pd.Series with some valid regions names if type='names', regions codes if type='codes' else mixed-type list.
    """
    if request.param == 'names':
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
    elif request.param == 'codes':
        return pd.Series([18, 15, 6, 1, 3, 13, 10, 14, 5, 19])
    else:
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
                18,
                15,
                6,
                1,
                3,
                13,
                10,
                14,
                5,
                19,
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


# Ensure same index as input series index


@pytest.mark.parametrize('include_geometry', [True, False])
@pytest.mark.parametrize('population_limits', ['auto', 'total', [50.0, 75]])
@pytest.mark.parametrize('level', ['municipality', 'province', 'region'])
def test_pandas_extension_return_df_with_same_index_as_input(
    dummy_series, level, include_geometry, population_limits
):
    with pandas_activate_context(include_geometry=include_geometry):
        if level == 'municipality':
            output = dummy_series.italy_geopop.from_municipality(
                population_limits=population_limits
            )
        elif level == 'province':
            output = dummy_series.italy_geopop.from_province(
                population_limits=population_limits
            )
        elif level == 'region':
            output = dummy_series.italy_geopop.from_region(
                population_limits=population_limits
            )
    diffs = output.index.to_series() != dummy_series.index.to_series()
    assert diffs.sum() == 0


# Ensure returned df has correct columns


@pytest.mark.parametrize('include_geometry', [True, False])
@pytest.mark.parametrize(
    'population_limits,population_labels',
    [
        ('auto', None),
        ('total', None),
        ([50.0, 75], None),
        ([50], ['below_50', 'above_50']),
    ],
)
def test_pandas_extension_from_municipality_returns_right_columns(
    municipality, include_geometry, population_limits, population_labels
):
    if population_limits == 'auto':
        pop_cols = _auto_population_limits_columns
    elif population_limits == 'total':
        pop_cols = _total_population_columns
    else:
        pop_cols = []
        if population_labels is None:
            _pop_limits = prepare_limits(population_limits)
            for c in generate_labels_for_age_cutoffs(_pop_limits):
                pop_cols.append(c)
                pop_cols.append(f'{c}_M')
                pop_cols.append(f'{c}_F')
        else:
            for c in population_labels:
                pop_cols.append(c)
                pop_cols.append(f'{c}_M')
                pop_cols.append(f'{c}_F')
    with pandas_activate_context(include_geometry=include_geometry):
        output = municipality.italy_geopop.from_municipality(
            population_limits=population_limits, population_labels=population_labels
        )
    df_columns = list(output.columns)
    for c in (
        _municipality_columns
        + _province_columns
        + _region_columns
        + pop_cols
        + (['geometry'] if include_geometry else [])
    ):
        pytest.assume(c in df_columns)
        if c in df_columns:
            df_columns.remove(c)
    assert len(df_columns) == 0


@pytest.mark.parametrize('include_geometry', [True, False])
@pytest.mark.parametrize(
    'population_limits,population_labels',
    [
        ('auto', None),
        ('total', None),
        ([50.0, 75], None),
        ([50], ['below_50', 'above_50']),
    ],
)
def test_pandas_extension_from_municipality_finds_results(
    municipality, include_geometry, population_limits, population_labels
):
    if population_limits == 'auto':
        pop_cols = _auto_population_limits_columns
    elif population_limits == 'total':
        pop_cols = _total_population_columns
    else:
        pop_cols = []
        if population_labels is None:
            _pop_limits = prepare_limits(population_limits)
            for c in generate_labels_for_age_cutoffs(_pop_limits):
                pop_cols.append(c)
                pop_cols.append(f'{c}_M')
                pop_cols.append(f'{c}_F')
        else:
            for c in population_labels:
                pop_cols.append(c)
                pop_cols.append(f'{c}_M')
                pop_cols.append(f'{c}_F')
    with pandas_activate_context(include_geometry=include_geometry):
        output = municipality.italy_geopop.from_municipality(
            population_limits=population_limits, population_labels=population_labels
        )
    assert not len(output[output.municipality_code.isna()])


@pytest.mark.parametrize('include_geometry', [True, False])
@pytest.mark.parametrize(
    'population_limits,population_labels',
    [
        ('auto', None),
        ('total', None),
        ([50.0, 75], None),
        ([50], ['below_50', 'above_50']),
    ],
)
def test_pandas_extension_from_province_returns_right_columns(
    province, include_geometry, population_limits, population_labels
):
    if population_limits == 'auto':
        pop_cols = _auto_population_limits_columns
    elif population_limits == 'total':
        pop_cols = _total_population_columns
    else:
        pop_cols = []
        if population_labels is None:
            _pop_limits = prepare_limits(population_limits)
            for c in generate_labels_for_age_cutoffs(_pop_limits):
                pop_cols.append(c)
                pop_cols.append(f'{c}_M')
                pop_cols.append(f'{c}_F')
        else:
            for c in population_labels:
                pop_cols.append(c)
                pop_cols.append(f'{c}_M')
                pop_cols.append(f'{c}_F')
    with pandas_activate_context(include_geometry=include_geometry):
        output = province.italy_geopop.from_province(
            population_limits=population_limits, population_labels=population_labels
        )
    df_columns = list(output.columns)
    for c in (
        ['municipalities']
        + _province_columns
        + _region_columns
        + pop_cols
        + (['geometry'] if include_geometry else [])
    ):
        pytest.assume(c in df_columns)
        if c in df_columns:
            df_columns.remove(c)
    assert len(df_columns) == 0


@pytest.mark.parametrize('include_geometry', [True, False])
@pytest.mark.parametrize(
    'population_limits,population_labels',
    [
        ('auto', None),
        ('total', None),
        ([50.0, 75], None),
        ([50], ['below_50', 'above_50']),
    ],
)
def test_pandas_extension_from_province_finds_results(
    province, include_geometry, population_limits, population_labels
):
    if population_limits == 'auto':
        pop_cols = _auto_population_limits_columns
    elif population_limits == 'total':
        pop_cols = _total_population_columns
    else:
        pop_cols = []
        if population_labels is None:
            _pop_limits = prepare_limits(population_limits)
            for c in generate_labels_for_age_cutoffs(_pop_limits):
                pop_cols.append(c)
                pop_cols.append(f'{c}_M')
                pop_cols.append(f'{c}_F')
        else:
            for c in population_labels:
                pop_cols.append(c)
                pop_cols.append(f'{c}_M')
                pop_cols.append(f'{c}_F')
    with pandas_activate_context(include_geometry=include_geometry):
        output = province.italy_geopop.from_province(
            population_limits=population_limits, population_labels=population_labels
        )
    assert not len(output[output.province_code.isna()])


@pytest.mark.parametrize('include_geometry', [True, False])
@pytest.mark.parametrize(
    'population_limits,population_labels',
    [
        ('auto', None),
        ('total', None),
        ([50.0, 75], None),
        ([50], ['below_50', 'above_50']),
    ],
)
def test_pandas_extension_from_region_returns_right_columns(
    region, include_geometry, population_limits, population_labels
):
    if population_limits == 'auto':
        pop_cols = _auto_population_limits_columns
    elif population_limits == 'total':
        pop_cols = _total_population_columns
    else:
        pop_cols = []
        if population_labels is None:
            _pop_limits = prepare_limits(population_limits)
            for c in generate_labels_for_age_cutoffs(_pop_limits):
                pop_cols.append(c)
                pop_cols.append(f'{c}_M')
                pop_cols.append(f'{c}_F')
        else:
            for c in population_labels:
                pop_cols.append(c)
                pop_cols.append(f'{c}_M')
                pop_cols.append(f'{c}_F')
    with pandas_activate_context(include_geometry=include_geometry):
        output = region.italy_geopop.from_region(
            population_limits=population_limits, population_labels=population_labels
        )
    df_columns = list(output.columns)
    for c in (
        ['provinces']
        + _region_columns
        + pop_cols
        + (['geometry'] if include_geometry else [])
    ):
        pytest.assume(c in df_columns)
        if c in df_columns:
            df_columns.remove(c)
    assert len(df_columns) == 0


@pytest.mark.parametrize('include_geometry', [True, False])
@pytest.mark.parametrize(
    'population_limits,population_labels',
    [
        ('auto', None),
        ('total', None),
        ([50.0, 75], None),
        ([50], ['below_50', 'above_50']),
    ],
)
def test_pandas_extension_from_region_finds_results(
    region, include_geometry, population_limits, population_labels
):
    if population_limits == 'auto':
        pop_cols = _auto_population_limits_columns
    elif population_limits == 'total':
        pop_cols = _total_population_columns
    else:
        pop_cols = []
        if population_labels is None:
            _pop_limits = prepare_limits(population_limits)
            for c in generate_labels_for_age_cutoffs(_pop_limits):
                pop_cols.append(c)
                pop_cols.append(f'{c}_M')
                pop_cols.append(f'{c}_F')
        else:
            for c in population_labels:
                pop_cols.append(c)
                pop_cols.append(f'{c}_M')
                pop_cols.append(f'{c}_F')
    with pandas_activate_context(include_geometry=include_geometry):
        output = region.italy_geopop.from_region(
            population_limits=population_limits, population_labels=population_labels
        )
    assert not len(output[output.region_code.isna()])


# Test smart features
@pytest.mark.parametrize('include_geometry', [True, False])
def test_pandas_extension_find_correct_municipality_information_from_complex_municipality_name(
    municipality_name_complex, municipality_name_complex_to_simple, include_geometry
):
    with pandas_activate_context(include_geometry=include_geometry):
        expected = municipality_name_complex_to_simple.italy_geopop.from_municipality()
        output = municipality_name_complex.italy_geopop.smart_from_municipality()
    assert (output != expected).sum().sum() == 0


@pytest.mark.parametrize('include_geometry', [True, False])
def test_pandas_extension_return_nan_for_non_unequivocal_municipality_name(
    not_unequivocal_municipality_name_complex, include_geometry
):
    with pandas_activate_context(include_geometry=include_geometry):
        output = (
            not_unequivocal_municipality_name_complex.italy_geopop.smart_from_municipality()
        )
    assert output.isna().all().all()


@pytest.mark.parametrize('include_geometry', [True, False])
def test_pandas_extension_find_correct_province_information_from_complex_province_name(
    province_name_complex, province_name_complex_to_simple, include_geometry
):
    with pandas_activate_context(include_geometry=include_geometry):
        expected = province_name_complex_to_simple.italy_geopop.from_province().drop(
            ['municipalities'], axis=1
        )
        output = province_name_complex.italy_geopop.smart_from_province().drop(
            ['municipalities'], axis=1
        )
    assert (output != expected).sum().sum() == 0


@pytest.mark.parametrize('include_geometry', [True, False])
def test_pandas_extension_return_nan_for_non_unequivocal_province_name(
    not_unequivocal_province_name_complex, include_geometry
):
    with pandas_activate_context(include_geometry=include_geometry):
        output = (
            not_unequivocal_province_name_complex.italy_geopop.smart_from_province()
        )
    assert output.isna().all().all()


@pytest.mark.parametrize('include_geometry', [True, False])
def test_pandas_extension_find_correct_region_information_from_complex_region_name(
    region_name_complex, region_name_complex_to_simple, include_geometry
):
    with pandas_activate_context(include_geometry=include_geometry):
        expected = region_name_complex_to_simple.italy_geopop.from_region().drop(
            ['provinces'], axis=1
        )
        output = region_name_complex.italy_geopop.smart_from_region().drop(
            ['provinces'], axis=1
        )
    assert (output != expected).sum().sum() == 0


@pytest.mark.parametrize('include_geometry', [True, False])
def test_pandas_extension_return_nan_for_non_unequivocal_region_name(
    not_unequivocal_region_name_complex, include_geometry
):
    with pandas_activate_context(include_geometry=include_geometry):
        output = not_unequivocal_region_name_complex.italy_geopop.smart_from_region()
    assert output.isna().all().all()


# Decide if is worth to add a test that checks if returned data is correct
