🔥 API
============
..
   Generated with sphinx-apidoc --force --tocfile api -o ./source ../italy_geopop/

Data provided by the package
--------------------------------

Population data
********************

Population data provided by ISTAT (Istituto Italiano di Statistica). Starting from version ``0.4.0`` the database contains data for every age from 0 to 100 years and divided into males and females.
Male data will have the suffix ``_M`` and female data will have the suffix ``_F`` while the sum of both males and females will have no suffix at all.

.. important::
  Age ``100`` contains data for age ≥ 100 years.

.. _default-label-naming-rule:

**Default label naming rule**

Considering ``population_limits=[25, 50, 75]``, the default label prefix naming rule will be:

- ``<25`` for the first element.
- ``25-50`` for the second elements.
- ``50-75`` for the penultimate element.
- ``>=75`` for the last element.

Don't forget that those prefix will be combined with the suffix ``_M``, ``_F``, obtaining the following labels:

- ``<25_M``, ``<25_F`` and ``<25`` for the first element (males, females, all).
- ``25-50_M``, ``25-50_F`` and ``25-50`` for the second element.
- ``50-75_M``, ``50-75_F`` and ``50-75`` for the penultimate element.
- ``>=75_M``, ``>=75_F`` and ``>=75`` for the last element.

**Customizing population group cutoffs**

When using methods that take ``population_limits`` as parameter three different behaviour are contemplated.

1. ``population_limits='total'`` - returns the total population with the prefix ``'population'`` so return columns will be ``population_M``, ``population_F`` and ``population``.

2. ``population_limits='auto'`` - returns population divided in default age groups using default age cutoffs that are ``[3, 11, 19, 25, 50, 65, 75]``. The generated groups will be called according to the :ref:`default label naming rule<default-label-naming-rule>` defined above.

3. ``population_limits=[int]`` - returns population divided in age groups using the provided cutoffs. ``population_limits`` will be sorted in ascending order, converted to int and duplicates will be removed. The generated groups will be called according to the :ref:`default label naming rule<default-label-naming-rule>` defined above.

.. important::
   Remember that custom provided cutoffs will be used to generate groups whose lower bound is included and upper bound is excluded. For example, if you provide ``population_limits=[25, 50, 75]`` the generated groups will be ``[25, 50)`` and ``[50, 75)``. Plus a group that includes ages lower than the first cutoff and a group that includes ages greater or equal than the last will be added, in this example ``[0, 25)`` and the last group will be ``[75, ]``.

.. warning::
   Values below or equal than 0 and greater than 100 will be ignored.
   

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



