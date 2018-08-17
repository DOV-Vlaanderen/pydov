"""Module grouping tests for the boring search module."""
import datetime

import pytest
from pandas import DataFrame

from owslib.fes import PropertyIsEqualTo
from pydov.search.boring import BoringSearch
from pydov.types.boring import Boring
from pydov.util import owsutil
from pydov.util.errors import (
    InvalidFieldError,
)
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

location_md_metadata = 'tests/data/types/boring/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/boring/fc_featurecatalogue.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/boring/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/types/boring/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/boring/feature.xml'
location_dov_xml = 'tests/data/types/boring/boring.xml'


@pytest.fixture
def md_metadata(wfs, mp_remote_md):
    """PyTest fixture providing a MD_Metadata instance of the
    dov-pub:Boringen layer.

    Parameters
    ----------
    wfs : pytest.fixture returning owslib.wfs.WebFeatureService
        WebFeatureService based on the local GetCapabilities.
    mp_remote_md : pytest.fixture
        Monkeypatch the call to get the remote metadata of the
        dov-pub:Boringen layer.

    Returns
    -------
    owslib.iso.MD_Metadata
        Parsed metadata describing the Boringen WFS layer in more detail,
        in the ISO 19115/19139 format.

    """
    contentmetadata = wfs.contents['dov-pub:Boringen']
    return owsutil.get_remote_metadata(contentmetadata)


@pytest.fixture
def boringsearch():
    """PyTest fixture returning an instance of pydov.search.BoringSearch.

    Returns
    -------
    pydov.search.BoringSearch
        An instance of BoringSearch to perform search operations on the DOV
        type 'Boring'.

    """
    return BoringSearch()


class TestBoringSearch(AbstractTestSearch):
    """Class grouping tests for the pydov.search.BoringSearch class."""
    def test_get_fields(self, mp_wfs, mp_remote_describefeaturetype,
                        mp_remote_md, mp_remote_fc, boringsearch):
        """Test the get_fields method.

        Test whether the returned fields match the format specified
        in the documentation.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            dov-pub:Boringen layer.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata of the
            dov-pub:Boringen layer.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue
            of the
            dov-pub:Boringen layer.
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations
            on the DOV type 'Boring'.
        """
        fields = boringsearch.get_fields()
        self.abstract_test_get_fields(fields)

    def test_search_both_location_query(self, mp_remote_describefeaturetype,
                                        mp_remote_wfs_feature, boringsearch):
        """Test the search method providing both a location and a query.

        Test whether a dataframe is returned.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            dov-pub:Boringen layer.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        query = PropertyIsEqualTo(propertyname='gemeente',
                                  literal='Blankenberge')

        df = boringsearch.search(location=(1, 2, 3, 4),
                                 query=query,
                                 return_fields=('pkey_boring', 'boornummer'))

        assert type(df) is DataFrame

    def test_search(self, mp_wfs, mp_remote_describefeaturetype, mp_remote_md,
                    mp_remote_fc, mp_remote_wfs_feature, mp_dov_xml,
                    boringsearch):
        """Test the search method with only the query parameter.

        Test whether the result is correct.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            dov-pub:Boringen layer.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata of the
            dov-pub:Boringen layer.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue of the
            dov-pub:Boringen layer.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote Boring XML data.
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')
        df = boringsearch.search(query=query)

        assert type(df) is DataFrame

        assert list(df) == ['pkey_boring', 'boornummer', 'x', 'y', 'mv_mtaw',
                            'start_boring_mtaw', 'gemeente',
                            'diepte_boring_van', 'diepte_boring_tot',
                            'datum_aanvang', 'uitvoerder', 'boorgatmeting',
                            'diepte_methode_van', 'diepte_methode_tot',
                            'boormethode']

        self.abstract_test_search_checkrows(df, Boring)

        assert df.mv_mtaw.hasnans

        # dtype checks of the resulting df columns
        fields = Boring.get_fields()
        self.abstract_test_df_dtypes(df, fields)

        # specific test for the Zulu time wfs 1.1.0 issue
        assert df.datum_aanvang.unique()[0] == datetime.date(2004, 12, 20)

    def test_search_returnfields(self, mp_remote_wfs_feature,
                                 boringsearch):
        """Test the search method with the query parameter and a selection of
        return fields.

        Test whether the output dataframe contains only the selected return
        fields.

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        df = boringsearch.search(query=query,
                                 return_fields=('pkey_boring', 'boornummer',
                                                'diepte_boring_tot',
                                                'datum_aanvang'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_boring', 'boornummer', 'diepte_boring_tot',
                            'datum_aanvang']

    def test_search_returnfields_subtype(self, mp_remote_wfs_feature,
                                         boringsearch):
        """Test the search method with the query parameter and a selection of
        return fields, including fields from a subtype.

        Test whether the output dataframe contains only the selected return
        fields.

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        df = boringsearch.search(query=query,
                                 return_fields=('pkey_boring', 'boornummer',
                                                'diepte_methode_van',
                                                'diepte_methode_tot'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_boring', 'boornummer', 'diepte_methode_van',
                            'diepte_methode_tot']

    def test_search_returnfields_order(self, mp_remote_wfs_feature,
                                       boringsearch):
        """Test the search method with the query parameter and a selection of
        return fields in another ordering.

        Test whether the output dataframe contains only the selected return
        fields, in the order that is documented in
        docs/description_output_dataframes.rst

        Parameters
        ----------
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        df = boringsearch.search(query=query,
                                 return_fields=('pkey_boring', 'boornummer',
                                                'datum_aanvang',
                                                'diepte_boring_tot'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_boring', 'boornummer', 'diepte_boring_tot',
                            'datum_aanvang']

    def test_search_wrongreturnfields(self, boringsearch):
        """Test the search method with the query parameter and an inexistent
        return field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        with pytest.raises(InvalidFieldError):
            boringsearch.search(query=query,
                                return_fields=('pkey_boring', 'onbestaand'))

    def test_search_wrongreturnfieldstype(self, boringsearch):
        """Test the search method with the query parameter and a single
        return field as string.

        Test whether an AttributeError is raised.

        Parameters
        ----------
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        with pytest.raises(AttributeError):
            boringsearch.search(query=query,
                                return_fields='datum_aanvang')

    def test_search_query_wrongfield(self, boringsearch):
        """Test the search method with the query parameter using an
        inexistent query field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        query = PropertyIsEqualTo(propertyname='onbestaand',
                                  literal='Geotechnisch onderzoek')

        with pytest.raises(InvalidFieldError):
            boringsearch.search(query=query)

    def test_search_query_wrongfield_returnfield(self, boringsearch):
        """Test the search method with the query parameter using an
        return-only field as query field.

        Test whether an InvalidFieldError is raised.

        Parameters
        ----------
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        query = PropertyIsEqualTo(propertyname='boormethode',
                                  literal='Geotechnisch onderzoek')

        with pytest.raises(InvalidFieldError):
            boringsearch.search(query=query)

    def test_search_extrareturnfields(self, mp_remote_describefeaturetype,
                                      mp_remote_wfs_feature, mp_dov_xml,
                                      boringsearch):
        """Test the search method with the query parameter and an extra WFS
        field as return field.

        Parameters
        ----------
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        df = boringsearch.search(query=query,
                                 return_fields=('pkey_boring', 'doel'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_boring', 'doel']

    def test_search_xmlresolving(self, mp_remote_describefeaturetype,
                                 mp_remote_wfs_feature, mp_dov_xml,
                                 boringsearch):
        """Test the search method with return fields from XML but not from a
        subtype.

        Test whether the output dataframe contains the resolved XML data.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            dov-pub:Boringen layer.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        mp_dov_xml : pytest.fixture
            Monkeypatch the call to get the remote Boring XML data.
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        df = boringsearch.search(query=query,
                                 return_fields=('pkey_boring', 'boornummer',
                                                'boorgatmeting'))

        assert type(df) is DataFrame

        assert list(df) == ['pkey_boring', 'boornummer', 'boorgatmeting']
        assert not df.boorgatmeting[0]
