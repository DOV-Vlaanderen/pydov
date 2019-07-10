.. _history:

=======
History
=======

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

  * Update contributing guidelines)

v0.1.3
------

* This release will be the first on Zenodo.
