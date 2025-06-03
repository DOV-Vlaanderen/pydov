.. _select_datasets:

===============
Select datasets
===============

To get started with pydov you should first determine which information you want to search for. DOV provides a lot of different datasets about soil, subsoil and groundwater of Flanders, most of which can be queried using pydov.

Depending on the type of data you want to query, you need a different search class instance. To search for boreholes for instance, you'd write::

    from pydov.search.boring import BoringSearch

    borehole_search = BoringSearch()
    # df = borehole_search.search(...)

While you'll need to instantiate a different search class for each datatype, querying the datatypes from then on is similar as each one supports the same ``search()`` method. You can use similar queries for each of them, filtering on :ref:`attributes <query_attribute>`, :ref:`location <query_location>`, :ref:`sorting, limiting, <sort_limit>` and :ref:`customizing the output fields <output_df_fields>`.

Generally the datasets consist of a main type and a subtype, where the resulting dataframe will contain multiple records for each instance of the main type based on the records of the subtype (you can think of this as a 'left join' between the main and the subtype).

Currently, we support the following datasets:

.. contents:: Datasets
    :local:

Soil
****

.. contents:: Soil datasets
    :local:

Soil sites (Bodemsites)
-----------------------

Type
    Bodemsite (Soil site)

Subtype
    No subtype

Search class
    :class:`pydov.search.bodemsite.BodemsiteSearch`

Default dataframe output
  .. csv-table:: Soil sites (Bodemsites)
    :header-rows: 1

    Field,Source,Cost,Datatype,Example
    pkey_bodemsite,Bodemsite,1,string,https://www.dov.vlaanderen.be/data/bodemsite/2013-000180
    naam,Bodemsite,1,string,Meise_Neerpoorten
    waarnemingsdatum,Bodemsite,1,date,nan
    beschrijving,Bodemsite,1,string,grasland
    invoerdatum,Bodemsite,10,date,nan

Soil plots (Bodemlocaties)
--------------------------

Type
    Bodemlocatie (Soil plot)

Subtype
    No subtype

Search class
    :class:`pydov.search.bodemlocatie.BodemlocatieSearch`

Default dataframe output
    .. csv-table:: Soil plots (Bodemlocaties)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_bodemlocatie,Bodemlocatie,1,string,https://www.dov.vlaanderen.be/data/bodemlocatie/2011-000002
        pkey_bodemsite,Bodemlocatie,1,string,https://www.dov.vlaanderen.be/data/bodemsite/2011-000245
        naam,Bodemlocatie,1,string,STARC_4
        type,Bodemlocatie,1,string,profielput
        waarnemingsdatum,Bodemlocatie,1,date,nan
        doel,Bodemlocatie,1,string,archeologische landschappelijke profielputten
        x,Bodemlocatie,1,float,206553.85
        y,Bodemlocatie,1,float,168891.11
        mv_mtaw,Bodemlocatie,1,float,44.00
        erfgoed,Bodemlocatie,1,boolean,true
        bodemstreek,Bodemlocatie,1,string,Zandleemstreek
        invoerdatum,Bodemlocatie,10,date,nan
        educatieve_waarde,Bodemlocatie,10,string,ZEER

Soil intervals (Bodemdiepteintervallen)
---------------------------------------

Type
    Bodemdiepteinterval (Soil interval)

Subtype
    No subtype

Search class
    :class:`pydov.search.bodemdiepteinterval.BodemdiepteintervalSearch`

Default dataframe output
      .. csv-table:: Soil intervals (Bodemdiepteintervallen)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_diepteinterval,Bodemdiepteinterval,1,string,https://www.dov.vlaanderen.be/data/bodemdiepteinterval/2018-000003
        pkey_bodemopbouw,Bodemdiepteinterval,1,string,https://www.dov.vlaanderen.be/data/bodemopbouw/2018-000001
        pkey_bodemlocatie,Bodemdiepteinterval,1,string,https://www.dov.vlaanderen.be/data/bodemlocatie/2014-000001
        nr,Bodemdiepteinterval,1,integer,3
        type,Bodemdiepteinterval,1,string,horizont
        naam,Bodemdiepteinterval,1,string,Bg
        bovengrens1_cm,Bodemdiepteinterval,1,float,40.0
        bovengrens2_cm,Bodemdiepteinterval,1,float,NaN
        ondergrens1_cm,Bodemdiepteinterval,1,float,65.0
        ondergrens2_cm,Bodemdiepteinterval,1,float,NaN
        ondergrens_bereikt,Bodemdiepteinterval,1,string,NVT
        grensduidelijkheid,Bodemdiepteinterval,1,string,abrupt - overgang 0-2 cm breed
        grensregelmatigheid,Bodemdiepteinterval,1,string,bijna vlak
        beschrijving,Bodemdiepteinterval,1,string,onverweerd moedermateriaal met gleyverschijnselen
        x,Bodemdiepteinterval,1,float,187237.11
        y,Bodemdiepteinterval,1,float,163028.83
        mv_mtaw,Bodemdiepteinterval,1,float,49.0

Soil samples (Bodemmonsters)
----------------------------

Type
    Bodemmonster (Soil sample)

Subtype
    No subtype

Search class
    :class:`pydov.search.bodemmonster.BodemmonsterSearch`

Default dataframe output
      .. csv-table:: Soil samples (Bodemmonsters)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_bodemmonster,Bodemmonster,1,string,https://www.dov.vlaanderen.be/data/bodemmonster/1964-264869
        pkey_bodemlocatie,Bodemmonster,1,string,https://www.dov.vlaanderen.be/data/bodemlocatie/2015-000745
        pkey_parent,Bodemmonster,1,string,https://www.dov.vlaanderen.be/data/diepteinterval/2019-003366
        x,Bodemmonster,1,float,206553.85
        y,Bodemmonster,1,float,168891.11
        mv_mtaw,Bodemmonster,1,float,44.00
        identificatie,Bodemmonster,1,string,KART_PROF_073E/12_H2_M1
        datum_monstername,Bodemmonster,1,date,1964-11-12
        tijdstip_monstername,Bodemmonster,10,string,NaN
        type,Bodemmonster,1,string,ENK
        monstername_door,Bodemmonster,1,string,Centrum voor Grondonderzoek (C.V.G.)
        techniek,Bodemmonster,1,string,NaN
        condities,Bodemmonster,1,string,Zie scan analoge profielbeschrijving
        diepte_van_cm,Bodemmonster,1,float,30
        diepte_tot_cm,Bodemmonster,1,float,45
        labo,Bodemmonster,1,string,Centrum voor Grondonderzoek (C.V.G.)

Soil observations (Bodemobservaties)
------------------------------------

Type
    Bodemobservatie (Soil observations)

Subtype
    Fractiemeting (Fraction measurement)

Search class
    :class:`pydov.search.bodemobservatie.BodemobservatieSearch`

Default dataframe output
      .. csv-table:: Soil observations (Bodemobservaties)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_bodemobservatie,Bodemobservatie,1,string,https://www.dov.vlaanderen.be/data/bodemobservatie/2019-349078
        pkey_bodemlocatie,Bodemobservatie,1,string,https://www.dov.vlaanderen.be/data/bodemlocatie/1952-007078
        pkey_parent,Bodemobservatie,1,string,https://www.dov.vlaanderen.be/data/bodemlocatie/1952-007078
        x,Bodemobservatie,1,float,206553.85
        y,Bodemobservatie,1,float,168891.11
        mv_mtaw,Bodemobservatie,1,float,44.00
        diepte_van_cm,Bodemobservatie,1,float,30
        diepte_tot_cm,Bodemobservatie,1,float,45
        observatiedatum,Bodemobservatie,10,date,1964-11-12
        invoerdatum,Bodemobservatie,10,date,NaN
        parametergroep,Bodemobservatie,10,string,Bodem_fysisch_structuur
        parameter,Bodemobservatie,1,string,organische_c_perc
        detectie,Bodemobservatie,10,string,<
        waarde,Bodemobservatie,1,string,0.38
        eenheid,Bodemobservatie,1,string,%
        veld_labo,Bodemobservatie,1,string,VELD
        methode,Bodemobservatie,1,string,Aardewerk nieuwe methode organische koolstof
        betrouwbaarheid,Bodemobservatie,10,string,onbekend
        fractiemeting_ondergrens,Fractiemeting,10,float,NaN
        fractiemeting_bovengrens,Fractiemeting,10,float,NaN
        fractiemeting_waarde,Fractiemeting,10,float,NaN

Soil classifications (Bodemclassificaties)
------------------------------------------

Type
    Bodemclassificatie (Soil classification)

Subtype
    No subtype

Search class
    :class:`pydov.search.bodemclassificatie.BodemclassificatieSearch`

Default dataframe output
      .. csv-table:: Soil classifications (Bodemclassificaties)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_bodemclassificatie,Bodemclassificatie,1,string,https://www.dov.vlaanderen.be/data/belgischebodemclassificatie/2018-000146
        pkey_bodemlocatie,Bodemclassificatie,1,string,https://www.dov.vlaanderen.be/data/bodemlocatie/2015-000146
        x,Bodemclassificatie,1,float,248905.67
        y,Bodemclassificatie,1,float,200391.29
        mv_mtaw,Bodemclassificatie,1,float,32.9
        classificatietype,Bodemclassificatie,1,string,Algemene Belgische classificatie
        bodemtype,Bodemclassificatie,1,string,Scbz
        auteurs,Bodemclassificatie,1,string,Dondeyne, Stefaan (KULeuven)

Subsoil
*******

.. contents:: Subsoil datasets
    :local:

Boreholes (Boringen)
--------------------

Type
    Boring (Borehole)

Subtype
    Boormethode (Method)

Search class
    :class:`pydov.search.boring.BoringSearch`

Default dataframe output
      .. csv-table:: Boreholes (boringen)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_boring,Boring,1,string,https://www.dov.vlaanderen.be/data/boring/1930-120730
        boornummer,Boring,1,string,kb15d28w-B164
        x,Boring,1,float,152301.0
        y,Boring,1,float,211682.0
        mv_mtaw,Boring,10,float,8.00
        start_boring_mtaw,Boring,1,float,8.00
        gemeente,Boring,1,string,Wuustwezel
        diepte_boring_van,Boring,10,float,0.00
        diepte_boring_tot,Boring,1,float,19.00
        datum_aanvang,Boring,1,date,1930-10-01
        uitvoerder,Boring,1,string,Smet - Dessel
        boorgatmeting,Boring,10,boolean,false
        diepte_methode_van,Boormethode,10,float,0.00
        diepte_methode_tot,Boormethode,10,float,19.00
        boormethode,Boormethode,10,string,droge boring

Borehole samples (Grondmonsters)
--------------------------------

Type
    Grondmonster (Borehole sample)

Subtype
    Korrelverdeling (Particle size distribution)

Search class
    :class:`pydov.search.grondmonster.GrondmonsterSearch`

Default dataframe output
      .. csv-table:: Borehole samples (grondmonsters)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_grondmonster,Grondmonster,1,string,https://www.dov.vlaanderen.be/data/grondmonster/2017-168758
        naam,Grondmonster,1,string,N3A
        pkey_parents,Grondmonster,1,list of string,[https://www.dov.vlaanderen.be/data/boring/2005-003015]
        datum,Grondmonster,1,date,2005-02-02
        diepte_van_m,Grondmonster,1,float,5.9
        diepte_tot_m,Grondmonster,1,float,6.05
        monstertype,Grondmonster,1,string,ongeroerd
        monstersamenstelling,Grondmonster,1,string,ENKELVOUDIG
        astm_naam,Grondmonster,10,string,Organic silt
        grondsoort_bggg,Grondmonster,10,string,humush. klei
        humusgehalte,Grondmonster,10,float,15.6
        kalkgehalte,Grondmonster,10,float,4.4
        uitrolgrens,Grondmonster,10,float,50.4
        vloeigrens,Grondmonster,10,float,86.4
        glauconiet_totaal,Grondmonster,10,float,NaN
        korrelvolumemassa,Grondmonster,10,float,NaN
        volumemassa,Grondmonster,10,float,NaN
        watergehalte,Grondmonster,10,float,NaN
        methode,Korrelverdeling,10,string,Korrelverdeling d.m.v. hydrometer/areometer
        diameter,Korrelverdeling,10,float,0.001
        fractie,Korrelverdeling,10,float,45.8

CPT measurements (Sonderingen)
------------------------------

Type
    Sondering (CPT measurement)

Subtype
    Meetdata (CPT data)

Search class
    :class:`pydov.search.sondering.SonderingSearch`

Default dataframe output
      .. csv-table:: CPT measurements (sonderingen)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_sondering,Sondering,1,string,https://www.dov.vlaanderen.be/data/sondering/2002-010317
        sondeernummer,Sondering,1,string,GEO-02/079-S3
        x,Sondering,1,float,142767
        y,Sondering,1,float,221907
        mv_mtaw,Sondering,10,float,NaN
        start_sondering_mtaw,Sondering,1,float,2.39
        diepte_sondering_van,Sondering,1,float,0
        diepte_sondering_tot,Sondering,1,float,16
        datum_aanvang,Sondering,1,date,2002-07-04
        uitvoerder,Sondering,1,string,MVG - Afdeling Geotechniek
        sondeermethode,Sondering,1,string,continu elektrisch
        apparaat,Sondering,1,string,200kN - RUPS
        datum_gw_meting,Sondering,10,datetime,2002-07-04 13:50:00
        diepte_gw_m,Sondering,10,float,1.2
        lengte,Meetdata,10,float,1.2
        diepte,Meetdata,10,float,1.2
        qc,Meetdata,10,float,0.68
        Qt,Meetdata,10,float,NaN
        fs,Meetdata,10,float,10
        u,Meetdata,10,float,7
        i,Meetdata,10,float,0.1


Formal stratigraphy (Formele stratigrafie)
------------------------------------------

Type
    FormeleStratigrafie (Formal stratigraphy)

Subtype
    FormeleStratigrafieLaag (Formal stratigraphy layer)

Search class
    :class:`pydov.search.interpretaties.FormeleStratigrafieSearch`

Default dataframe output
      .. csv-table:: Formal stratigraphy (Formele stratigrafie)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_interpretatie,FormeleStratigrafie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2002-227082
        pkey_boring,FormeleStratigrafie,1,string,NaN
        pkey_sondering,FormeleStratigrafie,1,string,https://www.dov.vlaanderen.be/data/sondering/1989-068788
        betrouwbaarheid_interpretatie,FormeleStratigrafie,1,string,goed
        x,FormeleStratigrafie,1,float,108455
        y,FormeleStratigrafie,1,float,194565
        start_interpretatie_mtaw,FormeleStratigrafie,1,float,6.62
        diepte_laag_van,FormeleStratigrafieLaag,10,float,0
        diepte_laag_tot,FormeleStratigrafieLaag,10,float,13
        lid1,FormeleStratigrafieLaag,10,string,Q
        relatie_lid1_lid2,FormeleStratigrafieLaag,10,string,T
        lid2,FormeleStratigrafieLaag,10,string,Q

Informal stratigraphy (Informele stratigrafie)
----------------------------------------------

Type
    InformeleStratigrafie (Informal stratigraphy)

Subtype
    InformeleStratigrafieLaag (Informal stratigraphy layer)

Search class
    :class:`pydov.search.interpretaties.InformeleStratigrafieSearch`

Default dataframe output
      .. csv-table:: Informal stratigraphy (Informele stratigrafie)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_interpretatie,InformeleStratigrafie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2016-290843
        pkey_boring,InformeleStratigrafie,1,string,https://www.dov.vlaanderen.be/data/boring/1893-073690
        pkey_sondering,InformeleStratigrafie,1,string,NaN
        betrouwbaarheid_interpretatie,InformeleStratigrafie,1,string,onbekend
        x,InformeleStratigrafie,1,float,108900
        y,InformeleStratigrafie,1,float,194425
        start_interpretatie_mtaw,InformeleStratigrafie,1,float,6.00
        diepte_laag_van,InformeleStratigrafieLaag,10,float,0
        diepte_laag_tot,InformeleStratigrafieLaag,10,float,18.58
        beschrijving,InformeleStratigrafieLaag,10,string,Q

Hydrogeological stratigraphy (Hydrogeologische stratigrafie)
------------------------------------------------------------

Type
    HydrogeologischeStratigrafie (Hydrogeological stratigraphy)

Subtype
    HydrogeologischeStratigrafieLaag (Hydrogeological stratigraphy layer)

Search class
    :class:`pydov.search.interpretaties.HydrogeologischeStratigrafieSearch`

Default dataframe output
    .. csv-table:: Hydrogeological stratigraphy (Hydrogeologische stratigrafie)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_interpretatie,HydrogeologischeStratigrafie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2001-198755
        pkey_boring,HydrogeologischeStratigrafie,1,string,https://www.dov.vlaanderen.be/data/boring/1890-073688
        betrouwbaarheid_interpretatie,HydrogeologischeStratigrafie,1,string,goed
        x,HydrogeologischeStratigrafie,1,float,108773
        y,HydrogeologischeStratigrafie,1,float,194124
        start_interpretatie_mtaw,HydrogeologischeStratigrafie,1,float,7.00
        diepte_laag_van,HydrogeologischeStratigrafieLaag,10,float,0
        diepte_laag_tot,HydrogeologischeStratigrafieLaag,10,float,8
        aquifer,HydrogeologischeStratigrafieLaag,10,string,0110

Informal hydrogeological stratigraphy (Informele hydrogeologische stratigrafie)
-------------------------------------------------------------------------------

Type
    InformeleHydrogeologischeStratigrafie (Informal hydrogeological stratigraphy)

Subtype
    InformeleHydrogeologischeStratigrafieLaag (Informal hydrogeological stratigraphy layer)

Search class
    :class:`pydov.search.interpretaties.InformeleHydrogeologischeStratigrafieSearch`

Default dataframe output
      .. csv-table:: Informal hydrogeological stratigraphy (Informele hydrogeologische stratigrafie)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_interpretatie,InformeleHydrogeologischeStratigrafie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2003-297769
        pkey_boring,InformeleHydrogeologischeStratigrafie,1,string,https://www.dov.vlaanderen.be/data/boring/2003-147935
        betrouwbaarheid_interpretatie,InformeleHydrogeologischeStratigrafie,1,string,goed
        x,InformeleHydrogeologischeStratigrafie,1,float,208607
        y,InformeleHydrogeologischeStratigrafie,1,float,210792
        start_interpretatie_mtaw,InformeleHydrogeologischeStratigrafie,1,float,38.94
        diepte_laag_van,InformeleHydrogeologischeStratigrafieLaag,10,float,0
        diepte_laag_tot,InformeleHydrogeologischeStratigrafieLaag,10,float,1.5
        beschrijving,InformeleHydrogeologischeStratigrafieLaag,10,string,Quartair

Coded lithology (Gecodeerde lithologie)
---------------------------------------

Type
    GecodeerdeLithologie (Coded lithology)

Subtype
    GecodeerdeLithologieLaag (Coded lithology layer)

Search class
    :class:`pydov.search.interpretaties.GecodeerdeLithologieSearch`

Default dataframe output
      .. csv-table:: Coded lithology (Gecodeerde lithologie)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_interpretatie,GecodeerdeLithologie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2003-205091
        pkey_boring,GecodeerdeLithologie,1,string,https://www.dov.vlaanderen.be/data/boring/2003-076348
        betrouwbaarheid_interpretatie,GecodeerdeLithologie,1,string,goed
        x,GecodeerdeLithologie,1,float,110601
        y,GecodeerdeLithologie,1,float,196625
        start_interpretatie_mtaw,GecodeerdeLithologie,1,float,6.38
        diepte_laag_van,GecodeerdeLithologieLaag,10,float,4
        diepte_laag_tot,GecodeerdeLithologieLaag,10,float,4.5
        hoofdnaam1_grondsoort,GecodeerdeLithologieLaag,10,string,MZ
        hoofdnaam2_grondsoort,GecodeerdeLithologieLaag,10,string,NaN
        bijmenging1_plaatselijk,GecodeerdeLithologieLaag,10,boolean,False
        bijmenging1_hoeveelheid,GecodeerdeLithologieLaag,10,string,N
        bijmenging1_grondsoort,GecodeerdeLithologieLaag,10,string,SC
        bijmenging2_plaatselijk,GecodeerdeLithologieLaag,10,boolean,NaN
        bijmenging2_hoeveelheid,GecodeerdeLithologieLaag,10,string,NaN
        bijmenging2_grondsoort,GecodeerdeLithologieLaag,10,string,NaN
        bijmenging3_plaatselijk,GecodeerdeLithologieLaag,10,boolean,NaN
        bijmenging3_hoeveelheid,GecodeerdeLithologieLaag,10,string,NaN
        bijmenging3_grondsoort,GecodeerdeLithologieLaag,10,string,NaN

Geotechnical encoding (Geotechnische codering)
----------------------------------------------

Type
    GeotechnischeCodering (Geotechnical encoding)

Subtype
    GeotechnischeCoderingLaag (Geotechnical encoding layer)

Search class
    :class:`pydov.search.interpretaties.GeotechnischeCoderingSearch`

Default dataframe output
      .. csv-table:: Geotechnical encoding (Geotechnische codering)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_interpretatie,GeotechnischeCodering,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2014-184535
        pkey_boring,GeotechnischeCodering,1,string,https://www.dov.vlaanderen.be/data/boring/1957-033538
        betrouwbaarheid_interpretatie,GeotechnischeCodering,1,string,goed
        x,GeotechnischeCodering,1,float,108851
        y,GeotechnischeCodering,1,float,196510
        start_interpretatie_mtaw,GeotechnischeCodering,1,float,10.55
        diepte_laag_van,GeotechnischeCoderingLaag,10,float,1
        diepte_laag_tot,GeotechnischeCoderingLaag,10,float,1.5
        hoofdnaam1_grondsoort,GeotechnischeCoderingLaag,10,string,XZ
        hoofdnaam2_grondsoort,GeotechnischeCoderingLaag,10,string,NaN
        bijmenging1_plaatselijk,GeotechnischeCoderingLaag,10,boolean,NaN
        bijmenging1_hoeveelheid,GeotechnischeCoderingLaag,10,string,NaN
        bijmenging1_grondsoort,GeotechnischeCoderingLaag,10,string,NaN
        bijmenging2_plaatselijk,GeotechnischeCoderingLaag,10,boolean,NaN
        bijmenging2_hoeveelheid,GeotechnischeCoderingLaag,10,string,NaN
        bijmenging2_grondsoort,GeotechnischeCoderingLaag,10,string,NaN
        bijmenging3_plaatselijk,GeotechnischeCoderingLaag,10,boolean,NaN
        bijmenging3_hoeveelheid,GeotechnischeCoderingLaag,10,string,NaN
        bijmenging3_grondsoort,GeotechnischeCoderingLaag,10,string,NaN

Lithological descriptions (Lithologische beschrijvingen)
--------------------------------------------------------

Type
    LithologischeBeschrijvingen (Lithological descriptions)

Subtype
    LithologischeBeschrijvingenLaag (Lithological descriptions layer)

Search class
    :class:`pydov.search.interpretaties.LithologischeBeschrijvingenSearch`

Default dataframe output
      .. csv-table:: Lithological descriptions (Lithologische beschrijvingen)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_interpretatie,LithologischeBeschrijvingen,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2017-302166
        pkey_boring,LithologischeBeschrijvingen,1,string,https://www.dov.vlaanderen.be/data/boring/2017-151410
        betrouwbaarheid_interpretatie,LithologischeBeschrijvingen,1,string,onbekend
        x,LithologischeBeschrijvingen,1,float,109491
        y,LithologischeBeschrijvingen,1,float,196700
        start_interpretatie_mtaw,LithologischeBeschrijvingen,1,float,7.90
        diepte_laag_van,LithologischeBeschrijvingenLaag,10,float,0
        diepte_laag_tot,LithologischeBeschrijvingenLaag,10,float,1
        beschrijving,LithologischeBeschrijvingenLaag,10,string,klei/zand

Quaternary stratigraphy (Quartair stratigrafie)
-----------------------------------------------

Type
    QuartairStratigrafie (Quaternary stratigraphy)

Subtype
    QuartairStratigrafieLaag (Quaternary stratigraphy layer)

Search class
    :class:`pydov.search.interpretaties.QuartairStratigrafieSearch`

Default dataframe output
      .. csv-table:: Quaternary stratigraphy (Quartaire stratigrafie)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_interpretatie,QuartairStratigrafie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/1999-057087
        pkey_boring,QuartairStratigrafie,1,string,https://www.dov.vlaanderen.be/data/boring/1941-000322
        betrouwbaarheid_interpretatie,QuartairStratigrafie,1,string,onbekend
        x,QuartairStratigrafie,1,float,128277
        y,QuartairStratigrafie,1,float,178987
        start_interpretatie_mtaw,QuartairStratigrafie,1,float,9.56
        diepte_laag_van,QuartairStratigrafieLaag,10,float,0
        diepte_laag_tot,QuartairStratigrafieLaag,10,float,8
        lid1,QuartairStratigrafieLaag,10,string,F1
        relatie_lid1_lid2,QuartairStratigrafieLaag,10,string,T
        lid2,QuartairStratigrafieLaag,10,string,F1

Groundwater
***********

.. contents:: Groundwater datasets
    :local:

Groundwater screens (Grondwaterfilters)
---------------------------------------

Type
    GrondwaterFilter (Groundwater screen)

Subtype
    Peilmeting (Water head level)

Search class
    :class:`pydov.search.grondwaterfilter.GrondwaterFilterSearch`

Remarks
    Mind that the timeseries contains two columns referring to the time: `datum` and `tijdstip`, with datatype `date`, respectively `string`. This distinction is required because the `tijdstip` field is not mandatory whereas the `date` is. It is up to the user to combine these fields in a datetime object if required.

Default dataframe output
    .. csv-table:: Groundwater screens (grondwaterfilters)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_filter,GrondwaterFilter,1,string,https://www.dov.vlaanderen.be/data/filter/1989-001024
        pkey_grondwaterlocatie,GrondwaterFilter,1,string,https://www.dov.vlaanderen.be/data/put/2017-000200
        gw_id,GrondwaterFilter,1,string,4-0053
        filternummer,GrondwaterFilter,1,string,1
        filtertype,GrondwaterFilter,1,string,peilfilter
        x,GrondwaterFilter,1,float,110490
        y,GrondwaterFilter,1,float,194090
        start_grondwaterlocatie_mtaw,GrondwaterFilter,1,float,NaN
        mv_mtaw,GrondwaterFilter,10,float,NaN
        gemeente,GrondwaterFilter,1,string,Destelbergen
        meetnet_code,GrondwaterFilter,10,string,1
        aquifer_code,GrondwaterFilter,10,string,0100
        grondwaterlichaam_code,GrondwaterFilter,10,string,CVS_0160_GWL_1
        regime,GrondwaterFilter,10,string,freatisch
        diepte_onderkant_filter,GrondwaterFilter,1,float,13
        lengte_filter,GrondwaterFilter,1,float,2
        datum,Peilmeting,10,date,2004-05-18
        tijdstip,Peilmeting,10,string,NaN
        peil_mtaw,Peilmeting,10,float,4.6
        betrouwbaarheid,Peilmeting,10,string,goed
        methode,Peilmeting,10,string,peillint
        filterstatus,Peilmeting,10,string,1
        filtertoestand,Peilmeting,10,string,in rust

Groundwater samples (Grondwatermonsters)
----------------------------------------

Type
    GrondwaterMonster (Groundwater sample)

Subtype
    Observatie (Quality measurement)

Search class
    :class:`pydov.search.grondwatermonster.GrondwaterMonsterSearch`

Default dataframe output
      .. csv-table:: Groundwater samples (grondwatermonsters)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        pkey_grondwatermonster,GrondwaterMonster,1,string,https://www.dov.vlaanderen.be/data/watermonster/2010-001344
        grondwatermonsternummer,GrondwaterMonster,1,string,2-0114/M2010
        pkey_grondwaterlocatie,GrondwaterMonster,1,string,https://www.dov.vlaanderen.be/data/put/2017-000096
        gw_id,GrondwaterMonster,1,string,2-0114
        pkey_filter,GrondwaterMonster,1,string,https://www.dov.vlaanderen.be/data/filter/1996-001085
        filternummer,GrondwaterMonster,1,string,1
        x,GrondwaterMonster,1,float,153030
        y,GrondwaterMonster,1,float,158805
        start_grondwaterlocatie_mtaw,GrondwaterMonster,1,float,129.88
        gemeente,GrondwaterMonster,1,string,Sint-Genesius-Rode
        datum_monstername,GrondwaterMonster,1,date,2020-01-20
        parametergroep,Observatie,10,string,Zware metalen
        parameter,Observatie,10,string,Hg
        detectie,Observatie,10,string,<
        waarde,Observatie,10,float,0.5
        eenheid,Observatie,10,string,µg/l
        veld_labo,Observatie,10,string,LABO

Groundwater permits (Grondwatervergunningen)
--------------------------------------------

Type
    GrondwaterVergunning (Groundwater permit)

Subtype
    No subtype

Search class
    :class:`pydov.search.grondwatervergunning.GrondwaterVergunningSearch`

Default dataframe output
      .. csv-table:: Groundwater permits (grondwatervergunningen)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        id_vergunning,GrondwaterVergunning,1,string,66229
        pkey_installatie,GrondwaterVergunning,1,string,https://www.dov.vlaanderen.be/data/installatie/2020-093103
        x,GrondwaterVergunning,1,float,157403.75
        y,GrondwaterVergunning,1,float,214471.32
        diepte,GrondwaterVergunning,1,float,10.0
        exploitant_naam,GrondwaterVergunning,1,string,AQUAFIN
        watnr,GrondwaterVergunning,1,string,VLA-0019-A
        vlaremrubriek,GrondwaterVergunning,1,string,53.2.2.b)2
        vergund_jaardebiet,GrondwaterVergunning,1,float,493000.0
        vergund_dagdebiet,GrondwaterVergunning,1,float,nan
        van_datum_termijn,GrondwaterVergunning,1,date,2019-08-09
        tot_datum_termijn,GrondwaterVergunning,1,date,nan
        aquifer_vergunning,GrondwaterVergunning,1,string,0200: Kempens Aquifersysteem
        inrichtingsklasse,GrondwaterVergunning,1,string,Klasse 1 - Vlaams project
        nacebelcode,GrondwaterVergunning,1,string,37000: Afvalwaterafvoer
        actie_waakgebied,GrondwaterVergunning,1,string,nan
        cbbnr,GrondwaterVergunning,1,string,00418870000022
        kbonr,GrondwaterVergunning,1,string,044691388

Generic
*******

DOV WFS layer
-------------

Next to the custom types defined in pydov above, you can also query any WFS layer available in the DOV WFS service.
You can find all available WFS layers in our `metadata catalogue`_.

    .. _metadata catalogue: https://dov.vlaanderen.be/geonetwork/

Search class
    :class:`pydov.search.generic.WfsSearch`

Remarks
    When instantiating the WfsSearch class, you can provide the workspace-qualified layer name of your interest, for example::

        from pydov.search.generic import WfsSearch

        s = WfsSearch('erosie:erosie_gemeente')

Example dataframe output
    By default the output dataframe will contain all attribute columns from the requested WFS layer, for example:

    .. csv-table:: Groundwater permits (grondwatervergunningen)
        :header-rows: 1

        Field,Source,Cost,Datatype,Example
        dataengine_id,WfsType,1,integer,1
        gemeentelijke_erosiegevoeligheid,WfsType,1,string,zeer weinig erosiegevoelig
        klasse,WfsType,1,integer,5
        gemeente,WfsType,1,string,Zoersel
        provincie,WfsType,1,string,Antwerpen