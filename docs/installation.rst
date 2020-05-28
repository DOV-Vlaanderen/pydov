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


For package contributors
------------------------

Noticed a bug, want to improve the documentation? Great! Have a look at the :ref:`contributing guidelines <contribute>`.
Want to dive into the code directly on your local machine?

- Clone the `Github repo`_:

.. code-block:: console

    $ git clone git://github.com/DOV-Vlaanderen/pydov

- Create a development environment, for example using `conda`_ or `virtualenv`_:

.. code-block:: console

    $ # using conda
    $ conda create -n pydov python=3.7
    $ conda activate pydov

    # or

    $ # using virtualenv
    $ virtualenv pydov
    $ source pydov/bin/activate | pydov\Scripts\activate

- install all development dependencies and the package in development mode:

.. code-block:: console

    $ pip install -e .[devs]

.. note::
    If the :code:`sphinx-build` (or :code:`make html`) CLI command returns an error, try to reinstall sphinx separately in the environment using
    :code:`pip install -U sphinx`.

.. _conda: https://docs.conda.io/en/latest/miniconda.html
.. _virtualenv: https://virtualenv.pypa.io/en/latest/

