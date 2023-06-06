"""Module grouping tests for the bodemdiepteinterval search module."""
import datetime

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.bodemdiepteinterval import BodemdiepteintervalSearch
from pydov.types.bodemdiepteinterval import Bodemdiepteinterval
from pydov.types.fields import ReturnFieldList
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/bodemdiepteinterval/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/bodemdiepteinterval/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/bodemdiepteinterval/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/bodemdiepteinterval/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemdiepteinterval/feature.xml'
location_xsd_base = 'tests/data/types/bodemdiepteinterval/xsd_*.xml'


class TestBodemdiepteintervalSearch(AbstractTestSearch):

    search_instance = BodemdiepteintervalSearch()
    datatype_class = Bodemdiepteinterval

    valid_query_single = PropertyIsEqualTo(
        propertyname='pkey_diepteinterval',
        literal=build_dov_url('data/bodemdiepteinterval/2018-000004'))

    inexistent_field = 'onbestaand'
    wfs_field = 'ondergrens_bereikt'
    xml_field = None

    valid_returnfields = ReturnFieldList.from_field_names('pkey_diepteinterval', 'naam', 'bovengrens1_cm')
    valid_returnfields_subtype = None
    valid_returnfields_extra = ReturnFieldList.from_field_names('pkey_diepteinterval', 'naam', 'Monsters')

    df_default_columns = [
        'pkey_diepteinterval', 'pkey_bodemopbouw', 'pkey_bodemlocatie',
        'nr', 'type', 'naam', 'bovengrens1_cm', 'bovengrens2_cm',
        'ondergrens1_cm', 'ondergrens2_cm', 'ondergrens_bereikt',
        'grensduidelijkheid', 'grensregelmatigheid', 'beschrijving', 'x', 'y',
        'mv_mtaw']
