
.. _quickstart:

-----------
Quick start
-----------

To get started with pydov you should first determine which information you want to search for. DOV provides a lot of different datasets about soil, subsoil and groundwater of Flanders, most of which can be queried using pydov. Check out the datasets we support on the :ref:`select datasets <select_datasets>` page.

Each of the datasets can be queried using a search object for this dataset. While the search objects are different, the workflow is the same for each dataset. Relevant classes can be imported from the pydov.search package, for example if we'd like to query the boreholes dataset:

.. code-block:: python

    from pydov.search.boring import BoringSearch
    boringsearch = BoringSearch()

Now we can query for boreholes either on :ref:`attributes <query_attribute>`, on :ref:`location <query_location>` or on a combination of both. To query on attributes, we use the OGC filter functions from OWSLib. For example, to request all boreholes with a depth over 550 m, we would use the following ``query`` parameter:

.. code-block:: python

    from owslib.fes2 import PropertyIsGreaterThan

    dataframe = boringsearch.search(
        query=PropertyIsGreaterThan(
            propertyname='diepte_tot_m', literal='550')
    )
    dataframe

pydov will perform the search and load the matching data (status is shown in the progress bar) into a Pandas DataFrame:

::

    [000/253] ..................................................
    [050/253] ..................................................
    [100/253] ..................................................
    [150/253] ..................................................
    [200/253] ..................................................
    [250/253] ...

                                               pkey_boring     boornummer         x         y  mv_mtaw  start_boring_mtaw           gemeente  diepte_boring_van  diepte_boring_tot datum_aanvang                          uitvoerder  boorgatmeting  diepte_methode_van  diepte_methode_tot  boormethode
    0    https://www.dov.vlaanderen.be/data/boring/1965...  kb15d27e-B149  144820.0  217840.0     2.00               2.00            Beveren                0.0             622.00    1965-07-13  Belgische Geologische Dienst (BGD)           True                0.00              622.00     onbekend
    1    https://www.dov.vlaanderen.be/data/boring/1984...    kb9d9w-B244  200063.0  235530.0    30.44              30.44             Ravels                0.0             570.00    1984-03-19                       Smet - Dessel           True                0.00              570.00  spoelboring
    2    https://www.dov.vlaanderen.be/data/boring/2016...  kb25d61e-B348  209825.6  195829.2    38.00              38.00           Beringen                0.0             575.00           NaN                            onbekend          False                0.00              575.00     onbekend
    3    https://www.dov.vlaanderen.be/data/boring/1901...    kb26d63e-B1  237924.0  194897.0    65.00              65.00         Opglabbeek                0.0             713.27    1901-01-01  Belgische Geologische Dienst (BGD)          False                0.00              713.27     onbekend
    4    https://www.dov.vlaanderen.be/data/boring/1902...    kb26d63e-B2  235262.0  197398.0    75.30              75.30  Meeuwen-Gruitrode                0.0             870.10    1902-01-01  Belgische Geologische Dienst (BGD)          False                0.00              870.10     onbekend
    ..                                                 ...            ...       ...       ...      ...                ...                ...                ...                ...           ...                                 ...            ...                 ...                 ...          ...
    405  https://www.dov.vlaanderen.be/data/boring/2002...    BGD048e0294  238725.0  201000.0    51.00              51.00               Bree                0.0             571.15    2002-05-21                          Smet - GWT           True              416.09              566.14    rollerbit
    406  https://www.dov.vlaanderen.be/data/boring/2002...    BGD048e0294  238725.0  201000.0    51.00              51.00               Bree                0.0             571.15    2002-05-21                          Smet - GWT           True              566.14              571.15   kernboring
    407  https://www.dov.vlaanderen.be/data/boring/1995...    BGD016E0230  174827.0  227892.0    28.00              28.00        Rijkevorsel                0.0            1061.00    1995-01-01                               Cofor          False                0.00             1061.00  spoelboring
    408  https://www.dov.vlaanderen.be/data/boring/1995...    BGD016E0231  174839.0  227842.0    28.00              28.00        Rijkevorsel                0.0            1150.00    1995-01-01                               Cofor          False                0.00             1150.00  spoelboring
    409  https://www.dov.vlaanderen.be/data/boring/1996...    BGD016E0232  174839.0  227846.0    28.00              28.00        Rijkevorsel                0.0            1042.10    1996-01-01                               Cofor          False                0.00             1042.10  spoelboring

    [410 rows x 15 columns]

To query on location, we use location objects and spatial filters from the pydov.util.location module. For example, to request all boreholes in a given bounding box, we would use the following ``location`` parameter:

.. code-block:: python

    from pydov.util.location import Within, Box

    dataframe = boringsearch.search(
        location=Within(Box(107500, 202000, 108500, 203000))
    )
    dataframe.head()

pydov will perform the search and load the matching data into a Pandas DataFrame. For convenience, only the first 5 lines are shown in the output using the :code:`.head()` method from Pandas:

::

    [000/035] ...............cc..................

                                             pkey_boring           boornummer         x         y  mv_mtaw  start_boring_mtaw gemeente  diepte_boring_van  diepte_boring_tot datum_aanvang                                uitvoerder  boorgatmeting  diepte_methode_van  diepte_methode_tot   boormethode
    0  https://www.dov.vlaanderen.be/data/boring/1998...  UG-TGO-98/01-SB12F2  107585.0  202595.0     5.06               5.06  Evergem                0.0               7.25    1998-02-05  Universiteit Gent - Geologisch Instituut          False                 0.0                7.25   spoelboring
    1  https://www.dov.vlaanderen.be/data/boring/1895...         kb14d40e-B65  107881.0  202552.0     5.00               5.00     Gent                0.0               1.80    1895-01-01                                  onbekend          False                 0.0                1.80  droge boring
    2  https://www.dov.vlaanderen.be/data/boring/1927...        kb14d40e-B128  108006.0  202737.0     5.00               5.00     Gent                0.0              38.00    1927-01-01                       Van Santen-Wetteren          False                 0.0               38.00   spoelboring
    3  https://www.dov.vlaanderen.be/data/boring/1947...        kb14d40e-B182  108054.0  202838.0     5.00               5.00     Gent                0.0             276.00    1947-01-01                Behiels-(Lemmens)-Wetteren          False                 0.0              276.00   spoelboring
    4  https://www.dov.vlaanderen.be/data/boring/1947...        kb14d40e-B183  108054.0  202838.0     5.00               5.00     Gent                0.0             312.00    1947-01-01                                  onbekend          False                 0.0              312.00  droge boring

.. note::

    Notice the :code:`cc` in the progress bar while loading of the data? It means the data was loaded from
    your local cache instead of being downloaded, as it was already part of an earlier data request. See the :ref:`caching documentation <caching>`
    for more in-depth information.

Attribute queries can be combined with location filtering by specifying both parameters in the search call:

.. code-block:: python

    dataframe = boringsearch.search(
        query=PropertyIsGreaterThan(
            propertyname='diepte_tot_m', literal='550'),
        location=Within(Box(107500, 202000, 108500, 203000))
    )
    dataframe

pydov will perform the search and return the data that matches both the attribute and the location filters as a Pandas DataFrame:

::

    [000/002] cc

                                             pkey_boring     boornummer         x         y  mv_mtaw  start_boring_mtaw gemeente  diepte_boring_van  diepte_boring_tot datum_aanvang uitvoerder  boorgatmeting  diepte_methode_van  diepte_methode_tot boormethode
    0  https://www.dov.vlaanderen.be/data/boring/1989...  kb14d40e-B777  108015.0  202860.0      5.0                5.0     Gent                0.0              660.0    1989-01-25   onbekend          False                 0.0               660.0    onbekend
    1  https://www.dov.vlaanderen.be/data/boring/1972...  kb14d40e-B778  108090.0  202835.0      5.0                5.0     Gent                0.0              600.0    1972-05-17   onbekend          False                 0.0               600.0    onbekend


The :ref:`query_attribute` and :ref:`query_location` pages provide an overview of the query options for attributes and locations respectively.

.. admonition:: Background

    All the pydov functionalities rely on the existing DOV webservices. An in-depth overview of the available services and endpoints is provided on the :ref:`accessing DOV data <endpoints>` page. To retrieve data, pydov uses a combination of the available :ref:`WFS services <vector_wfs>` and the :ref:`XML representation <xml_data>` of the core DOV data.

    For the datasets listed above (the full overview is enlisted :ref:`here <xml_data>`), the package converts the data into a Pandas :class:`~pandas.DataFrame`, i.e. denormalizing the data. A Pandas DataFrame is a table-like format and the Python `Pandas package`_ provides powerful operations, such as filtering, subsetting, group by operations, etc., making further analysis easy.

    .. _Pandas package: https://pandas.pydata.org/

    As pydov relies on the XML data returned by the existing DOV webservices, downloads of these files can slow down the data retrieval. To mitigate this, pydov implements some additional features that you can use to speed up your searches. Details are explained in the :ref:`performance guide <performance>`.
