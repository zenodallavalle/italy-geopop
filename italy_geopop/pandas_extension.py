from contextlib import contextmanager
import numpy as np
import pandas as pd
from warnings import warn

from ._decorators import cache, handle_return_cols
from italy_geopop import geopop


def pandas_activate(include_geometry=False):
    """Activate pandas extension registering italy_geopop as pandas.Series `accessor <https://pandas.pydata.org/docs/development/extending.html>`_.

    :param include_geometry: specifies if geometry column should also be returned when accessor is used, defaults to False
    :type include_geometry: bool, optional

    :return: None

    .. warning::
        ``include_geometry=True`` comports costs in term of speed as geographic datasets need to be loaded.

    .. example:.
        .. code-block:: python
        :linenos:
            from italy_geopop.pandas_extension import pandas_activate
            pandas_activate(include_geometry=False)
            data = pd.Series(["Torino", "Agliè", "Airasca"])
            data.italy_geopop.from_municipality()
    """
    italy_geopop_df = geopop.ItalyGeopopDataFrame()

    @pd.api.extensions.register_series_accessor('italy_geopop')
    class GeopopPandas:
        def __init__(self, pandas_obj) -> None:
            self._obj = pandas_obj

        @classmethod
        def _generate_empty_serie(cls, df, index) -> pd.Series:
            columns = df.columns.tolist()
            data = [np.nan for _ in columns]
            return pd.Series(data, index=columns, name=index)

        @classmethod
        def _extract_serie(cls, df, index) -> pd.Series:
            try:
                ret = pd.Series(df.loc[index, :])
                return ret
            except ValueError:
                warn(f"Multiple values found for value '{index}'")
            except KeyError:
                pass
            ret = cls._generate_empty_serie(df, index)
            return ret

        @property
        def population_df(self) -> geopop.ItalyGeopopDataFrame:
            return italy_geopop_df

        @staticmethod
        @cache
        def _generate_municipality_dfs(
            include_geometry,
        ) -> tuple[pd.DataFrame, pd.DataFrame]:
            if not include_geometry:
                temp_df = italy_geopop_df.copy()
            else:
                temp_df = pd.merge(
                    italy_geopop_df.get_municipalities_geometry(),
                    italy_geopop_df,
                    how='right',
                    right_on='municipality_code',
                    left_index=True,
                )
            temp_df['_index'] = temp_df.municipality.str.lower()
            str_indexed = temp_df.set_index('_index')
            temp_df['_index'] = temp_df.municipality_code
            code_indexed = temp_df.set_index('_index')
            return str_indexed, code_indexed

        @handle_return_cols(include_geometry=include_geometry)
        def from_municipality(self) -> pd.DataFrame:
            str_indexed, code_indexed = self._generate_municipality_dfs(
                include_geometry=include_geometry
            )

            @cache
            def get_data(x) -> pd.Series:
                x = str(x).strip().lower()
                try:
                    x = int(float(x))
                    return self._extract_serie(code_indexed, x)
                except Exception:
                    return self._extract_serie(str_indexed, x)

            return self._obj.apply(get_data)

        @staticmethod
        @cache
        def _generate_province_dfs(
            include_geometry,
        ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
            if not include_geometry:
                temp_df = italy_geopop_df.aggregate_province()
            else:
                temp_df = pd.merge(
                    italy_geopop_df.get_provinces_geometry(),
                    italy_geopop_df.aggregate_province(),
                    how='right',
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

        @handle_return_cols(include_geometry=include_geometry)
        def from_province(self) -> pd.DataFrame:
            str_indexed, code_indexed, short_str_indexed = self._generate_province_dfs(
                include_geometry=include_geometry
            )

            @cache
            def get_data(x) -> pd.Series:
                x = str(x).strip()
                try:
                    x = int(float(x))
                    return self._extract_serie(code_indexed, x)
                except ValueError:
                    if len(x) == 2:
                        return self._extract_serie(short_str_indexed, x.upper())
                    else:
                        return self._extract_serie(str_indexed, x.lower())

            return self._obj.apply(get_data)

        @staticmethod
        @cache
        def _generate_region_dfs(include_geometry) -> tuple[pd.DataFrame, pd.DataFrame]:
            if not include_geometry:
                temp_df = italy_geopop_df.aggregate_region()
            else:
                temp_df = pd.merge(
                    italy_geopop_df.get_regions_geometry(),
                    italy_geopop_df.aggregate_region(),
                    how='right',
                    right_on='region_code',
                    left_index=True,
                )
            temp_df['_index'] = temp_df.region.str.lower()
            str_indexed = temp_df.set_index('_index')
            temp_df['_index'] = temp_df.region_code
            code_indexed = temp_df.set_index('_index')
            return str_indexed, code_indexed

        @handle_return_cols(include_geometry=include_geometry)
        def from_region(self) -> pd.DataFrame:
            str_indexed, code_indexed = self._generate_region_dfs(
                include_geometry=include_geometry
            )

            @cache
            def get_data(x) -> pd.Series:
                x = str(x).strip().lower()
                try:
                    x = int(float(x))
                    return self._extract_serie(code_indexed, x)
                except ValueError:
                    return self._extract_serie(str_indexed, x)

            return self._obj.apply(get_data)


@contextmanager
def pandas_activate_context(include_geometry=False):
    """
    Same as activate but lives within the context.

    :param include_geometry: same as `italy_geopop.activate <#italy_geopop.pandas_extension.pandas_activate>`_.
    :yields: Context with `italy_geopop` accessor registered to pd.Series.
    """
    try:
        pandas_activate(include_geometry=include_geometry)
        yield
    except:
        pass
    finally:
        try:
            del pd.Series.italy_geopop
        except AttributeError:
            pass
