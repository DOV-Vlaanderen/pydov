
.. _userguide:

==========
User guide
==========

.. toctree::
   :maxdepth: 1
   :hidden:

   df_format
   query_cost
   caching
   hooks

All the pydov functionalities rely on the existing DOV webservices. An in-depth
overview of the available services and endpoints is provided on the :ref:`accessing DOV data <endpoints>` page. To retrieve
data, pydov uses a combination of the available :ref:`WFS services <vector_wfs>` and the
:ref:`XML representation <xml_data>` of the core DOV data.

For the main data sources (the overview is enlisted :ref:`here <xml_data>`), the package converts the data
into (a set of) Pandas :class:`~pandas.DataFrame`, i.e. denormalizing the data. A Pandas :class:`~pandas.DataFrame`
is a column based format and the Python `Pandas package`_ provides powerful operations such as
filtering, subsetting, group by operations, etc. making further analysis possible.

.. _Pandas package: https://pandas.pydata.org/

The output format for each of the main data object types is defined in the
:ref:`object type overview <object_types>`:

* :ref:`Boreholes <ref_boreholes>` output derived from :class:`~pydov.search.boring.BoringSearch`
* :ref:`Groundwater screen<ref_gwfilter>` output derived from :class:`~pydov.search.grondwaterfilter.GrondwaterFilterSearch`
* :ref:`Interpretations <ref_interpretations>` output derived from one of the available interpretation search classes, e.g. :class:`~pydov.search.interpretaties.InformeleStratigrafieSearch`
* :ref:`CPT data <ref_cpt_data>` (not yet implemented)


The workflow to query data is for each of the data object types the same. In the following,
:ref:`Groundwater screen<ref_gwfilter>` is used for the example.

Start with creating an instance of a ``**Search`` class of the appropriate data object class:

::

    from pydov.search.grondwaterfilter import GrondwaterFilterSearch
    gwfilter = GrondwaterFilterSearch()

To search the locations and data points of interest, you can search with ``location`` options, ``query`` options
or both:

::

    df = gwfilter.search(query=PropertyIsEqualTo(propertyname='gemeente',
                                                 literal='Boortmeerbeek'),
                         location=(87676, 163442, 91194, 168043))

The returned information is a :class:`~pandas.DataFrame` as described in the :ref:`object type overview <object_types>`.

The supported query elements for the ``location`` argument is currently a bbox, provided as
tuple (*minx, miny, maxx, maxy*). Other geographical inputs like a coorindate with buffer or
a polygon are not yet implemented.

For the ``query`` argument, pydov relies on the `OWSLib package`_ operators, providing a Python interface to
the WFS protocol operators, such as ``PropertyIsEqualTo``, ``PropertyIsGreaterThan``,...

.. _OWSLib package: https://geopython.github.io/OWSLib/

Hence, in the example code, the groundwater screens in between the given bbox and with the property ``gemeente``
equal to *Boortmeerbeek*. More detailed use cases using these operators are provided
in the :ref:`tutorials section <tutorials>`.

As pydov relies on the ``XML`` returned by the existing DOV webservices, recurrent downloads of these files
can slow down the data search and queries. To counteract this, pydov implementes some additional features
explained in the :ref:`query duration guide <query_cost>`.

Using custom filter expressions
*******************************

pydov adds two custom filter expressions to the available set from OGC described above. They can be imported from the pydov.util.query module.


Query using lists
-----------------

pydov extends the default OGC filter expressions described above with a new expression `PropertyInList` that allows you to use lists (of strings) in search queries.

The `PropertyInList` internally translates to a `PropertyIsEqualTo` and is relevant for string, numeric, date or boolean attributes:

PropertyInList
    Search for one of a list of exact matches.

    Internally this is translated to ``Or([PropertyIsEqualTo(), PropertyIsEqualTo(), ...])``.

    Example: ``PropertyInList(propertyname='methode', list=['ramkernboring', 'spoelboring', 'spade'])``


Join different searches
-----------------------

The `Join` expression allows you to join multiple searches together. This allows combining results from different datasets to get the results you're looking for. Instead of an propertyname and a literal (or a list of literals), this expression takes a Pandas dataframe and a join column. The join column should be a column that exists in the dataframe and is one of the attributes of the type that is being searched.

Join
    Join searches together using a common attribute.

    Example: ``Join(dataframe=df_boringen, join_column='pkey_boring')``

The following example returns all the lithological descriptions of boreholes that are at least 20 meters deep (note that this is different from 'lithological descriptions with a depth of at least 20m'):

::

    from pydov.util.query import Join

    from pydov.search.boring import BoringSearch
    from pydov.search.interpretaties import LithologischeBeschrijvingenSearch

    bs = BoringSearch()
    ls = LithologischeBeschrijvingenSearch()

    boringen = bs.search(query=PropertyIsGreaterThan('diepte_tot_m', '20'),
                         return_fields=('pkey_boring',))

    lithologische_beschrijvingen = ls.search(query=Join(boringen, 'pkey_boring'))

`Join` expressions can be logically combined with other filter expressions, for example to further restrict the resultset:

::

    from owslib.fes import And
    from owslib.fes import PropertyIsEqualTo

    from pydov.util.query import Join

    from pydov.search.boring import BoringSearch
    from pydov.search.interpretaties import LithologischeBeschrijvingenSearch

    bs = BoringSearch()
    ls = LithologischeBeschrijvingenSearch()

    boringen = bs.search(query=PropertyIsGreaterThan('diepte_tot_m', '20'),
                         return_fields=('pkey_boring',))

    lithologische_beschrijvingen = ls.search(query=And([Join(boringen, 'pkey_boring'),
                                                        PropertyIsEqualTo('betrouwbaarheid_interpretatie', 'goed')]))
