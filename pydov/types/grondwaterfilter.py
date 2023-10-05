# -*- coding: utf-8 -*-
"""Module containing the DOV data type for screens (Filter), including
subtypes."""
from pydov.types.fields import WfsField, XmlField, XsdType
from pydov.types.ligging import MvMtawField
from pydov.util.dovutil import build_dov_url

from .abstract import AbstractDovSubType, AbstractDovType

_filterDataCodes_xsd = build_dov_url(
    'xdov/schema/latest/xsd/kern/gwmeetnet/FilterDataCodes.xsd')


class Peilmeting(AbstractDovSubType):

    rootpath = './/filtermeting/peilmeting'

    fields = [
        XmlField(name='datum',
                 source_xpath='/datum',
                 definition='Datum waarop de peilmeting uitgevoerd werd.',
                 datatype='date'),
        XmlField(name='tijdstip',
                 source_xpath='/tijdstip',
                 definition='Tijdstip waarop de peilmeting uitgevoerd werd ('
                            'optioneel).',
                 datatype='string'),
        XmlField(name='peil_mtaw',
                 source_xpath='/peil_mtaw',
                 definition='Diepte van de peilmeting, uitgedrukt in mTAW.',
                 datatype='float'),
        XmlField(name='betrouwbaarheid',
                 source_xpath='/betrouwbaarheid',
                 definition='Betrouwbaarheid van de peilmeting (goed, '
                            'onbekend of twijfelachtig).',
                 datatype='string'),
        XmlField(name='methode',
                 source_xpath='/methode',
                 definition='Methode waarop de peilmeting uitgevoerd werd.',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=_filterDataCodes_xsd,
                     typename='PeilmetingMethodeEnumType')),
        XmlField(name='filterstatus',
                 source_xpath='/filterstatus',
                 definition='Status van de filter tijdens de peilmeting (in '
                            'rust - werking).',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=_filterDataCodes_xsd,
                     typename='FilterstatusEnumType')),
        XmlField(name='filtertoestand',
                 source_xpath='/filtertoestand',
                 definition="Filtertoestand bij de peilmeting. "
                            "Standaardwaarde is '1' = Normaal.",
                 datatype='integer',
                 xsd_type=XsdType(
                     xsd_schema=_filterDataCodes_xsd,
                     typename='FiltertoestandEnumType'))
    ]


class GrondwaterFilter(AbstractDovType):
    """Class representing the DOV data type for Groundwater screens."""

    subtypes = [Peilmeting]

    fields = [
        WfsField(name='pkey_filter', source_field='filterfiche',
                 datatype='string'),
        WfsField(name='pkey_grondwaterlocatie', source_field='putfiche',
                 datatype='string'),
        WfsField(name='gw_id', source_field='GW_ID', datatype='string'),
        WfsField(name='filternummer', source_field='filternummer',
                 datatype='string'),
        WfsField(name='filtertype', source_field='filtertype',
                 datatype='string'),
        WfsField(name='x', source_field='X_mL72', datatype='float'),
        WfsField(name='y', source_field='Y_mL72', datatype='float'),
        WfsField(name='start_grondwaterlocatie_mtaw', source_field='Z_mTAW',
                 datatype='float'),
        MvMtawField('Maaiveldhoogte in mTAW op dag '
                    'dat de put/boring uitgevoerd werd'),
        WfsField(name='gemeente', source_field='gemeente', datatype='string'),
        XmlField(name='meetnet_code',
                 source_xpath='/filter/meetnet',
                 definition='Tot welk meetnet behoort deze filter.',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=_filterDataCodes_xsd,
                     typename='MeetnetEnumType')),
        XmlField(name='aquifer_code',
                 source_xpath='/filter/ligging/aquifer',
                 definition='De aquifer (watervoerende laag) waarin de filter '
                            'hangt (code) (HCOVv1)',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=build_dov_url(
                         'xdov/schema/latest/xsd/kern/interpretatie/'
                         'HydrogeologischeStratigrafieDataCodes.xsd'),
                     typename='AquiferHCOVv1EnumType')),
        XmlField(name='grondwaterlichaam_code',
                 source_xpath='/filter/ligging/grondwaterlichaam',
                 definition='',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=_filterDataCodes_xsd,
                     typename='GrondwaterlichaamEnumType')),
        XmlField(name='regime',
                 source_xpath='/filter/ligging/regime',
                 definition='',
                 datatype='string'),
        WfsField(name='diepte_onderkant_filter',
                 source_field='onderkant_filter_m', datatype='float'),
        WfsField(name='lengte_filter', source_field='lengte_filter_m',
                 datatype='float')
    ]

    pkey_fieldname = 'filterfiche'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Filter (screen), being a URI of the form
            `https://www.dov.vlaanderen.be/data/filter/<id>`.

        """
        super().__init__('filter', pkey)
