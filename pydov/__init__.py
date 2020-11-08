# -*- coding: utf-8 -*-
import requests
import urllib3

import pydov.util.caching
from pydov.util.hooks import Hooks, SimpleStatusHook
from pydov.util.net import TimeoutHTTPAdapter

__author__ = """DOV-Vlaanderen"""
__version__ = '2.0.0'

cache = pydov.util.caching.GzipTextFileCache()

hooks = Hooks(
    (SimpleStatusHook(),)
)

# Package wide requests session object. This increases performance as using a
# session object allows connection pooling and TCP connection reuse.
request_timeout = 300
session = requests.Session()

session.headers.update({'user-agent': 'pydov/{}'.format(pydov.__version__)})

try:
    retry = urllib3.util.Retry(total=10, connect=5, read=3, redirect=5,
                               allowed_methods=set(['GET', 'POST']))
except TypeError:
    retry = urllib3.util.Retry(total=10, connect=5, read=3, redirect=5,
                               method_whitelist=set(['GET', 'POST']))

adapter = TimeoutHTTPAdapter(timeout=request_timeout, max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
