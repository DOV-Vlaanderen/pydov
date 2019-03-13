"""Module grouping tests for the pydov.util.owsutil module."""
import copy

import pytest
from numpy.compat import unicode

from owslib.etree import etree
from owslib.fes import (
    PropertyIsEqualTo,
    FilterRequest,
)
from owslib.iso import MD_Metadata
from owslib.util import nspath_eval
from pydov.util import owsutil
from pydov.util.errors import (
    MetadataNotFoundError,
    FeatureCatalogueNotFoundError,
)
from pydov.util.location import (
    Within,
    Box,
)
from tests.abstract import clean_xml

from tests.test_search_boring import (
    md_metadata,
    mp_remote_md,
    mp_remote_describefeaturetype,
    mp_remote_fc,
    location_md_metadata,
    location_fc_featurecatalogue,
    location_wfs_describefeaturetype,
)

from tests.test_search import (
    wfs,
    mp_wfs,
    mp_remote_fc_notfound
)


class TestOwsutil(object):
    """Class grouping tests for the pydov.util.owsutil module."""

    def test_get_csw_base_url(self, wfs):
        """Test the owsutil.get_csw_base_url method.

        Test whether the CSW base URL of the dov-pub:Boringen layer is correct.

        Parameters
        ----------
        wfs : pytest.fixture returning owslib.wfs.WebFeatureService
            WebFeatureService based on the local GetCapabilities.

        """
        contentmetadata = wfs.contents['dov-pub:Boringen']
        assert owsutil.get_csw_base_url(contentmetadata) == \
               'https://www.dov.vlaanderen.be/geonetwork/srv/nl/csw'

    def test_get_csw_base_url_nometadataurls(self, wfs):
        """Test the owsutil.get_csw_base_url method for a layer without
        metdata urls.

        Test whether a MetadataNotFoundError is raised.

        Parameters
        ----------
        wfs : pytest.fixture returning owslib.wfs.WebFeatureService
            WebFeatureService based on the local GetCapabilities.

        """
        contents = copy.deepcopy(wfs.contents)
        contentmetadata = contents['dov-pub:Boringen']
        contentmetadata.metadataUrls = []
        with pytest.raises(MetadataNotFoundError):
            owsutil.get_csw_base_url(contentmetadata)

    def test_get_featurecatalogue_uuid(self, md_metadata):
        """Test the owsutil.get_featurecatalogue_uuid method.

        Test whether the featurecatalogue uuid of the dov-pub:Boringen layer
        is correct.

        Parameters
        ----------
        md_metadata : pytest.fixture providing owslib.iso.MD_Metadata
            Parsed metadata describing the Boringen WFS layer in more detail,
            in the ISO 19115/19139 format.

        """
        assert owsutil.get_featurecatalogue_uuid(md_metadata) == \
               'c0cbd397-520f-4ee1-aca7-d70e271eeed6'

    def test_get_featurecatalogue_uuid_nocontentinfo(self, md_metadata):
        """Test the owsutil.get_featurecatalogue_uuid method when the
        metadata is missing the gmd:contentInfo element.

        Test whether a FeatureCatalogueNotFoundError is raised.

        Parameters
        ----------
        md_metadata : pytest.fixture providing owslib.iso.MD_Metadata
            Parsed metadata describing the Boringen WFS layer in more detail,
            in the ISO 19115/19139 format.

        """
        tree = etree.fromstring(md_metadata.xml)
        root = tree.find('{http://www.isotc211.org/2005/gmd}MD_Metadata')
        for ci in tree.findall(
                './/{http://www.isotc211.org/2005/gmd}contentInfo'):
            root.remove(ci)
        md_metadata.xml = etree.tostring(tree)

        with pytest.raises(FeatureCatalogueNotFoundError):
            owsutil.get_featurecatalogue_uuid(md_metadata)

    def test_get_featurecatalogue_uuid_nouuidref(self, md_metadata):
        """Test the owsutil.get_featurecatalogue_uuid method when the
        gmd:contentInfo element is missing a 'uuidref' attribute.

        Test whether a FeatureCatalogueNotFoundError is raised.

        Parameters
        ----------
        md_metadata : pytest.fixture providing owslib.iso.MD_Metadata
            Parsed metadata describing the Boringen WFS layer in more detail,
            in the ISO 19115/19139 format.

        """
        tree = etree.fromstring(md_metadata.xml)
        for ci in tree.findall(nspath_eval(
            'gmd:MD_Metadata/gmd:contentInfo/'
            'gmd:MD_FeatureCatalogueDescription/'
            'gmd:featureCatalogueCitation',
            {'gmd': 'http://www.isotc211.org/2005/gmd'})):
            ci.attrib.pop('uuidref')
        md_metadata.xml = etree.tostring(tree)

        with pytest.raises(FeatureCatalogueNotFoundError):
            owsutil.get_featurecatalogue_uuid(md_metadata)

    def test_get_namespace(self, wfs, mp_remote_describefeaturetype):
        """Test the owsutil.get_namespace method.

        Test whether the namespace of the dov-pub:Boringen layer is correct.

        Parameters
        ----------
        wfs : pytest.fixture returning owslib.wfs.WebFeatureService
            WebFeatureService based on the local GetCapabilities.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            dov-pub:Boringen layer.

        """
        assert owsutil.get_namespace(wfs, 'dov-pub:Boringen') == \
               'http://dov.vlaanderen.be/ocdov/dov-pub'

    def test_get_remote_featurecatalogue(self, mp_remote_fc):
        """Test the owsutil.get_remote_featurecatalogue method.

        Test whether the feature catalogue of the dov-pub:Boringen layer
        matches the format described in the docs.

        Parameters
        ----------
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue of the
            dov-pub:Boringen layer.

        """
        fc = owsutil.get_remote_featurecatalogue(
            'https://www.dov.vlaanderen.be/geonetwork/srv/nl/csw',
            'c0cbd397-520f-4ee1-aca7-d70e271eeed6')

        assert type(fc) is dict

        assert 'definition' in fc
        assert type(fc['definition']) in (str, unicode)

        assert 'attributes' in fc
        assert type(fc['attributes']) is dict

        attrs = fc['attributes']
        if len(attrs) > 0:
            for attr in attrs.values():
                assert type(attr) is dict

                assert 'definition' in attr
                assert type(attr['definition']) in (str, unicode)

                assert 'values' in attr

                if attr['values'] is not None:
                    assert type(attr['values']) is dict

                    for v in attr['values'].keys():
                        assert type(v) in (str, unicode)
                        assert type(attr['values'][v]) in (str, unicode) or \
                               attr['values'][v] is None
                    assert len(attr['values'].keys()) == len(
                        set(attr['values'].keys()))

                assert 'multiplicity' in attr
                mp = attr['multiplicity']
                assert type(mp) is tuple
                assert len(mp) == 2
                assert mp[0] in (0, 1)
                assert (type(mp[1]) is int and mp[1] > 0) or mp[1] == 'Inf'

    def test_get_remote_featurecataloge_baduuid(self, mp_remote_fc_notfound):
        """Test the owsutil.get_remote_featurecatalogue method with an
        inexistent feature catalogue uuid.

        Test whether a FeatureCatalogueNotFoundError is raised.

        Parameters
        ----------
        mp_remote_fc_notfound : pytest.fixture
            Monkeypatch the call to get an inexistent remote featurecatalogue.

        """
        with pytest.raises(FeatureCatalogueNotFoundError):
            owsutil.get_remote_featurecatalogue(
                'https://www.dov.vlaanderen.be/geonetwork/srv/nl/csw',
                'badfc000-0000-0000-0000-badfc00badfc')

    def test_get_remote_metadata(self, md_metadata):
        """Test the owsutil.get_remote_metadata method.

        Test whether the resulting MD_Metadata is correct.

        Parameters
        ----------
        md_metadata : pytest.fixture returning owslib.iso.MD_Metadata
            Parsed metadata describing the Boringen WFS layer in more detail,
            in the ISO 19115/19139 format.

        """
        assert type(md_metadata) is MD_Metadata

    def test_get_remote_metadata_nometadataurls(self, wfs):
        """Test the owsutil.get_remote_metadata method when the WFS layer
        missed metadata URLs.

        Test whether a MetadataNotFoundError is raised.

        Parameters
        ----------
        wfs : pytest.fixture returning owslib.wfs.WebFeatureService
            WebFeatureService based on the local GetCapabilities.

        """
        contents = copy.deepcopy(wfs.contents)
        contentmetadata = contents['dov-pub:Boringen']
        contentmetadata.metadataUrls = []
        with pytest.raises(MetadataNotFoundError):
            owsutil.get_remote_metadata(contentmetadata)

    def test_wfs_build_getfeature_request_onlytypename(self):
        """Test the owsutil.wfs_build_getfeature_request method with only a
        typename specified.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        xml = owsutil.wfs_build_getfeature_request('dov-pub:Boringen')
        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="1.1.0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs '
            'http://schemas.opengis.net/wfs/1.1.0/wfs.xsd"><wfs:Query '
            'typeName="dov-pub:Boringen"><ogc:Filter '
            'xmlns:ogc="http://www.opengis.net/ogc"/></wfs:Query></wfs'
            ':GetFeature>')

    def test_wfs_build_getfeature_request_bbox_nogeometrycolumn(self):
        """Test the owsutil.wfs_build_getfeature_request method with a location
        argument but without the geometry_column argument.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            xml = owsutil.wfs_build_getfeature_request(
                'dov-pub:Boringen',
                location=Within(Box(151650, 214675, 151750, 214775)))

    def test_wfs_build_getfeature_request_bbox(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        typename, box and geometry_column.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen',
            location=Within(Box(151650, 214675, 151750, 214775)),
            geometry_column='geom')
        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="1.1.0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs '
            'http://schemas.opengis.net/wfs/1.1.0/wfs.xsd"><wfs:Query '
            'typeName="dov-pub:Boringen"><ogc:Filter '
            'xmlns:ogc="http://www.opengis.net/ogc"><ogc:Within> '
            '<ogc:PropertyName>geom</ogc:PropertyName><gml:Envelope '
            'xmlns:gml="http://www.opengis.net/gml" srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370"><gml'
            ':lowerCorner>151650.000000 '
            '214675.000000</gml:lowerCorner><gml:upperCorner>151750.000000 '
            '214775.000000</gml:upperCorner></gml:Envelope></ogc:Within></ogc'
            ':Filter></wfs:Query></wfs:GetFeature>')

    def test_wfs_build_getfeature_request_propertyname(self):
        """Test the owsutil.wfs_build_getfeature_request method with a list
        of propertynames.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', propertyname=['fiche', 'diepte_tot_m'])
        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="1.1.0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs '
            'http://schemas.opengis.net/wfs/1.1.0/wfs.xsd"> <wfs:Query '
            'typeName="dov-pub:Boringen"> '
            '<wfs:PropertyName>fiche</wfs:PropertyName> '
            '<wfs:PropertyName>diepte_tot_m</wfs:PropertyName> <ogc:Filter/> '
            '</wfs:Query> </wfs:GetFeature>')

    def test_wfs_build_getfeature_request_filter(self):
        """Test the owsutil.wfs_build_getfeature_request method with an
        attribute filter.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        query = PropertyIsEqualTo(propertyname='gemeente',
                                  literal='Herstappe')
        filter_request = FilterRequest()
        filter_request = filter_request.setConstraint(query)
        try:
            filter_request = etree.tostring(filter_request,
                                            encoding='unicode')
        except LookupError:
            # Python2.7 without lxml uses 'utf-8' instead.
            filter_request = etree.tostring(filter_request,
                                            encoding='utf-8')

        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', filter=filter_request)
        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="1.1.0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs '
            'http://schemas.opengis.net/wfs/1.1.0/wfs.xsd"> <wfs:Query '
            'typeName="dov-pub:Boringen"> <ogc:Filter> '
            '<ogc:PropertyIsEqualTo> '
            '<ogc:PropertyName>gemeente</ogc:PropertyName> '
            '<ogc:Literal>Herstappe</ogc:Literal> </ogc:PropertyIsEqualTo> '
            '</ogc:Filter> </wfs:Query> </wfs:GetFeature>')

    def test_wfs_build_getfeature_request_bbox_filter(self):
        """Test the owsutil.wfs_build_getfeature_request method with an
        attribute filter, a box and a geometry_column.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        query = PropertyIsEqualTo(propertyname='gemeente',
                                  literal='Herstappe')
        filter_request = FilterRequest()
        filter_request = filter_request.setConstraint(query)
        try:
            filter_request = etree.tostring(filter_request,
                                            encoding='unicode')
        except LookupError:
            # Python2.7 without lxml uses 'utf-8' instead.
            filter_request = etree.tostring(filter_request,
                                            encoding='utf-8')

        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', filter=filter_request,
            location=Within(Box(151650, 214675, 151750, 214775)),
            geometry_column='geom')
        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="1.1.0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs '
            'http://schemas.opengis.net/wfs/1.1.0/wfs.xsd"> <wfs:Query '
            'typeName="dov-pub:Boringen"> <ogc:Filter> <ogc:And> '
            '<ogc:PropertyIsEqualTo> '
            '<ogc:PropertyName>gemeente</ogc:PropertyName> '
            '<ogc:Literal>Herstappe</ogc:Literal> </ogc:PropertyIsEqualTo> '
            '<ogc:Within> <ogc:PropertyName>geom</ogc:PropertyName> '
            '<gml:Envelope xmlns:gml="http://www.opengis.net/gml" '
            'srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370"> '
            '<gml:lowerCorner>151650.000000 214675.000000</gml:lowerCorner> '
            '<gml:upperCorner>151750.000000 214775.000000</gml:upperCorner> '
            '</gml:Envelope> </ogc:Within> </ogc:And> </ogc:Filter> '
            '</wfs:Query> </wfs:GetFeature>')

    def test_wfs_build_getfeature_request_bbox_filter_propertyname(self):
        """Test the owsutil.wfs_build_getfeature_request method with an
        attribute filter, a box, a geometry_column and a list of
        propertynames.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        query = PropertyIsEqualTo(propertyname='gemeente',
                                  literal='Herstappe')
        filter_request = FilterRequest()
        filter_request = filter_request.setConstraint(query)
        try:
            filter_request = etree.tostring(filter_request,
                                            encoding='unicode')
        except LookupError:
            # Python2.7 without lxml uses 'utf-8' instead.
            filter_request = etree.tostring(filter_request,
                                            encoding='utf-8')

        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', filter=filter_request,
            location=Within(Box(151650, 214675, 151750, 214775)),
            geometry_column='geom', propertyname=['fiche', 'diepte_tot_m'])
        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="1.1.0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs '
            'http://schemas.opengis.net/wfs/1.1.0/wfs.xsd"> <wfs:Query '
            'typeName="dov-pub:Boringen"> '
            '<wfs:PropertyName>fiche</wfs:PropertyName> '
            '<wfs:PropertyName>diepte_tot_m</wfs:PropertyName> <ogc:Filter> '
            '<ogc:And> <ogc:PropertyIsEqualTo> '
            '<ogc:PropertyName>gemeente</ogc:PropertyName> '
            '<ogc:Literal>Herstappe</ogc:Literal> </ogc:PropertyIsEqualTo> '
            '<ogc:Within> <ogc:PropertyName>geom</ogc:PropertyName> '
            '<gml:Envelope xmlns:gml="http://www.opengis.net/gml" '
            'srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370"> '
            '<gml:lowerCorner>151650.000000 214675.000000</gml:lowerCorner> '
            '<gml:upperCorner>151750.000000 214775.000000</gml:upperCorner> '
            '</gml:Envelope> </ogc:Within> </ogc:And> </ogc:Filter> '
            '</wfs:Query> </wfs:GetFeature>')
