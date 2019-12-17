# pydov <img src="docs/_static/img/logo.png" align="right" alt="" width="120">

[![Build Status](https://travis-ci.org/DOV-Vlaanderen/pydov.svg?branch=master)](https://travis-ci.org/DOV-Vlaanderen/pydov) [![AppVeyor Build status](https://ci.appveyor.com/api/projects/status/4ljy2a0p661v3d9k/branch/master?svg=true)](https://ci.appveyor.com/project/Roel/pydov) [![Documentation Status](https://readthedocs.org/projects/pydov/badge/?version=latest)](https://pydov.readthedocs.io/en/latest/?badge=latest) [![Coverage Status](https://coveralls.io/repos/github/DOV-Vlaanderen/pydov/badge.svg?branch=master)](https://coveralls.io/github/DOV-Vlaanderen/pydov?branch=master) [![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2788680.svg)](https://doi.org/10.5281/zenodo.2788680)

pydov is a Python package to query and download data from [Databank Ondergrond Vlaanderen (DOV)](https://www.dov.vlaanderen.be). It is hosted on [GitHub](https://github.com/DOV-Vlaanderen/pydov) and development is coordinated by Databank Ondergrond Vlaanderen (DOV). DOV aggregates data about soil, subsoil and groundwater of Flanders and makes them publicly available. Interactive and human-readable extraction and querying of the data is provided by a [web application](https://www.dov.vlaanderen.be/portaal/?module=verkenner#ModulePage), whereas the focus of this package is to **support machine-based extraction and conversion of the data**.

To get started, see the documentation at https://pydov.readthedocs.io.

Please note that downloading DOV data with pydov is governed by the same [disclaimer](https://www.dov.vlaanderen.be/page/disclaimer) that applies to the other DOV services. Be sure to consult it when using DOV data with pydov.

## Installation

You can install `pydov` stable easily using pip:

```shell script
pip install pydov
```

Or clone the Git repository and install with `setup.py` to get the latest snapshot from the master branch.

## Quick start

Read the [quick start](https://pydov.readthedocs.io/en/stable/quickstart.html) from the docs or jump straight in:

```python
from pydov.search.boring import BoringSearch
from pydov.util.location import Within, Box

from owslib.fes import PropertyIsGreaterThan

boringsearch = BoringSearch()

dataframe = boringsearch.search(
    query=PropertyIsGreaterThan( propertyname='diepte_tot_m', literal='2000'),
    location=Within(Box(94720, 186910, 112220, 202870))
)
```

## Documentation

Full documentation of `pydov` can be found on our [ReadTheDocs page](https://pydov.readthedocs.io).

## Meta

- We welcome [contributions](.github/CONTRIBUTING.rst) including bug reports.
- License: MIT
- Citation information can be found on [Zenodo](https://doi.org/10.5281/zenodo.2788680).


- Please note that this project is released with a [Contributor Code of Conduct](.github/CODE_OF_CONDUCT.rst). By participating in this project you agree to abide by its terms.


- Also note that downloading DOV data with pydov is governed by the same [disclaimer](https://www.dov.vlaanderen.be/page/disclaimer) that applies to the other DOV services. Be sure to consult it when using DOV data with pydov.
