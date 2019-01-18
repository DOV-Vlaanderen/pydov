# -*- coding: utf-8 -*-
"""Module containing the DOV data type for CPT measurements (Sonderingen),
including subtypes."""
from pydov.types.abstract import (
    AbstractDovType,
    AbstractDovSubType,
)


class Meetdata(AbstractDovSubType):

    _name = 'penetratietest'
    _rootpath = './/sondering/sondeonderzoek/penetratietest/meetdata'

    _fields = [{
        'name': 'z',
        'source': 'xml',
        'sourcefield': '/sondeerdiepte',
        'definition': 'Diepte waarop sondeerparameters geregistreerd werden, '
                      'uitgedrukt in meter ten opzicht van het aanvangspeil.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'qc',
        'source': 'xml',
        'sourcefield': '/qc',
        'definition': 'Opgemeten waarde van de conusweerstand, uitgedrukt in '
                      'MPa.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'Qt',
        'source': 'xml',
        'sourcefield': '/Qt',
        'definition': 'Opgemeten waarde van de totale weerstand, uitgedrukt '
                      'in kN.',
        'type': 'string',
        'notnull': False
    }, {
        'name': 'fs',
        'source': 'xml',
        'sourcefield': '/fs',
        'definition': 'Opgemeten waarde van de plaatelijke kleefweerstand, '
                      'uitgedrukt in kPa.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'u',
        'source': 'xml',
        'sourcefield': '/u',
        'definition': 'Opgemeten waarde van de porienwaterspanning, '
                      'uitgedrukt in kPa.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'i',
        'source': 'xml',
        'sourcefield': '/i',
        'definition': 'Opgemeten waarde van de inclinatie, uitgedrukt in '
                      'graden.',
        'type': 'float',
        'notnull': False
    }]


class Sondering(AbstractDovType):
    """Class representing the DOV data type for CPT measurements."""

    _subtypes = [Meetdata]

    _fields = [{
        'name': 'pkey_sondering',
        'source': 'wfs',
        'sourcefield': 'fiche',
        'type': 'string'
    }, {
        'name': 'sondeernummer',
        'source': 'wfs',
        'sourcefield': 'sondeernummer',
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
        'name': 'start_sondering_mtaw',
        'source': 'wfs',
        'sourcefield': 'Z_mTAW',
        'type': 'float'
    }, {
        'name': 'diepte_sondering_van',
        'source': 'wfs',
        'sourcefield': 'diepte_van_m',
        'type': 'float'
    }, {
        'name': 'diepte_sondering_tot',
        'source': 'wfs',
        'sourcefield': 'diepte_tot_m',
        'type': 'float'
    }, {
        'name': 'datum_aanvang',
        'source': 'wfs',
        'sourcefield': 'datum_aanvang',
        'type': 'date'
    }, {
        'name': 'uitvoerder',
        'source': 'wfs',
        'sourcefield': 'uitvoerder',
        'type': 'string'
    }, {
        'name': 'sondeermethode',
        'source': 'wfs',
        'sourcefield': 'sondeermethode',
        'type': 'string'
    }, {
        'name': 'apparaat',
        'source': 'wfs',
        'sourcefield': 'apparaat_type',
        'type': 'string'
    }, {
        'name': 'datum_gw_meting',
        'source': 'xml',
        'sourcefield': '/sondering/visueelonderzoek/'
                       'datumtijd_waarneming_grondwaterstand',
        'definition': 'Datum en tijdstip van waarneming van de '
                      'grondwaterstand.',
        'type': 'datetime',
        'notnull': False
    }, {
        'name': 'diepte_gw_m',
        'source': 'xml',
        'sourcefield': '/sondering/visueelonderzoek/grondwaterstand',
        'definition': 'Diepte water in meter ten opzicht van het '
                      'aanvangspeil.',
        'type': 'float',
        'notnull': False
    }]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Sondering (CPT measurement), being a URI of
            the form `https://www.dov.vlaanderen.be/data/sondering/<id>`.

        """
        super(Sondering, self).__init__('sondering', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        """Build `Sondering` instance from a WFS feature element.

        Parameters
        ----------
        feature : etree.Element
            XML element representing a single record of the WFS layer.
        namespace : str
            Namespace associated with this WFS featuretype.

        Returns
        -------
        sondering : Sondering
            An instance of this class populated with the data from the WFS
            element.

        """
        s = Sondering(feature.findtext('./{%s}fiche' % namespace))

        for field in cls.get_fields(source=('wfs',)).values():
            s.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return s
