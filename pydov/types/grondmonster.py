# -*- coding: utf-8 -*-
"""Module containing the DOV data type for grondmonster, including
subtypes."""
from pydov.types.fields import WfsField, XmlField, XsdType

from .abstract import AbstractDovSubType, AbstractDovType


class Korrelverdeling(AbstractDovSubType):

    rootpath = './/grondmonster/observatieReeksData/' \
        'korrelverdeling_reeks/korrelverdeling'

    fields = [
        XmlField(name='diameter',
                 source_xpath='/diameter',
                 definition='.',
                 datatype='float',
                 notnull=False),
        XmlField(name='fractie',
                 source_xpath='/fractie',
                 definition='.',
                 datatype='float',
                 notnull=False),
        XmlField(name='methode',
                 source_xpath='/methode',
                 definition='.',
                 datatype='string',
                 notnull=False)
    ]


class Grondmonster(AbstractDovType):
    """Class representing the DOV data type for ground samples."""

    subtypes = [Korrelverdeling]

    __grondmonsterDataCodesEnumType = XsdType(
        xsd_schema='https://www.dov.vlaanderen.be/xdov/schema/latest/'
                   'xsd/kern/grondmonster/GrondmonsterDataCodes.xsd',
        typename='MonsterEnumType'
    )

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
                 source_xpath='/grondmonster/observatieData/observatie['
                              'parameter="ASTM_NAAM"]/waarde_text',
                 definition='ASTM_naam',
                 datatype='string'),
        XmlField(name='grondsoort_bggg',
                 source_xpath='/grondmonster/observatieData/observatie['
                              'parameter="BGGG"]/waarde_text',
                 definition='Grondsoort BGGG',
                 datatype='string'),
        XmlField(name='humusgehalte',
                 source_xpath='/grondmonster/observatieData/observatie['
                              'parameter="HUMUSGEHALTE"]/waarde_numeriek',
                 definition='Humusgehalte',
                 datatype='float'),
        XmlField(name='kalkgehalte',
                 source_xpath='/grondmonster/observatieData/observatie['
                              'parameter="KALKGEHALTE"]/waarde_numeriek',
                 definition='Kalkgehalte',
                 datatype='float'),
        XmlField(name='uitrolgrens',
                 source_xpath='/grondmonster/observatieData/observatie['
                              'parameter="UITROLGRENS"]/waarde_numeriek',
                 definition='Uitrolgrens',
                 datatype='float'),
        XmlField(name='vloeigrens',
                 source_xpath='/grondmonster/observatieData/observatie['
                              'parameter="VLOEIGRENS"]/waarde_numeriek',
                 definition='Vloeigrens',
                 datatype='float'),
        XmlField(name='glauconiet_totaal',
                 source_xpath='/grondmonster/observatieData/observatie['
                              'parameter="GLAUCONIET_TOTAAL"]/waarde_numeriek',
                 definition='Glauconiet totaal in percent',
                 datatype='float'),
        XmlField(name='korrelvolumemassa',
                 source_xpath='/grondmonster/observatieData/observatie['
                              'parameter="KORRELVOLUMEMASSA"]/waarde_numeriek',
                 definition='',
                 datatype='float'),
        XmlField(name='volumemassa',
                 source_xpath='/grondmonster/observatieData/observatie['
                              'parameter="VOLUMEMASSA"]/waarde_numeriek',
                 definition='',
                 datatype='float'),
        XmlField(name='watergehalte',
                 source_xpath='/grondmonster/observatieData/observatie['
                              'parameter="WATERGEHALTE"]/waarde_numeriek',
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
