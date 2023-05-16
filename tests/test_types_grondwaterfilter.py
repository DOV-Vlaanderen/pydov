"""Module grouping tests for the pydov.types.boring module."""
from pydov.types.fields import ReturnFieldList
from pydov.types.grondwaterfilter import GrondwaterFilter
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/grondwaterfilter/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondwaterfilter/feature.xml'
location_dov_xml = 'tests/data/types/grondwaterfilter/grondwaterfilter.xml'


class TestGrondwaterFilter(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.grondwaterfilter.GrondwaterFilter class."""

    datatype_class = GrondwaterFilter
    namespace = 'http://dov.vlaanderen.be/grondwater/gw_meetnetten'
    pkey_base = build_dov_url('data/filter/')

    field_names = [
        'pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
        'filternummer', 'filtertype', 'x', 'y',
        'start_grondwaterlocatie_mtaw', 'mv_mtaw',
        'gemeente', 'meetnet_code', 'aquifer_code',
        'grondwaterlichaam_code', 'regime',
        'diepte_onderkant_filter', 'lengte_filter',
        'datum', 'tijdstip', 'peil_mtaw',
        'betrouwbaarheid', 'methode', 'filterstatus', 'filtertoestand']
    field_names_subtypes = [
        'datum', 'tijdstip', 'peil_mtaw', 'betrouwbaarheid',
        'methode']
    field_names_nosubtypes = [
        'pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
        'filternummer', 'filtertype', 'x', 'y',
        'start_grondwaterlocatie_mtaw', 'mv_mtaw',
        'gemeente', 'meetnet_code', 'aquifer_code',
        'grondwaterlichaam_code', 'regime',
        'diepte_onderkant_filter', 'lengte_filter']

    valid_returnfields = ReturnFieldList.from_field_names('pkey_filter', 'meetnet_code')
    valid_returnfields_subtype = ReturnFieldList.from_field_names('pkey_filter', 'peil_mtaw')

    inexistent_field = 'onbestaand'
