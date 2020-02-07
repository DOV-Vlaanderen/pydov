# -*- coding: utf-8 -*-
"""Module grouping utility functions for DOV XML services."""
import os

from owslib.etree import etree
from pydov.util.errors import XmlParseError
import pydov
from pydov.util.hooks import HookRunner


def build_dov_url(path):
    """Build the DOV url consisting of the fixed DOV base url, appended with
    the given path.

    Returns
    -------
    str
        The absolute DOV url.

    """
    if 'PYDOV_BASE_URL' in os.environ:
        base_url = os.environ['PYDOV_BASE_URL']
    else:
        base_url = 'https://www.dov.vlaanderen.be/'

    return base_url + path.lstrip('/')


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

    request = pydov.session.get(url, timeout=pydov.request_timeout)
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
    response = HookRunner.execute_inject_meta_response(url)

    if response is None:
        response = get_remote_url(url)

    HookRunner.execute_meta_received(url, response)

    return response


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
    response = HookRunner.execute_inject_xml_response(url)

    if response is None:
        response = get_remote_url(url)

    HookRunner.execute_xml_received(url, response)

    return response


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
