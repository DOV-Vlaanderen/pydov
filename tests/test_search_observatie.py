"""Module grouping tests for the observatie search module."""
import datetime

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.observatie import ObservatieSearch
from pydov.types.observatie import Observatie
from pydov.types.fields import ReturnFieldList
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/observatie/md_metadata.xml'
location_fc_featurecatalogue = 'tests/data/types/observatie/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = 'tests/data/types/observatie/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/observatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/observatie/feature.xml'
location_dov_xml = 'tests/data/types/observatie/observatie.xml'
location_xsd_base = 'tests/data/types/observatie/xsd_*.xml'


class TestObservatieSearch(AbstractTestSearch):

    search_instance = ObservatieSearch()
    datatype_class = Observatie
    valid_query_single = PropertyIsEqualTo(propertyname='pkey_observatie', literal=build_dov_url('data/observatie/2022-2759196'))

    inexistent_field = 'onbestaand'
    wfs_field = 'parameter'
    xml_field = None


    valid_returnfields = ReturnFieldList.from_field_names('pkey_observatie', 'fenomeentijd', 'diepte_van_m')
    valid_returnfields_subtype = ReturnFieldList.from_field_names()
    valid_returnfields_extra = ReturnFieldList.from_field_names()


    df_default_columns = ['pkey_observatie', 'pkey_parent', 'fenomeentijd', 'diepte_van_m', 'diepte_tot_m',
                              'parametergroep', 'parameter', 'detectieconditie', 'resultaat', 'eenheid', 'methode',
                              'uitvoerder', 'herkomst']


