# -*- coding: utf-8 -*-
"""Module containing the DOV data type for bodemobservaties, including
subtypes."""
from pydov.types.fields import WfsField, XmlField

from .abstract import AbstractDovSubType, AbstractDovType


class Fractiemeting(AbstractDovSubType):
    rootpath = './/bodemobservatie/fractiemeting'

    fields = [
        XmlField(name='fractiemeting_ondergrens',
                 source_xpath='ondergrens',
                 definition='ondergrens van de fractiemeting in µm',
                 datatype='float',
                 notnull=False),
        XmlField(name='fractiemeting_bovengrens',
                 source_xpath='bovengrens',
                 definition='bovengrens van de fractiemeting in µm',
                 datatype='float',
                 notnull=False),
        XmlField(name='fractiemeting_waarde',
                 source_xpath='waarde',
                 definition='gemeten massaprocent van de fractie',
                 datatype='float',
                 notnull=False)
    ]


class Bodemobservatie(AbstractDovType):
    """Class representing the DOV data type for bodemobservaties."""

    subtypes = [Fractiemeting]

    fields = [
        WfsField(name='pkey_bodemobservatie',
                 source_field='Bodemobservatiefiche',
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
        WfsField(name='diepte_van_cm', source_field='Diepte_van',
                 datatype='float'),
        WfsField(name='diepte_tot_cm', source_field='Diepte_tot',
                 datatype='float'),
        XmlField(name='observatiedatum',
                 source_xpath='/bodemobservatie/observatiedatum',
                 definition='Observatiedatum van de bodemobservatie',
                 datatype='date'),
        XmlField(name='invoerdatum',
                 source_xpath='/bodemobservatie/invoerdatum',
                 definition='Invoerdatum van de bodemobservatie.',
                 datatype='date'),
        XmlField(name='parametergroep',
                 source_xpath='/bodemobservatie/parametergroep',
                 definition='Indeling van de parameter naar groep, '
                 + 'bvb anionen, kationen, .... Is indicatief.',
                 datatype='string'),
        WfsField(name='parameter', source_field='Parameter',
                 datatype='string'),
        XmlField(name='detectie',
                 source_xpath='/bodemobservatie/detectieconditie',
                 definition='boven/onder detectielimiet',
                 datatype='string'),
        WfsField(name='waarde', source_field='Waarde', datatype='string'),
        WfsField(name='eenheid', source_field='Eenheid', datatype='string'),
        WfsField(name='veld_labo', source_field='Labo_of_veld',
                 datatype='string'),
        WfsField(name='methode', source_field='Observatiemethode',
                 datatype='string'),
        XmlField(name='betrouwbaarheid',
                 source_xpath='/bodemobservatie/betrouwbaarheid',
                 definition='Betrouwbaarheid van de meting.',
                 datatype='string')
    ]

    pkey_fieldname = 'Bodemobservatiefiche'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Bodemobservatie, being a URI of the form
            `https://www.dov.vlaanderen.be/data/bodemobservatie/<id>`.

        """
        super().__init__('bodemobservatie', pkey)
