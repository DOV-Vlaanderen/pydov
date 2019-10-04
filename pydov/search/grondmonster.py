# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV borehole data."""
import pandas as pd

from pydov.search.abstract import AbstractSearch
from pydov.types.fields import _WfsInjectedField
from pydov.types.grondmonster import Grondmonster
from pydov.util import owsutil


class GrondmonsterSearch(AbstractSearch):
    """Search class to retrieve the grain size distribution of
    ground samples ('grondmonster')"""

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self, objecttype=Grondmonster):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Grondmonster type.
            Optional: defaults to the Grondmonster type containing the fields
            described in the documentation.

        """
        super(GrondmonsterSearch, self).\
            __init__('boringen:grondmonsters', objecttype)

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer."""
        if GrondmonsterSearch.__wfs_namespace is None:
            GrondmonsterSearch.__wfs_namespace = self._get_namespace()

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class."""
        if self._fields is None:
            if GrondmonsterSearch.__wfs_schema is None:
                GrondmonsterSearch.__wfs_schema = self._get_schema()

            if GrondmonsterSearch.__md_metadata is None:
                GrondmonsterSearch.__md_metadata = \
                    self._get_remote_metadata()

            if GrondmonsterSearch.__fc_featurecatalogue is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    GrondmonsterSearch.__md_metadata)

                GrondmonsterSearch.__fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            if GrondmonsterSearch.__xsd_schemas is None:
                GrondmonsterSearch.__xsd_schemas = \
                    self._get_remote_xsd_schemas()

            fields = self._build_fields(
                GrondmonsterSearch.__wfs_schema,
                GrondmonsterSearch.__fc_featurecatalogue,
                GrondmonsterSearch.__xsd_schemas)

            for field in fields.values():
                if field['name'] not in self._type.get_field_names(
                        include_wfs_injected=True):
                    self._type.fields.append(
                        _WfsInjectedField(name=field['name'],
                                          datatype=field['type']))

            self._fields = self._build_fields(
                GrondmonsterSearch.__wfs_schema,
                GrondmonsterSearch.__fc_featurecatalogue,
                GrondmonsterSearch.__xsd_schemas)

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        """Search for ground samples (Grondmonster). Provide either
        `location` or `query`. When `return_fields` is None,
        all fields are returned.

        Parameters
        ----------
        location : pydov.util.location.AbstractLocationFilter or \
                    owslib.fes.BinaryLogicOpType<AbstractLocationFilter> or \
                    owslib.fes.UnaryLogicOpType<AbstractLocationFilter>
            Location filter limiting the features to retrieve. Can either be a
            single instance of a subclass of AbstractLocationFilter, or a
            combination using And, Or, Not of AbstractLocationFilters.
        query : owslib.fes.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        sort_by : owslib.fes.SortBy, optional
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
            When not one of `location`, `query` or `max_features` is provided.

        pydov.util.errors.InvalidFieldError
            When at least one of the fields in `return_fields` is unknown.

            When a field that is only accessible as return field is used as
            a query parameter.

            When a field that can only be used as a query parameter is used as
            a return field.

        pydov.util.errors.FeatureOverflowError
            When the number of features to be returned is equal to the
            maxFeatures limit of the WFS server.

        AttributeError
            When the argument supplied as return_fields is not a list,
            tuple or set.

        """
        self._pre_search_validation(location, query, sort_by, return_fields,
                                    max_features)

        fts = self._search(location=location, query=query, sort_by=sort_by,
                           return_fields=return_fields,
                           max_features=max_features)

        grondmonster = self._type.from_wfs(fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=self._type.to_df_array(grondmonster, return_fields),
            columns=self._type.get_field_names(return_fields))
        return df
