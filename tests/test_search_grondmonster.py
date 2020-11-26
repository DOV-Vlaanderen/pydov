"""Module grouping tests for the search grondmonster module."""

from owslib.fes import PropertyIsEqualTo

from pydov.search.grondmonster import GrondmonsterSearch
from pydov.types.grondmonster import Grondmonster
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/grondmonster/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/grondmonster/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/grondmonster/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/grondmonster/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondmonster/feature.xml'
location_dov_xml = 'tests/data/types/grondmonster/grondmonster.xml'
location_xsd_base = 'tests/data/types/grondmonster/xsd_*.xml'


class TestGrondmonsterSearch(AbstractTestSearch):

    search_instance = GrondmonsterSearch()
    datatype_class = Grondmonster

    valid_query_single = PropertyIsEqualTo(propertyname='boornummer',
                                           literal='GEO-04/024-B6')

    inexistent_field = 'onbestaand'
    wfs_field = 'boornummer'
    xml_field = 'astm_naam'

    valid_returnfields = ('pkey_grondmonster', 'boornummer')
    valid_returnfields_subtype = (
        'pkey_grondmonster', 'boornummer', 'diameter')
    valid_returnfields_extra = ('pkey_grondmonster', 'korrelverdeling')

    df_default_columns = [
        'pkey_grondmonster', 'naam', 'pkey_boring', 'boornummer',
        'datum', 'x', 'y', 'gemeente', 'diepte_van_m', 'diepte_tot_m',
        'peil_van_mtaw', 'peil_tot_mtaw', 'monstertype', 'astm_naam',
        'grondsoort_bggg', 'humusgehalte', 'kalkgehalte',
        'uitrolgrens', 'vloeigrens', 'glauconiet',
        'korrelvolumemassa', 'volumemassa', 'watergehalte',
        'diameter', 'fractie', 'methode']

    def test_search_xmlresolving(self, mp_get_schema,
                                 mp_remote_describefeaturetype,
                                 mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with return fields from XML but not from a
        subtype.

        Test whether the output dataframe contains the resolved XML data.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = self.search_instance.search(
            query=self.valid_query_single,
            return_fields=('pkey_grondmonster', 'boornummer', 'humusgehalte',
                           'methode'))

        assert df.humusgehalte[0] == 4.7
        assert df.methode[0] == 'ZEEFPROEF'

    def test_issue_285(self, mp_get_schema,
                       mp_remote_describefeaturetype,
                       mp_remote_wfs_feature, mp_dov_xml):
        """Test whether korrelvolumemassa, volumemassa and watergehalte
        resolve correctly.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.
        """
        df = self.search_instance.search(
            query=self.valid_query_single,
            return_fields=(
                'boornummer',
                'naam',
                'korrelvolumemassa',
                'volumemassa',
                'watergehalte'))

        assert df.korrelvolumemassa[0] == 2.65
        assert df.volumemassa[0] == 1.627
        assert df.watergehalte[0] == 57.7
