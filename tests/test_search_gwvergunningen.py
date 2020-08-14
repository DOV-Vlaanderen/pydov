"""Tests for grondwatervergunningen"""
from owslib.fes import PropertyIsEqualTo
from pandas import DataFrame

from pydov.search.gwvergunningen import GwvergunningenSearch
from pydov.types.gwvergunningen import Gwvergunningen
from tests.abstract import AbstractTestSearch

location_md_metadata = \
    'tests/data/types/gwvergunningen/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/gwvergunningen/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/gwvergunningen/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/gwvergunningen/' \
                          'wfsgetfeature.xml'
location_wfs_feature = \
    'tests/data/types/gwvergunningen/feature.xml'
location_dov_xml = \
    'tests/data/types/gwvergunningen/gwvergunningen.xml'
location_xsd_base = 'tests/data/types/gwvergunningen/xsd_*.xml'


class TestGwvergunningenSearch(AbstractTestSearch):

    search_instance = GwvergunningenSearch()
    datatype_class = Gwvergunningen

    valid_query_single = PropertyIsEqualTo(propertyname='installatie',
        literal='https://www.dov.vlaanderen.be/data/installatie/2019-088045')

    inexistent_field = 'onbestaand'
    xml_field = None
    wfs_field = 'installatie'

    valid_returnfields = ('pkey_vergunning',
                          'diepte')
    valid_returnfields_subtype = None
    valid_returnfields_extra = ('inrichtingsnummer', 'vergund_aantal_putten')

    df_default_columns = ['pkey_vergunning', 'pkey_installatie', 'x', 'y',
                          'diepte', 'exploitant_naam', 'watnr', 'vlaremrubriek',
                          'vergund_jaardebiet', 'vergund_dagdebiet',
                          'van_datum_termijn', 'tot_datum_termijn',
                          'aquifer_vergunning', 'inrichtingsklasse', 'nacebelcode',
                          'actie_waakgebied', 'cbbnr', 'kbonr']


    def test_search_customreturnfields(self, mp_get_schema,
                                       mp_remote_describefeaturetype,
                                       mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with custom return fields.

        Test whether the output dataframe is correct.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType .
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = self.search_instance.search(
            query=self.valid_query_single,
            return_fields=('pkey_vergunning', 'pkey_installatie',
                           ))

        assert isinstance(df, DataFrame)

        assert list(df) == ['pkey_vergunning', 'pkey_installatie',
                            ]

    def test_search_wfs_resolve(self, mp_get_schema,
                                mp_remote_describefeaturetype,
                                mp_remote_wfs_feature,):
        """Test the search method with return fields from WFS but not from
        XML.

        Test whether the output dataframe contains the resolved WFS data.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.

        """
        df = self.search_instance.search(
            query=self.valid_query_single,
            return_fields=('pkey_vergunning', 'diepte'))

        assert df.diepte[0] == 32.0
