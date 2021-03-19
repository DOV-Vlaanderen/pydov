.. _history:

=======
History
=======

v2.0.1
------

* Fixes and improvements

  * Fix the 'z' field of the Sondering type, it is replaced by 'lengte' and 'diepte' following the DOV XSD schema update.

v2.0.0
------

* News

  * This version drops support for Python 2.7 and Python 3.5.

  * This version is supported on Python 3.6, 3.7 and 3.8.

* Fixes and improvements

  * Fix the korrelvolumemassa, volumemassa and watergehalte fields of Grondmonster type.

  * Add the 'mv_mtaw' field to the GrondwaterFilter type.

  * Extend the hooks system and distinguish between read and inject hooks. The 'xml_requested' hook has been removed in favor of 'xml_received'.

  * Generate stable WFS GetFeature requests, allowing f.ex. hooks to reuse cached responses.

* Development-only updates

  * Remove some code duplication between pydov and OWSLib.

  * Simplify test fixtures setup.

  * Remove duplicate docstrings to simplify the codebase.

* Documentation-only updates

  * Add introductory tutorial.

  * Add a tutorial on how to use a WFS geometry as location query.

  * Update development installation instructions.

  * Update folium examples to support the latest pyproj version.

  * Add extra Binder links on top of each tutorial.

  * Improve charts by including a title and axis labels.

  * Improve README by adding dataframe output.


v1.0.0
------

* News

  * This version is promoted to Stable.

  * This version is the last to support Python 2.7.

* Fixes and improvements

  * Fix the PropertyInList and Join query operators.

  * Increase the default request timeout to 5 minutes to enable larger WFS queries.

  * Retype the `meetnet_code` field of GrondwaterFilter from integer to string.

  * Pin the dependencies to keep explicit Python2 support.

* Development-only updates

  * Make the DOV base URL configurable to be able to test against the DOV testing environment.


v0.3.0
------

* News

  * This version is promoted to Beta.

  * This version adds support for Python3.7 (next to 2.7, 3.5 and 3.6)

* New features

  * Add new object type for Borehole samples (grondmonsters)

  * Add new object type for Groundwater samples (grondwatermonsters)

  * Add new object type for Informal hydrogeological stratigraphy (informele hydrogeologische stratigrafie)

  * Add support for runtime object type customization (pluggable types) allowing full control of the output dataframes

  * Add support for limit (max_features) when searching: this allows to explore the results of a query easily

  * Add support for sorting when searching, allowing to retrieve f.ex. the deepest borehole etc.

* Fixes and improvements

  * Fix 'mv_mtaw' field of GrondwaterFilter, it is renamed to 'start_grondwaterlocatie_mtaw'

  * Output dataframe columns are now in the order provided in return_fields, if available.

  * The PropertyInList and Join query operators now work with single-item lists and dataframes too.

* Documentation-only updates

  * Fix DOI badge and Zenodo link: always link to the latest release


v0.2.1
------

* Fixes and improvements

  * Fix download of Feature Catalogues from the new DOV Geonetwork 3.6 instance.

v0.2.0
------

* New features

  * Add new object type for Quaternary stratigraphy (Quartair stratigrafie)

  * Add support for using Join using a different column name: `Join(df, on='...', using='...')`

  * Add 'filterstatus' and 'filtertoestand' to Peilmeting subtype of GrondwaterFilter

* Fixes and improvements

  * Fix search for GrondwaterFilters (update for WFS service changes regarding `filternr`)

  * Fix 'Methode' field of Peilmeting subtype of GrondwaterFilter

  * Exclude empty filters (i.e. Put without Filter) from GrondwaterFilterSearch

  * Improve performance by using parallel processing and connection pooling

* Documentation-only updates

  * Update contributing guidelines

v0.1.3
------

* This release will be the first on Zenodo.
