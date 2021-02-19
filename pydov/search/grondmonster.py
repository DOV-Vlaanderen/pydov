# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV borehole data."""
from pydov.search.abstract import AbstractSearch
from pydov.types.grondmonster import Grondmonster


class GrondmonsterSearch(AbstractSearch):
    """Search class to retrieve the grain size distribution of
    ground samples ('grondmonster')"""

    def __init__(self, objecttype=Grondmonster):
        """Initialisation.

        Parameters
        ----------
        objecttype : subclass of pydov.types.abstract.AbstractDovType
            Reference to a class representing the Grondmonster type.
            Optional: defaults to the Grondmonster type containing the fields
            described in the documentation.

        """
        super(GrondmonsterSearch, self).\
            __init__('boringen:grondmonsters', objecttype)
