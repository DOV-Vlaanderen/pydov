"""Module grouping tests for the search monster module."""

import datetime
from owslib.fes2 import PropertyIsEqualTo
from pydov.search.monster import MonsterSearch
from pydov.types.fields import ReturnFieldList
from pydov.types.monster import Monster, MonsterDetails, Monsterbehandeling
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/monster/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/monster/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/monster/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/monster/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/monster/feature.xml'
location_dov_xml = 'tests/data/types/monster/monster.xml'
location_xsd_base = 'tests/data/types/monster/xsd_*.xml'


class TestMonsterSearch(AbstractTestSearch):

    search_instance = MonsterSearch()
    search_class = MonsterSearch
    datatype_class = Monster

    valid_query_single = PropertyIsEqualTo(propertyname='permkey_monster',
                                           literal='2017-143287')

    inexistent_field = 'onbestaand'
    wfs_field = 'bemonsteringsprocedure'
    xml_field = None
    valid_returnfields = ReturnFieldList.from_field_names(
        'pkey_monster', 'diepte_van_m')
    valid_returnfields_subtype = None
    valid_returnfields_extra = ReturnFieldList.from_field_names(
        'observaties', 'opmerkingen')

    df_default_columns = [
        'pkey_monster', 'naam', 'pkey_parents', 'materiaalklasse',
        'datum_monstername', 'diepte_van_m', 'diepte_tot_m',
        'monstertype', 'monstersamenstelling', 'bemonsteringsprocedure', 'bemonsteringsinstrument',
        'bemonstering_door']

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
        search_type = Monster.with_extra_fields(MonsterDetails)

        search_instance = self.search_class(
            objecttype=search_type)

        df = search_instance.search(
            query=self.valid_query_single)

        assert sorted(list(df)) == sorted(search_type.get_field_names())

    def test_search_with_monster_details(self, mp_get_schema,
                                         mp_remote_describefeaturetype,
                                         mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with an objecttype with the MonsterDetails
        fields.

        Test whether the output dataframe contains the extra fields and the
        values are correct.

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
        search_type = Monster.with_extra_fields(MonsterDetails)

        search_instance = self.search_class(
            objecttype=search_type)

        df = search_instance.search(
            query=self.valid_query_single)

        assert df.iloc[0].datum_monstername == datetime.date(2022, 1, 19)
        assert df.iloc[0].tijdstip_monstername == '10:00:00'

    def test_search_subtype_with_customxmlfield(
            self, mp_get_schema, mp_remote_describefeaturetype,
            mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with an objecttype with the Monsterbehandeling
        subtype.

        Test whether the output dataframe contains the extra fields and the
        values are correct. Especially test whether a result is returned
        from the custom XML fields from the subtype.

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
        search_type = Monster.with_subtype(Monsterbehandeling)

        search_instance = self.search_class(
            objecttype=search_type)

        df = search_instance.search(
            query=self.valid_query_single)

        assert df.iloc[0].monsterbehandeling_door == (
            'VO - Instituut voor Landbouw-, Visserij- en Voedingsonderzoek'
            ' (ILVO)')

        assert df.iloc[0].monsterbehandeling_behandeling == (
            'Monstervoorbereiding door')

        assert df.iloc[0].monsterbehandeling_behandeling_waarde == (
            'VO - Instituut voor Landbouw-, Visserij- en Voedingsonderzoek'
            ' (ILVO)')
