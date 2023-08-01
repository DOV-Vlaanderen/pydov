import pydov
import pytest
import os
import re

from owslib.etree import etree
from owslib.fes2 import PropertyIsGreaterThanOrEqualTo
from pydov.search.boring import BoringSearch
from pydov.util import owsutil

location_md_metadata = 'tests/data/types/boring/md_metadata.xml'
location_fc_featurecatalogue = \
    'tests/data/types/boring/fc_featurecatalogue.xml'
location_wfs_capabilities = 'tests/data/wfs_paging/wfscapabilities.xml'
location_wfs_describefeaturetype = \
    'tests/data/types/boring/wfsdescribefeaturetype.xml'
location_wfs_getfeature = 'tests/data/wfs_paging/wfsgetfeature.xml'

page_size = 10


@pytest.fixture
def wfs_capabilities():
    """PyTest fixture providing the WFS GetCapabilities response based on a 
    local copy. Adjusts the CountDefault parameter to the configured 
    `page_size` in this module.

    Returns
    -------
    bytes
        WFS 2.0.0 GetCapabilities response.
    """
    with open('tests/data/util/owsutil/wfscapabilities.xml', 'r',
              encoding='utf-8') as f:

        data = re.sub(r'<ows:Constraint name="CountDefault"><ows:NoValues/>'
                      r'<ows:DefaultValue>[1-9][0-9]*</ows:DefaultValue>'
                      r'</ows:Constraint>',
                      '<ows:Constraint name="CountDefault"><ows:NoValues/>'
                      f'<ows:DefaultValue>{page_size}</ows:DefaultValue>'
                      '</ows:Constraint>',
                      f.read())

        if not isinstance(data, bytes):
            data = data.encode('utf-8')

    return data


@pytest.fixture
def mp_wfs_max_features(monkeypatch, wfs_capabilities):
    """Monkeypatch the call to get the WFS capabilities maximum features.

    This ensures the maximum features are read from the testdata capabilities.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.
    wfs_capabilities : pytest.fixture
        PyTest fixture providing the WFS capabilities from the testdata.

    """
    max_features = owsutil.get_wfs_max_features(wfs_capabilities)

    def __get_wfs_max_features(*args, **kwargs):
        return max_features

    monkeypatch.setattr(pydov.util.owsutil,
                        'get_wfs_max_features',
                        __get_wfs_max_features)


@pytest.fixture
def mp_remote_wfs_paged_feature(monkeypatch, request):
    """Monkeypatch the call to get WFS features.

    This monkeypatch requires a module variable ``location_wfs_getfeature``
    with the path to the wfs_getfeature file on disk.

    This patch uses both the start_index as well as the max_features from the
    WFS request to ensure the right page and number of results are returned.

    Parameters
    ----------
    monkeypatch : pytest.fixture
        PyTest monkeypatch fixture.
    request : pytest.fixture
        PyTest fixture providing request context.

    """
    def __get_remote_wfs_feature(*args, **kwargs):
        start_index = int(kwargs['get_feature_request'].get('startIndex'))

        count = kwargs['get_feature_request'].get('count')
        count = int(count) if count is not None else None

        file_path = getattr(request.module, "location_wfs_getfeature")
        file_path = (file_path[:file_path.rfind(
            '.')] + f'_{start_index//page_size}' +
            file_path[file_path.rfind('.'):])

        if not os.path.exists(file_path):
            raise RuntimeError(
                f'Error reading testdata: {file_path} does not exist.')

        with open(file_path, 'r') as f:
            data = f.read()

            if count is not None:
                tree = etree.fromstring(data)
                members = tree.findall(
                    './/{http://www.opengis.net/wfs/2.0}member')
                for i in range(len(members)):
                    if i >= count:
                        tree.remove(members[i])
                data = etree.tostring(tree)

            if not isinstance(data, bytes):
                data = data.encode('utf-8')
        return data

    monkeypatch.setattr(pydov.util.owsutil,
                        'wfs_get_feature',
                        __get_remote_wfs_feature)


class TestSearchWfsPaging(object):
    """Class grouping tests regarding WFS paging."""

    def test_all_features_paged(
            self, mp_wfs, mp_get_schema, mp_remote_describefeaturetype,
            mp_wfs_max_features, mp_remote_wfs_paged_feature):
        """Test a search needing multiple pages.

        Test whether the number of returned features is correct.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_wfs_max_features : pytest.fixture
            Monkeypatch the call to get the maximum features from the
            capabilities.
        mp_remote_wfs_paged_feature : pytest.fixture
            Monkeypatch the call to the remote WFS GetFeature, with support
            for paging.

        """
        s = BoringSearch()
        df = s.search(query=PropertyIsGreaterThanOrEqualTo(
            'diepte_tot_m', '0'), return_fields=['pkey_boring'])
        assert len(df) == 20

    def test_max_features_first_page(
            self, mp_wfs, mp_get_schema, mp_remote_describefeaturetype,
            mp_wfs_max_features, mp_remote_wfs_paged_feature):
        """Test a search using max_features where the maximum is less than the
        WFS page size.

        Test whether the number of returned features is correct.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_wfs_max_features : pytest.fixture
            Monkeypatch the call to get the maximum features from the
            capabilities.
        mp_remote_wfs_paged_feature : pytest.fixture
            Monkeypatch the call to the remote WFS GetFeature, with support
            for paging.

        """
        s = BoringSearch()
        df = s.search(return_fields=['pkey_boring'], max_features=5)
        assert len(df) == 5

    def test_max_features_paged(
            self, mp_wfs, mp_get_schema, mp_remote_describefeaturetype,
            mp_wfs_max_features, mp_remote_wfs_paged_feature):
        """Test a search using max_features where the maximum is greater than
        the WFS page size.

        Test whether the number of returned features is correct.

        Parameters
        ----------
        mp_wfs : pytest.fixture
            Monkeypatch the call to the remote GetCapabilities request.
        mp_wfs_max_features : pytest.fixture
            Monkeypatch the call to get the maximum features from the
            capabilities.
        mp_remote_wfs_paged_feature : pytest.fixture
            Monkeypatch the call to the remote WFS GetFeature, with support
            for paging.

        """
        s = BoringSearch()
        df = s.search(return_fields=['pkey_boring'], max_features=15)
        assert len(df) == 15
