"""Module grouping tests for the pydov.types.observatie module."""

from pydov.types.observatie import Observatie
from pydov.types.fields import ReturnFieldList
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/observatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/observatie/feature.xml'
location_dov_xml = 'tests/data/types/observatie/observatie.xml'


class TestObservatie(AbstractTestTypes):
    """Class grouping tests for the pydov.types.observatie.Observatie class."""

    datatype_class = Observatie
    namespace = 'http://dov.vlaanderen.be/ocdov/monster'
    pkey_base = build_dov_url('data/observatie/')

    sorted_subtypes = ['ObservatieHerhaling']
    sorted_fieldsets = ['ObservatieDetails']

    field_names = ['pkey_observatie', 'pkey_parent', 'fenomeentijd', 'diepte_van_m', 'diepte_tot_m', 'parametergroep',
                   'parameter', 'detectieconditie', 'resultaat', 'eenheid', 'methode', 'uitvoerder', 'herkomst']
    field_names_subtypes = []
    field_names_nosubtypes = ['pkey_observatie', 'pkey_parent', 'fenomeentijd', 'diepte_van_m', 'diepte_tot_m',
                              'parametergroep', 'parameter', 'detectieconditie', 'resultaat', 'eenheid', 'methode',
                              'uitvoerder', 'herkomst']

    valid_returnfields = ReturnFieldList.from_field_names(
        'pkey_observatie', 'diepte_van_m')
    valid_returnfields_subtype = ReturnFieldList.from_field_names()
    inexistent_field = 'onbestaand'
