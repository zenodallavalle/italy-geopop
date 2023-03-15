import geopandas as gpd
import pandas as pd
import pytest
import warnings

from italy_geopop.geopop import Geopop

_municipality_columns = [
    'municipality',
    'province',
    'province_code',
    'province_short',
    'region',
    'region_code',
]

_province_columns = [
    'region',
    'region_code',
    'province',
    'province_short',
    'municipalities',
]

_region_columns = [
    'region',
    'provinces',
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
def gp() -> Geopop:
    return Geopop()


@pytest.mark.parametrize(
    'df',
    [
        Geopop().italy_municipalities,
        Geopop().italy_provinces,
        Geopop().italy_regions,
        Geopop().population_df,
        Geopop().get_italian_population_for_municipalites(),
        Geopop().get_italian_population_for_provinces(),
        Geopop().get_italian_population_for_regions(),
    ],
)
def test_is_pandas_instance(df):
    assert isinstance(df, pd.DataFrame)


@pytest.mark.parametrize(
    'df',
    [
        Geopop().italy_municipalities_geometry,
        Geopop().italy_provinces_geometry,
        Geopop().italy_regions_geometry,
    ],
)
def test_is_geopandas_instance(df):
    assert isinstance(df, gpd.GeoDataFrame)


@pytest.mark.parametrize(
    'df,index,columns_list',
    [
        (
            Geopop().italy_municipalities,
            'municipality_code',
            _municipality_columns,
        ),
        (
            Geopop().italy_provinces,
            'province_code',
            _province_columns,
        ),
        (
            Geopop().italy_regions,
            'region_code',
            _region_columns,
        ),
        (
            Geopop().population_df,
            'municipality_code',
            ['age', 'F', 'M', 'tot'],
        ),
        (
            Geopop().get_italian_population_for_municipalites(),
            'municipality_code',
            _auto_population_limits_columns,
        ),
        (
            Geopop().get_italian_population_for_provinces(),
            'province_code',
            _auto_population_limits_columns,
        ),
        (
            Geopop().get_italian_population_for_regions(),
            'region_code',
            _auto_population_limits_columns,
        ),
        (Geopop().italy_municipalities_geometry, 'municipality_code', ['geometry']),
        (Geopop().italy_provinces_geometry, 'province_code', ['geometry']),
        (Geopop().italy_regions_geometry, 'region_code', ['geometry']),
    ],
)
def test_dataframe_has_the_right_index_and_columns(df, index, columns_list):
    assert df.index.name == index
    df_columns = list(df.columns)

    for col in columns_list:
        assert col in df_columns
        if col in df_columns:
            df_columns.remove(col)
    if len(df_columns):
        raise AssertionError(
            'Columns "{}" are not expected in dataframe'.format(df_columns)
        )


def test_population_male_female_if_present_is_coherent(gp):
    municipality_pop_df = gp.compose_df(level='municipality', population_limits='total')
    municipality_pop_df['_check_population'] = (
        municipality_pop_df.population_M + municipality_pop_df.population_F
    ).round()
    diff_df = municipality_pop_df[
        municipality_pop_df.population != municipality_pop_df._check_population
    ].copy()
    diff_df = diff_df.dropna(
        subset=['population_M', 'population_F', 'population'], how='all'
    )
    if len(diff_df.population):
        raise AssertionError(
            'population_M + population_F differs from population for municipalities: {}.'.format(
                ', '.join(diff_df.municipality)
            )
        )


@pytest.mark.parametrize(
    'df,expected_length',
    [
        (Geopop().italy_municipalities, 7904),
        (Geopop().italy_provinces, 107),
        (Geopop().italy_regions, 20),
        # (
        #     Geopop().get_italian_population_for_municipalites(),
        #     7904,
        # ),
        (Geopop().get_italian_population_for_provinces(), 107),
        (Geopop().get_italian_population_for_regions(), 20),
        # (Geopop().italy_municipalities_geometry, 7904),
        (Geopop().italy_provinces_geometry, 107),
        (Geopop().italy_regions_geometry, 20),
        (Geopop().compose_df(level='municipality'), 7904),
        (Geopop().compose_df(level='province'), 107),
        (Geopop().compose_df(level='region'), 20),
    ],
)
def test_series_length_is_right(df, expected_length):
    assert len(df) == expected_length


def test_if_population_data_is_missing(gp):
    municipality_pop_df = gp.compose_df(level='municipality', population_limits='total')
    if municipality_pop_df.isnull().sum().sum():
        na_municipalities = municipality_pop_df.municipality.loc[
            municipality_pop_df.population_M.isnull()
        ]
        warnings.warn(
            'population_M mussing for municipalities: {}.'.format(
                ', '.join(na_municipalities)
            )
        )

    if municipality_pop_df.isnull().sum().sum():
        na_municipalities = municipality_pop_df.municipality.loc[
            municipality_pop_df.population_M.isnull()
        ]
        warnings.warn(
            'population_F mussing for municipalities: {}.'.format(
                ', '.join(na_municipalities)
            )
        )

    if municipality_pop_df.isnull().sum().sum():
        na_municipalities = municipality_pop_df.municipality.loc[
            municipality_pop_df.population_M.isnull()
        ]
        warnings.warn(
            'population mussing for municipalities: {}.'.format(
                ', '.join(na_municipalities)
            )
        )
