# -*- coding: utf-8 -*-
"""Module grouping utility functions for DOV XML services."""
import requests

import pydov
from owslib.etree import etree
from pydov.util.errors import XmlParseError

# Global requests session object. This increases performance as using a
# session object allows connection pooling and TCP connection reuse. It is
# initialised upon first usage by get_dov_xml().
session = None


def get_dov_xml(url):
    """Request the XML from the remote DOV webservices and return it.

    Parameters
    ----------
    url : str
        URL of the DOV object to download.

    Returns
    -------
    xml : bytes
        The raw XML data of this DOV object as bytes.

    """
    global session
    if not session:
        session = requests.Session()
        session.headers.update({'user-agent': 'PyDOV/%s' % pydov.__version__})

    request = session.get(url, timeout=60)
    request.encoding = 'utf-8'
    return request.text.encode('utf8')


def parse_dov_xml(xml_data):
    """Parse the given XML data into an ElemenTree.

    Parameters
    ----------
    xml_data : bytes
        The raw XML data of a DOV object as bytes.

    Returns
    -------
    tree : etree.ElementTree
        Parsed XML tree of the DOV object.

    """
    try:
        parser = etree.XMLParser(ns_clean=True, recover=True)
    except TypeError:
        parser = etree.XMLParser()

    try:
        tree = etree.fromstring(xml_data, parser=parser)
        return tree
    except Exception:
        raise XmlParseError("Failed to parse XML record.")
