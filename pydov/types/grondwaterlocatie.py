# -*- coding: utf-8 -*-
"""Module containing the DOV data type for screens (Filter), including
subtypes."""
from pydov.types.fields import (
    WfsField,
    XmlField,
)
from .abstract import (
    AbstractDovType,
    AbstractDovSubType,
)


class Beheerder(AbstractDovSubType):

    rootpath = './/grondwaterlocatie/beheer'

    fields = [
        XmlField(name='beheerder_vanaf',
                 source_xpath='/vanaf',
                 datatype='date',
                 definition='Datum vanaf wanneer de grondwaterlocatie in '
                            'beheer is bij deze beheerder.'),
        XmlField(name='beheerder_tot',
                 source_xpath='/tot',
                 datatype='date',
                 definition='Datum tot wanneer de grondwaterlocatie in '
                            'beheer is bij deze beheerder. Blijft leeg als '
                            'deze beheerder de huidige beheerder is.'),
        XmlField(name='beheerder',
                 source_xpath='/beheerder/naam',
                 datatype='string',
                 definition='De beheerder van de grondwaterlocatie in het '
                            'opgegeven interval.')
    ]


class GrondwaterLocatie(AbstractDovType):
    """Class representing the DOV data type for Groundwater screens."""

    subtypes = [Beheerder]

    fields = [
        WfsField(name='pkey_grondwaterlocatie', source_field='putfiche',
                 datatype='string'),
        WfsField(name='gw_id', source_field='GW_ID', datatype='string'),
        WfsField(name='x', source_field='X_mL72', datatype='float'),
        WfsField(name='y', source_field='Y_mL72', datatype='float'),
        XmlField(name='mv_mtaw',
                 source_xpath='/grondwaterlocatie/puntligging'
                              '/oorspronkelijk_maaiveld/waarde',
                 definition='Maaiveldhoogte in mTAW op dag dat de '
                            'grondwaterlocatie aangemaakt werd.',
                 datatype='float'),
        WfsField(name='start_grondwaterlocatie_mtaw', source_field='Z_mTAW',
                 datatype='float'),
        WfsField(name='gemeente', source_field='gemeente', datatype='string')
    ]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Filter (screen), being a URI of the form
            `https://www.dov.vlaanderen.be/data/filter/<id>`.

        """
        super(GrondwaterLocatie, self).__init__('put', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        """Build `GrondwaterFilter` instance from a WFS feature element.

        Parameters
        ----------
        feature : etree.Element
            XML element representing a single record of the WFS layer.
        namespace : str
            Namespace associated with this WFS featuretype.

        Returns
        -------
        filter : GrondwaterFilter
            An instance of this class populated with the data from the WFS
            element.

        """
        gwlocatie = cls(
            feature.findtext('./{{{}}}putfiche'.format(namespace)))

        for field in cls.get_fields(source=('wfs',)).values():
            gwlocatie.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return gwlocatie
