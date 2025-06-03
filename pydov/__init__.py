# -*- coding: utf-8 -*-
import pydov.util.caching
from pydov.util.hooks import Hooks, SimpleStatusHook
from pydov.util.net import SessionFactory, proxy_autoconfiguration

__author__ = """DOV-Vlaanderen"""
__version__ = '3.3.0'

cache = pydov.util.caching.GzipTextFileCache()

hooks = Hooks(
    (SimpleStatusHook(),)
)

# try proxy autoconfiguration via PAC
proxy_autoconfiguration()

# Package wide requests session object. This increases performance as using a
# session object allows connection pooling and TCP connection reuse.
session = SessionFactory.get_session()
