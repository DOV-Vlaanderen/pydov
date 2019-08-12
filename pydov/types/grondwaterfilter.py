# -*- coding: utf-8 -*-
"""Module containing the DOV data type for screens (Filter), including
subtypes."""

from .abstract import (
    AbstractDovType,
    AbstractDovSubType,
    XmlField,
    XsdType,
    WfsField,
)


class Peilmeting(AbstractDovSubType):

    rootpath = './/filtermeting/peilmeting'

    fields = [
        XmlField(name='datum',
                 source_xpath='/datum',
                 definition='Datum van opmeten.',
                 datatype='date',
                 notnull=True),
        XmlField(name='tijdstip',
                 source_xpath='/tijdstip',
                 definition='Tijdstip van opmeten (optioneel).',
                 datatype='string',
                 notnull=False),
        XmlField(name='peil_mtaw',
                 source_xpath='/peil_mtaw',
                 definition='Diepte van de peilmeting, uitgedrukt in mTAW.',
                 datatype='float',
                 notnull=False),
        XmlField(name='betrouwbaarheid',
                 source_xpath='/betrouwbaarheid',
                 definition='Lijst van betrouwbaarheden (goed, onbekend of'
                            'twijfelachtig).',
                 datatype='string',
                 notnull=False),
        XmlField(name='methode',
                 source_xpath='/methode',
                 definition='Methode waarop de peilmeting uitgevoerd werd.',
                 datatype='string',
                 notnull=False,
                 xsd_type=XsdType(
                     xsd_schema='https://www.dov.vlaanderen.be/xdov/schema/'
                                'latest/xsd/kern/gwmeetnet/'
                                'FilterDataCodes.xsd',
                     typename='PeilmetingMethodeEnumType')),
        XmlField(name='filterstatus',
                 source_xpath='/filterstatus',
                 definition='Status van de filter tijdens de peilmeting (in '
                            'rust - werking).',
                 datatype='string',
                 notnull=False,
                 xsd_type=XsdType(
                     xsd_schema='https://www.dov.vlaanderen.be/xdov/schema/'
                                'latest/xsd/kern/gwmeetnet/'
                                'FilterDataCodes.xsd',
                     typename='FilterstatusEnumType')),
        XmlField(name='filtertoestand',
                 source_xpath='/filtertoestand',
                 definition="Filtertoestand bij de peilmeting. "
                            "Standaardwaarde is '1' = Normaal.",
                 datatype='integer',
                 notnull=False,
                 xsd_type=XsdType(
                     xsd_schema='https://www.dov.vlaanderen.be/xdov/schema/'
                                'latest/xsd/kern/gwmeetnet/'
                                'FilterDataCodes.xsd',
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
        WfsField(name='mv_mtaw', source_field='Z_mTAW', datatype='float'),
        WfsField(name='gemeente', source_field='gemeente', datatype='string'),
        XmlField(name='meetnet_code',
                 source_xpath='/filter/meetnet',
                 definition='Tot welk meetnet behoort deze filter.',
                 datatype='integer',
                 notnull=False,
                 xsd_type=XsdType(
                     xsd_schema='https://www.dov.vlaanderen.be/xdov/schema/'
                                'latest/xsd/kern/gwmeetnet/'
                                'FilterDataCodes.xsd',
                     typename='MeetnetEnumType')),
        XmlField(name='aquifer_code',
                 source_xpath='/filter/ligging/aquifer',
                 definition='In welke watervoerende laag hangt de filter '
                            '(code).',
                 datatype='string',
                 notnull=False,
                 xsd_type=XsdType(
                     xsd_schema='https://www.dov.vlaanderen.be/xdov/schema/'
                                'latest/xsd/kern/interpretatie/'
                                'HydrogeologischeStratigrafieDataCodes.xsd',
                     typename='AquiferEnumType')),
        XmlField(name='grondwaterlichaam_code',
                 source_xpath='/filter/ligging/grondwaterlichaam',
                 definition='',
                 datatype='string',
                 notnull=False,
                 xsd_type=XsdType(
                     xsd_schema='https://www.dov.vlaanderen.be/xdov/schema/'
                                'latest/xsd/kern/gwmeetnet/'
                                'FilterDataCodes.xsd',
                     typename='GrondwaterlichaamEnumType')),
        XmlField(name='regime',
                 source_xpath='/filter/ligging/regime',
                 definition='',
                 datatype='string',
                 notnull=False),
        WfsField(name='diepte_onderkant_filter',
                 source_field='onderkant_filter_m', datatype='float'),
        WfsField(name='lengte_filter', source_field='lengte_filter_m',
                 datatype='float')
    ]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Filter (screen), being a URI of the form
            `https://www.dov.vlaanderen.be/data/boring/<id>`.

        """
        super(GrondwaterFilter, self).__init__('filter', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        """Build `GrondwaterFilter` instance from a WFS feature element.

        Parameters
        ----------
        feature : etree.Element
            XML element representing a single record of the WFS layer.
        namespace : str
            Namespace associated with this WFS featuretype.

        Returns
        -------
        filter : GrondwaterFilter
            An instance of this class populated with the data from the WFS
            element.

        """
        gwfilter = cls(feature.findtext('./{%s}filterfiche' % namespace))

        for field in cls.get_fields(source=('wfs',)).values():
            gwfilter.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return gwfilter
