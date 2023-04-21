"""Module grouping tests for the pydov.types.generic module."""

from pydov.types.abstract import AbstractDovType
from pydov.types.generic import WfsTypeFactory
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/generic/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/generic/feature.xml'
location_dov_xml = None


class TestWfsTypeFactory():
    """Class grouping tests for the pydov.types.generic.WfsTypeFactory class."""

    def test_get_wfs_type(self):
        """Test creating a WfsType for a given test layer.

        Test whether the created type is a subclass of AbstractDovType.
        """
        erfgoedType = WfsTypeFactory.get_wfs_type(
            'bodem_varia:bodemkundig_erfgoed')
        assert issubclass(erfgoedType, AbstractDovType)


class TestWfsTypeFactoryOpdracht(AbstractTestTypes):
    """Class grouping tests for the pydov.types.generic.WfsTypeFactory class
    for the dov-pub:Opdrachten type."""

    datatype_class = WfsTypeFactory.get_wfs_type('dov-pub:Opdrachten')
    namespace = 'http://dov.vlaanderen.be/dov-pub/Opdrachten'
    pkey_base = None

    field_names = []
    field_names_subtypes = None
    field_names_nosubtypes = []

    valid_returnfields = None
    valid_returnfields_subtype = None

    inexistent_field = 'onbestaand'

    def test_get_field_names_returnfields_nosubtypes(self):
        """WfsType have no fixed fields."""
        assert True

    def test_get_field_names_returnfields_order(self):
        """WfsType have no fixed fields."""
        assert True

    def test_get_field_names_wrongreturnfields(self):
        """WfsType have no fixed fields."""
        assert True

    def test_get_field_names_wrongreturnfieldstype(self):
        """WfsType have no fixed fields."""
        assert True
