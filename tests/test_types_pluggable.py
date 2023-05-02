import pytest
from owslib.fes2 import PropertyIsEqualTo

from pydov.search.grondwaterfilter import GrondwaterFilterSearch
from pydov.types.abstract import AbstractDovSubType
from pydov.types.fields import XmlField
from pydov.types.grondwaterfilter import GrondwaterFilter
from pydov.util.dovutil import build_dov_url

location_md_metadata = 'tests/data/types/grondwaterfilter/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/grondwaterfilter/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/grondwaterfilter/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/grondwaterfilter/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondwaterfilter/feature.xml'
location_dov_xml = 'tests/data/types/grondwaterfilter/grondwaterfilter.xml'
location_xsd_base = 'tests/data/types/grondwaterfilter/xsd_*.xml'


class MyGrondwaterFilter(GrondwaterFilter):

    fields = GrondwaterFilter.extend_fields([
        XmlField(name='grondwatersysteem',
                 source_xpath='/filter/ligging/grondwatersysteem',
                 definition='Grondwatersysteem waarin de filter hangt.',
                 datatype='string')
    ])


class MyWrongGrondwaterFilter(GrondwaterFilter):

    fields = GrondwaterFilter.extend_fields([
        {'name': 'grondwatersysteem',
         'source': 'xml',
         'sourcefield': '/filter/ligging/grondwatersysteem',
         'definition': 'Grondwatersysteem waarin de filter hangt.',
         'type': 'string',
         'notnull': False
         }
    ])


class MyFilterOpbouw(AbstractDovSubType):

    rootpath = './/filter/opbouw/onderdeel'

    fields = [
        XmlField(name='opbouw_van',
                 source_xpath='/van',
                 definition='Opbouw van',
                 datatype='float'),
        XmlField(name='opbouw_tot',
                 source_xpath='/tot',
                 definition='Opbouw tot',
                 datatype='float'),
        XmlField(name='opbouw_element',
                 source_xpath='/filterelement',
                 definition='Opbouw element',
                 datatype='string',
                 notnull=False)
    ]


class MyGrondwaterFilterOpbouw(GrondwaterFilter):

    subtypes = [MyFilterOpbouw]


class TestMyWrongGrondwaterFilter(object):
    """Class grouping tests for the MyWrongGrondwaterFilter custom type."""

    def test_get_fields(
            self, mp_wfs, mp_get_schema, mp_remote_describefeaturetype,
            mp_remote_md, mp_remote_fc, mp_remote_xsd, mp_remote_wfs_feature,
            mp_dov_xml):
        """Test the get_fields method.

        Test whether a RuntimeError is raised.

        """
        fs = GrondwaterFilterSearch(objecttype=MyWrongGrondwaterFilter)

        with pytest.raises(RuntimeError):
            fs.get_fields()

    def test_search(
            self, mp_wfs, mp_get_schema, mp_remote_describefeaturetype,
            mp_remote_md, mp_remote_fc, mp_remote_xsd, mp_remote_wfs_feature,
            mp_dov_xml):
        """Test the search method.

        Test whether a RuntimeError is raised.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        fs = GrondwaterFilterSearch(objecttype=MyWrongGrondwaterFilter)

        with pytest.raises(RuntimeError):
            fs.search(query=PropertyIsEqualTo(
                propertyname='filterfiche',
                literal=build_dov_url('data/filter/2003-004471')))


class TestMyGrondwaterFilter(object):
    """Class grouping tests for the MyGrondwaterFilter custom type."""

    def test_get_fields(self, mp_wfs, mp_remote_describefeaturetype,
                        mp_remote_md, mp_remote_fc, mp_remote_wfs_feature,
                        mp_dov_xml):
        """Test the get_fields method.

        Test whether the extra field is available in the output of the
        get_fields metadata.

        """
        fs = GrondwaterFilterSearch(objecttype=MyGrondwaterFilter)
        fields = fs.get_fields()

        assert 'grondwatersysteem' in fields

    def test_search(self, mp_wfs, mp_remote_describefeaturetype,
                    mp_remote_md, mp_remote_fc, mp_remote_wfs_feature,
                    mp_dov_xml):
        """Test the search method.

        Test whether the extra fields from the custom type are resolved into
        data in the result dataframe.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        fs = GrondwaterFilterSearch(objecttype=MyGrondwaterFilter)

        df = fs.search(query=PropertyIsEqualTo(
            propertyname='filterfiche',
            literal=build_dov_url('data/filter/2003-004471')))

        assert 'grondwatersysteem' in df
        assert df.iloc[0].grondwatersysteem == 'Centraal Vlaams Systeem'


class TestMyGrondwaterFilterOpbouw(object):
    """Class grouping tests for the MyGrondwaterFilterOpbouw and
    MyFilterOpbouw custom type."""

    def test_get_fields(self, mp_wfs, mp_remote_describefeaturetype,
                        mp_remote_md, mp_remote_fc, mp_remote_wfs_feature,
                        mp_dov_xml):
        """Test the get_fields method.

        Test whether the extra field is available in the output of the
        get_fields metadata.

        """
        fs = GrondwaterFilterSearch(objecttype=MyGrondwaterFilterOpbouw)
        fields = fs.get_fields()

        assert 'datum' not in fields
        assert 'peil_mtaw' not in fields

        assert 'opbouw_van' in fields
        assert 'opbouw_tot' in fields
        assert 'opbouw_element' in fields

    def test_search(self, mp_wfs, mp_remote_describefeaturetype,
                    mp_remote_md, mp_remote_fc, mp_remote_wfs_feature,
                    mp_dov_xml):
        """Test the search method.

        Test whether the extra fields from the custom type are resolved into
        data in the result dataframe.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        fs = GrondwaterFilterSearch(objecttype=MyGrondwaterFilterOpbouw)

        df = fs.search(query=PropertyIsEqualTo(
            propertyname='filterfiche',
            literal=build_dov_url('data/filter/2003-004471')))

        assert 'opbouw_van' in df
        assert 'opbouw_tot' in df
        assert 'opbouw_element' in df

        assert df.iloc[-1].opbouw_van == 2.5
        assert df.iloc[-1].opbouw_tot == 2.7
        assert df.iloc[-1].opbouw_element == 'zandvang'
