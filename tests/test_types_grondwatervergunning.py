"""Module grouping tests for the pydov.types.boring module."""

from pydov.types.fields import ReturnFieldList
from pydov.types.grondwatervergunning import GrondwaterVergunning
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = \
    'tests/data/types/grondwatervergunning/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondwatervergunning/feature.xml'
location_dov_xml = None


class TestGrondwaterVergunning(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.grondwatervergunning.GrondwaterVergunning class."""

    datatype_class = GrondwaterVergunning
    namespace = 'http://dov.vlaanderen.be/grondwater/gw_vergunningen'
    pkey_base = None

    field_names = [
        'id_vergunning', 'pkey_installatie', 'x', 'y',
        'diepte', 'exploitant_naam', 'watnr', 'vlaremrubriek',
        'vergund_jaardebiet', 'vergund_dagdebiet',
        'van_datum_termijn', 'tot_datum_termijn',
        'aquifer_vergunning', 'inrichtingsklasse', 'nacebelcode',
        'actie_waakgebied', 'cbbnr', 'kbonr']
    field_names_subtypes = None
    field_names_nosubtypes = [
        'id_vergunning', 'pkey_installatie', 'x', 'y',
        'diepte', 'exploitant_naam', 'watnr', 'vlaremrubriek',
        'vergund_jaardebiet', 'vergund_dagdebiet',
        'van_datum_termijn', 'tot_datum_termijn',
        'aquifer_vergunning', 'inrichtingsklasse', 'nacebelcode',
        'actie_waakgebied', 'cbbnr', 'kbonr']

    valid_returnfields = ReturnFieldList.from_field_names('id_vergunning', 'diepte')
    valid_returnfields_subtype = None

    inexistent_field = 'onbestaand'
