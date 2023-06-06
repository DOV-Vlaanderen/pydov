"""Module grouping tests for the pydov.types.bodemlocatie module."""

from pydov.types.bodemlocatie import Bodemlocatie
from pydov.types.fields import ReturnFieldList
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/bodemlocatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemlocatie/feature.xml'
location_dov_xml = 'tests/data/types/bodemlocatie/bodemlocatie.xml'


class TestBodemlocatie(AbstractTestTypes):
    """Class grouping tests for the pydov.types.bodemlocatie.Bodemlocatie class."""

    datatype_class = Bodemlocatie
    namespace = 'https://www.dov.vlaanderen.be/bodem'
    pkey_base = build_dov_url('data/bodemlocatie/')

    field_names = [
        'pkey_bodemlocatie', 'pkey_bodemsite',
        'naam', 'type', 'waarnemingsdatum', 'doel',
        'x', 'y', 'mv_mtaw',
        'erfgoed', 'bodemstreek',
        'invoerdatum', 'educatieve_waarde'
    ]
    field_names_subtypes = []
    field_names_nosubtypes = [
        'pkey_bodemlocatie', 'pkey_bodemsite',
        'naam', 'type', 'waarnemingsdatum', 'doel',
        'x', 'y', 'mv_mtaw',
        'erfgoed', 'bodemstreek',
        'invoerdatum', 'educatieve_waarde'
    ]

    valid_returnfields = ReturnFieldList.from_field_names('pkey_bodemlocatie', 'naam')
    valid_returnfields_subtype = ReturnFieldList.from_field_names('pkey_bodemlocatie', 'naam')

    inexistent_field = 'onbestaand'

    def test_get_field_names_wrongreturnfields_nosubtypes(self):
        """Test the get_field_names method when disabling subtypes
        and including an otherwise valid return field.

        Test whether an InvalidFieldError is raised.

        Override because bodemlocatie has no subtypes.
        """
        assert True
