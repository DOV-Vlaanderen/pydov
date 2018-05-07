# -*- coding: utf-8 -*-
"""Module implementing a local cache for downloaded XML files."""
import datetime
import os
import re
import shutil
import tempfile

from owslib.util import openURL


class TransparentCache(object):
    """Class for transparent caching of downloaded XML files from DOV."""
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
        if cachedir:
            self.basepath = cachedir
        else:
            self.basepath = os.path.join(tempfile.gettempdir(), 'pydov')
        self.max_age = max_age
        self.re_type_key = re.compile(
            r'https?://www.dov.vlaanderen.be/data/([' '^/]+)/([^\.]+)')

        try:
            if not os.path.exists(self.basepath):
                os.makedirs(self.basepath)
        except Exception:
            pass

    def _get_type_key(self, url):
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
        datatype = self.re_type_key.search(url)
        if datatype and len(datatype.groups()) > 1:
            return datatype.group(1), datatype.group(2)

    def _save(self, datatype, key, content):
        """Save the given content in the cache.

        Parameters
        ----------
        datatype : str
            Datatype of the DOV object to save.
        key : str
            Unique and permanent object key of the DOV object to save.
        content : str (xml)
            XML content describing the DOV object.

        """
        folder = os.path.join(self.basepath, datatype)

        if not os.path.exists(folder):
            os.makedirs(folder)

        filepath = os.path.join(folder, key + '.xml')
        with open(filepath, 'w') as f:
            f.write(content)

    def _valid(self, datatype, key):
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
        filepath = os.path.join(self.basepath, datatype, key + '.xml')
        if not os.path.exists(filepath):
            return False

        last_modification = datetime.datetime.fromtimestamp(
            os.path.getmtime(filepath))
        now = datetime.datetime.now()

        if (now - last_modification) > self.max_age:
            return False
        else:
            return True

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
        filepath = os.path.join(self.basepath, datatype, key + '.xml')
        with open(filepath, 'r') as f:
            return f.read()

    def get(self, url):
        """Get the XML data for the DOV object referenced by the given URL.

        If a valid version exists in the cache, it will be loaded and
        returned. If no valid version exists, the XML will be downloaded
        from the DOV webservice, saved in the cache and returned.

        Parameters
        ----------
        url : str
            Permanent URL to a DOV object.

        Returns
        -------
        str (xml)
            XML content describing the DOV object.

        """
        datatype, key = self._get_type_key(url)

        if self._valid(datatype, key):
            try:
                return self._load(datatype, key).encode('utf-8')
            except Exception:
                pass

        data = openURL(url).read()
        try:
            self._save(datatype, key, data.decode('utf-8'))
        except Exception:
            pass

        return data

    def clean(self):
        """Clean the cache by removing the cache directory.

        Since during normal use the cache grows by adding new objects and
        overwriting existing ones with a new version, you can use this
        function to erase the cache.

        Note that the default directory to save the cache is a temporary
        location provided by the operating system, and as a subsequence the
        OS will normally take care of its removal.

        Note that this method is currently not called anywhere in the code,
        but it is provided as reference.

        """
        shutil.rmtree(self.basepath)
