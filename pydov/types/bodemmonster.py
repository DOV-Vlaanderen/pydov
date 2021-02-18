# -*- coding: utf-8 -*-
"""Module containing the DOV data type for bodemmonsters, including
subtypes."""
from pydov.types.fields import WfsField, XmlField

from .abstract import AbstractDovType


class Bodemmonster(AbstractDovType):
    """Class representing the DOV data type for bodemmonsters."""

    subtypes = []

    fields = [
        WfsField(name='pkey_bodemmonster', source_field='Bodemmonsterfiche', datatype='string'),
        WfsField(name='identificatie', source_field='Bodemmonster', datatype='string'),
        WfsField(name='datum_monstername', source_field='Datum_monsterafname', datatype='date'),
        XmlField(name='tijdstip_monstername',
                 source_xpath='/bodemmonster/tijdstip_monstername',
                 definition='Tijdstip waarop het monster werd genomen.',
                 datatype='time'),
        WfsField(name='type', source_field='Type', datatype='string'),
        WfsField(name='monsternamedoor', source_field='Monsterafname_door', datatype='string'),
        WfsField(name='techniek', source_field='Techniek_monsterafname', datatype='string'),
        WfsField(name='condities', source_field='Condities_monsterafname', datatype='string'),
        WfsField(name='van', source_field='Diepte_van', datatype='float'),
        WfsField(name='tot', source_field='Diepte_tot', datatype='float'),
        WfsField(name='labo', source_field='Labo', datatype='string'),
        XmlField(name='laboreferentie',
                 source_xpath='/bodemmonster/laboreferentie',
                 definition='Referentie laboverslag.',
                 datatype='string'),
        XmlField(name='opmerking',
                 source_xpath='/bodemmonster/opmerking',
                 definition='Opmerking aan het bodemmonster.',
                 datatype='string')
    ]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Bodemmonster, being a URI of the form
            `https://www.dov.vlaanderen.be/data/bodemmonster/<id>`.

        """
        super(Bodemmonster, self).__init__('bodemmonster', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        b = cls(feature.findtext('./{{{}}}Bodemmonsterfiche'.format(namespace)))

        for field in cls.get_fields(source=('wfs',)).values():
            b.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return b
