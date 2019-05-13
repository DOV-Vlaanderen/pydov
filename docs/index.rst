Welcome to pydov's documentation!
==================================

.. image:: https://travis-ci.org/DOV-Vlaanderen/pydov.svg?branch=master
    :target: https://travis-ci.org/DOV-Vlaanderen/pydov

.. image:: https://ci.appveyor.com/api/projects/status/4ljy2a0p661v3d9k/branch/master?svg=true
    :target: https://ci.appveyor.com/project/Roel/pydov

.. image:: https://readthedocs.org/projects/pydov/badge/?version=latest
    :target: http://pydov.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/DOV-Vlaanderen/pydov/badge.svg?branch=master
    :target: https://coveralls.io/github/DOV-Vlaanderen/pydov?branch=master

A Python package to query and download data from Databank Ondergrond Vlaanderen (DOV).

* Free software: MIT license
* Documentation: https://pydov.readthedocs.io

Introduction
------------

The pydov package is a community effort and everyone is welcome to contribute. It
is hosted on `GitHub <https://github.com/DOV-Vlaanderen/pydov>`_ and development is
coordinated by `Databank Ondergrond Vlaanderen (DOV) <https://www.dov.vlaanderen.be>`_. DOV
aggregates data about soil, subsoil and groundwater of Flanders and makes them publicly
available. Interactive and human-readable extraction and querying of the data is provided
by a `web application <https://www.dov.vlaanderen.be/portaal/?module=verkenner>`_\ , whereas
the focus of this package is to support **machine-based** extraction and conversion of
the data. The pacakge aims to support a set of complementary use cases, for example:

* integrate DOV data in larger data processing pipelines
* support the reproducibility and/or repeatability of research studies
* integrate the data in third-party applications

The machine-based availability of the data can potentially serve a diverse community of
researchers, consultants, modelers, and students. As performant and proper functioning
of DOV data processing is of interest to the variety of users, we believe that a
community-based effort to develop and maintain these functionalities as an open source
package provides the optimal development traject.

Please note that downloading DOV data with pydov is governed by the same `disclaimer <https://www.dov.vlaanderen.be/page/disclaimer>`_ that applies to the other DOV services. Be sure to consult it when using DOV data with pydov.

Getting started
---------------

After :ref:`installation`, check the :ref:`quickstart` instructions for a first introduction of
the pydov functionalities. For a more in-depth overview of the capabilities,
the :ref:`tutorials` illustrate different capabilities of the pydov package
for each of the object types (:class:`~pydov.search.grondwaterfilter.GrondwaterFilterSearch`,
:class:`~pydov.search.boring.BoringSearch` and the interpretations derived from
:class:`~pydov.search.interpretaties.InformeleStratigrafieSearch`).

The setup of appropriate queries on attribute or location is similar for the different data types and
crucial to get acces to the required data. The :ref:`query_attribute` and :ref:`query_location` explain
the query options for attributes and locations respectively.

All functionalities are build on top of the existing webservices provided
by DOV. For more details about these services and endpoints, check
the :ref:`endpoints` page.


Contents:
=========

.. toctree::
   :caption: Getting started
   :maxdepth: 1

   installation
   quickstart
   tutorials

.. toctree::
   :caption: User guide
   :maxdepth: 1

   query_attribute
   query_location
   performance
   df_format
   caching
   hooks

.. toctree::
   :caption: Developer guide
   :maxdepth: 1

   contributing
   endpoints
   reference
   history
   authors
   conduct

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
