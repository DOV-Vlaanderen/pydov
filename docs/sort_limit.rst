.. _sort_limit:

=======================
Sorting and using limit
=======================

To find data based on the ordering of one or more of its attributes, we can use the sort_by and max_features parameters of the search objects.

Sorting
*******

Next to the `query` and `location` parameters in the search method, you can use the ``sort_by`` parameter to apply an ordering in the results you retrieve.
While the query and location filters restrict the features returned to the ones matching your query, `sort_by` only influences the order of those results.

Sorting is mainly useful in combination with the `max_features` parameter described below: this allows to retrieve the X latest interpretations, deepest boreholes, etc.

A `sort_by` expression consists of a query field (`propertyname`) and an ordering (`ASC` for ascending or `DESC` for descending). pydov uses the SortBy expression from the OWSLib library, defined in the owslib.fes2 package.

SortBy
    Sort on one or multiple attributes. Takes a list of SortProperty instances for sorting.

    Example: ``SortBy([SortProperty(propertyname='diepte_boring_tot', order='DESC')])``


Finding the 10 deepest boreholes is now straightforward::

    from pydov.search.boring import BoringSearch
    from owslib.fes2 import SortBy, SortProperty

    bs = BoringSearch()
    df = bs.search(sort_by=SortBy([SortProperty('diepte_boring_tot', 'DESC')]),
                   max_features=10,
                   return_fields=('pkey_boring', 'diepte_boring_tot'))


Limit number of features
************************

Within the search method, the ``max_features`` parameter can be used to limit the number of WFS features you want to
be returned. This is mainly useful when exploring the data or in combination with the `sort_by` parameter. The following example
limits the number of features to 2 within the search for grondwaterfilter. The usage is similar for the search for other objects.

::

    from pydov.search.grondwaterfilter import GrondwaterFilterSearch
    from pydov.util.location import Within, Box

    gwfilter = GrondwaterFilterSearch()
    df = gwfilter.search(location=Within(Box(93378, 168009, 94246, 169873)),
                         max_features=2)

Mind that the amount of features requested not necessarily equals the number of lines in the resulting DataFrame. For example in the case
of `grondwaterfilter` multiple water levels can be available for each feature, resulting in multiple rows.
