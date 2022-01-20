# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV
bodemdiepteinterval data."""
from ..types.bodemdiepteinterval import Bodemdiepteinterval
from .abstract import AbstractSearch


class BodemdiepteintervalSearch(AbstractSearch):
    """Search class to retrieve information about bodemdiepteintervallen."""

    def __init__(self, objecttype=Bodemdiepteinterval):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Bodemdiepteinterval type.
            Optional: defaults to the Bodemdiepteinterval type containing the
            fields described in the documentation.

        """
        super(BodemdiepteintervalSearch, self).__init__(
            'bodem:bodemdiepteintervallen', objecttype)
