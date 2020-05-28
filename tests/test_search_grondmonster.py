"""Module grouping tests for the search grondmonster module."""
import datetime

from owslib.fes import PropertyIsEqualTo

from pydov.search.grondmonster import GrondmonsterSearch
from pydov.types.grondmonster import Grondmonster
from tests.abstract import AbstractTestSearch
from tests.test_search import (mp_dov_xml, mp_dov_xml_broken, mp_get_schema,
                               mp_remote_describefeaturetype, mp_remote_fc,
                               mp_remote_md, mp_remote_wfs_feature,
                               mp_remote_xsd, mp_wfs, wfs, wfs_feature,
                               wfs_getfeature)

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
    def get_search_object(self):
        return GrondmonsterSearch()

    def get_type(self):
        return Grondmonster

    def get_valid_query_single(self):
        return PropertyIsEqualTo(propertyname='boornummer',
                                 literal='GEO-04/024-B6')

    def get_inexistent_field(self):
        return 'onbestaand'

    def get_wfs_field(self):
        return 'boornummer'

    def get_xml_field(self):
        return 'astm_naam'

    def get_valid_returnfields(self):
        return ('pkey_grondmonster', 'boornummer')

    def get_valid_returnfields_subtype(self):
        return ('pkey_grondmonster', 'boornummer', 'diameter')

    def get_valid_returnfields_extra(self):
        return ('pkey_grondmonster', 'korrelverdeling')

    def get_df_default_columns(self):
        return ['pkey_grondmonster', 'naam', 'pkey_boring', 'boornummer',
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
        df = self.get_search_object().search(
            query=self.get_valid_query_single(),
            return_fields=('pkey_grondmonster', 'boornummer', 'humusgehalte',
                           'methode'))

        assert df.humusgehalte[0] == 15.6
        assert df.methode[22] == 'AREOMETER'
