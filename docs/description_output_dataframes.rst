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

Below the desired attributes for each interpretation as 
item /newline/ new_name, data_type, example
The new_name column represents the headers of the final dataframe.
Some elements can occur more than once, e.g. 'bijmenging' in 'Gecodeerde
lithologie' or 'Geotechnische coderingen'. All occurrences should be included 
as new records in the final dataframe.
One of pkey_boring or pkey_sondering is empty, pointing to the source of the 
interpreted data.


  .. csv-table:: Informele stratigrafie
    :header-rows: 1

    source,new_name,data_type,example
    url,pkey_interpretatie,string,https://.../2001-186513.xml
    url_boring,pkey_boring,string,https://.../2001-186513.xml
    url_sondering,pkey_sondering,string,https://.../2001-186513.xml
    /ns3:dov-schema/interpretaties/informelestratigrafie/laag/van,diepte_laag_van,float,0.00
    /ns3:dov-schema/interpretaties/informelestratigrafie/laag/tot,diepte_laag_tot,float,1.74
    /ns3:dov-schema/interpretaties/informelestratigrafie/laag/beschrijving,beschrijving,string,Quartair

|

 .. csv-table:: Formele stratigrafie
    :header-rows: 1

    source,new_name,data_type,example
    url,pkey_interpretatie,string,https://.../2001-186513.xml
    url_boring,pkey_boring,string,https://.../2001-186513.xml
    url_sondering,pkey_sondering,string,https://.../2001-186513.xml
    /ns3:dov-schema/interpretaties/formelestratigrafie/laag/van,diepte_laag_van,float,0.00
    /ns3:dov-schema/interpretaties/formelestratigrafie/laag/tot,diepte_laag_tot,float,1.75
    /ns3:dov-schema/interpretaties/formelestratigrafie/laag/lid1,lid1,string,Q
    /ns3:dov-schema/interpretaties/formelestratigrafie/laag/relatie_lid1_lid2,relatie_lid1_lid2,string,T
    /ns3:dov-schema/interpretaties/formelestratigrafie/laag/lid2,lid2,string,Q

|

  .. csv-table:: Lithologische beschrijvingen
    :header-rows: 1

    source,new_name,data_type,example
    url,pkey_interpretatie,string,https://.../2001-186513.xml
    url_boring,pkey_boring,string,https://.../2001-186513.xml
    url_sondering,pkey_sondering,string,https://.../2001-186513.xml
    /ns3:dov-schema/interpretaties/lithologischebeschrijving/laag/van,diepte_laag_van,float,0.00
    /ns3:dov-schema/interpretaties/lithologischebeschrijving/laag/tot,diepte_laag_tot,float,1.75
    /ns3:dov-schema/interpretaties/lithologischebeschrijving/laag/beschrijving,beschrijving,Terre végétale sableuse

|

  .. csv-table:: Gecodeerde lithologie
    :header-rows: 1

    source,new_name,data_type,example
    url,pkey_interpretatie,string,https://.../2001-186513.xml
    url_boring,pkey_boring,string,https://.../2001-186513.xml
    url_sondering,pkey_sondering,string,https://.../2001-186513.xml
    /ns3:dov-schema/interpretaties/gecodeerdelithologie/laag/van,diepte_laag_van,float,0.00
    /ns3:dov-schema/interpretaties/gecodeerdelithologie/laag/tot,diepte_laag_tot,float,1.75
    /ns3:dov-schema/interpretaties/gecodeerdelithologie/laag/hoofdnaam/grondsoort,hoofd_grondsoort,string,KL
    /ns3:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging/plaatselijk,bijmenging_plaatselijk,boolean,false
    /ns3:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging/hoeveelheid,bijmening_hoeveelheid,string,N
    /ns3:dov-schema/interpretaties/gecodeerdelithologie/laag/bijmenging/grondsoort,bijmenging_grondsoort,string,XZ

|

  .. csv-table:: Hydrogeologische stratigrafie
    :header-rows: 1

    source,new_name,data_type,example
    url,pkey_interpretatie,string,https://.../2001-186513.xml
    url_boring,pkey_boring,string,https://.../2001-186513.xml
    url_sondering,pkey_sondering,string,https://.../2001-186513.xml
    /ns3:dov-schema/interpretaties/hydrogeologischeinterpretatie/laag/van,diepte_laag_van,float,0.00
    /ns3:dov-schema/interpretaties/hydrogeologischeinterpretatie/laag/tot,diepte_laag_tot,float,1.75
    /ns3:dov-schema/interpretaties/hydrogeologischeinterpretatie/laag/aquifer,aquifer,string,0252

|

  .. csv-table:: Informele hydrogeologische stratigrafie
    :header-rows: 1

    source,new_name,data_type,example
    url,pkey_interpretatie,string,https://.../2001-186513.xml
    url_boring,pkey_boring,string,https://.../2001-186513.xml
    url_sondering,pkey_sondering,string,https://.../2001-186513.xml
    /ns3:dov-schema/interpretaties/informelehydrostratigrafie/laag/van,diepte_laag_van,float,0.00
    /ns3:dov-schema/interpretaties/informelehydrostratigrafie/laag/tot,diepte_laag_tot,float,1.75
    /ns3:dov-schema/interpretaties/informelehydrostratigrafie/laag/beschrijving,beschrijving,string,Quartair

|

  .. csv-table:: Quartaire stratigrafie
    :header-rows: 1

    source,new_name,data_type,example
    url,pkey_interpretatie,string,https://.../2001-186513.xml
    url_boring,pkey_boring,string,https://.../2001-186513.xml
    url_sondering,pkey_sondering,string,https://.../2001-186513.xml
    /ns3:dov-schema/interpretaties/quartairstratigrafie/laag/van,diepte_laag_van,float,0.00
    /ns3:dov-schema/interpretaties/quartairstratigrafie/laag/tot,diepte_laag_tot,float,1.75
    /ns3:dov-schema/interpretaties/quartairstratigrafie/laag/lid1,lid1,string,F
    /ns3:dov-schema/interpretaties/quartairstratigrafie/laag/relatie_lid1_lid2,relatie_lid1_lid2,string,T
    /ns3:dov-schema/interpretaties/quartairstratigrafie/laag/lid2,lid2,string,F

|

  .. csv-table:: Geotechnische coderingen
    :header-rows: 1

    source,new_name,data_type,example
    url,pkey_interpretatie,string,https://.../2001-186513.xml
    url_boring,pkey_boring,string,https://.../2001-186513.xml
    url_sondering,pkey_sondering,string,https://.../2001-186513.xml
    /ns3:dov-schema/interpretaties/geotechnischecodering/laag/van,diepte_laag_van,float,0.00
    /ns3:dov-schema/interpretaties/geotechnischecodering/laag/tot,diepte_laag_tot,float,1.75
    /ns3:dov-schema/interpretaties/geotechnischecodering/laag/hoofdnaam/grondsoort,hoofd_grondsoort,string,KL
    /ns3:dov-schema/interpretaties/geotechnischecodering/laag/bijmenging/plaatselijk,bijmenging_plaatselijk,boolean,false
    /ns3:dov-schema/interpretaties/geotechnischecodering/laag/bijmenging/hoeveelheid,bijmening_hoeveelheid,string,N
    /ns3:dov-schema/interpretaties/geotechnischecodering/laag/bijmenging/grondsoort,bijmenging_grondsoort,string,XZ

|

Boreholes
=========

Below the desired attributes for each borehole as 
item /newline/ new_name, data_type, example
The new_name column represents the headers of the final dataframe.

The output of the boreholes can be joined with the interpretations following
the pkey_boring AND ('van' and 'tot') attributes of both dataframes. E.g.: 
multiple layers are discernced 'van'/'tot' in the interpretations for in
between the 'methode_van'/'methode_tot' of the borehole: 
    JOIN ON pkey_boring
    AND interpretation["van"] >= boring["methode_van"]
    AND interpretation["tot"] <= boring["methode_tot"]


  .. csv-table:: Boringen
    :header-rows: 1

    source,new_name,data_type,example
    url,pkey_boring,string,https://.../2001-186513.xml
    /ns3:dov-schema/boring/xy/x,x,float,152301.0
    /ns3:dov-schema/boring/xy/y,y,float,211682.0
    /ns3:dov-schema/boring/oorspronkelijk_maaiveld/waarde,mv_mtaw,float,8.00
    z_mtaw_boring,start_boring_mtaw,float,8.00
    /ns3:dov-schema/boring/diepte_van,diepte_boring_van,float,0.00
    /ns3:dov-schema/boring/diepte_tot,diepte_boring_tot,float,19.00
    /ns3:dov-schema/boring/datum_aanvang,datum_aanvang,date,1930-10-01
    /ns3:dov-schema/boring/uitvoerder/naam,uitvoerder,string,Smet - Dessel
    /ns3:dov-schema/boring/boorgatmeting/uitgevoerd,boorgatmeting,boolean,false
    /ns3:dov-schema/boring/details/boormethode/van,diepte_methode_van,float,0.00
    /ns3:dov-schema/boring/details/boormethode/tot,diepte_methode_tot,float,19.00
    /ns3:dov-schema/boring/details/boormethode/methode,boormethode,string,droge boring
