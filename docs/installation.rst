.. highlight:: shell

.. _installation:

============
Installation
============

Stable release
--------------

To install pydov, run this command in your terminal:

.. code-block:: console

    $ pip install pydov

This is the preferred method to install pydov, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/

.. note::

    To be able to use vector files not defined as GML (for example ESRI Shape files), some additional dependencies
    are required which are not installed by default. One of the dependencies is `Fiona`_, it is described as "GDAL’s
    neat and nimble vector API for Python programmers". `GDAL`_ is a translator library for raster and vector
    geospatial data formats. Fiona is also required by `GeoPandas`_. Combining these three packages, vector files like
    ESRI Shape files can be converted to GML files and used in spatial queries to DOV. To install the required
    dependencies to handle vector files, add the `vectorfile` option to the installation instruction:

    .. code-block:: console

        pip install pydov[vectorfile]

    Installing these package on Windows can be cumbersome. Please consult the installation guides of the
    different packages. If you are using conda, pre-install them with :code:`conda install -c conda-forge fiona geopandas`
    in your pydov conda environment before running the pydov installation. If you are not using conda,
    give the following a try:

    #. Install `pipwin`_ using :code:`pip install pipwin`
    #. Using pipwin, download the latest Windows binaries for GDAL, Fiona and GeoPandas provided by `Christoph Gohlke`_:

      #. Install `GDAL`_ with :code:`pipwin install gdal`
      #. Install `Fiona`_ with :code:`pipwin install fiona`
      #. Install `GeoPandas`_ with :code:`pipwin install geopandas`

.. _Fiona: https://pypi.org/project/Fiona/
.. _GDAL: https://gdal.org/
.. _GeoPandas: https://geopandas.org/
.. _Pipwin: https://pypi.org/project/pipwin/
.. _Christoph Gohlke: https://www.lfd.uci.edu/~gohlke/pythonlibs/

From sources
------------

The sources for pydov can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/DOV-Vlaanderen/pydov

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/DOV-Vlaanderen/pydov/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install

.. _Github repo: https://github.com/DOV-Vlaanderen/pydov
.. _tarball: https://github.com/DOV-Vlaanderen/pydov/tarball/master


.. _devinstallation:

For package contributors
------------------------

Noticed a bug, want to improve the documentation? Great! Want to dive into the code directly on your local machine? Make sure to
have the development environment setup:

- Fork the `project repository <https://github.com/DOV-Vlaanderen/pydov>`_ by clicking on the 'Fork' button
  near the top right of the page. This creates a copy of the code under your personal GitHub user account.

- Clone the `Github repo`_:

.. code-block:: console

    $ git clone git://github.com/YOUR-GITHUB-USERNAME/pydov

- Create a development environment, for example using `conda`_ or `venv`_:

.. code-block:: console

    # using conda:
      $ conda create -n pydov python=3.7
      $ conda activate pydov

    # or using venv (commands are OS dependent):
      # linux users
        $ python3 -m venv pydov/venv              # linux users
        $ source pydov/venv/bin/activate          # linux users

      # windows users
        $ python3 -m venv pydov\venv              # windows users
        $ pydov\venv\Scripts\activate             # windows users

The Python documentation on `virtual environments`_ provides more guidance on using a development environment.

- From inside the "pydov" repository folder, install all development dependencies and the package in development mode:

.. code-block:: console

    $ pip install -e .[devs]

- To build the documentation, make sure to also install `pandoc`_ as it is required by `Sphinx`_, the
  tool used to generate the documentation website. See the `pandoc installation instructions`_.

.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _pandoc: https://pandoc.org
.. _pandoc installation instructions: https://pandoc.org/installing.html

.. note::
    If the :code:`sphinx-build` (or :code:`make html`) CLI command returns an error, try to reinstall sphinx separately in the environment using
    :code:`pip install -U sphinx`.

Have a look at the :ref:`development guidelines <dev-guidelines>` to see how we develop the pydov package and get more information on the workflow.

.. _conda: https://docs.conda.io/en/latest/miniconda.html
.. _venv: https://docs.python.org/3/library/venv.html#module-venv
.. _virtual environments: https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments
