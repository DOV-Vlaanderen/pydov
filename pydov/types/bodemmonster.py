# -*- coding: utf-8 -*-
"""Module containing the DOV data type for bodemmonsters, including
subtypes."""
from pydov.types.fields import WfsField, XmlField

from .abstract import AbstractDovType


class Bodemmonster(AbstractDovType):
    """Class representing the DOV data type for bodemmonsters."""

    subtypes = []

    fields = [
        WfsField(name='pkey_bodemmonster', source_field='Bodemmonsterfiche',
                 datatype='string'),
        WfsField(name='pkey_bodemlocatie',
                 source_field='Bodemlocatiefiche',
                 datatype='string'),
        WfsField(name='pkey_parent',
                 source_field='Parentfiche',
                 datatype='string'),
        WfsField(name='x', source_field='X_mL72', datatype='float'),
        WfsField(name='y', source_field='Y_mL72', datatype='float'),
        WfsField(name='mv_mtaw', source_field='mv_mTAW', datatype='float'),
        WfsField(name='identificatie', source_field='Bodemmonster',
                 datatype='string'),
        WfsField(name='datum_monstername', source_field='Datum_monsterafname',
                 datatype='date'),
        XmlField(name='tijdstip_monstername',
                 source_xpath='/bodemmonster/tijdstip_monstername',
                 definition='Tijdstip waarop het monster werd genomen.',
                 datatype='string'),
        WfsField(name='type', source_field='Type', datatype='string'),
        WfsField(name='monstername_door', source_field='Monsterafname_door',
                 datatype='string'),
        WfsField(name='techniek', source_field='Techniek_monsterafname',
                 datatype='string'),
        WfsField(name='condities', source_field='Condities_monsterafname',
                 datatype='string'),
        WfsField(name='diepte_van_cm', source_field='Diepte_van',
                 datatype='float'),
        WfsField(name='diepte_tot_cm', source_field='Diepte_tot',
                 datatype='float'),
        WfsField(name='labo', source_field='Labo', datatype='string')
    ]

    pkey_fieldname = 'Bodemmonsterfiche'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Bodemmonster, being a URI of the form
            `https://www.dov.vlaanderen.be/data/bodemmonster/<id>`.

        """
        super().__init__('bodemmonster', pkey)
