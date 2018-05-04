"""Module grouping tests for the search grondwaterfilter module."""
import sys

import pytest
from pandas import DataFrame

import pydov
from owslib.fes import PropertyIsEqualTo
from pydov.search.grondwaterfilter import GrondwaterFilterSearch
from pydov.types.grondwaterfilter import GrondwaterFilter
from tests.abstract import AbstractTestSearch

from tests.test_search import (
    mp_wfs,
    wfs,
)

@pytest.fixture
def grondwaterfiltersearch():
    """PyTest fixture returning an instance of pydov.search.BoringSearch.

    Returns
    -------
    pydov.search.BoringSearch
        An instance of BoringSearch to perform search operations on the DOV
        type 'Boring'.

    """
    return GrondwaterFilterSearch()


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
        with open(
            'tests/data/types/grondwaterfilter/wfsdescribefeaturetype.xml',
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
        with open('tests/data/types/grondwaterfilter/md_metadata.xml',
                  'r') as f:
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
def mp_remote_fc(monkeypatch):
    """Monkeypatch the call to get the remote feature catalogue of the
    dov-pub:Boringen layer.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """

    def __get_remote_fc(*args, **kwargs):
        with open('tests/data/types/grondwaterfilter/fc_featurecatalogue.xml',
                  'r') as f:
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
def mp_remote_wfs_feature(monkeypatch):
    """Monkeypatch the call to get WFS features.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.

    """
    def __get_remote_wfs_feature(*args, **kwargs):
        with open('tests/data/types/grondwaterfilter/wfsgetfeature.xml',
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
        with open('tests/data/types/grondwaterfilter/grondwaterfilter.xml',
                  'r') as f:
            data = f.read()
            if type(data) is not bytes:
                data = data.encode('utf-8')
        return data

    monkeypatch.setattr(pydov.types.abstract.AbstractDovType,
                        '_get_xml_data', _get_xml_data)


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
            dov-pub:Boringen layer.
        mp_remote_md : pytest.fixture
            Monkeypatch the call to get the remote metadata of the
            dov-pub:Boringen layer.
        mp_remote_fc : pytest.fixture
            Monkeypatch the call to get the remote feature catalogue
            of the
            dov-pub:Boringen layer.
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
            dov-pub:Boringen layer.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        boringsearch : pytest.fixture returning pydov.search.BoringSearch
            An instance of BoringSearch to perform search operations on the DOV
            type 'Boring'.

        """
        query = PropertyIsEqualTo(propertyname='gemeente',
                                  literal='Blankenberge')

        df = grondwaterfiltersearch.search(
            location=(1, 2, 3, 4), query=query,
            return_fields=('pkey_filter', 'filternummer'))

        assert type(df) is DataFrame
