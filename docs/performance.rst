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
