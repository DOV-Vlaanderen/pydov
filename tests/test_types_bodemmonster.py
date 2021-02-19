# -*- coding: utf-8 -*-
"""Module grouping tests for the pydov.types.bodemmonster module."""

from pydov.types.bodemmonster import Bodemmonster
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/bodemobservatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemobservatie/feature.xml'
location_dov_xml = 'tests/data/types/bodemobservatie/bodemobservatie.xml'


class TestBodemmonster(AbstractTestTypes):
    """Class grouping tests for the pydov.types.bodemmonster.Bodemmonster class."""

    datatype_class = Bodemmonster
    namespace = 'https://www.dov.vlaanderen.be/bodem'
    pkey_base = build_dov_url('data/bodemmonster/')

    field_names = [
            'pkey_bodemmonster', 'identificatie',
            'datum_monstername', 'tijdstip_monstername',
            'type', 'monsternamedoor', 'techniek', 
            'condities', 'van', 'tot', 'labo',
            'laboreferentie', 'opmerking'
        ]
    field_names_subtypes = []
    field_names_nosubtypes = [
            'pkey_bodemmonster', 'identificatie',
            'datum_monstername', 'tijdstip_monstername',
            'type', 'monsternamedoor', 'techniek', 
            'condities', 'van', 'tot', 'labo',
            'laboreferentie', 'opmerking'
    ]

    valid_returnfields = ('pkey_bodemmonster', 'identificatie')
    valid_returnfields_subtype = ('pkey_bodemmonster', 'identificatie')

    inexistent_field = 'onbestaand'

    def test_get_field_names_wrongreturnfields_nosubtypes(self):
        """Test the get_field_names method when disabling subtypes
        and including an otherwise valid return field.

        Test whether an InvalidFieldError is raised.

        Override because bodemmonster has no subtypes.
        """
        assert True
