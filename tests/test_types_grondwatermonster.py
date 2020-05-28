"""Module grouping tests for the pydov.types.boring module."""
from pydov.types.grondwatermonster import GrondwaterMonster
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes
from tests.test_search_grondwatermonster import (location_dov_xml,
                                                 location_wfs_feature,
                                                 location_wfs_getfeature,
                                                 mp_dov_xml, wfs_feature,
                                                 wfs_getfeature)


class TestGrondwaterMonster(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.grondwaterfilter.GrondwaterFilter class."""
    def get_type(self):
        return GrondwaterMonster

    def get_namespace(self):
        return 'http://dov.vlaanderen.be/grondwater/gw_meetnetten'

    def get_pkey_base(self):
        return build_dov_url('data/watermonster/')

    def get_field_names(self):
        return ['pkey_grondwatermonster', 'grondwatermonsternummer',
                'pkey_grondwaterlocatie', 'gw_id', 'pkey_filter',
                'filternummer', 'x', 'y', 'start_grondwaterlocatie_mtaw',
                'gemeente', 'datum_monstername', 'parametergroep',
                'parameter', 'detectie', 'waarde', 'eenheid', 'veld_labo']

    def get_field_names_subtypes(self):
        return ['parametergroep', 'parameter', 'detectie',
                'waarde', 'eenheid', 'veld_labo']

    def get_field_names_nosubtypes(self):
        return ['pkey_grondwatermonster', 'grondwatermonsternummer',
                'pkey_grondwaterlocatie', 'gw_id', 'pkey_filter',
                'filternummer', 'x', 'y', 'start_grondwaterlocatie_mtaw',
                'gemeente', 'datum_monstername']

    def get_valid_returnfields(self):
        return ('y', 'gemeente')

    def get_valid_returnfields_subtype(self):
        return ('pkey_filter', 'pkey_grondwatermonster', 'eenheid')

    def get_inexistent_field(self):
        return 'onbestaand'
