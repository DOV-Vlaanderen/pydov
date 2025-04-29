"""Module grouping tests for the pydov.types.monster module."""

from pydov.types.fields import ReturnFieldList
from pydov.types.monster import Monster
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/monster/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/monster/feature.xml'
location_dov_xml = 'tests/data/types/monster/monster.xml'


class TestMonster(AbstractTestTypes):
    """Class grouping tests for the pydov.types.monster.Monster
    class."""

    datatype_class = Monster
    namespace = 'http://dov.vlaanderen.be/ocdov/monster'
    pkey_base = build_dov_url('data/monster/')

    field_names = [
        'pkey_monster', 'naam', 'pkey_parents', 'materiaalklasse',
        'datum_monstername', 'diepte_van_m', 'diepte_tot_m',
        'monstertype', 'monstersamenstelling', 'bemonsteringsprocedure', 'bemonsteringsinstrument',
        'bemonstering_door', 'bemonsterd_object_type',
        'bemonsterd_object_naam', 'bemonsterd_object_permkey']
    field_names_subtypes = [
        'bemonsterd_object_type',
        'bemonsterd_object_naam', 'bemonsterd_object_permkey']
    field_names_nosubtypes = [
        'pkey_monster', 'naam', 'pkey_parents', 'materiaalklasse',
        'datum_monstername', 'diepte_van_m', 'diepte_tot_m',
        'monstertype', 'monstersamenstelling', 'bemonsteringsprocedure', 'bemonsteringsinstrument',
        'bemonstering_door']


    valid_returnfields = ReturnFieldList.from_field_names(
        'pkey_monster', 'diepte_tot_m')
    valid_returnfields_subtype = ReturnFieldList.from_field_names(
        'monster_link','bemonsterd_object_type', 'bemonsterd_object_naam', 'bemonsterd_object_permkey')
    inexistent_field = 'onbestaand'


