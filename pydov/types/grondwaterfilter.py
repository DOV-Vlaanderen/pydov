# -*- coding: utf-8 -*-
"""Module containing the DOV data type for screens (Filter), including
subtypes."""

from .abstract import (
    AbstractDovType,
    AbstractDovSubType,
)


class Peilmeting(AbstractDovSubType):

    _name = 'peilmeting'
    _rootpath = './/filtermeting/peilmeting'

    _fields = [{
        'name': 'datum',
        'source': 'xml',
        'sourcefield': '/datum',
        'definition': 'Datum van opmeten.',
        'type': 'date',
        'notnull': True
    }, {
        'name': 'tijdstip',
        'source': 'xml',
        'sourcefield': '/tijdstip',
        'definition': 'Tijdstip van opmeten (optioneel).',
        'type': 'string',
        'notnull': False
    }, {
        'name': 'peil_mtaw',
        'source': 'xml',
        'sourcefield': '/peil_mtaw',
        'definition': 'Diepte van de peilmeting, uitgedrukt in mTAW.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'betrouwbaarheid',
        'source': 'xml',
        'sourcefield': '/betrouwbaarheid',
        'definition': 'Lijst van betrouwbaarheden (goed, onbekend of'
                      'twijfelachtig).',
        'type': 'string',
        'notnull': False
    }, {
        'name': 'methode',
        'source': 'xml',
        'sourcefield': '/peilmeting/methode',
        'definition': 'Methode waarop de peilmeting uitgevoerd werd.',
        'type': 'string',
        'notnull': False
    }]


class GrondwaterFilter(AbstractDovType):
    """Class representing the DOV data type for Groundwater screens."""

    _subtypes = [Peilmeting]

    _xsd_schemas = [
        'https://www.dov.vlaanderen.be/xdov/schema/latest/xsd/kern/'
        'gwmeetnet/FilterDataCodes.xsd',
        'https://www.dov.vlaanderen.be/xdov/schema/latest/xsd/kern/'
        'interpretatie/HydrogeologischeStratigrafieDataCodes.xsd'
    ]

    _fields = [{
        'name': 'pkey_filter',
        'source': 'wfs',
        'sourcefield': 'filterfiche',
        'type': 'string'
    }, {
        'name': 'pkey_grondwaterlocatie',
        'source': 'wfs',
        'sourcefield': 'putfiche',
        'type': 'string'
    }, {
        'name': 'gw_id',
        'source': 'wfs',
        'sourcefield': 'GW_ID',
        'type': 'string'
    }, {
        'name': 'filternummer',
        'source': 'wfs',
        'sourcefield': 'filternr',
        'type': 'string'
    }, {
        'name': 'filtertype',
        'source': 'wfs',
        'sourcefield': 'filtertype',
        'type': 'string'
    }, {
        'name': 'x',
        'source': 'wfs',
        'sourcefield': 'X_mL72',
        'type': 'float'
    }, {
        'name': 'y',
        'source': 'wfs',
        'sourcefield': 'Y_mL72',
        'type': 'float'
    }, {
        'name': 'mv_mtaw',
        'source': 'wfs',
        'sourcefield': 'Z_mTAW',
        'type': 'float'
    }, {
        'name': 'gemeente',
        'source': 'wfs',
        'sourcefield': 'gemeente',
        'type': 'string'
    }, {
        'name': 'meetnet_code',
        'source': 'xml',
        'sourcefield': '/filter/meetnet',
        'xsd_type': 'MeetnetEnumType',
        'definition': 'Tot welk meetnet behoort deze filter.',
        'type': 'integer',
        'notnull': False
    }, {
        'name': 'aquifer_code',
        'source': 'xml',
        'sourcefield': '/filter/ligging/aquifer',
        'xsd_type': 'AquiferEnumType',
        'definition': 'In welke watervoerende laag hangt de filter (code).',
        'type': 'string',
        'notnull': False
    }, {
        'name': 'grondwaterlichaam_code',
        'source': 'xml',
        'sourcefield': '/filter/ligging/grondwaterlichaam',
        'xsd_type': 'GrondwaterlichaamEnumType',
        'definition': '',
        'type': 'string',
        'notnull': False
    }, {
        'name': 'regime',
        'source': 'xml',
        'sourcefield': '/filter/ligging/regime',
        'definition': '',
        'type': 'string',
        'notnull': False
    }, {
        'name': 'diepte_onderkant_filter',
        'source': 'wfs',
        'sourcefield': 'onderkant_filter_m',
        'type': 'float'
    }, {
        'name': 'lengte_filter',
        'source': 'wfs',
        'sourcefield': 'lengte_filter_m',
        'type': 'float'
    }]

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
        gwfilter = GrondwaterFilter(
            feature.findtext('./{%s}filterfiche' % namespace))

        for field in cls.get_fields(source=('wfs',)).values():
            gwfilter.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return gwfilter
