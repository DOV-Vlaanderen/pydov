"""Module grouping tests for the pydov.types.boring module."""

from pydov.types.abstract import AbstractDovType
from pydov.types.boring import Boring, MethodeXyz
from pydov.types.fields import ReturnFieldList, XmlField
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/boring/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/boring/feature.xml'
location_dov_xml = 'tests/data/types/boring/boring.xml'


class TestBoring(AbstractTestTypes):
    """Class grouping tests for the pydov.types.boring.Boring class."""

    datatype_class = Boring
    namespace = 'http://dov.vlaanderen.be/ocdov/dov-pub'
    pkey_base = build_dov_url('data/boring/')

    field_names = [
        'pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
        'start_boring_mtaw', 'gemeente', 'diepte_boring_van',
        'diepte_boring_tot', 'datum_aanvang', 'uitvoerder',
        'boorgatmeting', 'diepte_methode_van',
        'diepte_methode_tot', 'boormethode']
    field_names_subtypes = [
        'diepte_methode_van',
        'diepte_methode_tot', 'boormethode']
    field_names_nosubtypes = [
        'pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
        'start_boring_mtaw', 'gemeente', 'diepte_boring_van',
        'diepte_boring_tot', 'datum_aanvang', 'uitvoerder',
        'boorgatmeting']

    valid_returnfields = ReturnFieldList.from_field_names('pkey_boring', 'diepte_boring_tot')
    valid_returnfields_subtype = ReturnFieldList.from_field_names(
        'pkey_boring', 'diepte_methode_van', 'boormethode')

    inexistent_field = 'onbestaand'

    def test_get_fieldsets(self):
        """Test the get_fieldsets method.

        Test whether the correct fieldsets are returned.

        """

        fieldsets = sorted(Boring.get_fieldsets().keys())
        assert fieldsets == ['MethodeXyz']

    def test_with_extra_fields_fieldset(self):
        """Test the with_extra_fields method using a predefined fieldset.

        Test whether the fields are correctly added to the type.

        """
        new_type = Boring.with_extra_fields(MethodeXyz)
        assert issubclass(new_type, AbstractDovType)

        own_field_names = Boring.get_field_names()
        extra_field_names = MethodeXyz.get_field_names()
        all_field_names = new_type.get_field_names()

        for field in extra_field_names:
            assert field in all_field_names
            all_field_names.remove(field)

        assert all_field_names == own_field_names

    def test_with_extra_fields_custom(self):
        """Test the with_extra_fields method using a custom list of fields.

        Test whether the fields are correctly added to the type.

        """
        new_type = Boring.with_extra_fields([
            XmlField(name='methode_xy',
                     source_xpath='/boring/ligging/metadata_locatiebepaling'
                     '/methode',
                     datatype='string')
        ])
        assert issubclass(new_type, AbstractDovType)

        own_field_names = Boring.get_field_names()
        extra_field_names = ['methode_xy']
        all_field_names = new_type.get_field_names()

        for field in extra_field_names:
            assert field in all_field_names
            all_field_names.remove(field)

        assert all_field_names == own_field_names
