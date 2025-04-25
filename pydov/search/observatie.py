# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV observation data."""
from ..types.observatie import Observatie
from .abstract import AbstractSearch


class ObservatieSearch(AbstractSearch):
    """Search class to retrieve information about observations (Observatie)."""

    def __init__(self, objecttype=Observatie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Observatie type.
            Optional: defaults to the Observatie type containing the fields
            described in the documentation.

        """
        super(ObservatieSearch, self).__init__(
            'monster:observaties', objecttype)
