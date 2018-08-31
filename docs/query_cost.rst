.. _query_cost:

==============
Query duration
==============

Downloads of the `XML` files provided by the :ref:`DOV webservices <endpoints>` can slow down the data search and
queries, certainly if request are actually reusing information from the same (downloaded) XML file.

To overcome this as much as possible, pydov probides two strategies:

    1. Option to only request ``wfs`` fields using the ``return_fields`` argument
    2. Caching of downloaded files

Using the ``return_fields`` argument
------------------------------------

When only ``wfs`` fields are queried, there is no need to download XML files and the duration of the requests
will be much smaller. Certainly for exploration and testing the queries, this can be beneficial.

To do so, the ``search`` methods provide the ``return_fields`` argument. This argument requires a
list of fields to be returned in the output data. When only requesting fields from the ``wfs``, as
enlisted in the :ref:`object type overview <object_types>` for each of the objects, no XML downloads
are required, resulting in faster requests.

Caching downloaded XML files
----------------------------

To deal with multiple downloads of the same `XML`, pydov uses basic caching of these files. For more information
on the caching settings, see :ref:`the caching guide <caching>`.
