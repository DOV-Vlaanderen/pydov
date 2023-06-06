"""Module grouping tests for the
pydov.types.interpretaties.InformeleStratigrafie class."""
from pydov.types.fields import ReturnFieldList
from pydov.types.interpretaties import GecodeerdeLithologie
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = \
    'tests/data/types/interpretaties/gecodeerde_lithologie/' \
    'wfsgetfeature.xml'
location_wfs_feature = \
    'tests/data/types/interpretaties/gecodeerde_lithologie/feature.xml'
location_dov_xml = \
    'tests/data/types/interpretaties/gecodeerde_lithologie' \
    '/gecodeerde_lithologie.xml'


class TestGecodeerdeLithologie(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.interpretaties.GecodeerdeLithologie class."""

    datatype_class = GecodeerdeLithologie
    namespace = 'http://dov.vlaanderen.be/ocdov/interpretaties'
    pkey_base = build_dov_url('data/interpretatie/')

    field_names = [
        'pkey_interpretatie', 'pkey_boring',
        'betrouwbaarheid_interpretatie', 'x', 'y',
        'start_interpretatie_mtaw',
        'diepte_laag_van', 'diepte_laag_tot',
        'hoofdnaam1_grondsoort', 'hoofdnaam2_grondsoort',
        'bijmenging1_plaatselijk', 'bijmenging1_hoeveelheid',
        'bijmenging1_grondsoort',
        'bijmenging2_plaatselijk', 'bijmenging2_hoeveelheid',
        'bijmenging2_grondsoort',
        'bijmenging3_plaatselijk', 'bijmenging3_hoeveelheid',
        'bijmenging3_grondsoort']
    field_names_subtypes = [
        'diepte_laag_van', 'diepte_laag_tot',
        'hoofdnaam1_grondsoort', 'hoofdnaam2_grondsoort',
        'bijmenging1_plaatselijk', 'bijmenging1_hoeveelheid',
        'bijmenging1_grondsoort',
        'bijmenging2_plaatselijk', 'bijmenging2_hoeveelheid',
        'bijmenging2_grondsoort',
        'bijmenging3_plaatselijk', 'bijmenging3_hoeveelheid',
        'bijmenging3_grondsoort']
    field_names_nosubtypes = [
        'pkey_interpretatie', 'pkey_boring',
        'betrouwbaarheid_interpretatie', 'x', 'y',
        'start_interpretatie_mtaw']

    valid_returnfields = ReturnFieldList.from_field_names('pkey_interpretatie', 'pkey_boring')
    valid_returnfields_subtype = ReturnFieldList.from_field_names(
        'pkey_interpretatie', 'diepte_laag_van', 'diepte_laag_tot')

    inexistent_field = 'onbestaand'
