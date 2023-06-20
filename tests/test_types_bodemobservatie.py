# -*- coding: utf-8 -*-
"""Module grouping tests for the pydov.types.bodemobservatie module."""

from pydov.types.bodemobservatie import Bodemobservatie
from pydov.types.fields import ReturnFieldList
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/bodemobservatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemobservatie/feature.xml'
location_dov_xml = 'tests/data/types/bodemobservatie/bodemobservatie.xml'


class TestBodemobservatie(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.bodemobservatie.Bodemobservatie class."""

    datatype_class = Bodemobservatie
    namespace = 'https://www.dov.vlaanderen.be/bodem'
    pkey_base = build_dov_url('data/bodemobservatie/')

    field_names = ['pkey_bodemobservatie', 'pkey_bodemlocatie',
                   'pkey_parent', 'x', 'y', 'mv_mtaw', 'diepte_van_cm',
                   'diepte_tot_cm', 'observatiedatum', 'invoerdatum',
                   'parametergroep', 'parameter', 'detectie', 'waarde',
                   'eenheid', 'veld_labo', 'methode', 'betrouwbaarheid',
                   'fractiemeting_ondergrens', 'fractiemeting_bovengrens',
                   'fractiemeting_waarde']
    field_names_subtypes = []
    field_names_nosubtypes = [
        'pkey_bodemobservatie', 'pkey_bodemlocatie',
        'pkey_parent', 'x', 'y', 'mv_mtaw', 'diepte_van_cm',
        'diepte_tot_cm', 'observatiedatum', 'invoerdatum',
        'parametergroep', 'parameter', 'detectie', 'waarde',
        'eenheid', 'veld_labo', 'methode', 'betrouwbaarheid']

    valid_returnfields = ReturnFieldList.from_field_names('pkey_bodemobservatie', 'parameter')
    valid_returnfields_subtype = ReturnFieldList.from_field_names('pkey_bodemobservatie', 'parameter',
                                                                  'fractiemeting_ondergrens')

    inexistent_field = 'onbestaand'
