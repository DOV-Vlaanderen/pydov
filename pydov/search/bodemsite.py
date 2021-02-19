# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV bodemsite data."""
from ..types.bodemsite import Bodemsite
from .abstract import AbstractSearch


class BodemsiteSearch(AbstractSearch):
    """Search class to retrieve information about bodemlocaties."""

    def __init__(self, objecttype=Bodemsite):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Bodemsite type.
            Optional: defaults to the Bodemsite type containing the fields
            described in the documentation.

        """
        super(BodemsiteSearch, self).__init__('bodem:bodemsites', objecttype)
