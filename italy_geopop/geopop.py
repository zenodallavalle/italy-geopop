import geopandas as gpd
import numpy as np
import pandas as pd
import os

from .decorators import cache

_current_abs_dir = os.path.dirname(os.path.realpath(__file__))


class ItalyGeopopDataFrame(pd.DataFrame):
    @classmethod
    def _generate_municipality_records(cls, df) -> pd.Series:
        data = df[['municipality_code', 'municipality']].to_dict('records')
        return pd.Series([data], index=['municipalities'])

    @classmethod
    def _generate_province_records(cls, df) -> pd.Series:
        ret = (
            df.groupby(['province_code', 'province', 'province_short'])
            .apply(cls._generate_municipality_records)
            .reset_index()
        )
        data = ret.to_dict('records')
        return pd.Series([data], index=['provinces'])

    @classmethod
    def _aggregate_province(cls, df) -> pd.Series:
        left_row = cls._generate_municipality_records(df)
        right_row = (
            df[
                [
                    'province_code',
                    'province',
                    'province_short',
                    'region',
                    'region_code',
                    'population',
                    'population_F',
                    'population_M',
                ]
            ]
            .groupby(['province_code', 'province', 'province_short'])
            .agg(
                {
                    'region': 'first',
                    'region_code': 'first',
                    'population': 'sum',
                    'population_F': 'sum',
                    'population_M': 'sum',
                }
            )
            .iloc[0, :]
        )
        print(pd.concat([left_row, right_row]))
        return pd.concat([left_row, right_row])

    @classmethod
    def _aggregate_region(cls, df) -> pd.Series:
        left_row = cls._generate_province_records(df)
        right_row = df[['population', 'population_F', 'population_M']].sum()
        return pd.concat([left_row, right_row])

    def __init__(self) -> None:
        super().__init__(
            pd.read_csv(
                os.path.join(_current_abs_dir, 'italy_geo_pop_2022.csv'),
                na_values=[
                    '',
                    '#N/A',
                    '#N/A N/A',
                    '#NA',
                    '-1.#IND',
                    '-1.#QNAN',
                    '-NaN',
                    '-nan',
                    '1.#IND',
                    '1.#QNAN',
                    '<NA>',
                    'N/A',
                    'NULL',
                    'NaN',
                    'n/a',
                    'nan',
                    'null',
                    # 'NA' #This is used by Napoli short province
                ],
                keep_default_na=False,
                dtype={
                    'population_M': np.float64,
                    'population_F': np.float64,
                    'population': np.float64,
                },
            )
        )

    def aggregate_province(self) -> pd.DataFrame:
        return (
            self.groupby(['province_code', 'province', 'province_short'])
            .apply(ItalyGeopopDataFrame._aggregate_province)
            .reset_index()
        )

    def aggregate_region(self) -> pd.DataFrame:
        return (
            self.groupby(['region', 'region_code'])
            .apply(ItalyGeopopDataFrame._aggregate_region)
            .reset_index()
        )

    @classmethod
    @cache
    def get_municipalities_geometry(cls) -> pd.DataFrame:
        data = gpd.read_file(
            os.path.join(_current_abs_dir, 'limits_IT_municipalities.geojson')
        )
        cols_rename = {
            'com_istat_code_num': 'municipality_code',
            'geometry': 'geometry',
        }

        data = data.rename(columns=cols_rename)
        data = data[cols_rename.values()].set_index('municipality_code')
        return data

    @classmethod
    @cache
    def get_provinces_geometry(cls) -> pd.DataFrame:
        file = gpd.read_file(
            os.path.join(_current_abs_dir, './limits_IT_provinces.geojson')
        )
        cols_rename = {
            'prov_istat_code_num': 'province_code',
            'geometry': 'geometry',
        }

        file = file.rename(columns=cols_rename)
        file = file[cols_rename.values()].set_index('province_code')
        return file

    @classmethod
    @cache
    def get_regions_geometry(cls) -> pd.DataFrame:
        file = gpd.read_file(
            os.path.join(_current_abs_dir, './limits_IT_regions.geojson')
        )
        cols_rename = {
            'reg_istat_code_num': 'region_code',
            'geometry': 'geometry',
        }

        file = file.rename(columns=cols_rename)
        file = file[cols_rename.values()].set_index('region_code')
        return file
