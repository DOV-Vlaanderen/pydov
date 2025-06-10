"""Module grouping tests for the boring search module."""
import datetime

import pytest

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.boring import BoringSearch
from pydov.types.boring import Boring, MethodeXyz
from pydov.types.fields import GeometryReturnField, ReturnFieldList
from tests.abstract import AbstractTestSearch, ServiceCheck

location_md_metadata = 'tests/data/types/boring/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/boring/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/boring/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/boring/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/boring/feature.xml'
location_dov_xml = 'tests/data/types/boring/boring.xml'
location_codelists = 'tests/data/types/boring'


class TestBoringSearch(AbstractTestSearch):

    datatype_class = Boring
    search_class = BoringSearch
    search_instance = BoringSearch()

    valid_query_single = PropertyIsEqualTo(propertyname='boornummer',
                                           literal='GEO-04/169-BNo-B1')

    inexistent_field = 'onbestaand'
    wfs_field = 'boornummer'
    xml_field = 'boormethode'

    valid_returnfields = ReturnFieldList.from_field_names('pkey_boring', 'boornummer', 'diepte_boring_tot',
                                                          'datum_aanvang')
    valid_returnfields_subtype = ReturnFieldList.from_field_names('pkey_boring', 'boornummer',
                                                                  'diepte_methode_van', 'diepte_methode_tot')
    valid_returnfields_extra = ReturnFieldList.from_field_names('pkey_boring', 'doel')

    df_default_columns = ['pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
                          'start_boring_mtaw', 'gemeente',
                          'diepte_boring_van', 'diepte_boring_tot',
                          'datum_aanvang', 'uitvoerder', 'boorgatmeting',
                          'diepte_methode_van', 'diepte_methode_tot',
                          'boormethode']

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
        assert df.datum_aanvang.unique()[0] == datetime.date(2004, 12, 20)

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

        assert df.mv_mtaw.hasnans

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
            return_fields=('pkey_boring', 'boornummer', 'boorgatmeting'))

        assert not df.boorgatmeting[0]

    def test_get_fields_with_extra_fields(self, mp_get_schema,
                                          mp_remote_describefeaturetype,
                                          mp_remote_wfs_feature, mp_dov_xml):
        """Test the get_fields method with an objecttype with extra fields.

        Test whether the get_fields contains the extra fields.

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
        search_instance = self.search_class(
            objecttype=Boring.with_extra_fields(MethodeXyz))

        fields = search_instance.get_fields()

        for field in MethodeXyz.get_field_names():
            assert field in fields

    def test_search_with_extra_fields(self, mp_get_schema,
                                      mp_remote_describefeaturetype,
                                      mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with an objecttype with extra fields.

        Test whether the output dataframe contains the extra fields.

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
        search_type = Boring.with_extra_fields(MethodeXyz)

        search_instance = self.search_class(
            objecttype=search_type)

        df = search_instance.search(
            query=self.valid_query_single)

        assert sorted(list(df)) == sorted(search_type.get_field_names())

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_geometry_coordinate_order_4326(self):
        """Test whether the order of the returned coordinates is correct for
        the EPSG:4326 coordinate system.

        """
        df = self.search_instance.search(
            query=self.valid_query_single,
            return_fields=[
                'pkey_boring', GeometryReturnField('geom', 4326)]
        )

        assert round(df.geom.iloc[0].x, 2) == 4.39
        assert round(df.geom.iloc[0].y, 2) == 51.24

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_geometry_coordinate_order_31370(self):
        """Test whether the order of the returned coordinates is correct for
        the EPSG:31370 coordinate system.

        """
        df = self.search_instance.search(
            query=self.valid_query_single,
            return_fields=[
                'pkey_boring', GeometryReturnField('geom', 31370)]
        )

        assert round(df.geom.iloc[0].x, 2) == 151680.75
        assert round(df.geom.iloc[0].y, 2) == 214678.06
