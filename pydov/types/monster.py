# -*- coding: utf-8 -*-
"""Module containing the DOV data type for monster, including
subtypes."""
from pydov.types.fields import WfsField, XmlField
from .abstract import AbstractDovSubType, AbstractDovType


class BemonsterdObject(AbstractDovSubType):

    rootpath = './/monster/bemonsterdobject'

    fields = [
        XmlField(name='bemonsterd_object_type',
                 source_xpath='/monster/bemonsterdobject/objecttype',
                 definition='Objecttype',
                 datatype='string'),
        XmlField(name='bemonsterd_object_naam',
                 source_xpath='/monster/bemonsterdobject/naam',
                 definition='DOV naam',
                 datatype='string'),
        XmlField(name='bemonsterd_object_permkey',
                 source_xpath='/monster/bemonsterdobject/permkey',
                 definition='Een unieke DOV identifier '
                            'in de vorm van een permkey.',
                 datatype='string')
    ]


class Monster(AbstractDovType):
    """Class representing the DOV data type for ground samples."""

    def _split_pkey_parents(agg_value):
        """
        Splits the given aggregated value into parent keys.

        Parameters
        ----------
        agg_value : str
            Aggregated value containing parent keys, separated by '|'.

        Returns
        -------
        generator of str
            Generator yielding non-empty parent keys extracted from the input.
        """
        return (pkey for pkey in agg_value.strip(
            '| ').split('|') if pkey != '')


    fields = [
        WfsField(name='pkey_monster',
                 source_field='monster_link',
                 datatype='string'),
        WfsField(name='naam',
                 source_field='monster',
                 datatype='string'),
        WfsField(name='pkey_parents',
                 source_field='gekoppeld_aan_link',
                 datatype='string',
                 split_fn=_split_pkey_parents),
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
