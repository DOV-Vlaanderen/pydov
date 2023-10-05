# -*- coding: utf-8 -*-
"""Module containing generic fields for the location (ligging) of objects."""

import numpy as np

from pydov.types.fields import _CustomXmlField


class MvMtawField(_CustomXmlField):
    """Field for retrieving the mv_mtaw value from the height of the point in
    relevant cases."""

    def __init__(self, definition):
        """Initialise a MvMtawField (mv_mtaw) with given definition.

        Parameters
        ----------
        definition : string
            Type-specific definition of the mv_mtaw field.
        """
        super().__init__(
            name='mv_mtaw',
            definition=definition,
            datatype='float',
            notnull=False
        )

    def calculate(self, cls, tree):
        # Support the old format too
        oorspronkelijk_maaiveld = cls._parse(
            func=tree.findtext,
            xpath='.//oorspronkelijk_maaiveld/waarde',
            namespace=None,
            returntype='float'
        )
        if oorspronkelijk_maaiveld is not np.nan:
            return oorspronkelijk_maaiveld

        # Check if referentiepunt is Maaiveld
        referentiepunt = cls._parse(
            func=tree.findtext,
            xpath='.//ligging/metadata_hoogtebepaling/referentiepunt_type',
            namespace=None,
            returntype='string'
        )
        if referentiepunt != 'Maaiveld':
            # If referentiepunt is not Maaiveld, we don't know the height of
            # maaiveld
            return np.nan

        # If referentiepunt is Maaiveld, height of the ligging is Maaiveld
        point = tree.findtext(
            './/ligging/{http://www.opengis.net/gml/3.2}Point/'
            '{http://www.opengis.net/gml/3.2}pos'
        )
        coords = point.split(' ')
        if len(coords) == 3:
            hoogte = float(coords[-1])
            return hoogte
        else:
            return np.nan
