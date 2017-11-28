=====
PyDOV
=====

.. image:: https://travis-ci.org/DOV-Vlaanderen/pydov.svg?branch=master
    :target: https://travis-ci.org/DOV-Vlaanderen/pydov

.. image:: https://ci.appveyor.com/api/projects/status/4ljy2a0p661v3d9k?svg=true
    :target: https://ci.appveyor.com/project/Roel/pydov

.. image:: https://readthedocs.org/projects/pydov/badge/?version=latest
    :target: http://pydov.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/DOV-Vlaanderen/pydov/badge.svg?branch=master
    :target: https://coveralls.io/github/DOV-Vlaanderen/pydov?branch=master

A Python package to query and download data from Databank Ondergrond Vlaanderen (DOV).

* Free software: MIT license
* Documentation: https://pydov.readthedocs.io.

Introduction
------------

The pydov package is a community effort and everyone is welcome to contribute. It is hosted on `GitHub <https://github.com/DOV-Vlaanderen/pydov>`_ and development is coordinated by `Databank Ondergrond Vlaanderen (DOV) <https://dov.vlaanderen.be/dovweb/html/index.html>`_. DOV aggregates data about soil, subsoil and groundwater of Flanders and makes them publicly available. Interactive and human-readable extraction and querying of the data is provided by a `web application <https://www.dov.vlaanderen.be/portaal/?module=verkenner#ModulePage>`_\ , whereas the focus of this package is to support **machine-based** extraction and conversion of the data. The pacakge aims to support a set of complementary use cases, for example:

* integrate DOV data in larger data processing pipelines
* support the reproducibility and/or repeatability of research studies
* integrate the data in third-party applications

The machine-based availability of the data can potentially serve a diverse community of researchers, consultants, modelers, and students. As performant and proper functioning of DOV data processing is of interest to the variety of users, we believe that a community-based effort to develop and maintain these functionalities as an open source package provides the optimal development traject.

Scope of the package
--------------------

The ``pydov`` provides in the first place a convenient wrapper around the XML **export** of the `DOV Verkenner <https://www.dov.vlaanderen.be/portaal/?module=verkenner#ModulePage>`_ and related applications, in combination with the available `DOV WMS/WFS webservices <https://dov.vlaanderen.be/dovweb/html/services.html>`_. By combining the information of these web services, different data request use cases can be automated.

The central elements of the package are:

#. ``search``, i.e. check the available information to download and atrributes to query
#. ``download_``, i.e. extraction part: downloading data based on a single station or a list of stations. The user extracts data using the available filters. An important filter is the ``location``, which can be expressed using different spatial entities, ``coordinates``, ``boundingbox``\ , ``aquifer``\ , ``polygon``\ ,...
#. ``subset_*``\ , i.e. filter part: this should provide some straightforward functions to further filter the downloaded data.
#. ``to_***``\ , i.e. conversion part: the data is stored or exported to a new file-format that could be useful for the user. ``to_csv``\ / ``to_excel`` are straight forward examples, but more advanced and domain-specific export functionalities are envisioned, e.g. ``to_modflow()``\ , ``to_menyanthes()``\ , ``to_swap()``

