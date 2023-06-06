# -*- coding: utf-8 -*-
"""Module grouping tests for the bodemobservatie search module."""
import datetime

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.bodemobservatie import BodemobservatieSearch
from pydov.types.bodemobservatie import Bodemobservatie
from pydov.types.fields import ReturnFieldList
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/bodemobservatie/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/bodemobservatie/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/bodemobservatie/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/bodemobservatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemobservatie/feature.xml'
location_dov_xml = 'tests/data/types/bodemobservatie/bodemobservatie.xml'
location_xsd_base = 'tests/data/types/bodemobservatie/xsd_*.xml'


class TestBodemobservatieSearch(AbstractTestSearch):

    search_instance = BodemobservatieSearch()
    datatype_class = Bodemobservatie

    valid_query_single = PropertyIsEqualTo(propertyname='Bodemobservatie',
                                           literal='2019-1027345')

    inexistent_field = 'onbestaand'
    wfs_field = 'parameter'
    xml_field = 'observatiedatum'

    valid_returnfields = ReturnFieldList.from_field_names(
        'pkey_bodemobservatie',
        'parameter')
    valid_returnfields_subtype = ReturnFieldList.from_field_names(
        'pkey_bodemobservatie',
        'parameter',
        'observatiedatum')
    valid_returnfields_extra = ReturnFieldList.from_field_names(
        'pkey_bodemobservatie',
        'parameter',
        'Opmerkingen')

    df_default_columns = [
        'pkey_bodemobservatie', 'pkey_bodemlocatie',
        'pkey_parent', 'x', 'y', 'mv_mtaw', 'diepte_van_cm',
        'diepte_tot_cm', 'observatiedatum', 'invoerdatum',
        'parametergroep', 'parameter', 'detectie', 'waarde',
        'eenheid', 'veld_labo', 'methode', 'betrouwbaarheid',
        'fractiemeting_ondergrens', 'fractiemeting_bovengrens',
        'fractiemeting_waarde']

    def test_search_date(self, mp_wfs, mp_get_schema,
                         mp_remote_describefeaturetype, mp_remote_md,
                         mp_remote_fc, mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with only the query parameter.

        Test whether the result is correct.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = self.search_instance.search(
            query=self.valid_query_single)

        # specific test for the Zulu time wfs 1.1.0 issue
        assert df.observatiedatum.unique()[0] == datetime.date(2015, 12, 10)
