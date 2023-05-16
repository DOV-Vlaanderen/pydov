"""Module grouping tests for the search grondwatermonster module."""
import datetime

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.grondwatermonster import GrondwaterMonsterSearch
from pydov.types.fields import ReturnFieldList
from pydov.types.grondwatermonster import GrondwaterMonster
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/grondwatermonster/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/grondwatermonster/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/grondwatermonster/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/grondwatermonster/' \
    'wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondwatermonster/feature.xml'
location_dov_xml = 'tests/data/types/grondwatermonster/grondwatermonster.xml'
location_xsd_base = 'tests/data/types/grondwatermonster/xsd_*.xml'


class TestGrondwaterMonsterSearch(AbstractTestSearch):

    search_instance = GrondwaterMonsterSearch()
    datatype_class = GrondwaterMonster

    valid_query_single = PropertyIsEqualTo(
        propertyname='grondwatermonsterfiche',
        literal=build_dov_url('data/watermonster/2006-115684'))

    inexistent_field = 'onbestaand'
    wfs_field = 'kationen'
    xml_field = 'eenheid'

    valid_returnfields = ReturnFieldList.from_field_names('pkey_grondwatermonster', 'datum_monstername')
    valid_returnfields_subtype = ReturnFieldList.from_field_names(
        'pkey_grondwatermonster', 'datum_monstername', 'eenheid')
    valid_returnfields_extra = ReturnFieldList.from_field_names('pkey_grondwatermonster', 'kationen')

    df_default_columns = [
        'pkey_grondwatermonster', 'grondwatermonsternummer',
        'pkey_grondwaterlocatie', 'gw_id', 'pkey_filter',
        'filternummer', 'x', 'y', 'start_grondwaterlocatie_mtaw',
        'gemeente', 'datum_monstername', 'parametergroep',
        'parameter', 'detectie', 'waarde', 'eenheid', 'veld_labo']

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
        assert df.datum_monstername.sort_values()[0] == datetime.date(
            2006, 5, 19)
