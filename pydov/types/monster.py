# -*- coding: utf-8 -*-
"""Module containing the DOV data type for monster, including
subtypes."""
import datetime
import numpy as np
from pydov.types.fields import _CustomXmlField, WfsField

from .abstract import AbstractDovFieldSet, AbstractDovType


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


class TijdstipMonsternameField(_CustomXmlField):
    """Field for retrieving the time of the sampling from the relevant XML
    field."""

    def __init__(self):
        super().__init__(
            name='tijdstip_monstername',
            definition=("Tijdstip waarop het monster werd verkregen uit het "
                        "bemonsterdObject."),
            datatype='string',
            notnull=False
        )

    def calculate(self, cls, tree):
        tijdstip = cls._parse(
            func=tree.findtext,
            xpath='.//bemonsteringstijdstip/tijdstip',
            namespace=None,
            returntype='string'
        )
        if tijdstip is not np.nan:
            return tijdstip

        datumtijd = cls._parse(
            func=tree.findtext,
            xpath='.//bemonsteringstijdstip/datumtijd',
            namespace=None,
            returntype='string'
        )
        if datumtijd is not np.nan:
            timestamp = datetime.datetime.fromisoformat(datumtijd)
            return timestamp.strftime('%H:%M:%S')

        return np.nan


class MonsterDetails(AbstractDovFieldSet):
    """Fieldset containing fields with extra details about the sample."""

    intended_for = ['Monster']

    fields = [
        TijdstipMonsternameField()
    ]
