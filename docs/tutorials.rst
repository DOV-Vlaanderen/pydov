.. _tutorials:

=========
Tutorials
=========


These tutorials illustrate use cases the pydov package supports, split
up by different topics each setup as a `jupyter notebook`_
you can run yourself. The introductory tutorial bundles most 
of the interesting features and methods of pydov and would be a good
start.

.. _jupyter notebook: http://jupyter.org/

.. note::
    These tutorials use a number of Python packages that are not required by the pydov package itself. For example `folium`_
    to create interactive maps. We keep track of these dependencies in the :code:`binder/requirements.txt` file. If you want to run the tutorials
    on your own computer, install these packages to your existing :code:`conda` or :code:`venv` environment by running:

    ::

        pip install -r binder/requirements.txt

    One of the dependencies is `Fiona`_, it is described as "`GDAL`_’s neat and nimble vector API for Python programmers". `GDAL`_ is a 
    translator library for raster and vector geospatial data formats. Fiona makes it easy to work with. It's required by GeoPandas,
    which extends the Pandas DataFrames we all love. Combining these three packages, it makes us easy to convert ESRI Shape files to GML files.
    However, it can be cumbersome to get it installed on a Windows. Please consult the installation guides of the different packages or give
    the following a try:

    #. Download the latest wheel (choose the approptiate version, based on your python distribution and operating system) 
       from `www.lfd.uci.edu`_ for both `Fiona`_ and `GDAL`_. For example `Fiona‑1.8.17‑cp38‑cp38‑win_amd64.whl` will 
       allow you to install `Fiona`_ for your python 3.8 distribution on a 64bit Windows system.
    #. Install the wheels using :code:`pip install <your wheel>`
    #. Install `GeoPandas`_ using :code:`pip install geopandas`

.. _folium: https://pypi.org/project/folium/
.. _Fiona: https://pypi.org/project/Fiona/
.. _GDAL: https://gdal.org/
.. _www.lfd.uci.edu: https://www.lfd.uci.edu/~gohlke/pythonlibs/
.. _GeoPandas: https://geopandas.org/

To run these interactively online without installation, use the following binder link:

.. image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/dov-vlaanderen/pydov/master?filepath=docs%2Fnotebooks


.. toctree::
   :maxdepth: 1

   notebooks/introductory_tutorial.ipynb
   notebooks/search_boringen.ipynb
   notebooks/search_sonderingen.ipynb
   notebooks/search_grondwaterfilters.ipynb
   notebooks/search_grondwatermonsters.ipynb
   notebooks/search_formele_stratigrafie.ipynb
   notebooks/search_informele_stratigrafie.ipynb
   notebooks/search_hydrogeologische_stratigrafie.ipynb
   notebooks/search_informele_hydrostratigrafie.ipynb
   notebooks/search_lithologische_beschrijvingen.ipynb
   notebooks/search_gecodeerde_lithologie.ipynb
   notebooks/search_geotechnische_codering.ipynb
   notebooks/search_quartaire_stratigrafie.ipynb
   notebooks/search_grondmonsters.ipynb
   notebooks/customizing_object_types.ipynb
   notebooks/remote_wfs_gml_query.ipynb
   notebooks/caching.ipynb
