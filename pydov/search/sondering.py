# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV CPT data."""
from pydov.search.abstract import AbstractSearch
from pydov.types.sondering import Sondering


class SonderingSearch(AbstractSearch):
    """Search class to retrieve information about CPT measurements (
    Sonderingen)."""

    def __init__(self, objecttype=Sondering):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Sondering type.
            Optional: defaults to the Sondering type containing
            the fields described in the documentation.

        """
        super(SonderingSearch, self).__init__(
            'dov-pub:Sonderingen', objecttype)
