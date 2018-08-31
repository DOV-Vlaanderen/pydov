
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
