# -*- encoding: utf-8 -*-
import os
import time

import pytest

import pydov
from owslib.fes import PropertyIsEqualTo
from pydov.search.boring import BoringSearch

from tests.abstract import (
    AbstractTestSearch,
    service_ok,
)

from tests.test_util_caching import (
    cache,
    nocache,
)

class TestEncoding(AbstractTestSearch):
    """Class grouping tests related to encoding issues."""

    @pytest.mark.online
    @pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
    @nocache
    def test_search(self):
        """Test the search method with strange character in the output.

        Test whether the output has the correct encoding.

        """
        boringsearch = BoringSearch()
        query = PropertyIsEqualTo(
            propertyname='pkey_boring',
            literal='https://www.dov.vlaanderen.be/data/boring/1928-031159')

        df = boringsearch.search(query=query,
                                 return_fields=('pkey_boring', 'uitvoerder'))

        assert df.uitvoerder[0] == u'Societé Belge des Bétons'

    @pytest.mark.online
    @pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
    def test_search_cache(self, cache):
        """Test the search method with strange character in the output.

        Test whether the output has the correct encoding, both with and
        without using the cache.

        Parameters
        ----------
        cache : pytest.fixture providing  pydov.util.caching.TransparentCache
            TransparentCache using a temporary directory and a maximum age
            of 1 second.

        """
        orig_cache = pydov.cache
        pydov.cache = cache

        boringsearch = BoringSearch()
        query = PropertyIsEqualTo(
            propertyname='pkey_boring',
            literal='https://www.dov.vlaanderen.be/data/boring/1928-031159')

        df = boringsearch.search(query=query,
                                 return_fields=('pkey_boring', 'uitvoerder',
                                                'mv_mtaw'))

        assert df.uitvoerder[0] == u'Societé Belge des Bétons'

        assert os.path.exists(os.path.join(
            cache.cachedir, 'boring', '1928-031159.xml'))

        df = boringsearch.search(query=query,
                                 return_fields=('pkey_boring', 'uitvoerder',
                                                'mv_mtaw'))

        assert df.uitvoerder[0] == u'Societé Belge des Bétons'

        pydov.cache = orig_cache

    @pytest.mark.online
    @pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
    def test_caching(self, cache):
        """Test the caching of an XML containing strange characters.

        Test whether the data is saved in the cache.

        Parameters
        ----------
        cache : pytest.fixture providing  pydov.util.caching.TransparentCache
            TransparentCache using a temporary directory and a maximum age
            of 1 second.

        """
        cached_file = os.path.join(
            cache.cachedir, 'boring', '1995-056089.xml')

        cache.clean()
        assert not os.path.exists(cached_file)

        cache.get('https://www.dov.vlaanderen.be/data/boring/1995-056089.xml')
        assert os.path.exists(cached_file)

        with open(cached_file, 'r') as cf:
            cached_data = cf.read()
            print(cached_data)
            assert cached_data != ""

        first_download_time = os.path.getmtime(cached_file)

        time.sleep(0.5)
        cache.get('https://www.dov.vlaanderen.be/data/boring/1995-056089.xml')
        # assure we didn't redownload the file:
        assert os.path.getmtime(cached_file) == first_download_time

    @pytest.mark.online
    @pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
    def test_save_content(self, cache):
        """Test the caching of an XML containing strange characters.

        Test if the contents of the saved document are the same as the
        original data.

        Parameters
        ----------
        cache : pytest.fixture providing  pydov.util.caching.TransparentCache
            TransparentCache using a temporary directory and a maximum age
            of 1 second.

        """
        cached_file = os.path.join(
            cache.cachedir, 'boring', '1995-056089.xml')

        cache.clean()
        assert not os.path.exists(cached_file)

        ref_data = cache.get(
            'https://www.dov.vlaanderen.be/data/boring/1995-056089.xml')
        assert os.path.exists(cached_file)

        with open(cached_file, 'r') as cached:
            cached_data = cached.read()

        assert cached_data == ref_data

    @pytest.mark.online
    @pytest.mark.skipif(not service_ok(), reason="DOV service is unreachable")
    def test_reuse_content(self, cache):
        """Test the caching of an XML containing strange characters.

        Test if the contents returned by the cache are the same as the
        original data.

        Parameters
        ----------
        cache : pytest.fixture providing  pydov.util.caching.TransparentCache
            TransparentCache using a temporary directory and a maximum age
            of 1 second.

        """
        cached_file = os.path.join(
            cache.cachedir, 'boring', '1995-056089.xml')

        cache.clean()
        assert not os.path.exists(cached_file)

        ref_data = cache.get(
            'https://www.dov.vlaanderen.be/data/boring/1995-056089.xml')
        assert os.path.exists(cached_file)

        cached_data = cache.get(
            'https://www.dov.vlaanderen.be/data/boring/1995-056089.xml')

        assert cached_data == ref_data
