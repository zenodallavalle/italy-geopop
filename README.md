# 🗺️ 🇮🇹 Italy-geopop

[![Documentation Status](https://readthedocs.org/projects/italy-geopop/badge/?version=latest)](https://italy-geopop.readthedocs.io/en/latest/?badge=latest)

- [🗺️ 🇮🇹 Italy-geopop](#️--italy-geopop)
  - [🧐 What is it?](#-what-is-it)
  - [🚀 Main features](#-main-features)
  - [🏪 Where to get it](#-where-to-get-it)
  - [🔌 Example of use](#-example-of-use)
  - [📖 License](#-license)
  - [🔎 Full docs reference](#-full-docs-reference)
  - [👩‍💻 Contributes](#-contributes)
  - [🐛 Bugs and issues](#-bugs-and-issues)

## 🧐 What is it?

**Italy-geopop** is a python library that provides instant access to **italian geospatial and population data**.

## 🚀 Main features

- Easy access to italian geospatial and population data
- Easy geospatial plot made possible by the usage of [geopandas](https://geopandas.org/en/stable/)
- Easy linkage of italy-geopop data with your data made possible by using [pandas](https://pandas.pydata.org/) and the registration of italy-geopop as [pandas accessor](https://pandas.pydata.org/docs/development/extending.html)

You only need a list of [municipalities](https://en.wikipedia.org/wiki/List_of_municipalities_of_Italy) (or municipality ISTAT codes), [provinces](https://en.wikipedia.org/wiki/Provinces_of_Italy) (or province ISTAT codes or province abbreviations (e.g. `Torino` -> `TO`)) and [regions](https://en.wikipedia.org/wiki/Regions_of_Italy) (or region ISTAT codes).
ISTAT codes can be found [here](https://it.wikipedia.org/wiki/Codice_ISTAT) or [here](https://dait.interno.gov.it/territorio-e-autonomie-locali/sut/elenco_codici_comuni.php).

## 🏪 Where to get it

**PyPi**

`pip install italy-geopop`, as simple as that.

**GitHub - specific version (e.g. 0.1.1)**

`pip install git+https://github.com/zenodallavalle/italy-geopop.git@v0.1.1`

**GitHub - latest (main branch)**

`pip install git+https://github.com/zenodallavalle/italy-geopop.git@main`

**GitHub - development branch**

`pip install git+https://github.com/zenodallavalle/italy-geopop.git@dev`

## 🔌 Example of use

```
>>> from italy_geopop.pandas_extension import pandas_activate
>>> pandas_activate(include_geometry=False)
```

```
>>> pd.Series(["Torino", "Agliè", "Airasca"]).italy_geopop.from_municipality()
```

|     | geometry     | municipality | municipality_code | province_code | province | province_short | region   | region_code | population | population_F | population_M |
| --- | ------------ | ------------ | ----------------- | ------------- | -------- | -------------- | -------- | ----------- | ---------- | ------------ | ------------ |
| 0   | MULTIPOLYGON | Torino       | 1272              | 1             | Torino   | TO             | Piemonte | 1           | 848748.0   | 441686.0     | 407062.0     |
| 1   | MULTIPOLYGON | Agliè        | 1001              | 1             | Torino   | TO             | Piemonte | 1           | 2562.0     | 1347.0       | 1215.0       |
| 2   | MULTIPOLYGON | Airasca      | 1002              | 1             | Torino   | TO             | Piemonte | 1           | 3660.0     | 1793.0       | 1867.0       |

```
>>> pd.Series(["Torino", "Milano", "Venezia"]).italy_geopop.from_province()
```

|     | geometry     | province_code | province | province_short | municipalities            | region    | region_code | population | population_F | population_M |
| --- | ------------ | ------------- | -------- | -------------- | ------------------------- | --------- | ----------- | ---------- | ------------ | ------------ |
| 0   | POLYGON      | 1             | Torino   | TO             | [{'municipality_code': 10 | Piemonte  | 1           | 2208370.0  | 1137159.0    | 1071211.0    |
| 1   | MULTIPOLYGON | 15            | Milano   | MI             | [{'municipality_code': 15 | Lombardia | 3           | 3214630.0  | 1650192.0    | 1564438.0    |
| 2   | POLYGON      | 27            | Venezia  | VE             | [{'municipality_code': 27 | Veneto    | 5           | 836916.0   | 429501.0     | 407415.0     |

```
>>> pd.Series(["Piemonte", "Lombardia", "Veneto"]).italy_geopop.from_region()
```

|     | geometry     | region    | region_code | provinces                 | population | population_F | population_M |
| --- | ------------ | --------- | ----------- | ------------------------- | ---------- | ------------ | ------------ |
| 0   | POLYGON      | Piemonte  | 1           | [{'province_code': 1, 'pr | 4256350.0  | 2182505.0    | 2073845.0    |
| 1   | MULTIPOLYGON | Lombardia | 3           | [{'province_code': 12, 'p | 9943004.0  | 5061476.0    | 4881528.0    |
| 2   | POLYGON      | Veneto    | 5           | [{'province_code': 23, 'p | 4847745.0  | 2467002.0    | 2380743.0    |

```
>>> pd.Series(["Regione Lombardia", "Regione del Veneto", "Veneto o Lombardia", 15]).italy_geopop.smart_from_region()
```

|     | geometry     | region    | region_code | provinces                 | population | population_F | population_M |
| --- | ------------ | --------- | ----------- | ------------------------- | ---------- | ------------ | ------------ |
| 0   | MULTIPOLYGON | Lombardia | 3.0         | [{'province_code': 12, 'p | 9943004.0  | 5061476.0    | 4881528.0    |
| 1   | POLYGON      | Veneto    | 5.0         | [{'province_code': 23, 'p | 4847745.0  | 2467002.0    | 2380743.0    |
| 2   | nan          | nan       | nan         | nan                       | nan        | nan          | nan          |
| 3   | MULTIPOLYGON | Campania  | 15.0        | [{'province_code': 61, 'p | 5624420.0  | 2876843.0    | 2747577.0    |

## 📖 License

Italy-geopop is distributed under Creative Commons license ([CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)). Full license can be read at [LICENSE](https://github.com/zenodallavalle/italy-geopop/blob/main/LICENSE).

Italy-geopop includes data from:

- [openpolis/geojson-italy](https://github.com/openpolis/geojson-italy), at the dime of writing distributed under Creative Commons license (CC-BY-4.0)
- [ISTAT](https://www.istat.it/en/) data, at the time of writing distributed under Creative Commons license (CC-BY-3.0), more info [here](https://www.istat.it/en/legal-notice)

## 🔎 Full docs reference

You can find full docs on [italy-geopop.readthedocs.io](https://italy-geopop.readthedocs.io/en/latest).

## 👩‍💻 Contributes

- [Zeno Dalla Valle](https://github.com/zenodallavalle/italy-geopop) - creator and mantainer

## 🐛 Bugs and issues

If you experience an issue using this library first check the FAQ, you may find an immediate solution to your problem.

If your problem is not listed or the proposed solution did not worked for you, please report bugs via GitHub issues [here](https://github.com/zenodallavalle/italy-geopop/issues) providing also a minimum reproducible example.
