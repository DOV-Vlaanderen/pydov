# -*- coding: utf-8 -*-
"""Module containing generic search classes to retrieve DOV WFS data."""

from pydov.search.abstract import AbstractSearch
from pydov.types.generic import WfsTypeFactory


class WfsSearch(AbstractSearch):
    """Search class for generic WFS layers from DOV."""

    def __init__(self, layer):
        """Initialisation.

        Create a new WfsSearch instance to query a generic WFS layer from DOV.
        Check out the available WFS layers via
        https://dov.vlaanderen.be/geonetwork

        Parameters
        ----------
        layer : str
            Workspace qualified layername of the layer to query.
        """
        super(WfsSearch, self).__init__(
            layer, WfsTypeFactory.get_wfs_type(layer))
