# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV CPT data."""
import pandas as pd

from pydov.search.abstract import AbstractSearch
from pydov.types.sondering import Sondering
from pydov.util import owsutil


class SonderingSearch(AbstractSearch):
    """Search class to retrieve information about CPT measurements (
    Sonderingen)."""

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self):
        """Initialisation."""
        super(SonderingSearch, self).__init__('dov-pub:Sonderingen', Sondering)

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer."""
        if SonderingSearch.__wfs_namespace is None:
            SonderingSearch.__wfs_namespace = self._get_namespace()

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class."""
        if self._fields is None:
            if SonderingSearch.__wfs_schema is None:
                SonderingSearch.__wfs_schema = self._get_schema()

            if SonderingSearch.__md_metadata is None:
                SonderingSearch.__md_metadata = self._get_remote_metadata()

            if SonderingSearch.__fc_featurecatalogue is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    SonderingSearch.__md_metadata)

                SonderingSearch.__fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            if SonderingSearch.__xsd_schemas is None:
                SonderingSearch.__xsd_schemas = \
                    self._get_remote_xsd_schemas()

            fields = self._build_fields(
                SonderingSearch.__wfs_schema,
                SonderingSearch.__fc_featurecatalogue,
                SonderingSearch.__xsd_schemas)

            for field in fields.values():
                if field['name'] not in self._type.get_field_names(
                        include_wfs_injected=True):
                    self._type._fields.append({
                        'name': field['name'],
                        'source': 'wfs',
                        'sourcefield': field['name'],
                        'type': field['type'],
                        'wfs_injected': True
                    })

            self._fields = self._build_fields(
                SonderingSearch.__wfs_schema,
                SonderingSearch.__fc_featurecatalogue,
                SonderingSearch.__xsd_schemas)

    def search(self, location=None, query=None, return_fields=None):
        """Search for CPT measurements (Sondering). Provide `location` and/or
        `query`. When `return_fields` is None, all fields are returned.

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
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.

        Returns
        -------
        pandas.core.frame.DataFrame
            DataFrame containing the output of the search query.

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not one of `location` or `query` is provided.

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
        fts = self._search(location=location, query=query,
                           return_fields=return_fields)

        sonderingen = Sondering.from_wfs(fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=Sondering.to_df_array(sonderingen, return_fields),
            columns=Sondering.get_field_names(return_fields))
        return df
