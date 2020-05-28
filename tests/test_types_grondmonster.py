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
    """Class grouping tests for the pydov.types.grondmonster.Grondmonster class."""
    def get_type(self):
        return Grondmonster

    def get_namespace(self):
        return 'http://dov.vlaanderen.be/ocdov/boringen'

    def get_pkey_base(self):
        return build_dov_url('data/grondmonster/')

    def get_field_names(self):
        return ['pkey_grondmonster', 'naam', 'pkey_boring', 'boornummer',
                'datum', 'x', 'y', 'gemeente', 'diepte_van_m', 'diepte_tot_m',
                'peil_van_mtaw', 'peil_tot_mtaw', 'monstertype', 'astm_naam',
                'grondsoort_bggg', 'humusgehalte', 'kalkgehalte',
                'uitrolgrens', 'vloeigrens', 'glauconiet',
                'korrelvolumemassa', 'volumemassa', 'watergehalte',
                'diameter', 'fractie', 'methode']

    def get_field_names_subtypes(self):
        return ['diepte_methode_van', 'diepte_methode_tot', 'boormethode']

    def get_field_names_nosubtypes(self):
        return ['pkey_grondmonster', 'naam', 'pkey_boring', 'boornummer',
                'datum', 'x', 'y', 'gemeente', 'diepte_van_m', 'diepte_tot_m',
                'peil_van_mtaw', 'peil_tot_mtaw', 'monstertype', 'astm_naam',
                'grondsoort_bggg', 'humusgehalte', 'kalkgehalte',
                'uitrolgrens', 'vloeigrens', 'glauconiet',
                'korrelvolumemassa', 'volumemassa', 'watergehalte']

    def get_valid_returnfields(self):
        return ('pkey_grondmonster', 'diepte_tot_m')

    def get_valid_returnfields_subtype(self):
        return ('diameter', 'fractie', 'methode')

    def get_inexistent_field(self):
        return 'onbestaand'
