import datetime
import gzip
import os
import sys
import tempfile
import time
from importlib import reload
from subprocess import Popen

import numpy as np
import pytest
from owslib.fes2 import PropertyIsEqualTo

import pydov
from pydov.search.boring import BoringSearch
from pydov.search.grondwaterfilter import GrondwaterFilterSearch
from pydov.util.caching import GzipTextFileCache
from pydov.util.dovutil import build_dov_url
from pydov.util.errors import XmlFetchWarning, XmlStaleWarning, XsdFetchWarning
from pydov.util.hooks import Hooks
from tests.abstract import ServiceCheck
from tests.test_util_hooks import HookCounter


@pytest.fixture(scope="module", autouse=True)
def dov_proxy_no_xdov():
    """Fixture to start the DOV proxy and set PYDOV_BASE_URL to route
    traffic through it.

    The DOV proxy behaves as the XDOV server would be unavailable.

    """
    process = Popen([sys.executable,
                     os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'stub', 'dov_proxy.py'),
                     '--dov-base-url', build_dov_url('/'),
                     '--no-xdov'])
    time.sleep(2)

    orig_base_url = os.environ.get('PYDOV_BASE_URL', None)
    os.environ['PYDOV_BASE_URL'] = 'http://localhost:1337/'

    yield

    if orig_base_url is not None:
        os.environ['PYDOV_BASE_URL'] = orig_base_url
    else:
        del(os.environ['PYDOV_BASE_URL'])

    process.terminate()
    process.communicate()


@pytest.fixture(scope="module", autouse=True)
def reload_modules(dov_proxy_no_xdov):
    """Reload the boring and grondwaterfilter modules after setting
    PYDOV_BASE_URL.

    These need to be reloaded because they use the PYDOV_BASE_URL at import
    time to set the location of XSD schemas.

    Parameters
    ----------
    dov_proxy_no_xdov : pytest.fixture
        Fixture starting the DOV proxy and setting PYDOV_BASE_URL accordingly.
    """
    reload(pydov.types.boring)
    reload(pydov.types.grondwaterfilter)

    yield

    reload(pydov.types.boring)
    reload(pydov.types.grondwaterfilter)


@pytest.fixture(scope="function", autouse=True)
def reset_cache(dov_proxy_no_xdov):
    """Reset the cache to a temporary folder to remove influence from other
    tests.

    The cache needs to be reset after setting the PYDOV_BASE_URL variable
    because at initialisation this URL is used to construct a regex for
    determining the datatype of an XML request.

    Parameters
    ----------
    dov_proxy_no_xdov : pytest.fixture
        Fixture starting the DOV proxy and setting PYDOV_BASE_URL accordingly.
    """
    gziptext_cache = GzipTextFileCache(
        cachedir=os.path.join(tempfile.gettempdir(), 'pydov_tests_error'),
        max_age=datetime.timedelta(seconds=0.1))
    gziptext_cache.remove()

    orig_cache = pydov.cache
    pydov.cache = gziptext_cache

    yield

    gziptext_cache.remove()
    pydov.cache = orig_cache


@pytest.fixture
def test_hook_count():
    """PyTest fixture temporarily disabling default hooks and installing
    HookCounter."""
    orig_hooks = pydov.hooks

    pydov.hooks = Hooks(
        (HookCounter(),)
    )
    yield

    pydov.hooks = orig_hooks


class TestNoXDOV(object):
    """Class grouping tests related failing DOV services."""

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_do_not_cache_error(self):
        """Test whether the 404 error page does not end up being cached."""
        bs = BoringSearch(objecttype=pydov.types.boring.Boring)

        bs.search(query=PropertyIsEqualTo(
            'pkey_boring', build_dov_url('data/boring/2004-103984')))

        assert not os.path.exists(os.path.join(
            pydov.cache.cachedir, 'boring', '2004-103984.xml.gz'
        ))

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_do_not_overwrite_stale_cache(self):
        """Test whether a stale copy of the data which exists in the cache is
        not overwritten by the 404 error page."""
        bs = BoringSearch(objecttype=pydov.types.boring.Boring)

        testdata_path = os.path.join(
            'tests', 'data', 'types', 'boring', 'boring.xml')

        cache_path = os.path.join(
            pydov.cache.cachedir, 'boring', '2004-103984.xml.gz'
        )
        os.makedirs(os.path.dirname(cache_path))

        with open(testdata_path, 'r') as testdata:
            with gzip.open(cache_path, 'wb') as cached_data:
                cached_data.write(testdata.read().encode('utf8'))
        time.sleep(0.5)

        bs.search(query=PropertyIsEqualTo(
            'pkey_boring', build_dov_url('data/boring/2004-103984')))

        with gzip.open(cache_path, 'rb') as cached_data:
            assert 'GEO-04/169-BNo-B1' in cached_data.read().decode('utf8')

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_stale_warning(self):
        """Test whether a stale version of the data from the cache is used in
        case of a service error, and if a warning is issued to the user."""
        bs = BoringSearch(objecttype=pydov.types.boring.Boring)

        testdata_path = os.path.join(
            'tests', 'data', 'types', 'boring', 'boring.xml')

        cache_path = os.path.join(
            pydov.cache.cachedir, 'boring', '2004-103984.xml.gz'
        )
        os.makedirs(os.path.dirname(cache_path))

        with open(testdata_path, 'r') as testdata:
            with gzip.open(cache_path, 'wb') as cached_data:
                cached_data.write(testdata.read().encode('utf8'))
        time.sleep(0.5)

        with pytest.warns(XmlStaleWarning):
            df = bs.search(query=PropertyIsEqualTo(
                'pkey_boring', build_dov_url('data/boring/2004-103984')))

        assert not df.iloc[0].boorgatmeting
        assert df.iloc[0].boormethode == 'spade'

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_stale_disabled(self):
        """Test whether no stale version of the data from the cache is used
        when disabled, and if a warning is issued to the user."""
        pydov.cache.stale_on_error = False

        bs = BoringSearch(objecttype=pydov.types.boring.Boring)

        testdata_path = os.path.join(
            'tests', 'data', 'types', 'boring', 'boring.xml')

        cache_path = os.path.join(
            pydov.cache.cachedir, 'boring', '2004-103984.xml.gz'
        )
        os.makedirs(os.path.dirname(cache_path))

        with open(testdata_path, 'r') as testdata:
            with gzip.open(cache_path, 'wb') as cached_data:
                cached_data.write(testdata.read().encode('utf8'))
        time.sleep(0.5)

        with pytest.warns(XmlFetchWarning):
            df = bs.search(query=PropertyIsEqualTo(
                'pkey_boring', build_dov_url('data/boring/2004-103984')))

        assert np.isnan(df.iloc[0].boorgatmeting)
        assert np.isnan(df.iloc[0].boormethode)

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_wfs_data_present(self):
        """Test whether data available in the WFS is present in the dataframe
        in case of a service error in XDOV."""
        bs = BoringSearch(objecttype=pydov.types.boring.Boring)

        df = bs.search(query=PropertyIsEqualTo(
            'pkey_boring', build_dov_url('data/boring/2016-122561')))

        assert df.iloc[0].gemeente == 'Wortegem-Petegem'

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_nan_and_fetch_warning(self):
        """Test whether the XML data is set tot NaN in case of an error and
        no stale cache is available. Also test if a warning is given to the
        user."""
        bs = BoringSearch(objecttype=pydov.types.boring.Boring)

        with pytest.warns(XmlFetchWarning):
            df = bs.search(query=PropertyIsEqualTo(
                'pkey_boring', build_dov_url('data/boring/2016-122561')))

        assert np.isnan(df.iloc[0].boorgatmeting)

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_no_xsd_warning(self):
        """Test whether the metadata can still be retrieved, and that the
        XSD values are unavailable. Also test if a warning is given to the
        user."""
        with pytest.warns(XsdFetchWarning):
            gwf = GrondwaterFilterSearch(
                objecttype=pydov.types.grondwaterfilter.GrondwaterFilter)
            fields = gwf.get_fields()

        assert 'values' not in fields['aquifer_code']

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_no_xsd_wfs_only(self):
        """Test whether the WFS data is available, even if XSD schemas cannot
        be resolved."""
        gwf = GrondwaterFilterSearch(
            objecttype=pydov.types.grondwaterfilter.GrondwaterFilter)

        df = gwf.search(max_features=1)
        assert df.iloc[0].pkey_filter is not None

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_hooks_fetch_error(self, test_hook_count):
        """Test if the correct hooks are fired when the XML fails to be
        fetched from DOV.

        Parameters
        ----------
        test_hook_count : pytest.fixture
            Fixture removing default hooks and installing HookCounter.
        """
        bs = BoringSearch(objecttype=pydov.types.boring.Boring)

        bs.search(query=PropertyIsEqualTo(
            'pkey_boring', build_dov_url('data/boring/2004-103984')))

        assert pydov.hooks[0].count_wfs_search_init == 1
        assert pydov.hooks[0].count_wfs_search_result == 1
        assert pydov.hooks[0].count_wfs_search_result_received == 1

        assert pydov.hooks[0].count_xml_received == 0
        assert pydov.hooks[0].count_xml_cache_hit == 0
        assert pydov.hooks[0].count_xml_downloaded == 0
        assert pydov.hooks[0].count_xml_stale_hit == 0
        assert pydov.hooks[0].count_xml_fetch_error == 1

        assert pydov.hooks[0].count_meta_received > 0
        assert pydov.hooks[0].count_inject_meta_response > 0

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_hooks_stale(self, test_hook_count):
        """Test if the correct hooks are fired when a stale XML document is
        returned from the cache.

        Parameters
        ----------
        test_hook_count : pytest.fixture
            Fixture removing default hooks and installing HookCounter.
        """
        bs = BoringSearch(objecttype=pydov.types.boring.Boring)

        testdata_path = os.path.join(
            'tests', 'data', 'types', 'boring', 'boring.xml')

        cache_path = os.path.join(
            pydov.cache.cachedir, 'boring', '2004-103984.xml.gz'
        )
        os.makedirs(os.path.dirname(cache_path))

        with open(testdata_path, 'r') as testdata:
            with gzip.open(cache_path, 'wb') as cached_data:
                cached_data.write(testdata.read().encode('utf8'))
        time.sleep(0.5)

        bs.search(query=PropertyIsEqualTo(
            'pkey_boring', build_dov_url('data/boring/2004-103984')))

        assert pydov.hooks[0].count_wfs_search_init == 1
        assert pydov.hooks[0].count_wfs_search_result == 1
        assert pydov.hooks[0].count_wfs_search_result_received == 1

        assert pydov.hooks[0].count_xml_received == 0
        assert pydov.hooks[0].count_xml_cache_hit == 0
        assert pydov.hooks[0].count_xml_downloaded == 0
        assert pydov.hooks[0].count_xml_stale_hit == 1
        assert pydov.hooks[0].count_xml_fetch_error == 0

        assert pydov.hooks[0].count_meta_received > 0
        assert pydov.hooks[0].count_inject_meta_response > 0
