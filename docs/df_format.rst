.. _object_types:

=======================
Output data description
=======================

.. warning::

    This page is to be removed once all datasets described below are implemented and documented in the :ref:`output_df_fields` section.

The defined output format description of the Pandas :class:`~pandas.DataFrame` for each of the
downloadable data objects:

* :ref:`Interpretations <ref_interpretations>`
* :ref:`Boreholes <ref_boreholes>`
* :ref:`CPT data <ref_cpt_data>`
* :ref:`Groundwater screen<ref_gwfilter>`

For each :class:`~pandas.DataFrame` the following fields are available:

* ``source``: defines the origin of the value, either *wfs* or *xml*
* ``field``: name of the field in the ``source``
* ``new_name``: header name of the output Pandas :class:`~pandas.DataFrame`
* ``data_type``: data type of the column output (e.g. float, date,...)
* ``example``: an example value of the output

The  ``source`` of the information has an implication on the duration of the data request, as data requests
that require downloads of multiple ``xml`` file will take more time. For more information on the duration
difference of ``wfs`` based versus ``xml`` based queries, see :ref:`query duration guide <performance>`.

Not all ``wfs`` fields are included in the :class:`~pandas.DataFrame`, but they can be used
to select records from the DOV database. For example, whe searching on :ref:`Boreholes <ref_boreholes>`,
the presence of the ``informele_stratigrafie``,
``formele_stratigrafie``, ``hydrogeologische_stratigrafie``, etc. are available in the ``wfs`` as
boolean fields to search on.


.. _ref_interpretations:

Interpretations (In Dutch: interpretaties)
==========================================

Possible interpretations are:

 * Informele stratigrafie
 * Formele stratigrafie
 * Lithologische beschrijvingen
 * Gecodeerde lithologie
 * Hydrogeologische stratigrafie
 * Informele hydrogeologische stratigrafie
 * Quartaire stratigrafie
 * Geotechnische coderingen

For each of the interpretations, the available attributes are enlisted in each table table.

Remark that for each depth record, different types can occur resulting in multiple rows for that specific
depth record in the final :class:`~pandas.DataFrame`, e.g. *bijmenging* in *Gecodeerde
lithologie* or *Geotechnische coderingen'*.

As interpretations are either linked to :ref:`Boreholes <ref_boreholes>` or :ref:`CPT data <ref_cpt_data>`,
one of the ``pkey_boring`` or ``pkey_sondering`` is empty and the other pointing to the source of the
interpreted data.

  .. csv-table:: Informele stratigrafie
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,Interpretatiefiche,pkey_interpretatie,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=boring,pkey_boring,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=sondering,pkey_sondering,string,https://.../2001-186513.xml
    wfs,Betrouwbaarheid,betrouwbaarheid_interpretatie,string,goed
    wfs,X_mL72,x,float,152301.0
    wfs,Y_mL72,y,float,211682.0
    wfs,diepte_tot_m,diepte_tot_m,float,20.0
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
    wfs,X_mL72,x,float,152301.0
    wfs,Y_mL72,y,float,211682.0
    wfs,diepte_tot_m,diepte_tot_m,float,20.0
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
    wfs,X_mL72,x,float,152301.0
    wfs,Y_mL72,y,float,211682.0
    wfs,diepte_tot_m,diepte_tot_m,float,20.0
    xml,/kern:dov-schema/interpretaties/lithologischebeschrijving/laag/van,diepte_laag_van,float,0.00
    xml,/kern:dov-schema/interpretaties/lithologischebeschrijving/laag/tot,diepte_laag_tot,float,1.75
    xml,/kern:dov-schema/interpretaties/lithologischebeschrijving/laag/beschrijving,beschrijving,string,Terre végétale sableuse

|

  .. csv-table:: Gecodeerde lithologie and Geotechnische codering
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,Interpretatiefiche,pkey_interpretatie,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=boring,pkey_boring,string,https://.../2001-186513.xml
    wfs,Betrouwbaarheid,betrouwbaarheid_interpretatie,string,goed
    wfs,X_mL72,x,float,152301.0
    wfs,Y_mL72,y,float,211682.0
    wfs,diepte_tot_m,diepte_tot_m,float,20.0
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/van,diepte_laag_van,float,0.00
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/tot,diepte_laag_tot,float,1.75
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/hoofdnaam[1]/grondsoort,hoofdnaam1_grondsoort,string,KL
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/hoofdnaam[2]/grondsoort,hoofdnaam2_grondsoort,string,KL
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging[1]/plaatselijk,bijmenging1_plaatselijk,boolean,false
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging[1]/hoeveelheid,bijmenging1_hoeveelheid,string,N
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging[1]/grondsoort,bijmenging1_grondsoort,string,XZ
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging[2]/plaatselijk,bijmenging2_plaatselijk,boolean,false
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging[2]/hoeveelheid,bijmenging2_hoeveelheid,string,N
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging[2]/grondsoort,bijmenging2_grondsoort,string,XZ
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging[3]/plaatselijk,bijmenging3_plaatselijk,boolean,false
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging[3]/hoeveelheid,bijmenging3_hoeveelheid,string,N
    xml,/kern:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging[3]/grondsoort,bijmenging3_grondsoort,string,XZ

|

  .. csv-table:: Hydrogeologische stratigrafie
    :header-rows: 1

    source,field,new_name,data_type,example
    wfs,Interpretatiefiche,pkey_interpretatie,string,https://.../2001-186513.xml
    wfs,Proeffiche if Type_proef=boring,pkey_boring,string,https://.../2001-186513.xml
    wfs,Betrouwbaarheid,betrouwbaarheid_interpretatie,string,goed
    wfs,X_mL72,x,float,152301.0
    wfs,Y_mL72,y,float,211682.0
    wfs,diepte_tot_m,diepte_tot_m,float,20.0
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
    wfs,X_mL72,x,float,152301.0
    wfs,Y_mL72,y,float,211682.0
    wfs,diepte_tot_m,diepte_tot_m,float,20.0
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
    wfs,X_mL72,x,float,152301.0
    wfs,Y_mL72,y,float,211682.0
    wfs,diepte_tot_m,diepte_tot_m,float,2.0
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
    wfs,X_mL72,x,float,152301.0
    wfs,Y_mL72,y,float,211682.0
    wfs,diepte_tot_m,diepte_tot_m,float,20.0
    xml,/kern:dov-schema/interpretaties/geotechnischecodering/laag/van,diepte_laag_van,float,0.00
    xml,/kern:dov-schema/interpretaties/geotechnischecodering/laag/tot,diepte_laag_tot,float,1.75
    xml,/kern:dov-schema/interpretaties/geotechnischecodering/laag/hoofdnaam/grondsoort,hoofd_grondsoort,string,KL
    xml,/kern:dov-schema/interpretaties/geotechnischecodering/laag/bijmenging/plaatselijk,bijmenging_plaatselijk,boolean,false
    xml,/kern:dov-schema/interpretaties/geotechnischecodering/laag/bijmenging/hoeveelheid,bijmening_hoeveelheid,string,N
    xml,/kern:dov-schema/interpretaties/geotechnischecodering/laag/bijmenging/grondsoort,bijmenging_grondsoort,string,XZ

|

.. _ref_boreholes:

Boreholes (In Dutch: boring)
============================

If required, the output of the :ref:`Boreholes <ref_boreholes>` can be joined with the
:ref:`Interpretations <ref_interpretations>` using the ``pkey_boring``
in combination with the ``van`` and ``tot`` attributes of both dataframes. For example,
multiple layers are discernced 'van'/'tot' in the interpretations for in between
the 'methode_van'/'methode_tot' of the Borehole:

::

    JOIN ON pkey_boring
    AND interpretation["van"] >= boring["methode_van"]
    AND interpretation["tot"] <= boring["methode_tot"]

|

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



.. _ref_cpt_data:

CPT data (In Dutch: sonderingen)
================================

When requesting Cone Penetration Test (CPT) data, two dataframes are discerned:

 1. metadata about the measurement (location, type etc.)
 2. actual measurement data from the ``xml``, with the ``pkey`` to JOIN with the metadata

More than one measurement can be performed, listed as a ``metingWeerstand`` type, i.e.:
qc, Qt, fs, u and i. All elements are by default included in the output dataframe, where
``NaN`` s indicate that it wasn not measured.

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
    xml,/kern:dov-schema/sondering/visueelonderzoek/grondwaterstand,diepte_gw_m,float,02/09/2011

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

.. _ref_gwfilter:

Groundwater screen (In Dutch: Grondwaterfilter)
===============================================

The :class:`~pydov.types.GrondwaterFilter` contains the data available from the `meetnetten`

This can be translated to three dataframes:

 * Screen, with the screen location information
 * Observations
 * Piezometric water level


location
~~~~~~~~
The fields contained in the :class:`~pandas.DataFrame` are similar to those derived from an online search
on the `DOV verkenner`_

.. _DOV verkenner: https://www.dov.vlaanderen.be/portaal/?module=verkenner#ModulePage

  .. csv-table:: Screen
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

Piezometric water level
~~~~~~~~~~~~~~~~~~~~~~~

  .. csv-table:: Peilmetingen (groundwater)
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

Observations
~~~~~~~~~~~~

  .. csv-table:: Observations (groundwater)
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
