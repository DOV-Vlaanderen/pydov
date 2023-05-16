"""Module grouping tests for the pydov.types.bodemsite module."""

from pydov.types.bodemsite import Bodemsite
from pydov.types.fields import ReturnFieldList
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/bodemsite/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemsite/feature.xml'
location_dov_xml = 'tests/data/types/bodemsite/bodemsite.xml'


class TestBodemsite(AbstractTestTypes):
    """Class grouping tests for the pydov.types.bodemsite.Bodemsite class."""

    datatype_class = Bodemsite
    namespace = 'https://www.dov.vlaanderen.be/bodem'
    pkey_base = build_dov_url('data/bodemsite/')

    field_names = [
        'pkey_bodemsite', 'naam', 'waarnemingsdatum', 'beschrijving',
        'invoerdatum'
    ]
    field_names_subtypes = []
    field_names_nosubtypes = [
        'pkey_bodemsite', 'naam', 'waarnemingsdatum', 'beschrijving',
        'invoerdatum'
    ]

    valid_returnfields = ReturnFieldList.from_field_names('pkey_bodemsite', 'naam')
    valid_returnfields_subtype = ReturnFieldList.from_field_names('pkey_bodemsite', 'naam')

    inexistent_field = 'onbestaand'

    def test_get_field_names_wrongreturnfields_nosubtypes(self):
        """Test the get_field_names method when disabling subtypes
        and including an otherwise valid return field.

        Test whether an InvalidFieldError is raised.

        Override because bodemsite has no subtypes.
        """
        assert True
