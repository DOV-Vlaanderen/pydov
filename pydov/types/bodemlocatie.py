# -*- coding: utf-8 -*-
"""Module containing the DOV data type for bodemlocaties, including
subtypes."""
from pydov.types.fields import WfsField, XmlField

from .abstract import AbstractDovType


class Bodemlocatie(AbstractDovType):
    """Class representing the DOV data type for bodemlocaties."""

    subtypes = []

    fields = [
        WfsField(name='pkey_bodemlocatie', source_field='Bodemlocatiefiche',
                 datatype='string'),
        WfsField(name='pkey_bodemsite', source_field='Bodemsitefiche',
                 datatype='string'),
        WfsField(name='naam', source_field='Naam', datatype='string'),
        WfsField(name='type', source_field='Type', datatype='string'),
        WfsField(name='waarnemingsdatum', source_field='Datum',
                 datatype='date'),
        WfsField(name='doel', source_field='Doel', datatype='string'),
        WfsField(name='x', source_field='X_mL72', datatype='float'),
        WfsField(name='y', source_field='Y_mL72', datatype='float'),
        WfsField(name='mv_mtaw', source_field='mv_mTAW', datatype='float'),
        WfsField(name='erfgoed', source_field='Erfgoed', datatype='boolean'),
        WfsField(name='bodemstreek', source_field='Bodemstreek',
                 datatype='string'),
        XmlField(name='invoerdatum',
                 source_xpath='/bodemlocatie/invoerdatum',
                 definition='Datum van invoer van de bodemlocatie.',
                 datatype='date'),
        XmlField(name='educatieve_waarde',
                 source_xpath='/bodemlocatie/educatieve_waarde',
                 definition='Educatieve waarde van de bodemlocatie.',
                 datatype='string')
    ]

    pkey_fieldname = 'Bodemlocatiefiche'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Bodemlocatie, being a URI of the form
            `https://www.dov.vlaanderen.be/data/bodemlocatie/<id>`.

        """
        super().__init__('bodemlocatie', pkey)
