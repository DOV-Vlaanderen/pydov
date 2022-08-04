"""Module for test for features without subtype values."""

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.grondwaterfilter import GrondwaterFilterSearch
from pydov.util.dovutil import build_dov_url

location_md_metadata = 'tests/data/types/grondwaterfilter/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/grondwaterfilter/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/grondwaterfilter/wfsdescribefeaturetype.xml'
location_xsd_base = 'tests/data/types/grondwaterfilter/xsd_*.xml'

location_wfs_getfeature = \
    'tests/data/types/grondwaterfilter/wfsgetfeature_geenpeilmeting.xml'
location_wfs_feature = \
    'tests/data/types/grondwaterfilter/feature_geenpeilmeting.xml'
location_dov_xml = \
    'tests/data/types/grondwaterfilter/grondwaterfilter_geenpeilmeting.xml'


class TestSearchNoSubtype(object):
    def test_search_nosubtype(self, mp_wfs, mp_remote_md, mp_remote_fc,
                              mp_get_schema, mp_remote_describefeaturetype,
                              mp_remote_wfs_feature, mp_remote_xsd,
                              mp_dov_xml):
        """Test the search method with a result containing no elements from
        the subtype.

        Test whether the output dataframe contains the results, with the
        columns of the subtype set to NaN.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_remote_xsd : pytest.fixture
            Monkeypatch the call to get XSD schemas.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = GrondwaterFilterSearch().search(
            query=PropertyIsEqualTo(
                'pkey_filter',
                build_dov_url('data/filter/1976-101132.xml')
            )
        )

        assert len(df.pkey_filter) == 1

        assert df.datum.hasnans
        assert df.tijdstip.hasnans
        assert df.peil_mtaw.hasnans
        assert df.betrouwbaarheid.hasnans
