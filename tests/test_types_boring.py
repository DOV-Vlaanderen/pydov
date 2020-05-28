"""Module grouping tests for the pydov.types.boring module."""

from pydov.types.boring import Boring
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes
from tests.test_search_boring import (location_dov_xml, location_wfs_feature,
                                      location_wfs_getfeature, mp_dov_xml,
                                      wfs_feature, wfs_getfeature)


class TestBoring(AbstractTestTypes):
    """Class grouping tests for the pydov.types.boring.Boring class."""
    def get_type(self):
        return Boring

    def get_namespace(self):
        return 'http://dov.vlaanderen.be/ocdov/dov-pub'

    def get_pkey_base(self):
        return build_dov_url('data/boring/')

    def get_field_names(self):
        return ['pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
                'start_boring_mtaw', 'gemeente', 'diepte_boring_van',
                'diepte_boring_tot', 'datum_aanvang', 'uitvoerder',
                'boorgatmeting', 'diepte_methode_van',
                'diepte_methode_tot', 'boormethode']

    def get_field_names_subtypes(self):
        return ['diepte_methode_van', 'diepte_methode_tot', 'boormethode']

    def get_field_names_nosubtypes(self):
        return ['pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
                'start_boring_mtaw', 'gemeente', 'diepte_boring_van',
                'diepte_boring_tot', 'datum_aanvang', 'uitvoerder',
                'boorgatmeting']

    def get_valid_returnfields(self):
        return ('pkey_boring', 'diepte_boring_tot')

    def get_valid_returnfields_subtype(self):
        return ('pkey_boring', 'diepte_methode_van', 'boormethode')

    def get_inexistent_field(self):
        return 'onbestaand'
