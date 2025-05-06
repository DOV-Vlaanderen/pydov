"""Module grouping tests for the pydov.util.owsutil module."""
import copy

import pytest
from owslib.etree import etree
from owslib.fes2 import FilterRequest, PropertyIsEqualTo, SortBy, SortProperty, Or
from owslib.iso import MD_Metadata
from owslib.util import nspath_eval

from pydov.util import owsutil
from pydov.util.dovutil import build_dov_url
from pydov.util.location import Box, Within, WithinDistance
from tests.abstract import clean_xml

location_md_metadata = 'tests/data/types/boring/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/boring/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/boring/wfsdescribefeaturetype.xml'


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
            build_dov_url('geonetwork/srv/dut/csw')

    def test_get_csw_base_url_nometadataurls(self, wfs):
        """Test the owsutil.get_csw_base_url method for a layer without
        metadata urls.

        Test whether None is returned.

        Parameters
        ----------
        wfs : pytest.fixture returning owslib.wfs.WebFeatureService
            WebFeatureService based on the local GetCapabilities.

        """
        contents = copy.deepcopy(wfs.contents)
        contentmetadata = contents['dov-pub:Boringen']
        contentmetadata.metadataUrls = []

        assert owsutil.get_csw_base_url(contentmetadata) is None

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

        Test whether None is returned.

        Parameters
        ----------
        md_metadata : pytest.fixture providing owslib.iso.MD_Metadata
            Parsed metadata describing the Boringen WFS layer in more detail,
            in the ISO 19115/19139 format.

        """
        tree = etree.fromstring(md_metadata.xml)
        for ci in tree.findall(
                './/{http://www.isotc211.org/2005/gmd}contentInfo'):
            tree.remove(ci)
        md_metadata = MD_Metadata(tree)

        assert owsutil.get_featurecatalogue_uuid(md_metadata) is None

    def test_get_featurecatalogue_uuid_nouuidref(self, md_metadata):
        """Test the owsutil.get_featurecatalogue_uuid method when the
        gmd:contentInfo element is missing a 'uuidref' attribute.

        Test whether None is returned.

        Parameters
        ----------
        md_metadata : pytest.fixture providing owslib.iso.MD_Metadata
            Parsed metadata describing the Boringen WFS layer in more detail,
            in the ISO 19115/19139 format.

        """
        tree = etree.fromstring(md_metadata.xml)
        for ci in tree.findall(nspath_eval(
            'gmd:contentInfo/'
            'gmd:MD_FeatureCatalogueDescription/'
            'gmd:featureCatalogueCitation',
                {'gmd': 'http://www.isotc211.org/2005/gmd'})):
            ci.attrib.pop('uuidref')
        md_metadata = MD_Metadata(tree)

        assert owsutil.get_featurecatalogue_uuid(md_metadata) is None

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
            build_dov_url('geonetwork/srv/nl/csw'),
            'c0cbd397-520f-4ee1-aca7-d70e271eeed6')

        assert isinstance(fc, dict)

        assert 'definition' in fc
        assert isinstance(fc['definition'], str)

        assert 'attributes' in fc
        assert isinstance(fc['attributes'], dict)

        attrs = fc['attributes']
        if len(attrs) > 0:
            for attr in attrs.values():
                assert isinstance(attr, dict)

                assert 'definition' in attr
                assert isinstance(attr['definition'], str)

                assert 'values' in attr

                if attr['values'] is not None:
                    assert isinstance(attr['values'], dict)

                    for v in attr['values'].keys():
                        assert isinstance(v, str)
                        assert isinstance(attr['values'][v], str) or \
                            attr['values'][v] is None
                    assert len(attr['values'].keys()) == len(
                        set(attr['values'].keys()))

                assert 'multiplicity' in attr
                mp = attr['multiplicity']
                assert isinstance(mp, tuple)
                assert len(mp) == 2
                assert mp[0] in (0, 1)
                assert (isinstance(mp[1], int) and mp[1] > 0) or mp[1] == 'Inf'

    def test_get_remote_featurecataloge_baduuid(self, mp_remote_fc_notfound):
        """Test the owsutil.get_remote_featurecatalogue method with an
        inexistent feature catalogue uuid.

        Test whether None is returned.

        Parameters
        ----------
        mp_remote_fc_notfound : pytest.fixture
            Monkeypatch the call to get an inexistent remote featurecatalogue.

        """
        assert owsutil.get_remote_featurecatalogue(
            build_dov_url('geonetwork/srv/nl/csw'),
            'badfc000-0000-0000-0000-badfc00badfc') is None

    def test_get_remote_metadata(self, md_metadata):
        """Test the owsutil.get_remote_metadata method.

        Test whether the resulting MD_Metadata is correct.

        Parameters
        ----------
        md_metadata : pytest.fixture returning owslib.iso.MD_Metadata
            Parsed metadata describing the Boringen WFS layer in more detail,
            in the ISO 19115/19139 format.

        """
        assert isinstance(md_metadata, MD_Metadata)

    def test_get_wfs_max_features(self, wfs_capabilities):
        """Test the owsutil.get_wfs_max_features method.

        Test whether the default maximum number of features can be found.

        Parameters
        ----------
        wfs_capabilities : pytest.fixture
            PyTest fixture providing the WFS GetCapabilities response.
        """
        max_features = owsutil.get_wfs_max_features(wfs_capabilities)

        assert isinstance(max_features, int)
        assert max_features > 0


class TestWfsGetFeatureRequest(object):
    """Class grouping tests checking the WFS GetFeature request generation."""

    def test_wfs_build_getfeature_request_onlytypename(self):
        """Test the owsutil.wfs_build_getfeature_request method with only a
        typename specified.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        xml = owsutil.wfs_build_getfeature_request('dov-pub:Boringen')

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs/2.0" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="2.0.0" startIndex="0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs/2.0 '
            'http://schemas.opengis.net/wfs/2.0/wfs.xsd"><wfs:Query '
            'typeNames="dov-pub:Boringen"/></wfs'
            ':GetFeature>')

    def test_wfs_build_getfeature_start_index(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        startIndex defined.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', start_index=3)

        assert "startIndex" in xml.attrib.keys()
        assert xml.attrib["startIndex"] == "3"

    def test_wfs_build_getfeature_start_index_negative(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        a negative startIndex value.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            owsutil.wfs_build_getfeature_request(
                'dov-pub:Boringen', start_index=-5)

    def test_wfs_build_getfeature_start_index_none(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        a startIndex value of None.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            owsutil.wfs_build_getfeature_request(
                'dov-pub:Boringen', start_index=None)

    def test_wfs_build_getfeature_start_index_float(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        a floating point startIndex value.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            owsutil.wfs_build_getfeature_request(
                'dov-pub:Boringen', start_index=1.5)

    def test_wfs_build_getfeature_start_index_string(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        an non-integer startIndex value.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            owsutil.wfs_build_getfeature_request(
                'dov-pub:Boringen', start_index="0")

    def test_wfs_build_getfeature_maxfeatures(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        limited set of features defined.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', max_features=3)

        assert "count" in xml.attrib.keys()
        assert xml.attrib["count"] == "3"

    def test_wfs_build_getfeature_maxfeatures_negative(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        a negative maxfeature value.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            owsutil.wfs_build_getfeature_request(
                'dov-pub:Boringen', max_features=-5)

    def test_wfs_build_getfeature_maxfeatures_float(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        a floating point maxfeature value.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            owsutil.wfs_build_getfeature_request(
                'dov-pub:Boringen', max_features=1.5)

    def test_wfs_build_getfeature_maxfeatures_zero(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        a maxfeature value of 0.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            owsutil.wfs_build_getfeature_request(
                'dov-pub:Boringen', max_features=0)

    def test_wfs_build_getfeature_maxfeatures_string(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        an non-integer maxfeature value.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            owsutil.wfs_build_getfeature_request(
                'dov-pub:Boringen', max_features="0")

    def test_wfs_build_getfeature_request_bbox_nogeometrycolumn(self):
        """Test the owsutil.wfs_build_getfeature_request method with a location
        argument but without the geometry_column argument.

        Test whether an AttributeError is raised.

        """
        with pytest.raises(AttributeError):
            owsutil.wfs_build_getfeature_request(
                'dov-pub:Boringen',
                location=Within(Box(151650, 214675, 151750, 214775)))

    def test_wfs_build_getfeature_request_bbox(self, mp_gml_id):
        """Test the owsutil.wfs_build_getfeature_request method with a
        typename, box and geometry_column.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen',
            location=Within(Box(151650, 214675, 151750, 214775)),
            geometry_column='geom')

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs/2.0" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="2.0.0" startIndex="0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs/2.0 '
            'http://schemas.opengis.net/wfs/2.0/wfs.xsd"><wfs:Query '
            'typeNames="dov-pub:Boringen"><fes:Filter '
            'xmlns:fes="http://www.opengis.net/fes/2.0"><fes:Within> '
            '<fes:ValueReference>geom</fes:ValueReference><gml:Envelope '
            'xmlns:gml="http://www.opengis.net/gml/3.2" srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid"><gml:lowerCorner>151650.000000 '
            '214675.000000</gml:lowerCorner><gml:upperCorner>151750.000000 '
            '214775.000000</gml:upperCorner></gml:Envelope></fes:Within></fes'
            ':Filter></wfs:Query></wfs:GetFeature>')

    def test_wfs_build_getfeature_request_gml_id_stable(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        typename, box and geometry_column.
        Test whether the XML of the WFS GetFeature call is stable.
        """
        xml1 = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen',
            location=Within(Box(151650, 214675, 151750, 214775)),
            geometry_column='geom')

        xml2 = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen',
            location=Within(Box(151650, 214675, 151750, 214775)),
            geometry_column='geom')

        assert etree.tostring(xml1) == etree.tostring(xml2)

    def test_wfs_build_getfeature_request_gml_id_unique(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        typename, two boxes and geometry_column.
        Test whether the GML ids in the XML of the WFS GetFeature are unique.
        """
        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen',
            location=Or([
                Within(Box(100000, 120000, 200000, 220000)),
                WithinDistance(Box(100000, 120000, 200000, 220000), 10)
            ]),
            geometry_column='geom')

        gml_items = xml.findall('.//*[@{http://www.opengis.net/gml/3.2}id]')
        gml_ids = [i.get('{http://www.opengis.net/gml/3.2}id') for i in gml_items]

        assert len(gml_ids) == len(set(gml_ids))

    def test_wfs_build_getfeature_request_propertyname(self):
        """Test the owsutil.wfs_build_getfeature_request method with a list
        of propertynames.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', propertyname=['fiche', 'diepte_tot_m'])

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs/2.0" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="2.0.0" startIndex="0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs/2.0 '
            'http://schemas.opengis.net/wfs/2.0/wfs.xsd"> <wfs:Query '
            'typeNames="dov-pub:Boringen"> '
            '<wfs:PropertyName>diepte_tot_m</wfs:PropertyName> '
            '<wfs:PropertyName>fiche</wfs:PropertyName>'
            '</wfs:Query> </wfs:GetFeature>')

    def test_wfs_build_getfeature_request_propertyname_stable(self):
        """Test the owsutil.wfs_build_getfeature_request method with a list
        of propertynames.

        Test whether the XML of the WFS GetFeature that is being generated is
        stable (i.e. independent of the order of the propertynames).

        """
        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', propertyname=['fiche', 'diepte_tot_m'])

        xml2 = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', propertyname=['diepte_tot_m', 'fiche'])

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            etree.tostring(xml2).decode('utf8'))

    def test_wfs_build_getfeature_request_filter(self):
        """Test the owsutil.wfs_build_getfeature_request method with an
        attribute filter.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        query = PropertyIsEqualTo(propertyname='gemeente',
                                  literal='Herstappe')
        filter_request = FilterRequest()
        filter_request = filter_request.setConstraint(query)
        filter_request = etree.tostring(filter_request, encoding='unicode')

        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', filter=filter_request)

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs/2.0" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="2.0.0" startIndex="0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs/2.0 '
            'http://schemas.opengis.net/wfs/2.0/wfs.xsd"> <wfs:Query '
            'typeNames="dov-pub:Boringen"> <fes:Filter> '
            '<fes:PropertyIsEqualTo> '
            '<fes:ValueReference>gemeente</fes:ValueReference> '
            '<ogc:Literal>Herstappe</ogc:Literal> </fes:PropertyIsEqualTo> '
            '</ogc:Filter> </wfs:Query> </wfs:GetFeature>')

    def test_wfs_build_getfeature_request_bbox_filter(self, mp_gml_id):
        """Test the owsutil.wfs_build_getfeature_request method with an
        attribute filter, a box and a geometry_column.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        query = PropertyIsEqualTo(propertyname='gemeente',
                                  literal='Herstappe')
        filter_request = FilterRequest()
        filter_request = filter_request.setConstraint(query)
        filter_request = etree.tostring(filter_request, encoding='unicode')

        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', filter=filter_request,
            location=Within(Box(151650, 214675, 151750, 214775)),
            geometry_column='geom')

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs/2.0" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="2.0.0" startIndex="0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs/2.0 '
            'http://schemas.opengis.net/wfs/2.0/wfs.xsd"> <wfs:Query '
            'typeNames="dov-pub:Boringen"> <fes:Filter> <fes:And> '
            '<fes:PropertyIsEqualTo> '
            '<fes:ValueReference>gemeente</fes:ValueReference> '
            '<ogc:Literal>Herstappe</ogc:Literal> </fes:PropertyIsEqualTo> '
            '<fes:Within> <fes:ValueReference>geom</fes:ValueReference> '
            '<gml:Envelope xmlns:gml="http://www.opengis.net/gml" '
            'srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid"> '
            '<gml:lowerCorner>151650.000000 214675.000000</gml:lowerCorner> '
            '<gml:upperCorner>151750.000000 214775.000000</gml:upperCorner> '
            '</gml:Envelope> </fes:Within> </fes:And> </fes:Filter> '
            '</wfs:Query> </wfs:GetFeature>')

    def test_wfs_build_getfeature_request_bbox_filter_propertyname(
            self, mp_gml_id):
        """Test the owsutil.wfs_build_getfeature_request method with an
        attribute filter, a box, a geometry_column and a list of
        propertynames.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        query = PropertyIsEqualTo(propertyname='gemeente',
                                  literal='Herstappe')
        filter_request = FilterRequest()
        filter_request = filter_request.setConstraint(query)
        filter_request = etree.tostring(filter_request, encoding='unicode')

        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', filter=filter_request,
            location=Within(Box(151650, 214675, 151750, 214775)),
            geometry_column='geom', propertyname=['fiche', 'diepte_tot_m'])

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs/2.0" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="2.0.0" startIndex="0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs/2.0 '
            'http://schemas.opengis.net/wfs/2.0/wfs.xsd"> <wfs:Query '
            'typeNames="dov-pub:Boringen"> '
            '<wfs:PropertyName>diepte_tot_m</wfs:PropertyName> '
            '<wfs:PropertyName>fiche</wfs:PropertyName> <fes:Filter> '
            '<fes:And> <fes:PropertyIsEqualTo> '
            '<fes:ValueReference>gemeente</fes:ValueReference> '
            '<ogc:Literal>Herstappe</ogc:Literal> </fes:PropertyIsEqualTo> '
            '<fes:Within> <fes:ValueReference>geom</fes:ValueReference> '
            '<gml:Envelope xmlns:gml="http://www.opengis.net/gml" '
            'srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid"> '
            '<gml:lowerCorner>151650.000000 214675.000000</gml:lowerCorner> '
            '<gml:upperCorner>151750.000000 214775.000000</gml:upperCorner> '
            '</gml:Envelope> </fes:Within> </fes:And> </fes:Filter> '
            '</wfs:Query> </wfs:GetFeature>')

    def test_wfs_build_getfeature_request_sortby(self):
        """Test the owsutil.wfs_build_getfeature_request method with a sortby.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        sort_by = SortBy([SortProperty('diepte_tot_m', 'DESC')])

        sort_by = etree.tostring(sort_by.toXML(), encoding='unicode')

        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', propertyname=['fiche', 'diepte_tot_m'],
            sort_by=sort_by)

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs/2.0" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="2.0.0" startIndex="0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs/2.0 '
            'http://schemas.opengis.net/wfs/2.0/wfs.xsd"><wfs:Query '
            'typeNames="dov-pub:Boringen"><wfs:PropertyName>diepte_tot_m</wfs'
            ':PropertyName><wfs:PropertyName>fiche</wfs:PropertyName'
            '><fes:SortBy><fes:SortProperty><fes:ValueReference'
            '>diepte_tot_m</fes:ValueReference><ogfesc:SortOrder>DESC</fes'
            ':SortOrder></fes:SortProperty></fes:SortBy></wfs:Query></wfs'
            ':GetFeature>')

    def test_wfs_build_getfeature_request_sortby_multi(self):
        """Test the owsutil.wfs_build_getfeature_request method with a
        sortby containing multiple sort properties.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        sort_by = SortBy([SortProperty('diepte_tot_m', 'DESC'),
                          SortProperty('datum_aanvang', 'ASC')])

        sort_by = etree.tostring(sort_by.toXML(), encoding='unicode')

        xml = owsutil.wfs_build_getfeature_request(
            'dov-pub:Boringen', propertyname=['fiche', 'diepte_tot_m'],
            sort_by=sort_by)

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs/2.0" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="2.0.0" startIndex="0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs/2.0 '
            'http://schemas.opengis.net/wfs/2.0/wfs.xsd"><wfs:Query '
            'typeNames="dov-pub:Boringen"><wfs:PropertyName>diepte_tot_m</wfs'
            ':PropertyName><wfs:PropertyName>fiche</wfs:PropertyName'
            '><fes:SortBy><fes:SortProperty><fes:ValueReference'
            '>diepte_tot_m</fes:ValueReference><fes:SortOrder>DESC</fes'
            ':SortOrder></fes:SortProperty><fes:SortProperty><fes'
            ':ValueReference>datum_aanvang</fes:ValueReference><fes:SortOrder>'
            'ASC</fes:SortOrder></fes:SortProperty></fes:SortBy></wfs:Query>'
            '</wfs:GetFeature>')

    def test_wfs_build_getfeature_request_srs(self):
        """Test the owsutil.wfs_build_getfeature_request method with only a
        typename and an SRS.

        Test whether the XML of the WFS GetFeature call is generated correctly.

        """
        xml = owsutil.wfs_build_getfeature_request('dov-pub:Boringen', crs='EPSG:31370')

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<wfs:GetFeature xmlns:wfs="http://www.opengis.net/wfs/2.0" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'service="WFS" version="2.0.0" startIndex="0" '
            'xsi:schemaLocation="http://www.opengis.net/wfs/2.0 '
            'http://schemas.opengis.net/wfs/2.0/wfs.xsd"><wfs:Query '
            'typeNames="dov-pub:Boringen" '
            'srsName="urn:ogc:def:crs:EPSG::31370"/></wfs:GetFeature>')

    def test_wfs_build_getfeature_request_srs_wrongtype(self):
        """Test the owsutil.wfs_build_getfeature_request method with only a
        typename and an CRS of the wrong type.

        Test whether a TypeError is raised.

        """
        with pytest.raises(TypeError):
            owsutil.wfs_build_getfeature_request('dov-pub:Boringen', crs=31370)

    def test_wfs_build_getfeature_request_srs_wrongvalue(self):
        """Test the owsutil.wfs_build_getfeature_request method with only a
        typename and an CRS of the wrong type.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            owsutil.wfs_build_getfeature_request('dov-pub:Boringen', crs='31370')
