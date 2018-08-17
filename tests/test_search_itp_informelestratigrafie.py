"""Module grouping tests for the interpretaties search module."""
import datetime

import pytest
from pandas import DataFrame

from owslib.fes import PropertyIsEqualTo
from pydov.search.interpretaties import InformeleStratigrafieSearch
from pydov.types.interpretaties import InformeleStratigrafie
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

location_md_metadata = \
    'tests/data/types/interpretaties/informele_stratigrafie/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/interpretaties/informele_stratigrafie/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/interpretaties/informele_stratigrafie/wfsdescribefeaturetype.xml'
location_wfs_getfeature = \
    'tests/data/types/interpretaties/informele_stratigrafie/wfsgetfeature.xml'
location_wfs_feature = \
    'tests/data/types/interpretaties/informele_stratigrafie/feature.xml'
location_dov_xml = \
    'tests/data/types/interpretaties/informele_stratigrafie' \
    '/informele_stratigrafie.xml'


@pytest.fixture
def informelestratigrafiesearch():
    """PyTest fixture returning an instance of
    pydov.search.interpretaties.InformeleStratigrafieSearch.

    Returns
    -------
    pydov.search.interpretaties.InformeleStratigrafieSearch
        An instance of InformeleStratigrafieSearch to perform search
        operations on the DOV type 'Informele stratigrafie'.

    """
    return InformeleStratigrafieSearch()


class TestInformeleStratigrafieSearch(AbstractTestSearch):
    """Class grouping tests for the
    pydov.search.interpretaties.InformeleStratigrafieSearch class."""
    def test_get_fields(self, mp_wfs, mp_remote_describefeaturetype,
                        mp_remote_md, mp_remote_fc,
                        informelestratigrafiesearch):
        """Test the get_fields method.

        Test whether the returned fields match the format specified
        in the documentation.

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
        informelestratigrafiesearch : pytest.fixture returning
                pydov.search.interpretaties.InformeleStratigrafieSearch
            An instance of InformeleStratigrafieSearch to perform search
            operations on the DOV type 'Informele stratigrafie'.

        """
        fields = informelestratigrafiesearch.get_fields()
        self.abstract_test_get_fields(fields)

    def test_search_both_location_query(self, mp_remote_describefeaturetype,
                                        mp_remote_wfs_feature,
                                        informelestratigrafiesearch):
        """Test the search method providing both a location and a query.

        Test whether a dataframe is returned.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        informelestratigrafiesearch : pytest.fixture returning
                pydov.search.interpretaties.InformeleStratigrafieSearch
            An instance of InformeleStratigrafieSearch to perform search
            operations on the DOV type 'Informele stratigrafie'.

        """
        query = PropertyIsEqualTo(propertyname='gemeente',
                                  literal='Blankenberge')

        df = informelestratigrafiesearch.search(
            location=(1, 2, 3, 4), query=query,
            return_fields=('pkey_interpretatie',
                           'betrouwbaarheid_interpretatie'))

        assert type(df) is DataFrame

    def test_search(self, mp_wfs, mp_remote_describefeaturetype, mp_remote_md,
                    mp_remote_fc, mp_remote_wfs_feature, mp_dov_xml,
                    informelestratigrafiesearch):
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
        informelestratigrafiesearch : pytest.fixture returning
                pydov.search.interpretaties.InformeleStratigrafieSearch
            An instance of InformeleStratigrafieSearch to perform search
            operations on the DOV type 'Informele stratigrafie'.

        """
        query = PropertyIsEqualTo(propertyname='Proefnummer',
                                  literal='kb21d54e-B45')
        df = informelestratigrafiesearch.search(query=query)

        assert type(df) is DataFrame

        assert list(df) == ['pkey_interpretatie', 'pkey_boring',
                            'pkey_sondering',
                            'betrouwbaarheid_interpretatie',
                            'diepte_laag_van', 'diepte_laag_tot',
                            'beschrijving']

        self.abstract_test_search_checkrows(df, InformeleStratigrafie)

        assert df.pkey_sondering.hasnans

        # dtype checks of the resulting df columns
        fields = InformeleStratigrafie.get_fields(
            source=('wfs', 'xml', 'custom'))
        self.abstract_test_df_dtypes(df, fields)

    def test_search_returnfields(self, mp_remote_wfs_feature,
                                 informelestratigrafiesearch):
        """Test the search method with the query parameter and a selection of
        return fields.

        Test whether the output dataframe contains only the selected return
        fields.

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        informelestratigrafiesearch : pytest.fixture returning
                pydov.search.interpretaties.InformeleStratigrafieSearch
            An instance of InformeleStratigrafieSearch to perform search
            operations on the DOV type 'Informele stratigrafie'.

        """
        query = PropertyIsEqualTo(propertyname='Proefnummer',
                                  literal='kb21d54e-B45')

        df = informelestratigrafiesearch.search(
            query=query, return_fields=('pkey_interpretatie',
                                        'betrouwbaarheid_interpretatie'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_interpretatie',
                            'betrouwbaarheid_interpretatie']

    def test_search_returnfields_subtype(self, mp_remote_wfs_feature,
                                         informelestratigrafiesearch):
        """Test the search method with the query parameter and a selection of
        return fields, including fields from a subtype

        Test whether the output dataframe contains only the selected return
        fields.

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        informelestratigrafiesearch : pytest.fixture returning
                pydov.search.interpretaties.InformeleStratigrafieSearch
            An instance of InformeleStratigrafieSearch to perform search
            operations on the DOV type 'Informele stratigrafie'.

        """
        query = PropertyIsEqualTo(propertyname='Proefnummer',
                                  literal='kb21d54e-B45')

        df = informelestratigrafiesearch.search(
            query=query, return_fields=('pkey_interpretatie',
                                        'betrouwbaarheid_interpretatie',
                                        'diepte_laag_van', 'diepte_laag_tot'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_interpretatie',
                            'betrouwbaarheid_interpretatie',
                            'diepte_laag_van', 'diepte_laag_tot']

    def test_search_returnfields_order(self, mp_remote_wfs_feature,
                                       informelestratigrafiesearch):
        """Test the search method with the query parameter and a selection of
        return fields in another ordering.

        Test whether the output dataframe contains only the selected return
        fields, in the order that is documented in
        docs/description_output_dataframes.rst

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        informelestratigrafiesearch : pytest.fixture returning
                pydov.search.interpretaties.InformeleStratigrafieSearch
            An instance of InformeleStratigrafieSearch to perform search
            operations on the DOV type 'Informele stratigrafie'.

        """
        query = PropertyIsEqualTo(propertyname='Proefnummer',
                                  literal='kb21d54e-B45')

        df = informelestratigrafiesearch.search(
            query=query, return_fields=('pkey_interpretatie',
                                        'betrouwbaarheid_interpretatie',
                                        'diepte_laag_tot', 'diepte_laag_van'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_interpretatie',
                            'betrouwbaarheid_interpretatie',
                            'diepte_laag_van', 'diepte_laag_tot']

    def test_search_wrongreturnfields(self, informelestratigrafiesearch):
        """Test the search method with the query parameter and an inexistent
        return field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        informelestratigrafiesearch : pytest.fixture returning
                pydov.search.interpretaties.InformeleStratigrafieSearch
            An instance of InformeleStratigrafieSearch to perform search
            operations on the DOV type 'Informele stratigrafie'.

        """
        query = PropertyIsEqualTo(propertyname='Proefnummer',
                                  literal='kb21d54e-B45')

        with pytest.raises(InvalidFieldError):
            informelestratigrafiesearch.search(
                query=query, return_fields=('pkey_interpretatie',
                                            'onbestaand'))

    def test_search_wrongreturnfieldstype(self, informelestratigrafiesearch):
        """Test the search method with the query parameter and a single
        return field as string.

        Test whether an AttributeError is raised.

        Parameters
        ----------
        informelestratigrafiesearch : pytest.fixture returning
                pydov.search.interpretaties.InformeleStratigrafieSearch
            An instance of InformeleStratigrafieSearch to perform search
            operations on the DOV type 'Informele stratigrafie'.

        """
        query = PropertyIsEqualTo(propertyname='Proefnummer',
                                  literal='kb21d54e-B45')

        with pytest.raises(AttributeError):
            informelestratigrafiesearch.search(
                query=query, return_fields='pkey_interpretatie')

    def test_search_query_wrongfield(self, informelestratigrafiesearch):
        """Test the search method with the query parameter using an
        inexistent query field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        informelestratigrafiesearch : pytest.fixture returning
                pydov.search.interpretaties.InformeleStratigrafieSearch
            An instance of InformeleStratigrafieSearch to perform search
            operations on the DOV type 'Informele stratigrafie'.

        """
        query = PropertyIsEqualTo(propertyname='onbestaand',
                                  literal='Geotechnisch onderzoek')

        with pytest.raises(InvalidFieldError):
            informelestratigrafiesearch.search(query=query)

    def test_search_query_wrongfield_returnfield(
            self, informelestratigrafiesearch):
        """Test the search method with the query parameter using an
        return-only field as query field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        informelestratigrafiesearch : pytest.fixture returning
                pydov.search.interpretaties.InformeleStratigrafieSearch
            An instance of InformeleStratigrafieSearch to perform search
            operations on the DOV type 'Informele stratigrafie'.

        """
        query = PropertyIsEqualTo(propertyname='diepte_laag_van',
                                  literal='0')

        with pytest.raises(InvalidFieldError):
            informelestratigrafiesearch.search(query=query)

    def test_search_extrareturnfields(self, mp_remote_describefeaturetype,
                                      mp_remote_wfs_feature, mp_dov_xml,
                                      informelestratigrafiesearch):
        """Test the search method with the query parameter and an extra WFS
        field as return field.

        Parameters
        ----------
        informelestratigrafiesearch : pytest.fixture returning
                pydov.search.interpretaties.InformeleStratigrafieSearch
            An instance of InformeleStratigrafieSearch to perform search
            operations on the DOV type 'Informele stratigrafie'.

        """
        query = PropertyIsEqualTo(propertyname='Proefnummer',
                                  literal='kb21d54e-B45')

        df = informelestratigrafiesearch.search(query=query,
                                 return_fields=('pkey_interpretatie',
                                                'gemeente'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_interpretatie', 'gemeente']

    def test_search_customreturnfields(self, mp_remote_describefeaturetype,
                                       mp_remote_wfs_feature, mp_dov_xml,
                                       informelestratigrafiesearch):
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
        informelestratigrafiesearch : pytest.fixture returning
                pydov.search.interpretaties.InformeleStratigrafieSearch
            An instance of InformeleStratigrafieSearch to perform search
            operations on the DOV type 'Informele stratigrafie'.

        """
        query = PropertyIsEqualTo(propertyname='Proefnummer',
                                  literal='kb21d54e-B45')

        df = informelestratigrafiesearch.search(query=query,
                                 return_fields=('pkey_interpretatie',
                                                'pkey_boring',
                                                'pkey_sondering'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_interpretatie', 'pkey_boring',
                            'pkey_sondering']

        assert df.pkey_boring[0] is not None
        assert df.pkey_sondering[0] is None
