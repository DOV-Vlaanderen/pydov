"""Module grouping tests for the
pydov.types.interpretaties.LithologischeBeschrijvingen class."""
from pydov.types.interpretaties import LithologischeBeschrijvingen
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes
from tests.test_search_itp_lithologischebeschrijvingen import (
    location_dov_xml, location_wfs_feature, location_wfs_getfeature,
    mp_dov_xml, wfs_feature, wfs_getfeature)


class TestLithologischeBeschrijvingen(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.interpretaties.LithologischeBeschrijvingen class."""
    def get_type(self):
        return LithologischeBeschrijvingen

    def get_namespace(self):
        return 'http://dov.vlaanderen.be/ocdov/interpretaties'

    def get_pkey_base(self):
        return build_dov_url('data/interpretatie/')

    def get_field_names(self):
        return ['pkey_interpretatie', 'pkey_boring',
                'betrouwbaarheid_interpretatie', 'x', 'y',
                'diepte_laag_van', 'diepte_laag_tot', 'beschrijving']

    def get_field_names_subtypes(self):
        return ['diepte_laag_van', 'diepte_laag_tot', 'beschrijving']

    def get_field_names_nosubtypes(self):
        return ['pkey_interpretatie', 'pkey_boring',
                'betrouwbaarheid_interpretatie', 'x', 'y']

    def get_valid_returnfields(self):
        return ('pkey_interpretatie', 'pkey_boring')

    def get_valid_returnfields_subtype(self):
        return ('pkey_interpretatie', 'diepte_laag_van', 'diepte_laag_tot')

    def get_inexistent_field(self):
        return 'onbestaand'
