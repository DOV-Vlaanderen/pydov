# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV data."""

from owslib.wfs import WebFeatureService

from pydov.util.errors import LayerNotFoundError
from pydov.util import owsutil


class AbstractSearch(object):
    __wfs = None

    def __init__(self):
        self.fields = None

    @staticmethod
    def init_wfs():
        if AbstractSearch.__wfs is None:
            AbstractSearch.__wfs = WebFeatureService(
                url="https://www.dov.vlaanderen.be/geoserver/wms",
                version="1.1.0")

    @staticmethod
    def _get_layer(layer):
        AbstractSearch.init_wfs()

        if layer not in AbstractSearch.__wfs.contents:
            raise LayerNotFoundError('Layer %s could not be found' % layer)
        else:
            return AbstractSearch.__wfs.contents[layer]

    @staticmethod
    def _get_schema(layer):
        AbstractSearch.init_wfs()
        layername = layer.split(':')[1] if ':' in layer else layer
        return AbstractSearch.__wfs.get_schema(layername)

    def _get_remote_metadata(self, layer):
        wfs_layer = self._get_layer(layer)
        return owsutil.get_remote_metadata(wfs_layer)

    def _get_csw_base_url(self, layer):
        wfs_layer = self._get_layer(layer)
        return owsutil.get_csw_base_url(wfs_layer)

    def _build_fields(self, wfs_schema, fc):
        fields = {}
        for attr in wfs_schema['properties'].keys():
            if attr in fc['attributes']:
                attrft = fc['attributes'][attr]
                field = {'name': attr,
                         'definition': attrft['definition'],
                         'type': wfs_schema['properties'][attr]}
                if attrft['values'] is not None:
                    stripped_values = [v.strip() for v in attrft['values']
                                       if len(v.strip()) > 0]
                    if len(stripped_values) > 0:
                        field['values'] = stripped_values
                fields[attr] = field
        return fields

    def get_description(self, layer):
        wfs_layer = self._get_layer(layer)
        return wfs_layer.abstract

    def get_fields(self, layer):
        return NotImplementedError


class BoringSearch(AbstractSearch):
    __wfs_schema = None
    __md_metadata = None
    __fc_featurecatalogue = None

    def __init__(self):
        super(BoringSearch, self).__init__()
        self.__layer = 'dov-pub:Boringen'

    def get_description(self):
        return super(BoringSearch, self).get_description(self.__layer)

    def get_fields(self):
        if self.fields is not None:
            return self.fields

        if BoringSearch.__wfs_schema is None:
            BoringSearch.__wfs_schema = self._get_schema(self.__layer)

        if BoringSearch.__md_metadata is None:
            BoringSearch.__md_metadata = self._get_remote_metadata(
                self.__layer)

        if BoringSearch.__fc_featurecatalogue is None:
            csw_url = self._get_csw_base_url(self.__layer)
            fc_uuid = owsutil.get_featurecatalogue_uuid(
                BoringSearch.__md_metadata)

            BoringSearch.__fc_featurecatalogue = \
                owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

        self.fields = self._build_fields(
            BoringSearch.__wfs_schema, BoringSearch.__fc_featurecatalogue)

        return self.fields

    def search(self, location=None, query=None, return_fields=None):
        if location is None and query is None:
            return AttributeError

        # return dataframe
        return NotImplementedError


if __name__ == '__main__':
    for i in range(10):
        b = BoringSearch()
        fields = b.get_fields()
        print(fields)
