"""Module grouping tests for the
pydov.types.interpretaties.LithologischeBeschrijvingen class."""
from pydov.types.interpretaties import LithologischeBeschrijvingen
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = \
    'tests/data/types/interpretaties/lithologische_beschrijvingen/' \
    'wfsgetfeature.xml'
location_wfs_feature = \
    'tests/data/types/interpretaties/lithologische_beschrijvingen/feature.xml'
location_dov_xml = \
    'tests/data/types/interpretaties/lithologische_beschrijvingen' \
    '/lithologische_beschrijvingen.xml'


class TestLithologischeBeschrijvingen(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.interpretaties.LithologischeBeschrijvingen class."""

    datatype_class = LithologischeBeschrijvingen
    namespace = 'http://dov.vlaanderen.be/ocdov/interpretaties'
    pkey_base = build_dov_url('data/interpretatie/')

    field_names = [
        'pkey_interpretatie', 'pkey_boring',
        'betrouwbaarheid_interpretatie', 'x', 'y',
        'diepte_laag_van', 'diepte_laag_tot', 'beschrijving']
    field_names_subtypes = [
        'diepte_laag_van', 'diepte_laag_tot', 'beschrijving']
    field_names_nosubtypes = [
        'pkey_interpretatie', 'pkey_boring',
        'betrouwbaarheid_interpretatie', 'x', 'y']

    valid_returnfields = ('pkey_interpretatie', 'pkey_boring')
    valid_returnfields_subtype = (
        'pkey_interpretatie', 'diepte_laag_van', 'diepte_laag_tot')

    inexistent_field = 'onbestaand'
