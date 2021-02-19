# -*- coding: utf-8 -*-
"""Module containing the DOV data type for bodemsites, including
subtypes."""
from pydov.types.fields import WfsField, XmlField

from .abstract import AbstractDovType


class Bodemsite(AbstractDovType):
    """Class representing the DOV data type for bodemsites."""

    subtypes = []

    fields = [
        WfsField(name='pkey_bodemsite', source_field='Bodemsitefiche',
                 datatype='string'),
        WfsField(name='naam', source_field='Naam', datatype='string'),
        WfsField(name='datum', source_field='Datum', datatype='date'),
        WfsField(name='beschrijving', source_field='Beschrijving',
                 datatype='string'),
        XmlField(name='waarnemingsdatum',
                 source_xpath='/bodemsite/waarnemingsdatum',
                 definition='Datum van waarneming van de bodemsite.',
                 datatype='date'),
        XmlField(name='invoerdatum',
                 source_xpath='/bodemsite/invoerdatum',
                 definition='Datum van invoer van de bodemsite.',
                 datatype='date')
    ]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Bodemsite, being a URI of the form
            `https://www.dov.vlaanderen.be/data/bodemsite/<id>`.

        """
        super(Bodemsite, self).__init__('bodemsite', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        b = cls(feature.findtext('./{{{}}}Bodemsitefiche'.format(namespace)))

        for field in cls.get_fields(source=('wfs',)).values():
            b.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return b
