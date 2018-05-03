# -*- coding: utf-8 -*-
"""Module grouping utility functions for OWS services."""
import requests

from owslib.feature.schema import (
    _get_describefeaturetype_url,
    _get_elements,
    XS_NAMESPACE,
    GML_NAMESPACES
)

try:
    # Python3
    from urllib.parse import urlparse
except ImportError:
    # Python2
    from urlparse import urlparse

from owslib.etree import etree
from owslib.iso import MD_Metadata
from owslib.namespaces import Namespaces
from owslib.util import (
    openURL,
    nspath_eval,
    findall,
)

from pydov.util.errors import (
    MetadataNotFoundError,
    FeatureCatalogueNotFoundError,
)


def __get_namespaces():
    """Get default namespaces from OWSLib, extended with the 'gfc' namespace
    to be able to parse feature catalogues."""
    n = Namespaces()
    ns = n.get_namespaces()
    ns[None] = n.get_namespace("gmd")
    ns['gfc'] = 'http://www.isotc211.org/2005/gfc'
    return ns


__namespaces = __get_namespaces()


def __get_remote_md(md_url):
    """Request the remote metadata by calling the `md_url` and
    returning the response.

    Parameters
    ----------
    md_url : str
        URL to the remote metadata.

    Returns
    -------
    bytes
        Response containing the remote metadata.

    """
    return openURL(md_url).read()


def __get_remote_fc(fc_url):
    """Request the remote featurecatalogue by calling the `fc_url` and
    returning the response.

    Parameters
    ----------
    fc_url : str
        URL to the remote feature catalogue.

    Returns
    -------
    bytes
        Response containing the remote feature catalogue.

    """
    return openURL(fc_url).read()


def __get_remote_describefeaturetype(describefeaturetype_url):
    """Request the remote DescribeFeatureType by calling the
    `describefeaturetype_url` and returning the response.

    Parameters
    ----------
    describefeaturetype_url : str
        URL to the DescribeFeatureType.

    Returns
    -------
    bytes
        Response containing the remote DescribeFeatureType.

    """
    return openURL(describefeaturetype_url).read()


def get_remote_metadata(contentmetadata):
    """Request and parse the remote metadata associated with the layer
    described in `contentmetadata`.

    Parameters
    ----------
    contentmetadata : owslib.feature.wfs110.ContentMetadata
        Content metadata associated with a WFS layer, containing the
        associated `metadataUrls`.

    Returns
    -------
    owslib.iso.MD_Metadata
        Parsed remote metadata describing the WFS layer in more detail,
        in the ISO 19115/19139 format.

    Raises
    ------
    pydov.util.errors.MetadataNotFoundError
        If the `contentmetadata` has no valid metadata URL associated with it.

    """
    md_url = None
    for md in contentmetadata.metadataUrls:
        if md.get('url', None) is not None \
                and 'getrecordbyid' in md.get('url', "").lower():
            md_url = md.get('url')

    if md_url is None:
        raise MetadataNotFoundError

    content = __get_remote_md(md_url)
    doc = etree.fromstring(content)
    return MD_Metadata(doc)


def get_csw_base_url(contentmetadata):
    """Get the CSW base url for the remote metadata associated with the
    layer described in `contentmetadata`.

    Parameters
    ----------
    contentmetadata : owslib.feature.wfs110.ContentMetadata
        Content metadata associated with a WFS layer.

    Returns
    -------
    url : str
        Base URL of the CSW service where the remote metadata and feature
        catalogue can be requested.

    Raises
    ------
    pydov.util.errors.MetadataNotFoundError
        If the `contentmetadata` has no valid metadata URL associated with it.

    """
    md_url = None
    for md in contentmetadata.metadataUrls:
        if md.get('url', None) is not None \
                and 'getrecordbyid' in md.get('url', "").lower():
            md_url = md.get('url')

    if md_url is None:
        raise MetadataNotFoundError

    parsed_url = urlparse(md_url)
    return parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path


def get_featurecatalogue_uuid(md_metadata):
    """Get the UUID of the feature catalogue associated with the metadata.

    Parameters
    ----------
    md_metadata : owslib.iso.MD_Metadata
        Metadata parsed according to the ISO 19115/19139 format.

    Returns
    -------
    uuid : str
        Universally unique identifier of the feature catalogue associated
        with the metadata.

    Raises
    ------
    pydov.util.errors.FeatureCatalogueNotFoundError
        If there is no Feature Catalogue associated with the metadata or its
        UUID could not be retrieved.

    """
    tree = etree.fromstring(md_metadata.xml)

    citation = tree.find(nspath_eval(
        'gmd:MD_Metadata/gmd:contentInfo/gmd:MD_FeatureCatalogueDescription/'
        'gmd:featureCatalogueCitation', __namespaces))

    if citation is None:
        raise FeatureCatalogueNotFoundError

    uuid = citation.attrib.get('uuidref', None)
    if uuid is None:
        raise FeatureCatalogueNotFoundError

    return uuid


def get_remote_featurecatalogue(csw_url, fc_uuid):
    """Request and parse the remote feature catalogue described by the CSW
    base url and feature catalogue UUID.

    Parameters
    ----------
    csw_url : str
        Base URL of the CSW service to query, should end with 'csw'.
    fc_uuid : str
        Universally unique identifier of the feature catalogue.

    Returns
    -------
    dict
        Dictionary with fields described in the feature catalogue, using the
        following schema:

        >>>   {'definition' : 'feature type definition',
        >>>    'attributes' : {'name':
        >>>      {'definition' : 'attribute definition',
        >>>       'values' : ['list of', 'values'],
        >>>       'multiplicity': (lower, upper)}
        >>>    }
        >>>   }

        Where the lower multiplicity is always and integer and the upper
        multiplicity is either an integer or the str 'Inf' indicating an
        infinate value.

    Raises
    ------
    pydov.util.errors.FeatureCatalogueNotFoundError
        If there is no feature catalogue with given UUID available in the
        given CSW service.

    """
    fc_url = csw_url + '?Service=CSW&Request=GetRecordById&Version=2.0.2' \
                       '&outputSchema=http://www.isotc211.org/2005/gmd' \
                       '&elementSetName=full&id=' + fc_uuid

    content = __get_remote_fc(fc_url)
    tree = etree.fromstring(content)

    fc = tree.find(nspath_eval('gfc:FC_FeatureCatalogue', __namespaces))
    if fc is None:
        raise FeatureCatalogueNotFoundError

    r = {}
    r['definition'] = fc.findtext(nspath_eval(
        'gfc:featureType/gfc:FC_FeatureType/gfc:definition/'
        'gco:CharacterString', __namespaces))

    attributes = {}
    for a in fc.findall(nspath_eval(
            'gfc:featureType/gfc:FC_FeatureType/gfc:carrierOfCharacteristics/'
            'gfc:FC_FeatureAttribute', __namespaces)):
        attr = {}
        name = a.findtext(
            nspath_eval('gfc:memberName/gco:LocalName', __namespaces))
        attr['definition'] = a.findtext(nspath_eval(
            'gfc:definition/gco:CharacterString', __namespaces))

        try:
            multiplicity_lower = int(a.findtext(nspath_eval(
                'gfc:cardinality/gco:Multiplicity/gco:range/gco'
                ':MultiplicityRange/gco:lower/gco:Integer', __namespaces)))
        except (TypeError, ValueError):
            multiplicity_lower = 0

        upper = a.find(nspath_eval(
            'gfc:cardinality/gco:Multiplicity/gco:range/gco'
            ':MultiplicityRange/gco:upper/gco:UnlimitedInteger',
            __namespaces))

        try:
            multiplicity_upper = int(upper.text)
        except (TypeError, ValueError):
            multiplicity_upper = None

        if upper.get('isInfinite', 'false').lower() == 'true':
            multiplicity_upper = 'Inf'

        values = []
        for lv in a.findall(nspath_eval('gfc:listedValue/gfc:FC_ListedValue',
                                        __namespaces)):
            value = lv.findtext(nspath_eval('gfc:label/gco:CharacterString',
                                            __namespaces))
            if value is not None:
                values.append(value)
        attr['values'] = values
        attr['multiplicity'] = (multiplicity_lower, multiplicity_upper)
        attributes[name] = attr

    r['attributes'] = attributes
    return r


def get_namespace(wfs, layer):
    """Request the namespace associated with a layer by performing a
    DescribeFeatureType request.

    Parameters
    ----------
    wfs : owslib.wfs.WebFeatureService
        WFS service to use, associated with the layer.
    layer : str
        Workspace-qualified name of the layer to get the namespace of (
        typename).

    Returns
    -------
    namespace : str
        URI of the namespace associated with the given layer.

    """
    from owslib.feature.schema import _get_describefeaturetype_url
    url = _get_describefeaturetype_url(url=wfs.url, version='1.1.0',
                                       typename=layer)
    schema = __get_remote_describefeaturetype(url)
    tree = etree.fromstring(schema)
    namespace = tree.attrib.get('targetNamespace', None)
    return namespace


def _construct_schema(elements, nsmap):
    """Copy the owslib.feature.schema.get_schema method to be able to get
    the geometry column name.

    Parameters
    ----------
    elements : list<Element>
        List of elements
    nsmap : dict
        Namespace map

    Returns
    -------
    dict
        Schema

    """
    schema = {
        'properties': {},
        'geometry': None
    }

    schema_key = None
    gml_key = None

    # if nsmap is defined, use it
    if nsmap:
        for key in nsmap:
            if nsmap[key] == XS_NAMESPACE:
                schema_key = key
            if nsmap[key] in GML_NAMESPACES:
                gml_key = key
    # if no nsmap is defined, we have to guess
    else:
        gml_key = 'gml'
        schema_key = 'xsd'

    mappings = {
        'PointPropertyType': 'Point',
        'PolygonPropertyType': 'Polygon',
        'LineStringPropertyType': 'LineString',
        'MultiPointPropertyType': 'MultiPoint',
        'MultiLineStringPropertyType': 'MultiLineString',
        'MultiPolygonPropertyType': 'MultiPolygon',
        'MultiGeometryPropertyType': 'MultiGeometry',
        'GeometryPropertyType': 'GeometryCollection',
        'SurfacePropertyType': '3D Polygon',
        'MultiSurfacePropertyType': '3D MultiPolygon'
    }

    for element in elements:
        data_type = element.attrib['type'].replace(gml_key + ':', '')
        name = element.attrib['name']

        if data_type in mappings:
            schema['geometry'] = mappings[data_type]
            schema['geometry_column'] = name
        else:
            schema['properties'][name] = data_type.replace(schema_key+':', '')

    if schema['properties'] or schema['geometry']:
        return schema
    else:
        return None


def get_remote_schema(url, typename, version='1.0.0'):
    """Copy the owslib.feature.schema.get_schema method to be able to
    monkeypatch the openURL request in tests.

    Parameters
    ----------
    url : str
        Base URL of the WFS service.
    typename : str
        Typename of the feature type to get the schema of.
    version : str
        Version of WFS to use. Defaults to 1.0.0

    Returns
    -------
    dict
        Schema of the given WFS layer.

    """
    url = _get_describefeaturetype_url(url, version, typename)
    res = __get_remote_describefeaturetype(url)
    root = etree.fromstring(res)

    if ':' in typename:
        typename = typename.split(':')[1]
    type_element = findall(root, '{%s}element' % XS_NAMESPACE,
                           attribute_name='name', attribute_value=typename)[0]
    complex_type = type_element.attrib['type'].split(":")[1]
    elements = _get_elements(complex_type, root)
    nsmap = None
    if hasattr(root, 'nsmap'):
        nsmap = root.nsmap
    return _construct_schema(elements, nsmap)


def wfs_build_getfeature_request(typename, geometry_column=None, bbox=None,
                                 filter=None, propertyname=None,
                                 version='1.1.0'):
    """Build a WFS GetFeature request in XML to be used as payload in a WFS
    GetFeature request using POST.

    Parameters
    ----------
    typename : str
        Typename to query.
    geometry_column : str, optional
        Name of the geometry column to use in the spatial filter.
        Required if the ``bbox`` parameter is supplied.
    bbox : tuple<minx,miny,maxx,maxy>, optional
        The bounding box limiting the features to retrieve.
        Requires ``geometry_column`` to be supplied as well.
    filter : owslib.fes.FilterRequest, optional
        Filter request to search on attribute values.
    propertyname : list<str>, optional
        List of properties to return. Defaults to all properties.
    version : str, optional
        WFS version to use. Defaults to 1.1.0

    Raises
    ------
    AttributeError
        If ``bbox`` is given without ``geometry_column``.

    Returns
    -------
    element : etree.Element
        XML element representing the WFS GetFeature request.

    """
    if bbox is not None and geometry_column is None:
        raise AttributeError('bbox requires geometry_column and it is None')

    xml = etree.Element('{http://www.opengis.net/wfs}GetFeature')
    xml.set('service', 'WFS')
    xml.set('version', version)

    xml.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
            'http://www.opengis.net/wfs '
            'http://schemas.opengis.net/wfs/%s/wfs.xsd' % version)

    query = etree.Element('{http://www.opengis.net/wfs}Query')
    query.set('typeName', typename)

    if propertyname and len(propertyname) > 0:
        for property in propertyname:
            propertyname_xml = etree.Element(
                '{http://www.opengis.net/wfs}PropertyName')
            propertyname_xml.text = property
            query.append(propertyname_xml)

    filter_xml = etree.Element('{http://www.opengis.net/ogc}Filter')
    filter_parent = filter_xml

    if filter is not None and bbox is not None:
        # if both filter and bbox are specified, we wrap them inside an
        # ogc:And
        and_xml = etree.Element('{http://www.opengis.net/ogc}And')
        filter_xml.append(and_xml)
        filter_parent = and_xml

    if filter is not None:
        filterrequest = etree.fromstring(filter)
        filter_parent.append(filterrequest[0])

    if bbox is not None:
        within = etree.Element('{http://www.opengis.net/ogc}Within')
        geom = etree.Element('{http://www.opengis.net/ogc}PropertyName')
        geom.text = geometry_column
        within.append(geom)

        envelope = etree.Element('{http://www.opengis.net/gml}Envelope')
        envelope.set('srsDimension', '2')
        envelope.set('srsName',
                     'http://www.opengis.net/gml/srs/epsg.xml#31370')

        lower_corner = etree.Element('{http://www.opengis.net/gml}lowerCorner')
        lower_corner.text = '%0.3f %0.3f' % (bbox[0], bbox[1])
        envelope.append(lower_corner)

        upper_corner = etree.Element('{http://www.opengis.net/gml}upperCorner')
        upper_corner.text = '%0.3f %0.3f' % (bbox[2], bbox[3])
        envelope.append(upper_corner)
        within.append(envelope)
        filter_parent.append(within)

    query.append(filter_xml)
    xml.append(query)
    return xml


def wfs_get_feature(baseurl, get_feature_request):
    """Perform a WFS request using POST.

    Parameters
    ----------
    baseurl : str
        Base URL of the WFS service.
    get_feature_request : etree.Element
        XML element representing the WFS GetFeature request.

    Returns
    -------
    bytes
        Response of the WFS service.

    """
    data = etree.tostring(get_feature_request)
    request = requests.post(baseurl, data)
    return request.text.encode('utf8')
