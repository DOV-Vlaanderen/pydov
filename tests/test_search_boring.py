"""Module grouping tests for the boring search module."""
import datetime
import sys

import pytest
from pandas import DataFrame

import pydov
from owslib.etree import etree
from owslib.fes import PropertyIsEqualTo
from pydov.search.boring import BoringSearch
from pydov.types.boring import Boring
from pydov.util import owsutil
from pydov.util.errors import (
    InvalidSearchParameterError,
    InvalidFieldError,
)
from tests.abstract import AbstractTestSearch

from tests.test_search import (
    mp_wfs,
    wfs,
)


@pytest.fixture
def mp_remote_md(wfs, monkeypatch):
    """Monkeypatch the call to get the remote metadata of the
    dov-pub:Boringen layer.

    Parameters
    ----------
    wfs : pytest.fixture returning owslib.wfs.WebFeatureService
        WebFeatureService based on the local GetCapabilities.
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """
    def __get_remote_md(*args, **kwargs):
        with open('tests/data/types/boring/md_metadata.xml', 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    if sys.version_info[0] < 3:
        monkeypatch.setattr('pydov.util.owsutil.__get_remote_md.func_code',
                            __get_remote_md.func_code)
    else:
        monkeypatch.setattr('pydov.util.owsutil.__get_remote_md.__code__',
                            __get_remote_md.__code__)


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
def mp_remote_fc(monkeypatch):
    """Monkeypatch the call to get the remote feature catalogue of the
    dov-pub:Boringen layer.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """
    def __get_remote_fc(*args, **kwargs):
        with open('tests/data/types/boring/fc_featurecatalogue.xml', 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    if sys.version_info[0] < 3:
        monkeypatch.setattr('pydov.util.owsutil.__get_remote_fc.func_code',
                            __get_remote_fc.func_code)
    else:
        monkeypatch.setattr('pydov.util.owsutil.__get_remote_fc.__code__',
                            __get_remote_fc.__code__)


@pytest.fixture
def mp_remote_describefeaturetype(monkeypatch):
    """Monkeypatch the call to a remote DescribeFeatureType of the
    dov-pub:Boringen layer.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """
    def __get_remote_describefeaturetype(*args, **kwargs):
        with open('tests/data/types/boring/wfsdescribefeaturetype.xml',
                  'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    if sys.version_info[0] < 3:
        monkeypatch.setattr(
            'pydov.util.owsutil.__get_remote_describefeaturetype.func_code',
            __get_remote_describefeaturetype.func_code)
    else:
        monkeypatch.setattr(
            'pydov.util.owsutil.__get_remote_describefeaturetype.__code__',
            __get_remote_describefeaturetype.__code__)


@pytest.fixture
def wfs_getfeature():
    """PyTest fixture providing a WFS GetFeature response for the
    dov-pub:Boringen layer.

    Returns
    -------
    str
        WFS response of a GetFeature call to the dov-pub:Boringen layer.

    """
    with open('tests/data/types/boring/wfsgetfeature.xml', 'r') as f:
        data = f.read()
        return data


@pytest.fixture
def mp_remote_wfs_feature(monkeypatch):
    """Monkeypatch the call to get WFS features.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """
    def __get_remote_wfs_feature(*args, **kwargs):
        with open('tests/data/types/boring/wfsgetfeature.xml',
                  'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    if sys.version_info[0] < 3:
        monkeypatch.setattr(
            'pydov.util.owsutil.wfs_get_feature',
            __get_remote_wfs_feature)
    else:
        monkeypatch.setattr(
            'pydov.util.owsutil.wfs_get_feature',
            __get_remote_wfs_feature)


@pytest.fixture
def mp_dov_xml(monkeypatch):
    """Monkeypatch the call to get the remote Boring XML data.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """

    def _get_xml_data(*args, **kwargs):
        with open('tests/data/types/boring/boring.xml', 'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    monkeypatch.setattr(pydov.types.abstract.AbstractDovType,
                        '_get_xml_data', _get_xml_data)


@pytest.fixture
def wfs_feature():
    """PyTest fixture providing an XML of a WFS feature element of a Boring
    record.

    Returns
    -------
    etree.Element
        XML element representing a single record of the Boring WFS layer.

    """
    with open('tests/data/types/boring/feature.xml', 'r') as f:
        return etree.fromstring(f.read())


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

        allfields = Boring.get_field_names()
        ownfields = Boring.get_field_names(include_subtypes=False)
        subfields = [f for f in allfields if f not in ownfields]

        for field in list(df):
            if field in ownfields:
                assert len(df[field].unique()) == 1
            elif field in subfields:
                assert len(df[field].unique()) == len(df)

        assert df.mv_mtaw.hasnans

        fields = Boring.get_fields()

        # dtype checks of the resulting df columns
        self.abstract_test_df_dtypes(df, fields)

        assert len(df) == 2
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

    def test_search_query_wrongtype(self, boringsearch):
        """Test the search method with the query parameter using a wrong
        query type.

        Test whether an InvalidSearchParameterError is raised.

        Parameters
        ----------
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        with pytest.raises(InvalidSearchParameterError):
            boringsearch.search(query='computer says no')

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
        assert df.boorgatmeting[0] == False
