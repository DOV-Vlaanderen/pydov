"""Module grouping tests for the pydov.types.grondmonster module."""

from pydov.types.grondmonster import Grondmonster
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes
from tests.test_search_grondmonster import (location_dov_xml,
                                            location_wfs_feature,
                                            location_wfs_getfeature,
                                            mp_dov_xml, wfs_feature,
                                            wfs_getfeature)


class TestGrondmonster(AbstractTestTypes):
    """Class grouping tests for the pydov.types.grondmonster.Grondmonster
    class."""

    datatype_class = Grondmonster
    namespace = 'http://dov.vlaanderen.be/ocdov/boringen'
    pkey_base = build_dov_url('data/grondmonster/')

    field_names = [
        'pkey_grondmonster', 'naam', 'pkey_boring', 'boornummer',
        'datum', 'x', 'y', 'gemeente', 'diepte_van_m', 'diepte_tot_m',
        'peil_van_mtaw', 'peil_tot_mtaw', 'monstertype', 'astm_naam',
        'grondsoort_bggg', 'humusgehalte', 'kalkgehalte',
        'uitrolgrens', 'vloeigrens', 'glauconiet',
        'korrelvolumemassa', 'volumemassa', 'watergehalte',
        'diameter', 'fractie', 'methode']
    field_names_subtypes = [
        'diepte_methode_van', 'diepte_methode_tot', 'boormethode']
    field_names_nosubtypes = [
        'pkey_grondmonster', 'naam', 'pkey_boring', 'boornummer',
        'datum', 'x', 'y', 'gemeente', 'diepte_van_m', 'diepte_tot_m',
        'peil_van_mtaw', 'peil_tot_mtaw', 'monstertype', 'astm_naam',
        'grondsoort_bggg', 'humusgehalte', 'kalkgehalte',
        'uitrolgrens', 'vloeigrens', 'glauconiet',
        'korrelvolumemassa', 'volumemassa', 'watergehalte']

    valid_returnfields = ('pkey_grondmonster', 'diepte_tot_m')
    valid_returnfields_subtype = ('diameter', 'fractie', 'methode')

    inexistent_field = 'onbestaand'
