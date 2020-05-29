# -*- coding: utf-8 -*-
"""Module containing the DOV data types for interpretations, including
subtypes."""
import numpy as np

from pydov.types.abstract import AbstractDovSubType, AbstractDovType
from pydov.types.fields import WfsField, XmlField, XsdType, _CustomField
from pydov.util.dovutil import build_dov_url


class AbstractCommonInterpretatie(AbstractDovType):
    """Abstract base class for interpretations that can be linked to
    boreholes or cone penetration tests."""

    fields = [
        WfsField(name='pkey_interpretatie',
                 source_field='Interpretatiefiche', datatype='string'),
        _CustomField(name='pkey_boring',
                     definition='URL die verwijst naar de gegevens van de '
                                'boring waaraan deze informele stratigrafie '
                                'gekoppeld is (indien gekoppeld aan een '
                                'boring).',
                     datatype='string'),
        _CustomField(name='pkey_sondering',
                     definition='URL die verwijst naar de gegevens van de '
                                'sondering waaraan deze informele '
                                'stratigrafie gekoppeld is (indien gekoppeld '
                                'aan een sondering).',
                     datatype='string'),
        WfsField(name='betrouwbaarheid_interpretatie',
                 source_field='Betrouwbaarheid', datatype='string'),
        WfsField(name='x', source_field='X_mL72', datatype='float'),
        WfsField(name='y', source_field='Y_mL72', datatype='float')
    ]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Interpretatie (interpretations), being a
            URI of the form
            `https://www.dov.vlaanderen.be/data/interpretatie/<id>`.

        """
        super(AbstractCommonInterpretatie, self).__init__(
            'interpretatie', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        instance = cls(
            feature.findtext('./{{{}}}Interpretatiefiche'.format(namespace)))

        typeproef = cls._parse(
            func=feature.findtext,
            xpath='Type_proef',
            namespace=namespace,
            returntype='string'
        )

        if typeproef == 'Boring':
            instance.data['pkey_boring'] = cls._parse(
                func=feature.findtext,
                xpath='Proeffiche',
                namespace=namespace,
                returntype='string'
            )
            instance.data['pkey_sondering'] = np.nan
        elif typeproef == 'Sondering':
            instance.data['pkey_sondering'] = cls._parse(
                func=feature.findtext,
                xpath='Proeffiche',
                namespace=namespace,
                returntype='string'
            )
            instance.data['pkey_boring'] = np.nan
        else:
            instance.data['pkey_boring'] = np.nan
            instance.data['pkey_sondering'] = np.nan

        for field in cls.get_fields(source=('wfs',)).values():
            if field['name'] in ['pkey_boring', 'pkey_sondering']:
                continue

            instance.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return instance


class AbstractBoringInterpretatie(AbstractDovType):
    """Abstract base class for interpretations that are linked to boreholes
    only."""

    fields = [
        WfsField(name='pkey_interpretatie',
                 source_field='Interpretatiefiche', datatype='string'),
        WfsField(name='pkey_boring', source_field='Proeffiche',
                 datatype='string'),
        WfsField(name='betrouwbaarheid_interpretatie',
                 source_field='Betrouwbaarheid', datatype='string'),
        WfsField(name='x', source_field='X_mL72', datatype='float'),
        WfsField(name='y', source_field='Y_mL72', datatype='float')
    ]

    def __init__(self, pkey):
        """Initialisation.

        Parameters
        ----------
        pkey : str
            Permanent key of the Interpretatie (interpretations), being a
            URI of the form
            `https://www.dov.vlaanderen.be/data/interpretatie/<id>`.

        """
        super(AbstractBoringInterpretatie, self).__init__(
            'interpretatie', pkey)

    @classmethod
    def from_wfs_element(cls, feature, namespace):
        instance = cls(
            feature.findtext('./{{{}}}Interpretatiefiche'.format(namespace)))

        for field in cls.get_fields(source=('wfs',)).values():
            instance.data[field['name']] = cls._parse(
                func=feature.findtext,
                xpath=field['sourcefield'],
                namespace=namespace,
                returntype=field.get('type', None)
            )

        return instance


class InformeleStratigrafieLaag(AbstractDovSubType):

    rootpath = './/informelestratigrafie/laag'

    fields = [
        XmlField(name='diepte_laag_van',
                 source_xpath='/van',
                 definition='Diepte van de bovenkant van de laag informele '
                            'stratigrafie in meter.',
                 datatype='float'),
        XmlField(name='diepte_laag_tot',
                 source_xpath='/tot',
                 definition='Diepte van de onderkant van de laag informele '
                            'stratigrafie in meter.',
                 datatype='float'),
        XmlField(name='beschrijving',
                 source_xpath='/beschrijving',
                 definition='Benoeming van de eenheid van de laag informele '
                            'stratigrafie in vrije tekst (onbeperkt in '
                            'lengte).',
                 datatype='string')
    ]


class InformeleStratigrafie(AbstractCommonInterpretatie):
    """Class representing the DOV data type for 'informele stratigrafie'
    interpretations."""

    subtypes = [InformeleStratigrafieLaag]


class FormeleStratigrafieLaag(AbstractDovSubType):

    rootpath = './/formelestratigrafie/laag'

    fields = [
        XmlField(name='diepte_laag_van',
                 source_xpath='/van',
                 definition='Diepte van de bovenkant van de laag Formele '
                            'stratigrafie in meter.',
                 datatype='float'),
        XmlField(name='diepte_laag_tot',
                 source_xpath='/tot',
                 definition='Diepte van de onderkant van de laag Formele '
                            'stratigrafie in meter.',
                 datatype='float'),
        XmlField(name='lid1',
                 source_xpath='/lid1',
                 definition='eerste eenheid van de laag formele stratigrafie',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=build_dov_url(
                         'xdov/schema/latest/xsd/kern/interpretatie/'
                         'FormeleStratigrafieDataCodes.xsd'),
                     typename='FormeleStratigrafieLedenEnumType')),
        XmlField(name='relatie_lid1_lid2',
                 source_xpath='/relatie_lid1_lid2',
                 definition='verbinding/relatie tussen lid1 en lid2 van de '
                            'laag formele stratigrafie',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=build_dov_url(
                         'xdov/schema/latest/xsd/kern/interpretatie/'
                         'InterpretatieDataCodes.xsd'),
                     typename='RelatieLedenEnumType')),
        XmlField(name='lid2',
                 source_xpath='/lid2',
                 definition='tweede eenheid van de laag formele stratigrafie. '
                      'Indien niet ingevuld wordt default de waarde van lid1 '
                      'ingevuld',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=build_dov_url(
                         'xdov/schema/latest/xsd/kern/interpretatie/'
                         'FormeleStratigrafieDataCodes.xsd'),
                     typename='FormeleStratigrafieLedenEnumType'))
    ]


class FormeleStratigrafie(AbstractCommonInterpretatie):
    """Class representing the DOV data type for 'Formele stratigrafie'
    interpretations."""

    subtypes = [FormeleStratigrafieLaag]


class HydrogeologischeStratigrafieLaag(AbstractDovSubType):

    rootpath = './/hydrogeologischeinterpretatie/laag'

    fields = [
        XmlField(name='diepte_laag_van',
                 source_xpath='/van',
                 definition='Diepte van de bovenkant van de laag '
                            'hydrogeologische stratigrafie in meter.',
                 datatype='float'),
        XmlField(name='diepte_laag_tot',
                 source_xpath='/tot',
                 definition='Diepte van de onderkant van de laag '
                            'hydrogeologische stratigrafie in meter.',
                 datatype='float'),
        XmlField(name='aquifer',
                 source_xpath='/aquifer',
                 definition='code van de watervoerende laag waarin de laag '
                            'Hydrogeologische stratigrafie zich bevindt.',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=build_dov_url(
                         'xdov/schema/latest/xsd/kern/interpretatie/'
                         'HydrogeologischeStratigrafieDataCodes.xsd'),
                     typename='AquiferEnumType'
                 ))
    ]


class HydrogeologischeStratigrafie(AbstractBoringInterpretatie):
    """Class representing the DOV data type for 'hydrogeologische
    stratigrafie' interpretations."""

    subtypes = [HydrogeologischeStratigrafieLaag]


class LithologischeBeschrijvingLaag(AbstractDovSubType):

    rootpath = './/lithologischebeschrijving/laag'

    fields = [
        XmlField(name='diepte_laag_van',
                 source_xpath='/van',
                 definition='Diepte van de bovenkant van de laag '
                            'lithologische beschrijving in meter.',
                 datatype='float'),
        XmlField(name='diepte_laag_tot',
                 source_xpath='/tot',
                 definition='Diepte van de onderkant van de laag '
                            'lithologische beschrijving in meter.',
                 datatype='float'),
        XmlField(name='beschrijving',
                 source_xpath='/beschrijving',
                 definition='Lithologische beschrijving van de laag in vrije '
                            'tekst (onbeperkt in lengte)',
                 datatype='string')
    ]


class LithologischeBeschrijvingen(AbstractBoringInterpretatie):
    """Class representing the DOV data type for 'lithologische
    beschrijvingen' interpretations."""

    subtypes = [LithologischeBeschrijvingLaag]


class GecodeerdeLithologieLaag(AbstractDovSubType):

    rootpath = './/gecodeerdelithologie/laag'

    __gecodeerdHoofdnaamCodesEnumType = XsdType(
        xsd_schema=build_dov_url('xdov/schema/latest/xsd/kern/interpretatie/'
                                 'GecodeerdeLithologieDataCodes.xsd'),
        typename='GecodeerdHoofdnaamCodesEnumType'
    )

    __gecodeerdBijmengingHoeveelheidEnumType = XsdType(
        xsd_schema=build_dov_url(
            'xdov/schema/latest/xsd/kern/interpretatie/'
            'GecodeerdeLithologieDataCodes.xsd'),
        typename='GecodeerdBijmengingHoeveelheidEnumType'
    )

    fields = [
        XmlField(name='diepte_laag_van',
                 source_xpath='/van',
                 definition='Diepte van de bovenkant van de laag '
                            'gecodeerde lithologie in meter.',
                 datatype='float'),
        XmlField(name='diepte_laag_tot',
                 source_xpath='/tot',
                 definition='Diepte van de onderkant van de laag '
                            'gecodeerde lithologie in meter.',
                 datatype='float'),
        XmlField(name='hoofdnaam1_grondsoort',
                 source_xpath='/hoofdnaam[1]/grondsoort',
                 definition='Primaire grondsoort (als code) van de laag '
                            'gecodeerde lithologie',
                 datatype='string',
                 xsd_type=__gecodeerdHoofdnaamCodesEnumType),
        XmlField(name='hoofdnaam2_grondsoort',
                 source_xpath='/hoofdnaam[2]/grondsoort',
                 definition='Secundaire grondsoort (als code) van de laag '
                            'gecodeerde lithologie',
                 datatype='string',
                 xsd_type=__gecodeerdHoofdnaamCodesEnumType),
        XmlField(name='bijmenging1_plaatselijk',
                 source_xpath='/bijmenging[1]/plaatselijk',
                 definition='plaatselijk of niet-plaatselijk',
                 datatype='boolean'),
        XmlField(name='bijmenging1_hoeveelheid',
                 source_xpath='/bijmenging[1]/hoeveelheid',
                 definition='aanduiding van de hoeveelheid bijmenging',
                 datatype='string',
                 xsd_type=__gecodeerdBijmengingHoeveelheidEnumType),
        XmlField(name='bijmenging1_grondsoort',
                 source_xpath='/bijmenging[1]/grondsoort',
                 definition='type grondsoort (als code) van de laag '
                            'gecodeerde lithologie of geotechnische codering',
                 datatype='string',
                 xsd_type=__gecodeerdHoofdnaamCodesEnumType),
        XmlField(name='bijmenging2_plaatselijk',
                 source_xpath='/bijmenging[2]/plaatselijk',
                 definition='plaatselijk of niet-plaatselijk',
                 datatype='boolean'),
        XmlField(name='bijmenging2_hoeveelheid',
                 source_xpath='/bijmenging[2]/hoeveelheid',
                 definition='aanduiding van de hoeveelheid bijmenging',
                 datatype='string',
                 xsd_type=__gecodeerdBijmengingHoeveelheidEnumType),
        XmlField(name='bijmenging2_grondsoort',
                 source_xpath='/bijmenging[2]/grondsoort',
                 definition='type grondsoort (als code) van de laag '
                            'gecodeerde lithologie of geotechnische codering',
                 datatype='string',
                 xsd_type=__gecodeerdHoofdnaamCodesEnumType),
        XmlField(name='bijmenging3_plaatselijk',
                 source_xpath='/bijmenging[3]/plaatselijk',
                 definition='plaatselijk of niet-plaatselijk',
                 datatype='boolean'),
        XmlField(name='bijmenging3_hoeveelheid',
                 source_xpath='/bijmenging[3]/hoeveelheid',
                 definition='aanduiding van de hoeveelheid bijmenging',
                 datatype='string',
                 xsd_type=__gecodeerdBijmengingHoeveelheidEnumType),
        XmlField(name='bijmenging3_grondsoort',
                 source_xpath='/bijmenging[3]/grondsoort',
                 definition='type grondsoort (als code) van de laag '
                            'gecodeerde lithologie of geotechnische codering',
                 datatype='string',
                 xsd_type=__gecodeerdHoofdnaamCodesEnumType)
    ]


class GecodeerdeLithologie(AbstractBoringInterpretatie):
    """Class representing the DOV data type for 'gecodeerde
    lithologie' interpretations."""

    subtypes = [GecodeerdeLithologieLaag]


class GeotechnischeCoderingLaag(AbstractDovSubType):

    rootpath = './/geotechnischecodering/laag'

    __geotechnischeCoderingHoofdnaamCodesEnumType = XsdType(
        xsd_schema=build_dov_url(
            'xdov/schema/latest/xsd/kern/interpretatie/'
            'GeotechnischeCoderingDataCodes.xsd'),
        typename='GeotechnischeCoderingHoofdnaamCodesEnumType'
    )

    __gtCoderingBijmengingHoeveelheidEnumType = XsdType(
        xsd_schema=build_dov_url(
            'xdov/schema/latest/xsd/kern/interpretatie/'
            'GeotechnischeCoderingDataCodes.xsd'),
        typename='GeotechnischeCoderingBijmengingHoeveelheidEnumType'
    )

    fields = [
        XmlField(name='diepte_laag_van',
                 source_xpath='/van',
                 definition='Diepte van de bovenkant van de laag '
                            'geotechnische codering in meter.',
                 datatype='float'),
        XmlField(name='diepte_laag_tot',
                 source_xpath='/tot',
                 definition='Diepte van de onderkant van de laag '
                            'geotechnische codering in meter.',
                 datatype='float'),
        XmlField(name='hoofdnaam1_grondsoort',
                 source_xpath='/hoofdnaam[1]/grondsoort',
                 definition='hoofdnaam (als code) van de laag geotechnische '
                            'codering',
                 datatype='string',
                 xsd_type=__geotechnischeCoderingHoofdnaamCodesEnumType),
        XmlField(name='hoofdnaam2_grondsoort',
                 source_xpath='/hoofdnaam[2]/grondsoort',
                 definition='Secundaire grondsoort (als code) van de laag '
                            'geotechnische codering',
                 datatype='string',
                 xsd_type=__geotechnischeCoderingHoofdnaamCodesEnumType),
        XmlField(name='bijmenging1_plaatselijk',
                 source_xpath='/bijmenging[1]/plaatselijk',
                 definition='plaatselijk of niet-plaatselijk',
                 datatype='boolean'),
        XmlField(name='bijmenging1_hoeveelheid',
                 source_xpath='/bijmenging[1]/hoeveelheid',
                 definition='aanduiding van de hoeveelheid bijmenging',
                 datatype='string',
                 xsd_type=__gtCoderingBijmengingHoeveelheidEnumType),
        XmlField(name='bijmenging1_grondsoort',
                 source_xpath='/bijmenging[1]/grondsoort',
                 definition='type grondsoort (als code) van de laag '
                            'geotechnische codering',
                 datatype='string',
                 xsd_type=__geotechnischeCoderingHoofdnaamCodesEnumType),
        XmlField(name='bijmenging2_plaatselijk',
                 source_xpath='/bijmenging[2]/plaatselijk',
                 definition='plaatselijk of niet-plaatselijk',
                 datatype='boolean'),
        XmlField(name='bijmenging2_hoeveelheid',
                 source_xpath='/bijmenging[2]/hoeveelheid',
                 definition='aanduiding van de hoeveelheid bijmenging',
                 datatype='string',
                 xsd_type=__gtCoderingBijmengingHoeveelheidEnumType),
        XmlField(name='bijmenging2_grondsoort',
                 source_xpath='/bijmenging[2]/grondsoort',
                 definition='type grondsoort (als code) van de laag '
                            'geotechnische codering',
                 datatype='string',
                 xsd_type=__geotechnischeCoderingHoofdnaamCodesEnumType),
        XmlField(name='bijmenging3_plaatselijk',
                 source_xpath='/bijmenging[3]/plaatselijk',
                 definition='plaatselijk of niet-plaatselijk',
                 datatype='boolean'),
        XmlField(name='bijmenging3_hoeveelheid',
                 source_xpath='/bijmenging[3]/hoeveelheid',
                 definition='aanduiding van de hoeveelheid bijmenging',
                 datatype='string',
                 xsd_type=__gtCoderingBijmengingHoeveelheidEnumType),
        XmlField(name='bijmenging3_grondsoort',
                 source_xpath='/bijmenging[3]/grondsoort',
                 definition='type grondsoort (als code) van de laag '
                            'geotechnische codering',
                 datatype='string',
                 xsd_type=__geotechnischeCoderingHoofdnaamCodesEnumType)
    ]


class GeotechnischeCodering(AbstractBoringInterpretatie):
    """Class representing the DOV data type for 'geotechnische
    codering' interpretations."""

    subtypes = [GeotechnischeCoderingLaag]


class QuartairStratigrafieLaag(AbstractDovSubType):

    rootpath = './/quartairstratigrafie/laag'

    fields = [
        XmlField(name='diepte_laag_van',
                 source_xpath='/van',
                 definition='diepte van de bovenkant van de laag '
                            'quartairstratigrafie in meter',
                 datatype='float'),
        XmlField(name='diepte_laag_tot',
                 source_xpath='/tot',
                 definition='diepte van de onderkant van de laag '
                            'quartairstratigrafie in meter',
                 datatype='float'),
        XmlField(name='lid1',
                 source_xpath='/lid1',
                 definition='eerste eenheid van de laag quartairstratigrafie',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=build_dov_url(
                         'xdov/schema/latest/xsd/kern/interpretatie/'
                         'QuartairStratigrafieDataCodes.xsd'),
                     typename='QuartairStratigrafieLedenEnumType')),
        XmlField(name='relatie_lid1_lid2',
                 source_xpath='/relatie_lid1_lid2',
                 definition='verbinding of relatie tussen lid1 en lid2 van de '
                            'laag quartairstratigrafie',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=build_dov_url(
                         'xdov/schema/latest/xsd/kern/interpretatie/'
                         'InterpretatieDataCodes.xsd'),
                     typename='RelatieLedenEnumType')),
        XmlField(name='lid2',
                 source_xpath='/lid2',
                 definition='tweede eenheid van de laag quartairstratigrafie. '
                      'Indien niet ingevuld wordt default dezelfde waarde '
                      'als voor Lid1 ingevuld',
                 datatype='string',
                 xsd_type=XsdType(
                     xsd_schema=build_dov_url(
                         'xdov/schema/latest/xsd/kern/interpretatie/'
                         'QuartairStratigrafieDataCodes.xsd'),
                     typename='QuartairStratigrafieLedenEnumType'))
    ]


class QuartairStratigrafie(AbstractBoringInterpretatie):
    """Class representing the DOV data type for 'Quartairstratigrafie'
    interpretations."""

    subtypes = [QuartairStratigrafieLaag]


class InformeleHydrogeologischeStratigrafieLaag(AbstractDovSubType):

    rootpath = './/informelehydrostratigrafie/laag'

    fields = [
        XmlField(name='diepte_laag_van',
                 source_xpath='/van',
                 definition='Diepte van de bovenkant van de laag informele '
                            'hydrostratigrafie in meter.',
                 datatype='float'),
        XmlField(name='diepte_laag_tot',
                 source_xpath='/tot',
                 definition='Diepte van de onderkant van de laag informele '
                            'hydrostratigrafie in meter.',
                 datatype='float'),
        XmlField(name='beschrijving',
                 source_xpath='/beschrijving',
                 definition='Benoeming van de eenheid van de laag informele '
                            'hydrostratigrafie in vrije tekst (onbeperkt in '
                            'lengte).',
                 datatype='string')
    ]


class InformeleHydrogeologischeStratigrafie(AbstractBoringInterpretatie):
    """Class representing the DOV data type for 'informele stratigrafie'
    interpretations."""

    subtypes = [InformeleHydrogeologischeStratigrafieLaag]
