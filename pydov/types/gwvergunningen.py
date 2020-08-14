# -*- coding: utf-8 -*-
"""Module containing the DOV data type for GW permits."""
from pydov.types.abstract import AbstractDovType
from pydov.types.fields import WfsField


class Gwvergunningen(AbstractDovType):
    """Class representing the DOV data type for groundwater abstraction
    permits."""

    subtypes = []

    fields = [
        WfsField(name='pkey_vergunning', source_field='id',
                 datatype='string'),
        WfsField(name='pkey_installatie', source_field='installatie',
                 datatype='string'),
        WfsField(name='x', source_field='installatie_X_mL72', datatype='float'),
        WfsField(name='y', source_field='installatie_Y_mL72', datatype='float'),
        WfsField(name='diepte', source_field='vergunde_diepte_m', datatype='float'),
        WfsField(name='exploitant_naam', source_field='exploitant_naam',
                 datatype='string'),
        WfsField(name='watnr', source_field='watnr',
                 datatype='string'),
        WfsField(name='vlaremrubriek', source_field='vlaremrubriek',
                 datatype='string'),
        WfsField(name='vergund_jaardebiet', source_field='vergund_jaardebiet',
                 datatype='float'),
        WfsField(name='vergund_dagdebiet', source_field='vergund_dagdebiet',
                 datatype='float'),
        WfsField(name='van_datum_termijn', source_field='van_datum_termijn',
                 datatype='date'),
        WfsField(name='tot_datum_termijn', source_field='tot_datum_termijn',
                 datatype='date'),
        WfsField(name='aquifer_vergunning', source_field='aquifer_vergunning',
                 datatype='string'),
        WfsField(name='inrichtingsklasse', source_field='inrichtingsklasse',
                 datatype='string'),
        WfsField(name='nacebelcode', source_field='IIOA_nacebelcode',
                 datatype='string'),
        WfsField(name='actie_waakgebied', source_field='actie_waakgebied',
                 datatype='string'),
        WfsField(name='cbbnr', source_field='exploitant_CBBnr',
                 datatype='string'),
        WfsField(name='kbonr', source_field='exploitant_KBOnr',
                 datatype='string'),
    ]

    def __init__(self, pkey=r'to_be_defined'):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Gwvergunningen (permits), being a URI
            of the form
            `https://www.dov.vlaanderen.be/data/installatie/<id>`.

        """
        super(Gwvergunningen, self).__init__('gwvergunningen', pkey=r'to_be_defined')

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        s = cls(feature.findtext('./{{{}}}fiche'.format(namespace)))

        for field in cls.get_fields(source=('wfs',)).values():
            s.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return s
