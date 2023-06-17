Database Tables
===============

These are the classes that define all the tables in the database.
Under each table, all the columns (which are the class attributes)
are listed.

There are four tables that represent the Self-Sufficiency Standard
data: ``sss.SSS`` contains the columns that are present in all files,
while ``sss.Miscellaneous``, ``sss.HealthCare`` and ``sss.ARPA`` are
helper tables with extra information for some rows in ``sss.SSS``.
The ``sss.Report`` table contains information about when the
Self-Sufficiency Standard report was prepared.

Supplementary information useful for various analyses are contained
the ``sss.GeoID``, ``sss.PUMA``, and ``sss.City`` tables.

Self-Sufficiency Data Tables
----------------------------
.. autoclass:: sss.SSS
    :members:

.. autoclass:: sss.Miscellaneous
    :members:

.. autoclass:: sss.HealthCare
    :members:

.. autoclass:: sss.ARPA
    :members:


Report table
----------
.. autoclass:: sss.Report
    :members:


Geographical Identifier table
-----------------------------
.. autoclass:: sss.GeoID
    :members:

PUMA table
----------
.. autoclass:: sss.PUMA
    :members:

City table
----------
.. autoclass:: sss.City
    :members:
