# -*- coding: utf-8 -*-
import requests

import pydov.util.caching
from pydov.util.hooks import SimpleStatusHook

__author__ = """DOV-Vlaanderen"""
__version__ = '0.1.3'

cache = pydov.util.caching.GzipTextFileCache()

hooks = [
    SimpleStatusHook(),
]

# Package wide requests session object. This increases performance as using a
# session object allows connection pooling and TCP connection reuse.
session = requests.Session(timeout=60)
session.headers.update({'user-agent': 'pydov/%s' % pydov.__version__})
