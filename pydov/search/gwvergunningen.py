# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve permit data."""
import pandas as pd

from pydov.search.abstract import AbstractSearch
from pydov.types.fields import _WfsInjectedField
from pydov.types.gwvergunningen import Gwvergunningen
from pydov.util import owsutil


class GwvergunningenSearch(AbstractSearch):
    """Search class to retrieve information about Gw permits (
    Sonderingen)."""

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None
    __xsd_schemas = None

    def __init__(self, objecttype=Gwvergunningen):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Gwvergunningen type.
            Optional: defaults to the Gwvergunningen type containing
            the fields described in the documentation.

        """
        super(GwvergunningenSearch, self).__init__(
            'gw_vergunningen:alle_verg', objecttype)

    def _init_namespace(self):
        if GwvergunningenSearch.__wfs_namespace is None:
            GwvergunningenSearch.__wfs_namespace = self._get_namespace()

    def _init_fields(self):
        if self._fields is None:
            if GwvergunningenSearch.__wfs_schema is None:
                GwvergunningenSearch.__wfs_schema = self._get_schema()

            if GwvergunningenSearch.__md_metadata is None:
                GwvergunningenSearch.__md_metadata = self._get_remote_metadata()

            if GwvergunningenSearch.__fc_featurecatalogue is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    GwvergunningenSearch.__md_metadata)

                GwvergunningenSearch.__fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            if GwvergunningenSearch.__xsd_schemas is None:
                GwvergunningenSearch.__xsd_schemas = \
                    self._get_remote_xsd_schemas()

            fields = self._build_fields(
                GwvergunningenSearch.__wfs_schema,
                GwvergunningenSearch.__fc_featurecatalogue,
                GwvergunningenSearch.__xsd_schemas)

            for field in fields.values():
                if field['name'] not in self._type.get_field_names(
                        include_wfs_injected=True):
                    self._type.fields.append(
                        _WfsInjectedField(name=field['name'],
                                          datatype=field['type']))

            self._fields = self._build_fields(
                GwvergunningenSearch.__wfs_schema,
                GwvergunningenSearch.__fc_featurecatalogue,
                GwvergunningenSearch.__xsd_schemas)

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        fts = self._search(location=location, query=query, sort_by=sort_by,
                           return_fields=return_fields,
                           max_features=max_features)

        Gwvergunningen = self._type.from_wfs(fts, self.__wfs_namespace)

        df = pd.DataFrame(
            data=self._type.to_df_array(Gwvergunningen, return_fields),
            columns=self._type.get_field_names(return_fields))
        return df
