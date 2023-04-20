# -*- coding: utf-8 -*-
"""Module containing the generic DOV data types."""

from pydov.types.abstract import AbstractDovType


class WfsTypeFactory:
    """Class to generate pydov type classes at runtime for given WFS layers."""

    @staticmethod
    def get_wfs_type(layer):
        """Generate a new pydov WfsType class for the given layer.

        Parameters
        ----------
        layer : str
            Workspace qualified layer name, uniquely identifying the layer
            within the DOV WFS service.

        Returns
        -------
        class
            WfsType class for the given layer.
        """
        class WfsType(AbstractDovType):

            fields = []

            def __init__(self, pkey):
                super().__init__(layer, pkey)

        return WfsType
