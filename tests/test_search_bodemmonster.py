# -*- coding: utf-8 -*-
"""Module grouping tests for the bodemmonster search module."""
import datetime

from owslib.fes2 import PropertyIsEqualTo

from pydov.search.bodemmonster import BodemmonsterSearch
from pydov.types.bodemmonster import Bodemmonster
from pydov.types.fields import ReturnFieldList
from tests.abstract import AbstractTestSearch

location_md_metadata = 'tests/data/types/bodemmonster/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/bodemmonster/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/bodemmonster/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/bodemmonster/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/bodemmonster/feature.xml'
location_dov_xml = 'tests/data/types/bodemmonster/bodemmonster.xml'
location_xsd_base = 'tests/data/types/bodemmonster/xsd_*.xml'


class TestBodemmonsterSearch(AbstractTestSearch):

    search_instance = BodemmonsterSearch()
    datatype_class = Bodemmonster

    valid_query_single = PropertyIsEqualTo(propertyname='identificatie',
                                           literal='A0055738')

    inexistent_field = 'onbestaand'
    wfs_field = 'identificatie'
    xml_field = 'opmerking'

    valid_returnfields = ReturnFieldList.from_field_names('pkey_bodemmonster', 'identificatie')
    valid_returnfields_subtype = ReturnFieldList.from_field_names(
        'pkey_bodemmonster',
        'identificatie',
        'tijdstip_monstername')
    valid_returnfields_extra = ReturnFieldList.from_field_names(
        'pkey_bodemmonster',
        'identificatie',
        'Opdrachten')

    df_default_columns = ['pkey_bodemmonster', 'pkey_bodemlocatie',
                          'pkey_parent',
                          'x', 'y', 'mv_mtaw', 'identificatie',
                          'datum_monstername', 'tijdstip_monstername',
                          'type', 'monstername_door', 'techniek',
                          'condities', 'diepte_van_cm', 'diepte_tot_cm',
                          'labo']

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
        assert df.datum_monstername.unique()[0] == datetime.date(2015, 6, 30)
