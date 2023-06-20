"""Module grouping tests for the pydov.types.sondering module."""

from pydov.types.fields import ReturnFieldList
from pydov.types.sondering import Sondering
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/sondering/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/sondering/feature.xml'
location_dov_xml = 'tests/data/types/sondering/sondering.xml'


class TestSondering(AbstractTestTypes):
    """Class grouping tests for the pydov.types.sondering.Sondering class."""

    datatype_class = Sondering
    namespace = 'http://dov.vlaanderen.be/ocdov/dov-pub'
    pkey_base = build_dov_url('data/sondering/')

    field_names = [
        'pkey_sondering', 'sondeernummer', 'x', 'y', 'mv_mtaw',
        'start_sondering_mtaw', 'diepte_sondering_van',
        'diepte_sondering_tot', 'datum_aanvang', 'uitvoerder',
        'sondeermethode', 'apparaat', 'datum_gw_meting',
        'diepte_gw_m', 'lengte', 'diepte', 'qc', 'Qt', 'fs', 'u', 'i']
    field_names_subtypes = [
        'lengte', 'diepte', 'qc', 'Qt', 'fs', 'u', 'i']
    field_names_nosubtypes = [
        'pkey_sondering', 'sondeernummer', 'x', 'y', 'mv_mtaw',
        'start_sondering_mtaw', 'diepte_sondering_van',
        'diepte_sondering_tot', 'datum_aanvang', 'uitvoerder',
        'sondeermethode', 'apparaat', 'datum_gw_meting',
        'diepte_gw_m']

    valid_returnfields = ReturnFieldList.from_field_names('pkey_sondering', 'sondeernummer')
    valid_returnfields_subtype = ReturnFieldList.from_field_names('pkey_sondering', 'sondeernummer', 'z')

    inexistent_field = 'onbestaand'
