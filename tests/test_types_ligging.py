# -*- coding: utf-8 -*-
"""Module containing tests for generic fields regarding location (ligging)."""


import numpy as np
from owslib.etree import etree

from pydov.types.boring import Boring
from pydov.types.ligging import MvMtawField


class TestMvMtawField:
    def test_original_xml(self):
        """Test whether the correct mv_mtaw value is returned for the original XML schema."""
        mv_mtaw_field = MvMtawField('Maaiveldhoogte in mTAW op dag dat de boring uitgevoerd werd.')

        boring_tree = etree.fromstring(
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <ns4:dov-schema xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns4="http://kern.schemas.dov.vlaanderen.be" xsi:schemaLocation="http://kern.schemas.dov.vlaanderen.be https://www.dov.vlaanderen.be/xdov/schema/latest/xsd/kern/dov.xsd">
                    <boring>
                        <identificatie>kb29d84e-B574</identificatie>
                        <dataidentifier>
                            <permkey>2016-122561</permkey>
                            <uri>https://oefen.dov.vlaanderen.be/data/boring/2016-122561</uri>
                        </dataidentifier>
                        <xy>
                            <x>92424.00</x>
                            <y>170752.00</y>
                            <betrouwbaarheid>onbekend</betrouwbaarheid>
                            <methode_opmeten>gedigitaliseerd op topokaart</methode_opmeten>
                            <origine_opmeten>
                                <naam>Universiteit Gent</naam>
                            </origine_opmeten>
                        </xy>
                        <gemeente>45061</gemeente>
                        <oorspronkelijk_maaiveld>
                            <waarde>40.00</waarde>
                            <betrouwbaarheid>onbekend</betrouwbaarheid>
                            <methode_opmeten>afgeleid van topokaart</methode_opmeten>
                            <origine_opmeten>
                                <naam>Universiteit Gent</naam>
                            </origine_opmeten>
                        </oorspronkelijk_maaiveld>
                        <start_tov_maaiveld>
                            <gestart_op>MAAIVELD</gestart_op>
                        </start_tov_maaiveld>
                        <diepte_van>0.00</diepte_van>
                        <diepte_tot>0.00</diepte_tot>
                        <wet_kader>
                            <niet_ingedeeld/>
                        </wet_kader>
                        <uitvoerder>
                            <naam>onbekend</naam>
                        </uitvoerder>
                        <opdrachtgever>
                            <naam>onbekend</naam>
                        </opdrachtgever>
                        <dataleverancier>
                            <naam>onbekend</naam>
                        </dataleverancier>
                        <boorgatmeting>
                            <uitgevoerd>false</uitgevoerd>
                        </boorgatmeting>
                        <stalen>
                            <bewaard>false</bewaard>
                        </stalen>
                        <details>
                            <boormethode>
                                <van>0.00</van>
                                <tot>0.00</tot>
                                <methode>onbekend</methode>
                            </boormethode>
                        </details>
                    </boring>
                </ns4:dov-schema>""".encode('utf8'))

        mv_mtaw = mv_mtaw_field.calculate(Boring, boring_tree)
        assert mv_mtaw == 40.0

    def test_new_xml_maaiveld(self):
        """Test whether the correct mv_mtaw value is returned for the new XML schema."""
        mv_mtaw_field = MvMtawField('Maaiveldhoogte in mTAW op dag dat de boring uitgevoerd werd.')

        boring_tree = etree.fromstring(
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <ns4:dov-schema xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns4="http://kern.schemas.dov.vlaanderen.be" xsi:schemaLocation="http://kern.schemas.dov.vlaanderen.be https://www.dov.vlaanderen.be/xdov/schema/latest/xsd/kern/dov.xsd">
                    <boring>
                        <identificatie>kb29d84e-B574</identificatie>
                        <dataidentifier>
                            <permkey>2016-122561</permkey>
                            <uri>https://ontwikkel.dov.vlaanderen.be/data/boring/2016-122561</uri>
                        </dataidentifier>
                        <ligging>
                            <gml:Point srsName="urn:ogc:def:crs:EPSG::6190" srsDimension="3">
                                <gml:pos>92424.0 170752.0 40.0</gml:pos>
                            </gml:Point>
                            <metadata_locatiebepaling>
                                <methode>gedigitaliseerd op topokaart</methode>
                                <uitvoerder>
                                    <naam>Universiteit Gent</naam>
                                </uitvoerder>
                                <betrouwbaarheid>onbekend</betrouwbaarheid>
                            </metadata_locatiebepaling>
                            <metadata_hoogtebepaling>
                                <methode>afgeleid van topokaart</methode>
                                <uitvoerder>
                                    <naam>Universiteit Gent</naam>
                                </uitvoerder>
                                <betrouwbaarheid>onbekend</betrouwbaarheid>
                                <referentiepunt_type>Maaiveld</referentiepunt_type>
                            </metadata_hoogtebepaling>
                        </ligging>
                        <diepte_van>0.00</diepte_van>
                        <diepte_tot>0.00</diepte_tot>
                        <wet_kader>
                            <niet_ingedeeld/>
                        </wet_kader>
                        <uitvoerder>
                            <naam>onbekend</naam>
                        </uitvoerder>
                        <opdrachtgever>
                            <naam>onbekend</naam>
                        </opdrachtgever>
                        <dataleverancier>
                            <naam>onbekend</naam>
                        </dataleverancier>
                        <boorgatmeting>
                            <uitgevoerd>false</uitgevoerd>
                        </boorgatmeting>
                        <stalen>
                            <bewaard>true</bewaard>
                        </stalen>
                        <details>
                            <boormethode>
                                <van>0.00</van>
                                <tot>0.00</tot>
                                <methode>onbekend</methode>
                            </boormethode>
                        </details>
                        <opdracht>CTE verzamel Opdrachtgever</opdracht>
                    </boring>
                </ns4:dov-schema>""".encode('utf8'))

        mv_mtaw = mv_mtaw_field.calculate(Boring, boring_tree)
        assert mv_mtaw == 40.0

    def test_new_xml_nomaaiveld(self):
        """Test whether NaN is returned when the reference point is not Maaiveld."""
        mv_mtaw_field = MvMtawField('Maaiveldhoogte in mTAW op dag dat de boring uitgevoerd werd.')

        boring_tree = etree.fromstring(
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <ns4:dov-schema xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns4="http://kern.schemas.dov.vlaanderen.be" xsi:schemaLocation="http://kern.schemas.dov.vlaanderen.be https://www.dov.vlaanderen.be/xdov/schema/latest/xsd/kern/dov.xsd">
                    <boring>
                        <identificatie>kb29d84e-B574</identificatie>
                        <dataidentifier>
                            <permkey>2016-122561</permkey>
                            <uri>https://ontwikkel.dov.vlaanderen.be/data/boring/2016-122561</uri>
                        </dataidentifier>
                        <ligging>
                            <gml:Point srsName="urn:ogc:def:crs:EPSG::6190" srsDimension="3">
                                <gml:pos>92424.0 170752.0 40.0</gml:pos>
                            </gml:Point>
                            <metadata_locatiebepaling>
                                <methode>gedigitaliseerd op topokaart</methode>
                                <uitvoerder>
                                    <naam>Universiteit Gent</naam>
                                </uitvoerder>
                                <betrouwbaarheid>onbekend</betrouwbaarheid>
                            </metadata_locatiebepaling>
                            <metadata_hoogtebepaling>
                                <methode>afgeleid van topokaart</methode>
                                <uitvoerder>
                                    <naam>Universiteit Gent</naam>
                                </uitvoerder>
                                <betrouwbaarheid>onbekend</betrouwbaarheid>
                                <referentiepunt_type>Aanvangspeil</referentiepunt_type>
                            </metadata_hoogtebepaling>
                        </ligging>
                        <diepte_van>0.00</diepte_van>
                        <diepte_tot>0.00</diepte_tot>
                        <wet_kader>
                            <niet_ingedeeld/>
                        </wet_kader>
                        <uitvoerder>
                            <naam>onbekend</naam>
                        </uitvoerder>
                        <opdrachtgever>
                            <naam>onbekend</naam>
                        </opdrachtgever>
                        <dataleverancier>
                            <naam>onbekend</naam>
                        </dataleverancier>
                        <boorgatmeting>
                            <uitgevoerd>false</uitgevoerd>
                        </boorgatmeting>
                        <stalen>
                            <bewaard>true</bewaard>
                        </stalen>
                        <details>
                            <boormethode>
                                <van>0.00</van>
                                <tot>0.00</tot>
                                <methode>onbekend</methode>
                            </boormethode>
                        </details>
                        <opdracht>CTE verzamel Opdrachtgever</opdracht>
                    </boring>
                </ns4:dov-schema>""".encode('utf8'))

        mv_mtaw = mv_mtaw_field.calculate(Boring, boring_tree)
        assert mv_mtaw is np.nan

    def test_new_xml_noheight(self):
        """Test whether NaN is returned when the point does not have height information."""
        mv_mtaw_field = MvMtawField('Maaiveldhoogte in mTAW op dag dat de boring uitgevoerd werd.')

        boring_tree = etree.fromstring(
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <ns4:dov-schema xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns4="http://kern.schemas.dov.vlaanderen.be" xsi:schemaLocation="http://kern.schemas.dov.vlaanderen.be https://www.dov.vlaanderen.be/xdov/schema/latest/xsd/kern/dov.xsd">
                    <boring>
                        <identificatie>kb29d84e-B574</identificatie>
                        <dataidentifier>
                            <permkey>2016-122561</permkey>
                            <uri>https://ontwikkel.dov.vlaanderen.be/data/boring/2016-122561</uri>
                        </dataidentifier>
                        <ligging>
                            <gml:Point srsName="urn:ogc:def:crs:EPSG::31370" srsDimension="2">
                                <gml:pos>92424.0 170752.0</gml:pos>
                            </gml:Point>
                            <metadata_locatiebepaling>
                                <methode>gedigitaliseerd op topokaart</methode>
                                <uitvoerder>
                                    <naam>Universiteit Gent</naam>
                                </uitvoerder>
                                <betrouwbaarheid>onbekend</betrouwbaarheid>
                            </metadata_locatiebepaling>
                            <metadata_hoogtebepaling>
                                <methode>afgeleid van topokaart</methode>
                                <uitvoerder>
                                    <naam>Universiteit Gent</naam>
                                </uitvoerder>
                                <betrouwbaarheid>onbekend</betrouwbaarheid>
                                <referentiepunt_type>Maaiveld</referentiepunt_type>
                            </metadata_hoogtebepaling>
                        </ligging>
                        <diepte_van>0.00</diepte_van>
                        <diepte_tot>0.00</diepte_tot>
                        <wet_kader>
                            <niet_ingedeeld/>
                        </wet_kader>
                        <uitvoerder>
                            <naam>onbekend</naam>
                        </uitvoerder>
                        <opdrachtgever>
                            <naam>onbekend</naam>
                        </opdrachtgever>
                        <dataleverancier>
                            <naam>onbekend</naam>
                        </dataleverancier>
                        <boorgatmeting>
                            <uitgevoerd>false</uitgevoerd>
                        </boorgatmeting>
                        <stalen>
                            <bewaard>true</bewaard>
                        </stalen>
                        <details>
                            <boormethode>
                                <van>0.00</van>
                                <tot>0.00</tot>
                                <methode>onbekend</methode>
                            </boormethode>
                        </details>
                        <opdracht>CTE verzamel Opdrachtgever</opdracht>
                    </boring>
                </ns4:dov-schema>""".encode('utf8'))

        mv_mtaw = mv_mtaw_field.calculate(Boring, boring_tree)
        assert mv_mtaw is np.nan
