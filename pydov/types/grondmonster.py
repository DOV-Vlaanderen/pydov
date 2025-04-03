# -*- coding: utf-8 -*-
"""Module containing the DOV data type for grondmonster, including
subtypes."""
from pydov.types.fields import WfsField, XmlField

from .abstract import AbstractDovSubType, AbstractDovType, AbstractDovFieldSet


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

    fields = [
        WfsField(name='pkey_grondmonster',
                 source_field='grondmonsterfiche',
                 datatype='string'),
        WfsField(name='naam',
                 source_field='naam',
                 datatype='string'),
        WfsField(name='pkey_boring',
                 source_field='boringfiche',
                 datatype='string'),
        WfsField(name='boornummer',
                 source_field='boornummer',
                 datatype='string'),
        XmlField(name='datum',
                 source_xpath='/grondmonster/datum_monstername',
                 datatype='date',),
        WfsField(name='x',
                 source_field='X_mL72',
                 datatype='float'),
        WfsField(name='y',
                 source_field='Y_mL72',
                 datatype='float'),
        WfsField(name='gemeente',
                 source_field='gemeente',
                 datatype='string'),
        WfsField(name='diepte_van_m',
                 source_field='diepte_van_m',
                 datatype='float'),
        WfsField(name='diepte_tot_m',
                 source_field='diepte_tot_m',
                 datatype='float'),
        WfsField(name='peil_van_mtaw',
                 source_field='peil_van_mTAW',
                 datatype='float'),
        WfsField(name='peil_tot_mtaw',
                 source_field='peil_tot_mTAW',
                 datatype='float'),
        WfsField(name='monstertype',
                 source_field='monstertype',
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

    pkey_fieldname = 'grondmonsterfiche'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Grondmonster, being a URI of the form
            `https://www.dov.vlaanderen.be/data/grondmonster/<id>`.

        """
        super().__init__('grondmonster', pkey)


class GlauconietWaarden(AbstractDovFieldSet):
    """Fieldset containing all the different glauconite values."""

    intended_for = Grondmonster

    fields = [
        XmlField(name='glauconiet_gt500',
                 source_xpath='/grondmonster/observatieData/observatie['
                 'parameter="GLAUCONIET_GT500"]/'
                              'waarde_numeriek',
                 definition='Glauconiet fractie groter 500 micron (%)',
                 datatype='float'),
        XmlField(name='glauconiet_tss',
                 source_xpath='/grondmonster/observatieData/observatie['
                 'parameter="GLAUCONIET_TSS"]/'
                              'waarde_numeriek',
                 definition='Glauconiet fractie kleiner 500micron en '
                 'groter 63micron (%)',
                 datatype='float'),
        XmlField(name='glauconiet_kl63',
                 source_xpath='/grondmonster/observatieData/observatie['
                 'parameter="GLAUCONIET_KL63"]/'
                              'waarde_numeriek',
                 definition='Glauconiet fractie kleiner 63micron (%)',
                 datatype='float')
    ]
