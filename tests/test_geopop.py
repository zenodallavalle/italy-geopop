import geopandas as gpd
import pandas as pd
import pytest
import warnings

from italy_geopop.geopop import ItalyGeopopDataFrame

_required_columns = [
    'municipality',
    'municipality_code',
    'province_code',
    'province',
    'province_short',
    'region',
    'region_code',
    'population',
    'population_M',
    'population_F',
]


def test_initialization():
    df = ItalyGeopopDataFrame()
    assert isinstance(df, (ItalyGeopopDataFrame, pd.DataFrame))


@pytest.fixture
def geopop_df() -> ItalyGeopopDataFrame:
    return ItalyGeopopDataFrame()


def test_generate_municipality_records(geopop_df):
    for col in _required_columns:
        pytest.assume(col in geopop_df.columns)


def test_population_male_female_if_present_is_coherent(geopop_df):
    geopop_df['_check_population'] = (
        geopop_df.population_M + geopop_df.population_F
    ).round()
    diff_df = geopop_df[geopop_df.population != geopop_df._check_population].copy()
    diff_df = diff_df.dropna(
        subset=['population_M', 'population_F', 'population'], how='all'
    )
    if len(diff_df.population):
        raise AssertionError(
            'population_M + population_F differs from population in for municipalities: {}.'.format(
                ', '.join(diff_df.municipality)
            )
        )


def test_regions_are_20(geopop_df):
    assert len(geopop_df.region.unique()) == 20


def test_region_codes_are_20(geopop_df):
    assert len(geopop_df.region_code.unique()) == 20


def test_provinces_are_107(geopop_df):
    assert len(geopop_df.province.unique()) == 107


def test_provinces_short_are_107(geopop_df):
    assert len(geopop_df.province_short.unique()) == 107


def test_province_codes_are_107(geopop_df):
    assert len(geopop_df.province_code.unique()) == 107


def test_municipality_has_no_null_values(geopop_df):
    assert geopop_df.municipality.isnull().sum() == 0


def test_municipality_code_has_no_null_values(geopop_df):
    assert geopop_df.municipality_code.isnull().sum() == 0


def test_province_code_has_no_null_values(geopop_df):
    assert geopop_df.province_code.isnull().sum() == 0


def test_province_has_no_null_values(geopop_df):
    assert geopop_df.province.isnull().sum() == 0


def test_province_short_has_no_null_values(geopop_df):
    assert geopop_df.province_short.isnull().sum() == 0


def test_region_has_no_null_values(geopop_df):
    assert geopop_df.region.isnull().sum() == 0


def test_region_code_has_no_null_values(geopop_df):
    assert geopop_df.region_code.isnull().sum() == 0


def test_if_population_data_is_missing(geopop_df):
    if geopop_df.population_M.isnull().sum():
        na_municipalities = geopop_df.municipality.loc[geopop_df.population_M.isnull()]
        warnings.warn(
            'population_M mussing for municipalities: {}.'.format(
                ', '.join(na_municipalities)
            )
        )

    if geopop_df.population_F.isnull().sum():
        na_municipalities = geopop_df.municipality.loc[geopop_df.population_F.isnull()]
        warnings.warn(
            'population_F mussing for municipalities: {}.'.format(
                ', '.join(na_municipalities)
            )
        )

    if geopop_df.population.isnull().sum():
        na_municipalities = geopop_df.municipality.loc[geopop_df.population.isnull()]
        warnings.warn(
            'population mussing for municipalities: {}.'.format(
                ', '.join(na_municipalities)
            )
        )


def test_ItalyGeopopDataFrame_get_municipalities_geometry_is_geodataframe_instance(
    geopop_df,
):
    assert isinstance(geopop_df.get_municipalities_geometry(), gpd.GeoDataFrame)


def test_ItalyGeopopDataFrame_get_municipalities_geometry_has_geometry_column(
    geopop_df,
):
    assert hasattr(geopop_df.get_municipalities_geometry(), 'geometry')


def test_ItalyGeopopDataFrame_get_provinces_geometry_is_geodataframe_instance(
    geopop_df,
):
    assert isinstance(geopop_df.get_provinces_geometry(), gpd.GeoDataFrame)


def test_ItalyGeopopDataFrame_get_provinces_geometry_has_geometry_column(geopop_df):
    assert hasattr(geopop_df.get_provinces_geometry(), 'geometry')


def test_ItalyGeopopDataFrame_get_provinces_geometry_has_107_rows(geopop_df):
    assert len(geopop_df.get_provinces_geometry()) == 107


def test_ItalyGeopopDataFrame_get_regions_geometry_is_geodataframe_instance(geopop_df):
    assert isinstance(geopop_df.get_regions_geometry(), gpd.GeoDataFrame)


def test_ItalyGeopopDataFrame_get_regions_geometry_has_geometry_column(geopop_df):
    assert hasattr(geopop_df.get_regions_geometry(), 'geometry')


def test_ItalyGeopopDataFrame_get_regions_geometry_has_20_rows(geopop_df):
    assert len(geopop_df.get_regions_geometry()) == 20


## Add test for aggreagate_ methods
