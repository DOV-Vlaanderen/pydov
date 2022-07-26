"""Module grouping tests for the interpretaties search module."""

import pandas as pd
from owslib.fes import PropertyIsEqualTo
from pandas import DataFrame

from pydov.search.interpretaties import HydrogeologischeStratigrafieSearch
from pydov.types.interpretaties import HydrogeologischeStratigrafie
from tests.abstract import AbstractTestSearch

location_md_metadata = \
    'tests/data/types/interpretaties/hydrogeologische_stratigrafie/' \
    'md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/interpretaties/hydrogeologische_stratigrafie/' \
    'fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/interpretaties/hydrogeologische_stratigrafie/' \
    'wfsdescribefeaturetype.xml'
location_wfs_getfeature = \
    'tests/data/types/interpretaties/hydrogeologische_stratigrafie/' \
    'wfsgetfeature.xml'
location_wfs_feature = \
    'tests/data/types/interpretaties/hydrogeologische_stratigrafie/feature.xml'
location_dov_xml = \
    'tests/data/types/interpretaties/hydrogeologische_stratigrafie' \
    '/hydrogeologische_stratigrafie.xml'
location_xsd_base = \
    'tests/data/types/interpretaties/hydrogeologische_stratigrafie/xsd_*.xml'


class TestHydrogeologischeStratigrafieSearch(AbstractTestSearch):

    search_instance = HydrogeologischeStratigrafieSearch()
    datatype_class = HydrogeologischeStratigrafie

    valid_query_single = PropertyIsEqualTo(propertyname='Proefnummer',
                                           literal='GEO-74/254-b1')

    inexistent_field = 'onbestaand'
    wfs_field = 'Proefnummer'
    xml_field = 'aquifer'

    valid_returnfields = ('pkey_interpretatie',
                          'betrouwbaarheid_interpretatie')
    valid_returnfields_subtype = (
        'pkey_interpretatie', 'diepte_laag_van', 'diepte_laag_tot')
    valid_returnfields_extra = ('pkey_interpretatie', 'gemeente')

    df_default_columns = ['pkey_interpretatie', 'pkey_boring',
                          'betrouwbaarheid_interpretatie', 'x', 'y',
                          'start_interpretatie_mtaw',
                          'diepte_laag_van', 'diepte_laag_tot',
                          'aquifer']

    def test_search_nan(self, mp_wfs, mp_get_schema,
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
        self.search_instance.search(
            query=self.valid_query_single)

    def test_search_customreturnfields(self, mp_get_schema,
                                       mp_remote_describefeaturetype,
                                       mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with custom return fields.

        Test whether the output dataframe is correct.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType .
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = self.search_instance.search(
            query=self.valid_query_single,
            return_fields=('pkey_interpretatie', 'pkey_boring'))

        assert isinstance(df, DataFrame)

        assert list(df) == ['pkey_interpretatie', 'pkey_boring']

        assert not pd.isnull(df.pkey_boring[0])

    def test_search_xml_resolve(self, mp_get_schema,
                                mp_remote_describefeaturetype,
                                mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with return fields from XML but not from a
        subtype.

        Test whether the output dataframe contains the resolved XML data.

        Parameters
        ----------
        mp_get_schema : pytest.fixture
            Monkeypatch the call to a remote OWSLib schema.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = self.search_instance.search(
            query=self.valid_query_single,
            return_fields=('pkey_interpretatie', 'diepte_laag_tot'))

        assert df.diepte_laag_tot[0] == 2.5
