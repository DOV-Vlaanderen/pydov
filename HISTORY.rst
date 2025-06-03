.. _history:

=======
History
=======

v3.3.0
------

- New features

  - Introduce PropertyLikeList and FuzzyJoin query utilities to search for, and join on, fuzzy (non-exact) matches. (#406)

  - Add support for splitting field values into a list of values. (#407)

- Fixes and improvements

  - Update grondmonster type based on WFS/XSD schema updates. (#408)

  - Always request geometry using urn:ogc: srsName to fix coordinate ordering. (#413, #418)


v3.2.0
------

- News

  - This version drops support for Python 3.8.

  - This version adds support for Python 3.12 and Python 3.13.

  - This version is supported on Python 3.9, 3.10, 3.11, 3.12 and 3.13.

- Fixes and improvements

  - Update grondmonster XML based on XSD schema updates. (#404)

  - Fix GMLObject tests. (#401)


v3.1.0
------

- News

  - Add `contribution <https://github.com/DOV-Vlaanderen/pydov/tree/master/contrib>`_ section in the pydov repository. (#394)

- New features

  - Add support for generic DOV WFS layers. Next to the existing 'fixed' datatypes, this make all other WFS data we publish
    available in pydov too, allowing to use them using the same search options as for other datatypes. (#383)

    To support this we are now also more relaxed about metadata being available: we will still use it when it's available,
    but will no longer raise errors when it's not. While all of our layers should have metadata available,
    most of them don't have a feature catalogue. We will now return 'None' in the description of get_fields() when this is missing.

  - Add support for geometry return fields. (#386)

    While it was already possible to do advanced spatial queries, up until now the resulting dataframes only contained 
    attribute fields and not the geometry of the feature. When the necessary dependencies are installed, it is now 
    possible to add geometry fields to your dataframe using the ``return_fields`` parameter. Converting the resulting 
    dataframe into a GeoPandas geodataframe then becomes easy.

- Fixes and improvements

  - Generate stable and unique GML ids for Box and Point locations. (#387, #388)

  - Fix property name replacement in sort_by. (#390, #391)

  - Update mv_mtaw fields based on updated DOV XML schema. (#395)

- Documentation-only updates

  - Open tutorial notebooks through documentation. (#385)


v3.0.0
------

- News

  - This version drops support for Python 3.7.

  - This version adds support for Python 3.11.

  - This version is supported on Python 3.8, 3.9, 3.10 and 3.11.

- Breaking changes

  - pydov3 uses WFS 2.0.0 instead of WFS 1.1.0, as a consequence attribute filters
    should now use FES2.0 and location filters should now use GML3.2. This change 
    impacts a number of places:

      - ``query`` parameter in the 
        :class:`pydov.search.abstract.AbstractSearch.search` method

        Attribute query operators, like PropertyIsEqualTo, PropertyIsGreaterThan and so 
        on, should from now on be imported from the owslib.fes2 package instead 
        of the owslib.fes package. E.g.::

          # change this
          from owslib.fes import And, PropertyIsEqualTo

          # into this
          from owslib.fes2 import And, PropertyIsEqualTo

      - ``sort_by`` parameter in the 
        :class:`pydov.search.abstract.AbstractSearch.search` method

        Also the SortBy operator should from now on be imported from the the owslib.fes2 
        package instead of the owslib.fes package. E.g.::

          # change this
          from owslib.fes import SortBy, SortProperty

          # into this
          from owslib.fes2 import SortBy, SortProperty

      - The :class:`pydov.util.location.GmlObject` class now expects GML3.2 
        geometries instead of GML3.1.1.

        Use GML3.2 objects from now on.

      - The :class:`pydov.util.location.GmlFilter` class now expects GML3.2 
        documents instead of GML3.1.1.

        Transform the document to GML3.2 yourself
        or use a :class:`pydov.util.location.GeometryFilter` instead.

  - The new WFS 2.0.0 querying also allows paged WFS requests which has impact
    on a number of hooks:

      - :class:`pydov.util.hooks.AbstractReadHook.wfs_search_init` now has a 
        single argument ``params`` with all the parameters used to initiate the 
        WFS search.

      - :class:`pydov.util.hooks.AbstractReadHook.wfs_search_result` now has
        two arguments ``number_matched`` and ``number_returned``. Since there 
        can be multiple (paged) WFS results per search, this hook can now be called 
        multiple times per search query. It can also be called simultaneously
        from different threads.

      - :class:`pydov.util.hooks.AbstractReadHook.wfs_search_result_received` is
        affected in a similar manner: this too can now be called multiple times 
        per search, simultaneously from different threads.

      - :class:`pydov.util.hooks.AbstractInjectHook.inject_wfs_getfeature_response`
        is affected as well. This too can now be called multiple times per search, 
        simultaneously from different threads.

- New features

  - Add support for WFS paging, allowing larger queries. It is now possible to
    execute queries larger than the WFS response feature limit of 10000 features
    without running into a FeatureOverflowError. (#194)

    Please be kind to our infrastructure and only request the data you need.

  - Add support for repeatable sessions, allowing recording and replaying of
    pydov sessions. More information and use cases can be found in the
    `documentation <https://pydov.readthedocs.io/en/stable/repeatable_log.html>`_. (#224)

- Fixes and improvements

  - Fix parsing of datetime fields.
  - Replace unparseable data with NaN and issue a warning. (#368)
  - Raise MetadataNotFoundError when remote metadata fails to be downloaded or
    parsed.
  - Populate custom fields in all circumstances. (#379)


v2.2.3
------

* Fixes and improvements

  * Following the 0.28.1 OWSLib security release, disable XML entity resolution when using lxml's XMLParser.


v2.2.2
------

* Fixes and improvements

  * When data received from DOV fails to be parsed by pydov, set it to NaN and issue a warning instead of crashing.


v2.2.1
------

* Fixes and improvements

  * AquiferEnumType has been replaced with AquiferHCOVv1EnumType in both Grondwaterfilter and HydrogeologischeStratigrafie.


v2.2.0
------

- News

  - This version adds support for Python 3.10.

  - This version drops support for Python 3.6.

  - This version is supported on Python 3.7, 3.8, 3.9 and 3.10.

- New features

  - Add new object types for soil data, including:

    - Soil depth intervals (bodemdiepteintervallen)

    - Soil classifications (bodemclassificaties)

  - Added `Fractiemeting` as a subtype to the `Bodemobservatie` type.

  - Renamed `glauconiet` to `glauconiet_totaal` in Grondmonster and added example on how to retrieve detailed glauconite values.

  - Added support for proxy server autodiscovery using PAC.


v2.1.0
------

- News

  - This version adds support for Python 3.9.

  - This version is supported on Python 3.6, 3.7, 3.8 and 3.9.

  - We are proud to be a part of the growing `pyOpenSci <https://www.pyopensci.org/>`_ community promoting open and reproducible research.

- New features

  - Add support for location-based searching using vectorfiles (f.ex. Shapefile, Geopackage) and Geopandas dataframes.

  - Add new object type for groundwater permits (GrondwaterVergunning)

  - Add new object types for soil data, including:

    - Soil sites (Bodemsite)

    - Soil plots (Bodemlocatie)

    - Soil samples (Bodemmonster)

    - Soil observations (Bodemobservatie)

- Fixes and improvements

  - Fix bugs that occur when the XML webservice is unavailable, i.e. prevent caching errors and return stale data if available.

  - Retry failed network requests to make pydov more resilient to bad network connections.

  - Switched from the main DOV WFS endpoint to workspace-level endpoints, this is more efficient and allows a cleaner codebase.

  - Add the `start_interpretatie_mtaw` field to the interpretatie types.

  - Add the `mv_mtaw` field to the Sondering type.

v2.0.1
------

- Fixes and improvements

  - Fix the 'z' field of the Sondering type, it is replaced by 'lengte' and 'diepte' following the DOV XSD schema update.

v2.0.0
------

- News

  - This version drops support for Python 2.7 and Python 3.5.

  - This version is supported on Python 3.6, 3.7 and 3.8.

- Fixes and improvements

  - Fix the korrelvolumemassa, volumemassa and watergehalte fields of Grondmonster type.

  - Add the 'mv_mtaw' field to the GrondwaterFilter type.

  - Extend the hooks system and distinguish between read and inject hooks. The 'xml_requested' hook has been removed in favor of 'xml_received'.

  - Generate stable WFS GetFeature requests, allowing f.ex. hooks to reuse cached responses.

- Development-only updates

  - Remove some code duplication between pydov and OWSLib.

  - Simplify test fixtures setup.

  - Remove duplicate docstrings to simplify the codebase.

- Documentation-only updates

  - Add introductory tutorial.

  - Add a tutorial on how to use a WFS geometry as location query.

  - Update development installation instructions.

  - Update folium examples to support the latest pyproj version.

  - Add extra Binder links on top of each tutorial.

  - Improve charts by including a title and axis labels.

  - Improve README by adding dataframe output.


v1.0.0
------

- News

  - This version is promoted to Stable.

  - This version is the last to support Python 2.7.

- Fixes and improvements

  - Fix the PropertyInList and Join query operators.

  - Increase the default request timeout to 5 minutes to enable larger WFS queries.

  - Retype the `meetnet_code` field of GrondwaterFilter from integer to string.

  - Pin the dependencies to keep explicit Python2 support.

- Development-only updates

  - Make the DOV base URL configurable to be able to test against the DOV testing environment.


v0.3.0
------

- News

  - This version is promoted to Beta.

  - This version adds support for Python3.7 (next to 2.7, 3.5 and 3.6)

- New features

  - Add new object type for Borehole samples (grondmonsters)

  - Add new object type for Groundwater samples (grondwatermonsters)

  - Add new object type for Informal hydrogeological stratigraphy (informele hydrogeologische stratigrafie)

  - Add support for runtime object type customization (pluggable types) allowing full control of the output dataframes

  - Add support for limit (max_features) when searching: this allows to explore the results of a query easily

  - Add support for sorting when searching, allowing to retrieve f.ex. the deepest borehole etc.

- Fixes and improvements

  - Fix 'mv_mtaw' field of GrondwaterFilter, it is renamed to 'start_grondwaterlocatie_mtaw'

  - Output dataframe columns are now in the order provided in return_fields, if available.

  - The PropertyInList and Join query operators now work with single-item lists and dataframes too.

- Documentation-only updates

  - Fix DOI badge and Zenodo link: always link to the latest release


v0.2.1
------

- Fixes and improvements

  - Fix download of Feature Catalogues from the new DOV Geonetwork 3.6 instance.

v0.2.0
------

- New features

  - Add new object type for Quaternary stratigraphy (Quartair stratigrafie)

  - Add support for using Join using a different column name: `Join(df, on='...', using='...')`

  - Add 'filterstatus' and 'filtertoestand' to Peilmeting subtype of GrondwaterFilter

- Fixes and improvements

  - Fix search for GrondwaterFilters (update for WFS service changes regarding `filternr`)

  - Fix 'Methode' field of Peilmeting subtype of GrondwaterFilter

  - Exclude empty filters (i.e. Put without Filter) from GrondwaterFilterSearch

  - Improve performance by using parallel processing and connection pooling

- Documentation-only updates

  - Update contributing guidelines

v0.1.3
------

- This release will be the first on Zenodo.
