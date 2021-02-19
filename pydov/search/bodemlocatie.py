# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV bodemlocatie data."""
from ..types.bodemlocatie import Bodemlocatie
from .abstract import AbstractSearch


class BodemlocatieSearch(AbstractSearch):
    """Search class to retrieve information about bodemlocaties."""

    def __init__(self, objecttype=Bodemlocatie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Bodemlocatie type.
            Optional: defaults to the Bodemlocatie type containing the fields
            described in the documentation.

        """
        super(BodemlocatieSearch, self).__init__('bodem:bodemlocaties',
                                                 objecttype)
