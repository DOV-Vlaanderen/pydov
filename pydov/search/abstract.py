# -*- coding: utf-8 -*-
"""Module containing the abstract search classes to retrieve DOV data."""

from itertools import chain
import datetime
import math
import warnings
import re

import owslib
import owslib.fes2
from owslib.etree import etree
from owslib.feature import get_schema
from owslib.fes2 import FilterRequest
from owslib.wfs import WebFeatureService
import pandas as pd
import numpy as np

import pydov
from pydov.types.fields import (_WfsInjectedField, GeometryReturnField,
                                ReturnFieldList)
from pydov.util import owsutil
from pydov.util.dovutil import build_dov_url, get_xsd_schema
from pydov.util.errors import (InvalidFieldError, InvalidSearchParameterError,
                               LayerNotFoundError, WfsGetFeatureError,
                               DataParseWarning)
from pydov.util.hooks import HookRunner
from pydov.util.net import LocalSessionThreadPool

# compile regex for matching datetime
re_datetime = re.compile(
    r'([0-9]{4}-[0-9]{2}-[0-9]{2}T'
    r'[0-9]{2}:[0-9]{2}:[0-9]{2})'
    r'(\.[0-9]+)?([\+\-][0-9]{2}:?[0-9]{2})?(Z?)')


class AbstractCommon(object):
    """Class grouping methods common to AbstractSearch and
    AbstractTypeCommon."""

    @classmethod
    def __strtobool(cls, val):
        """Convert a string representation of truth to true (1) or false (0).

        True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
        are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
        'val' is anything else.

        Parameters
        ----------
        val : str
            String representation to convert to boolean.

        Returns
        -------
        boolean
            The converted boolean value.

        Raises
        ------
        ValueError
            If the string cannot be converted to a boolean value.
        """
        val = val.lower()
        if val in ('y', 'yes', 't', 'true', 'on', '1'):
            return True
        elif val in ('n', 'no', 'f', 'false', 'off', '0'):
            return False
        else:
            raise ValueError(
                "Cannot convert truth value %r to boolean." % (val,))

    @classmethod
    def _typeconvert(cls, text, returntype):
        """Parse the text to the given returntype.

        Parameters
        ----------
        text : str
           Text to convert
        returntype : str
            Parse the text to this output datatype. One of
            `string`, `float`, `integer`, `date`, `datetime`, `boolean`.

        Returns
        -------
        str or float or int or bool or datetime.date or datetime.datetime
            Returns the parsed text converted to the type described by
            `returntype`.

        """
        if returntype == 'string':
            def typeconvert(x):
                return u'' + (x.strip())
        elif returntype == 'integer':
            def typeconvert(x):
                return int(x)
        elif returntype == 'float':
            def typeconvert(x):
                return float(x)
        elif returntype == 'date':
            def typeconvert(x):
                # Patch for Zulu-time issue of geoserver for WFS 1.1.0
                if x.endswith('Z'):
                    return datetime.datetime.strptime(x, '%Y-%m-%dZ').date() \
                        + datetime.timedelta(days=1)
                else:
                    return datetime.datetime.strptime(x, '%Y-%m-%d').date()
        elif returntype == 'datetime':
            def typeconvert(x):
                x_match = re_datetime.search(x)
                if x_match is None:
                    raise ValueError(f'Cannot parse datetime from value "{x}"')
                x_datetime, x_millisecs, x_tz, x_zulu = x_match.groups()

                fmt = '%Y-%m-%dT%H:%M:%S'
                val = x_datetime

                if x_millisecs is not None:
                    x_millisecs = int(x_millisecs[1:])
                    fmt += '.%f'
                    val += f'.{x_millisecs:0>6}'

                if x_tz is not None:
                    fmt += '%z'
                    val += x_tz

                dtime = datetime.datetime.strptime(val, fmt)
                if x_zulu == 'Z':
                    dtime += datetime.timedelta(hours=1)
                return dtime
        elif returntype == 'boolean':
            def typeconvert(x):
                return cls.__strtobool(x)
        elif returntype == 'geometry':
            def typeconvert(x):
                if isinstance(x, etree._Element):
                    if owsutil.has_geom_support():
                        import shapely.geometry
                        import pygml
                        return shapely.geometry.shape(
                            pygml.parse(etree.tostring(x[0]).decode('utf8')))
                    else:
                        # this shouldn't happen
                        return etree.tostring(x[0]).decode('utf8')
                return np.nan
        else:
            def typeconvert(x):
                return x

        try:
            return typeconvert(text)
        except ValueError as e:
            warnings.warn(
                f"Failed to convert data to correct datatype: {e}. Resulting "
                "dataframe will be incomplete.",
                DataParseWarning)
            return np.nan


class AbstractSearch(AbstractCommon):
    """Abstract search class grouping methods common to all DOV search
    classes. Not to be instantiated or used directly."""

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

        self._wfs = None
        self._wfs_schema = None
        self._wfs_namespace = None
        self._wfs_max_features = None
        self._md_metadata = None
        self._fc_featurecatalogue = None
        self._xsd_schemas = None

    def _get_wfs_endpoint(self):
        """Get the WFS endpoint URL to use for accessing the feature type.

        Returns
        -------
        str
            The WFS endpoint URL.
        """
        base_url = build_dov_url('geoserver/')
        workspace = self._layer.split(':')[0]
        return base_url + workspace + '/wfs'

    def _init_wfs(self):
        """Initialise the WFS service. If the WFS service is not
        instantiated yet, do so and save it in a static variable available
        to all subclasses and instances.
        """
        if self._wfs is None:
            wfs_endpoint_url = self._get_wfs_endpoint()

            capabilities = owsutil.get_wfs_capabilities(
                wfs_endpoint_url + '?request=GetCapabilities&version=2.0.0')

            self._wfs = WebFeatureService(
                url=wfs_endpoint_url, version="2.0.0", xml=capabilities)

            self._wfs_max_features = owsutil.get_wfs_max_features(capabilities)

    def _init_namespace(self):
        """Initialise the WFS namespace associated with the layer.

        Raises
        ------
        NotImplementedError
            This is an abstract method that should be implemented in a
            subclass.

        """
        if self._wfs_namespace is None:
            self._wfs_namespace = self._get_namespace()

    def _init_fields(self):
        """Initialise the fields and their metadata available in this search
        class.

        Raises
        ------
        NotImplementedError
            This is an abstract method that should be implemented in a
            subclass.

        """
        if self._fields is None:
            if self._wfs_schema is None:
                self._wfs_schema = self._get_schema()

            if self._md_metadata is None:
                self._md_metadata = self._get_remote_metadata()

            if self._md_metadata is not None and \
                    self._fc_featurecatalogue is None:
                csw_url = self._get_csw_base_url()
                fc_uuid = owsutil.get_featurecatalogue_uuid(self._md_metadata)
                if fc_uuid is not None:
                    self._fc_featurecatalogue = \
                        owsutil.get_remote_featurecatalogue(csw_url, fc_uuid)

            if self._xsd_schemas is None:
                self._xsd_schemas = self._get_remote_xsd_schemas()

            fields = self._build_fields(
                self._wfs_schema,
                self._fc_featurecatalogue,
                self._xsd_schemas)

            for field in fields.values():
                if field['name'] not in self._type.get_field_names(
                        include_wfs_injected=True):
                    self._type.fields.append(
                        _WfsInjectedField(name=field['name'],
                                          datatype=field['type']))

            self._fields = self._build_fields(
                self._wfs_schema,
                self._fc_featurecatalogue,
                self._xsd_schemas)

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

        if self._layer not in self._wfs.contents:
            raise LayerNotFoundError(
                'Layer {} could not be found'.format(self._layer))
        else:
            return self._wfs.contents[self._layer]

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
        return get_schema(
            build_dov_url('geoserver/wfs'), layername, '2.0.0')

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
        return owsutil.get_namespace(self._wfs, self._layer)

    def _get_remote_metadata(self):
        """Request and parse the remote metadata associated with the layer.

        Returns
        -------
        owslib.iso.MD_Metadata or None
            Parsed remote metadata describing the WFS layer in more detail,
            in the ISO 19115/19139 format or None when no metadata could be
            found or parsed.

        """
        wfs_layer = self._get_layer()
        return owsutil.get_remote_metadata(wfs_layer)

    def _get_remote_xsd_schemas(self):
        """Request and parse the remote XSD schemas associated with this type.

        Returns
        -------
        list of etree.ElementTree
            List of parsed XSD schemas associated with this type.

        """
        xsd_schemas = [get_xsd_schema(i) for i in self._type.get_xsd_schemas()]
        return [etree.fromstring(i) for i in xsd_schemas if i is not None]

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

    @classmethod
    def _get_xsd_enum_values(cls, xsd_schemas, xml_field):
        """Get the distinct enum values from XSD schemas for a given XML field.

        Depending of the 'xsd_type' of the XML field, retrieve the distinct
        enum values and definitions from the XSD schemas.

        Parameters
        ----------
        xsd_schemas : list of etree.ElementTree
            List of parsed XSD schemas.
        xml_field : dict
            Dictionary describing the XML field, including a 'xsd_type' key
            linking the type to the enum type in (one of) the XSD schemas.

        Returns
        -------
        values : dict
            Dictionary containing the enum values as keys (in the datatype
            of the XML field) and the definitions as values.

        """
        values = None
        if xml_field.get('xsd_type', None):
            values = {}
            for schema in xsd_schemas:
                tree_values = schema.findall(
                    './/{{http://www.w3.org/2001/XMLSchema}}simpleType['
                    '@name="{}"]/'
                    '{{http://www.w3.org/2001/XMLSchema}}restriction/'
                    '{{http://www.w3.org/2001/XMLSchema}}enumeration'.format(
                        xml_field.get('xsd_type')))
                for e in tree_values:
                    value = cls._typeconvert(
                        e.get('value'), xml_field.get('type'))
                    values[value] = e.findtext(
                        './{http://www.w3.org/2001/XMLSchema}annotation/{'
                        'http://www.w3.org/2001/XMLSchema}documentation')
            if len(values) == 0:
                values = None
        return values

    def _build_fields(self, wfs_schema, feature_catalogue, xsd_schemas):
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

            list (boolean)
                Whether the field value is a list type. The items in the list
                will be of the `type` specified above.

            notnull (boolean)
                Whether the field is mandatory (True) or can be null (False).

            cost (integer)
                The cost associated with the request of this field in the
                output dataframe.

        Raises
        ------
        RuntimeError
            When the defined fields of this type are invalid.

        """
        fields = {}
        self._wfs_fields = []
        self._geometry_column = wfs_schema.get('geometry_column', None)

        for f in self._type.get_fields(include_subtypes=False).values():
            if not isinstance(f, pydov.types.fields.AbstractField):
                raise RuntimeError(
                    "Type '{}' fields should be instances of "
                    "pydov.types.fields.AbstractField, found {}.".format(
                        self._type.__name__, str(type(f))))

        for f in self._type.get_fields(include_subtypes=True).values():
            if not isinstance(f, pydov.types.fields.AbstractField):
                raise RuntimeError(
                    "Fields of subtype of '{}' should be instances of "
                    "pydov.types.fields.AbstractField, found {}.".format(
                        self._type.__name__, str(type(f))))

        _map_wfs_datatypes = {
            'int': 'integer',
            'long': 'integer',
            'decimal': 'float',
            'double': 'float',
            'dateTime': 'datetime'
        }

        df_wfs_fields = self._type.get_fields(source=('wfs',)).values()
        for f in df_wfs_fields:
            self._map_wfs_source_df[f['sourcefield']] = f['name']
            self._map_df_wfs_source[f['name']] = f['sourcefield']

        for wfs_field in wfs_schema['properties'].keys():
            self._wfs_fields.append(wfs_field)

            name = self._map_wfs_source_df.get(wfs_field, wfs_field)

            is_list = False
            for f in df_wfs_fields:
                if f['name'] == name:
                    is_list = f['split_fn'] is not None

            field = {
                'name': name,
                'definition': None,
                'type': _map_wfs_datatypes.get(
                    wfs_schema['properties'][wfs_field],
                    wfs_schema['properties'][wfs_field]),
                'list': is_list,
                'notnull': False,
                'query': True,
                'cost': 1
            }

            if feature_catalogue is not None and \
                    wfs_field in feature_catalogue['attributes']:
                fc_field = feature_catalogue['attributes'][wfs_field]
                field['definition'] = fc_field['definition']
                field['notnull'] = fc_field['multiplicity'][0] > 0

                if fc_field['values'] is not None:
                    field['values'] = fc_field['values']

            fields[name] = field

        if owsutil.has_geom_support() and 'geometry' in wfs_schema and \
                'geometry_column' in wfs_schema:
            name = wfs_schema['geometry_column']
            self._wfs_fields.append(name)

            field = {
                'name': name,
                'definition': None,
                'type': 'geometry',
                'list': False,
                'notnull': False,
                'query': False,
                'cost': 1
            }

            fields[name] = field

        for xml_field in self._type.get_fields(source=['xml']).values():
            field = {
                'name': xml_field['name'],
                'type': xml_field['type'],
                'list': xml_field['split_fn'] is not None,
                'definition': xml_field['definition'],
                'notnull': xml_field['notnull'],
                'query': False,
                'cost': 10
            }

            values = self._get_xsd_enum_values(xsd_schemas, xml_field)
            if values is not None:
                field['values'] = values

            fields[field['name']] = field

        for custom_field in self._type.get_fields(
                source=['custom_wfs']).values():
            field = {
                'name': custom_field['name'],
                'type': custom_field['type'],
                'list': False,
                'definition': custom_field['definition'],
                'notnull': custom_field['notnull'],
                'query': False,
                'cost': 1
            }
            fields[field['name']] = field

        for custom_field in self._type.get_fields(
                source=['custom_xml']).values():
            field = {
                'name': custom_field['name'],
                'type': custom_field['type'],
                'list': False,
                'definition': custom_field['definition'],
                'notnull': custom_field['notnull'],
                'query': False,
                'cost': 10
            }
            fields[field['name']] = field

        return fields

    def _pre_search_validation(self, location, query, sort_by,
                               return_fields, max_features):
        """Perform validation on the parameters of the search query.

        Parameters
        ----------
        location : pydov.util.location.AbstractLocationFilter
            Location filter limiting the features to retrieve.
        query : owslib.fes2.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes2. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        sort_by : owslib.fes2.SortBy, optional
            List of properties to sort by.
        return_fields : pydov.types.fields.ReturnFieldList
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`.
        max_features : int
            Limit the maximum number of features to request.

        Raises
        ------
        pydov.util.errors.InvalidSearchParameterError
            When not one of `location`, `query` or `max_features` is provided.

        pydov.util.errors.InvalidFieldError
            When at least one of the fields in `return_fields` is unknown.

            When a field that is only accessible as return field is used as
            a query parameter.

        """
        if location is None and query is None and max_features is None:
            raise InvalidSearchParameterError(
                'Provide either the location or the query parameter or the '
                'max_features parameter.'
            )

        if query is not None:
            if not isinstance(query, owslib.fes2.OgcExpression):
                if isinstance(query, owslib.fes.OgcExpression):
                    raise InvalidSearchParameterError(
                        "Query should be an owslib.fes2.OgcExpression.\n"
                        "Try importing your query operators, like "
                        f"'{query.__class__.__name__}', "
                        "from the owslib.fes2 package."
                    )

                raise InvalidSearchParameterError(
                    "Query should be an owslib.fes2.OgcExpression.")

            filter_request = FilterRequest()
            filter_request = filter_request.setConstraint(query)

            self._init_fields()
            for property_name in filter_request.findall(
                    './/{http://www.opengis.net/fes/2.0}ValueReference'):
                name = property_name.text
                if name not in self._map_df_wfs_source \
                        and name not in self._wfs_fields:
                    if name in self._fields:
                        raise InvalidFieldError(
                            "Cannot use return field '{}' in query.".format(
                                name))
                    raise InvalidFieldError(
                        "Unknown query parameter: '{}'".format(name))

                if name in self._wfs_fields and name in self._fields and \
                        self._fields[name]['type'] == 'geometry':
                    raise InvalidFieldError(
                        ("Cannot use geometry field '{}' in attribute query. "
                         "Use the 'location' parameter for "
                         "spatial filtering.").format(name)
                    )

        if location is not None:
            self._init_fields()

        if sort_by is not None:
            if not isinstance(sort_by, owslib.fes2.SortBy):
                raise InvalidSearchParameterError(
                    "SortBy should be an owslib.fes2.SortBy")

            self._init_fields()
            for property_name in sort_by.toXML().findall(
                    './/{http://www.opengis.net/fes/2.0}ValueReference'):
                name = property_name.text
                if name not in self._map_df_wfs_source \
                        and name not in self._wfs_fields:
                    if name in self._fields:
                        raise InvalidFieldError(
                            "Cannot use return field '{}' for sorting.".format(
                                name))
                    raise InvalidFieldError(
                        "Unknown query parameter: '{}'".format(name))

        return_fields = ReturnFieldList.from_field_names(return_fields)
        if return_fields is not None:
            if not isinstance(return_fields, ReturnFieldList):
                raise AttributeError(
                    'return_fields should be an instance of '
                    'pydov.types.fields.ReturnFieldList')

            self._init_fields()
            for rf in return_fields:
                if rf.name not in self._fields:
                    if rf.name in self._map_wfs_source_df:
                        raise InvalidFieldError(
                            "Unknown return field: "
                            "'{}'. Did you mean '{}'?".format(
                                rf, self._map_wfs_source_df[rf]))
                    if rf.name.lower() in [i.lower() for i in
                                           self._map_wfs_source_df.keys()]:
                        sugg = [i for i in self._map_wfs_source_df.keys() if
                                i.lower() == rf.name.lower()][0]
                        raise InvalidFieldError(
                            "Unknown return field: "
                            "'{}'. Did you mean '{}'?".format(rf.name, sugg))
                    raise InvalidFieldError(
                        "Unknown return field: '{}'".format(rf.name))
        elif len(self._type.fields) == 0:
            self._init_fields()

    @staticmethod
    def _get_remote_wfs_feature(wfs, typename, location, filter,
                                sort_by, propertyname, max_features,
                                geometry_column, crs=None, start_index=0,
                                session=None):
        """Perform the WFS 2.0 GetFeature call to get features from the remote
        service.

        Parameters
        ----------
        typename : str
            Layername to query.
        location : pydov.util.location.AbstractLocationFilter
            Location filter limiting the features to retrieve.
        filter : str of owslib.fes2.FilterRequest
            Filter request to search on attribute values.
        sort_by : str of owslib.fes2.SortBy, optional
            List of properties to sort by.
        propertyname : list<str>
            List of properties to return.
        max_features : int
            Limit the maximum number of features to request.
        geometry_column : str
            Name of the geometry column to use in the spatial filter.
        crs : str
            EPSG code of the CRS of the geometries that will be returned.
            Defaults to None, which means the default CRS of the WFS layer.
        start_index : int
            Index of the first feature to return. Can be used for paging.
        session : requests.Session
            Session to use to perform HTTP requests for data. Defaults to None,
            which means a new session will be created for each request.

        Returns
        -------
        wfs_response, wfs_getfeature_request : bytes, etree.Element
            Response of the WFS service.

        """
        wfs_getfeature_xml = owsutil.wfs_build_getfeature_request(
            geometry_column=geometry_column,
            typename=typename,
            location=location,
            filter=filter,
            sort_by=sort_by,
            max_features=max_features,
            propertyname=propertyname,
            start_index=start_index,
            crs=crs
        )

        tree = HookRunner.execute_inject_wfs_getfeature_response(
            wfs_getfeature_xml)

        if tree is not None:
            return tree, wfs_getfeature_xml

        return owsutil.wfs_get_feature(
            baseurl=wfs.url,
            get_feature_request=wfs_getfeature_xml,
            session=session
        ), wfs_getfeature_xml

    def _search(self, location=None, query=None, return_fields=None,
                sort_by=None, max_features=None, extra_wfs_fields=[]):
        """Perform the WFS search by issuing a GetFeature request.

        Parameters
        ----------
        location : pydov.util.location.AbstractLocationFilter
            Location filter limiting the features to retrieve.
        query : owslib.fes2.OgcExpression
            OGC filter expression to use for searching. This can contain any
            combination of filter elements defined in owslib.fes2. The query
            should use the fields provided in `get_fields()`. Note that not
            all fields are currently supported as a search parameter.
        return_fields : list<str>
            A list of fields to be returned in the output data. This should
            be a subset of the fields provided in `get_fields()`. Note that
            not all fields are currently supported as return fields.
        sort_by : owslib.fes2.SortBy, optional
            List of properties to sort by.
        max_features : int
            Limit the maximum number of features to request.
        extra_wfs_fields: list<str>
            A list of extra fields to be included in the WFS requests,
            regardless whether they're needed as return field. Optional,
            defaults to an empty list.

        Returns
        ------
        list of etree.Element
            XML trees of the WFS responses containing the features matching
            the location and the query.

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

        """
        self._pre_search_validation(location, query, sort_by, return_fields,
                                    max_features)
        self._init_namespace()
        self._init_wfs()

        filter_request = None
        if query is not None:
            filter_request = FilterRequest()
            filter_request = filter_request.setConstraint(query)

        if filter_request is not None:
            for property_name in filter_request.findall(
                    './/{http://www.opengis.net/fes/2.0}ValueReference'):
                property_name.text = self._map_df_wfs_source.get(
                    property_name.text, property_name.text)

            filter_request = etree.tostring(filter_request, encoding='unicode')

        if self._type.pkey_fieldname is not None:
            wfs_property_names = [self._type.pkey_fieldname]
        else:
            wfs_property_names = []

        if return_fields is None:
            wfs_property_names.extend([
                f['sourcefield'] for f in self._type.get_fields(
                    source=('wfs',)).values() if (
                        self._type.pkey_fieldname is None
                        or not f.get('wfs_injected', False))])
            geom_return_crs = None
        else:
            wfs_property_names.extend([self._map_df_wfs_source[i]
                                       for i in self._map_df_wfs_source
                                       if i in return_fields])

            geom_return_crs = [f.epsg for f in return_fields
                               if isinstance(f, GeometryReturnField)]
            if len(geom_return_crs) > 0:
                geom_return_crs = f'EPSG:{geom_return_crs[0]}'
            else:
                geom_return_crs = None

        extra_custom_fields = set()
        for custom_field in self._type.get_fields(
                source=('custom_wfs',)).values():
            extra_custom_fields.update(custom_field.requires_wfs_fields())

        wfs_property_names.extend(extra_wfs_fields)
        wfs_property_names.extend(list(extra_custom_fields))
        wfs_property_names = list(set(wfs_property_names))

        if sort_by is not None:
            sort_by_xml = sort_by.toXML()
            for property_name in sort_by_xml.findall(
                    './/{http://www.opengis.net/fes/2.0}ValueReference'):
                property_name.text = self._map_df_wfs_source.get(
                    property_name.text, property_name.text)

            sort_by = etree.tostring(sort_by_xml, encoding='unicode')

        HookRunner.execute_wfs_search_init(params=dict(
            typename=self._layer,
            location=location,
            filter=filter_request,
            sort_by=sort_by,
            max_features=max_features,
            propertynames=wfs_property_names,
            geometry_column=self._geometry_column
        ))

        def _get_remote_wfs(start_index=0, max_features=None, session=None):
            fts, getfeature = self._get_remote_wfs_feature(
                wfs=self._wfs,
                typename=self._layer,
                location=location,
                filter=filter_request,
                sort_by=sort_by,
                max_features=max_features,
                propertyname=wfs_property_names,
                geometry_column=self._geometry_column,
                crs=geom_return_crs,
                start_index=start_index,
                session=session)

            tree = etree.fromstring(fts)

            if tree.get('numberReturned') is None:
                raise WfsGetFeatureError(
                    "Error retrieving features of layer '{}' from "
                    "DOV WFS server:\n{}".format(
                        self._layer,
                        etree.tostring(tree).decode('utf8')))

            number_matched = int(tree.get('numberMatched'))
            number_returned = int(tree.get('numberReturned'))

            HookRunner.execute_wfs_search_result(
                number_matched, number_returned)

            HookRunner.execute_wfs_search_result_received(getfeature, tree)

            return tree

        result = []

        # execute the first WFS query
        tree = _get_remote_wfs(
            start_index=0, max_features=max_features, session=pydov.session)
        result.append(tree)

        number_matched = int(tree.get('numberMatched'))
        number_returned = int(tree.get('numberReturned'))

        if max_features is not None and number_returned == max_features:
            # we asked for a limited number of features and we got all of them,
            # we're done!
            pass
        elif number_matched == number_returned:
            # all features that matched the query were returned,
            # we're done!
            pass
        else:
            # more features matched the query than were returned by the server,
            # we need more requests to fetch the rest of the results
            pool = LocalSessionThreadPool()

            if max_features is not None:
                fts_to_get = min(
                    max_features, number_matched) - number_returned
            else:
                fts_to_get = number_matched - number_returned
            fts_per_req = self._wfs_max_features or number_returned
            extra_reqs = math.ceil(fts_to_get/fts_per_req)

            for i in range(extra_reqs):
                start_index = (i+1)*fts_per_req
                if i == extra_reqs - 1:
                    # last request
                    if fts_to_get == fts_per_req:
                        max_features = None
                    else:
                        max_features = fts_to_get % fts_per_req
                else:
                    max_features = fts_per_req

                pool.execute(_get_remote_wfs, (start_index, max_features))

            for r in pool.join():
                if r.get_error():
                    raise r.get_error()

                worker_result = r.get_result()
                if worker_result is not None and len(worker_result) > 0:
                    result.append(worker_result)

        return result

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

            list (boolean)
                Whether the field value is a list type. The items in the list
                will be of the `type` specified above.

            notnull (boolean)
                Whether the field is mandatory (True) or can be null (False).

            query (boolean)
                Whether the field can be used in an attribute query.

            cost (integer)
                The cost associated with the request of this field in the
                output dataframe.

            Optionally, it can contain:

            values (list)
                A list of possible values for this field.

        """
        self._init_fields()
        return self._fields

    def search(self, location=None, query=None,
               sort_by=None, return_fields=None, max_features=None):
        """Search for objects of this type. Provide `location` and/or
        `query` and/or `max_features`.
        When `return_fields` is None, all fields are returned.

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
        return_fields = ReturnFieldList.from_field_names(return_fields)

        trees = self._search(location=location, query=query, sort_by=sort_by,
                             return_fields=return_fields,
                             max_features=max_features)

        feature_generators = []
        for tree in trees:
            feature_generators.append(
                self._type.from_wfs(tree, self._wfs_namespace))

        cols = self._type.get_field_names(return_fields, include_geometry=True)
        if len(cols) == 0:
            cols = self._type.get_field_names(
                return_fields, include_wfs_injected=True,
                include_geometry=False)

        df = pd.DataFrame(
            data=self._type.to_df_array(
                chain.from_iterable(feature_generators), return_fields),
            columns=cols)
        return df
