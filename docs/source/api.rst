🔥 API
============
..
   Generated with sphinx-apidoc --force --tocfile api -o ./source ../italy_geopop/

Data provided by the package
--------------------------------

Population data
********************

Population data provided by ISTAT (Istituto Italiano di Statistica).

- ``population_M: float`` - male population;

- ``population_F: float`` - female population;

- ``population: float`` - sum of male and female populations.

Some municipalities have no population data available. Italy-geopop will return `numpy.nan <https://numpy.org/doc/stable/reference/constants.html#numpy.nan>`_.

.. _municipality-data:

Municipality data
**********************

- ``municipality: str`` - municipality name, capitalized, available only if data is retrieved using :py:meth:`italy_goepop.pandas_extension.ItalyGeopop.from_municipality`.
- ``municipality_code: int`` - municipality istat code, available only if data is retrieved using :py:meth:`italy_goepop.pandas_extension.ItalyGeopop.from_municipality`.
- ``municipalities: list`` - a list of dictionaries with the following structure ``{'municipality_code': <municipality code:int>, 'municipality': <municipality name:str}``, available only if data is retrieved using :py:meth:`italy_goepop.pandas_extension.ItalyGeopop.from_province`.

.. _province-data:

Province data
******************

- ``province: str`` - province name, capitalized, available only if data is retrieved using :py:meth:`italy_goepop.pandas_extension.ItalyGeopop.from_province`.
- ``province_code: int`` - province istat code, available only if data is retrieved using :py:meth:`italy_goepop.pandas_extension.ItalyGeopop.from_province`.
- ``provinces: list`` - a list of dictionaries with the following structure ``{'province_code': <province code:int>, 'province': <province name:str, 'municipalities':list[{'municipality_code': <municipality code:int>, 'municipality': <municipality name:str}]}``, available only if data is retrieved using :py:meth:`italy_goepop.pandas_extension.ItalyGeopop.from_region`.


Region data
*******************

- ``region: str`` - region name, capitalized, available if data is retrieved using :py:meth:`italy_goepop.pandas_extension.ItalyGeopop.from_region`.
- ``region_code: int`` - region istat code, available if data is retrieved using :py:meth:`italy_goepop.pandas_extension.ItalyGeopop.from_region`.


Geospatial data
**********************

- .. raw:: html

      <p>
         <code class="docutils literal notranslate">
            <span class="pre">geometry:</span>
            <span class="pre">
               <a class="reference external" href="https://shapely.readthedocs.io/en/latest/geometry.html">geometry types</a>
            </span>
         </code> - geospatial data needed to plot geography, available only if accessor was activated with <code class="docutils literal">include_geometry=True</code>.
      </p>
      


italy\_geopop.pandas\_extension
--------------------------------------
.. _pandas_extension:
.. automodule:: italy_geopop.pandas_extension
   :members:
   :noindex:
   :undoc-members:
   


italy\_geopop.geopop
---------------------------

.. automodule:: italy_geopop.geopop
   :members:
   :noindex:
   :undoc-members:
   :show-inheritance:



