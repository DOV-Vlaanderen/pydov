import datetime
import gzip
import os
import platform
import signal
import sys
import tempfile
import time
from importlib import reload
from subprocess import Popen

import numpy as np
import pytest
from owslib.fes import PropertyIsEqualTo

import pydov
from pydov.search.boring import BoringSearch
from pydov.search.grondwaterfilter import GrondwaterFilterSearch
from pydov.util.caching import GzipTextFileCache
from pydov.util.errors import XmlFetchWarning, XmlStaleWarning, XsdFetchWarning
from tests.abstract import ServiceCheck


@pytest.fixture(scope="module", autouse=True)
def dov_proxy_no_xdov():
    process = Popen([sys.executable,
                     os.path.join('tests', 'stub', 'dov_proxy.py'),
                     '--no-xdov'])
    time.sleep(2)

    os.environ['PYDOV_BASE_URL'] = 'http://localhost:1337/'

    yield

    del os.environ['PYDOV_BASE_URL']

    if platform.system() == 'Windows':
        process.send_signal(signal.CTRL_C_EVENT)
    else:
        process.send_signal(signal.SIGINT)
    time.sleep(2)


@pytest.fixture(scope="module", autouse=True)
def reload_modules(dov_proxy_no_xdov):
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
        Fixture starting up the DOV proxy stub and setting PYDOV_BASE_URL
        accordingly.
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


class TestErrorPaths(object):
    """Class grouping tests related failing DOV services."""

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_do_not_cache_error(self):
        bs = BoringSearch(objecttype=pydov.types.boring.Boring)

        bs.search(query=PropertyIsEqualTo(
            'pkey_boring',
            'https://www.dov.vlaanderen.be/data/boring/2004-103984'))

        assert not os.path.exists(os.path.join(
            pydov.cache.cachedir, 'boring', '2004-103984.xml.gz'
        ))
        assert False

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_do_not_overwrite_stale_cache(self):
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
            'pkey_boring',
            'https://www.dov.vlaanderen.be/data/boring/2004-103984'))

        with gzip.open(cache_path, 'rb') as cached_data:
            assert 'GEO-04/169-BNo-B1' in cached_data.read().decode('utf8')

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_stale_warning(self):
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
                'pkey_boring',
                'https://www.dov.vlaanderen.be/data/boring/2004-103984'))

        assert df.iloc[0].boorgatmeting == False
        assert df.iloc[0].boormethode == 'spade'

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_wfs_data_present(self):
        bs = BoringSearch(objecttype=pydov.types.boring.Boring)

        df = bs.search(query=PropertyIsEqualTo(
            'pkey_boring',
            'https://www.dov.vlaanderen.be/data/boring/2016-122561'))

        assert df.iloc[0].gemeente == 'Wortegem-Petegem'

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_nan_and_fetch_warning(self):
        bs = BoringSearch(objecttype=pydov.types.boring.Boring)

        with pytest.warns(XmlFetchWarning):
            df = bs.search(query=PropertyIsEqualTo(
                'pkey_boring',
                'https://www.dov.vlaanderen.be/data/boring/2016-122561'))

        assert np.isnan(df.iloc[0].boorgatmeting)

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_no_xsd_warning(self):
        with pytest.warns(XsdFetchWarning):
            gwf = GrondwaterFilterSearch(
                objecttype=pydov.types.grondwaterfilter.GrondwaterFilter)
            fields = gwf.get_fields()

        assert 'values' not in fields['aquifer_code']

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_no_xsd_wfs_only(self):
        gwf = GrondwaterFilterSearch(
            objecttype=pydov.types.grondwaterfilter.GrondwaterFilter)

        df = gwf.search(max_features=1)
        assert df.iloc[0].pkey_filter is not None
