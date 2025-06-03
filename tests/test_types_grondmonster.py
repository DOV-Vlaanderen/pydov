"""Module grouping tests for the pydov.types.grondmonster module."""

from pydov.types.fields import ReturnFieldList
from pydov.types.grondmonster import Grondmonster
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/grondmonster/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondmonster/feature.xml'
location_dov_xml = 'tests/data/types/grondmonster/grondmonster.xml'


class TestGrondmonster(AbstractTestTypes):
    """Class grouping tests for the pydov.types.grondmonster.Grondmonster
    class."""

    datatype_class = Grondmonster
    namespace = 'http://dov.vlaanderen.be/ocdov/boringen'
    pkey_base = build_dov_url('data/monster/')

    field_names = [
        'pkey_grondmonster', 'naam', 'pkey_parents', 'datum', 'diepte_van_m',
        'diepte_tot_m', 'monstertype', 'monstersamenstelling', 'astm_naam',
        'grondsoort_bggg', 'humusgehalte', 'kalkgehalte',
        'uitrolgrens', 'vloeigrens', 'glauconiet_totaal',
        'korrelvolumemassa', 'volumemassa', 'watergehalte',
        'methode', 'diameter', 'fractie']
    field_names_subtypes = [
        'methode', 'diameter', 'fractie']
    field_names_nosubtypes = [
        'pkey_grondmonster', 'naam', 'pkey_parents', 'datum', 'diepte_van_m',
        'diepte_tot_m', 'monstertype', 'monstersamenstelling', 'astm_naam',
        'grondsoort_bggg', 'humusgehalte', 'kalkgehalte',
        'uitrolgrens', 'vloeigrens', 'glauconiet_totaal',
        'korrelvolumemassa', 'volumemassa', 'watergehalte']

    valid_returnfields = ReturnFieldList.from_field_names(
        'pkey_grondmonster', 'diepte_tot_m')
    valid_returnfields_subtype = ReturnFieldList.from_field_names(
        'diameter', 'fractie', 'methode')

    inexistent_field = 'onbestaand'
