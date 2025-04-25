# -*- coding: utf-8 -*-
"""Module containing the DOV data type for boreholes (Boring), including
subtypes."""
from pydov.types.fields import WfsField, XmlField, XsdType
from pydov.util.dovutil import build_dov_url
from pydov.types.ligging import MvMtawField

from .abstract import AbstractDovFieldSet, AbstractDovSubType, AbstractDovType


class BoorMethode(AbstractDovSubType):
    """Subtype listing the method used to make the borehole."""

    intended_for = ['Boring']

    rootpath = './/boring/details/boormethode'

    fields = [
        XmlField(name='diepte_methode_van',
                 source_xpath='/van',
                 definition='Bovenkant van de laag die met een bepaalde '
                            'methode aangeboord werd, in meter.',
                 datatype='float'),
        XmlField(name='diepte_methode_tot',
                 source_xpath='/tot',
                 definition='Onderkant van de laag die met een bepaalde '
                            'methode aangeboord werd, in meter.',
                 datatype='float'),
        XmlField(name='boormethode',
                 source_xpath='/methode',
                 definition='Boormethode voor het diepte-interval.',
                 datatype='string')
    ]


class Kleur(AbstractDovSubType):
    """Subtype listing the color values of the borehole."""

    intended_for = ['Boring']

    rootpath = './/boring/details/kleur'

    fields = [
        XmlField(name='diepte_kleur_van',
                 source_xpath='/van',
                 definition='Bovenkant van de laag met een bepaalde '
                            'bekisting, in meter.',
                 datatype='float'),
        XmlField(name='diepte_kleur_tot',
                 source_xpath='/tot',
                 definition='Onderkant van de laag met een bepaalde '
                            'bekisting, in meter.',
                 datatype='float'),
        XmlField(name='kleur',
                 source_xpath='/kleur',
                 definition='Grondkleur voor het diepte-interval',
                 datatype='string')
    ]


class Boring(AbstractDovType):
    """Class representing the DOV data type for boreholes."""

    subtypes = [BoorMethode]

    fields = [
        WfsField(name='pkey_boring', source_field='fiche', datatype='string'),
        WfsField(name='boornummer', source_field='boornummer',
                 datatype='string'),
        WfsField(name='x', source_field='X_mL72', datatype='float'),
        WfsField(name='y', source_field='Y_mL72', datatype='float'),
        MvMtawField('Maaiveldhoogte in mTAW op dag dat de boring '
                    'uitgevoerd werd.'),
        WfsField(name='start_boring_mtaw', source_field='Z_mTAW',
                 datatype='float'),
        WfsField(name='gemeente', source_field='gemeente', datatype='string'),
        XmlField(name='diepte_boring_van',
                 source_xpath='/boring/diepte_van',
                 definition='Startdiepte van de boring (in meter).',
                 datatype='float',
                 notnull=True),
        WfsField(name='diepte_boring_tot', source_field='diepte_tot_m',
                 datatype='float'),
        WfsField(name='datum_aanvang', source_field='datum_aanvang',
                 datatype='date'),
        WfsField(name='uitvoerder', source_field='uitvoerder',
                 datatype='string'),
        XmlField(name='boorgatmeting',
                 source_xpath='/boring/boorgatmeting/uitgevoerd',
                 definition='Is er een boorgatmeting uitgevoerd (ja/nee).',
                 datatype='boolean')
    ]

    pkey_fieldname = 'fiche'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Boring (borehole), being a URI of the form
            `https://www.dov.vlaanderen.be/data/boring/<id>`.

        """
        super().__init__('boring', pkey)


class MethodeXyz(AbstractDovFieldSet):
    """Fieldset containing fields for method and reliability of the point
    location of the borehole."""

    __generiekeDataCodes = build_dov_url(
        'xdov/schema/latest/xsd/kern/generiek/GeneriekeDataCodes.xsd')

    intended_for = ['Boring']

    fields = [
        XmlField(name='methode_xy',
                 source_xpath='/boring/ligging/metadata_locatiebepaling'
                 '/methode',
                 definition='Methode waarop de x en y-coordinaat opgemeten '
                 'werden.',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=__generiekeDataCodes,
                     typename='MethodeOpmetenXyEnumType')),
        XmlField(name='betrouwbaarheid_xy',
                 source_xpath='/boring/ligging/metadata_locatiebepaling'
                 '/betrouwbaarheid',
                 definition='Betrouwbaarheid van het opmeten van de x en '
                 'y-coordinaat.',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=__generiekeDataCodes,
                     typename='BetrouwbaarheidXyzEnumType')),
        XmlField(name='methode_z',
                 source_xpath='/boring/ligging/metadata_hoogtebepaling'
                 '/methode',
                 definition='Methode waarop de z-coordinaat '
                 'opgemeten werd.',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=__generiekeDataCodes,
                     typename='MethodeOpmetenZEnumType')),
        XmlField(name='betrouwbaarheid_z',
                 source_xpath='/boring/ligging/metadata_hoogtebepaling'
                 '/betrouwbaarheid',
                 definition='Betrouwbaarheid van het opmeten van de '
                 'z-coordinaat.',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=__generiekeDataCodes,
                     typename='BetrouwbaarheidXyzEnumType'))
    ]
