"""Module grouping tests for the search monster module."""

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.monster import MonsterSearch
from pydov.types.fields import ReturnFieldList
from pydov.types.monster import Monster
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
    valid_returnfields_extra = ReturnFieldList.from_field_names('observaties', 'opmerkingen')


    df_default_columns = [
        'pkey_monster', 'naam', 'pkey_parents', 'materiaalklasse',
        'datum_monstername', 'diepte_van_m', 'diepte_tot_m',
        'monstertype', 'monstersamenstelling', 'bemonsteringsprocedure', 'bemonsteringsinstrument',
        'bemonstering_door']


