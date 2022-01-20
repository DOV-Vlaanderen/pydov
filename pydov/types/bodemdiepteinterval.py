# -*- coding: utf-8 -*-
"""Module containing the DOV data type for bodemdiepteintervallen, including
subtypes."""
from pydov.types.fields import WfsField

from .abstract import AbstractDovType


class Bodemdiepteinterval(AbstractDovType):
    """Class representing the DOV data type for bodemdiepteinterval."""

    subtypes = []

    fields = [
        WfsField(name='nr',
                 source_field='Nr',
                 datatype='float'),
        WfsField(name='type',
                 source_field='Type',
                 datatype='string'),
        WfsField(name='pkey_diepteinterval',
                 source_field='Diepteintervalfiche',
                 datatype='string'),
        WfsField(name='pkey_bodemopbouw',
                 source_field='Bodemopbouwfiche',
                 datatype='string'),
        WfsField(name='pkey_bodemlocatie',
                 source_field='Bodemlocatiefiche',
                 datatype='string'),
        WfsField(name='naam',
                 source_field='Naam',
                 datatype='string'),
        WfsField(name='bovengrens1',
                 source_field='Bovengrens1',
                 datatype='float'),
        WfsField(name='bovengrens2',
                 source_field='Bovengrens2',
                 datatype='float'),
        WfsField(name='ondergrens1',
                 source_field='Ondergrens1',
                 datatype='float'),
        WfsField(name='ondergrens2',
                 source_field='Ondergrens2',
                 datatype='float'),
        WfsField(name='ondergrens_bereikt',
                 source_field='Ondergrens_bereikt',
                 datatype='string'),
        WfsField(name='grensduidelijkheid',
                 source_field='Grensduidelijkheid',
                 datatype='string'),
        WfsField(name='grensregelmatigheid',
                 source_field='Grensregelmatigheid',
                 datatype='string'),
        WfsField(name='beschrijving',
                 source_field='Beschrijving',
                 datatype='string'),
        WfsField(name='x',
                 source_field='X_mL72',
                 datatype='float'),
        WfsField(name='y',
                 source_field='Y_mL72',
                 datatype='float'),
        WfsField(name='mv_mtaw',
                 source_field='mv_mTAW',
                 datatype='float'),
    ]

    pkey_fieldname = 'Diepteintervalfiche'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Bodemdiepteinterval, being a URI of the form
            `https://www.dov.vlaanderen.be/data/bodemdiepteinterval/<id>`.

        """
        super().__init__('bodemdiepteinterval', pkey)
