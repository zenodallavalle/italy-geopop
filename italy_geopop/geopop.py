import geopandas as gpd
import numpy as np
import pandas as pd
import os

_current_abs_dir = os.path.dirname(os.path.realpath(__file__))


class ItalyGeopopDataFrame(pd.DataFrame):
    """A subclass of `pandas.DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_ that contains italian population from ISTAT."""

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
                    'province',
                    'province_code',
                    'province_short',
                    'region',
                    'region_code',
                    'population',
                    'population_F',
                    'population_M',
                ]
            ]
            .groupby(['province', 'province_code', 'province_short'])
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
                    # 'NA' #This is Napoli province abbreviation
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
        """Aggregate provinces.

        :return: 2-dimensional dataframe with provinces, provinces codes, provinces abbreviations, regions, regions code, municipalities (as a list of municipality records (see :ref:`municipality data <municipality-data>`)) and population data for every province.
        :rtype: pandas.DataFrame
        """
        return (
            self.groupby(['province', 'province_code', 'province_short'])
            .apply(ItalyGeopopDataFrame._aggregate_province)
            .reset_index()
        )

    def aggregate_region(self) -> pd.DataFrame:
        """Aggregate provinces.

        :return: 2-dimensional dataframe with regions, regions code, provinces (as a list of provinces records (see :ref:`province data <province-data>`)) and population data for every region.
        :rtype: pandas.DataFrame
        """
        return (
            self.groupby(['region', 'region_code'])
            .apply(ItalyGeopopDataFrame._aggregate_region)
            .reset_index()
        )

    @classmethod
    def get_municipalities_geometry(cls) -> pd.DataFrame:
        """Classmethod to get geospatial data for plotting municipalities.

        :return: a 2-dimensional dataframe with one column, ``geometry``, and ``municipality_code`` as index.
        :rtype: pd.DataFrame
        """
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
    def get_provinces_geometry(cls) -> pd.DataFrame:
        """Classmethod to get geospatial data for plotting provinces.

        :return: a 2-dimensional dataframe with one column, ``geometry``, and ``province_code`` as index.
        :rtype: pd.DataFrame
        """
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
    def get_regions_geometry(cls) -> pd.DataFrame:
        """Classmethod to get geospatial data for plotting regions.

        :return: a 2-dimensional dataframe with one column, ``geometry``, and ``region_code`` as index.
        :rtype: pd.DataFrame
        """
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
