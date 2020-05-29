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

Have a look at the :ref:`development guidelines <dev-guidelines>` to see ow we develop the pydov package and get more information on the workflow.

.. _conda: https://docs.conda.io/en/latest/miniconda.html
.. _venv: https://docs.python.org/3/library/venv.html#module-venv
.. _virtual environments: https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments
