"""Module grouping tests for the bodemsite search module."""
import datetime

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.bodemsite import BodemsiteSearch
from pydov.types.bodemsite import Bodemsite
from pydov.types.fields import ReturnFieldList
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/bodemsite/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/bodemsite/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/bodemsite/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/bodemsite/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemsite/feature.xml'
location_dov_xml = 'tests/data/types/bodemsite/bodemsite.xml'
location_xsd_base = 'tests/data/types/bodemsite/xsd_*.xml'


class TestBodemsiteSearch(AbstractTestSearch):

    search_instance = BodemsiteSearch()
    datatype_class = Bodemsite

    valid_query_single = PropertyIsEqualTo(propertyname='naam',
                                           literal='Meise_Neerpoorten')

    inexistent_field = 'onbestaand'
    wfs_field = 'naam'
    xml_field = 'invoerdatum'

    valid_returnfields = ReturnFieldList.from_field_names('pkey_bodemsite', 'naam', 'waarnemingsdatum')
    valid_returnfields_subtype = ReturnFieldList.from_field_names('pkey_bodemsite', 'naam', 'invoerdatum')
    valid_returnfields_extra = ReturnFieldList.from_field_names(
        'pkey_bodemsite',
        'naam',
        'Aantal_bodemlocaties')

    df_default_columns = ['pkey_bodemsite', 'naam', 'waarnemingsdatum',
                          'beschrijving', 'invoerdatum']

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
        assert df.waarnemingsdatum.unique()[0] == datetime.date(2013, 9, 16)
