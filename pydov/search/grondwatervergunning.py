# -*- coding: utf-8 -*-
"""Module containing the search classes to retrieve permit data."""
import pandas as pd

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

    def search(self, location=None, query=None, sort_by=None,
               return_fields=None, max_features=None):
        fts = self._search(location=location, query=query, sort_by=sort_by,
                           return_fields=return_fields,
                           max_features=max_features)

        gw_vergunningen = self._type.from_wfs(fts, self._wfs_namespace)

        df = pd.DataFrame(
            data=self._type.to_df_array(gw_vergunningen, return_fields),
            columns=self._type.get_field_names(return_fields))
        return df
