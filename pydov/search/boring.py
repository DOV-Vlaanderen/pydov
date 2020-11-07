# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve DOV borehole data."""
import pandas as pd

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

    def search(self, location=None, query=None,
               sort_by=None, return_fields=None, max_features=None):
        fts = self._search(location=location, query=query, sort_by=sort_by,
                           return_fields=return_fields,
                           max_features=max_features)

        boringen = self._type.from_wfs(fts, self._wfs_namespace)

        df = pd.DataFrame(
            data=self._type.to_df_array(boringen, return_fields),
            columns=self._type.get_field_names(return_fields))
        return df
