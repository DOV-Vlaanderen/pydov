"""Module grouping tests for the
pydov.types.interpretaties.InformeleStratigrafie class."""
from pydov.types.fields import ReturnFieldList
from pydov.types.interpretaties import HydrogeologischeStratigrafie
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = \
    'tests/data/types/interpretaties/hydrogeologische_stratigrafie/' \
    'wfsgetfeature.xml'
location_wfs_feature = \
    'tests/data/types/interpretaties/hydrogeologische_stratigrafie/feature.xml'
location_dov_xml = \
    'tests/data/types/interpretaties/hydrogeologische_stratigrafie' \
    '/hydrogeologische_stratigrafie.xml'


class TestHydrogeologischeStratigrafie(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.interpretaties.HydrogeologischeStratigrafie class."""

    datatype_class = HydrogeologischeStratigrafie
    namespace = 'http://dov.vlaanderen.be/ocdov/interpretaties'
    pkey_base = build_dov_url('data/interpretatie/')

    field_names = [
        'pkey_interpretatie', 'pkey_boring',
        'betrouwbaarheid_interpretatie', 'x', 'y',
        'start_interpretatie_mtaw',
        'diepte_laag_van', 'diepte_laag_tot', 'aquifer']
    field_names_subtypes = [
        'diepte_laag_van', 'diepte_laag_tot', 'aquifer']
    field_names_nosubtypes = [
        'pkey_interpretatie', 'pkey_boring',
        'betrouwbaarheid_interpretatie', 'x', 'y',
        'start_interpretatie_mtaw']

    valid_returnfields = ReturnFieldList.from_field_names('pkey_interpretatie', 'pkey_boring')
    valid_returnfields_subtype = ReturnFieldList.from_field_names(
        'pkey_interpretatie', 'diepte_laag_van', 'diepte_laag_tot')

    inexistent_field = 'onbestaand'
