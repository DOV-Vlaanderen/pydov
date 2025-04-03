.. highlight:: shell

.. _installation:

============
Installation
============

Standard version
----------------

To install pydov, run this command in your terminal:

.. code-block:: console

    pip install pydov

This is the preferred method to install pydov, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

Additional geometry support
---------------------------

To be able to use and return geometry fields and vector files other than GML (for example ESRI Shapefiles), some additional dependencies
are required which are not installed by default. To install the required dependencies, add the ``geom`` option to the installation instruction:

.. code-block:: console

    pip install pydov[geom]

If you are using conda, you can also pre-install them with :code:`conda install -c conda-forge fiona geopandas shapely`
in your pydov conda environment before running the pydov installation.

This will enable:

 - :class:`pydov.util.location.GeometryFilter` for spatial querying using vectory files supported by fiona
 - :class:`pydov.util.location.GeopandasFilter` for spatial querying using GeoPandas GeoDataFrames
 - Fields with type 'geometry' to be used as return fields, using :class:`pydov.types.fields.GeometryReturnField`

Additional proxy support
------------------------

If your organisation or network requires the use of a proxy server and has the possibility for it to be autodiscovered using PAC (Proxy Auto-Configuration), pydov can support this too. This requires the installation of extra dependencies not included by default. To install the required dependencies, add the ``proxy`` option to the installation instruction:

.. code-block:: console

    pip install pydov[proxy]

This will enable:

 - Proxy server autodiscovery using PAC. You don't need to make any changes to your scripts to use this functionality, if it is installed it will be used.

More information can be found on the :ref:`network_proxy` page.
