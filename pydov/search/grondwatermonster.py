# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV groundwater samples."""
from ..types.grondwatermonster import GrondwaterMonster
from .abstract import AbstractSearch


class GrondwaterMonsterSearch(AbstractSearch):
    """Search class to retrieve information about groundwater samples
    (GrondwaterMonster).
    """

    def __init__(self, objecttype=GrondwaterMonster):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the GrondwaterFilter type.
            Optional: defaults to the GrondwaterFilter type containing the
            fields described in the documentation.

        """
        super(GrondwaterMonsterSearch,
              self).__init__('gw_meetnetten:grondwatermonsters', objecttype)
