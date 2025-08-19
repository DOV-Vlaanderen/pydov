# -*- coding: utf-8 -*-
"""Module containing the DOV data type for observations (Observatie), including
subtypes."""
from pydov.types.fields import WfsField, XmlField
from pydov.types.fields_custom import OsloCodeListValueField

from .abstract import AbstractDovSubType, AbstractDovFieldSet


class ObservatieDetails(AbstractDovFieldSet):
    """Fieldset containing fields with extra details about the observation."""

    intended_for = ['Observatie']

    fields = [
        OsloCodeListValueField(name='betrouwbaarheid',
                               source_xpath='.//betrouwbaarheid',
                               conceptscheme='betrouwbaarheid',
                               definition='Betrouwbaarheid van de observatie',
                               datatype='string'),
        XmlField(name='geobserveerd_object_type',
                 source_xpath='.//geobserveerd_object/objecttype',
                 definition='Objecttype van het geobserveerd object',
                 datatype='string'),
        XmlField(name='geobserveerd_object_naam',
                 source_xpath='.//geobserveerd_object/naam',
                 definition='DOV naam van het geobserveerd object',
                 datatype='string'),
        XmlField(name='geobserveerd_object_permkey',
                 source_xpath='.//geobserveerd_object/permkey',
                 definition='Een unieke DOV identifier '
                            'in de vorm van een permkey.',
                 datatype='string')
    ]


class ObservatieHerhaling(AbstractDovSubType):
    """Subtype showing the repetition information of an observation."""

    rootpath = './/observatie/herhaling'
    intended_for = ['Observatie']

    fields = [
        XmlField(name='herhaling_aantal',
                 source_xpath='/aantal',
                 definition='Aantal herhalingen',
                 datatype='integer'),
        XmlField(name='herhaling_minimum',
                 source_xpath='/minimum',
                 definition='Minimum waarde',
                 datatype='float'),
        XmlField(name='herhaling_maximum',
                 source_xpath='/maximum',
                 definition='Maximum waarde',
                 datatype='float'),
        XmlField(name='herhaling_standaardafwijking',
                 source_xpath='/standaardafwijking',
                 definition='Standaardafwijking metingen',
                 datatype='float')
    ]
from pydov.types.fields import WfsField, XmlField, _CustomXmlField
from .abstract import AbstractDovType, AbstractDovSubType
import numpy as np


class ObservatieSecParResultField(_CustomXmlField):
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
        waarde_num = cls._parse(
            func=tree.findtext,
            xpath='/waarde_numeriek',
            namespace=None,
            returntype='string'
        )
        if waarde_num is not np.nan and waarde_num != '':
            return waarde_num
        waarde_text = cls._parse(
            func=tree.findtext,
            xpath='/waarde_text',
            namespace=None,
            returntype='string'
        )
        if waarde_text is not np.nan and waarde_text != '':
            return waarde_text
        else:
            return np.nan


class SecundaireParameter(AbstractDovSubType):
    """Subtype showing the secondary parameter of an observation."""

    rootpath = './/observatie/secundaireparameter'
    intended_for = ['Observatie']

    fields = [
        XmlField(name='secundaireparameter_parameter',
                 source_xpath='/parameter',
                 definition='Secundaire parameter',
                 datatype='string'),
        ObservatieSecParResultField(name='secundaireparameter_resultaat',
                                    definition="Resultaat van de "
                                               "secudaire parameter"),
        XmlField(name='secundaireparameter_eenheid',
                 source_xpath='/eenheid',
                 definition='Eenheid',
                 datatype='string')
    ]


class Observatie(AbstractDovType):
    """Class representing the DOV data type for observations."""

    fields = [
        WfsField(name='pkey_observatie', source_field='observatie_link',
                 datatype='string'),
        WfsField(name='pkey_parent', source_field='gekoppeld_aan_link',
                 datatype='string'),
        WfsField(name='fenomeentijd', source_field='fenomeentijd',
                 datatype='date'),
        WfsField(name='diepte_van_m', source_field='diepte_van_m',
                 datatype='float'),
        WfsField(name='diepte_tot_m', source_field='diepte_tot_m',
                 datatype='float'),
        WfsField(name='parametergroep', source_field='parametergroep',
                 datatype='string'),
        WfsField(name='parameter', source_field='parameter',
                 datatype='string'),
        WfsField(name='detectieconditie', source_field='detectieconditie',
                 datatype='string'),
        WfsField(name='resultaat', source_field='resultaat',
                 datatype='string'),
        WfsField(name='eenheid', source_field='eenheid',
                 datatype='string'),
        WfsField(name='methode', source_field='methode',
                 datatype='string'),
        WfsField(name='uitvoerder', source_field='uitvoerder',
                 datatype='string'),
        WfsField(name='herkomst', source_field='herkomst',
                 datatype='string')
    ]

    pkey_fieldname = 'observatie_link'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Observatie (observation),
             being a URI of the form
            `https://www.dov.vlaanderen.be/data/observatie/<id>`.

        """
        super().__init__('observatie', pkey)
