DovGrondwaterFilter object
==========================

Het DOVGrondwaterFilter object bevat alle data van een zoekactie op de laag meetnetten.

Acherliggend zit de meeste informatie vervat in 3 dataframes:

 * ligging: bevat de ligging (xyz)
 * observaties
 * peilmetingen


Ligging
~~~~~~~
In deze dataframe komen gelijkaardige velden als bij het zoeken in de site:

  .. csv-table:: Ligging
    :header-rows: 1

    source,new_name,data_type,example
    url,permkey_filter,permkey, https://www.dov.vlaanderen.be/data/filter/2003-000253.xml
    url,permkey_gw_id,permkey, https://www.dov.vlaanderen.be/data/put/2017-002063.xml
    ns3:dov-schema/grondwaterlocatie/identificatie, gw_id, tekst, 900/82/1
    ns3:dov-schema/filter/identificatie, filternummer, tekst, 1
    ns3:dov-schema/filter/filtertype, filtertype, tekst, peilfilter
    ns3:dov-schema/grondwaterlocatie/puntligging/xy/x, x, numeric, 257021.8
    ns3:dov-schema/grondwaterlocatie/puntligging/xy/y, y, numeric, 159758.4
    (complex), z_mtaw, numeric, 257021.8
    ns3:dov-schema/grondwaterlocatie/puntligging/gemeente, gemeente, niscode, 73109
    ns3:dov-schema/filter/meetnet, meetnet, numeriek(codelijst), 8
    ns3:dov-schema/filter/ligging/aquifer, aquifer, numeriek(codelijst), 1300
    ns3:dov-schema/filter/ligging/grondwaterlichaam, aquifer, numeriek(codelijst), BLKS_1100_GWL_1M
    ns3:dov-schema/filter/ligging/regime, aquifer, numeriek(codelijst), freatisch
    (complex - filteropbouw), onderkant filter, numeriek(codelijst), 8
    (complex - filteropbouw), lengte filter, numeriek(codelijst), 8


Observaties
~~~~~~~~~~~

  .. csv-table:: Observaties (grondwater)
    :header-rows: 1

    source,new_name,data_type,example
    ns3:dov-schema/filtermeting/filter/permkey**, permkey_filter, permkey, https://www.dov.vlaanderen.be/data/filter/2003-000253.xml
    ns3:dov-schema/filtermeting/grondwaterlocatie, gw_id, tekst, 900/82/1
    ns3:dov-schema/filtermeting/filter/identificatie, tekst, filternummer, 1
    ns3:dov-schema/filtermeting/peilmeting/peil_mtaw, peil_mtaw, numeriek, 121.88
    ns3:dov-schema/filtermeting/peilmeting/betrouwbaarheid, betrouwbaarheid, tekst (codelijst), goed
    ns3:dov-schema/filtermeting/peilmeting/methode, methode, tekst(codelijst), peillint


Peilmetingen
~~~~~~~~~~~~

  .. csv-table:: Peilmetingen (grondwater)
    :header-rows: 1

    source,new_name,data_type,example
    ns3:dov-schema/filtermeting/filter/permkey**, permkey_filter, permkey, https://www.dov.vlaanderen.be/data/filter/2003-000253.xml
    ns3:dov-schema/filtermeting/grondwaterlocatie, gw_id, tekst, 900/82/1
    ns3:dov-schema/filtermeting/filter/identificatie, tekst, filternummer, 1
    ns3:dov-schema/filtermeting/peilmeting/peil_mtaw, peil_mtaw, numeriek, 121.88
    ns3:dov-schema/filtermeting/peilmeting/betrouwbaarheid, betrouwbaarheid, tekst (codelijst), goed
    ns3:dov-schema/filtermeting/peilmeting/methode, methode, tekst(codelijst), peillint

