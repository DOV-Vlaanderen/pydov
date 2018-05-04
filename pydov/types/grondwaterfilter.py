# -*- coding: utf-8 -*-
"""Module containing the DOV data type for screens (Filter), including
subtypes."""

from owslib.etree import etree

from pydov.types.abstract import (
    AbstractDovType,
    AbstractDovSubType,
)


class Peilmeting(AbstractDovSubType):

    _name = 'peilmeting'
    _rootpath = './/filtermeting/peilmeting'

    _fields = [{
        'name': 'datum',
        'source': 'xml',
        'sourcefield': '/datum',  # relative to rootpath
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
        'sourcefield': '/peil_mtaw', # relative to rootpath
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

    def __init__(self):
        """Initialisation."""
        super(Peilmeting, self).__init__('peilmeting')

    @classmethod
    def from_xml_element(cls, element):
        """Build an instance of this subtype from a single XML element.

        Parameters
        ----------
        element : etree.Element
            XML element representing a single record of this subtype.

        """
        peilmeting = Peilmeting()

        for field in cls.get_fields().values():
            peilmeting.data[field['name']] = peilmeting._parse(
                func=element.findtext,
                xpath=field['sourcefield'],
                namespace=None,
                returntype=field.get('type', None)
            )

        return peilmeting

class GrondwaterFilter(AbstractDovType):
    """Class representing the DOV data type for Groundwater screens."""

    _subtypes = [Peilmeting]

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
        'name': 'gemeente',
        'source': 'wfs',
        'sourcefield': 'gemeente',
        'type': 'string'
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
    }, {
        'name': 'mv_mtaw',
        'source': 'xml',
        'sourcefield':
            '/grondwaterlocatie/puntligging/oorspronkelijk_maaiveld',
        'definition': 'Maaiveldhoogte in mTAW op dag dat de put/boring '
                      'uitgevoerd werd.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'meetnet_code',
        'source': 'xml',
        'sourcefield': '/filter/meetnet',
        'definition': 'Tot welk meetnet behoort deze filter.',
        'type': 'integer',
        'notnull': False
    }, {
        'name': 'aquifer_code',
        'source': 'xml',
        'sourcefield': '/filter/ligging/aquifer',
        'definition': 'In welke watervoerende laag hangt de filter (code).',
        'type': 'string',
        'notnull': False
    }, {
        'name': 'grondwaterlichaam_code',
        'source': 'xml',
        'sourcefield': '/filter/ligging/grondwaterlichaam',
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
    }]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Filter (screen), being a URI of the form
            `https://www.dov.vlaanderen.be/data/boring/<id>`.

        """
        super(GrondwaterFilter, self).__init__('grondwaterfilter', pkey)

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

    def _parse_xml_data(self):
        """Get remote XML data for this DOV object, parse the raw XML and
        save the results in the data object.
        """
        xml = self._get_xml_data()
        tree = etree.fromstring(xml)

        for field in self.get_fields(source=('xml',),
                                     include_subtypes=False).values():
            self.data[field['name']] = self._parse(
                func=tree.findtext,
                xpath=field['sourcefield'],
                namespace=None,
                returntype=field.get('type', None)
            )

        self._parse_subtypes(xml)
