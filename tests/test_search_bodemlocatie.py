"""Module grouping tests for the bodemlocatie search module."""
import datetime

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.bodemlocatie import BodemlocatieSearch
from pydov.types.bodemlocatie import Bodemlocatie
from pydov.types.fields import ReturnFieldList
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/bodemlocatie/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/bodemlocatie/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/bodemlocatie/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/bodemlocatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemlocatie/feature.xml'
location_dov_xml = 'tests/data/types/bodemlocatie/bodemlocatie.xml'
location_xsd_base = 'tests/data/types/bodemlocatie/xsd_*.xml'


class TestBodemlocatieSearch(AbstractTestSearch):

    search_instance = BodemlocatieSearch()
    datatype_class = Bodemlocatie

    valid_query_single = PropertyIsEqualTo(propertyname='naam',
                                           literal='STARC_4')

    inexistent_field = 'onbestaand'
    wfs_field = 'naam'
    xml_field = 'invoerdatum'

    valid_returnfields = ReturnFieldList.from_field_names('pkey_bodemlocatie', 'naam', 'waarnemingsdatum')
    valid_returnfields_subtype = ReturnFieldList.from_field_names(
        'pkey_bodemlocatie',
        'naam',
        'educatieve_waarde')
    valid_returnfields_extra = ReturnFieldList.from_field_names('pkey_bodemlocatie', 'naam', 'erfgoed')

    df_default_columns = ['pkey_bodemlocatie', 'pkey_bodemsite',
                          'naam', 'type', 'waarnemingsdatum', 'doel', 'x', 'y',
                          'mv_mtaw', 'erfgoed', 'bodemstreek',
                          'invoerdatum',
                          'educatieve_waarde']

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
        assert df.waarnemingsdatum.unique()[0] == datetime.date(2011, 9, 16)
