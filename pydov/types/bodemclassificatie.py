# -*- coding: utf-8 -*-
"""Module containing the DOV data type for bodemclassificatie, including
subtypes."""
from pydov.types.fields import WfsField, XmlField

from .abstract import AbstractDovType


class Bodemclassificatie(AbstractDovType):
    """Class representing the DOV data type for bodemobservaties."""

    subtypes = []

    fields = [
        WfsField(name='pkey_bodemclassificatie',
                 source_field='Bodemclassificatiefiche',
                 datatype='string'),
        WfsField(name='pkey_bodemlocatie',
                 source_field='Bodemlocatiefiche',
                 datatype='string'),
        WfsField(name='x', source_field='X_mL72', datatype='float'),
        WfsField(name='y', source_field='Y_mL72', datatype='float'),
        WfsField(name='mv_mtaw', source_field='mv_mTAW', datatype='float'),
        WfsField(name='classificatietype', source_field='Classificatietype', datatype='string'),
        WfsField(name='bodemtype', source_field='Bodemtype', datatype='string'),
        WfsField(name='auteurs', source_field='Auteurs',
                 datatype='string')
    ]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Bodemclassificatie, being a URI of the form
            `https://www.dov.vlaanderen.be/data/**classificatie/<id>`.

        """
        super(Bodemclassificatie, self).__init__('bodemclassificatie', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        b = cls(feature.findtext('./{{{}}}Bodemclassificatiefiche'
                                 .format(namespace)))

        for field in cls.get_fields(source=('wfs',)).values():
            b.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return b
