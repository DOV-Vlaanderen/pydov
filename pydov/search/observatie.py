# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV observation data."""
from ..types.observatie import Observatie, Fractiemeting
from .abstract import AbstractSearch

from owslib.fes2 import PropertyIsEqualTo, And


class ObservatieSearch(AbstractSearch):
    """Search class to retrieve information about observations (Observatie).

    This will return observations of any type.
    """

    def __init__(self, objecttype=Observatie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Observatie type.
            Optional: defaults to the Observatie type containing the fields
            described in the documentation.

        """
        super(ObservatieSearch, self).__init__(
            'monster:observaties', objecttype)


class ObservatieFractiemetingSearch(ObservatieSearch):
    """Search class to retrieve information about fraction measurements.

    This will return only observation of type 'Textuurmeting' and will
    by default include the fields of the Fractiemeting subtype
    """

    def __init__(self, objecttype=Observatie.with_subtype(Fractiemeting)):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Observatie type.
            Optional: defaults to the Observatie type containing the fields
            described in the documentation.

        """
        super(ObservatieFractiemetingSearch, self).__init__(objecttype)

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        """Search for objects of this type. Provide `location` and/or
        `query` and/or `max_features`.
        When `return_fields` is None, all fields are returned.

        Will return only observations of type 'Textuurmeting', by
        extending the query with a filter on the `observatietype` field.

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

        observatietype_filter = PropertyIsEqualTo(
            'observatietype', 'Textuurmeting')

        if query is not None:
            query = And([query, observatietype_filter])
        else:
            query = observatietype_filter

        omitted_fields = ['resultaat', 'detectieconditie']
        if return_fields is None:
            return_fields = [
                f for f in self._type.get_field_names()
                if f not in omitted_fields
            ]

        return super().search(
            location=location, query=query, sort_by=sort_by,
            return_fields=return_fields, max_features=max_features)
