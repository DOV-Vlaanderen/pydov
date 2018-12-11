# -*- coding: utf-8 -*-
"""Module containing the abstract search classes to retrieve DOV data."""

import owslib
import pydov
from owslib.etree import etree
from owslib.fes import (
    FilterRequest,
    Or,
    PropertyIsEqualTo,
)
from owslib.wfs import WebFeatureService
from pydov.util import owsutil
from pydov.util.errors import (
    LayerNotFoundError,
    InvalidSearchParameterError,
    FeatureOverflowError,
    InvalidFieldError,
)
from ..util.owsutil import get_remote_schema


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
        self._wfs_fields = None
        self._geometry_column = None

        self._map_wfs_source_df = {}
        self._map_df_wfs_source = {}

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
        return get_remote_schema(
            'https://www.dov.vlaanderen.be/geoserver/wfs', layername)

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
        self._wfs_fields = []
        self._geometry_column = wfs_schema.get('geometry_column', None)

        _map_wfs_datatypes = {
            'int': 'integer',
            'decimal': 'float',
            'double': 'float'
        }

        df_wfs_fields = self._type.get_fields(source=('wfs',)).values()
        for f in df_wfs_fields:
            self._map_wfs_source_df[f['sourcefield']] = f['name']
            self._map_df_wfs_source[f['name']] = f['sourcefield']

        for wfs_field in wfs_schema['properties'].keys():
            if wfs_field in feature_catalogue['attributes']:
                fc_field = feature_catalogue['attributes'][wfs_field]
                self._wfs_fields.append(wfs_field)

                name = self._map_wfs_source_df.get(wfs_field, wfs_field)

                field = {
                    'name': name,
                    'definition': fc_field['definition'],
                    'type': _map_wfs_datatypes.get(
                        wfs_schema['properties'][wfs_field],
                        wfs_schema['properties'][wfs_field]),
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

        for custom_field in self._type.get_fields(source=['custom']).values():
            field = {
                'name': custom_field['name'],
                'type': custom_field['type'],
                'definition': custom_field['definition'],
                'notnull': custom_field['notnull'],
                'cost': 1
            }
            fields[field['name']] = field

        return fields

    def _pre_search_validation(self, location=None, query=None,
                               return_fields=None):
        """Perform validation on the parameters of the search query.

        Parameters
        ----------
        location : tuple<minx,miny,maxx,maxy>
            The bounding box limiting the features to retrieve.
        query : owslib.fes.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        return_fields : list<str> or tuple<str> or set<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`.

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not one of `location` or `query` is provided.

        pydov.util.errors.InvalidFieldError
            When at least one of the fields in `return_fields` is unknown.

            When a field that is only accessible as return field is used as
            a query parameter.

        """
        if location is None and query is None:
            raise InvalidSearchParameterError(
                'Provide either the location or the query parameter.'
            )

        if query is not None:
            if not isinstance(query, owslib.fes.OgcExpression):
                raise InvalidSearchParameterError(
                    "Query should be an owslib.fes.OgcExpression.")

            filter_request = FilterRequest()
            filter_request = filter_request.setConstraint(query)

            self._init_fields()
            for property_name in filter_request.findall(
                    './/{http://www.opengis.net/ogc}PropertyName'):
                name = property_name.text
                if name not in self._map_df_wfs_source \
                        and name not in self._wfs_fields:
                    if name in self._fields:
                        raise InvalidFieldError(
                            "Cannot use return field '%s' in query." % name
                        )
                    raise InvalidFieldError(
                        "Unknown query parameter: '%s'" % name)

        if location is not None:
            self._init_fields()

        if return_fields is not None:
            if type(return_fields) not in (list, tuple, set):
                raise AttributeError('return_fields should be a list, '
                                     'tuple or set')

            self._init_fields()
            for rf in return_fields:
                if rf not in self._fields:
                    if rf in self._map_wfs_source_df:
                        raise InvalidFieldError(
                            "Unknown return field: '%s'. Did you mean '%s'?"
                            % (rf, self._map_wfs_source_df[rf]))
                    if rf.lower() in [i.lower() for i in
                                      self._map_wfs_source_df.keys()]:
                        sugg = [i for i in self._map_wfs_source_df.keys() if
                                i.lower() == rf.lower()][0]
                        raise InvalidFieldError(
                            "Unknown return field: '%s'. Did you mean '%s'?"
                            % (rf, sugg))
                    raise InvalidFieldError(
                        "Unknown return field: '%s'" % rf)

    @staticmethod
    def _get_remote_wfs_feature(wfs, typename, bbox, filter, propertyname,
                                geometry_column):
        """Perform the WFS GetFeature call to get features from the remote
        service.

        Parameters
        ----------
        typename : str
            Layername to query.
        bbox : tuple<minx,miny,maxx,maxy>
            The bounding box limiting the features to retrieve.
        filter : owslib.fes.FilterRequest
            Filter request to search on attribute values.
        propertyname : list<str>
            List of properties to return.
        geometry_column : str
            Name of the geometry column to use in the spatial filter.

        Returns
        -------
        bytes
            Response of the WFS service.

        """
        wfs_getfeature_xml = owsutil.wfs_build_getfeature_request(
            version=wfs.version,
            geometry_column=geometry_column,
            typename=typename,
            bbox=bbox,
            filter=filter,
            propertyname=propertyname
        )

        for hook in pydov.hooks:
            hook.wfs_search_init(typename)

        return owsutil.wfs_get_feature(
            baseurl=wfs.url,
            get_feature_request=wfs_getfeature_xml
        )

    def _search(self, location=None, query=None, return_fields=None,
                extra_wfs_fields=[]):
        """Perform the WFS search by issuing a GetFeature request.

        Parameters
        ----------
        location : tuple<minx,miny,maxx,maxy>
            The bounding box limiting the features to retrieve.
        query : owslib.fes.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        return_fields : list<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.
        extra_wfs_fields: list<str>
            A list of extra fields to be included in the WFS requests,
            regardless whether they're needed as return field. Optional,
            defaults to an empty list.

        Returns
        -------
        etree.Element
            XML tree of the WFS response containing the features matching
            the location or the query.

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

        """
        self._pre_search_validation(location, query, return_fields)
        self._init_namespace()
        self._init_wfs()

        filter_request = None
        if query is not None:
            filter_request = FilterRequest()
            filter_request = filter_request.setConstraint(query)

        if filter_request is not None:
            for property_name in filter_request.findall(
                    './/{http://www.opengis.net/ogc}PropertyName'):
                property_name.text = self._map_df_wfs_source.get(
                    property_name.text, property_name.text)

            try:
                filter_request = etree.tostring(filter_request,
                                                encoding='unicode')
            except LookupError:
                # Python2.7 without lxml uses 'utf-8' instead.
                filter_request = etree.tostring(filter_request,
                                                encoding='utf-8')

        if return_fields is None:
            wfs_property_names = [
                f['sourcefield'] for f in self._type.get_fields(
                    source=('wfs',)).values() if not f.get(
                    'wfs_injected', False)]
        else:
            wfs_property_names = [self._map_df_wfs_source[i]
                                  for i in self._map_df_wfs_source
                                  if i.startswith('pkey')]
            wfs_property_names.extend([self._map_df_wfs_source[i]
                                       for i in self._map_df_wfs_source
                                       if i in return_fields])

        wfs_property_names.extend(extra_wfs_fields)
        wfs_property_names = list(set(wfs_property_names))

        fts = self._get_remote_wfs_feature(
            wfs=self.__wfs,
            typename=self._layer,
            bbox=location,
            filter=filter_request,
            propertyname=wfs_property_names,
            geometry_column=self._geometry_column)

        tree = etree.fromstring(fts)

        if int(tree.get('numberOfFeatures')) == 10000:
            raise FeatureOverflowError(
                'Reached the limit of %i returned features. Please split up '
                'the query to ensure getting all results.' % 10000)

        for hook in pydov.hooks:
            hook.wfs_search_result(int(tree.get('numberOfFeatures')))

        return tree

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

            Optionally, it can contain:

            values (list)
                A list of possible values for this field.

        """
        self._init_fields()
        return self._fields
