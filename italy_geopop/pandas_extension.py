from contextlib import contextmanager
from functools import cache
import re
import numpy as np
import pandas as pd

from typing import Any, Optional

from ._utils import handle_return_cols, match_single_key
from . import geopop


class ItalyGeopop:
    """Serves as base for registering ``italy_geopop`` as pandas accessor. You shouldn't initalize it directly.

    Instead, from a ``pandas.Series`` object you can access its methods via ``italy_geopop`` attribute.
    """

    def __init__(
        self,
        pandas_obj: Any,
        include_geometry: bool = False,
        data_year: Optional[int] = None,
    ) -> None:
        self.data_year = data_year
        self.geopop = geopop.Geopop(data_year=self.data_year)
        self.include_geometry = include_geometry
        self._obj = pandas_obj

    @classmethod
    def _generate_empty_serie(cls, columns) -> pd.Series:
        return pd.Series([np.nan for _ in columns], index=columns)

    def get_population_data(
        self,
        level: str = "municipality",
        include_geometry: bool = False,
        population_limits: list | str = "auto",
        population_labels: list | None = None,
    ) -> pd.DataFrame:
        """Same as :py:meth:`italy_geopop.geopop.Geopop.compose_df`."""
        level = level.lower().strip()
        if level in set(["municipality", "province", "region"]):
            return self.geopop.compose_df(
                level=level,
                population_limits=population_limits,
                population_labels=population_labels,
                include_geometry=include_geometry,
            )

        else:
            raise ValueError(
                f'level must be "municipality", "province" or "region" not "{level}"'
            )

    def _generate_municipality_dfs(
        self,
        population_limits: list | str = "auto",
        population_labels: list | None = None,
        include_geometry: bool = False,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        temp_df = self.geopop.compose_df(
            level="municipality",
            population_limits=population_limits,
            population_labels=population_labels,
            include_geometry=include_geometry,
        )
        temp_df["_index"] = temp_df.municipality.str.lower()
        str_indexed = temp_df.set_index("_index")
        temp_df["_index"] = temp_df.municipality_code
        code_indexed = temp_df.set_index("_index")
        temp_df["_index"] = temp_df.cadastral_code.str.lower()
        cadastral_indexed = temp_df.set_index("_index")
        return str_indexed, code_indexed, cadastral_indexed

    def from_municipality(
        self,
        return_cols: list | str | re.Pattern | None = None,
        regex: bool = False,
        population_limits: list | str = "auto",
        population_labels: list | None = None,
    ) -> pd.DataFrame:
        """Get data for municipalities.
        Input series can contain municipalities names, municipalities istat codes or municipalities cadastral code (also known as Belfiore's code); *data types can also be mixed*.
        If input data is not found in italian data, a row of NaNs is returned, *this behaviour may change in the future.*

        :param return_cols: used to subset the returned data in order to provide the requested fields. If None, all available fields are returned. If is an instance of re.Pattern or is a string and regex param is True columns will be filtered and returned only if their names match the regular expression. The available fields are listed above, defaults to None.
        :type return_cols: list[str] | None, optional.
        :param regex: if True, return_cols is interpreted as a regex pattern, defaults to False.
        :type regex: bool, optional.
        :param population_limits: see above, can be a list of int or ``'total'`` or ``'auto'``, defaults to 'auto'.
        :type population_limits: list[int] | str, optional.
        :param population_labels: a list of strings that defines labels name, if None the :ref:`default label naming rule<default-label-naming-rule>` will be used, defaults to None.
        :type population_labels: list[str] | None, optional.

        :raises KeyError: if return_cols is or contains a column not listed above or includes ``geometry`` and accessor was intialize without geometry data.

        :return: Requested data in a 2-dimensional dataframe that has the same index of input data.
        :rtype: pandas.DataFrame
        """
        str_indexed, code_indexed, cadastral_indexed = self._generate_municipality_dfs(
            population_limits=population_limits,
            population_labels=population_labels,
            include_geometry=self.include_geometry,
        )
        empty_serie = self._generate_empty_serie(str_indexed.columns.to_list())
        str_indexed = dict(str_indexed.iterrows())
        code_indexed = dict(code_indexed.iterrows())
        cadastral_indexed = dict(cadastral_indexed.iterrows())

        @cache
        def get_data(x) -> pd.Series:
            x = str(x).strip().lower()
            try:
                x = int(float(x))
                return code_indexed.get(x, empty_serie)
            except Exception:
                if re.fullmatch("[a-z][0-9]{3}", x):
                    return cadastral_indexed.get(x, empty_serie)
                else:
                    return str_indexed.get(x, empty_serie)

        return handle_return_cols(self._obj.apply(get_data), return_cols, regex)

    def _generate_province_dfs(
        self,
        population_limits: list | str = "auto",
        population_labels: list | None = None,
        include_geometry: bool = False,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        temp_df = self.geopop.compose_df(
            level="province",
            population_limits=population_limits,
            population_labels=population_labels,
            include_geometry=include_geometry,
        )
        temp_df["_index"] = temp_df.province.str.lower()
        str_indexed = temp_df.set_index("_index")
        temp_df["_index"] = temp_df.province_code
        code_indexed = temp_df.set_index("_index")
        temp_df["_index"] = temp_df.province_short.str.upper()
        short_str_indexed = temp_df.set_index("_index")
        return str_indexed, code_indexed, short_str_indexed

    def from_province(
        self,
        return_cols: list | str | re.Pattern | None = None,
        regex: bool = False,
        population_limits: list | str = "auto",
        population_labels: list | None = None,
    ) -> pd.DataFrame:
        """Get data for provinces.
        Input series can contain provinces names, provinces abbreviations or provinces istat codes; *data types can also be mixed*.
        If input data is not found in italian data, a row of NaNs is returned, *this behaviour may change in the future.*

        :param return_cols: used to subset the returned data in order to provide the requested fields. If None, all available fields are returned. If is an instance of re.Pattern or is a string and regex param is True columns will be filtered and returned only if their names match the regular expression. The available fields are listed above, defaults to None.
        :type return_cols: list[str] | None, optional.
        :param regex: if True, return_cols is interpreted as a regex pattern, defaults to False.
        :type regex: bool, optional.
        :param population_limits: see above, can be a list of int or ``'total'`` or ``'auto'``, defaults to 'auto'.
        :type population_limits: list[int] | str, optional.
        :param population_labels: a list of strings that defines labels name, if None the :ref:`default label naming rule<default-label-naming-rule>` will be used, defaults to None.
        :type population_labels: list[str] | None, optional.

        .. note::
            To understand how ``municipalities`` are grouped, see above :ref:`Municipality data <municipality-data>`.

        :raises KeyError: if return_cols is or contains a column not listed above or includes ``geometry`` and accessor was intialize without geometry data.

        :return: Requested data in a 2-dimensional dataframe that has the same index of input data.
        :rtype: pandas.DataFrame
        """
        str_indexed, code_indexed, short_str_indexed = self._generate_province_dfs(
            population_limits=population_limits,
            population_labels=population_labels,
            include_geometry=self.include_geometry,
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

        return handle_return_cols(self._obj.apply(get_data), return_cols, regex)

    def _generate_region_dfs(
        self,
        population_limits: list | str = "auto",
        population_labels: list | None = None,
        include_geometry: bool = False,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        temp_df = self.geopop.compose_df(
            level="region",
            population_limits=population_limits,
            population_labels=population_labels,
            include_geometry=include_geometry,
        )
        temp_df["_index"] = temp_df.region.str.lower()
        str_indexed = temp_df.set_index("_index")
        temp_df["_index"] = temp_df.region_code
        code_indexed = temp_df.set_index("_index")
        return str_indexed, code_indexed

    def from_region(
        self,
        return_cols: list | str | re.Pattern | None = None,
        regex: bool = False,
        population_limits: list | str = "auto",
        population_labels: list | None = None,
    ) -> pd.DataFrame:
        """Get data for regions.
        Input series can contain regions names or regions istat codes; *data types can also be mixed*.
        If input data is not found in italian data, a row of NaNs is returned, *this behaviour may change in the future.*

        :param return_cols: used to subset the returned data in order to provide the requested fields. If None, all available fields are returned. If is an instance of re.Pattern or is a string and regex param is True columns will be filtered and returned only if their names match the regular expression. The available fields are listed above, defaults to None.
        :type return_cols: list[str] | None, optional.
        :param regex: if True, return_cols is interpreted as a regex pattern, defaults to False.
        :type regex: bool, optional.
        :param population_limits: see above, can be a list of int or ``'total'`` or ``'auto'``, defaults to 'auto'.
        :type population_limits: list[int] | str, optional.
        :param population_labels: a list of strings that defines labels name, if None the :ref:`default label naming rule<default-label-naming-rule>` will be used, defaults to None.
        :type population_labels: list[str] | None, optional.

        .. note::
            To understand how ``provinces`` are grouped, see above :ref:`Province data <province-data>`.

        :raises KeyError: if return_cols is or contains a column not listed above or includes ``geometry`` and accessor was intialize without geometry data.

        :return: Requested data in a 2-dimensional dataframe that has the same index of input data.
        :rtype: pandas.DataFrame
        """
        str_indexed, code_indexed = self._generate_region_dfs(
            population_limits=population_limits,
            population_labels=population_labels,
            include_geometry=self.include_geometry,
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

        return handle_return_cols(self._obj.apply(get_data), return_cols, regex)

    def smart_from_municipality(
        self,
        return_cols: list | str | re.Pattern | None = None,
        regex: bool = False,
        population_limits: list | str = "auto",
        population_labels: list | None = None,
    ) -> pd.DataFrame | pd.Series:
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
            population_limits=population_limits,
            population_labels=population_labels,
            include_geometry=self.include_geometry,
        )[0]
        ret = self.from_municipality(
            population_limits=population_limits,
            population_labels=population_labels,
        )
        nans = self._obj[ret[ret.municipality.isnull()].index].copy()

        empty_serie = self._generate_empty_serie(str_indexed.columns.to_list())
        str_indexed = dict(str_indexed.iterrows())

        @cache
        def get_data(x):
            key = match_single_key(str_indexed.keys(), str(x).strip().lower())
            return str_indexed.get(key, empty_serie)

        ret = ret.fillna(nans.apply(get_data))

        return handle_return_cols(ret, return_cols, regex)

    def smart_from_province(
        self,
        return_cols: list | str | re.Pattern | None = None,
        regex: bool = False,
        population_limits: list | str = "auto",
        population_labels: list | None = None,
    ) -> pd.DataFrame | pd.Series:
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
            population_limits=population_limits,
            population_labels=population_labels,
            include_geometry=self.include_geometry,
        )[0]
        ret = self.from_province(
            population_limits=population_limits,
            population_labels=population_labels,
        )
        nans = self._obj[ret[ret.region.isnull()].index].copy()

        empty_serie = self._generate_empty_serie(str_indexed.columns.to_list())
        str_indexed = dict(str_indexed.iterrows())

        @cache
        def get_data(x):
            key = match_single_key(str_indexed.keys(), str(x).strip().lower())
            return str_indexed.get(key, empty_serie)

        ret = ret.fillna(nans.apply(get_data))

        return handle_return_cols(ret, return_cols, regex)

    def smart_from_region(
        self,
        return_cols: list | str | re.Pattern | None = None,
        regex: bool = False,
        population_limits: list | str = "auto",
        population_labels: list | None = None,
    ) -> pd.DataFrame | pd.Series:
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
            population_limits=population_limits,
            population_labels=population_labels,
            include_geometry=self.include_geometry,
        )[0]
        ret = self.from_region(
            population_limits=population_limits,
            population_labels=population_labels,
        )
        nans = self._obj[ret[ret.region.isnull()].index].copy()

        empty_serie = self._generate_empty_serie(str_indexed.columns.to_list())
        str_indexed = dict(str_indexed.iterrows())

        @cache
        def get_data(x):
            key = match_single_key(str_indexed.keys(), str(x).strip().lower())
            return str_indexed.get(key, empty_serie)

        ret = ret.fillna(nans.apply(get_data))

        return handle_return_cols(ret, return_cols, regex)


def pandas_activate(include_geometry=False, data_year: Optional[int] = None):
    """Activate pandas extension registering class :py:class:ItalyGeopop as pandas.Series `accessor <https://pandas.pydata.org/docs/development/extending.html>`_ named ``italy_geopop``.

    :param include_geometry: specifies if geometry column should also be returned when accessor is used, defaults to False.
    :type include_geometry: bool, optional.
    :param data_year: year of data to use, if None the latest available data will be used, defaults to None.
    :type data_year: int, optional.

    :return: None

    .. warning::
        ``include_geometry=True`` comports costs in term of speed as geospatial datasets need to be loaded.
    """

    @pd.api.extensions.register_series_accessor("italy_geopop")
    class Accessor(ItalyGeopop):
        def __init__(self, pandas_obj) -> None:
            super().__init__(
                pandas_obj, include_geometry=include_geometry, data_year=data_year
            )


@contextmanager
def pandas_activate_context(include_geometry=False, data_year: Optional[int] = None):
    """
    Same as activate but lives within the context. Useful if you want to register the accessor with different
    initialization options more than once in your code or if you want to free up memory right after you get the needed data
    (the trade off is that italy-geopop needs to be reinitialized everytime you register and use the accessor).

    :param include_geometry: same as `italy_geopop.activate <#italy_geopop.pandas_extension.pandas_activate>`_.
    :param data_year: same as `italy_geopop.activate <#italy_geopop.pandas_extension.pandas_activate>`_.

    :yields: Context with ``italy_geopop`` accessor registered to pd.Series.
    .. code-block:: python

       # pandas_activate_context example

       with pandas_activate_context():
           # You can access italy_geopop here

       # You cannot access italy_geopop here
    """
    try:
        pandas_activate(include_geometry=include_geometry, data_year=data_year)
        yield
    except Exception as e:
        raise e
    finally:
        try:
            del pd.Series.italy_geopop
        except AttributeError:
            pass
