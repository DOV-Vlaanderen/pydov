# -*- coding: utf-8 -*-
import requests

import pydov.util.caching
from pydov.util.hooks import (
    SimpleStatusHook,
    Hooks,
)

__author__ = """DOV-Vlaanderen"""
__version__ = '2.0.1'

cache = pydov.util.caching.GzipTextFileCache()

hooks = Hooks(
    (SimpleStatusHook(),)
)

# Package wide requests session object. This increases performance as using a
# session object allows connection pooling and TCP connection reuse.
request_timeout = 300
session = requests.Session()
session.headers.update({'user-agent': 'pydov/{}'.format(pydov.__version__)})
