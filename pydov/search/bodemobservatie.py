# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV
bodemobservatie data."""
from ..types.bodemobservatie import Bodemobservatie
from .abstract import AbstractSearch


class BodemobservatieSearch(AbstractSearch):
    """Search class to retrieve information about bodemobservaties."""

    def __init__(self, objecttype=Bodemobservatie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Bodemobservatie type.
            Optional: defaults to the Bodemobservatie type containing the
            fields described in the documentation.

        """
        super(BodemobservatieSearch, self).__init__('bodem:bodemobservaties',
                                                    objecttype)
