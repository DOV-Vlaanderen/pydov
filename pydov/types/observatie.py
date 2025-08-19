# -*- coding: utf-8 -*-
"""Module containing the DOV data type for observations (Observatie), including
subtypes."""
from collections import OrderedDict

import numpy as np

from pydov.types.fields import WfsField, XmlField, _CustomXmlField
from pydov.types.fields_custom import OsloCodeListValueField

from .abstract import AbstractDovSubType, AbstractDovFieldSet


class NumeriekTekstField(_CustomXmlField):
    """Field for retrieving a numeric or text value from the XML, depending on
    which is available. This is used for fields that can have either a numeric
    or text representation."""

    def __init__(self, name, definition, basename):
        """Initialise a NumeriekTekstField with given definition and basename.

        Parameters
        ----------
        name : string
            Name of the field, used in the resulting dataframe.
        definition : string
            Type-specific definition of the meetwaarde field.
        basename : string
            The basename of the field, which is used to find the correct XML
            elements in the DOV XML. The field will look for
            `<basename>_numeriek` and `<basename>_text` in the XML to
            retrieve the value.
        """
        super().__init__(
            name=name,
            definition=definition,
            datatype='string',
            notnull=False
        )

        self.basename = basename

    def calculate(self, cls, tree):
        """Calculate the value of the measurement.

        Parameters
        ----------
        tree : etree.ElementTree
            ElementTree of the DOV XML for this instance.

        Returns
        -------
        str
            Value of field, parsed from either <basename>_numeriek or
            <basename>_text.
        """

        waarde_numeriek = cls._parse(
            func=tree.findtext,
            xpath=f'.//{self.basename}_numeriek',
            namespace=None,
            returntype='string'
        )
        if waarde_numeriek is not np.nan:
            return waarde_numeriek

        waarde_text = cls._parse(
            func=tree.findtext,
            xpath=f'.//{self.basename}_text',
            namespace=None,
            returntype='string'
        )
        return waarde_text


class ObservatieDetails(AbstractDovFieldSet):
    """Fieldset containing fields with extra details about the observation."""

    intended_for = ['Observatie']

    fields = [
        OsloCodeListValueField(name='betrouwbaarheid',
                               source_xpath='.//betrouwbaarheid',
                               conceptscheme='betrouwbaarheid',
                               definition='Betrouwbaarheid van de observatie',
                               datatype='string'),
        XmlField(name='geobserveerd_object_type',
                 source_xpath='.//geobserveerd_object/objecttype',
                 definition='Objecttype van het geobserveerd object',
                 datatype='string'),
        XmlField(name='geobserveerd_object_naam',
                 source_xpath='.//geobserveerd_object/naam',
                 definition='DOV naam van het geobserveerd object',
                 datatype='string'),
        XmlField(name='geobserveerd_object_permkey',
                 source_xpath='.//geobserveerd_object/permkey',
                 definition='Een unieke DOV identifier '
                            'in de vorm van een permkey.',
                 datatype='string')
    ]


class ObservatieHerhaling(AbstractDovSubType):
    """Subtype showing the repetition information of an observation."""

    rootpath = './/observatie/herhaling'
    intended_for = ['Observatie']

    fields = [
        XmlField(name='herhaling_aantal',
                 source_xpath='/aantal',
                 definition='Aantal herhalingen',
                 datatype='integer'),
        XmlField(name='herhaling_minimum',
                 source_xpath='/minimum',
                 definition='Minimum waarde',
                 datatype='float'),
        XmlField(name='herhaling_maximum',
                 source_xpath='/maximum',
                 definition='Maximum waarde',
                 datatype='float'),
        XmlField(name='herhaling_standaardafwijking',
                 source_xpath='/standaardafwijking',
                 definition='Standaardafwijking metingen',
                 datatype='float')
    ]
from pydov.types.fields import WfsField, XmlField, _CustomXmlField
from .abstract import AbstractDovType, AbstractDovSubType
import numpy as np


class ObservatieSecParResultField(_CustomXmlField):
    """Field for retrieving the treatment of the sampling from the relevant XML
    field."""

    def __init__(self, name, definition):
        super().__init__(
            name=name,
            definition=definition,
            datatype='string',
            notnull=False
        )

    def calculate(self, cls, tree):
        waarde_num = cls._parse(
            func=tree.findtext,
            xpath='/waarde_numeriek',
            namespace=None,
            returntype='string'
        )
        if waarde_num is not np.nan and waarde_num != '':
            return waarde_num
        waarde_text = cls._parse(
            func=tree.findtext,
            xpath='/waarde_text',
            namespace=None,
            returntype='string'
        )
        if waarde_text is not np.nan and waarde_text != '':
            return waarde_text
        else:
            return np.nan


class SecundaireParameter(AbstractDovSubType):
    """Subtype showing the secondary parameter of an observation."""

    rootpath = './/observatie/secundaireparameter'
    intended_for = ['Observatie']

    fields = [
        XmlField(name='secundaireparameter_parameter',
                 source_xpath='/parameter',
                 definition='Secundaire parameter',
                 datatype='string'),
        ObservatieSecParResultField(name='secundaireparameter_resultaat',
                                    definition="Resultaat van de "
                                               "secudaire parameter"),
        XmlField(name='secundaireparameter_eenheid',
                 source_xpath='/eenheid',
                 definition='Eenheid',
                 datatype='string')
    ]


class Fractiemeting(AbstractDovSubType):
    """Subtype showing the details of a fraction measurement."""

    rootpath = './/waarde_fractiemeting/meting'
    intended_for = ['Observatie']

    fields = [
        XmlField(name='fractiemeting_ondergrens',
                 source_xpath='/ondergrens',
                 definition='Ondergrens van de fractiemeting in µm',
                 datatype='float'),
        XmlField(name='fractiemeting_bovengrens',
                 source_xpath='/bovengrens',
                 definition='Bovengrens van de fractiemeting in µm',
                 datatype='float'),
        XmlField(name='fractiemeting_waarde',
                 source_xpath='/waarde',
                 definition='Gemeten massaprocent van de fractie',
                 datatype='float')
    ]


class MeetreeksWaarde(AbstractDovSubType):
    """Subtype showing the details of a measurement value in a series."""

    rootpath = './/meetreekswaarde'
    intended_for = ['Meetreeks']

    fields = [
        NumeriekTekstField(name='meetreeks_meetpunt',
                           definition='Meetpunt',
                           basename='meetpunt'),
        NumeriekTekstField(name='meetreeks_meetwaarde',
                           definition='Meetwaarde',
                           basename='meetwaarde')
    ]


class Meetreeks(AbstractDovSubType):
    """Subtype showing the details of a measurement series."""

    rootpath = './/waarde_meetreeks'
    intended_for = ['Observatie']

    subtypes = [MeetreeksWaarde]

    fields = [
        XmlField(name='meetreeks_meetpunt_parameter',
                 source_xpath='/meetpuntparameter',
                 definition=('(Verkorte) naam van de parameter voor het '
                             'meetpunt'),
                 datatype='string'),
        XmlField(name='meetreeks_meetpunt_eenheid',
                 source_xpath='/meetpuntparameter_eenheid',
                 definition='Eenheid van de meetpuntparameter',
                 datatype='string'),
        XmlField(name='meetreeks_meetwaarde_parameter',
                 source_xpath='/meetwaardeparameter',
                 definition=('(Verkorte) naam van de parameter voor de '
                             'meetwaarde',),
                 datatype='string'),
        XmlField(name='meetreeks_meetwaarde_eenheid',
                 source_xpath='/meetwaardeparameter_eenheid',
                 definition='Eenheid van de meetwaardeparameter',
                 datatype='string')
    ]

    _preferred_field_order = [
        'meetreeks_meetpunt_parameter', 'meetreeks_meetpunt',
        'meetreeks_meetpunt_eenheid', 'meetreeks_meetwaarde_parameter',
        'meetreeks_meetwaarde', 'meetreeks_meetwaarde_eenheid'
    ]

    @classmethod
    def get_fields(cls):
        """Get the fields of the Meetreeks subtype.

        Returns
        -------
        list
            List of fields defined in this subtype.
        """
        return OrderedDict(sorted(
            super().get_fields().items(),
            key=lambda item: cls._preferred_field_order.index(item[0])))

    @classmethod
    def get_field_names(cls):
        """Get the field names of the Meetreeks subtype.

        Returns
        -------
        list
            List of field names defined in this subtype.
        """
        return sorted(super().get_field_names(),
                      key=Meetreeks._preferred_field_order.index)


class Observatie(AbstractDovType):
    """Class representing the DOV data type for observations."""

    fields = [
        WfsField(name='pkey_observatie', source_field='observatie_link',
                 datatype='string'),
        WfsField(name='pkey_parent', source_field='gekoppeld_aan_link',
                 datatype='string'),
        WfsField(name='fenomeentijd', source_field='fenomeentijd',
                 datatype='date'),
        WfsField(name='diepte_van_m', source_field='diepte_van_m',
                 datatype='float'),
        WfsField(name='diepte_tot_m', source_field='diepte_tot_m',
                 datatype='float'),
        WfsField(name='parametergroep', source_field='parametergroep',
                 datatype='string'),
        WfsField(name='parameter', source_field='parameter',
                 datatype='string'),
        WfsField(name='detectieconditie', source_field='detectieconditie',
                 datatype='string'),
        WfsField(name='resultaat', source_field='resultaat',
                 datatype='string'),
        WfsField(name='eenheid', source_field='eenheid',
                 datatype='string'),
        WfsField(name='methode', source_field='methode',
                 datatype='string'),
        WfsField(name='uitvoerder', source_field='uitvoerder',
                 datatype='string'),
        WfsField(name='herkomst', source_field='herkomst',
                 datatype='string')
    ]

    pkey_fieldname = 'observatie_link'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Observatie (observation),
             being a URI of the form
            `https://www.dov.vlaanderen.be/data/observatie/<id>`.

        """
        super().__init__('observatie', pkey)
