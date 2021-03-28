# -*- coding: utf-8 -*-
"""Module containing the DOV data type for bodemsites, including
subtypes."""
from pydov.types.fields import WfsField, XmlField

from .abstract import AbstractDovType


class Bodemsite(AbstractDovType):
    """Class representing the DOV data type for bodemsites."""

    subtypes = []

    fields = [
        WfsField(name='pkey_bodemsite', source_field='Bodemsitefiche',
                 datatype='string'),
        WfsField(name='naam', source_field='Naam', datatype='string'),
        WfsField(name='waarnemingsdatum', source_field='Datum',
                 datatype='date'),
        WfsField(name='beschrijving', source_field='Beschrijving',
                 datatype='string'),
        XmlField(name='invoerdatum',
                 source_xpath='/bodemsite/invoerdatum',
                 definition='Datum van invoer van de bodemsite.',
                 datatype='date')
    ]

    pkey_fieldname = 'Bodemsitefiche'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Bodemsite, being a URI of the form
            `https://www.dov.vlaanderen.be/data/bodemsite/<id>`.

        """
        super().__init__('bodemsite', pkey)
