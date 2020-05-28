"""Module grouping tests for the pydov.util.caching module."""

import gzip
import os
import time

import pytest

from pydov.util.dovutil import build_dov_url


class TestPlainTextFileCacheCache(object):
    """Class grouping tests for the pydov.util.caching.PlainTextFileCache
    class."""

    @pytest.mark.parametrize('plaintext_cache', [[]],
                             indirect=['plaintext_cache'])
    def test_clean(self, plaintext_cache, mp_remote_xml):
        """Test the clean method.

        Test whether the cached file and the cache directory are nonexistent
        after the clean method has been called.

        Parameters
        ----------
        plaintext_cache : pytest.fixture providing
                pydov.util.caching.PlainTextFileCache
            PlainTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            plaintext_cache.cachedir, 'boring', '2004-103984.xml')

        plaintext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

        plaintext_cache.clean()
        assert os.path.exists(cached_file)
        assert os.path.exists(plaintext_cache.cachedir)

        time.sleep(1.5)
        plaintext_cache.clean()
        assert not os.path.exists(cached_file)
        assert os.path.exists(plaintext_cache.cachedir)

    @pytest.mark.parametrize('plaintext_cache', [[]],
                             indirect=['plaintext_cache'])
    def test_remove(self, plaintext_cache, mp_remote_xml):
        """Test the remove method.

        Test whether the cache directory is nonexistent after the remove
        method has been called.

        Parameters
        ----------
        plaintext_cache : pytest.fixture providing
                pydov.util.caching.PlainTextFileCache
            PlainTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            plaintext_cache.cachedir, 'boring', '2004-103984.xml')

        plaintext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

        plaintext_cache.remove()
        assert not os.path.exists(cached_file)
        assert not os.path.exists(plaintext_cache.cachedir)

    @pytest.mark.parametrize('plaintext_cache', [[]],
                             indirect=['plaintext_cache'])
    def test_get_save(self, plaintext_cache, mp_remote_xml):
        """Test the get method.

        Test whether the document is saved in the cache.

        Parameters
        ----------
        plaintext_cache : pytest.fixture providing
                pydov.util.caching.PlainTextFileCache
            PlainTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            plaintext_cache.cachedir, 'boring', '2004-103984.xml')

        plaintext_cache.clean()
        assert not os.path.exists(cached_file)

        plaintext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

    @pytest.mark.parametrize('plaintext_cache', [[]],
                             indirect=['plaintext_cache'])
    def test_get_reuse(self, plaintext_cache, mp_remote_xml):
        """Test the get method.

        Test whether the document is saved in the cache and reused in a
        second function call.

        Parameters
        ----------
        plaintext_cache : pytest.fixture providing
                pydov.util.caching.PlainTextFileCache
            PlainTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            plaintext_cache.cachedir, 'boring', '2004-103984.xml')

        plaintext_cache.clean()
        assert not os.path.exists(cached_file)

        plaintext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

        first_download_time = os.path.getmtime(cached_file)

        time.sleep(0.5)
        plaintext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        # assure we didn't redownload the file:
        assert os.path.getmtime(cached_file) == first_download_time

    @pytest.mark.parametrize('plaintext_cache', [[]],
                             indirect=['plaintext_cache'])
    def test_get_invalid(self, plaintext_cache, mp_remote_xml):
        """Test the get method.

        Test whether the document is saved in the cache not reused if the
        second function call is after the maximum age of the cached file.

        Parameters
        ----------
        plaintext_cache : pytest.fixture providing
                pydov.util.caching.PlainTextFileCache
            PlainTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            plaintext_cache.cachedir, 'boring', '2004-103984.xml')

        plaintext_cache.clean()
        assert not os.path.exists(cached_file)

        plaintext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

        first_download_time = os.path.getmtime(cached_file)

        time.sleep(1.5)
        plaintext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        # assure we did redownload the file, since original is invalid now:
        assert os.path.getmtime(cached_file) > first_download_time

    @pytest.mark.parametrize('plaintext_cache', [[]],
                             indirect=['plaintext_cache'])
    def test_save_content(self, plaintext_cache, mp_remote_xml):
        """Test whether the data is saved in the cache.

        Test if the contents of the saved document are the same as the
        original data.

        Parameters
        ----------
        plaintext_cache : pytest.fixture providing
                pydov.util.caching.PlainTextFileCache
            PlainTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            plaintext_cache.cachedir, 'boring', '2004-103984.xml')

        plaintext_cache.clean()
        assert not os.path.exists(cached_file)

        plaintext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

        with open('tests/data/types/boring/boring.xml', 'r',
                  encoding='utf-8') as ref:
            ref_data = ref.read()

        with open(cached_file, 'r', encoding='utf-8') as cached:
            cached_data = cached.read()

        assert cached_data == ref_data

    @pytest.mark.parametrize('plaintext_cache', [[]],
                             indirect=['plaintext_cache'])
    def test_reuse_content(self, plaintext_cache, mp_remote_xml):
        """Test whether the saved data is reused.

        Test if the contents returned by the cache are the same as the
        original data.

        Parameters
        ----------
        plaintext_cache : pytest.fixture providing
                pydov.util.caching.PlainTextFileCache
            PlainTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            plaintext_cache.cachedir, 'boring', '2004-103984.xml')

        plaintext_cache.clean()
        assert not os.path.exists(cached_file)

        plaintext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

        with open('tests/data/types/boring/boring.xml', 'r') as ref:
            ref_data = ref.read().encode('utf-8')

        cached_data = plaintext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))

        assert cached_data == ref_data

    @pytest.mark.parametrize('plaintext_cache', [[]],
                             indirect=['plaintext_cache'])
    def test_return_type(self, plaintext_cache, mp_remote_xml):
        """The the return type of the get method.

        Test whether the get method returns the data in the same datatype (
        i.e. bytes) regardless of the data was cached or not.

        Parameters
        ----------
        plaintext_cache : pytest.fixture providing
                pydov.util.caching.PlainTextFileCache
            PlainTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            plaintext_cache.cachedir, 'boring', '2004-103984.xml')

        plaintext_cache.clean()
        assert not os.path.exists(cached_file)

        ref_data = plaintext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert isinstance(ref_data, bytes)

        assert os.path.exists(cached_file)

        cached_data = plaintext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert isinstance(cached_data, bytes)


class TestGzipTextFileCacheCache(object):
    """Class grouping tests for the pydov.util.caching.PlainTextFileCache
    class."""

    @pytest.mark.parametrize('gziptext_cache', [[]],
                             indirect=['gziptext_cache'])
    def test_clean(self, gziptext_cache, mp_remote_xml):
        """Test the clean method.

        Test whether the cached file and the cache directory are nonexistent
        after the clean method has been called.

        Parameters
        ----------
        gziptext_cache : pytest.fixture providing
                pydov.util.caching.GzipTextFileCache
            GzipTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            gziptext_cache.cachedir, 'boring', '2004-103984.xml.gz')

        gziptext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

        gziptext_cache.clean()
        assert os.path.exists(cached_file)
        assert os.path.exists(gziptext_cache.cachedir)

        time.sleep(1.5)
        gziptext_cache.clean()
        assert not os.path.exists(cached_file)
        assert os.path.exists(gziptext_cache.cachedir)

    @pytest.mark.parametrize('gziptext_cache', [[]],
                             indirect=['gziptext_cache'])
    def test_remove(self, gziptext_cache, mp_remote_xml):
        """Test the remove method.

        Test whether the cache directory is nonexistent after the remove
        method has been called.

        Parameters
        ----------
        gziptext_cache : pytest.fixture providing
                pydov.util.caching.GzipTextFileCache
            GzipTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            gziptext_cache.cachedir, 'boring', '2004-103984.xml.gz')

        gziptext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

        gziptext_cache.remove()
        assert not os.path.exists(cached_file)
        assert not os.path.exists(gziptext_cache.cachedir)

    @pytest.mark.parametrize('gziptext_cache', [[]],
                             indirect=['gziptext_cache'])
    def test_get_save(self, gziptext_cache, mp_remote_xml):
        """Test the get method.

        Test whether the document is saved in the cache.

        Parameters
        ----------
        gziptext_cache : pytest.fixture providing
                pydov.util.caching.GzipTextFileCache
            GzipTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            gziptext_cache.cachedir, 'boring', '2004-103984.xml.gz')

        gziptext_cache.clean()
        assert not os.path.exists(cached_file)

        gziptext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

    @pytest.mark.parametrize('gziptext_cache', [[]],
                             indirect=['gziptext_cache'])
    def test_get_reuse(self, gziptext_cache, mp_remote_xml):
        """Test the get method.

        Test whether the document is saved in the cache and reused in a
        second function call.

        Parameters
        ----------
        gziptext_cache : pytest.fixture providing
                pydov.util.caching.GzipTextFileCache
            GzipTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            gziptext_cache.cachedir, 'boring', '2004-103984.xml.gz')

        gziptext_cache.clean()
        assert not os.path.exists(cached_file)

        gziptext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

        first_download_time = os.path.getmtime(cached_file)

        time.sleep(0.5)
        gziptext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        # assure we didn't redownload the file:
        assert os.path.getmtime(cached_file) == first_download_time

    @pytest.mark.parametrize('gziptext_cache', [[]],
                             indirect=['gziptext_cache'])
    def test_get_invalid(self, gziptext_cache, mp_remote_xml):
        """Test the get method.

        Test whether the document is saved in the cache not reused if the
        second function call is after the maximum age of the cached file.

        Parameters
        ----------
        gziptext_cache : pytest.fixture providing
                pydov.util.caching.GzipTextFileCache
            GzipTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            gziptext_cache.cachedir, 'boring', '2004-103984.xml.gz')

        gziptext_cache.clean()
        assert not os.path.exists(cached_file)

        gziptext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

        first_download_time = os.path.getmtime(cached_file)

        time.sleep(1.5)
        gziptext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        # assure we did redownload the file, since original is invalid now:
        assert os.path.getmtime(cached_file) > first_download_time

    @pytest.mark.parametrize('gziptext_cache', [[]],
                             indirect=['gziptext_cache'])
    def test_save_content(self, gziptext_cache, mp_remote_xml):
        """Test whether the data is saved in the cache.

        Test if the contents of the saved document are the same as the
        original data.

        Parameters
        ----------
        gziptext_cache : pytest.fixture providing
                pydov.util.caching.GzipTextFileCache
            GzipTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            gziptext_cache.cachedir, 'boring', '2004-103984.xml.gz')

        gziptext_cache.clean()
        assert not os.path.exists(cached_file)

        gziptext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

        with open('tests/data/types/boring/boring.xml', 'r',
                  encoding='utf-8') as ref:
            ref_data = ref.read()

        with gzip.open(cached_file, 'rb') as cached:
            cached_data = cached.read().decode('utf-8')

        assert cached_data == ref_data

    @pytest.mark.parametrize('gziptext_cache', [[]],
                             indirect=['gziptext_cache'])
    def test_reuse_content(self, gziptext_cache, mp_remote_xml):
        """Test whether the saved data is reused.

        Test if the contents returned by the cache are the same as the
        original data.

        Parameters
        ----------
        gziptext_cache : pytest.fixture providing
                pydov.util.caching.GzipTextFileCache
            GzipTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            gziptext_cache.cachedir, 'boring', '2004-103984.xml.gz')

        gziptext_cache.clean()
        assert not os.path.exists(cached_file)

        gziptext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert os.path.exists(cached_file)

        with open('tests/data/types/boring/boring.xml', 'r') as ref:
            ref_data = ref.read().encode('utf-8')

        cached_data = gziptext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))

        assert cached_data == ref_data

    @pytest.mark.parametrize('gziptext_cache', [[]],
                             indirect=['gziptext_cache'])
    def test_return_type(self, gziptext_cache, mp_remote_xml):
        """The the return type of the get method.

        Test whether the get method returns the data in the same datatype (
        i.e. bytes) regardless of the data was cached or not.

        Parameters
        ----------
        gziptext_cache : pytest.fixture providing
                pydov.util.caching.GzipTextFileCache
            GzipTextFileCache using a temporary directory and a maximum age
            of 1 second.
        mp_remote_xml : pytest.fixture
            Monkeypatch the call to the remote DOV service returning an XML
            document.

        """
        cached_file = os.path.join(
            gziptext_cache.cachedir, 'boring', '2004-103984.xml.gz')

        gziptext_cache.clean()
        assert not os.path.exists(cached_file)

        ref_data = gziptext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert isinstance(ref_data, bytes)

        assert os.path.exists(cached_file)

        cached_data = gziptext_cache.get(
            build_dov_url('data/boring/2004-103984.xml'))
        assert isinstance(cached_data, bytes)
