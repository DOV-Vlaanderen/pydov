"""Module grouping tests for the pydov.types.boring module."""

from pydov.types.boring import Boring
from pydov.types.fields import ReturnFieldList
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/boring/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/boring/feature.xml'
location_dov_xml = 'tests/data/types/boring/boring.xml'


class TestBoring(AbstractTestTypes):
    """Class grouping tests for the pydov.types.boring.Boring class."""

    datatype_class = Boring
    namespace = 'http://dov.vlaanderen.be/ocdov/dov-pub'
    pkey_base = build_dov_url('data/boring/')

    field_names = [
        'pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
        'start_boring_mtaw', 'gemeente', 'diepte_boring_van',
        'diepte_boring_tot', 'datum_aanvang', 'uitvoerder',
        'boorgatmeting', 'diepte_methode_van',
        'diepte_methode_tot', 'boormethode']
    field_names_subtypes = [
        'diepte_methode_van',
        'diepte_methode_tot', 'boormethode']
    field_names_nosubtypes = [
        'pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
        'start_boring_mtaw', 'gemeente', 'diepte_boring_van',
        'diepte_boring_tot', 'datum_aanvang', 'uitvoerder',
        'boorgatmeting']

    valid_returnfields = ReturnFieldList.from_field_names('pkey_boring', 'diepte_boring_tot')
    valid_returnfields_subtype = ReturnFieldList.from_field_names(
        'pkey_boring', 'diepte_methode_van', 'boormethode')

    inexistent_field = 'onbestaand'
