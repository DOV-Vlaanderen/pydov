# -*- coding: utf-8 -*-
"""Module grouping utility functions for DOV XML services."""
import requests

import pydov
from owslib.etree import etree
from pydov.util.errors import XmlParseError


def get_remote_url(url):
    """Request the URL from the remote service and return its contents.

    Parameters
    ----------
    url : str
        URL to download.

    Returns
    -------
    xml : bytes
        The raw XML data as bytes.

    """
    headers = {'user-agent': 'PyDOV/%s' % pydov.__version__}

    request = requests.get(url, headers=headers, timeout=60)
    request.encoding = 'utf-8'
    return request.text.encode('utf8')


def get_xsd_schema(url):
    """Request the XSD schema from DOV webservices and return it.

    Parameters
    ----------
    url : str
        URL of the XSD schema to download.

    Returns
    -------
    xml : bytes
        The raw XML data of this XSD schema as bytes.

    """
    return get_remote_url(url)


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
    return get_remote_url(url)


def parse_dov_xml(xml_data):
    """Parse the given XML data into an ElementTree.

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
