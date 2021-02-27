# -*- coding: utf-8 -*-
"""Module implementing a local cache for downloaded XML files."""
import datetime
import gzip
import os
import re
import shutil
import tempfile
import warnings

from pydov.util.dovutil import build_dov_url, get_dov_xml
from pydov.util.errors import RemoteFetchError, XmlStaleWarning
from pydov.util.hooks import HookRunner


class AbstractCache(object):
    """Abstract base class for caching of downloaded XML files from DOV.

    Attributes
    ----------
    stale_on_error : bool, default to True
        Whether to return stale responses from the cache in case of a network
        error prevents downloading a fresh copy.
    """

    def __init__(self):
        """Initialisation."""
        self.stale_on_error = True

    def _get_remote(self, url, session=None):
        """Get the XML data by requesting it from the given URL.

        Parameters
        ----------
        url : str
            Permanent URL to a DOV object.
        session : requests.Session
            Session to use to perform HTTP requests for data. Defaults to None,
            which means a new session will be created for each request.

        Returns
        -------
        xml : bytes
            The raw XML data of this DOV object as bytes.

        """
        xml = get_dov_xml(url, session)
        HookRunner.execute_xml_downloaded(url.rstrip('.xml'))
        return xml

    def _emit_cache_hit(self, url):
        """Emit the XML cache hit event for all registered hooks.

        This notifies hooks that a valid XML document has been returned from
        the cache.

        Parameters
        ----------
        url : str
            Permanent URL to a DOV object.
        """
        HookRunner.execute_xml_cache_hit(url.rstrip('.xml'))

    def _emit_stale_hit(self, url):
        """Emit the XML stale hit event for all registered hooks.

        This notifies hooks that a stale XML document has been returned from
        the cache.

        Parameters
        ----------
        url : str
            Permanent URL to a DOV object.
        """
        HookRunner.execute_xml_stale_hit(url.rstrip('.xml'))

    def get(self, url, session=None):
        """Get the XML data for the DOV object referenced by the given URL.

        Because of parallel processing, this method will be called
        simultaneously from multiple threads. Make sure your implementation is
        threadsafe or uses locking.

        If a valid version exists in the cache, it will be loaded and
        returned. If no valid version exists, the XML will be downloaded
        from the DOV webservice, saved in the cache and returned.

        Parameters
        ----------
        url : str
            Permanent URL to a DOV object.
        session : requests.Session
            Session to use to perform HTTP requests for data. Defaults to None,
            which means a new session will be created for each request.

        Returns
        -------
        xml : bytes
            The raw XML data of this DOV object as bytes.

        """
        raise NotImplementedError('This should be implemented in a subclass.')

    def clean(self):
        """Clean the cache by removing old records from the cache.

        Since during normal use the cache only grows by adding new objects and
        overwriting existing ones with a new version, you can use this
        function to clean the cache. It will remove all records older than
        the maximum age from the cache.

        """
        raise NotImplementedError('This should be implemented in a subclass.')

    def remove(self):
        """Remove the entire cache."""
        raise NotImplementedError('This should be implemented in a subclass.')


class AbstractFileCache(AbstractCache):
    """Abstract class for filebased caching of downloaded XML files from
    DOV."""

    def __init__(self, max_age=datetime.timedelta(weeks=2), cachedir=None):
        """Initialisation.

        Set up the instance variables and create the cache directory if
        it does not exists already.

        Parameters
        ----------
        max_age : datetime.timedelta, optional
            The maximum age of a cached XML file to be valid. If the last
            modification date of the file is before this time, it will be
            redownloaded. Defaults to two weeks.
        cachedir : str, optional
            Path of the directory that will be used to save the cached XML
            files. Be sure to use a directory that will only be used for
            this PyDOV cache. Default to a temporary directory provided by
            the operating system.

        """
        super().__init__()

        if cachedir:
            self.cachedir = cachedir
        else:
            self.cachedir = os.path.join(tempfile.gettempdir(), 'pydov')
        self.max_age = max_age

        self._re_type_key = re.compile(
            build_dov_url('data/') + r'([^ /]+)/([^.]+)'
        )

        try:
            if not os.path.exists(self.cachedir):
                os.makedirs(self.cachedir)
        except Exception:
            pass

    def _get_filepath(self, datatype, key):
        """Get the location on disk where the object with given datatype and
        key is to be saved.

        Parameters
        ----------
        datatype : str
            Datatype of the DOV object.
        key : str
            Unique and permanent object key of the DOV object.

        Returns
        -------
        str
            Full absolute path on disk where the object is to be saved.

        """
        raise NotImplementedError('This should be implemented in a subclass.')

    def _get_type_key_from_url(self, url):
        """Parse a DOV permalink and return the datatype and object key.

        Parameters
        ----------
        url : str
            Permanent URL to a DOV object.

        Returns
        -------
        datatype : str
            Datatype of the DOV object referred to by the URL.
        key : str
            Unique and permanent key of the instance of the DOV object
            referred to by the URL.

        """
        datatype = self._re_type_key.search(url)
        if datatype and len(datatype.groups()) > 1:
            return datatype.group(1), datatype.group(2)

    def _get_type_key_from_path(self, path):
        """Parse a filepath and return the datatype and object key.

        Parameters
        ----------
        path : str
            Full, absolute, path to a cached file.

        Returns
        -------
        datatype : str
            Datatype of the DOV object referred to by the URL.
        key : str
            Unique and permanent key of the instance of the DOV object
            referred to by the URL.

        """
        raise NotImplementedError('This should be implemented in a subclass.')

    def _is_valid(self, datatype, key):
        """Check if a valid version of the given DOV object exists in the
        cache.

        A cached version is valid if it exists and the last modification
        time of the file is after the maximum age defined on initialisation.

        Parameters
        ----------
        datatype : str
            Datatype of the DOV object.
        key : str
            Unique and permanent object key of the DOV object.

        Returns
        -------
        bool
            True if a valid cached version exists, False otherwise.

        """
        filepath = self._get_filepath(datatype, key)
        if not os.path.exists(filepath):
            return False

        last_modification = datetime.datetime.fromtimestamp(
            os.path.getmtime(filepath))
        now = datetime.datetime.now()

        if (now - last_modification) > self.max_age:
            return False
        else:
            return True

    def _is_stale(self, datatype, key):
        """Check if a stale version of the given DOV object exists in the
        cache.

        A cached version is stale if it exists and the last modification
        time of the file is before the maximum age defined on initialisation.

        Parameters
        ----------
        datatype : str
            Datatype of the DOV object.
        key : str
            Unique and permanent object key of the DOV object.

        Returns
        -------
        bool
            True if a stale cached version exists, False otherwise.
        """
        if self._is_valid(datatype, key):
            return False

        filepath = self._get_filepath(datatype, key)
        return os.path.exists(filepath)

    def _load(self, datatype, key):
        """Read a cached version from disk.

        datatype : str
            Datatype of the DOV object.
        key : str
            Unique and permanent object key of the DOV object.

        Returns
        -------
        str (xml)
            XML string of the DOV object, loaded from the cache.

        """
        raise NotImplementedError('This should be implemented in a subclass.')

    def _save(self, datatype, key, content):
        """Save the given content in the cache.

        Parameters
        ----------
        datatype : str
            Datatype of the DOV object to save.
        key : str
            Unique and permanent object key of the DOV object to save.
        content : bytes
            The raw XML data of this DOV object as bytes.

        """
        raise NotImplementedError('This should be implemented in a subclass.')

    def get(self, url, session=None):
        datatype, key = self._get_type_key_from_url(url)

        data = HookRunner.execute_inject_xml_response(url)

        if data is not None:
            HookRunner.execute_xml_received(url, data)
            return data

        if self._is_valid(datatype, key):
            try:
                self._emit_cache_hit(url)
                data = self._load(datatype, key).encode('utf-8')

                HookRunner.execute_xml_received(url, data)
                return data
            except Exception:
                pass

        try:
            data = self._get_remote(url, session)
        except RemoteFetchError:
            if self.stale_on_error and self._is_stale(datatype, key):
                self._emit_stale_hit(url)
                warnings.warn((
                    "Failed to fetch remote XML document for "
                    "object '{}', using older stale version from cache. "
                    "Resulting dataframe will be out-of-date.".format(url)),
                    XmlStaleWarning)

                data = self._load(datatype, key).encode('utf-8')
                return data
            else:
                HookRunner.execute_xml_fetch_error(url)
                raise RemoteFetchError
        else:
            try:
                self._save(datatype, key, data)
            except Exception:
                pass

        return data

    def clean(self):
        """Clean the cache by removing old records from the cache.

        Since during normal use the cache only grows by adding new objects and
        overwriting existing ones with a new version, you can use this
        function to clean the cache. It will remove all records older than
        the maximum age from the cache.

        Note that this method is currently not called anywhere in the code,
        but it is provided as reference.

        """
        if os.path.exists(self.cachedir):
            for type in os.listdir(self.cachedir):
                for object in os.listdir(os.path.join(self.cachedir, type)):
                    datatype, key = self._get_type_key_from_path(
                        os.path.join(self.cachedir, type, object))
                    if not self._is_valid(datatype, key):
                        os.remove(
                            os.path.join(self.cachedir, datatype, object))

    def remove(self):
        """Remove the entire cache directory.

        Note that the default directory to save the cache is a temporary
        location provided by the operating system, and as a subsequence the
        OS will normally take care of its removal.

        Note that this method is currently not called anywhere in the code,
        but it is provided as reference.

        """
        if os.path.exists(self.cachedir):
            shutil.rmtree(self.cachedir)


class PlainTextFileCache(AbstractFileCache):
    """Class for plain text caching of downloaded XML files from DOV."""

    def _get_filepath(self, datatype, key):
        return os.path.join(self.cachedir, datatype, key + '.xml')

    def _get_type_key_from_path(self, path):
        key = os.path.basename(path).rstrip('.xml')
        datatype = os.path.dirname(path).split()[-1]
        return datatype, key

    def _save(self, datatype, key, content):
        filepath = self._get_filepath(datatype, key)
        folder = os.path.dirname(filepath)

        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.decode('utf-8'))

    def _load(self, datatype, key):
        filepath = self._get_filepath(datatype, key)
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()


class GzipTextFileCache(AbstractFileCache):
    """Class for GZipped text caching of downloaded XML files from DOV."""

    def _get_filepath(self, datatype, key):
        return os.path.join(self.cachedir, datatype, key + '.xml.gz')

    def _get_type_key_from_path(self, path):
        key = os.path.basename(path).rstrip('.xml.gz')
        datatype = os.path.dirname(path).split()[-1]
        return datatype, key

    def _save(self, datatype, key, content):
        filepath = self._get_filepath(datatype, key)
        folder = os.path.dirname(filepath)

        if not os.path.exists(folder):
            os.makedirs(folder)

        with gzip.open(filepath, 'wb') as f:
            f.write(content)

    def _load(self, datatype, key):
        filepath = self._get_filepath(datatype, key)
        with gzip.open(filepath, 'rb') as f:
            return f.read().decode('utf-8')
