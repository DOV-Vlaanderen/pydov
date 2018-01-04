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
