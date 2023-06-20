"""Module grouping tests for the search grondwaterfilter module."""
import datetime

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.grondwaterfilter import GrondwaterFilterSearch
from pydov.types.fields import ReturnFieldList
from pydov.types.grondwaterfilter import GrondwaterFilter
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/grondwaterfilter/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/grondwaterfilter/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/grondwaterfilter/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/grondwaterfilter/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondwaterfilter/feature.xml'
location_dov_xml = 'tests/data/types/grondwaterfilter/grondwaterfilter.xml'
location_xsd_base = 'tests/data/types/grondwaterfilter/xsd_*.xml'


class TestGrondwaterfilterSearch(AbstractTestSearch):

    search_instance = GrondwaterFilterSearch()
    datatype_class = GrondwaterFilter

    valid_query_single = PropertyIsEqualTo(propertyname='filterfiche',
                                           literal=build_dov_url(
                                               'data/filter/2003-004471'))

    inexistent_field = 'onbestaand'
    wfs_field = 'filternummer'
    xml_field = 'peil_mtaw'

    valid_returnfields = ReturnFieldList.from_field_names('pkey_filter', 'filternummer')
    valid_returnfields_subtype = ReturnFieldList.from_field_names('pkey_filter', 'filternummer', 'peil_mtaw')
    valid_returnfields_extra = ReturnFieldList.from_field_names('pkey_filter', 'beheerder')

    df_default_columns = ['pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
                          'filternummer', 'filtertype', 'x', 'y',
                          'start_grondwaterlocatie_mtaw', 'mv_mtaw',
                          'gemeente', 'meetnet_code', 'aquifer_code',
                          'grondwaterlichaam_code', 'regime',
                          'diepte_onderkant_filter', 'lengte_filter',
                          'datum', 'tijdstip', 'peil_mtaw',
                          'betrouwbaarheid', 'methode', 'filterstatus',
                          'filtertoestand']

    def test_search_date(self, mp_wfs, mp_get_schema,
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
        df = self.search_instance.search(
            query=self.valid_query_single)

        # specific test for the Zulu time wfs 1.1.0 issue
        assert df.datum.sort_values()[0] == datetime.date(2004, 4, 7)

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
            return_fields=('pkey_filter', 'gw_id', 'filternummer',
                           'meetnet_code'))

        assert df.meetnet_code[0] == '8'
