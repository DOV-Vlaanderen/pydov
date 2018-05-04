# -*- coding: utf-8 -*-
"""Module implementing a local cache for downloaded XML files."""
import datetime
import os
import re
import tempfile

from owslib.util import openURL


class TransparentCache(object):
    def __init__(self):
        self.basepath = os.path.join(tempfile.gettempdir(), 'pydov')
        self.max_age = datetime.timedelta(weeks=2)
        self.re_type_key = re.compile(
            r'https?://www.dov.vlaanderen.be/data/([' '^/]+)/([^\.]+)')

        try:
            if not os.path.exists(self.basepath):
                os.makedirs(self.basepath)
        except Exception:
            pass

    def _get_type_key(self, url):
        datatype = self.re_type_key.search(url)
        if datatype and len(datatype.groups()) > 1:
            return datatype.group(1), datatype.group(2)

    def _save(self, datatype, key, content):
        folder = os.path.join(self.basepath, datatype)

        if not os.path.exists(folder):
            os.makedirs(folder)

        filepath = os.path.join(folder, key + '.xml')
        with open(filepath, 'w') as f:
            f.write(content)

    def _valid(self, datatype, key):
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
        filepath = os.path.join(self.basepath, datatype, key + '.xml')
        with open(filepath, 'r') as f:
            return f.read()

    def get(self, url):
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
