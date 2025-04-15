"""Module grouping tests for the pydov.types.boring module."""
from pydov.types.abstract import AbstractDovSubType
from pydov.types.fields import ReturnFieldList, XmlField
from pydov.types.grondwaterfilter import GrondwaterFilter, Peilmeting
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

location_wfs_getfeature = 'tests/data/types/grondwaterfilter/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondwaterfilter/feature.xml'
location_dov_xml = 'tests/data/types/grondwaterfilter/grondwaterfilter.xml'


class TestGrondwaterFilter(AbstractTestTypes):
    """Class grouping tests for the
    pydov.types.grondwaterfilter.GrondwaterFilter class."""

    datatype_class = GrondwaterFilter
    namespace = 'http://dov.vlaanderen.be/grondwater/gw_meetnetten'
    pkey_base = build_dov_url('data/filter/')

    field_names = [
        'pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
        'filternummer', 'filtertype', 'x', 'y',
        'start_grondwaterlocatie_mtaw', 'mv_mtaw',
        'gemeente', 'meetnet_code', 'aquifer_code',
        'grondwaterlichaam_code', 'regime',
        'diepte_onderkant_filter', 'lengte_filter',
        'datum', 'tijdstip', 'peil_mtaw',
        'betrouwbaarheid', 'methode', 'filterstatus', 'filtertoestand']
    field_names_subtypes = [
        'datum', 'tijdstip', 'peil_mtaw', 'betrouwbaarheid',
        'methode']
    field_names_nosubtypes = [
        'pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
        'filternummer', 'filtertype', 'x', 'y',
        'start_grondwaterlocatie_mtaw', 'mv_mtaw',
        'gemeente', 'meetnet_code', 'aquifer_code',
        'grondwaterlichaam_code', 'regime',
        'diepte_onderkant_filter', 'lengte_filter']

    valid_returnfields = ReturnFieldList.from_field_names('pkey_filter', 'meetnet_code')
    valid_returnfields_subtype = ReturnFieldList.from_field_names('pkey_filter', 'peil_mtaw')

    inexistent_field = 'onbestaand'

    def test_subtype_with_extra_fields_custom(self):
        """Test the with_extra_fields method using a custom list of fields.

        Test whether the fields are correctly added to the type.

        """
        new_subtype = Peilmeting.with_extra_fields([
            XmlField(name='diepte_tov_referentiepunt',
                     source_xpath='/diepte_tov_referentiepunt',
                     datatype='float')
        ])
        assert issubclass(new_subtype, AbstractDovSubType)

        own_field_names = Peilmeting.get_field_names()
        extra_field_names = ['diepte_tov_referentiepunt']
        all_field_names = new_subtype.get_field_names()

        for field in extra_field_names:
            assert field in all_field_names
            all_field_names.remove(field)

        assert all_field_names == own_field_names
