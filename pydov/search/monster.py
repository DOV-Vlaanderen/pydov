# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV monster data."""
from ..types.monster import Monster
from .abstract import AbstractSearch


class MonsterSearch(AbstractSearch):
    """Search class to retrieve information about monsters."""

    def __init__(self, objecttype=Monster):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Monster type.
            Optional: defaults to the Monster type containing the fields
            described in the documentation.

        """
        super(MonsterSearch, self).__init__(
            'monster:monsters', objecttype
                )
