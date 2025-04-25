# -*- coding: utf-8 -*-
"""Module containing the DOV data type for observations (Observatie), including
subtypes."""
from pydov.types.fields import WfsField
from .abstract import AbstractDovType


class Observatie(AbstractDovType):
    """Class representing the DOV data type for observations."""

    subtypes = []

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
