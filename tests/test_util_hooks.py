import datetime
import pytest

import pydov
from owslib.fes import PropertyIsEqualTo
from pydov.search.boring import BoringSearch
from pydov.util.hooks import (
    AbstractHook,
    SimpleStatusHook,
)
from tests.abstract import service_ok

from tests.test_util_caching import (
    plaintext_cache,
    nocache,
)


class HookCounter(AbstractHook):
    """Hook implementation for testing purposes, counting all event calls."""
    def __init__(self):
        self.count_wfs_search_init = 0
        self.count_wfs_search_result = 0
        self.count_xml_requested = 0
        self.count_xml_cache_hit = 0
        self.count_xml_downloaded = 0

    def wfs_search_init(self, typename):
        """Called upon starting a WFS search.

        Parameters
        ----------
        typename : str
            The typename (layername) of the WFS service used for searching.

        """
        self.count_wfs_search_init += 1

    def wfs_search_result(self, number_of_results):
        """Called after a WFS search finished.

        Parameters
        ----------
        number_of_results : int
            The number of features returned by the WFS search.

        """
        self.count_wfs_search_result += 1

    def xml_requested(self, pkey_object):
        """Called upon requesting an XML document of an object.

        This is either followed by ``xml_cache_hit`` or ``xml_downloaded``.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        self.count_xml_requested += 1

    def xml_cache_hit(self, pkey_object):
        """Called when the XML document of an object is retrieved from the
        cache.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        self.count_xml_cache_hit += 1

    def xml_downloaded(self, pkey_object):
        """Called when the XML document of an object is downloaded from the
        DOV services.

        Parameters
        ----------
        pkey_object : str
            Permanent key of the requested object.

        """
        self.count_xml_downloaded += 1


@pytest.fixture
def temp_hooks():
    """PyTest fixture temporarily disabling default hooks and installing
    HookCounter."""
    orig_hooks = pydov.hooks
    temp_hooks = [HookCounter()]

    pydov.hooks = temp_hooks
    yield

    pydov.hooks = orig_hooks


class TestHooks(object):
    @pytest.mark.online
    @pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
    def test_wfs_only(self, temp_hooks):
        """Test the search method providing both a location and a query.

        Test whether a dataframe is returned.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            dov-pub:Boringen layer.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        temp_hooks : pytest.fixture
            Fixture removing default hooks and installing HookCounter.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        boringsearch = BoringSearch()
        df = boringsearch.search(
            query=query, return_fields=('pkey_boring', 'x', 'y'))

        assert pydov.hooks[0].count_wfs_search_init == 1
        assert pydov.hooks[0].count_wfs_search_result == 1
        assert pydov.hooks[0].count_xml_requested == 0
        assert pydov.hooks[0].count_xml_cache_hit == 0
        assert pydov.hooks[0].count_xml_downloaded == 0

    @pytest.mark.online
    @pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
    def test_wfs_and_xml_nocache(self, temp_hooks, nocache):
        """Test the search method providing both a location and a query.

        Test whether a dataframe is returned.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            dov-pub:Boringen layer.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        temp_hooks : pytest.fixture
            Fixture removing default hooks and installing HookCounter.
        nocache : pytest.fixture
            Fixture temporarily disabling caching.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        boringsearch = BoringSearch()
        df = boringsearch.search(
            query=query, return_fields=('pkey_boring', 'mv_mtaw'))

        assert pydov.hooks[0].count_wfs_search_init == 1
        assert pydov.hooks[0].count_wfs_search_result == 1
        assert pydov.hooks[0].count_xml_requested == 1
        assert pydov.hooks[0].count_xml_cache_hit == 0
        assert pydov.hooks[0].count_xml_downloaded == 1

        df = boringsearch.search(
            query=query, return_fields=('pkey_boring', 'mv_mtaw'))

        assert pydov.hooks[0].count_wfs_search_init == 2
        assert pydov.hooks[0].count_wfs_search_result == 2
        assert pydov.hooks[0].count_xml_requested == 2
        assert pydov.hooks[0].count_xml_cache_hit == 0
        assert pydov.hooks[0].count_xml_downloaded == 2

    @pytest.mark.online
    @pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
    @pytest.mark.parametrize('plaintext_cache',
                             [[datetime.timedelta(minutes=15)]],
                             indirect=['plaintext_cache'])
    def test_wfs_and_xml_cache(self, temp_hooks, plaintext_cache):
        """Test the search method providing both a location and a query.

        Test whether a dataframe is returned.

        Parameters
        ----------
        mp_remote_describefeaturetype : pytest.fixture
            Monkeypatch the call to a remote DescribeFeatureType of the
            dov-pub:Boringen layer.
        mp_remote_wfs_feature : pytest.fixture
            Monkeypatch the call to get WFS features.
        temp_hooks : pytest.fixture
            Fixture removing default hooks and installing HookCounter.
        plaintext_cache : pytest.fixture
            Fixture temporarily setting up a testcache with max_age of 1
            second.

        """
        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        boringsearch = BoringSearch()
        df = boringsearch.search(
            query=query, return_fields=('pkey_boring', 'mv_mtaw'))

        assert pydov.hooks[0].count_wfs_search_init == 1
        assert pydov.hooks[0].count_wfs_search_result == 1
        assert pydov.hooks[0].count_xml_requested == 1
        assert pydov.hooks[0].count_xml_cache_hit == 0
        assert pydov.hooks[0].count_xml_downloaded == 1

        df = boringsearch.search(
            query=query, return_fields=('pkey_boring', 'mv_mtaw'))

        assert pydov.hooks[0].count_wfs_search_init == 2
        assert pydov.hooks[0].count_wfs_search_result == 2
        assert pydov.hooks[0].count_xml_requested == 2
        assert pydov.hooks[0].count_xml_cache_hit == 1
        assert pydov.hooks[0].count_xml_downloaded == 1

    @pytest.mark.online
    @pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
    def test_default_hooks(self, nocache):
        """Test the default hooks by performing a simple search.

        Test whether no exceptions are raised.

        Parameters
        ----------
        nocache : pytest.fixture
            Fixture temporarily disabling caching.

        """
        pydov.hooks = [SimpleStatusHook()]

        query = PropertyIsEqualTo(propertyname='boornummer',
                                  literal='GEO-04/169-BNo-B1')

        boringsearch = BoringSearch()
        df = boringsearch.search(query=query)
