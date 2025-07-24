"""Module grouping tests for the observatie search module, focussing on
observaties with fractiemetingen."""

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.observatie import ObservatieFractiemetingSearch, Fractiemeting, ObservatieSearch
from pydov.types.fields import ReturnFieldList
from pydov.types.observatie import Observatie
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/observatie_fractiemeting/md_metadata.xml'
location_fc_featurecatalogue = 'tests/data/types/observatie_fractiemeting/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = 'tests/data/types/observatie_fractiemeting/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/observatie_fractiemeting/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/observatie_fractiemeting/feature.xml'
location_dov_xml = 'tests/data/types/observatie_fractiemeting/observatie.xml'
location_codelists = 'tests/data/types/observatie_fractiemeting'


class TestObservatieFractiemetingSearch(AbstractTestSearch):
    search_instance = ObservatieFractiemetingSearch()
    search_class = ObservatieFractiemetingSearch
    datatype_class = Observatie.with_subtype(Fractiemeting)

    valid_query_single = PropertyIsEqualTo(propertyname='pkey_observatie',
                                           literal=build_dov_url('data/observatie/1995-10282748'))

    inexistent_field = 'onbestaand'
    wfs_field = 'parameter'
    xml_field = None

    valid_returnfields = ReturnFieldList.from_field_names(
        'pkey_observatie', 'fenomeentijd', 'diepte_van_m')
    valid_returnfields_subtype = ReturnFieldList.from_field_names()
    valid_returnfields_extra = ReturnFieldList.from_field_names()

    df_default_columns = [
        'pkey_observatie', 'pkey_parent', 'fenomeentijd', 'diepte_van_m', 'diepte_tot_m',
        'parametergroep', 'parameter', 'detectieconditie', 'resultaat', 'eenheid', 'methode',
        'uitvoerder', 'herkomst', 'fractiemeting_ondergrens', 'fractiemeting_bovengrens',
        'fractiemeting_waarde']

    def test_search(self, mp_wfs, mp_get_schema,
                    mp_remote_codelist,
                    mp_remote_describefeaturetype,
                    mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method.

        Test whether the output dataframe contains the correct fields.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_codelist : pytest.fixture
            Monkeypatch the call to get remote codelists.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.
        """
        df = self.search_instance.search(
            query=self.valid_query_single)

        assert round(df.iloc[0].fractiemeting_ondergrens, 2) == 0
        assert round(df.iloc[0].fractiemeting_bovengrens, 2) == 2
        assert round(df.iloc[0].fractiemeting_waarde, 2) == 10.17

    def test_search_observatie(self, mp_wfs, mp_get_schema,
                               mp_remote_codelist,
                               mp_remote_describefeaturetype,
                               mp_remote_wfs_feature, mp_dov_xml):
        """Test whether the extra fields are returned when using the
        normal ObservatieSearch too.

        Test whether the output dataframe contains the correct fields.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_codelist : pytest.fixture
            Monkeypatch the call to get remote codelists.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.
        """
        search_instance = ObservatieSearch(
            Observatie.with_subtype(Fractiemeting))

        df = search_instance.search(
            query=self.valid_query_single)

        assert round(df.iloc[0].fractiemeting_ondergrens, 2) == 0
        assert round(df.iloc[0].fractiemeting_bovengrens, 2) == 2
        assert round(df.iloc[0].fractiemeting_waarde, 2) == 10.17
