# -*- coding: utf-8 -*-
import pydov.util.caching
from pydov.util.hooks import Hooks, SimpleStatusHook
from pydov.util.net import SessionFactory

__author__ = """DOV-Vlaanderen"""
__version__ = '2.1.0'

cache = pydov.util.caching.GzipTextFileCache()

hooks = Hooks(
    (SimpleStatusHook(),)
)

# Package wide requests session object. This increases performance as using a
# session object allows connection pooling and TCP connection reuse.
session = SessionFactory.get_session()
