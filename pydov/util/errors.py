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
