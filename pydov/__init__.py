# -*- coding: utf-8 -*-
import pydov.util.caching
from pydov.util.hooks import SimpleStatusHook

__author__ = """DOV-Vlaanderen"""
__version__ = '0.1.1'

cache = pydov.util.caching.GzipTextFileCache()

hooks = [
    SimpleStatusHook(),
]
