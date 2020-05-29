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
        if GrondmonsterSearch.__wfs_namespace is None:
            GrondmonsterSearch.__wfs_namespace = self._get_namespace()

    def _init_fields(self):
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
