# -*- coding: utf-8 -*-
"""Module grouping utility functions for OWS services."""
import warnings
from urllib.parse import urlparse
import re

from owslib.etree import etree
from owslib.fes2 import BinaryLogicOpType, UnaryLogicOpType
from owslib.namespaces import Namespaces
from owslib.util import nspath_eval

import pydov
from pydov.util.net import SessionFactory

from .hooks import HookRunner


def __get_namespaces():
    """Get default namespaces from OWSLib, extended with the 'gfc' namespace
    to be able to parse feature catalogues."""
    n = Namespaces()
    ns = n.get_namespaces()
    ns[None] = n.get_namespace("gmd")
    ns['gfc'] = 'http://www.isotc211.org/2005/gfc'
    return ns


__namespaces = __get_namespaces()

re_epsg = re.compile(r'^EPSG:[1-9]+[0-9]*')


def has_geom_support():
    try:
        import pygml
        import shapely
        return True or (pygml.__version__ and shapely.__version__)
    except ImportError:
        return False


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
    return get_url(fc_url)


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
    return get_url(describefeaturetype_url)


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
    owslib.iso.MD_Metadata or None
        Parsed remote metadata describing the WFS layer in more detail,
        in the ISO 19115/19139 format, or None when no metadata could be found
        or parsed.

    """
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        contentmetadata.parse_remote_metadata(pydov.util.net.request_timeout)

    for remote_md in contentmetadata.metadataUrls:
        if 'metadata' in remote_md and remote_md['metadata'] is not None:
            return remote_md['metadata']


def get_csw_base_url(contentmetadata):
    """Get the CSW base url for the remote metadata associated with the
    layer described in `contentmetadata`.

    Parameters
    ----------
    contentmetadata : owslib.feature.wfs110.ContentMetadata
        Content metadata associated with a WFS layer.

    Returns
    -------
    url : str or None
        Base URL of the CSW service where the remote metadata and feature
        catalogue can be requested or None when no metadata URL could be found.

    """
    md_url = None
    for md in contentmetadata.metadataUrls:
        if md.get('url', None) is not None \
                and 'getrecordbyid' in md.get('url', "").lower():
            md_url = md.get('url')

    if md_url is None:
        return None

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
    uuid : str or None
        Universally unique identifier of the feature catalogue associated
        with the metadata or None when there is no feature catalogue available.

    """
    fc_uuid = None

    contentinfo = md_metadata.contentinfo[0] if \
        len(md_metadata.contentinfo) > 0 else None
    if contentinfo is not None:
        fc_uuid = contentinfo.featurecatalogues[0] if \
            len(contentinfo.featurecatalogues) > 0 else None

    return fc_uuid


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
    dict or None
        Dictionary with fields described in the feature catalogue, using the
        following schema, or None when no feature catalogue with the given
        UUID could not be found:

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

    """
    fc_url = csw_url + '?Service=CSW&Request=GetRecordById&Version=2.0.2' \
                       '&outputSchema=http://www.isotc211.org/2005/gfc' \
                       '&elementSetName=full&id=' + fc_uuid

    content = __get_remote_fc(fc_url)
    tree = etree.fromstring(content)

    fc = tree.find(nspath_eval('gfc:FC_FeatureCatalogue', __namespaces))
    if fc is None:
        return None

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

        values = {}
        for lv in a.findall(nspath_eval('gfc:listedValue/gfc:FC_ListedValue',
                                        __namespaces)):
            label = lv.findtext(nspath_eval('gfc:label/gco:CharacterString',
                                            __namespaces))
            definition = lv.findtext(nspath_eval(
                'gfc:definition/gco:CharacterString', __namespaces))

            if label is not None:
                label = label.strip()
                if label != '':
                    if definition is not None:
                        values[label] = definition.strip() if \
                            definition.strip() != '' else None
                    else:
                        values[label] = None

        attr['values'] = values if len(values) > 0 else None

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
    url = _get_describefeaturetype_url(url=wfs.url, version='2.0.0',
                                       typename=layer)
    schema = __get_remote_describefeaturetype(url)
    tree = etree.fromstring(schema)
    namespace = tree.attrib.get('targetNamespace', None)
    return namespace


def get_wfs_max_features(capabilities):
    """Get the default maximum number of features the WFS service will return.

    Parameters
    ----------
    capabilities : bytes
        WFS 2.0.0 capabilities document.
    """
    tree = etree.fromstring(capabilities)

    count_default = tree.findtext(
        './/{http://www.opengis.net/ows/1.1}Operation[@name="GetFeature"]'
        '/{http://www.opengis.net/ows/1.1}Constraint[@name="CountDefault"]'
        '/{http://www.opengis.net/ows/1.1}DefaultValue')

    if count_default is not None:
        return int(count_default)


def set_geometry_column(location, geometry_column):
    """Set the geometry column of the location query recursively.

    Parameters
    ----------
    location : pydov.util.location.AbstractLocationFilter or \
                owslib.fes2.BinaryLogicOpType<AbstractLocationFilter> or \
                owslib.fes2.UnaryLogicOpType<AbstractLocationFilter>
        Location filter limiting the features to retrieve. Can either be a
        single instance of a subclass of AbstractLocationFilter, or a
        combination using And, Or, Not of AbstractLocationFilters.
    geometry_column : str
        The name of the geometry column to query.

    Returns
    -------
    etree.Element
        XML element of this location filter.

    """
    if isinstance(location, UnaryLogicOpType) or \
            isinstance(location, BinaryLogicOpType):
        for i in location.operations:
            set_geometry_column(i, geometry_column)
    else:
        location.set_geometry_column(geometry_column)

    return location.toXML()


def unique_gml_ids(location):
    """Make sure the location query has unique GML id's for all features.

    Parameters
    ----------
    location : etree.ElementTree
        XML tree of the location filter.
    Returns
    -------
    etree.ElementTree
        XML tree of the location filter with unique GML ids.

    """
    gml_items = location.findall('.//*[@{http://www.opengis.net/gml/3.2}id]')
    gml_ids = [i.get('{http://www.opengis.net/gml/3.2}id') for i in gml_items]

    if len(gml_ids) == len(set(gml_ids)):
        return location
    else:
        for ix, item in enumerate(gml_items):
            item.set('{http://www.opengis.net/gml/3.2}id', f'pydov.{ix}')
        return location


def wfs_build_getfeature_request(typename, geometry_column=None, location=None,
                                 filter=None, sort_by=None, propertyname=None,
                                 max_features=None, start_index=0,
                                 crs=None):
    """Build a WFS 2.0 GetFeature request in XML to be used as payload
    in a WFS 2.0 GetFeature request using POST.

    Parameters
    ----------
    typename : str
        Typename to query.
    geometry_column : str, optional
        Name of the geometry column to use in the spatial filter.
        Required if the ``location`` parameter is supplied.
    location : pydov.util.location.AbstractLocationFilter
        Location filter limiting the features to retrieve.
        Requires ``geometry_column`` to be supplied as well.
    filter : str of owslib.fes2.FilterRequest, optional
        Filter request to search on attribute values.
    sort_by : str of owslib.fes2.SortBy, optional
        List of properties to sort by.
    propertyname : list<str>, optional
        List of properties to return. Defaults to all properties.
    max_features : int
        Limit the maximum number of features to request.
    start_index : int
        The index of the first feature to return.
    crs : str
        EPSG code of the CRS of the geometries that will be returned. Defaults
        to None, which means the default CRS of the WFS layer.

    Raises
    ------
    AttributeError
        If ``bbox`` is given without ``geometry_column``.
        If ``max_features`` has an invalid value.
        If ``start_index`` had an invalid value.

    TypeError
        If ``crs`` is not a string.

    ValueError
        If ``crs`` does not start with 'EPSG'.

    Returns
    -------
    element : etree.Element
        XML element representing the WFS GetFeature request.

    """
    if location is not None and geometry_column is None:
        raise AttributeError('location requires geometry_column and it is '
                             'None')

    xml = etree.Element('{http://www.opengis.net/wfs/2.0}GetFeature')
    xml.set('service', 'WFS')
    xml.set('version', '2.0.0')

    if max_features is not None:
        if (not isinstance(max_features, int)) or (max_features <= 0):
            raise AttributeError('max_features should be a positive integer')
        xml.set('count', str(max_features))

    if (not isinstance(start_index, int)) or (start_index < 0):
        raise AttributeError('start_index should be a positive integer or 0')
    xml.set('startIndex', str(start_index))

    xml.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
            'http://www.opengis.net/wfs/2.0 '
            'http://schemas.opengis.net/wfs/2.0/wfs.xsd')

    query = etree.Element('{http://www.opengis.net/wfs/2.0}Query')
    query.set('typeNames', typename)

    if crs is not None:
        if not isinstance(crs, str):
            raise TypeError('crs should be a string starting with "EPSG"')

        if not re_epsg.match(crs):
            raise ValueError('crs should match the format "EPSG:1234"')

        query.set('srsName', f'urn:ogc:def:crs:{crs.replace(":", "::")}')

    if propertyname and len(propertyname) > 0:
        for property in sorted(propertyname):
            propertyname_xml = etree.Element(
                '{http://www.opengis.net/wfs/2.0}PropertyName')
            propertyname_xml.text = property
            query.append(propertyname_xml)

    filter_xml = etree.Element('{http://www.opengis.net/fes/2.0}Filter')
    filter_parent = filter_xml

    if filter is not None and location is not None:
        # if both filter and location are specified, we wrap them inside an
        # ogc:And
        and_xml = etree.Element('{http://www.opengis.net/fes/2.0}And')
        filter_xml.append(and_xml)
        filter_parent = and_xml

    if filter is not None:
        filterrequest = etree.fromstring(filter)
        filter_parent.append(filterrequest[0])

    if location is not None:
        location = set_geometry_column(location, geometry_column)
        location = unique_gml_ids(location)
        filter_parent.append(location)

    if filter is not None or location is not None:
        query.append(filter_xml)

    if sort_by is not None:
        query.append(etree.fromstring(sort_by))

    xml.append(query)
    return xml


def wfs_get_feature(baseurl, get_feature_request, session=None):
    """Perform a WFS request using POST.

    Parameters
    ----------
    baseurl : str
        Base URL of the WFS service.
    get_feature_request : etree.Element
        XML element representing the WFS GetFeature request.
    session : requests.Session
        Session to use to perform HTTP requests for data. Defaults to None,
        which means a new session will be created for each request.

    Returns
    -------
    bytes
        Response of the WFS service.

    """
    if session is None:
        session = SessionFactory.get_session()

    data = etree.tostring(get_feature_request)

    request = session.post(baseurl, data)
    request.encoding = 'utf-8'
    return request.text.encode('utf8')


def get_wfs_capabilities(url):
    """Perform a GET request to get the WFS capabilities.

    Parameters
    ----------
    url : str
        URL to request.

    Returns
    -------
    bytes
        Response containing the result of the WFS capabilities request.
    """
    return get_url(url)


def get_url(url):
    """Perform a GET request to an OWS service an return the result.

    Parameters
    ----------
    url : str
        URL to request.

    Returns
    -------
    bytes
        Response containing the result of the GET request.

    """
    response = HookRunner.execute_inject_meta_response(url)

    if response is None:
        request = pydov.session.get(url)
        request.encoding = 'utf-8'
        response = request.text.encode('utf8')

    HookRunner.execute_meta_received(url, response)

    return response
