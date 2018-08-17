"""Module grouping tests for the search grondwaterfilter module."""
import datetime

import pytest
from pandas import DataFrame

from owslib.fes import PropertyIsEqualTo
from pydov.search.grondwaterfilter import GrondwaterFilterSearch
from pydov.types.grondwaterfilter import GrondwaterFilter
from pydov.util.errors import InvalidFieldError
from tests.abstract import AbstractTestSearch

from tests.test_search import (
    mp_wfs,
    wfs,
    mp_remote_md,
    mp_remote_fc,
    mp_remote_describefeaturetype,
    mp_remote_wfs_feature,
    mp_dov_xml,
    wfs_getfeature,
    wfs_feature,
)

location_md_metadata = 'tests/data/types/grondwaterfilter/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/grondwaterfilter/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/grondwaterfilter/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/grondwaterfilter/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/grondwaterfilter/feature.xml'
location_dov_xml = 'tests/data/types/grondwaterfilter/grondwaterfilter.xml'


@pytest.fixture
def grondwaterfiltersearch():
    """PyTest fixture returning an instance of
     pydov.search.GrondwaterFilterSearch.

    Returns
    -------
    pydov.search.pydov.search.GrondwaterFilterSearch
        An instance of GrondwaterFilterSearch to perform search operations on
        the DOV type 'GrondwaterFilter'.

    """
    return GrondwaterFilterSearch()


class TestGrondwaterFilterSearch(AbstractTestSearch):
    """Class grouping tests for the pydov.search.GrondwaterFilterSearch class.
    """

    def test_get_fields(self, mp_wfs, mp_remote_describefeaturetype,
                        mp_remote_md, mp_remote_fc, grondwaterfiltersearch):
        """Test the get_fields method.

        Test whether the returned fields match the format specified
        in the documentation.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            gw_meetnetten:meetnetten layer.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata of the
            gw_meetnetten:meetnetten layer.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue
            of the
            gw_meetnetten:meetnetten layer.
        grondwaterfiltersearch : pytest.fixture returning
            pydov.search.GrondwaterFilterSearch
            An instance of GrondwaterFilterSearch to perform search operations
            on the DOV type 'GrondwaterFilter'.
        """
        fields = grondwaterfiltersearch.get_fields()
        self.abstract_test_get_fields(fields)

    def test_search_both_location_query(self, mp_remote_describefeaturetype,
                                        mp_remote_wfs_feature,
                                        grondwaterfiltersearch):
        """Test the search method providing both a location and a query.

        Test whether a dataframe is returned.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            gw_meetnetten:meetnetten layer.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        grondwaterfiltersearch : pytest.fixture returning
            pydov.search.GrondwaterFilterSearch
            An instance of GrondwaterFilterSearch to perform search operations
            on the DOV type 'GrondwaterFilter'.

        """
        query = PropertyIsEqualTo(propertyname='gemeente',
                                  literal='Blankenberge')

        df = grondwaterfiltersearch.search(
            location=(1, 2, 3, 4), query=query,
            return_fields=('pkey_filter', 'filternummer'))

        assert type(df) is DataFrame

    def test_search(self, mp_wfs, mp_remote_describefeaturetype, mp_remote_md,
                    mp_remote_fc, mp_remote_wfs_feature, mp_dov_xml,
                    grondwaterfiltersearch):
        """Test the search method with only the query parameter.

        Test whether the result is correct.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            gw_meetnetten:meetnetten layer.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata of the
            gw_meetnetten:meetnetten layer.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue of the
            gw_meetnetten:meetnetten layer.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote GrondwaterFilter XML data.
        grondwaterfiltersearch : pytest.fixture returning
            pydov.search.GrondwaterFilterSearch
            An instance of GrondwaterFilterSearch to perform search operations
            on the DOV type 'GrondwaterFilter'.

        """
        query = PropertyIsEqualTo(propertyname='filterfiche',
                                  literal='https://www.dov.vlaanderen.be/'
                                          'data/filter/2003-004471')
        df = grondwaterfiltersearch.search(query=query)

        assert type(df) is DataFrame

        assert list(df) == ['pkey_filter', 'pkey_grondwaterlocatie', 'gw_id',
                            'filternummer', 'filtertype', 'x', 'y', 'mv_mtaw',
                            'gemeente', 'meetnet_code', 'aquifer_code',
                            'grondwaterlichaam_code', 'regime',
                            'diepte_onderkant_filter', 'lengte_filter',
                            'datum', 'tijdstip', 'peil_mtaw',
                            'betrouwbaarheid', 'methode']

        self.abstract_test_search_checkrows(df, GrondwaterFilter)

        # dtype checks of the resulting df columns
        fields = GrondwaterFilter.get_fields()
        self.abstract_test_df_dtypes(df, fields)

        # specific test for the Zulu time wfs 1.1.0 issue
        assert df.datum.sort_values()[0] == datetime.date(2004, 4, 7)

    def test_search_returnfields(self, mp_remote_wfs_feature,
                                 grondwaterfiltersearch):
        """Test the search method with the query parameter and a selection of
        return fields.

        Test whether the output dataframe contains only the selected return
        fields.

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        grondwaterfiltersearch : pytest.fixture returning
            pydov.search.GrondwaterFilterSearch
            An instance of GrondwaterFilterSearch to perform search operations
            on the DOV type 'GrondwaterFilter'.

        """
        query = PropertyIsEqualTo(propertyname='filterfiche',
                                  literal='https://www.dov.vlaanderen.be/'
                                          'data/filter/2003-004471')

        df = grondwaterfiltersearch.search(
            query=query, return_fields=('pkey_filter', 'gw_id',
                                        'filternummer'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_filter', 'gw_id', 'filternummer']

    def test_search_returnfields_subtype(self, mp_remote_wfs_feature,
                                         grondwaterfiltersearch):
        """Test the search method with the query parameter and a selection of
        return fields, including fields from a subtype.

        Test whether the output dataframe contains only the selected return
        fields.

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        grondwaterfiltersearch : pytest.fixture returning
            pydov.search.GrondwaterFilterSearch
            An instance of GrondwaterFilterSearch to perform search operations
            on the DOV type 'GrondwaterFilter'.

        """
        query = PropertyIsEqualTo(propertyname='filterfiche',
                                  literal='https://www.dov.vlaanderen.be/'
                                          'data/filter/2003-004471')

        df = grondwaterfiltersearch.search(
            query=query, return_fields=('pkey_filter', 'gw_id',
                                        'filternummer', 'peil_mtaw'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_filter', 'gw_id', 'filternummer',
                            'peil_mtaw']

    def test_search_returnfields_order(self, mp_remote_wfs_feature,
                                       grondwaterfiltersearch):
        """Test the search method with the query parameter and a selection of
        return fields in another ordering.

        Test whether the output dataframe contains only the selected return
        fields, in the order that is documented in
        docs/description_output_dataframes.rst

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        grondwaterfiltersearch : pytest.fixture returning
            pydov.search.GrondwaterFilterSearch
            An instance of GrondwaterFilterSearch to perform search operations
            on the DOV type 'GrondwaterFilter'.

        """
        query = PropertyIsEqualTo(propertyname='filterfiche',
                                  literal='https://www.dov.vlaanderen.be/'
                                          'data/filter/2003-004471')

        df = grondwaterfiltersearch.search(
            query=query, return_fields=('filternummer', 'pkey_filter',
                                        'gw_id'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_filter', 'gw_id', 'filternummer']

    def test_search_wrongreturnfields(self, grondwaterfiltersearch):
        """Test the search method with the query parameter and an inexistent
        return field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        grondwaterfiltersearch : pytest.fixture returning
            pydov.search.GrondwaterFilterSearch
            An instance of GrondwaterFilterSearch to perform search operations
            on the DOV type 'GrondwaterFilter'.

        """
        query = PropertyIsEqualTo(propertyname='filterfiche',
                                  literal='https://www.dov.vlaanderen.be/'
                                          'data/filter/2003-004471')

        with pytest.raises(InvalidFieldError):
            grondwaterfiltersearch.search(
                query=query, return_fields=('pkey_filter', 'onbestaand'))

    def test_search_wrongreturnfieldstype(self, grondwaterfiltersearch):
        """Test the search method with the query parameter and a single
        return field as string.

        Test whether an AttributeError is raised.

        Parameters
        ----------
        grondwaterfiltersearch : pytest.fixture returning
            pydov.search.GrondwaterFilterSearch
            An instance of GrondwaterFilterSearch to perform search operations
            on the DOV type 'GrondwaterFilter'.

        """
        query = PropertyIsEqualTo(propertyname='filterfiche',
                                  literal='https://www.dov.vlaanderen.be/'
                                          'data/filter/2003-004471')

        with pytest.raises(AttributeError):
            grondwaterfiltersearch.search(query=query,
                                          return_fields='datum_aanvang')

    def test_search_query_wrongfield(self, grondwaterfiltersearch):
        """Test the search method with the query parameter using an
        inexistent query field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        grondwaterfiltersearch : pytest.fixture returning
            pydov.search.GrondwaterFilterSearch
            An instance of GrondwaterFilterSearch to perform search operations
            on the DOV type 'GrondwaterFilter'.

        """
        query = PropertyIsEqualTo(propertyname='onbestaand',
                                  literal='Geotechnisch onderzoek')

        with pytest.raises(InvalidFieldError):
            grondwaterfiltersearch.search(query=query)

    def test_search_query_wrongfield_returnfield(self, grondwaterfiltersearch):
        """Test the search method with the query parameter using an
        return-only field as query field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        grondwaterfiltersearch : pytest.fixture returning
            pydov.search.GrondwaterFilterSearch
            An instance of GrondwaterFilterSearch to perform search operations
            on the DOV type 'GrondwaterFilter'.

        """
        query = PropertyIsEqualTo(propertyname='meetnet_code',
                                  literal='8')

        with pytest.raises(InvalidFieldError):
            grondwaterfiltersearch.search(query=query)

    def test_search_extrareturnfields(self, mp_remote_describefeaturetype,
                                      mp_remote_wfs_feature, mp_dov_xml,
                                      grondwaterfiltersearch):
        """Test the search method with the query parameter and an extra WFS
        field as return field.

        Parameters
        ----------
        grondwaterfiltersearch : pytest.fixture returning
            pydov.search.GrondwaterFilterSearch
            An instance of GrondwaterFilterSearch to perform search operations
            on the DOV type 'GrondwaterFilter'.

        """
        query = PropertyIsEqualTo(propertyname='filterfiche',
                                  literal='https://www.dov.vlaanderen.be/'
                                          'data/filter/2003-004471')

        df = grondwaterfiltersearch.search(
            query=query, return_fields=('pkey_filter', 'oxidatie_reductie'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_filter', 'oxidatie_reductie']

    def test_search_xmlresolving(self, mp_remote_describefeaturetype,
                                 mp_remote_wfs_feature, mp_dov_xml,
                                 grondwaterfiltersearch):
        """Test the search method with return fields from XML but not from a
        subtype.

        Test whether the output dataframe contains the resolved XML data.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            gw_meetnetten:meetnetten layer.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote GrondwaterFilter XML data.
        grondwaterfiltersearch : pytest.fixture returning
            pydov.search.GrondwaterFilterSearch
            An instance of GrondwaterFilterSearch to perform search operations
            on the DOV type 'GrondwaterFilter'.

        """
        query = PropertyIsEqualTo(propertyname='filterfiche',
                                  literal='https://www.dov.vlaanderen.be/'
                                          'data/filter/2003-004471')

        df = grondwaterfiltersearch.search(
            query=query, return_fields=('pkey_filter', 'gw_id', 'filternummer',
                                        'meetnet_code'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_filter', 'gw_id', 'filternummer',
                            'meetnet_code']
        assert df.meetnet_code[0] == 8
