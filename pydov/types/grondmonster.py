# -*- coding: utf-8 -*-
"""Module containing the DOV data type for screens (Filter), including
subtypes."""
import numpy as np
from .abstract import (
    AbstractDovType,
    AbstractDovSubType,
)


class Korrelverdeling(AbstractDovSubType):

    _name = 'korrelverdeling'
    _rootpath = './/grondmonster/observatieReeksData/' \
                'korrelverdeling_reeks/korrelverdeling'

    _fields = [{
        'name': 'diameter',
        'source': 'xml',
        'sourcefield': '/diameter',
        'definition': '.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'fractie',
        'source': 'xml',
        'sourcefield': '/fractie',
        'definition': '.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'methode',
        'source': 'xml',
        'sourcefield': '/methode',
        'definition': '.',
        'type': 'string',
        'notnull': False
    }, ]


class Grondmonster(AbstractDovType):
    """Class representing the DOV data type for ground samples."""

    _subtypes = [Korrelverdeling]

    _xsd_schemas = [
        'https://www.dov.vlaanderen.be/xdov/schema/latest/xsd/kern/'
        'grondmonster/GrondmonsterDataCodes.xsd',
    ]

    _fields = [{
        'name': 'pkey_boring',
        'source': 'wfs',
        'sourcefield': 'boringfiche',
        'type': 'string'
    }, {
        'name': 'pkey_grondmonster',
        'source': 'wfs',
        'sourcefield': 'grondmonsterfiche',
        'type': 'string'
    }, {
        'name': 'naam',
        'source': 'wfs',
        'sourcefield': 'naam',
        'type': 'string'
    }, {
        'name': 'boornummer',
        'source': 'wfs',
        'sourcefield': 'boornummer',
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
        'name': 'z_mtaw',
        'source': 'wfs',
        'sourcefield': 'Z_mTAW',
        'type': 'float'
    }, {
        'name': 'gemeente',
        'source': 'wfs',
        'sourcefield': 'gemeente',
        'type': 'string'
    }, {
        'name': 'diepte_van_m',
        'source': 'wfs',
        'sourcefield': 'diepte_van_m',
        'type': 'float',
    }, {
        'name': 'diepte_tot_m',
        'source': 'wfs',
        'sourcefield': 'diepte_tot_m',
        'type': 'float',
    }, {
        'name': 'peil_tot_mtaw',
        'source': 'wfs',
        'sourcefield': 'peil_tot_mTAW',
        'type': 'float',
    }, {
        'name': 'monstertype',
        'source': 'xml',
        'sourcefield': '/grondmonster/monstertype',
        'xsd_type': 'MonsterEnumType',
        'definition': 'type monster',
        'type': 'string',
    }, {
        'name': 'astm_naam',
        'source': 'xml',
        'sourcefield': '/grondmonster/observatieData/observatie['
                       'parameter="ASTM_NAAM"]/waarde_text',
        'xsd_type': 'ParameterEnumType',
        'definition': 'ASTM_naam',
        'type': 'string'
    }, {
        'name': 'grondsoort_bggg',
        'source': 'xml',
        'sourcefield': '/grondmonster/observatieData/observatie['
                       'parameter="BGGG"]/waarde_text',
        'xsd_type': 'ParameterEnumType',
        'definition': 'Grondsoort BGGG',
        'type': 'string'
    }]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Filter (screen), being a URI of the form
            `https://www.dov.vlaanderen.be/data/boring/<id>`.

        """
        super(Grondmonster, self).__init__('grondmonster', pkey)

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
        grondmonster = Grondmonster(
            feature.findtext('./{%s}grondmonster' % namespace))

        for field in cls.get_fields(source=('wfs',)).values():
            grondmonster.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return grondmonster
