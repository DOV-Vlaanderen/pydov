Welcome to pydov's documentation!
==================================

.. image:: https://github.com/DOV-Vlaanderen/pydov/actions/workflows/ci.yml/badge.svg?branch=master
    :target: https://github.com/DOV-Vlaanderen/pydov

.. image:: https://readthedocs.org/projects/pydov/badge/?version=latest
    :target: http://pydov.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.2788680.svg
   :target: https://doi.org/10.5281/zenodo.2788680
   
.. image:: https://img.shields.io/badge/PyOpenSci-Peer%20Reviewed-success.svg
   :target: https://github.com/pyOpenSci/software-review/issues/19
   :alt: pyopensci approval

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
the data. The package aims to support a set of complementary use cases, for example:

* integrate DOV data in larger data processing pipelines
* support the reproducibility and/or repeatability of research studies
* integrate the data in third-party applications

The machine-based availability of the data can potentially serve a diverse community of
researchers, consultants, modelers, and students. As efficient and proper functioning
of DOV data processing is of interest to the variety of users, we believe that a
community-based effort to develop and maintain these functionalities as an open source
package provides the optimal development trajectory.

Please note that downloading DOV data with pydov is governed by the same `disclaimer <https://www.dov.vlaanderen.be/page/disclaimer>`_ that applies to the other DOV services. Be sure to consult it when using DOV data with pydov.

Getting started
---------------

After :ref:`installation`, check the :ref:`quickstart` instructions for a first introduction of
the pydov functionalities. For a more in-depth overview of the capabilities,
the :ref:`tutorials` illustrate different capabilities of the pydov package
for each of the object types.

:ref:`select_datasets` of your interest, and check the :ref:`query_attribute` and :ref:`query_location` pages to find the information you're looking for.
While the search objects are different, the workflow is the same for each dataset.

All functionalities are built on top of the existing webservices provided
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

   select_datasets
   query_attribute
   query_location
   output_fields
   sort_limit
   performance
   caching
   hooks
   repeatable_log
   network_proxy

.. toctree::
   :caption: Developer guide
   :maxdepth: 1

   contributing
   development
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
