# -*- coding: utf-8 -*-
"""Module containing the DOV data type for groundwater samples
(GrondwaterMonsters), including subtypes."""
from pydov.types.fields import WfsField, XmlField, XsdType
from pydov.util.dovutil import build_dov_url

from .abstract import AbstractDovSubType, AbstractDovType

_observatieDataCodes_xsd = build_dov_url(
    'xdov/schema/latest/xsd/kern/observatie/ObservatieDataCodes.xsd')


class Observatie(AbstractDovSubType):

    rootpath = './/filtermeting/watermonster/observatie'

    fields = [
        XmlField(name='parametergroep',
                 source_xpath='/parametergroep',
                 definition='Parametergroep',
                 datatype='string'),
        XmlField(name='parameter',
                 source_xpath='/parameter',
                 definition='Parameter',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=_observatieDataCodes_xsd,
                     typename='ParameterEnumType')),
        XmlField(name='detectie',
                 source_xpath='/detectieconditie',
                 definition='boven/onder detectielimiet',
                 datatype='string'),
        XmlField(name='waarde',
                 source_xpath='/waarde_numeriek',
                 definition='waarde (numeriek) van de parameter',
                 datatype='float'),
        XmlField(name='eenheid',
                 source_xpath='/eenheid',
                 definition='Eenheid',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=_observatieDataCodes_xsd,
                     typename='MeeteenheidEnumType')),
        XmlField(name='veld_labo',
                 source_xpath='/veld_labo',
                 definition='observatie in het LABO of op het VELD',
                 datatype='string'),
    ]


class GrondwaterMonster(AbstractDovType):
    """Class representing the DOV data type for Groundwater samples."""

    subtypes = [Observatie]

    fields = [
        WfsField(name='pkey_grondwatermonster',
                 source_field='grondwatermonsterfiche',
                 datatype='string'),
        WfsField(name='grondwatermonsternummer',
                 source_field='grondwatermonsternummer',
                 datatype='string'),
        WfsField(name='pkey_grondwaterlocatie',
                 source_field='grondwaterlocatiefiche',
                 datatype='string'),
        WfsField(name='gw_id', source_field='GW_ID', datatype='string'),
        WfsField(name='pkey_filter', source_field='filterfiche',
                 datatype='string'),
        WfsField(name='filternummer', source_field='filternr',
                 datatype='string'),
        WfsField(name='x', source_field='X_mL72', datatype='float'),
        WfsField(name='y', source_field='Y_mL72', datatype='float'),
        WfsField(name='start_grondwaterlocatie_mtaw', source_field='Z_mTAW',
                 datatype='float'),
        WfsField(name='gemeente', source_field='gemeente', datatype='string'),
        WfsField(name='datum_monstername', source_field='datum_monstername',
                 datatype='date'),
    ]

    pkey_fieldname = 'grondwatermonsterfiche'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the GrondwaterMonster (groundwater sample), being
            a URI of the form
            `https://www.dov.vlaanderen.be/data/watermonster/<id>`.

        """
        super().__init__('watermonster', pkey)
