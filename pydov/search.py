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
    """Abstract search class grouping methods common to all DOV search
    classes. Not to be instantiated or used directly."""

    __wfs = None

    def __init__(self, layer, objecttype):
        """Initialisation.

        Parameters
        ----------
        layer : str
            WFS layer to use for searching and retrieving records.
        objecttype : pydov.types.AbstractDovType
            Subclass of AbstractDovType indicating the associated DOV datatype.

        """
        self._layer = layer
        self._type = objecttype
        self._fields = None
        self._map_wfs_source_df = {}

    def _init_wfs(self):
        """Initialise the WFS service. If the WFS service is not
        instanciated yet, do so and save it in a static variable available
        to all subclasses and instances.
        """
        if AbstractSearch.__wfs is None:
            AbstractSearch.__wfs = WebFeatureService(
                url="https://www.dov.vlaanderen.be/geoserver/wfs",
                version="1.1.0")

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer.

        Raises
        ------
        NotImplementedError
            This is an abstract method that should be implemented in a
            subclass.

        """
        raise NotImplementedError('This should be implemented in a subclass.')

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class.

        Raises
        ------
        NotImplementedError
            This is an abstract method that should be implemented in a
            subclass.

        """
        raise NotImplementedError('This should be implemented in a subclass.')

    def _get_layer(self):
        """Get the WFS metadata for the layer.

        Returns
        -------
        owslib.feature.wfs110.ContentMetadata
            Content metadata describing the layer.

        Raises
        ------
        pydov.util.errors.LayerNotFoundError
            When the layer of this search class could not be found in the
            associated WFS service.

        """
        self._init_wfs()

        if self._layer not in self.__wfs.contents:
            raise LayerNotFoundError('Layer %s could not be found' %
                                     self._layer)
        else:
            return self.__wfs.contents[self._layer]

    def _get_schema(self):
        """Get the WFS schema (i.e. the output of the DescribeFeatureType
        request) of the layer.

        Returns
        -------
        schema : dict
            Schema associated with the layer.

        """
        self._init_wfs()
        layername = self._layer.split(':')[1] if ':' in self._layer else \
            self._layer
        return self.__wfs.get_schema(layername)

    def _get_namespace(self):
        """Get the WFS namespace of the layer.

        Returns
        -------
        namespace : str
            The namespace associated with the WFS layer. This is the
            namespace of the fields of this layer, needed to parse the
            output of a GetFeature request.

        """
        self._init_wfs()
        return owsutil.get_namespace(self.__wfs, self._layer)

    def _get_remote_metadata(self):
        """Request and parse the remote metadata associated with the layer.

        Returns
        -------
        owslib.iso.MD_Metadata
            Parsed remote metadata describing the WFS layer in more detail,
            in the ISO 19115/19139 format.

        """
        wfs_layer = self._get_layer()
        return owsutil.get_remote_metadata(wfs_layer)

    def _get_csw_base_url(self):
        """Get the CSW base url for the remote metadata associated with the
        layer.

        Returns
        -------
        url : str
            Base URL of the CSW service where the remote metadata and feature
            catalogue can be requested.

        """
        wfs_layer = self._get_layer()
        return owsutil.get_csw_base_url(wfs_layer)

    def _build_fields(self, wfs_schema, feature_catalogue):
        """Build the dictionary containing the metadata about the available
        fields.

        Parameters
        ----------
        wfs_schema : dict
            The schema associated with the WFS layer.
        feature_catalogue : dict
            Dictionary with fields described in the feature catalogue,
            as returned by pydov.util.owsutil.get_remote_featurecatalogue.

        Returns
        -------
        fields : dict<str,dict>
            Dictionary containing the metadata of the available fields,
            where the metadata dictionary includes:

            name (str)
                The name of the field.

            definition (str)
                The definition of the field.

            type (str)
                The datatype of the field.

            notnull (boolean)
                Whether the field is mandatory (True) or can be null (False).

            cost (integer)
                The cost associated with the request of this field in the
                output dataframe.

        """
        fields = {}

        df_wfs_fields = self._type.get_fields(source=('wfs',)).values()
        for f in df_wfs_fields:
            self._map_wfs_source_df[f['sourcefield']] = f['name']

        for wfs_field in wfs_schema['properties'].keys():
            if wfs_field in feature_catalogue['attributes']:
                fc_field = feature_catalogue['attributes'][wfs_field]

                name = self._map_wfs_source_df.get(wfs_field, wfs_field)

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

    def _pre_search_validation(self, location=None, query=None,
                               return_fields=None):
        """Perform validation on the parameters of the search query.

        Parameters
        ----------
        location : tuple<minx,maxx,miny,maxy>
            The bounding box limiting the features to retrieve.
        query : TODO
            TODO
        return_fields : TODO
            TODO

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not at least one of `location` or `query` is provided.

            When at least one of the field in `return_fields` is unknown.

        """
        if location is None and query is None:
            raise InvalidSearchParameterError(
                'Provide at least the location or the query parameter.')

        if return_fields is not None:
            self._init_fields()
            for rf in return_fields:
                if rf not in self._fields:
                    if rf in self._map_wfs_source_df:
                        raise InvalidSearchParameterError(
                            "Unkown return field: '%s'. Did you mean '%s'?"
                            % (rf, self._map_wfs_source_df[rf]))
                    raise InvalidSearchParameterError(
                        "Unknown return field: '%s'" % rf)

    def _search(self, location=None, query=None, return_fields=None):
        """Perform the WFS search by issuing a GetFeature request.

        Parameters
        ----------
        location : tuple<minx,maxx,miny,maxy>
            The bounding box limiting the features to retrieve.
        query : TODO
            TODO
        return_fields : TODO
            TODO

        Returns
        -------
        file like
            The WFS response containing the features matching the location
            and the query.

        """
        self._pre_search_validation(location, query, return_fields)
        self._init_namespace()

        if location is not None:  # FIXME
            self._init_wfs()
            fts = self.__wfs.getfeature(typename=self._layer,
                                        bbox=location).read()
            return fts

    def get_description(self):
        """Get the description of this search layer.

        Returns
        -------
        str
            The description of this layer.

        """
        wfs_layer = self._get_layer()
        return wfs_layer.abstract

    def get_fields(self):
        """Get the metadata of the fields that are available.

        Returns
        -------
        fields : dict<str,dict>
            Dictionary containing the metadata of the available fields,
            where the metadata dictionary includes:

            name (str)
                The name of the field.

            definition (str)
                The definition of the field.

            type (str)
                The datatype of the field.

            notnull (boolean)
                Whether the field is mandatory (True) or can be null (False).

            cost (integer)
                The cost associated with the request of this field in the
                output dataframe.

        """
        self._init_fields()
        return self._fields


class BoringSearch(AbstractSearch):
    """Search class to retrieve information about boreholes (Boring)."""

    __wfs_schema = None
    __wfs_namespace = None
    __md_metadata = None
    __fc_featurecatalogue = None

    def __init__(self):
        """Initialisation."""
        super(BoringSearch, self).__init__('dov-pub:Boringen', Boring)

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer."""
        if BoringSearch.__wfs_namespace is None:
            BoringSearch.__wfs_namespace = self._get_namespace()

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class."""
        if self._fields is None:
            if BoringSearch.__wfs_schema is None:
                BoringSearch.__wfs_schema = self._get_schema()

            if BoringSearch.__md_metadata is None:
                BoringSearch.__md_metadata = self._get_remote_metadata()

            if BoringSearch.__fc_featurecatalogue is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(
                    BoringSearch.__md_metadata)

                BoringSearch.__fc_featurecatalogue = \
                    owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            self._fields = self._build_fields(
                BoringSearch.__wfs_schema, BoringSearch.__fc_featurecatalogue)

    def search(self, location=None, query=None, return_fields=None):
        """Search for boreholes (Boring). Provide at least one of `location`
        or `query`. When `return_fields` is None, all fields are returned.

        Parameters
        ----------
        location : tuple<minx,maxx,miny,maxy>
            The bounding box limiting the features to retrieve.
        query : TODO
            TODO
        return_fields : TODO
            TODO

        Returns
        -------
        df : pandas.core.frame.DataFrame
            DataFrame containing the information about the boreholes (Boring)
            that match the search query.

        """
        fts = self._search(location=location, query=query,
                           return_fields=return_fields)

        boringen = Boring.from_wfs(fts, self.__wfs_namespace)

        df = pd.DataFrame(data=Boring.to_df_array(boringen),
                          columns=Boring.get_field_names())
        return df


if __name__ == '__main__':
    for i in range(10):
        b = BoringSearch()
        print(b.get_fields())

    b = BoringSearch()
    print(b.get_description())
    df = b.search(location=(115021, 196339, 118120, 197925))
    print(df)
