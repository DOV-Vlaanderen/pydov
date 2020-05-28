"""Module grouping tests for the pydov.types.boring module."""
from pydov.types.grondwaterfilter import GrondwaterFilter
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes
from tests.test_search_grondwaterfilter import (location_dov_xml,
                                                location_wfs_feature,
                                                location_wfs_getfeature,
                                                mp_dov_xml, wfs_feature,
                                                wfs_getfeature)


class TestGrondwaterFilter(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.grondwaterfilter.GrondwaterFilter class."""
    def get_type(self):
        return GrondwaterFilter

    def get_namespace(self):
        return 'http://dov.vlaanderen.be/grondwater/gw_meetnetten'

    def get_pkey_base(self):
        return build_dov_url('data/filter/')

    def get_field_names(self):
        return ['pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
                'filternummer', 'filtertype', 'x', 'y',
                'start_grondwaterlocatie_mtaw', 'mv_mtaw',
                'gemeente', 'meetnet_code', 'aquifer_code',
                'grondwaterlichaam_code', 'regime',
                'diepte_onderkant_filter', 'lengte_filter',
                'datum', 'tijdstip', 'peil_mtaw',
                'betrouwbaarheid', 'methode', 'filterstatus', 'filtertoestand']

    def get_field_names_subtypes(self):
        return ['datum', 'tijdstip', 'peil_mtaw', 'betrouwbaarheid',
                'methode']

    def get_field_names_nosubtypes(self):
        return ['pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
                'filternummer', 'filtertype', 'x', 'y',
                'start_grondwaterlocatie_mtaw', 'mv_mtaw',
                'gemeente', 'meetnet_code', 'aquifer_code',
                'grondwaterlichaam_code', 'regime',
                'diepte_onderkant_filter', 'lengte_filter']

    def get_valid_returnfields(self):
        return ('pkey_filter', 'meetnet_code')

    def get_valid_returnfields_subtype(self):
        return ('pkey_filter', 'peil_mtaw')

    def get_inexistent_field(self):
        return 'onbestaand'
