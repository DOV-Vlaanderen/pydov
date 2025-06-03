# -*- coding: utf-8 -*-
"""Module containing the DOV data type for monster, including
subtypes."""
from pydov.types.fields import WfsField, XmlField, _CustomXmlField
from .abstract import AbstractDovSubType, AbstractDovType, AbstractDovFieldSet

import datetime
import numpy as np


class TijdstipField(_CustomXmlField):
    """Retrieves the time from the relevant XML field.

    Returns
    -------
    str
        Timestamp in the format '%H:%M:%S'. Returns the value of the 'tijdstip'
        field from the XML. If 'tijdstip' is null, returns the time part of
        the 'datumtijd' field.
    """

    def __init__(self, name, definition, base_xpath):
        super().__init__(
            name=name,
            definition=definition,
            datatype='string',
            notnull=False
        )
        self.base_xpath = base_xpath

    def calculate(self, cls, tree):
        tijdstip = cls._parse(
            func=tree.findtext,
            xpath=self.base_xpath + 'tijdstip',
            namespace=None,
            returntype='string'
        )
        if tijdstip is not np.nan:
            return tijdstip

        datumtijd = cls._parse(
            func=tree.findtext,
            xpath=self.base_xpath + 'datumtijd',
            namespace=None,
            returntype='string'
        )
        if datumtijd is not np.nan:
            timestamp = datetime.datetime.fromisoformat(datumtijd)
            return timestamp.strftime('%H:%M:%S')

        return np.nan


class DatumField(_CustomXmlField):
    """Retrieves the date from the relevant XML field.

    Returns
    -------
    str
        Date in the format '%Y-%m-%d'. Returns the value of the 'datum' field
        from the XML. If 'datum' is null, returns the value of the
        'datumtijd' field.
    """

    def __init__(self, name, definition, base_xpath):
        super().__init__(
            name=name,
            definition=definition,
            datatype='string',
            notnull=False
        )
        self.base_xpath = base_xpath

    def calculate(self, cls, tree):
        date = cls._parse(
            func=tree.findtext,
            xpath=self.base_xpath + 'datum',
            namespace=None,
            returntype='string'
        )
        if date is not np.nan:
            return date

        date = cls._parse(
            func=tree.findtext,
            xpath=self.base_xpath + 'datumtijd',
            namespace=None,
            returntype='string'
        )
        if date is not np.nan:
            date = datetime.datetime.fromisoformat(date)
            return date.strftime('%Y-%m-%d')

        return np.nan


class MonsterBehandelingField(_CustomXmlField):
    """Field for retrieving the treatment of the sampling from the relevant XML
    field."""

    def __init__(self, name, definition):
        super().__init__(
            name=name,
            definition=definition,
            datatype='string',
            notnull=False
        )

    def calculate(self, cls, tree):
        behandeling = cls._parse(
            func=tree.findtext,
            xpath='.//verwerkingsdetails/behandeling',
            namespace=None,
            returntype='string'
        )
        if behandeling is not np.nan:
            return behandeling

        monstervoorbereiding = cls._parse(
            func=tree.findtext,
            xpath='.//verwerkingsdetails/monstervoorbereiding',
            namespace=None,
            returntype='string'
        )
        if monstervoorbereiding is not np.nan:
            return monstervoorbereiding

        return np.nan


class MonsterDetails(AbstractDovFieldSet):
    """Fieldset containing fields with extra
    details about the sample.
    """

    intended_for = ['Monster']

    fields = [
        TijdstipField(name='tijdstip_monstername',
                      definition="Tijdstip waarop het monster werd "
                                 "verkregen uit het bemonsterdObject.",
                      base_xpath='.//bemonsteringstijdstip/')
    ]


class BemonsterdObject(AbstractDovSubType):
    """Subtype listing the sampled object(s) of the sample."""

    rootpath = './/monster/bemonsterdObject'
    intended_for = ['Monster']

    fields = [
        XmlField(name='bemonsterd_object_type',
                 source_xpath='/objecttype',
                 definition='Objecttype',
                 datatype='string'),
        XmlField(name='bemonsterd_object_naam',
                 source_xpath='/naam',
                 definition='DOV naam',
                 datatype='string'),
        XmlField(name='bemonsterd_object_permkey',
                 source_xpath='/permkey',
                 definition='Een unieke DOV identifier '
                            'in de vorm van een permkey.',
                 datatype='string')
    ]


class Monsterbehandeling(AbstractDovSubType):
    """Subtype containing fields about the
    treatment of the sample."""

    intended_for = ['Monster']
    rootpath = './/monster/verwerkingsdetails'

    fields = [
        XmlField(name='monsterbehandeling_door',
                 source_xpath='procesoperator',
                 definition=("Operator die het monster behandeld heeft"),
                 datatype='string'),
        DatumField(name='monsterbehandeling_datum',
                   base_xpath='.//verwerkingsdetails/tijdstip/',
                   definition="Datum waarop het monster behandeld werd."),
        TijdstipField(name='monsterbehandeling_tijdstip',
                      definition="Tijdstip waarop het monster behandeld werd.",
                      base_xpath='.//verwerkingsdetails/tijdstip/'),
        MonsterBehandelingField(name='monsterbehandeling_behandeling',
                                definition="De behandeling of voorbereiding "
                                           "van het monster"),
        XmlField(name='monsterbehandeling_behandeling_waarde',
                 source_xpath='behandeling',
                 definition=("De behandeling van het monster"),
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
