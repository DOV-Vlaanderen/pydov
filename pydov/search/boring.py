# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV borehole data."""
from ..types.boring import Boring
from .abstract import AbstractSearch


class BoringSearch(AbstractSearch):
    """Search class to retrieve information about boreholes (Boring)."""

    def __init__(self, objecttype=Boring):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Boring type.
            Optional: defaults to the Boring type containing the fields
            described in the documentation.

        """
        super(BoringSearch, self).__init__('dov-pub:Boringen', objecttype)
