# -*- coding: utf-8 -*-
"""Module containing the DOV data type for grondmonster, including
subtypes."""
from pydov.types.fields import WfsField, XmlField

from .abstract import AbstractDovSubType, AbstractDovType


class KorrelverdelingMeetreeks(AbstractDovSubType):
    """Class representing the values of a Korrelverdeling."""

    rootpath = './/waarde_meetreeks/meetreekswaarde'

    fields = [
        XmlField(name='diameter',
                 source_xpath='/meetpunt_numeriek',
                 definition='Diameter van de korrels',
                 datatype='float',
                 notnull=False),
        XmlField(name='fractie',
                 source_xpath='/meetwaarde_numeriek',
                 definition='Fractie met grotere diameter',
                 datatype='float',
                 notnull=False),
    ]


class Korrelverdeling(AbstractDovSubType):
    """Class representing the Korrelverdelingen."""

    rootpath = (".//observatie[starts-with(parametergroep, "
                "'Onderkenningsproeven-korrelverdeling')]")

    subtypes = [KorrelverdelingMeetreeks]

    fields = [
        XmlField(name='methode',
                 source_xpath='/parameter',
                 definition=('Gebruikte methode om de korrelverdeling'
                             ' te bepalen'),
                 datatype='string',
                 notnull=False)
    ]


class Grondmonster(AbstractDovType):
    """Class representing the DOV data type for ground samples."""

    subtypes = [Korrelverdeling]

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
        WfsField(name='pkey_grondmonster',
                 source_field='monster_link',
                 datatype='string'),
        WfsField(name='naam',
                 source_field='monster',
                 datatype='string'),
        WfsField(name='pkey_parents',
                 source_field='gekoppeld_aan_link',
                 datatype='string',
                 split_fn=_split_pkey_parents),
        WfsField(name='datum',
                 source_field='bemonsteringsdatum',
                 datatype='date',),
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
        XmlField(name='astm_naam',
                 source_xpath='/observatie[parameter="ASTM_naam"]/waarde_text',
                 definition='ASTM_naam',
                 datatype='string'),
        XmlField(name='grondsoort_bggg',
                 source_xpath=('/observatie[parameter="Grondsoort '
                               'BGGG"]/waarde_text'),
                 definition='Grondsoort BGGG',
                 datatype='string'),
        XmlField(name='humusgehalte',
                 source_xpath=('/observatie[parameter="Gehalte Organische '
                               'stoffen"]/waarde_numeriek'),
                 definition='Humusgehalte',
                 datatype='float'),
        XmlField(name='kalkgehalte',
                 source_xpath=('/observatie[parameter="Gehalte Kalkachtige '
                               'stoffen"]/waarde_numeriek'),
                 definition='Kalkgehalte',
                 datatype='float'),
        XmlField(name='uitrolgrens',
                 source_xpath=('/observatie[parameter="Consistentiegrenzen - '
                               'Uitrolgrens"]/waarde_numeriek'),
                 definition='Uitrolgrens',
                 datatype='float'),
        XmlField(name='vloeigrens',
                 source_xpath=('/observatie[parameter="Consistentiegrenzen - '
                               'Vloeigrens"]/waarde_numeriek'),
                 definition='Vloeigrens',
                 datatype='float'),
        XmlField(name='glauconiet_totaal',
                 source_xpath=('/observatie[parameter="Glauconiet totaal"]/'
                               'waarde_numeriek'),
                 definition='Glauconiet totaal in percent',
                 datatype='float'),
        XmlField(name='korrelvolumemassa',
                 source_xpath=('observatie[parameter="korrelvolumemassa"]/'
                               'waarde_numeriek'),
                 definition='',
                 datatype='float'),
        XmlField(name='volumemassa',
                 source_xpath=('/observatie[parameter="volumemassa nat"]/'
                               'waarde_numeriek'),
                 definition='',
                 datatype='float'),
        XmlField(name='watergehalte',
                 source_xpath=('/observatie[parameter="watergehalte"]/'
                               'waarde_numeriek'),
                 definition='',
                 datatype='float')
    ]

    pkey_fieldname = 'monster_link'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Grondmonster, being a URI of the form
            `https://www.dov.vlaanderen.be/data/monster/<id>`.

        """
        super().__init__('monster', pkey)
