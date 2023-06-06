"""Module grouping tests for the sondering search module."""
import datetime

import pandas as pd
from owslib.fes2 import PropertyIsEqualTo

from pydov.search.sondering import SonderingSearch
from pydov.types.fields import ReturnFieldList
from pydov.types.sondering import Sondering
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/sondering/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/sondering/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/sondering/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/sondering/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/sondering/feature.xml'
location_dov_xml = 'tests/data/types/sondering/sondering.xml'
location_xsd_base = 'tests/data/types/sondering/xsd_*.xml'


class TestSonderingSearch(AbstractTestSearch):

    search_instance = SonderingSearch()
    datatype_class = Sondering

    valid_query_single = PropertyIsEqualTo(propertyname='sondeernummer',
                                           literal='GEO-61/3075-S1')

    inexistent_field = 'onbestaand'
    wfs_field = 'sondeernummer'
    xml_field = 'gw_meting'

    valid_returnfields = ReturnFieldList.from_field_names(
        'pkey_sondering', 'sondeernummer', 'diepte_sondering_tot',
                          'datum_aanvang')
    valid_returnfields_subtype = ReturnFieldList.from_field_names(
        'pkey_sondering', 'sondeernummer', 'lengte', 'qc', 'Qt')
    valid_returnfields_extra = ReturnFieldList.from_field_names('pkey_sondering', 'conus')

    df_default_columns = [
        'pkey_sondering', 'sondeernummer', 'x', 'y', 'mv_mtaw',
        'start_sondering_mtaw', 'diepte_sondering_van',
        'diepte_sondering_tot', 'datum_aanvang', 'uitvoerder',
        'sondeermethode', 'apparaat', 'datum_gw_meting',
        'diepte_gw_m', 'lengte', 'diepte', 'qc', 'Qt', 'fs', 'u', 'i']

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
        assert df.datum_aanvang.unique()[0] == datetime.date(2002, 12, 17)

        assert pd.Timestamp(
            df.datum_gw_meting.unique()[0]).to_pydatetime() == \
            datetime.datetime(2002, 12, 17, 14, 30, 0, 0)

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
        df = self.search_instance.search(
            query=self.valid_query_single)

        assert df.Qt.hasnans

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
            return_fields=('pkey_sondering', 'sondeernummer', 'diepte_gw_m'))

        assert df.diepte_gw_m[0] == 3.60
