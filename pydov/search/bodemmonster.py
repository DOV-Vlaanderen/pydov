# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV bodemmonster data."""
from ..types.bodemmonster import Bodemmonster
from .abstract import AbstractSearch


class BodemmonsterSearch(AbstractSearch):
    """Search class to retrieve information about bodemmonsters."""

    def __init__(self, objecttype=Bodemmonster):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Bodemmonster type.
            Optional: defaults to the Bodemmonster type containing the fields
            described in the documentation.

        """
        super(BodemmonsterSearch, self).__init__('bodem:bodemmonsters',
                                                 objecttype)
