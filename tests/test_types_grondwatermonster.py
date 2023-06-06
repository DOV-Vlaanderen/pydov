"""Module grouping tests for the pydov.types.boring module."""
from pydov.types.fields import ReturnFieldList
from pydov.types.grondwatermonster import GrondwaterMonster
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/grondwatermonster/' \
    'wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondwatermonster/feature.xml'
location_dov_xml = 'tests/data/types/grondwatermonster/grondwatermonster.xml'


class TestGrondwaterMonster(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.grondwaterfilter.GrondwaterFilter class."""

    datatype_class = GrondwaterMonster
    namespace = 'http://dov.vlaanderen.be/grondwater/gw_meetnetten'
    pkey_base = build_dov_url('data/watermonster/')

    field_names = [
        'pkey_grondwatermonster', 'grondwatermonsternummer',
        'pkey_grondwaterlocatie', 'gw_id', 'pkey_filter',
        'filternummer', 'x', 'y', 'start_grondwaterlocatie_mtaw',
        'gemeente', 'datum_monstername', 'parametergroep',
        'parameter', 'detectie', 'waarde', 'eenheid', 'veld_labo']
    field_names_subtypes = [
        'parametergroep', 'parameter', 'detectie',
        'waarde', 'eenheid', 'veld_labo']
    field_names_nosubtypes = [
        'pkey_grondwatermonster', 'grondwatermonsternummer',
        'pkey_grondwaterlocatie', 'gw_id', 'pkey_filter',
        'filternummer', 'x', 'y', 'start_grondwaterlocatie_mtaw',
        'gemeente', 'datum_monstername']

    valid_returnfields = ReturnFieldList.from_field_names('y', 'gemeente')
    valid_returnfields_subtype = ReturnFieldList.from_field_names(
        'pkey_filter', 'pkey_grondwatermonster', 'eenheid')

    inexistent_field = 'onbestaand'
