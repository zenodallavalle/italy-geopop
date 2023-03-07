from contextlib import contextmanager
from functools import cache
import numpy as np
import pandas as pd
from warnings import warn

from ._utils import handle_return_cols, simple_cache, match_single_word
from . import geopop


class ItalyGeopop:
    """Serves as base for registering ``italy_geopop`` as pandas accessor. You shouldn't initalize it directly.

    Instead, from a ``pandas.Series`` object you can access its methods via ``italy_geopop`` attribute.
    """

    def __init__(self, pandas_obj) -> None:
        self._obj = pandas_obj

    @classmethod
    def _generate_empty_serie(cls, columns) -> pd.Series:
        return pd.Series([np.nan for _ in columns], index=columns)

    @property
    def population_df(self) -> geopop.ItalyGeopopDataFrame:
        """Get all italy-geopop data in a subclass of ``pandas.DataFrame.``

        :return: All population (and geospatials if accessor was initialized with ``include_geometry=True``) data for every municipality.
        :rtype: geopop.ItalyGeopopDataFrame
        """
        return self.italy_geopop_df

    @staticmethod
    @simple_cache
    def _generate_municipality_dfs(
        italy_geopop_df: geopop.ItalyGeopopDataFrame, include_geometry: bool
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        if not include_geometry:
            temp_df = italy_geopop_df.copy()
        else:
            temp_df = pd.merge(
                italy_geopop_df.get_municipalities_geometry(),
                italy_geopop_df,
                how='outer',
                right_on='municipality_code',
                left_index=True,
            )
        temp_df['_index'] = temp_df.municipality.str.lower()
        str_indexed = temp_df.set_index('_index')
        temp_df['_index'] = temp_df.municipality_code
        code_indexed = temp_df.set_index('_index')
        return str_indexed, code_indexed

    def from_municipality(self, return_cols=None) -> pd.DataFrame:
        """Get data for municipalities.
        Input series can contain municipalities names or municipalities istat codes; *data types can also be mixed*.
        If input data is not found in italian data, a row of NaNs is returned, *this behaviour may change in the future.*

        :param return_cols: used to subset the returned data in order to provide the requested fields. If None, all available fields are returned. The available fields are listed above, defaults to None.
        :type include_geometry: bool, optional

        :raises KeyError: if return_cols is or contains a column not listed above or includes ``geometry`` and accessor was intialize without geometry data.

        :return: Requested data in a 2-dimensional dataframe that has the same index of input data.
        :rtype: pandas.DataFrame
        """
        str_indexed, code_indexed = self._generate_municipality_dfs(
            self.italy_geopop_df, include_geometry=self.include_geometry
        )
        empty_serie = self._generate_empty_serie(str_indexed.columns.to_list())
        str_indexed = dict(str_indexed.iterrows())
        code_indexed = dict(code_indexed.iterrows())

        @cache
        def get_data(x) -> pd.Series:
            x = str(x).strip().lower()
            try:
                x = int(float(x))
                return code_indexed.get(x, empty_serie)
            except Exception:
                return str_indexed.get(x, empty_serie)

        return handle_return_cols(self._obj.apply(get_data), return_cols)

    @staticmethod
    @simple_cache
    def _generate_province_dfs(
        italy_geopop_df: geopop.ItalyGeopopDataFrame, include_geometry: bool
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        if not include_geometry:
            temp_df = italy_geopop_df.aggregate_province()
        else:
            temp_df = pd.merge(
                italy_geopop_df.get_provinces_geometry(),
                italy_geopop_df.aggregate_province(),
                how='outer',
                right_on='province_code',
                left_index=True,
            )

        temp_df['_index'] = temp_df.province.str.lower()
        str_indexed = temp_df.set_index('_index')
        temp_df['_index'] = temp_df.province_code
        code_indexed = temp_df.set_index('_index')
        temp_df['_index'] = temp_df.province_short.str.upper()
        short_str_indexed = temp_df.set_index('_index')
        return str_indexed, code_indexed, short_str_indexed

    def from_province(self, return_cols=None) -> pd.DataFrame:
        """Get data for provinces.
        Input series can contain provinces names, provinces abbreviations or provinces istat codes; *data types can also be mixed*.
        If input data is not found in italian data, a row of NaNs is returned, *this behaviour may change in the future.*

        :param return_cols: used to subset the returned data in order to provide the requested fields. If None, all available fields are returned. The available fields are listed above, defaults to None.
        :type include_geometry: bool, optional

        .. note::
            To understand how ``municipalities`` are grouped, see above :ref:`Municipality data <municipality-data>`.

        :raises KeyError: if return_cols is or contains a column not listed above or includes ``geometry`` and accessor was intialize without geometry data.

        :return: Requested data in a 2-dimensional dataframe that has the same index of input data.
        :rtype: pandas.DataFrame
        """
        str_indexed, code_indexed, short_str_indexed = self._generate_province_dfs(
            self.italy_geopop_df, include_geometry=self.include_geometry
        )

        empty_serie = self._generate_empty_serie(str_indexed.columns.to_list())

        str_indexed = dict(str_indexed.iterrows())
        code_indexed = dict(code_indexed.iterrows())
        short_str_indexed = dict(short_str_indexed.iterrows())

        @cache
        def get_data(x) -> pd.Series:
            x = str(x).strip()
            try:
                x = int(float(x))
                return code_indexed.get(x, empty_serie)
            except ValueError:
                if len(x) == 2:
                    return short_str_indexed.get(x.upper(), empty_serie)

                else:
                    return str_indexed.get(x.lower(), empty_serie)

        return handle_return_cols(self._obj.apply(get_data), return_cols)

    @staticmethod
    @simple_cache
    def _generate_region_dfs(
        italy_geopop_df: geopop.ItalyGeopopDataFrame, include_geometry: bool
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        if not include_geometry:
            temp_df = italy_geopop_df.aggregate_region()
        else:
            temp_df = pd.merge(
                italy_geopop_df.get_regions_geometry(),
                italy_geopop_df.aggregate_region(),
                how='outer',
                right_on='region_code',
                left_index=True,
            )
        temp_df['_index'] = temp_df.region.str.lower()
        str_indexed = temp_df.set_index('_index')
        temp_df['_index'] = temp_df.region_code
        code_indexed = temp_df.set_index('_index')
        return str_indexed, code_indexed

    def from_region(self, return_cols=None) -> pd.DataFrame:
        """Get data for regions.
        Input series can contain regions names or regions istat codes; *data types can also be mixed*.
        If input data is not found in italian data, a row of NaNs is returned, *this behaviour may change in the future.*

        :param return_cols: used to subset the returned data in order to provide the requested fields. If None, all available fields are returned. The available fields are listed above, defaults to None.
        :type include_geometry: bool, optional

        .. note::
            To understand how ``provinces`` are grouped, see above :ref:`Province data <province-data>`.

        :raises KeyError: if return_cols is or contains a column not listed above or includes ``geometry`` and accessor was intialize without geometry data.

        :return: Requested data in a 2-dimensional dataframe that has the same index of input data.
        :rtype: pandas.DataFrame
        """
        str_indexed, code_indexed = self._generate_region_dfs(
            self.italy_geopop_df, include_geometry=self.include_geometry
        )
        empty_serie = self._generate_empty_serie(str_indexed.columns.to_list())

        str_indexed = dict(str_indexed.iterrows())
        code_indexed = dict(code_indexed.iterrows())

        @cache
        def get_data(x) -> pd.Series:
            x = str(x).strip().lower()
            try:
                x = int(float(x))
                return code_indexed.get(x, empty_serie)
            except ValueError:
                return str_indexed.get(x, empty_serie)

        return handle_return_cols(self._obj.apply(get_data), return_cols)

    def smart_from_municipality(self, return_cols=None) -> pd.DataFrame | pd.Series:
        """Same as ``from_municipality`` but can understand more complex text. Values are returned only if match is unequivocal.


        .. code-block:: python
           :linenos:

           >>> s = pd.Series(["Comune di Abano Terme", "Comune di Airasca", "Comune di Milano o di Verona?", 1001])
           >>> s.italy_geopop.smart_from_municipality(return_cols='municipality')
           0    Abano Terme
           1        Airasca
           2            NaN
           3          Agliè
           Name: municipality, dtype: object


        """
        str_indexed = self._generate_municipality_dfs(
            self.italy_geopop_df, include_geometry=self.include_geometry
        )[0]
        ret = self.from_municipality()
        nans = self._obj[ret[ret.municipality.isnull()].index].copy()

        empty_serie = self._generate_empty_serie(str_indexed.columns.to_list())
        str_indexed = dict(str_indexed.iterrows())

        @cache
        def get_data(x):
            key = match_single_word(str_indexed.keys(), str(x).strip().lower())
            return str_indexed.get(key, empty_serie)

        ret = ret.fillna(nans.apply(get_data))

        return handle_return_cols(ret, return_cols=return_cols)

    def smart_from_province(self, return_cols=None) -> pd.DataFrame | pd.Series:
        """Same as ``from_province`` but can understand more complex text. Values are returned only if match is unequivocal.


        .. code-block:: python
           :linenos:

           >>> s = pd.Series(["Citta' di Brescia", "Università degli studi di Milano", "Milano o Verona", 5])
           >>> s.italy_geopop.smart_from_province(return_cols='province')
           0    Brescia
           1     Milano
           2        NaN
           3       Asti
           Name: province, dtype: object


        """
        str_indexed = self._generate_province_dfs(
            self.italy_geopop_df, include_geometry=self.include_geometry
        )[0]
        ret = self.from_province()
        nans = self._obj[ret[ret.region.isnull()].index].copy()

        empty_serie = self._generate_empty_serie(str_indexed.columns.to_list())
        str_indexed = dict(str_indexed.iterrows())

        @cache
        def get_data(x):
            key = match_single_word(str_indexed.keys(), str(x).strip().lower())
            return str_indexed.get(key, empty_serie)

        ret = ret.fillna(nans.apply(get_data))

        return handle_return_cols(ret, return_cols=return_cols)

    def smart_from_region(self, return_cols=None) -> pd.DataFrame | pd.Series:
        """Same as ``from_region`` but can understand more complex text. Values are returned only if match is unequivocal.


        .. code-block:: python
           :linenos:

           >>> s = pd.Series(["Regione Lombardia", "Regione del Veneto", "Piemonte o Umbria?", 15])
           >>> s.italy_geopop.smart_from_region(return_cols='region')
           0    Lombardia
           1       Veneto
           2          NaN
           3     Campania
           Name: region, dtype: object


        """
        str_indexed = self._generate_region_dfs(
            self.italy_geopop_df, include_geometry=self.include_geometry
        )[0]
        ret = self.from_region()
        nans = self._obj[ret[ret.region.isnull()].index].copy()

        empty_serie = self._generate_empty_serie(str_indexed.columns.to_list())
        str_indexed = dict(str_indexed.iterrows())

        @cache
        def get_data(x):
            key = match_single_word(str_indexed.keys(), str(x).strip().lower())
            return str_indexed.get(key, empty_serie)

        ret = ret.fillna(nans.apply(get_data))

        return handle_return_cols(ret, return_cols=return_cols)


def pandas_activate(include_geometry=False):
    """Activate pandas extension registering class :py:class:ItalyGeopop as pandas.Series `accessor <https://pandas.pydata.org/docs/development/extending.html>`_ named ``italy_geopop``.

    :param include_geometry: specifies if geometry column should also be returned when accessor is used, defaults to False
    :type include_geometry: bool, optional

    :return: None

    .. warning::
        ``include_geometry=True`` comports costs in term of speed as geospatial datasets need to be loaded.
    """

    @pd.api.extensions.register_series_accessor('italy_geopop')
    class Accessor(ItalyGeopop):
        def __init__(self, pandas_obj) -> None:
            self.italy_geopop_df = geopop.ItalyGeopopDataFrame()
            self.include_geometry = include_geometry
            super().__init__(pandas_obj)


@contextmanager
def pandas_activate_context(include_geometry=False):
    """
    Same as activate but lives within the context. Useful if you want to register the accessor with different
    initialization options more than once in your code or if you want to free up memory right after you get the needed data
    (the trade off is that italy-geopop needs to be reinitialized everytime you register and use the accessor).

    :param include_geometry: same as `italy_geopop.activate <#italy_geopop.pandas_extension.pandas_activate>`_.
    :yields: Context with ``italy_geopop`` accessor registered to pd.Series.

    .. code-block:: python

       # pandas_activate_context example

       with pandas_activate_context():
           # You can access italy_geopop here

       # You cannot access italy_geopop here
    """
    try:
        pandas_activate(include_geometry=include_geometry)
        yield
    except Exception as e:
        raise e
    finally:
        try:
            del pd.Series.italy_geopop
        except AttributeError:
            pass
