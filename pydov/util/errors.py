class DOVError(Exception):
    """General error within PyDOV."""
    pass


class OWSError(DOVError):
    """Error regarding the OGC web services."""
    pass


class LayerNotFoundError(OWSError):
    """Error that occurs when a specific layer could not be found."""
    pass


class MetadataNotFoundError(OWSError):
    """Error that occurs when the metadata could not be found."""
    pass


class FeatureCatalogueNotFoundError(OWSError):
    """Error that occurs when the feature catalogue could not be found."""
    pass


class WfsGetFeatureError(OWSError):
    """Error that occurs when requesting features using WFS GetFeature."""
    pass


class FeatureOverflowError(OWSError):
    """Error that occurs when the amount of features returned by the WFS
    query reached the server limit."""
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


class DOVWarning(Warning):
    """General warning in PyDOV."""
    pass


class XmlParseWarning(DOVWarning):
    """Emitted when the failure to parse an XML document results in
    an incomplete dataframe."""
