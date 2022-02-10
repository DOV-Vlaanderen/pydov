# -*- coding: utf-8 -*-
"""Module containing the DOV data type for bodemclassificatie."""
from pydov.types.fields import WfsField
from .abstract import AbstractDovType


class Bodemclassificatie(AbstractDovType):
    """Class representing the DOV data type for bodemclassificaties."""

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
        WfsField(name='classificatietype',
                 source_field='Classificatietype', datatype='string'),
        WfsField(name='bodemtype', source_field='Bodemtype',
                 datatype='string'),
        WfsField(name='auteurs', source_field='Auteurs', datatype='string')
    ]

    pkey_fieldname = 'Bodemclassificatiefiche'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Bodemclassificatie, being a URI of the form
            `https://www.dov.vlaanderen.be/data/**classificatie/<id>`.

        """
        super().__init__('bodemclassificatie', pkey)
