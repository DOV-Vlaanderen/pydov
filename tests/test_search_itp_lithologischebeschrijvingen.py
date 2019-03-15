"""Module grouping tests for the interpretaties search module."""
import pandas as pd
import numpy as np
import pytest
from pandas import DataFrame

import pydov
from owslib.fes import PropertyIsEqualTo
from pydov.search.interpretaties import LithologischeBeschrijvingenSearch
from pydov.types.interpretaties import LithologischeBeschrijvingen
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
    'tests/data/types/interpretaties/lithologische_beschrijvingen/' \
    'md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/interpretaties/lithologische_beschrijvingen/' \
    'fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/interpretaties/lithologische_beschrijvingen/' \
    'wfsdescribefeaturetype.xml'
location_wfs_getfeature = \
    'tests/data/types/interpretaties/lithologische_beschrijvingen/' \
    'wfsgetfeature.xml'
location_wfs_feature = \
    'tests/data/types/interpretaties/lithologische_beschrijvingen/feature.xml'
location_dov_xml = \
    'tests/data/types/interpretaties/lithologische_beschrijvingen' \
    '/lithologische_beschrijvingen.xml'
location_xsd_base = \
    'tests/data/types/interpretaties/lithologische_beschrijvingen/xsd_*.xml'


class TestLithologischeBeschrijvingenSearch(AbstractTestSearch):
    def get_search_object(self):
        """Get an instance of the search object for this type.

        Returns
        -------
        pydov.search.interpretaties.LithologischeBeschrijvingenSearch
            Instance of LithologischeBeschrijvingenSearch used for searching.

        """
        return LithologischeBeschrijvingenSearch()

    def get_type(self):
        """Get the class reference for this datatype.

        Returns
        -------
        pydov.types.interpretaties.LithologischeBeschrijvingen
            Class reference for the LithologischeBeschrijvingen class.

        """
        return LithologischeBeschrijvingen

    def get_valid_query_single(self):
        """Get a valid query returning a single feature.

        Returns
        -------
        owslib.fes.OgcExpression
            OGC expression of the query.

        """
        return PropertyIsEqualTo(propertyname='Proefnummer',
                                 literal='kb15d28w-B345')

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
        return 'beschrijving'

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
                'betrouwbaarheid_interpretatie', 'x', 'y', 'diepte_laag_van',
                'diepte_laag_tot', 'beschrijving']

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
            return_fields=('pkey_interpretatie', 'pkey_boring')
        )

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

        assert df.diepte_laag_tot[0] == 1
