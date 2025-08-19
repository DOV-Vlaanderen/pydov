"""Module grouping tests for the pydov.types.observatie module."""

from pydov.types.observatie import Observatie, Meetreeks, NumeriekTekstField
from pydov.types.fields import ReturnFieldList
from pydov.util.dovutil import build_dov_url
from tests.abstract import AbstractTestTypes

from owslib.etree import etree

location_wfs_getfeature = 'tests/data/types/observatie/wfsgetfeature.xml'
location_wfs_feature = 'tests/data/types/observatie/feature.xml'
location_dov_xml = 'tests/data/types/observatie/observatie.xml'


class TestObservatie(AbstractTestTypes):
    """Class grouping tests for the pydov.types.observatie.Observatie class."""

    datatype_class = Observatie
    namespace = 'http://dov.vlaanderen.be/ocdov/monster'
    pkey_base = build_dov_url('data/observatie/')

    sorted_subtypes = ['Fractiemeting', 'Meetreeks', 'ObservatieHerhaling','SecundaireParameter']
    sorted_fieldsets = ['ObservatieDetails']

    field_names = ['pkey_observatie', 'pkey_parent', 'fenomeentijd', 'diepte_van_m', 'diepte_tot_m', 'parametergroep',
                   'parameter', 'detectieconditie', 'resultaat', 'eenheid', 'methode', 'uitvoerder', 'herkomst']
    field_names_subtypes = []
    field_names_nosubtypes = ['pkey_observatie', 'pkey_parent', 'fenomeentijd', 'diepte_van_m', 'diepte_tot_m',
                              'parametergroep', 'parameter', 'detectieconditie', 'resultaat', 'eenheid', 'methode',
                              'uitvoerder', 'herkomst']

    valid_returnfields = ReturnFieldList.from_field_names(
        'pkey_observatie', 'diepte_van_m')
    valid_returnfields_subtype = ReturnFieldList.from_field_names()
    inexistent_field = 'onbestaand'


class TestMeetreeks:
    """Class grouping tests for the pydov.types.observatie.Meetreeks class."""

    def test_get_field_names(self):
        """Test if the field names of the Meetreeks subtype are correct."""

        assert Meetreeks.get_field_names() == Meetreeks._preferred_field_order

    def test_get_fields(self):
        """Test if the fields of the Meetreeks subtype are correct."""

        assert list(
            Meetreeks.get_fields().keys()) == Meetreeks._preferred_field_order


class TestNumeriekTekstField:
    """Class grouping tests for the pydov.types.observatie.NumeriekTekstField class."""

    def test_calculate_numeriek(self):
        """Test if the NumeriekTekstField calculates the correct value from XML for numeric values."""

        meetwaarde_field = NumeriekTekstField(
            name='meetwaarde',
            definition='Test field Meetwaarde',
            basename='meetwaarde')

        meetpunt_field = NumeriekTekstField(
            name='meetpunt',
            definition='Test field Meetpunt',
            basename='meetpunt')

        xml_tree = etree.fromstring(
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
               <ns4:dov-schema xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns4="http://kern.schemas.dov.vlaanderen.be" xsi:schemaLocation="http://kern.schemas.dov.vlaanderen.be https://www.dov.vlaanderen.be/xdov/schema/latest/xsd/kern/dov.xsd">
                   <observatie>
                       <identificator>
                           <identificator>2025-43568400</identificator>
                           <toegekend_door>DOV</toegekend_door>
                       </identificator>
                       <geobserveerd_object>
                           <objecttype>monster</objecttype>
                           <naam>B1M1</naam>
                           <permkey>2025-385918</permkey>
                       </geobserveerd_object>
                       <diepte_van>17.0</diepte_van>
                       <diepte_tot>19.0</diepte_tot>
                       <parameter>Korrelverdeling d.m.v. laserdiffractie</parameter>
                       <parametergroep>Onderkenningsproeven-korrelverdeling </parametergroep>
                       <waarde_meetreeks>
                           <meetpuntparameter>Diameter</meetpuntparameter>
                           <meetpuntparameter_eenheid>mm</meetpuntparameter_eenheid>
                           <meetwaardeparameter>Fractie met grotere diameter</meetwaardeparameter>
                           <meetwaardeparameter_eenheid>%</meetwaardeparameter_eenheid>
                           <meetreekswaarde>
                               <meetwaarde_numeriek>99.99</meetwaarde_numeriek>
                               <meetpunt_numeriek>4.4E-5</meetpunt_numeriek>
                           </meetreekswaarde>
                        </waarde_meetreeks>
                     </observatie>
                </ns4:dov-schema>""".encode('utf8'))

        assert meetpunt_field.calculate(Meetreeks, xml_tree) == '4.4E-5'
        assert meetwaarde_field.calculate(Meetreeks, xml_tree) == '99.99'

    def test_calculate_text(self):
        """Test if the NumeriekTekstField calculates the correct value from XML for text values."""

        meetwaarde_field = NumeriekTekstField(
            name='meetwaarde',
            definition='Test field Meetwaarde',
            basename='meetwaarde')

        meetpunt_field = NumeriekTekstField(
            name='meetpunt',
            definition='Test field Meetpunt',
            basename='meetpunt')

        xml_tree = etree.fromstring(
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
               <ns4:dov-schema xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns4="http://kern.schemas.dov.vlaanderen.be" xsi:schemaLocation="http://kern.schemas.dov.vlaanderen.be https://www.dov.vlaanderen.be/xdov/schema/latest/xsd/kern/dov.xsd">
                   <observatie>
                       <identificator>
                           <identificator>2025-43568400</identificator>
                           <toegekend_door>DOV</toegekend_door>
                       </identificator>
                       <geobserveerd_object>
                           <objecttype>monster</objecttype>
                           <naam>B1M1</naam>
                           <permkey>2025-385918</permkey>
                       </geobserveerd_object>
                       <diepte_van>17.0</diepte_van>
                       <diepte_tot>19.0</diepte_tot>
                       <parameter>Korrelverdeling d.m.v. laserdiffractie</parameter>
                       <parametergroep>Onderkenningsproeven-korrelverdeling </parametergroep>
                       <waarde_meetreeks>
                           <meetpuntparameter>Diameter</meetpuntparameter>
                           <meetpuntparameter_eenheid>mm</meetpuntparameter_eenheid>
                           <meetwaardeparameter>Fractie met grotere diameter</meetwaardeparameter>
                           <meetwaardeparameter_eenheid>%</meetwaardeparameter_eenheid>
                           <meetreekswaarde>
                               <meetwaarde_text>meetwaarde: 99.99</meetwaarde_text>
                               <meetpunt_text>meetpunt: 4.4E-5</meetpunt_text>
                           </meetreekswaarde>
                        </waarde_meetreeks>
                     </observatie>
                </ns4:dov-schema>""".encode('utf8'))

        assert meetpunt_field.calculate(
            Meetreeks, xml_tree) == 'meetpunt: 4.4E-5'
        assert meetwaarde_field.calculate(
            Meetreeks, xml_tree) == 'meetwaarde: 99.99'
