# -*- coding: utf-8 -*-
"""Module grouping Exception classes."""


class DOVError(Exception):
    """General error within PyDOV."""
    pass


class RemoteFetchError(DOVError):
    """General error while fetching remote data from DOV webservices."""
    pass


class OWSError(DOVError):
    """Error regarding the OGC web services."""
    pass


class LayerNotFoundError(OWSError):
    """Error that occurs when a specific layer could not be found."""
    pass


class WfsGetFeatureError(OWSError):
    """Error that occurs when requesting features using WFS GetFeature."""
    pass


class InvalidSearchParameterError(DOVError):
    """Error that occurs when given invalid parameters to the DOV search."""
    pass


class InvalidFieldError(DOVError):
    """Error that occurs when using a field outside its scope."""
    pass


class XmlParseError(DOVError):
    """Error that occurs when the parsing of a DOV XML document failed."""
    pass


class LogReplayError(Exception):
    pass


class DOVWarning(Warning):
    """General warning in PyDOV."""
    pass


class XsdFetchWarning(DOVWarning):
    """Emitted when an XSD document fails to be fetched from the DOV
    webservice, resulting in the fields metadata to be incomplete."""


class XmlFetchWarning(DOVWarning):
    """Emitted when an XML document fails to be fetched from the DOV
    webservice, resulting in an incomplete dataframe."""


class XmlStaleWarning(DOVWarning):
    """Emitted when an XML document fails to be fetched from the DOV
    webservice and an older stale version is used from the cache, resulting
    in an out-of-date dataframe."""


class XmlParseWarning(DOVWarning):
    """Emitted when the failure to parse an XML document results in
    an incomplete dataframe."""


class DataParseWarning(DOVWarning):
    """Emitted when some data retrieved from DOV failed to be parsed according
    to the datatypes in pydov. The data that failed to be parsed is removed,
    resulting in an incomplete dataframe."""
