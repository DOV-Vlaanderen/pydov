# -*- coding: utf-8 -*-
"""Module containing the DOV data type for CPT measurements (Sonderingen),
including subtypes."""
from pydov.types.abstract import AbstractDovSubType, AbstractDovType
from pydov.types.fields import WfsField, XmlField
from pydov.types.ligging import MvMtawField


class Meetdata(AbstractDovSubType):

    rootpath = './/sondering/sondeonderzoek/penetratietest/meetdata'

    fields = [
        XmlField(name='lengte',
                 source_xpath='/lengte',
                 definition='Geregistreerde sondeerlengte, '
                            'uitgedrukt in meter.',
                 datatype='float'),
        XmlField(name='diepte',
                 source_xpath='/diepte',
                 definition='Diepte waarop sondeerparameters geregistreerd '
                            'werden, berekend uit de sondeerlengte en de '
                            'geregistreerde hellingsmeting, '
                            'uitgedrukt in meter.',
                 datatype='float'),
        XmlField(name='qc',
                 source_xpath='/qc',
                 definition='Opgemeten waarde van de conusweerstand, '
                            'uitgedrukt in MPa.',
                 datatype='float'),
        XmlField(name='Qt',
                 source_xpath='/Qt',
                 definition='Opgemeten waarde van de totale weerstand, '
                            'uitgedrukt in kN.',
                 datatype='float'),
        XmlField(name='fs',
                 source_xpath='/fs',
                 definition='Opgemeten waarde van de plaatelijke '
                            'kleefweerstand, uitgedrukt in kPa.',
                 datatype='float'),
        XmlField(name='u',
                 source_xpath='/u',
                 definition='Opgemeten waarde van de porienwaterspanning, '
                            'uitgedrukt in kPa.',
                 datatype='float'),
        XmlField(name='i',
                 source_xpath='/i',
                 definition='Opgemeten waarde van de inclinatie, uitgedrukt '
                            'in graden.',
                 datatype='float')
    ]


class Sondering(AbstractDovType):
    """Class representing the DOV data type for CPT measurements."""

    subtypes = [Meetdata]

    fields = [
        WfsField(name='pkey_sondering', source_field='fiche',
                 datatype='string'),
        WfsField(name='sondeernummer', source_field='sondeernummer',
                 datatype='string'),
        WfsField(name='x', source_field='X_mL72', datatype='float'),
        WfsField(name='y', source_field='Y_mL72', datatype='float'),
        MvMtawField('Maaiveldhoogte in mTAW op dag dat de sondering '
                    'uitgevoerd werd.'),
        WfsField(name='start_sondering_mtaw', source_field='Z_mTAW',
                 datatype='float'),
        WfsField(name='diepte_sondering_van', source_field='diepte_van_m',
                 datatype='float'),
        WfsField(name='diepte_sondering_tot', source_field='diepte_tot_m',
                 datatype='float'),
        WfsField(name='datum_aanvang', source_field='datum_aanvang',
                 datatype='date'),
        WfsField(name='uitvoerder', source_field='uitvoerder',
                 datatype='string'),
        WfsField(name='sondeermethode', source_field='sondeermethode',
                 datatype='string'),
        WfsField(name='apparaat', source_field='apparaat_type',
                 datatype='string'),
        XmlField(name='datum_gw_meting',
                 source_xpath='/sondering/visueelonderzoek/'
                              'datumtijd_waarneming_grondwaterstand',
                 definition='Datum en tijdstip van waarneming van de '
                            'grondwaterstand.',
                 datatype='datetime'),
        XmlField(name='diepte_gw_m',
                 source_xpath='/sondering/visueelonderzoek/grondwaterstand',
                 definition='Diepte water in meter ten opzicht van het '
                            'aanvangspeil.',
                 datatype='float')
    ]

    pkey_fieldname = 'fiche'

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Sondering (CPT measurement), being a URI of
            the form `https://www.dov.vlaanderen.be/data/sondering/<id>`.

        """
        super().__init__('sondering', pkey)
