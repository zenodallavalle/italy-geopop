🔌 Quick Usage
==================

.. note::
  Be sure to check out the :ref:`installation <installation>` section before.


First of all, activate the pandas extension

.. code-block:: python
  :linenos:

  from italy_geopop.pandas_extension import pandas_activate
  pandas_activate(include_geometry=True)



Municipalities
-----------------

Then you can use italy-geopop to get data for your `pd.Series <https://pandas.pydata.org/docs/reference/api/pandas.Series.html>`_ municipalities.

.. code-block:: python
  :lineno-start: 3

  data = pd.Series(["Torino", "Agliè", "Airasca"])
  data.italy_geopop.from_municipality()


.. csv-table::
  :file: _static/assets/quick_usage_01.csv
  :header-rows: 1

Provinces
-------------

You can also use italy-geopop to get data for your `pd.Series <https://pandas.pydata.org/docs/reference/api/pandas.Series.html>`_ provinces.

.. code-block:: python
  :lineno-start: 5

  data = pd.Series(["Torino", "Milano", "Venezia"])
  data.italy_geopop.from_province()


.. csv-table::
  :file: _static/assets/quick_usage_02.csv
  :header-rows: 1

Regions
-------------

Or you can use italy-geopop to get data for your `pd.Series <https://pandas.pydata.org/docs/reference/api/pandas.Series.html>`_ regions.

.. code-block:: python
  :lineno-start: 7

  data = pd.Series(["Piemonte", "Lombardia", "Veneto"])
  data.italy_geopop.from_region()


.. csv-table::
  :file: _static/assets/quick_usage_03.csv
  :header-rows: 1

More
-------
Check out complete guide for more informations.

