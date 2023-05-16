"""Module grouping tests for the pydov.types.bodemclassificatie module."""

from pydov.types.bodemclassificatie import Bodemclassificatie
from pydov.types.fields import ReturnFieldList
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/bodemclassificatie' \
    '/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemclassificatie/feature.xml'


class TestBodemclassificatie(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.bodemclassificatie.Bodemclassificatie class."""

    datatype_class = Bodemclassificatie
    namespace = 'https://www.dov.vlaanderen.be/bodem'
    pkey_base = build_dov_url('data/')

    field_names = [
        'pkey_bodemclassificatie', 'pkey_bodemlocatie', 'x', 'y', 'mv_mtaw',
        'classificatietype', 'bodemtype', 'auteurs'
    ]
    field_names_subtypes = []
    field_names_nosubtypes = [
        'pkey_bodemclassificatie', 'pkey_bodemlocatie', 'x', 'y', 'mv_mtaw',
        'classificatietype', 'bodemtype', 'auteurs'
    ]

    valid_returnfields = ReturnFieldList.from_field_names('pkey_bodemclassificatie', 'bodemtype')
    valid_returnfields_subtype = ReturnFieldList.from_field_names('pkey_bodemclassificatie', 'bodemtype')

    inexistent_field = 'onbestaand'

    def test_get_field_names_wrongreturnfields_nosubtypes(self):
        """Test the get_field_names method when disabling subtypes
        and including an otherwise valid return field.

        Test whether an InvalidFieldError is raised.

        Override because bodemclassificatie has no subtypes.
        """
        assert True

    def test_from_wfs_element(self, wfs_feature):
        """Test the from_wfs_element method.

        Test whether we can construct an instance from a WFS response element.

        Parameters
        ----------
        wfs_feature : pytest.fixture returning etree.Element
            Fixture providing an XML element representing a single record of
            the WFS layer.

        """
        feature = self.datatype_class.from_wfs_element(
            wfs_feature, self.namespace)

        assert isinstance(feature, self.datatype_class)

        if self.pkey_base is not None:
            assert feature.pkey.startswith(self.pkey_base)

        assert isinstance(feature.data, dict)
        assert isinstance(feature.subdata, dict)
