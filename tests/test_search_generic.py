"""Module grouping tests for the generic search module."""

from pydov.search.generic import WfsSearch
from pydov.types.fields import ReturnFieldList
from pydov.types.generic import WfsTypeFactory
from owslib.fes2 import PropertyIsEqualTo
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestSearch

location_md_metadata = \
    'tests/data/types/generic/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/generic/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/generic/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/generic/' \
                          'wfsgetfeature.xml'
location_wfs_feature = \
    'tests/data/types/generic/feature.xml'
location_dov_xml = None
location_xsd_base = 'tests/data/types/generic/xsd_*.xml'


class TestWfsSearch(AbstractTestSearch):

    search_instance = WfsSearch('dov-pub:Opdrachten')
    datatype_class = WfsTypeFactory.get_wfs_type('dov-pub:Opdrachten')

    valid_query_single = PropertyIsEqualTo(
        propertyname='fiche',
        literal=build_dov_url('data/opdracht/2021-026141%27'))

    inexistent_field = 'onbestaand'
    xml_field = None
    wfs_field = 'opdrachtgever'

    valid_returnfields = ReturnFieldList.from_field_names('opdrachtgever', 'opdrachtnemer')
    valid_returnfields_subtype = None
    valid_returnfields_extra = ReturnFieldList.from_field_names('startdatum', 'naam')

    df_default_columns = [
        'id', 'naam', 'fiche', 'omschrijving', 'startdatum', 'einddatum',
        'opdrachtgever', 'opdrachtnemer', 'dataleverancier', 'aard',
        'origine', 'eerste_invoer']

    def test_pluggable_type(self):
        """Generic WFS types are not pluggable."""
        assert True
