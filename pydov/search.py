# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV data."""

import pandas as pd
from owslib.wfs import WebFeatureService

from pydov.types import Boring
from pydov.util import owsutil
from pydov.util.errors import (
    LayerNotFoundError,
    InvalidSearchParameterError,
)


class AbstractSearch(object):
    __wfs = None

    def __init__(self, layer, type):
        self._layer = layer
        self._type = type
        self._source_df_map = {}
        self._fields = None

    @staticmethod
    def _init_wfs():
        if AbstractSearch.__wfs is None:
            AbstractSearch.__wfs = WebFeatureService(
                url="https://www.dov.vlaanderen.be/geoserver/wfs",
                version="1.1.0")

    @staticmethod
    def _get_layer(layer):
        AbstractSearch._init_wfs()

        if layer not in AbstractSearch.__wfs.contents:
            raise LayerNotFoundError('Layer %s could not be found' % layer)
        else:
            return AbstractSearch.__wfs.contents[layer]

    @staticmethod
    def _get_schema(layer):
        AbstractSearch._init_wfs()
        layername = layer.split(':')[1] if ':' in layer else layer
        return AbstractSearch.__wfs.get_schema(layername)

    @staticmethod
    def _get_namespace(layer):
        AbstractSearch._init_wfs()
        return owsutil.get_namespace(AbstractSearch.__wfs, layer)

    def _get_remote_metadata(self, layer):
        wfs_layer = self._get_layer(layer)
        return owsutil.get_remote_metadata(wfs_layer)

    def _get_csw_base_url(self, layer):
        wfs_layer = self._get_layer(layer)
        return owsutil.get_csw_base_url(wfs_layer)

    def _build_fields_old(self, wfs_schema, fc):
        fields = {}
        for wfs_field in wfs_schema['properties'].keys():
            if wfs_field in fc['attributes']:
                fc_field = fc['attributes'][wfs_field]
                name = self._source_df_map.get(wfs_field, wfs_field)
                field = {'name': name,
                         'definition': fc_field['definition'],
                         'type': wfs_schema['properties'][wfs_field],
                         'notnull': fc_field['multiplicity'][0] > 0}
                if fc_field['values'] is not None:
                    stripped_values = [v.strip() for v in fc_field['values']
                                       if len(v.strip()) > 0]
                    if len(stripped_values) > 0:
                        field['values'] = stripped_values
                fields[name] = field
        return fields

    def _build_fields(self, wfs_schema, fc):
        fields = {}

        df_wfs_fields = self._type.get_fields(source=('wfs',))
        map_wfs_source_df = {}
        for k in df_wfs_fields:
            map_wfs_source_df[df_wfs_fields[k]['sourcefield']] = k

        for wfs_field in wfs_schema['properties'].keys():
            if wfs_field in fc['attributes']:
                fc_field = fc['attributes'][wfs_field]

                name = map_wfs_source_df.get(wfs_field, wfs_field)

                field = {
                    'name': name,
                    'definition': fc_field['definition'],
                    'type': wfs_schema['properties'][wfs_field],
                    'notnull': fc_field['multiplicity'][0] > 0,
                    'cost': 1
                }

                if fc_field['values'] is not None:
                    stripped_values = [v.strip() for v in fc_field['values']
                                       if len(v.strip()) > 0]
                    if len(stripped_values) > 0:
                        field['values'] = stripped_values
                fields[name] = field

        for xml_field in self._type.get_fields(source=['xml']).values():
            field = {
                'name': xml_field['name'],
                'type': xml_field['type'],
                'definition': xml_field['definition'],
                'notnull': xml_field['notnull'],
                'cost': 10
            }
            fields[field['name']] = field

        return fields

    def get_description(self, layer):
        wfs_layer = self._get_layer(layer)
        return wfs_layer.abstract

    def get_fields(self):
        self._init_fields()
        return self._fields

    def _pre_search_validation(self, layer, location=None, query=None,
                               return_fields=None):
        if location is None and query is None:
            raise InvalidSearchParameterError('Provide at least the '
                                              'location or the query '
                                              'parameter.')

        if return_fields is not None:
            self._init_fields()
            for rf in return_fields:
                if rf not in self._fields:
                    if rf in self._source_df_map:
                        raise InvalidSearchParameterError(
                            "Unkown return field: '%s'. Did you mean '%s'?"
                            % (rf, self._source_df_map[rf]))
                    raise InvalidSearchParameterError(
                        "Unknown return field: '%s'" % rf)

    def search(self, layer, location=None, query=None, return_fields=None):
        if location is not None:
            AbstractSearch._init_wfs()
            fts = AbstractSearch.__wfs.getfeature(typename=layer,
                                                  bbox=location).read()
            return fts


class BoringSearch(AbstractSearch):
    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None

    def __init__(self):
        super(BoringSearch, self).__init__('dov-pub:Boringen', Boring)

        self._source_df_map = {}
        m = self._type.get_fields(source=('wfs',))
        for k in m:
            self._source_df_map[m[k]['sourcefield']] = k

    def _init_namespace(self):
        if BoringSearch.__wfs_namespace is None:
            BoringSearch.__wfs_namespace = self._get_namespace(self._layer)

    def _init_fields(self):
        if self._fields is None:
            if BoringSearch.__wfs_schema is None:
                BoringSearch.__wfs_schema = self._get_schema(self._layer)

            if BoringSearch.__md_metadata is None:
                BoringSearch.__md_metadata = self._get_remote_metadata(
                    self._layer)

            if BoringSearch.__fc_featurecatalogue is None:
                csw_url = self._get_csw_base_url(self._layer)
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    BoringSearch.__md_metadata)

                BoringSearch.__fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            self._fields = self._build_fields(
                BoringSearch.__wfs_schema, BoringSearch.__fc_featurecatalogue)

    def get_description(self):
        return super(BoringSearch, self).get_description(self._layer)

    def search(self, location=None, query=None, return_fields=None):
        self._pre_search_validation(self._layer, location, query,
                                    return_fields)

        fts = super(BoringSearch, self).search(layer=self._layer,
                                               location=location,
                                               query=query,
                                               return_fields=return_fields)

        self._init_namespace()
        boringen = Boring.from_wfs(fts, self.__wfs_namespace)

        df = pd.DataFrame(data=Boring.to_df_array(boringen),
                          columns=Boring.get_columns())
        return df


if __name__ == '__main__':
    b = BoringSearch()
    print(b.get_fields())
    df = b.search(location=(115021, 196339, 118120, 197925))
    print(df)
