"""Module grouping tests for the pydov.types.sondering module."""

from pydov.types.sondering import Sondering
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes
from tests.test_search_sondering import (location_dov_xml,
                                         location_wfs_feature,
                                         location_wfs_getfeature, mp_dov_xml,
                                         wfs_feature, wfs_getfeature)


class TestSondering(AbstractTestTypes):
    """Class grouping tests for the pydov.types.sondering.Sondering class."""
    def get_type(self):
        return Sondering

    def get_namespace(self):
        return 'http://dov.vlaanderen.be/ocdov/dov-pub'

    def get_pkey_base(self):
        return build_dov_url('data/sondering/')

    def get_field_names(self):
        return ['pkey_sondering', 'sondeernummer', 'x', 'y',
                'start_sondering_mtaw', 'diepte_sondering_van',
                'diepte_sondering_tot', 'datum_aanvang', 'uitvoerder',
                'sondeermethode', 'apparaat', 'datum_gw_meting',
                'diepte_gw_m', 'z', 'qc', 'Qt', 'fs', 'u', 'i']

    def get_field_names_subtypes(self):
        return ['z', 'qc', 'Qt', 'fs', 'u', 'i']

    def get_field_names_nosubtypes(self):
        return ['pkey_sondering', 'sondeernummer', 'x', 'y',
                'start_sondering_mtaw', 'diepte_sondering_van',
                'diepte_sondering_tot', 'datum_aanvang', 'uitvoerder',
                'sondeermethode', 'apparaat', 'datum_gw_meting',
                'diepte_gw_m']

    def get_valid_returnfields(self):
        return ('pkey_sondering', 'sondeernummer')

    def get_valid_returnfields_subtype(self):
        return ('pkey_sondering', 'sondeernummer', 'z')

    def get_inexistent_field(self):
        return 'onbestaand'
