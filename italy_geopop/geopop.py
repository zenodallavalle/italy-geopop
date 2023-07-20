import geopandas as gpd
import numpy as np
import pandas as pd
import os
from typing import Optional
from warnings import warn

from ._utils import (
    get_available_years,
    get_latest_available_year,
    cache,
    generate_labels_for_age_cutoffs,
    aggregate_province_pop,
    aggregate_region_pop,
    prepare_limits,
)

_current_abs_dir = os.path.dirname(os.path.realpath(__file__))
_data_abs_dir = os.path.join(_current_abs_dir, "data")

_default_age_cutoffs = [0, 3, 11, 19, 25, 50, 65, 75, 120]


class Geopop:
    """A class that contains italian geospatial and population data.

    :param data_year: the year of the data you need; if None the latests is automatically picked, defaults to None
    :type data_year: int, optional

    :raises ValueError: if ``data_year`` is not available
    """

    def __init__(self, data_year: Optional[int] = None):
        available_years = get_available_years(_data_abs_dir)
        if data_year is None:
            data_year = get_latest_available_year(_data_abs_dir)
            warn(f"No data_year specified, using latest available ({data_year}).")
        elif data_year not in available_years:
            raise ValueError(
                "data_year must be one of the available years ({}).".format(
                    ", ".join(map(str, available_years))
                )
            )
        self.data_year = data_year

    @property
    def italy_municipalities(self) -> pd.DataFrame:
        """Property to get italian municipalities data.

        :return: a 2-dimensional dataframe with ``municipality_code`` as index and ``municipality``, ``province_code``, ``province``, ``province_short``, ``region``, ``region_code`` as columns.
        :rtype: pd.DataFrame
        """

        if not hasattr(self, "_italy_municipalities"):
            setattr(
                self,
                "_italy_municipalities",
                pd.read_feather(
                    os.path.join(
                        _data_abs_dir,
                        f"{self.data_year}_italy_municipalities.feather",
                    ),
                ).set_index("municipality_code"),
            )
        return self._italy_municipalities

    @property
    def italy_provinces(self) -> pd.DataFrame:
        """Property to get italian provinces data.

        .. note::
            To understand how ``municipalities`` are grouped, see above :ref:`Municipality data <municipality-data>`.

        :return: a 2-dimensional dataframe with ``province_code`` as index and ``province``, ``province_short``, ``municipalities``, ``region``, ``region_code`` as columns.
        :rtype: pd.DataFrame
        """
        if not hasattr(self, "_italy_provinces"):
            setattr(
                self,
                "_italy_provinces",
                pd.read_feather(
                    os.path.join(
                        _data_abs_dir, f"{self.data_year}_italy_provinces.feather"
                    ),
                ).set_index("province_code"),
            )
        return self._italy_provinces

    @property
    def italy_regions(self) -> pd.DataFrame:
        """Property to get italian regions data.

        .. note::
            To understand how ``provinces`` are grouped, see above :ref:`Province data <province-data>`.

        :return: a 2-dimensional dataframe with ``region_code`` as index and ``region``, ``provinces`` as column.
        :rtype: pd.DataFrame
        """

        if not hasattr(self, "_italy_regions"):
            setattr(
                self,
                "_italy_regions",
                pd.read_feather(
                    os.path.join(
                        _data_abs_dir, f"{self.data_year}_italy_regions.feather"
                    ),
                ).set_index("region_code"),
            )
        return self._italy_regions

    @property
    def italy_municipalities_geometry(self) -> pd.DataFrame:
        """Property to get geospatial data for plotting municipalities.

        :return: a 2-dimensional dataframe with ``municipality_code`` as index and ``geometry`` as column.
        :rtype: pd.DataFrame
        """
        if not hasattr(self, "_italy_municipalities_geometry"):
            setattr(
                self,
                "_italy_municipalities_geometry",
                gpd.read_feather(
                    os.path.join(
                        _data_abs_dir,
                        f"{self.data_year}_italy_geo_municipalities.feather",
                    )
                ).set_index("municipality_code"),
            )
        return self._italy_municipalities_geometry

    @property
    def italy_provinces_geometry(self) -> pd.DataFrame:
        """Method to get geospatial data for plotting provinces.

        :return: a 2-dimensional dataframe with ``province_code`` as index and ``geometry`` as column.
        :rtype: pd.DataFrame
        """
        if not hasattr(self, "_italy_provinces_geometry"):
            setattr(
                self,
                "_italy_provinces_geometry",
                gpd.read_feather(
                    os.path.join(
                        _data_abs_dir, f"{self.data_year}_italy_geo_provinces.feather"
                    )
                ).set_index("province_code"),
            )
        return self._italy_provinces_geometry

    @property
    def italy_regions_geometry(self) -> pd.DataFrame:
        """Method to get geospatial data for plotting regions.

        :return: a 2-dimensional dataframe with ``region_code`` as index and ``geometry`` as column.
        :rtype: pd.DataFrame
        """
        if not hasattr(self, "_italy_regions_geometry"):
            setattr(
                self,
                "_italy_regions_geometry",
                gpd.read_feather(
                    os.path.join(
                        _data_abs_dir, f"{self.data_year}_italy_geo_regions.feather"
                    )
                ).set_index("region_code"),
            )
        return self._italy_regions_geometry

    @property
    def population_df(self) -> pd.DataFrame:
        """Method to get italian population data.

        :return: a 2-dimensional dataframe with ``municipality_code`` as index and and many columns with population data in `long` format (columns: ``age``, ``F``, ``M`` and ``tot``).
        :rtype: pd.DataFrame
        """

        if not hasattr(self, "_population_df"):
            setattr(
                self,
                "_population_df",
                pd.read_feather(
                    os.path.join(_data_abs_dir, f"{self.data_year}_italy_pop.feather"),
                ).set_index("municipality_code"),
            )
        return self._population_df

    @cache
    def get_italian_population_for_municipalites(
        self,
        population_limits: str | list = "auto",
        population_labels: list | None = None,
    ) -> pd.DataFrame:
        """Method to get italian population data for municipalities.

        :param population_limits: a list of int or ``'total'`` or ``'auto'``, defaults to 'auto'.
        :type population_limits: str | list, optional
        :param population_labels: a list of strings that defines labels name, defaults to None.
        :type population_labels: list[str] | None, optional

        :raises: ValueError if ``population_limits`` is not a list of int or a string in ``['total', 'auto']``.

        :return: a 2-dimensional dataframe with ``municipality_code`` as index and many columns according to ``population_limits`` and ``population_labels``, see above for more informations.
        :rtype: pd.DataFrame
        """

        if isinstance(population_limits, str):
            population_limits = population_limits.lower().strip()
            if population_limits == "total":
                pop_df = self.population_df.copy()
                ret = pop_df.groupby("municipality_code")[["F", "M", "tot"]].sum()
                ret["age_group"] = "population"
                ret = ret[["age_group", "F", "M", "tot"]]
            elif population_limits == "auto":
                pop_df = self.population_df.copy()
                slices = _default_age_cutoffs
                slices_labels = generate_labels_for_age_cutoffs(slices)
                pop_df["age_group"] = pd.cut(
                    pop_df.age,
                    bins=slices,
                    labels=slices_labels,
                    right=False,
                )
                ret = (
                    pop_df.groupby(["municipality_code", "age_group"])[
                        ["F", "M", "tot"]
                    ]
                    .sum()
                    .reset_index()
                    .set_index("municipality_code")
                )
            else:
                raise ValueError(
                    'population_limits must be a list of int that divides age groups or "auto" or "total" not "{}"'.format(
                        population_limits
                    )
                )
        else:
            slices = prepare_limits(population_limits)
            slices_labels = population_labels or generate_labels_for_age_cutoffs(slices)
            pop_df = self.population_df.copy()
            pop_df["age_group"] = pd.cut(
                pop_df.age, bins=slices, labels=slices_labels, right=False
            )
            ret = (
                pop_df.groupby(["municipality_code", "age_group"])[["F", "M", "tot"]]
                .sum()
                .reset_index()
                .set_index("municipality_code")
            )

        ret = ret.pivot(columns="age_group", values=["F", "M", "tot"])
        ret.columns = ret.columns.map(
            lambda x: f"{x[1]}_{x[0]}" if x[0] != "tot" else x[1]
        )
        return ret

    @cache
    def get_italian_population_for_provinces(
        self,
        population_limits: str | list = "auto",
        population_labels: list | None = None,
    ) -> pd.DataFrame:
        """Method to get italian population data for provinces.

        :param population_limits: a list of int or ``'total'`` or ``'auto'``, defaults to 'auto'.
        :type population_limits: str | list, optional
        :param population_labels: a list of strings that defines labels name, defaults to None.
        :type population_labels: list[str] | None, optional

        :raises: ValueError if ``population_limits`` is not a list of int or a string in ``['total', 'auto']``.

        :return: a 2-dimensional dataframe with ``province_code`` as index and many columns according to ``population_limits`` and ``population_labels``, see above for more informations.
        :rtype: pd.DataFrame
        """
        pop_df = self.get_italian_population_for_municipalites(
            population_limits, population_labels
        )
        geo_df = self.italy_municipalities
        return aggregate_province_pop(pop_df, geo_df)

    @cache
    def get_italian_population_for_regions(
        self,
        population_limits: str | list = "auto",
        population_labels: list | None = None,
    ) -> pd.DataFrame:
        """Method to get italian population data for regions.

        :param population_limits: a list of int or ``'total'`` or ``'auto'``, defaults to 'auto'.
        :type population_limits: str | list, optional
        :param population_labels: a list of strings that defines labels name, defaults to None.
        :type population_labels: list[str] | None, optional

        :raises: ValueError if ``population_limits`` is not a list of int or a string in ``['total', 'auto']``.

        :return: a 2-dimensional dataframe with ``region_code`` as index and many columns according to ``population_limits`` and ``population_labels``, see above for more informations.
        :rtype: pd.DataFrame
        """
        pop_df = self.get_italian_population_for_municipalites(
            population_limits, population_labels
        )
        geo_df = self.italy_municipalities
        return aggregate_region_pop(pop_df, geo_df)

    def compose_df(
        self,
        level="municipality",
        include_geometry=False,
        population_limits: str | list = "auto",
        population_labels: list | None = None,
    ):
        """Method to get a dataframe with administrative, geospatial and population data.

        :param level: the level of details of the dataframe that can be ``muncipality`` or ``province`` or ``region``, defaults to 'muncipality'.
        :type level: str, optional
        :param include_geometry: if True the dataframe will include geospatial data, defaults to False.
        :type include_geometry: bool, optional
        :param population_limits: a list of int or ``'total'`` or ``'auto'``, defaults to 'auto'.
        :type population_limits: str | list, optional
        :param population_labels: a list of str that defines labels name, defaults to None.
        :type population_labels: list | None, optional

        """
        level = level.lower().strip()
        if level == "municipality":
            if include_geometry:
                geo_df = self.italy_municipalities_geometry
            pop_df = self.get_italian_population_for_municipalites(
                population_limits=population_limits, population_labels=population_labels
            )
            mun_df = self.italy_municipalities
            if include_geometry:
                ret = pd.merge(
                    mun_df, geo_df, how="left", left_index=True, right_index=True
                )
                ret = pd.merge(
                    ret, pop_df, how="left", left_index=True, right_index=True
                )
            else:
                ret = pd.merge(
                    mun_df, pop_df, how="left", left_index=True, right_index=True
                )
            return ret.reset_index()
        elif level == "province":
            if include_geometry:
                geo_df = self.italy_provinces_geometry
            pop_df = self.get_italian_population_for_provinces(
                population_limits=population_limits, population_labels=population_labels
            )
            pro_df = self.italy_provinces
            if include_geometry:
                ret = pd.merge(
                    pro_df, geo_df, how="left", left_index=True, right_index=True
                )
                ret = pd.merge(
                    ret, pop_df, how="left", left_index=True, right_index=True
                )
            else:
                ret = pd.merge(
                    pro_df, pop_df, how="left", left_index=True, right_index=True
                )
            return ret.reset_index()
        elif level == "region":
            if include_geometry:
                geo_df = self.italy_regions_geometry
            pop_df = self.get_italian_population_for_regions(
                population_limits=population_limits, population_labels=population_labels
            )
            reg_df = self.italy_regions
            if include_geometry:
                ret = pd.merge(
                    reg_df, geo_df, how="left", left_index=True, right_index=True
                )
                ret = pd.merge(
                    ret, pop_df, how="left", left_index=True, right_index=True
                )
            else:
                ret = pd.merge(
                    reg_df, pop_df, how="left", left_index=True, right_index=True
                )
            return ret.reset_index()
        else:
            raise ValueError(
                f'level must be "municipality", "province" or "region" not "{level}"'
            )
