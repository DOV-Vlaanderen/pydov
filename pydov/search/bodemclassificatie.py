# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV bodemclassificatie
data."""
from ..types.bodemclassificatie import Bodemclassificatie
from .abstract import AbstractSearch


class BodemclassificatieSearch(AbstractSearch):
    """Search class to retrieve information about bodemclassificaties."""

    def __init__(self, objecttype=Bodemclassificatie):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Bodemclassificatie type.
            Optional: defaults to the Bodemclassificatie type containing the
            fields described in the documentation.

        """
        super(BodemclassificatieSearch, self).__init__(
            'bodem:bodemclassificaties', objecttype)
