"""Module grouping tests for the bodemclassificatie search module."""
from owslib.fes2 import PropertyIsEqualTo
from shapely.geometry import Point

from pydov.search.bodemclassificatie import BodemclassificatieSearch
from pydov.types.bodemclassificatie import Bodemclassificatie
from pydov.types.fields import ReturnFieldList
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/bodemclassificatie/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/bodemclassificatie/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/bodemclassificatie/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/bodemclassificatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemclassificatie/feature.xml'
location_dov_xml = 'tests/data/types/bodemclassificatie/bodemclassificatie.xml'
location_xsd_base = 'tests/data/types/bodemclassificatie/xsd_*.xml'


class TestBodemclassificatieSearch(AbstractTestSearch):

    search_instance = BodemclassificatieSearch()
    datatype_class = Bodemclassificatie

    valid_query_single = PropertyIsEqualTo(
        propertyname='pkey_bodemclassificatie',
        literal=build_dov_url('data/belgischebodemclassificatie/2018-000146'))

    inexistent_field = 'onbestaand'
    wfs_field = 'bodemtype'
    xml_field = None

    valid_returnfields = ReturnFieldList.from_field_names('pkey_bodemclassificatie', 'bodemtype',
                                                          'classificatietype')
    valid_returnfields_subtype = None
    valid_returnfields_extra = None

    df_default_columns = [
        'pkey_bodemclassificatie', 'pkey_bodemlocatie', 'x', 'y', 'mv_mtaw',
        'classificatietype', 'bodemtype', 'auteurs'
    ]
