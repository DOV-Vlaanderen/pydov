# -*- coding: utf-8 -*-
"""Module grouping tests for the pydov.types.bodemobservatie module."""

from pydov.types.bodemobservatie import Bodemobservatie
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/bodemobservatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemobservatie/feature.xml'
location_dov_xml = 'tests/data/types/bodemobservatie/bodemobservatie.xml'


class TestBodemobservatie(AbstractTestTypes):
    """Class grouping tests for the pydov.types.bodemobservatie.Bodemobservatie class."""

    datatype_class = Bodemobservatie
    namespace = 'https://www.dov.vlaanderen.be/bodem'
    pkey_base = build_dov_url('data/bodemobservatie/')

    field_names = ['pkey_bodemobservatie', 'pkey_bodemlocatie', 'Aan',
                   'pkey_parent', 'parameter', 'parametergroep',
                   'waarde', 'eenheid', 'ondergrens', 'bovengrens',
                   'methode', 'betrouwbaarheid', 'veld_labo',
                   'diepte_van', 'diepte_tot',
                   'observatiedatum', 'invoerdatum']
    field_names_subtypes = []
    field_names_nosubtypes = ['pkey_bodemobservatie', 'pkey_bodemlocatie', 'Aan',
                              'pkey_parent', 'parameter', 'parametergroep',
                              'waarde', 'eenheid', 'ondergrens', 'bovengrens',
                              'methode', 'betrouwbaarheid', 'veld_labo',
                              'diepte_van', 'diepte_tot',
                              'observatiedatum', 'invoerdatum']

    valid_returnfields = ('pkey_bodemobservatie', 'parameter')
    valid_returnfields_subtype = ('pkey_bodemobservatie', 'parameter')

    inexistent_field = 'onbestaand'

    def test_get_field_names_wrongreturnfields_nosubtypes(self):
        """Test the get_field_names method when disabling subtypes
        and including an otherwise valid return field.

        Test whether an InvalidFieldError is raised.

        Override because bodemobservatie has no subtypes.
        """
        assert True
