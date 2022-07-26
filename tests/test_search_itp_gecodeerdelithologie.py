"""Module grouping tests for the interpretaties search module."""
import pandas as pd
from owslib.fes import PropertyIsEqualTo
from pandas import DataFrame

from pydov.search.interpretaties import GecodeerdeLithologieSearch
from pydov.types.interpretaties import GecodeerdeLithologie
from tests.abstract import AbstractTestSearch

location_md_metadata = \
    'tests/data/types/interpretaties/gecodeerde_lithologie/' \
    'md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/interpretaties/gecodeerde_lithologie/' \
    'fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/interpretaties/gecodeerde_lithologie/' \
    'wfsdescribefeaturetype.xml'
location_wfs_getfeature = \
    'tests/data/types/interpretaties/gecodeerde_lithologie/' \
    'wfsgetfeature.xml'
location_wfs_feature = \
    'tests/data/types/interpretaties/gecodeerde_lithologie/feature.xml'
location_dov_xml = \
    'tests/data/types/interpretaties/gecodeerde_lithologie' \
    '/gecodeerde_lithologie.xml'
location_xsd_base = \
    'tests/data/types/interpretaties/gecodeerde_lithologie/xsd_*.xml'


class TestGecodeerdeLithologieSearch(AbstractTestSearch):

    search_instance = GecodeerdeLithologieSearch()
    datatype_class = GecodeerdeLithologie

    valid_query_single = PropertyIsEqualTo(propertyname='Proefnummer',
                                           literal='kb22d56w-B165')

    inexistent_field = 'onbestaand'
    wfs_field = 'Proefnummer'
    xml_field = 'grondsoort'

    valid_returnfields = ('pkey_interpretatie',
                          'betrouwbaarheid_interpretatie')
    valid_returnfields_subtype = (
        'pkey_interpretatie', 'diepte_laag_van', 'diepte_laag_tot')
    valid_returnfields_extra = ('pkey_interpretatie', 'gemeente')

    df_default_columns = ['pkey_interpretatie', 'pkey_boring',
                          'betrouwbaarheid_interpretatie', 'x', 'y',
                          'start_interpretatie_mtaw',
                          'diepte_laag_van', 'diepte_laag_tot',
                          'hoofdnaam1_grondsoort', 'hoofdnaam2_grondsoort',
                          'bijmenging1_plaatselijk', 'bijmenging1_hoeveelheid',
                          'bijmenging1_grondsoort', 'bijmenging2_plaatselijk',
                          'bijmenging2_hoeveelheid', 'bijmenging2_grondsoort',
                          'bijmenging3_plaatselijk', 'bijmenging3_hoeveelheid',
                          'bijmenging3_grondsoort']

    def test_search_nan(self, mp_wfs, mp_get_schema,
                        mp_remote_describefeaturetype, mp_remote_md,
                        mp_remote_fc, mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with only the query parameter.

        Test whether the result is correct.

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
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        self.search_instance.search(
            query=self.valid_query_single)

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
            return_fields=('pkey_interpretatie', 'pkey_boring'))

        assert isinstance(df, DataFrame)

        assert list(df) == ['pkey_interpretatie', 'pkey_boring']

        assert not pd.isnull(df.pkey_boring[0])

    def test_search_xml_resolve(self, mp_get_schema,
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
            return_fields=('pkey_interpretatie', 'diepte_laag_tot'))

        assert df.diepte_laag_tot[0] == 4.

    def test_search_multiple_return(self, mp_get_schema,
                                    mp_remote_describefeaturetype,
                                    mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method returning multiple (sub)elements of the same subject.

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
            return_fields=('pkey_interpretatie',
                           'hoofdnaam1_grondsoort',
                           'hoofdnaam2_grondsoort',
                           'bijmenging1_grondsoort',
                           'bijmenging1_hoeveelheid',
                           'bijmenging1_plaatselijk',
                           'bijmenging2_grondsoort',
                           'bijmenging3_grondsoort'))

        assert df.hoofdnaam1_grondsoort[4] == 'XZ'
        assert df.hoofdnaam2_grondsoort[4] == 'KL'
        assert df.bijmenging1_grondsoort[4] == 'GL'
        assert df.bijmenging1_hoeveelheid[2] == 'M'
        # mind that the column below is of dtype 'object'
        assert df.bijmenging1_plaatselijk[2] is False
        assert df.bijmenging2_grondsoort[5] == 'GL'
        assert df.bijmenging3_grondsoort[8] == 'NN'
