import os
import platform
import signal
import sys
import tempfile
import time
from subprocess import Popen

import pytest
from owslib.fes import PropertyIsEqualTo

import pydov
from pydov.search.boring import BoringSearch
from pydov.util.caching import GzipTextFileCache
from tests.abstract import ServiceCheck


@pytest.fixture(scope="module", autouse=True)
def dov_proxy_no_xdov():
    process = Popen([sys.executable,
                     os.path.join('tests', 'stub', 'dov_proxy.py'),
                     '--no-xdov'])
    time.sleep(2)

    os.environ['PYDOV_BASE_URL'] = 'http://localhost:1337/'
    gziptext_cache = GzipTextFileCache(
        cachedir=os.path.join(tempfile.gettempdir(), 'pydov_tests_error'))
    pydov.cache = gziptext_cache

    yield gziptext_cache

    gziptext_cache.remove()
    del os.environ['PYDOV_BASE_URL']

    if platform.system() == 'Windows':
        process.send_signal(signal.CTRL_C_EVENT)
    else:
        process.send_signal(signal.SIGINT)
    time.sleep(2)


class TestErrorPaths(object):
    """Class grouping tests related failing DOV services."""

    @pytest.mark.online
    @pytest.mark.skipif(not ServiceCheck.service_ok(),
                        reason="DOV service is unreachable")
    def test_do_not_cache_error(self):
        bs = BoringSearch()
        bs.search(query=PropertyIsEqualTo(
            'pkey_boring',
            'https://www.dov.vlaanderen.be/data/boring/2016-122561'))

        assert not os.path.exists(os.path.join(
            pydov.cache.cachedir, 'boring', '2016-122561.xml.gz'
        ))
        # assert not np.isnan(df.iloc[0].boorgatmeting)
