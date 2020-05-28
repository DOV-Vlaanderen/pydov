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

    datatype_class = Sondering
    namespace = 'http://dov.vlaanderen.be/ocdov/dov-pub'
    pkey_base = build_dov_url('data/sondering/')

    field_names = [
        'pkey_sondering', 'sondeernummer', 'x', 'y',
        'start_sondering_mtaw', 'diepte_sondering_van',
        'diepte_sondering_tot', 'datum_aanvang', 'uitvoerder',
        'sondeermethode', 'apparaat', 'datum_gw_meting',
        'diepte_gw_m', 'z', 'qc', 'Qt', 'fs', 'u', 'i']
    field_names_subtypes = [
        'z', 'qc', 'Qt', 'fs', 'u', 'i']
    field_names_nosubtypes = [
        'pkey_sondering', 'sondeernummer', 'x', 'y',
        'start_sondering_mtaw', 'diepte_sondering_van',
        'diepte_sondering_tot', 'datum_aanvang', 'uitvoerder',
        'sondeermethode', 'apparaat', 'datum_gw_meting',
        'diepte_gw_m']

    valid_returnfields = ('pkey_sondering', 'sondeernummer')
    valid_returnfields_subtype = ('pkey_sondering', 'sondeernummer', 'z')

    inexistent_field = 'onbestaand'
