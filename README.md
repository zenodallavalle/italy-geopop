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
- Population data available by age and sex with customable age ranges
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
>>> pd.Series(["Torino", "Agliè", "Airasca"]).italy_geopop.from_municipality(population_limits='total')
```

|     | municipality_code | municipality | province_code | province | province_short | region   | region_code | cadastral_code | geometry     | population_F | population_M | population |
| --- | ----------------- | ------------ | ------------- | -------- | -------------- | -------- | ----------- | -------------- | ------------ | ------------ | ------------ | ---------- |
| 0   | 1272              | Torino       | 1             | Torino   | TO             | Piemonte | 1           | L219           | MULTIPOLYGON | 441686.0     | 407062.0     | 848748.0   |
| 1   | 1001              | Agliè        | 1             | Torino   | TO             | Piemonte | 1           | A074           | MULTIPOLYGON | 1347.0       | 1215.0       | 2562.0     |
| 2   | 1002              | Airasca      | 1             | Torino   | TO             | Piemonte | 1           | A109           | MULTIPOLYGON | 1793.0       | 1867.0       | 3660.0     |

```
>>> pd.Series(["Torino", "Milano", "Venezia"]).italy_geopop.from_province(population_limits=[50], population_labels=['below_50', 'above_equal_50'])
```

|     | province_code | province | province_short | municipalities             | region    | region_code | geometry     | below_50_F | above_equal_50_F | below_50_M | above_equal_50_M | below_50  | above_equal_50 |
| --- | ------------- | -------- | -------------- | -------------------------- | --------- | ----------- | ------------ | ---------- | ---------------- | ---------- | ---------------- | --------- | -------------- |
| 0   | 1             | Torino   | TO             | [{'cadastral_code': 'A074' | Piemonte  | 1           | POLYGON      | 550793.0   | 586366.0         | 572143.0   | 499068.0         | 1122936.0 | 1085434.0      |
| 1   | 15            | Milano   | MI             | [{'cadastral_code': 'A010' | Lombardia | 3           | MULTIPOLYGON | 857481.0   | 792711.0         | 898004.0   | 666434.0         | 1755485.0 | 1459145.0      |
| 2   | 27            | Venezia  | VE             | [{'cadastral_code': 'A302' | Veneto    | 5           | POLYGON      | 205100.0   | 224401.0         | 214116.0   | 193299.0         | 419216.0  | 417700.0       |

```

> > > pd.Series(["Piemonte", "Lombardia", "Veneto"]).italy_geopop.from_region()

```

|     | region_code | region    | provinces                 | geometry     | <3_F     | 3-11_F   | 11-19_F  | 19-25_F  | 25-50_F   | 50-65_F   | 65-75_F  | >=75_F   | <3_M     | 3-11_M   | 11-19_M  | 19-25_M  | 25-50_M   | 50-65_M   | 65-75_M  | >=75_M   | <3       | 3-11     | 11-19    | 19-25    | 25-50     | 50-65     | 65-75     | >=75      |
| --- | ----------- | --------- | ------------------------- | ------------ | -------- | -------- | -------- | -------- | --------- | --------- | -------- | -------- | -------- | -------- | -------- | -------- | --------- | --------- | -------- | -------- | -------- | -------- | -------- | -------- | --------- | --------- | --------- | --------- |
| 0   | 1           | Piemonte  | [{'municipalities': array | POLYGON      | 40122.0  | 131269.0 | 149768.0 | 112474.0 | 614252.0  | 506764.0  | 279224.0 | 348632.0 | 42361.0  | 138788.0 | 159618.0 | 123911.0 | 629878.0  | 490464.0  | 251918.0 | 236907.0 | 82483.0  | 270057.0 | 309386.0 | 236385.0 | 1244130.0 | 997228.0  | 531142.0  | 585539.0  |
| 1   | 3           | Lombardia | [{'municipalities': array | MULTIPOLYGON | 103867.0 | 336353.0 | 378153.0 | 274455.0 | 1520576.0 | 1144338.0 | 586818.0 | 716916.0 | 109087.0 | 356547.0 | 403719.0 | 303888.0 | 1572013.0 | 1135834.0 | 524720.0 | 475720.0 | 212954.0 | 692900.0 | 781872.0 | 578343.0 | 3092589.0 | 2280172.0 | 1111538.0 | 1192636.0 |
| 2   | 5           | Veneto    | [{'municipalities': array | POLYGON      | 48285.0  | 157284.0 | 182441.0 | 136850.0 | 718105.0  | 578543.0  | 291166.0 | 354328.0 | 51390.0  | 166176.0 | 194064.0 | 149055.0 | 737009.0  | 573454.0  | 267403.0 | 242192.0 | 99675.0  | 323460.0 | 376505.0 | 285905.0 | 1455114.0 | 1151997.0 | 558569.0  | 596520.0  |

```

> > > pd.Series(["Regione Lombardia", "Regione del Veneto", "Veneto o Lombardia", 15]).italy_geopop.smart_from_region()

```

|     | region_code | region    | provinces                 | geometry     | <3_F     | 3-11_F   | 11-19_F  | 19-25_F  | 25-50_F   | 50-65_F   | 65-75_F  | >=75_F   | <3_M     | 3-11_M   | 11-19_M  | 19-25_M  | 25-50_M   | 50-65_M   | 65-75_M  | >=75_M   | <3       | 3-11     | 11-19    | 19-25    | 25-50     | 50-65     | 65-75     | >=75      |
| --- | ----------- | --------- | ------------------------- | ------------ | -------- | -------- | -------- | -------- | --------- | --------- | -------- | -------- | -------- | -------- | -------- | -------- | --------- | --------- | -------- | -------- | -------- | -------- | -------- | -------- | --------- | --------- | --------- | --------- |
| 0   | 3.0         | Lombardia | [{'municipalities': array | MULTIPOLYGON | 103867.0 | 336353.0 | 378153.0 | 274455.0 | 1520576.0 | 1144338.0 | 586818.0 | 716916.0 | 109087.0 | 356547.0 | 403719.0 | 303888.0 | 1572013.0 | 1135834.0 | 524720.0 | 475720.0 | 212954.0 | 692900.0 | 781872.0 | 578343.0 | 3092589.0 | 2280172.0 | 1111538.0 | 1192636.0 |
| 1   | 5.0         | Veneto    | [{'municipalities': array | POLYGON      | 48285.0  | 157284.0 | 182441.0 | 136850.0 | 718105.0  | 578543.0  | 291166.0 | 354328.0 | 51390.0  | 166176.0 | 194064.0 | 149055.0 | 737009.0  | 573454.0  | 267403.0 | 242192.0 | 99675.0  | 323460.0 | 376505.0 | 285905.0 | 1455114.0 | 1151997.0 | 558569.0  | 596520.0  |
| 2   | nan         | nan       | nan                       | nan          | nan      | nan      | nan      | nan      | nan       | nan       | nan      | nan      | nan      | nan      | nan      | nan      | nan       | nan       | nan      | nan      | nan      | nan      | nan      | nan      | nan       | nan       | nan       | nan       |
| 3   | 15.0        | Campania  | [{'municipalities': array | MULTIPOLYGON | 65798.0  | 201345.0 | 239653.0 | 185798.0 | 909861.0  | 641838.0  | 320637.0 | 311913.0 | 69298.0  | 213525.0 | 253444.0 | 200452.0 | 907541.0  | 602405.0  | 288497.0 | 212415.0 | 135096.0 | 414870.0 | 493097.0 | 386250.0 | 1817402.0 | 1244243.0 | 609134.0  | 524328.0  |

## 📖 License

Italy-geopop is distributed under Creative Commons license ([CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)). Full license can be read at [LICENSE](https://github.com/zenodallavalle/italy-geopop/blob/main/LICENSE).

Italy-geopop includes data from:

- [openpolis/geojson-italy](https://github.com/openpolis/geojson-italy), at the dime of writing distributed under Creative Commons license (CC-BY-4.0)
- [ISTAT](https://www.istat.it/en/) data, at the time of writing distributed under Creative Commons license (CC-BY-3.0), more info [here](https://www.istat.it/en/legal-notice)

## 🔎 Full docs reference

You can find full docs on [italy-geopop.readthedocs.io](https://italy-geopop.readthedocs.io/).

## 👩‍💻 Contributes

- [Zeno Dalla Valle](https://github.com/zenodallavalle/italy-geopop) - creator and mantainer

## 🐛 Bugs and issues

If you experience an issue using this library first check the FAQ, you may find an immediate solution to your problem.

If your problem is not listed or the proposed solution did not worked for you, please report bugs via GitHub issues [here](https://github.com/zenodallavalle/italy-geopop/issues) providing also a minimum reproducible example.
