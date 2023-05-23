# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV groundwater screen
 data."""
from owslib.fes2 import And, Not, PropertyIsNull

from ..types.grondwaterfilter import GrondwaterFilter
from .abstract import AbstractSearch


class GrondwaterFilterSearch(AbstractSearch):
    """Search class to retrieve information about groundwater screens
    (GrondwaterFilter).
    """

    def __init__(self, objecttype=GrondwaterFilter):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the GrondwaterFilter type.
            Optional: defaults to the GrondwaterFilter type containing the
            fields described in the documentation.

        """
        super(GrondwaterFilterSearch,
              self).__init__('gw_meetnetten:meetnetten', objecttype)

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        """Search for objects of this type. Provide `location` and/or
        `query` and/or `max_features`.
        When `return_fields` is None, all fields are returned.

        Excludes 'empty' filters (i.e. Putten without Filters) by extending
        the `query` with a not-null check on pkey_filter.

        Parameters
        ----------
        location : pydov.util.location.AbstractLocationFilter or \
                   owslib.fes2.BinaryLogicOpType<AbstractLocationFilter> or \
                   owslib.fes2.UnaryLogicOpType<AbstractLocationFilter>
            Location filter limiting the features to retrieve. Can either be a
            single instance of a subclass of AbstractLocationFilter, or a
            combination using And, Or, Not of AbstractLocationFilters.
        query : owslib.fes2.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes2. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        sort_by : owslib.fes2.SortBy, optional
            List of properties to sort by.
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.
        max_features : int
            Limit the maximum number of features to request.

        Returns
        -------
        pandas.core.frame.DataFrame
            DataFrame containing the output of the search query.

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not one of `location` or `query` or `max_features` is
            provided.

        pydov.util.errors.InvalidFieldError
            When at least one of the fields in `return_fields` is unknown.

            When a field that is only accessible as return field is used as
            a query parameter.

            When a field that can only be used as a query parameter is used as
            a return field.

        AttributeError
            When the argument supplied as return_fields is not a list,
            tuple or set.

        NotImplementedError
            This is an abstract method that should be implemented in a
            subclass.

        """
        self._pre_search_validation(location, query, sort_by, return_fields,
                                    max_features)

        exclude_empty_filters = Not([PropertyIsNull(
                                     propertyname='pkey_filter')])

        if query is not None:
            query = And([query, exclude_empty_filters])
        else:
            query = exclude_empty_filters

        return super().search(
            location=location, query=query, sort_by=sort_by,
            return_fields=return_fields, max_features=max_features)
