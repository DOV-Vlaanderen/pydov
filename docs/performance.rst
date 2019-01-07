.. _output_df_fields:

=======================
Output dataframe fields
=======================

When using pydov to search datasets, the returned dataframe has different default columns (fields) depending on the dataset. We believe each dataframe to contain the most relevant fields for the corresponding dataset, but pydov allows you to select the fields you want to be returned in the output dataframe.

Next to the `query` and `location` parameters, you can use the ``return_fields`` parameter of the `search` method to limit the columns in the dataframe and/or specify extra columns not included by default. The `return_fields` parameter takes a list of field names, which can be any combination of the available fields for the dataset you're searching.

You can get an overview of the available fields for a dataset using its search objects `get_fields` method. More information can be found in :ref:`available_attribute_fields`.

.. note::

    Significant performance gains can be achieved by only including the fields you need, and more specifically by including only fields with a cost of 1. More information can be found in the :ref:`performance` section below.


Default dataframe columns
*************************

Below the default dataframe fields for each dataset are listed:

Boreholes (boringen)
--------------------
  .. csv-table:: Boreholes (boringen)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/1930-120730
    boornummer,1,string,kb15d28w-B164
    x,1,float,152301.0
    y,1,float,211682.0
    mv_mtaw,10,float,8.00
    start_boring_mtaw,1,float,8.00
    gemeente,1,string,Wuustwezel
    diepte_boring_van,10,float,0.00
    diepte_boring_tot,1,float,19.00
    datum_aanvang,1,date,1930-10-01
    uitvoerder,1,string,Smet - Dessel
    boorgatmeting,10,boolean,false
    diepte_methode_van,10,float,0.00
    diepte_methode_tot,10,float,19.00
    boormethode,10,string,droge boring

Groundwater screens (grondwaterfilters)
---------------------------------------
  .. csv-table:: Groundwater screens (grondwaterfilters)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_filter,1,string,https://www.dov.vlaanderen.be/data/filter/1989-001024
    pkey_grondwaterlocatie,1,string,https://www.dov.vlaanderen.be/data/put/2017-000200
    gw_id,1,string,4-0053
    filternummer,1,string,1
    filtertype,1,string,peilfilter
    x,1,float,110490
    y,1,float,194090
    mv_mtaw,10,float,NaN
    gemeente,1,string,Destelbergen
    meetnet_code,10,integer,1
    aquifer_code,10,string,0100
    grondwaterlichaam_code,10,string,CVS_0160_GWL_1
    regime,10,string,freatisch
    diepte_onderkant_filter,1,float,13
    lengte_filter,1,float,2
    datum,10,date,2004-05-18
    tijdstip,10,string,NaN
    peil_mtaw,10,float,4.6
    betrouwbaarheid,10,string,goed
    methode,10,string,NaN

Informal stratigraphy (Informele stratigrafie)
----------------------------------------------
  .. csv-table:: Informal stratigraphy (Informele stratigrafie)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_interpretatie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2016-290843
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/1893-073690
    pkey_sondering,1,string,NaN
    betrouwbaarheid_interpretatie,1,string,onbekend
    x,1,float,108900
    y,1,float,194425
    diepte_laag_van,10,float,0
    diepte_laag_tot,10,float,18.58
    beschrijving,10,string,Q

Hydrogeological stratigraphy (Hydrogeologische stratigrafie)
------------------------------------------------------------
  .. csv-table:: Hydrogeological stratigraphy (Hydrogeologische stratigrafie)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_interpretatie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2001-198755
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/1890-073688
    betrouwbaarheid_interpretatie,1,string,goed
    x,1,float,108773
    y,1,float,194124
    diepte_laag_van,10,float,0
    diepte_laag_tot,10,float,8
    aquifer,10,string,0110

Coded lithology (Gecodeerde lithologie)
---------------------------------------
  .. csv-table:: Coded lithology (Gecodeerde lithologie)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_interpretatie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2003-205091
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/2003-076348
    betrouwbaarheid_interpretatie,1,string,goed
    x,1,float,110601
    y,1,float,196625
    diepte_laag_van,10,float,4
    diepte_laag_tot,10,float,4.5
    hoofdnaam1_grondsoort,10,string,MZ
    hoofdnaam2_grondsoort,10,string,NaN
    bijmenging1_plaatselijk,10,boolean,False
    bijmenging1_hoeveelheid,10,string,N
    bijmenging1_grondsoort,10,string,SC
    bijmenging2_plaatselijk,10,boolean,NaN
    bijmenging2_hoeveelheid,10,string,NaN
    bijmenging2_grondsoort,10,string,NaN
    bijmenging3_plaatselijk,10,boolean,NaN
    bijmenging3_hoeveelheid,10,string,NaN
    bijmenging3_grondsoort,10,string,NaN

Lithological descriptions (Lithologische beschrijvingen)
--------------------------------------------------------
  .. csv-table:: Lithological descriptions (Lithologische beschrijvingen)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_interpretatie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2017-302166
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/2017-151410
    betrouwbaarheid_interpretatie,1,string,onbekend
    x,1,float,109491
    y,1,float,196700
    diepte_laag_van,10,float,0
    diepte_laag_tot,10,float,1
    beschrijving,10,string,klei/zand

.. _performance:

===========
Performance
===========

pydov is built upon existing DOV webservices described in detail on the :ref:`accessing DOV data <endpoints>` page. Using WFS for searching and a combination of :ref:`WFS <vector_wfs>` and :ref:`XML  <xml_data>` services for data downloads, pydov is a reference client implementation on how to use stable DOV services to retrieve data.

While searching and downloading data through WFS is fairly efficient, downloading XML data can significantly slow down data retrieval. This is caused mostly due to the fact that a separate XML document needs to be downloaded for each feature in the WFS resultset.

You can use different strategies to optimize data downloads using pydov:

Limit the fields (or: columns) you request
    Using the ``return_fields`` argument of the search method, you can limit the columns to be returned in the output dataframe. Limiting this to the fields you need and excluding all other fields will increase the data download speed.

    A significant performance gain can be achieved by only including fields with a cost of 1. These fields are available in the WFS service, eliminating the need to download XML documents altogether.

Limit the features (or: rows) you request
    If you do need the data fields with a cost of 10 that require XML downloads, be sure to limit the number of features to retrieve to the ones that you are really interested in. You can build advanced search queries involving both attribute based filters (using the ``query`` parameter) and geographical filters (using the ``location`` parameter). Use them for example to restrict the download to a specific subset or your geographically defined study area.

    Using specific and detailed search queries will limit the number of features to be returned, and a a consequence limit the number of XML documents to be downloaded resulting in a faster download time.

Tweak the pydov cache settings
    To speed up subsequent queries involving the same or similar data, pydov uses a local disk cache for downloaded XML documents. By default, an XML document will be cached and reused up to two weeks after being downloaded. This means that the same XML document will not be downloaded more than once every two weeks, resulting in faster query times involving similar data.

    Depending on your use case or the data you're working with, it can be interesting to adjust the default cache expiration time of two weeks. If you work with slow changing data you can increase this time, so documents are cached for longer extending the performance improvement of using cached XML documents.

    However, if you're working with fast changing data it can be necessary to decrease the cache expiration time to get updated data faster than once every two weeks. It is clear that this can have negative consequences on performance. It is up to the user to make an tradeoff between performance and data delay.

    You can find more information about the caching implementation and how to tweak its settings in the :ref:`caching` section.
