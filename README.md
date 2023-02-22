# 🗺️ 🇮🇹 Italy-geopop

<style>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
    .dataframe tbody tr th {
        vertical-align: top;
    }
    .dataframe thead th {
        text-align: center;
    }
</style>

- [🗺️ 🇮🇹 Italy-geopop](#️--italy-geopop)
  - [🧐 What is](#-what-is)
  - [🚀 Main features](#-main-features)
  - [🏪 Where to get it](#-where-to-get-it)
  - [🔌 Example of use](#-example-of-use)
  - [📖 License](#-license)
  - [🔎 Full docs reference](#-full-docs-reference)
  - [👩‍💻 Contributes](#-contributes)
  - [🐛 Bugs and issues](#-bugs-and-issues)

## 🧐 What is

**Italy-geopop** is a python library that provides instant access to **italian geographic and demographic data**.

## 🚀 Main features

- Easy access to italian geographic and demographic data
- Easy geographic plot made possible by the usage of [geopandas](https://geopandas.org/en/stable/)
- Easy linkage of italy-geopop data with your data made possible by the use of [pandas](https://pandas.pydata.org/) and the registration of italy-geopop as [pandas accessor](https://pandas.pydata.org/docs/development/extending.html), so you can map directly your data and link with italy-geopop data

You only need a list of [municipalities](https://en.wikipedia.org/wiki/List_of_municipalities_of_Italy) (or municipality ISTAT codes), [provinces](https://en.wikipedia.org/wiki/Provinces_of_Italy) (or province ISTAT codes or province abbreviations (e.g. `Torino` -> `TO`)) and [regions](https://en.wikipedia.org/wiki/Regions_of_Italy) (or region ISTAT codes).
ISTAT codes can be found [here](https://it.wikipedia.org/wiki/Codice_ISTAT) or [here](https://dait.interno.gov.it/territorio-e-autonomie-locali/sut/elenco_codici_comuni.php).

## 🏪 Where to get it

**PyPi**

`pip install italy-geopop`, as simple as that.

**GitHub**

`pip install https://github.com/zenodallavalle/italy-geopop.git`

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

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>municipality</th>
      <th>municipality_code</th>
      <th>province_code</th>
      <th>province</th>
      <th>province_short</th>
      <th>region</th>
      <th>region_code</th>
      <th>population</th>
      <th>population_F</th>
      <th>population_M</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Torino</td>
      <td>1272</td>
      <td>1</td>
      <td>Torino</td>
      <td>TO</td>
      <td>Piemonte</td>
      <td>1</td>
      <td>848748.0</td>
      <td>441686.0</td>
      <td>407062.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Agliè</td>
      <td>1001</td>
      <td>1</td>
      <td>Torino</td>
      <td>TO</td>
      <td>Piemonte</td>
      <td>1</td>
      <td>2562.0</td>
      <td>1347.0</td>
      <td>1215.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Airasca</td>
      <td>1002</td>
      <td>1</td>
      <td>Torino</td>
      <td>TO</td>
      <td>Piemonte</td>
      <td>1</td>
      <td>3660.0</td>
      <td>1793.0</td>
      <td>1867.0</td>
    </tr>
  </tbody>
</table>
</div>

```
>>> pd.Series(["Torino", "Milano", "Venezia"]).italy_geopop.from_province()
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>province_code</th>
      <th>province</th>
      <th>province_short</th>
      <th>municipalities</th>
      <th>region</th>
      <th>region_code</th>
      <th>population</th>
      <th>population_F</th>
      <th>population_M</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Torino</td>
      <td>TO</td>
      <td>[{'municipality_code': 1001, 'municipality': '...</td>
      <td>Piemonte</td>
      <td>1</td>
      <td>2208370.0</td>
      <td>1137159.0</td>
      <td>1071211.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>15</td>
      <td>Milano</td>
      <td>MI</td>
      <td>[{'municipality_code': 15002, 'municipality': ...</td>
      <td>Lombardia</td>
      <td>3</td>
      <td>3214630.0</td>
      <td>1650192.0</td>
      <td>1564438.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>27</td>
      <td>Venezia</td>
      <td>VE</td>
      <td>[{'municipality_code': 27001, 'municipality': ...</td>
      <td>Veneto</td>
      <td>5</td>
      <td>836916.0</td>
      <td>429501.0</td>
      <td>407415.0</td>
    </tr>
  </tbody>
</table>
</div>

```
>>> pd.Series(["Piemonte", "Lombardia", "Veneto"]).italy_geopop.from_region()
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>region</th>
      <th>region_code</th>
      <th>provinces</th>
      <th>population</th>
      <th>population_F</th>
      <th>population_M</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Piemonte</td>
      <td>1</td>
      <td>[{'province_code': 1, 'province': 'Torino', 'p...</td>
      <td>4256350.0</td>
      <td>2182505.0</td>
      <td>2073845.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Lombardia</td>
      <td>3</td>
      <td>[{'province_code': 12, 'province': 'Varese', '...</td>
      <td>9943004.0</td>
      <td>5061476.0</td>
      <td>4881528.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Veneto</td>
      <td>5</td>
      <td>[{'province_code': 23, 'province': 'Verona', '...</td>
      <td>4847745.0</td>
      <td>2467002.0</td>
      <td>2380743.0</td>
    </tr>
  </tbody>
</table>
</div>

## 📖 License

Italy-geopop is distributed under Creative Commons license ([CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)). Full license can be read at [LICENSE](https://github.com/zenodallavalle/italy-geopop/blob/main/LICENSE).

Italy-geopop includes data from:

- [openpolis/geojson-italy](https://github.com/openpolis/geojson-italy), at the dime of writing distributed under Creative Commons license (CC-BY-4.0)
- [ISTAT](https://www.istat.it/en/) data, at the time of writing distributed under Creative Commons license (CC-BY-3.0), more info [here](https://www.istat.it/en/legal-notice)

## 🔎 Full docs reference

🚧 Work in progress 🏗️

## 👩‍💻 Contributes

- [Zeno Dalla Valle](https://github.com/zenodallavalle/italy-geopop) - creator and mantainer

## 🐛 Bugs and issues

Please report bugs via GitHub issues [here](https://github.com/zenodallavalle/italy-geopop/issues) providing also a minimum reproducible example.
