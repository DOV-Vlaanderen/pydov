"""Module grouping tests for the observatie search module."""

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.observatie import ObservatieSearch
from pydov.types.observatie import Observatie, ObservatieHerhaling
from pydov.types.fields import ReturnFieldList
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/observatie/md_metadata.xml'
location_fc_featurecatalogue = 'tests/data/types/observatie/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = 'tests/data/types/observatie/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/observatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/observatie/feature.xml'
location_dov_xml = 'tests/data/types/observatie/observatie.xml'
location_codelists = 'tests/data/types/observatie'


class TestObservatieSearch(AbstractTestSearch):
    search_instance = ObservatieSearch()
    search_class = ObservatieSearch
    datatype_class = Observatie

    valid_query_single = PropertyIsEqualTo(propertyname='pkey_observatie',
                                           literal=build_dov_url('data/observatie/2022-11963810'))

    inexistent_field = 'onbestaand'
    wfs_field = 'parameter'
    xml_field = None

    valid_returnfields = ReturnFieldList.from_field_names(
        'pkey_observatie', 'fenomeentijd', 'diepte_van_m')
    valid_returnfields_subtype = ReturnFieldList.from_field_names()
    valid_returnfields_extra = ReturnFieldList.from_field_names()

    df_default_columns = ['pkey_observatie', 'pkey_parent', 'fenomeentijd', 'diepte_van_m', 'diepte_tot_m',
                          'parametergroep', 'parameter', 'detectieconditie', 'resultaat', 'eenheid', 'methode',
                          'uitvoerder', 'herkomst']

    def test_search_with_herhalingen(self, mp_wfs, mp_get_schema,
                                     mp_remote_describefeaturetype,
                                     mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with the subtype ObservatieHerhaling.

        Test whether the output dataframe contains the extra fields.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.
        """
        search_type = Observatie.with_subtype(ObservatieHerhaling)

        search_instance = self.search_class(
            objecttype=search_type)

        df = search_instance.search(
            query=self.valid_query_single)

        assert df.iloc[0].herhaling_aantal == 32
        assert df.iloc[0].herhaling_minimum == 1
        assert df.iloc[0].herhaling_maximum == 1
        assert df.iloc[0].herhaling_standaardafwijking == 0
