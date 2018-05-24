Interpretations
===============

Possible interpretations are:
 * Informele stratigrafie
 * Formele stratigrafie
 * Lithologische beschrijvingen
 * Gecodeerde lithologie
 * Hydrogeologische stratigrafie
 * Informele hydrogeologische stratigrafie
 * Quartaire stratigrafie
 * Geotechnische coderingen

Below the desired attributes for each interpretation.
The new_name column represents the headers of the final dataframe.
Some elements can occur more than once, e.g. 'bijmenging' in 'Gecodeerde
lithologie' or 'Geotechnische coderingen'. All occurrences should be included
as new records in the final dataframe.
One of pkey_boring or pkey_sondering is empty, the other pointing to the source of the
interpreted data.


  .. csv-table:: Informele stratigrafie
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,Interpretatiefiche,pkey_interpretatie,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=boring,pkey_boring,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=sondering,pkey_sondering,string,https://.../2001-186513.xml
    wfs,Betrouwbaarheid,betrouwbaarheid_interpretatie,string,goed
    xml,/kern:dov-schema/interpretaties/informelestratigrafie/laag/van,diepte_laag_van,float,0.00
    xml,/kern:dov-schema/interpretaties/informelestratigrafie/laag/tot,diepte_laag_tot,float,1.74
    xml,/kern:dov-schema/interpretaties/informelestratigrafie/laag/beschrijving,beschrijving,string,Quartair

|

 .. csv-table:: Formele stratigrafie
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,Interpretatiefiche,pkey_interpretatie,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=boring,pkey_boring,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=sondering,pkey_sondering,string,https://.../2001-186513.xml
    wfs,Betrouwbaarheid,betrouwbaarheid_interpretatie,string,goed
    xml,/kern:dov-schema/interpretaties/formelestratigrafie/laag/betrouwbaarheid,betrouwbaarheid_laag,string,goed
    xml,/kern:dov-schema/interpretaties/formelestratigrafie/laag/van,diepte_laag_van,float,0.00
    xml,/kern:dov-schema/interpretaties/formelestratigrafie/laag/tot,diepte_laag_tot,float,1.75
    xml,/kern:dov-schema/interpretaties/formelestratigrafie/laag/lid1,lid1,string,Q
    xml,/kern:dov-schema/interpretaties/formelestratigrafie/laag/relatie_lid1_lid2,relatie_lid1_lid2,string,T
    xml,/kern:dov-schema/interpretaties/formelestratigrafie/laag/lid2,lid2,string,Q

|

  .. csv-table:: Lithologische beschrijvingen
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,Interpretatiefiche,pkey_interpretatie,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=boring,pkey_boring,string,https://.../2001-186513.xml
    wfs,Betrouwbaarheid,betrouwbaarheid_interpretatie,string,goed
    xml,/kern:dov-schema/interpretaties/lithologischebeschrijving/laag/van,diepte_laag_van,float,0.00
    xml,/kern:dov-schema/interpretaties/lithologischebeschrijving/laag/tot,diepte_laag_tot,float,1.75
    xml,/kern:dov-schema/interpretaties/lithologischebeschrijving/laag/beschrijving,beschrijving,string,Terre végétale sableuse

|

  .. csv-table:: Gecodeerde lithologie
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,Interpretatiefiche,pkey_interpretatie,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=boring,pkey_boring,string,https://.../2001-186513.xml
    wfs,Betrouwbaarheid,betrouwbaarheid_interpretatie,string,goed
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/van,diepte_laag_van,float,0.00
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/tot,diepte_laag_tot,float,1.75
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/hoofdnaam/grondsoort,hoofd_grondsoort,string,KL
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging/plaatselijk,bijmenging_plaatselijk,boolean,false
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging/hoeveelheid,bijmening_hoeveelheid,string,N
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging/grondsoort,bijmenging_grondsoort,string,XZ

|

  .. csv-table:: Hydrogeologische stratigrafie
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,Interpretatiefiche,pkey_interpretatie,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=boring,pkey_boring,string,https://.../2001-186513.xml
    wfs,Betrouwbaarheid,betrouwbaarheid_interpretatie,string,goed
    xml,/kern:dov-schema/interpretaties/hydrogeologischeinterpretatie/laag/van,diepte_laag_van,float,0.00
    xml,/kern:dov-schema/interpretaties/hydrogeologischeinterpretatie/laag/tot,diepte_laag_tot,float,1.75
    xml,/kern:dov-schema/interpretaties/hydrogeologischeinterpretatie/laag/aquifer,aquifer,string,0252

|

  .. csv-table:: Informele hydrogeologische stratigrafie
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,Interpretatiefiche,pkey_interpretatie,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=boring,pkey_boring,string,https://.../2001-186513.xml
    wfs,Betrouwbaarheid,betrouwbaarheid_interpretatie,string,goed
    xml,/kern:dov-schema/interpretaties/informelehydrostratigrafie/laag/van,diepte_laag_van,float,0.00
    xml,/kern:dov-schema/interpretaties/informelehydrostratigrafie/laag/tot,diepte_laag_tot,float,1.75
    xml,/kern:dov-schema/interpretaties/informelehydrostratigrafie/laag/beschrijving,beschrijving,string,Quartair

|

  .. csv-table:: Quartaire stratigrafie
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,Interpretatiefiche,pkey_interpretatie,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=boring,pkey_boring,string,https://.../2001-186513.xml
    wfs,Betrouwbaarheid,betrouwbaarheid_interpretatie,string,goed
    xml,/kern:dov-schema/interpretaties/quartairstratigrafie/laag/betrouwbaarheid,betrouwbaarheid_laag,string,goed
    xml,/kern:dov-schema/interpretaties/quartairstratigrafie/laag/van,diepte_laag_van,float,0.00
    xml,/kern:dov-schema/interpretaties/quartairstratigrafie/laag/tot,diepte_laag_tot,float,1.75
    xml,/kern:dov-schema/interpretaties/quartairstratigrafie/laag/lid1,lid1,string,F
    xml,/kern:dov-schema/interpretaties/quartairstratigrafie/laag/relatie_lid1_lid2,relatie_lid1_lid2,string,T
    xml,/kern:dov-schema/interpretaties/quartairstratigrafie/laag/lid2,lid2,string,F

|

  .. csv-table:: Geotechnische coderingen
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,Interpretatiefiche,pkey_interpretatie,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=boring,pkey_boring,string,https://.../2001-186513.xml
    wfs,Betrouwbaarheid,betrouwbaarheid_interpretatie,string,goed
    xml,/kern:dov-schema/interpretaties/geotechnischecodering/laag/van,diepte_laag_van,float,0.00
    xml,/kern:dov-schema/interpretaties/geotechnischecodering/laag/tot,diepte_laag_tot,float,1.75
    xml,/kern:dov-schema/interpretaties/geotechnischecodering/laag/hoofdnaam/grondsoort,hoofd_grondsoort,string,KL
    xml,/kern:dov-schema/interpretaties/geotechnischecodering/laag/bijmenging/plaatselijk,bijmenging_plaatselijk,boolean,false
    xml,/kern:dov-schema/interpretaties/geotechnischecodering/laag/bijmenging/hoeveelheid,bijmening_hoeveelheid,string,N
    xml,/kern:dov-schema/interpretaties/geotechnischecodering/laag/bijmenging/grondsoort,bijmenging_grondsoort,string,XZ

|

Boreholes
=========

Below the desired attributes for each borehole.
The new_name column represents the headers of the final dataframe.

The output of the boreholes can be joined with the interpretations following
the pkey_boring AND ('van' and 'tot') attributes of both dataframes. E.g.:
multiple layers are discernced 'van'/'tot' in the interpretations for in
between the 'methode_van'/'methode_tot' of the borehole:
    JOIN ON pkey_boring
    AND interpretation["van"] >= boring["methode_van"]
    AND interpretation["tot"] <= boring["methode_tot"]

In addition, not all wfs fields are included in the dataframe, but can be used
to select records from the DOV database. E.g.: 'informele_stratigrafie', 
'formele_stratigrafie', 'hydrogeologische_stratigrafie' etc. are boolean
fields available in the wfs to search on.

  .. csv-table:: Boringen
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,fiche,pkey_boring,string,https://.../2001-186513.xml
    wfs,boornummer,boornummer,string,kb15d28w-B164
    wfs,X_mL72,x,float,152301.0
    wfs,Y_mL72,y,float,211682.0
    xml,/kern:dov-schema/boring/oorspronkelijk_maaiveld/waarde,mv_mtaw,float,8.00
    wfs,Z_mTAW,start_boring_mtaw,float,8.00
    wfs,gemeente,gemeente,string,Wuustwezel
    xml,/kern:dov-schema/boring/diepte_van,diepte_boring_van,float,0.00
    wfs,diepte_tot_m,diepte_boring_tot,float,19.00
    wfs,datum_aanvang,datum_aanvang,date,1930-10-01
    wfs,uitvoerder,uitvoerder,string,Smet - Dessel
    xml,/kern:dov-schema/boring/boorgatmeting/uitgevoerd,boorgatmeting,boolean,false
    xml,/kern:dov-schema/boring/details/boormethode/van,diepte_methode_van,float,0.00
    xml,/kern:dov-schema/boring/details/boormethode/tot,diepte_methode_tot,float,19.00
    xml,/kern:dov-schema/boring/details/boormethode/methode,boormethode,string,droge boring

|

CPT data (In Dutch: sonderingen)
================================

Below the desired attributes for each CPT measurement. Two dataframes are discerned:
 * one with metadata about the measurement (location, type etc.)
 * one with actual measurement data from the xml, with the pkey to join the metadata

The new_name column represents the headers of the final dataframe.
More than one measurement can be performed, listed as a "metingWeerstand" type, i.e.:
qc, Qt, fs, u and i. All elements are by default included in the output dataframe, where
NaNs indicate that it wasn't measured.

In addition, not all wfs fields are included in the dataframe, but can be used
to select records from the DOV database. E.g.: 'informele_stratigrafie', 
'formele_stratigrafie' and 'hydrogeologische_stratigrafie' are boolean
fields available in the wfs to search on.

  .. csv-table:: Sonderingen metadata
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,fiche,pkey_sondering,string,https://.../2011-009205.xml
    wfs,sondeernummer,sondeernummer,string,GEO-10/139-S113
    wfs,X_mL72,x,float,68517.9
    wfs,Y_mL72,y,float,223693.3
    wfs,Z_mTAW,start_sondering_mtaw,float,5.40
    wfs,diepte_van_m,diepte_sondering_van,float,0.00
    wfs,diepte_tot_m,diepte_sondering_tot,float,30.48
    wfs,datum_aanvang,datum_aanvang,date,02/09/2011
    wfs,uitvoerder,uitvoerder,string,VO - Afdeling Geotechniek
    wfs,sondeermethode,sondeermethode,string,continu elektrisch
    wfs,apparaat_type,apparaat,string,200kN - MAN2
    xml,/kern:dov-schema/sondering/visueelonderzoek/datumtijd_waarneming_grondwaterstand,datum_gw_meting,date,02/09/2011
    xml,/kern:dov-schema/sondering/visueelonderzoek/grondwaterstand,gw_meting,float,02/09/2011

|

  .. csv-table:: Sonderingen measurement data
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,fiche,pkey_sondering,string,https://.../2011-009205.xml
    xml,/kern:dov-schema/sondering/sondeonderzoek/penetratietest/meetdata/sondeerdiepte,z,float,1.66
    xml,/kern:dov-schema/sondering/sondeonderzoek/penetratietest/meetdata/qc,qc,float,0.6500
    xml,/kern:dov-schema/sondering/sondeonderzoek/penetratietest/meetdata/Qt,Qt,float,NaN
    xml,/kern:dov-schema/sondering/sondeonderzoek/penetratietest/meetdata/fs,fs,float,18.0000
    xml,/kern:dov-schema/sondering/sondeonderzoek/penetratietest/meetdata/u,u,float,NaN
    xml,/kern:dov-schema/sondering/sondeonderzoek/penetratietest/meetdata/i,i,float,0.1000
    xml,/kern:dov-schema/sondering/sondeonderzoek/penetratietest/meetdata/qc,qc,float,NaN



GrondwaterFilter object
==========================

The GrondwaterFilter object contains the data available using the `meetnetten`

This can be translated to three data.frames:

 * Filter, with the screen location information
 * Peilmetingen
 * Observaties



Ligging
~~~~~~~
In deze dataframe komen gelijkaardige velden als bij het zoeken in de site:

  .. csv-table:: Filter
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,filterfiche,pkey_filter,string,https://www.dov.vlaanderen.be/data/filter/2003-000253.xml
    wfs,putfiche,pkey_grondwaterlocatie,string,https://www.dov.vlaanderen.be/data/put/2017-002063.xml
    wfs,GW_ID,gw_id,string,900/82/1
    wfs,filternr,filternummer,string,1
    wfs,filtertype,filtertype,string,peilfilter
    wfs,X_mL72,x,float,257021.8
    wfs,Y_mL72,y,float,159758.4
    xml,/kern:dov-schema/grondwaterlocatie/puntligging/oorspronkelijk_maaiveld, mv_mtaw, float, 257021.8
    wfs,gemeente,gemeente,string,Destelbergen
    xml,/kern:dov-schema/filter/meetnet,meetnet_code,integer(codelist),8
    xml,/kern:dov-schema/filter/ligging/aquifer,aquifer_code,string(codelist),1300
    xml,/kern:dov-schema/filter/ligging/grondwaterlichaam,grondwaterlichaam_code,string(codelist),BLKS_1100_GWL_1M
    xml,/kern:dov-schema/filter/ligging/regime,regime,string(codelist),freatisch
    wfs,onderkant_filter_m,diepte_onderkant_filter,float,8.3
    wfs,lengte_filter_m,lengte_filter,float,5.1


Logica filteropbouw
-------------------
voor het element waar
``kern:dov-schema/filter/opbouw/onderdeel/filterelement == 'filter'``
komt de onderkant van de filter overen met:
``kern:dov-schema/filter/opbouw/onderdeel/tot/``

De lengte komt overeen met
``kern:dov-schema/filter/opbouw/onderdeel/tot/ -
kern:dov-schema/filter/opbouw/onderdeel/van/``, dus de lengte van het filterelement.


Observaties
~~~~~~~~~~~

  .. csv-table:: Observaties (grondwater)
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,filterfiche,pkey_filter,string,https://www.dov.vlaanderen.be/data/filter/2003-000253.xml
    wfs,GW_ID,gw_id,string,1-0709
    wfs,filternr,filternummer,string,2
    xml,/kern:dov-schema/filtermeting/watermonster/identificatie,watermonster,string,1-0709-F2/M2015
    xml,/kern:dov-schema/filtermeting/watermonster/monstername/datum,datum_monstername,date,2015-09-03
    xml,/kern:dov-schema/filtermeting/watermonster/observatie/parameter,parameter,string(codelist),pH
    xml,/kern:dov-schema/filtermeting/watermonster/observatie/waarde_numeriek,waarde,float,5.12
    xml,/kern:dov-schema/filtermeting/watermonster/observatie/eenheid,eenheid,string(codelist),Sörensen
    xml,/kern:dov-schema/filtermeting/watermonster/observatie/betrouwbaarheid,betrouwbaarheid,string(codelist),twijfelachtig

Peilmetingen
~~~~~~~~~~~~

  .. csv-table:: Peilmetingen (grondwater)
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,filterfiche,pkey_filter,string,https://www.dov.vlaanderen.be/data/filter/2003-000253.xml
    wfs,GW_ID,gw_id,string,1-0709
    wfs,filternr,filternummer,string,2
    xml,/kern:dov-schema/filtermeting/peilmeting/datum,datum,date,2015-09-03
    xml,/kern:dov-schema/filtermeting/peilmeting/tijdstip,tijdstip,string,00:00
    xml,/kern:dov-schema/filtermeting/peilmeting/peil_mtaw,peil_mtaw,float,121.88
    xml,/kern:dov-schema/filtermeting/peilmeting/betrouwbaarheid,betrouwbaarheid,string(codelist),goed
    xml,/kern:dov-schema/filtermeting/peilmeting/methode,methode,string(codelist),peillint
