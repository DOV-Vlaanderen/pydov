
.. _quickstart:

-----------
Quick start
-----------

To get started with pydov you should first determine which information you want to search for. DOV provides a lot of different datasets about soil, subsoil and groundwater of Flanders, some of which can be queried using pydov.

Currently, we support the following datasets:

.. csv-table:: Dataset search objects
    :header-rows: 1

    Dataset,Dataset (Dutch),Search object
    Boreholes,Boringen,pydov.search.boring.BoringSearch
    CPT measurements,Sonderingen,pydov.search.sondering.SonderingSearch
    Groundwater screens,Grondwater filters,pydov.search.grondwaterfilter.GrondwaterFilterSearch
    Informal stratigraphy,Informele stratigrafie,pydov.search.interpretaties.InformeleStratigrafieSearch
    Formal stratigraphy,Formele stratigrafie,pydov.search.interpretaties.FormeleStratigrafieSearch
    Hydrogeological stratigraphy,Hydrogeologische stratigrafie,pydov.search.interpretaties.HydrogeologischeStratigrafieSearch
    Coded lithology,Gecodeerde lithologie,pydov.search.interpretaties.GecodeerdeLithologieSearch
    Geotechnical encoding,Geotechnische codering,pydov.search.interpretaties.GeotechnischeCoderingSearch
    Lithological descriptions,Lithologische beschrijvingen,pydov.search.interpretaties.LithologischeBeschrijvingenSearch

Each of the datasets can be queried using a search object for this dataset. While the search objects are different, the workflow is the same for each dataset. Relevant classes can be imported from the pydov.search package, for example if we'd like to query the boreholes dataset:

::

    from pydov.search.boring import BoringSearch
    boringsearch = BoringSearch()

Now we can query for boreholes either on attributes, on location or on a combination of both. To query on attributes, we use the OGC filter functions from OWSLib. For example, to request all boreholes with a depth over 2000 m, we would use the following ``query`` parameter:

::

    from owslib.fes import PropertyIsGreaterThan

    dataframe = boringsearch.search(
        query=PropertyIsGreaterThan(
            propertyname='diepte_tot_m', literal='2000')
    )

To query on location, we use location objects and spatial filters from the pydov.util.location module. For example, to request all boreholes in a given bounding box, we would use the following ``location`` parameter:

::

    from pydov.util.location import Within, Box

    dataframe = boringsearch.search(
        location=Within(Box(94720, 186910, 112220, 202870))
    )

Attribute queries can be combined with location filtering by specifying both parameters in the search call:

::

    dataframe = boringsearch.search(
        query=PropertyIsGreaterThan(
            propertyname='diepte_tot_m', literal='2000'),
        location=Within(Box(94720, 186910, 112220, 202870))
    )

The :ref:`query_attribute` and :ref:`query_location` pages provide an overview of the query options for attributes and locations respectively.

Background
    All the pydov functionalities rely on the existing DOV webservices. An in-depth overview of the available services and endpoints is provided on the :ref:`accessing DOV data <endpoints>` page. To retrieve data, pydov uses a combination of the available :ref:`WFS services <vector_wfs>` and the :ref:`XML representation <xml_data>` of the core DOV data.

    For the datasets listed above (the full overview is enlisted :ref:`here <xml_data>`), the package converts the data into a Pandas :class:`~pandas.DataFrame`, i.e. denormalizing the data. A Pandas DataFrame is a table-like format and the Python `Pandas package`_ provides powerful operations, such as filtering, subsetting, group by operations, etc., making further analysis easy.

    .. _Pandas package: https://pandas.pydata.org/

    As pydov relies on the XML data returned by the existing DOV webservices, downloads of these files can slow down the data retrieval. To mitigate this, pydov implementes some additional features that you can use to speed up your searches. Details are explained in the :ref:`performance guide <performance>`.
