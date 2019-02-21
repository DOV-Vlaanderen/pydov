"""Module grouping tests for the interpretaties search module."""
import pandas as pd
import numpy as np
import pytest
from pandas import DataFrame

import pydov
from owslib.fes import PropertyIsEqualTo
from pydov.search.interpretaties import GeotechnischeCoderingSearch
from pydov.types.interpretaties import GeotechnischeCodering
from tests.abstract import (
    AbstractTestSearch,
)

from tests.test_search import (
    mp_wfs,
    wfs,
    mp_remote_md,
    mp_remote_fc,
    mp_remote_describefeaturetype,
    mp_remote_wfs_feature,
    mp_remote_xsd,
    mp_dov_xml,
    mp_dov_xml_broken,
    wfs_getfeature,
    wfs_feature,
)

location_md_metadata = \
    'tests/data/types/interpretaties/geotechnische_codering/' \
    'md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/interpretaties/geotechnische_codering/' \
    'fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/interpretaties/geotechnische_codering/' \
    'wfsdescribefeaturetype.xml'
location_wfs_getfeature = \
    'tests/data/types/interpretaties/geotechnische_codering/' \
    'wfsgetfeature.xml'
location_wfs_feature = \
    'tests/data/types/interpretaties/geotechnische_codering/feature.xml'
location_dov_xml = \
    'tests/data/types/interpretaties/geotechnische_codering' \
    '/geotechnische_codering.xml'
location_xsd_base = \
    'tests/data/types/interpretaties/geotechnische_codering/xsd_*.xml'


class TestGeotechnischeCoderingSearch(AbstractTestSearch):
    def get_search_object(self):
        """Get an instance of the search object for this type.

        Returns
        -------
        pydov.search.interpretaties.GeotechnischeCoderingSearch
            Instance of GeotechnischeCoderingSearch used for searching.

        """
        return GeotechnischeCoderingSearch()

    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.interpretaties.GeotechnischeCodering
            Class reference for the GeotechnischeCodering class.

        """
        return GeotechnischeCodering

    def get_valid_query_single(self):
        """Get a valid query returning a single feature.

        Returns
        -------
        owslib.fes.OgcExpression
            OGC expression of the query.

        """
        return PropertyIsEqualTo(propertyname='Proefnummer',
                                 literal='GEO-15/139-B1')

    def get_inexistent_field(self):
        """Get the name of a field that doesn't exist.

        Returns
        -------
        str
            The name of an inexistent field.

        """
        return 'onbestaand'

    def get_xml_field(self):
        """Get the name of a field defined in XML only.

        Returns
        -------
        str
            The name of the XML field.

        """
        return 'grondsoort'

    def get_valid_returnfields(self):
        """Get a list of valid return fields from the main type.

        Returns
        -------
        tuple
            A tuple containing only valid return fields.

        """
        return ('pkey_interpretatie', 'betrouwbaarheid_interpretatie')

    def get_valid_returnfields_subtype(self):
        """Get a list of valid return fields, including fields from a subtype.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including fields from a
            subtype.

        """
        return ('pkey_interpretatie', 'diepte_laag_van', 'diepte_laag_tot')

    def get_valid_returnfields_extra(self):
        """Get a list of valid return fields, including extra WFS only
        fields not present in the default dataframe.

        Returns
        -------
        tuple
            A tuple containing valid return fields, including extra fields
            from WFS, not present in the default dataframe.

        """
        return ('pkey_interpretatie', 'gemeente')

    def get_df_default_columns(self):
        """Get a list of the column names (and order) from the default
        dataframe.

        Returns
        -------
        list
            A list of the column names of the default dataframe.

        """
        return ['pkey_interpretatie', 'pkey_boring',
                'betrouwbaarheid_interpretatie', 'x', 'y',
                'diepte_laag_van', 'diepte_laag_tot',
                'hoofdnaam1_grondsoort', 'hoofdnaam2_grondsoort',
                'bijmenging1_plaatselijk', 'bijmenging1_hoeveelheid',
                'bijmenging1_grondsoort',
                'bijmenging2_plaatselijk', 'bijmenging2_hoeveelheid',
                'bijmenging2_grondsoort',
                'bijmenging3_plaatselijk', 'bijmenging3_hoeveelheid',
                'bijmenging3_grondsoort']

    def test_search_nan(self, mp_wfs, mp_remote_describefeaturetype,
                        mp_remote_md, mp_remote_fc, mp_remote_wfs_feature,
                        mp_dov_xml):
        """Test the search method with only the query parameter.

        Test whether the result is correct.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
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
        df = self.get_search_object().search(
            query=self.get_valid_query_single())

    def test_search_customreturnfields(self, mp_remote_describefeaturetype,
                                       mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with custom return fields.

        Test whether the output dataframe is correct.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType .
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = self.get_search_object().search(
            query=self.get_valid_query_single(),
            return_fields=('pkey_interpretatie', 'pkey_boring'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_interpretatie', 'pkey_boring']

        assert not pd.isnull(df.pkey_boring[0])

    def test_search_xml_resolve(self, mp_remote_describefeaturetype,
                                mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method with return fields from XML but not from a
        subtype.

        Test whether the output dataframe contains the resolved XML data.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = self.get_search_object().search(
            query=self.get_valid_query_single(),
            return_fields=('pkey_interpretatie', 'diepte_laag_tot'))

        assert df.diepte_laag_tot[0] == 2.0

    def test_search_multiple_return(self, mp_remote_describefeaturetype,
                                    mp_remote_wfs_feature, mp_dov_xml):
        """Test the search method returning multiple (sub)elements of the same subject.

        Test whether the output dataframe contains the resolved XML data.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote XML data.

        """
        df = self.get_search_object().search(
            query=self.get_valid_query_single(),
            return_fields=('pkey_interpretatie',
                           'hoofdnaam1_grondsoort',
                           'hoofdnaam2_grondsoort',
                           'bijmenging1_grondsoort',
                           'bijmenging1_hoeveelheid',
                           'bijmenging1_plaatselijk'
                           ))

        assert df.hoofdnaam1_grondsoort[0] == 'FZ'
        assert df.hoofdnaam2_grondsoort[0] == 'LE'
        assert df.bijmenging1_grondsoort[0] == 'SN'
        assert df.bijmenging1_hoeveelheid[0] == 'N'
        # mind that the column below is of dtype 'object'
        assert df.bijmenging1_plaatselijk[0] is False
