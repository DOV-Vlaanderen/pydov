# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve permit data."""
from pydov.search.abstract import AbstractSearch
from pydov.types.grondwatervergunning import GrondwaterVergunning


class GrondwaterVergunningSearch(AbstractSearch):
    """Search class to retrieve information about Gw permits (
    all permits: current and historical)."""

    def __init__(self, objecttype=GrondwaterVergunning):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the GrondwaterVergunning type.
            Optional: defaults to the GrondwaterVergunning type containing
            the fields described in the documentation.

        """
        super(GrondwaterVergunningSearch, self).__init__(
            'gw_vergunningen:alle_verg', objecttype)
