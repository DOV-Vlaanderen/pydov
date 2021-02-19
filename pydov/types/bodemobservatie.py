# -*- coding: utf-8 -*-
"""Module containing the DOV data type for bodemobservaties, including
subtypes."""
from pydov.types.fields import WfsField, XmlField

from .abstract import AbstractDovType


class Bodemobservatie(AbstractDovType):
    """Class representing the DOV data type for bodemobservaties."""

    subtypes = []

    fields = [
        WfsField(name='pkey_bodemlocatie',
                 source_field='Bodemobservatiefiche',
                 datatype='string'),
        WfsField(name='parameter', source_field='Parameter',
                 datatype='string'),
        XmlField(name='parametergroep',
                 source_xpath='/bodemobservatie/parametergroep',
                 definition='Indeling van de parameter naar groep, '
                 + 'bvb anionen, kationen, .... Is indicatief.',
                 datatype='string'),
        WfsField(name='waarde', source_field='Waarde', datatype='string'),
        WfsField(name='eenheid', source_field='Eenheid', datatype='string'),
        XmlField(name='ondergrens',
                 source_xpath='/bodemobservatie/ondergrens',
                 definition='Het mogelijke minimum van de meting.',
                 datatype='float'),
        XmlField(name='bovengrens',
                 source_xpath='/bodemobservatie/bovengrens',
                 definition='Het mogelijke maximum van de meting.',
                 datatype='float'),
        WfsField(name='methode', source_field='Observatiemethode',
                 datatype='string'),
        XmlField(name='betrouwbaarheid',
                 source_xpath='/bodemobservatie/betrouwbaarheid',
                 definition='Betrouwbaarheid van de meting.',
                 datatype='string'),
        WfsField(name='veld_labo', source_field='Labo_of_veld',
                 datatype='string'),
        WfsField(name='diepte_van', source_field='Diepte_van',
                 datatype='float'),
        WfsField(name='diepte_tot', source_field='Diepte_tot',
                 datatype='float'),
        XmlField(name='observatiedatum',
                 source_xpath='/bodemobservatie/observatiedatum',
                 definition='Observatiedatum van de bodemobservatie',
                 datatype='date'),
        XmlField(name='invoerdatum',
                 source_xpath='/bodemobservatie/invoerdatum',
                 definition='Invoerdatum van de bodemobservatie.',
                 datatype='date'),
        XmlField(name='auteur',
                 source_xpath='/bodemobservatie/auteur',
                 definition='Auteur van de bodemobservatie.',
                 datatype='string')
    ]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Bodemobservatie, being a URI of the form
            `https://www.dov.vlaanderen.be/data/bodemobservatie/<id>`.

        """
        super(Bodemobservatie, self).__init__('bodemobservatie', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        b = cls(feature.findtext('./{{{}}}Bodemobservatiefiche'
                                 .format(namespace)))

        for field in cls.get_fields(source=('wfs',)).values():
            b.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return b
