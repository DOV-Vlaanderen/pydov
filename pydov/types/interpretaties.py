# -*- coding: utf-8 -*-
"""Module containing the DOV data type for boreholes (Boring), including
subtypes."""
import numpy as np

from pydov.types.abstract import (
    AbstractDovType,
    AbstractDovSubType,
)


class InformeleStratigrafieLaag(AbstractDovSubType):

    _name = 'informele_stratigrafie_laag'
    _rootpath = './/informelestratigrafie/laag'

    _fields = [{
        'name': 'diepte_laag_van',
        'source': 'xml',
        'sourcefield': '/van',
        'definition': 'Diepte van de bovenkant van de laag informele '
                      'stratigrafie in meter.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'diepte_laag_tot',
        'source': 'xml',
        'sourcefield': '/tot',
        'definition': 'Diepte van de onderkant van de laag informele '
                      'stratigrafie in meter.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'beschrijving',
        'source': 'xml',
        'sourcefield': '/beschrijving',
        'definition': 'Benoeming van de eenheid van de laag informele '
                      'stratigrafie in vrije tekst (onbeperkt in lengte).',
        'type': 'string',
        'notnull': False
    }]

    def __init__(self):
        """Initialisation."""
        super(InformeleStratigrafieLaag, self).__init__(
            'informele_stratigrafie_laag')

    @classmethod
    def from_xml_element(cls, element):
        """Build an instance of this subtype from a single XML element.

        Parameters
        ----------
        element : etree.Element
            XML element representing a single record of this subtype.

        """
        laag = InformeleStratigrafieLaag()

        for field in cls.get_fields().values():
            laag.data[field['name']] = laag._parse(
                func=element.findtext,
                xpath=field['sourcefield'],
                namespace=None,
                returntype=field.get('type', None)
            )

        return laag


class InformeleStratigrafie(AbstractDovType):
    """Class representing the DOV data type for boreholes."""

    _subtypes = [InformeleStratigrafieLaag]

    _fields = [{
        'name': 'pkey_interpretatie',
        'source': 'wfs',
        'sourcefield': 'Interpretatiefiche',
        'type': 'string'
    }, {
        'name': 'pkey_boring',
        'source': 'custom',
        'type': 'string',
        'definition': 'URL die verwijst naar de gegevens van de boring '
                      'waaraan deze informele stratigrafie gekoppeld is ('
                      'indien gekoppeld aan een boring).',
        'notnull': False
    }, {
        'name': 'pkey_sondering',
        'source': 'custom',
        'type': 'string',
        'definition': 'URL die verwijst naar de gegevens van de sondering '
                      'waaraan deze informele stratigrafie gekoppeld is ('
                      'indien gekoppeld aan een sondering).',
        'notnull': False
    }, {
        'name': 'betrouwbaarheid_interpretatie',
        'source': 'wfs',
        'sourcefield': 'Betrouwbaarheid',
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
    }]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Boring (borehole), being a URI of the form
            `https://www.dov.vlaanderen.be/data/boring/<id>`.

        """
        super(InformeleStratigrafie, self).__init__(
            'interpretatie', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        """Build `Boring` instance from a WFS feature element.

        Parameters
        ----------
        feature : etree.Element
            XML element representing a single record of the WFS layer.
        namespace : str
            Namespace associated with this WFS featuretype.

        Returns
        -------
        boring : Boring
            An instance of this class populated with the data from the WFS
            element.

        """
        infstrat = InformeleStratigrafie(
            feature.findtext('./{%s}Interpretatiefiche' % namespace))

        typeproef = cls._parse(
            func=feature.findtext,
            xpath='Type_proef',
            namespace=namespace,
            returntype='string'
        )

        if typeproef == 'Boring':
            infstrat.data['pkey_boring'] = cls._parse(
                func=feature.findtext,
                xpath='Proeffiche',
                namespace=namespace,
                returntype='string'
            )
            infstrat.data['pkey_sondering'] = np.nan
        elif typeproef == 'Sondering':
            infstrat.data['pkey_sondering'] = cls._parse(
                func=feature.findtext,
                xpath='Proeffiche',
                namespace=namespace,
                returntype='string'
            )
            infstrat.data['pkey_boring'] = np.nan
        else:
            infstrat.data['pkey_boring'] = np.nan
            infstrat.data['pkey_sondering'] = np.nan

        for field in cls.get_fields(source=('wfs',)).values():
            if field['name'] in ['pkey_boring', 'pkey_sondering']:
                continue

            infstrat.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return infstrat


class HydrogeologischeStratigrafieLaag(AbstractDovSubType):

    _name = 'hydrogeologische_stratigrafie_laag'
    _rootpath = './/hydrogeologischeinterpretatie/laag'

    _fields = [{
        'name': 'diepte_laag_van',
        'source': 'xml',
        'sourcefield': '/van',
        'definition': 'Diepte van de bovenkant van de laag hydrogeologische '
                      'stratigrafie in meter.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'diepte_laag_tot',
        'source': 'xml',
        'sourcefield': '/tot',
        'definition': 'Diepte van de onderkant van de laag hydrogeologische '
                      'stratigrafie in meter.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'aquifer',
        'source': 'xml',
        'sourcefield': '/aquifer',
        'definition': 'code van de watervoerende laag waarin de laag '
                      'Hydrogeologische stratigrafie zich bevindt.',
        'type': 'string',
        'notnull': False
    }]

    def __init__(self):
        """Initialisation."""
        super(HydrogeologischeStratigrafieLaag, self).__init__(
            'hydrogeologische_interpretatie_laag')

    @classmethod
    def from_xml_element(cls, element):
        """Build an instance of this subtype from a single XML element.

        Parameters
        ----------
        element : etree.Element
            XML element representing a single record of this subtype.

        """
        laag = HydrogeologischeStratigrafieLaag()

        for field in cls.get_fields().values():
            laag.data[field['name']] = laag._parse(
                func=element.findtext,
                xpath=field['sourcefield'],
                namespace=None,
                returntype=field.get('type', None)
            )

        return laag


class HydrogeologischeStratigrafie(AbstractDovType):
    """Class representing the DOV data type for boreholes."""

    _subtypes = [HydrogeologischeStratigrafieLaag]

    _fields = [{
        'name': 'pkey_interpretatie',
        'source': 'wfs',
        'sourcefield': 'Interpretatiefiche',
        'type': 'string'
    }, {
        'name': 'pkey_boring',
        'source': 'custom',
        'type': 'string',
        'definition': 'URL die verwijst naar de gegevens van de boring '
                      'waaraan deze hydrogeologische stratigrafie '
                      'gekoppeld is '
                      '(indien gekoppeld aan een boring).',
        'notnull': False
    }, {
        'name': 'pkey_sondering',
        'source': 'custom',
        'type': 'string',
        'definition': 'URL die verwijst naar de gegevens van de sondering '
                      'waaraan deze informele stratigrafie gekoppeld is ('
                      'indien gekoppeld aan een sondering).',
        'notnull': False
    }, {
        'name': 'betrouwbaarheid_interpretatie',
        'source': 'wfs',
        'sourcefield': 'Betrouwbaarheid',
        'type': 'string'
    },  {
        'name': 'x',
        'source': 'wfs',
        'sourcefield': 'X_mL72',
        'type': 'float'
    }, {
        'name': 'y',
        'source': 'wfs',
        'sourcefield': 'Y_mL72',
        'type': 'float'
    }]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Hydrogeologische stratigrafie, being a URI
            of the form
            `https://www.dov.vlaanderen.be/data/boring/<id>`.

        """
        super(HydrogeologischeStratigrafie, self).__init__(
              'interpretatie', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        """Build 'HydrogeologischeStratigrafie' instance from a WFS feature
        element.

        Parameters
        ----------
        feature : etree.Element
            XML element representing a single record of the WFS layer.
        namespace : str
            Namespace associated with this WFS featuretype.

        Returns
        -------
        HydrogeologischeStratigrafie : HydrogeologischeStratigrafie
            An instance of this class populated with the data from the WFS
            element.

        """
        hydstrat = HydrogeologischeStratigrafie(
            feature.findtext('./{%s}Interpretatiefiche' % namespace))

        typeproef = cls._parse(
            func=feature.findtext,
            xpath='Type_proef',
            namespace=namespace,
            returntype='string'
        )

        if typeproef == 'Boring':
            hydstrat.data['pkey_boring'] = cls._parse(
                func=feature.findtext,
                xpath='Proeffiche',
                namespace=namespace,
                returntype='string'
            )
            hydstrat.data['pkey_sondering'] = np.nan

        elif typeproef == 'Sondering':
            hydstrat.data['pkey_sondering'] = cls._parse(
                func=feature.findtext,
                xpath='Proeffiche',
                namespace=namespace,
                returntype='string'
            )
            hydstrat.data['pkey_boring'] = np.nan
        else:
            hydstrat.data['pkey_boring'] = np.nan
            hydstrat.data['pkey_sondering'] = np.nan

        for field in cls.get_fields(source=('wfs',)).values():
            if field['name'] in ['pkey_boring', 'pkey_sondering']:
                continue

            hydstrat.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return hydstrat


class LithologischeBeschrijvingLaag(AbstractDovSubType):

    _name = 'lithologische_beschrijving_laag'
    _rootpath = './/lithologischebeschrijving/laag'

    _fields = [{
        'name': 'diepte_laag_van',
        'source': 'xml',
        'sourcefield': '/van',
        'definition': 'Diepte van de bovenkant van de laag lithologische '
                      'beschrijving in meter.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'diepte_laag_tot',
        'source': 'xml',
        'sourcefield': '/tot',
        'definition': 'Diepte van de onderkant van de laag lithologische '
                      'beschrijving in meter.',
        'type': 'float',
        'notnull': False
    }, {
        'name': 'beschrijving',
        'source': 'xml',
        'sourcefield': '/beschrijving',
        'definition': 'Lithologische beschrijving van de laag in vrije tekst '
                      '(onbeperkt in lengte)',
        'type': 'string',
        'notnull': False
    }]

    def __init__(self):
        """Initialisation."""
        super(LithologischeBeschrijvingLaag, self).__init__(
            'lithologische_beschrijving_laag')

    @classmethod
    def from_xml_element(cls, element):
        """Build an instance of this subtype from a single XML element.

        Parameters
        ----------
        element : etree.Element
            XML element representing a single record of this subtype.

        """
        laag = LithologischeBeschrijvingLaag()

        for field in cls.get_fields().values():
            laag.data[field['name']] = laag._parse(
                func=element.findtext,
                xpath=field['sourcefield'],
                namespace=None,
                returntype=field.get('type', None)
            )

        return laag


class LithologischeBeschrijvingen(AbstractDovType):
    """Class representing the DOV data type for 'lithologische beschrijvingen' interpretations."""

    _subtypes = [LithologischeBeschrijvingLaag]

    _fields = [{
        'name': 'pkey_interpretatie',
        'source': 'wfs',
        'sourcefield': 'Interpretatiefiche',
        'type': 'string'
    }, {
        'name': 'pkey_boring',
        'source': 'custom',
        'type': 'string',
        'definition': 'URL die verwijst naar de gegevens van de boring '
                      'waaraan deze lithologische beschrijving '
                      'gekoppeld is '
                      '(indien gekoppeld aan een boring).',
        'notnull': False
    }, {
        'name': 'pkey_sondering',
        'source': 'custom',
        'type': 'string',
        'definition': 'URL die verwijst naar de gegevens van de sondering '
                      'waaraan deze lithologische beschrijving gekoppeld is '
                      '(indien gekoppeld aan een sondering).',
        'notnull': False
    }, {
        'name': 'betrouwbaarheid_interpretatie',
        'source': 'wfs',
        'sourcefield': 'Betrouwbaarheid',
        'type': 'string'
    },  {
        'name': 'x',
        'source': 'wfs',
        'sourcefield': 'X_mL72',
        'type': 'float'
    }, {
        'name': 'y',
        'source': 'wfs',
        'sourcefield': 'Y_mL72',
        'type': 'float'
    }]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the 'Lithologische beschrijvingen', being a URI
            of the form
            `https://www.dov.vlaanderen.be/data/interpretaties/<id>`.

        """
        super(LithologischeBeschrijvingen, self).__init__(
              'interpretatie', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        """Build 'LithologischeBeschrijvingen' instance from a WFS feature
        element.

        Parameters
        ----------
        feature : etree.Element
            XML element representing a single record of the WFS layer.
        namespace : str
            Namespace associated with this WFS featuretype.

        Returns
        -------
        LithologischeBeschrijvingen : LithologischeBeschrijvingen
            An instance of this class populated with the data from the WFS
            element.

        """
        lithobes = LithologischeBeschrijvingen(
            feature.findtext('./{%s}Interpretatiefiche' % namespace))

        typeproef = cls._parse(
            func=feature.findtext,
            xpath='Type_proef',
            namespace=namespace,
            returntype='string'
        )

        if typeproef == 'Boring':
            lithobes.data['pkey_boring'] = cls._parse(
                func=feature.findtext,
                xpath='Proeffiche',
                namespace=namespace,
                returntype='string'
            )
            lithobes.data['pkey_sondering'] = np.nan

        elif typeproef == 'Sondering':
            lithobes.data['pkey_sondering'] = cls._parse(
                func=feature.findtext,
                xpath='Proeffiche',
                namespace=namespace,
                returntype='string'
            )
            lithobes.data['pkey_boring'] = np.nan
        else:
            lithobes.data['pkey_boring'] = np.nan
            lithobes.data['pkey_sondering'] = np.nan

        for field in cls.get_fields(source=('wfs',)).values():
            if field['name'] in ['pkey_boring', 'pkey_sondering']:
                continue

            lithobes.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return lithobes


