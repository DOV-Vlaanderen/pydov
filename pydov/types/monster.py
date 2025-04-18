# -*- coding: utf-8 -*-
"""Module containing the DOV data type for monster, including
subtypes."""
from pydov.types.fields import WfsField, XmlField

from .abstract import AbstractDovSubType, AbstractDovType

class Monster(AbstractDovType):
    """Class representing the DOV data type for ground samples."""

    fields = [
        WfsField(name='pkey_monster',
                 source_field='monster_link',
                 datatype='string'),
        WfsField(name='naam',
                 source_field='monster',
                 datatype='string'),
        WfsField(name='pkey_parents',
                 source_field='gekoppeld_aan_link',
                 datatype='string'),
        WfsField(name='materiaalklasse',
                 source_field='materiaalklasse',
                 datatype='string'),
        WfsField(name='datum_monstername',
                 source_field='bemonsteringsdatum',
                 datatype='date'),
        WfsField(name='diepte_van_m',
                 source_field='diepte_van_m',
                 datatype='float'),
        WfsField(name='diepte_tot_m',
                 source_field='diepte_tot_m',
                 datatype='float'),
        WfsField(name='monstertype',
                 source_field='monstertype',
                 datatype='string'),
        WfsField(name='monstersamenstelling',
                 source_field='monstersamenstelling',
                 datatype='string'),
        WfsField(name='bemonsteringsprocedure',
                 source_field='bemonsteringsprocedure',
                 datatype='string'),
        WfsField(name='bemonsteringsinstrument',
                 source_field='bemonsteringsinstrument',
                 datatype='string'),
        WfsField(name='bemonstering_door',
                 source_field='bemonstering_door',
                 datatype='string')

    ]

    pkey_fieldname = 'monster_link'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Monster, being a URI of the form
            `https://www.dov.vlaanderen.be/data/monster/<id>`.

        """
        super().__init__('monster', pkey)
