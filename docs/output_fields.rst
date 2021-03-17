.. _output_df_fields:

=======================
Customizing data output
=======================

When using pydov to search datasets, the returned dataframe has different default columns (fields) depending on the dataset. We believe each dataframe to contain the most relevant fields for the corresponding dataset, but pydov allows you to select and customize the fields you want to be returned in the output dataframe.


Using return fields
*******************

Next to the `query` and `location` parameters, you can use the ``return_fields`` parameter of the `search` method to limit the columns in the dataframe and/or specify extra columns not included by default. The `return_fields` parameter takes a list of field names, which can be any combination of the available fields for the dataset you're searching.

For example, to query the boreholes in Ghent but only retrieve their depth, you'd use::

  from pydov.search.boring import BoringSearch

  bs = BoringSearch()
  df = bs.search(query=PropertyIsEqualTo('gemeente', 'Gent'), return_fields=('pkey_boring', 'diepte_boring_tot'))


Note that you can not only use ``return_fields`` to limit the columns from the default dataframe for you can also add extra fields not included in this default set. The following example returns the purpose ('doel') of all the Ghent boreholes::

  from pydov.search.boring import BoringSearch

  bs = BoringSearch()
  df = bs.search(query=PropertyIsEqualTo('gemeente', 'Gent'), return_fields=('pkey_boring', 'doel'))


You can get an overview of the available fields for a dataset using its search objects `get_fields` method. More information can be found in the :ref:`available_attribute_fields` section.

.. note::

    Significant performance gains can be achieved by only including the fields you need, and more specifically by including only fields with a cost of 1. More information can be found in the :ref:`performance` section below.

    For instance, in the examples above only fields with a cost of 1 are selected, allowing the results to be retrieved almost instantly. By selecting only fields available in the WFS service (i.e. fields with a cost of 1), pydov only needs a single WFS query to obtain the results and doesn't need to download any additional XML documents.


Defining custom object types
****************************

Should you want to make the returned dataframe fields more permanent or, more importantly, add extra XML fields to an existing object type, you can define your own object types and subtypes.

pydov works internally with *search classes* (in pydov.search) and object *types* and *subtypes* (in pydov.types). The former are derived from :class:`pydov.search.abstract.AbstractSearch` and define the WFS services to be queried while the latter define which fields to retrieve from the WFS and XML services for inclusion in the resulting dataframe.

An object main type (derived from :class:`pydov.types.abstract.AbstractDovType`, f.ex. GrondwaterFilter) can contain fields from both the WFS service as well as from the XML document, noting that there will be a single instance of the main type per WFS record. On the contrary, an object subtype (derived from :class:`pydov.types.abstract.AbstractDovSubType`, f.ex. Peilmeting) can list only fields from the XML document and can have a many-to-one relation with the main type: i.e. there can be multiple instances of the subtype for a given instance of the main type (f.ex. a single GrondwaterFilter can have multiple Peilmetingen). In the resulting output both will be combined in a single, flattened, dataframe whereby there will be as many rows as instances from the subtype, repeating the values of the main type for each one.

.. figure:: objecttypes.svg
   :alt: UML schema of search classes, object types and subtypes
   :align: center

   UML schema of search classes, object types and subtypes

Search classes and object types are loosely coupled, each search class being linked to the default object type of the corresponding DOV object, allowing users to retrieve the default dataframe output when performing a search. However, to enable advanced customization of dataframe output columns at runtime, pydov allows for specifying an alternative object type upon creating an instance of the search classes. This system of 'pluggable types' enables users to extend the default type or subtype fields, or in fact rewrite them completely for their use-case.

The three most common reasons to define custom types are listed below: adding an extra XML field to a main type, a subtype or defining a new custom subtype altogether.


Adding an XML field to a main type
----------------------------------

To add an extra XML field to an existing main type, you have to create a subclass and extend the base type's fields.

To extend the field list of the basetype, use its ``extend_fields`` class method, allowing the base object type to be unaffected by your changes. It takes a new list as its argument, containing the fields to be added. These should all be instances of :class:`pydov.types.fields.XmlField`. While it is possible to add instances of :class:`pydov.types.fields.WfsField` as well, this is generally not necessary as those can be used in the return_fields argument without being explicitly defined in the object type.

For example, to add the field 'methode_xy' to the Boring datatype, you'd write::

  from pydov.search.boring import BoringSearch
  from pydov.types.boring import Boring
  from pydov.types.fields import XmlField

  class MyBoring(Boring):
      fields = Boring.extend_fields([
          XmlField(name='methode_xy',
                   source_xpath='/boring/xy/methode_opmeten',
                   datatype='string')
      ])

  bs = BoringSearch(objecttype=MyBoring)
  df = bs.search(query=PropertyIsEqualTo('gemeente', 'Gent'))


Adding an XML field to a subtype
--------------------------------

To add an extra XML field to an existing subtype, you have to create a subclass of the subtype and extend its fields. You also have to subclass the main type in order to register your new subtype.

To extend the field list of the subtype, use its ``extend_fields`` class method, allowing the base subtype to be unaffected by your changes. It takes a new list as its argument, containing the fields to be added. These should all be instances of :class:`pydov.types.fields.XmlField`. The source_xpath will be interpreted relative to the base subtypes rootpath.

To register your new subtype in a custom main type, subclass the existing main type and overwrite its ``subtypes`` field with a new list containing your new subtype.

For example, to add the field 'opmeter' to the Peilmeting subtype, you'd write::

  from pydov.search.grondwaterfilter import GrondwaterFilterSearch
  from pydov.types.grondwaterfilter import GrondwaterFilter, Peilmeting
  from pydov.types.fields import XmlField

  class MyPeilmeting(Peilmeting):
      fields = Peilmeting.extend_fields([
          XmlField(name='opmeter',
                   source_xpath='/opmeter/naam',
                   datatype='string')
      ])

  class MyGrondwaterFilter(GrondwaterFilter):
      subtypes = [MyPeilmeting]

  fs = GrondwaterFilterSearch(objecttype=MyGrondwaterFilter)
  df = fs.search(query=PropertyIsEqualTo('gemeente', 'Gent'))


Adding a new subtype to a main type
-----------------------------------

To add a new subtype to an existing main type or, perhaps more likely, to replace the existing subtype of a main type, you have to specify the subtype and all of its fields. You also have to subclass the existing main type to register your subtype.

Your new subtype should be a direct subclass of :class:`pydov.types.abstract.AbstractDovSubType` and should implement both the ``rootpath`` as well as the ``fields`` variables. The rootpath is the XPath expression of the root instances of this subtype in the XML document and should always start with ``.//``. There will be one instance of this subtype (and, consequently, one row in the output dataframe) for each element matched by this XPath expression.

The fields should contain all the fields (or: columns in the output dataframe) of this new subtype. These should all be instances of :class:`pydov.types.fields.XmlField`. The source_xpath will be interpreted relative to the subtypes rootpath.

Suppose you are not interested in the actual measurements from the CPT data but are instead interested in the different techniques applied while measuring. To get a dataframe with the different techniques per CPT location, you'd create a new subtype and register it in your own CPT type::

  from pydov.search.sondering import SonderingSearch
  from pydov.types.abstract import AbstractDovSubType
  from pydov.types.sondering import Sondering
  from pydov.types.fields import XmlField

  class Technieken(AbstractDovSubType):

      rootpath = './/sondering/sondeonderzoek/penetratietest/technieken'

      fields = [
          XmlField(name='techniek_diepte',
                   source_xpath='/diepte_techniek',
                   datatype='float'),
          XmlField(name='techniek',
                   source_xpath='/techniek',
                   datatype='string')
          XmlField(name='techniek_andere',
                   source_xpath='/techniek_andere',
                   datatype='string')
      ]

  class MySondering(Sondering)
      subtypes = [Technieken]

  ms = SonderingSearch(objecttype=MySondering)
  df = ms.search(query=PropertyIsEqualTo('gemeente', 'Gent'))


Default dataframe columns
*************************

Boreholes (boringen)
--------------------
  .. csv-table:: Boreholes (boringen)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/1930-120730
    boornummer,1,string,kb15d28w-B164
    x,1,float,152301.0
    y,1,float,211682.0
    mv_mtaw,10,float,8.00
    start_boring_mtaw,1,float,8.00
    gemeente,1,string,Wuustwezel
    diepte_boring_van,10,float,0.00
    diepte_boring_tot,1,float,19.00
    datum_aanvang,1,date,1930-10-01
    uitvoerder,1,string,Smet - Dessel
    boorgatmeting,10,boolean,false
    diepte_methode_van,10,float,0.00
    diepte_methode_tot,10,float,19.00
    boormethode,10,string,droge boring

CPT measurements (sonderingen)
------------------------------
  .. csv-table:: CPT measurements (sonderingen)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_sondering,1,string,https://www.dov.vlaanderen.be/data/sondering/2002-010317
    x,1,float,142767
    y,1,float,221907
    start_sondering_mtaw,1,float,2.39
    diepte_sondering_van,1,float,0
    diepte_sondering_tot,1,float,16
    datum_aanvang,1,date,2002-07-04
    uitvoerder,1,string,MVG - Afdeling Geotechniek
    sondeermethode,1,string,continu elektrisch
    apparaat,1,string,200kN - RUPS
    datum_gw_meting,10,datetime,2002-07-04 13:50:00
    diepte_gw_m,10,float,1.2
    lengte,10,float,1.2
    diepte,10,float,1.2
    qc,10,float,0.68
    Qt,10,float,NaN
    fs,10,float,10
    u,10,float,7
    i,10,float,0.1

Groundwater screens (grondwaterfilters)
---------------------------------------

Mind that the timeseries contains two columns referring to the time: `datum` and `tijdstip`, with datatype `date`, respectively `string`. This distinction is required because the `tijdstip` field is not mandatory whereas the `date` is. It is up to the user to combine these fields in a datetime object if required.

  .. csv-table:: Groundwater screens (grondwaterfilters)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_filter,1,string,https://www.dov.vlaanderen.be/data/filter/1989-001024
    pkey_grondwaterlocatie,1,string,https://www.dov.vlaanderen.be/data/put/2017-000200
    gw_id,1,string,4-0053
    filternummer,1,string,1
    filtertype,1,string,peilfilter
    x,1,float,110490
    y,1,float,194090
    start_grondwaterlocatie_mtaw,1,float,NaN
    mv_mtaw,10,float,NaN
    gemeente,1,string,Destelbergen
    meetnet_code,10,string,1
    aquifer_code,10,string,0100
    grondwaterlichaam_code,10,string,CVS_0160_GWL_1
    regime,10,string,freatisch
    diepte_onderkant_filter,1,float,13
    lengte_filter,1,float,2
    datum,10,date,2004-05-18
    tijdstip,10,string,NaN
    peil_mtaw,10,float,4.6
    betrouwbaarheid,10,string,goed
    methode,10,string,peillint
    filterstatus,10,string,1
    filtertoestand,10,string,in rust

Groundwater samples (grondwatermonsters)
----------------------------------------
  .. csv-table:: Groundwater samples (grondwatermonsters)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_grondwatermonster,1,string,https://www.dov.vlaanderen.be/data/watermonster/2010-001344
    grondwatermonsternummer,1,string,2-0114/M2010
    pkey_grondwaterlocatie,1,string,https://www.dov.vlaanderen.be/data/put/2017-000096
    gw_id,1,string,2-0114
    pkey_filter,1,string,https://www.dov.vlaanderen.be/data/filter/1996-001085
    filternummer,1,string,1
    x,1,float,153030
    y,1,float,158805
    start_grondwaterlocatie_mtaw,1,float,129.88
    gemeente,1,string,Sint-Genesius-Rode
    datum_monstername,1,date,2020-01-20
    parametergroep,10,string,Zware metalen
    parameter,10,string,Hg
    detectie,10,string,<
    waarde,10,float,0.5
    eenheid,10,string,µg/l
    veld_labo,10,string,LABO

Formal stratigraphy (Formele stratigrafie)
------------------------------------------
  .. csv-table:: Formal stratigraphy (Formele stratigrafie)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_interpretatie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2002-227082
    pkey_boring,1,string,NaN
    pkey_sondering,1,string,https://www.dov.vlaanderen.be/data/sondering/1989-068788
    betrouwbaarheid_interpretatie,1,string,goed
    x,1,float,108455
    y,1,float,194565
    diepte_laag_van,10,float,0
    diepte_laag_tot,10,float,13
    lid1,10,string,Q
    relatie_lid1_lid2,10,string,T
    lid2,10,string,Q

Informal stratigraphy (Informele stratigrafie)
----------------------------------------------
  .. csv-table:: Informal stratigraphy (Informele stratigrafie)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_interpretatie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2016-290843
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/1893-073690
    pkey_sondering,1,string,NaN
    betrouwbaarheid_interpretatie,1,string,onbekend
    x,1,float,108900
    y,1,float,194425
    diepte_laag_van,10,float,0
    diepte_laag_tot,10,float,18.58
    beschrijving,10,string,Q

Hydrogeological stratigraphy (Hydrogeologische stratigrafie)
------------------------------------------------------------
  .. csv-table:: Hydrogeological stratigraphy (Hydrogeologische stratigrafie)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_interpretatie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2001-198755
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/1890-073688
    betrouwbaarheid_interpretatie,1,string,goed
    x,1,float,108773
    y,1,float,194124
    diepte_laag_van,10,float,0
    diepte_laag_tot,10,float,8
    aquifer,10,string,0110

Informal hydrogeological stratigraphy (Informele hydrogeologische stratigrafie)
-------------------------------------------------------------------------------
  .. csv-table:: Informal hydrogeological stratigraphy (Informele hydrogeologische stratigrafie)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_interpretatie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2003-297769
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/2003-147935
    betrouwbaarheid_interpretatie,1,string,goed
    x,1,float,208607
    y,1,float,210792
    diepte_laag_van,10,float,0
    diepte_laag_tot,10,float,1.5
    beschrijving,10,string,Quartair

Coded lithology (Gecodeerde lithologie)
---------------------------------------
  .. csv-table:: Coded lithology (Gecodeerde lithologie)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_interpretatie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2003-205091
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/2003-076348
    betrouwbaarheid_interpretatie,1,string,goed
    x,1,float,110601
    y,1,float,196625
    diepte_laag_van,10,float,4
    diepte_laag_tot,10,float,4.5
    hoofdnaam1_grondsoort,10,string,MZ
    hoofdnaam2_grondsoort,10,string,NaN
    bijmenging1_plaatselijk,10,boolean,False
    bijmenging1_hoeveelheid,10,string,N
    bijmenging1_grondsoort,10,string,SC
    bijmenging2_plaatselijk,10,boolean,NaN
    bijmenging2_hoeveelheid,10,string,NaN
    bijmenging2_grondsoort,10,string,NaN
    bijmenging3_plaatselijk,10,boolean,NaN
    bijmenging3_hoeveelheid,10,string,NaN
    bijmenging3_grondsoort,10,string,NaN

Geotechnical encoding (Geotechnische codering)
----------------------------------------------
  .. csv-table:: Geotechnical encoding (Geotechnische codering)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_interpretatie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2014-184535
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/1957-033538
    betrouwbaarheid_interpretatie,1,string,goed
    x,1,float,108851
    y,1,float,196510
    diepte_laag_van,10,float,1
    diepte_laag_tot,10,float,1.5
    hoofdnaam1_grondsoort,10,string,XZ
    hoofdnaam2_grondsoort,10,string,NaN
    bijmenging1_plaatselijk,10,boolean,NaN
    bijmenging1_hoeveelheid,10,string,NaN
    bijmenging1_grondsoort,10,string,NaN
    bijmenging2_plaatselijk,10,boolean,NaN
    bijmenging2_hoeveelheid,10,string,NaN
    bijmenging2_grondsoort,10,string,NaN
    bijmenging3_plaatselijk,10,boolean,NaN
    bijmenging3_hoeveelheid,10,string,NaN
    bijmenging3_grondsoort,10,string,NaN

Lithological descriptions (Lithologische beschrijvingen)
--------------------------------------------------------
  .. csv-table:: Lithological descriptions (Lithologische beschrijvingen)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_interpretatie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/2017-302166
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/2017-151410
    betrouwbaarheid_interpretatie,1,string,onbekend
    x,1,float,109491
    y,1,float,196700
    diepte_laag_van,10,float,0
    diepte_laag_tot,10,float,1
    beschrijving,10,string,klei/zand

Quaternary stratigraphy (Quartaire stratigrafie)
--------------------------------------------------------
  .. csv-table:: Quaternary stratigraphy (Quartaire stratigrafie)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_interpretatie,1,string,https://www.dov.vlaanderen.be/data/interpretatie/1999-057087
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/1941-000322
    betrouwbaarheid_interpretatie,1,string,onbekend
    x,1,float,128277
    y,1,float,178987
    diepte_laag_van,10,float,0
    diepte_laag_tot,10,float,8
    lid1,10,string,F1
    relatie_lid1_lid2,10,string,T
    lid2,10,string,F1

Borehole samples (grondmonsters)
--------------------------------
  .. csv-table:: Borehole samples (grondmonsters)
    :header-rows: 1

    Field,Cost,Datatype,Example
    pkey_grondmonster,1,string,https://www.dov.vlaanderen.be/data/grondmonster/2017-168758
    naam,1,string,N3A
    pkey_boring,1,string,https://www.dov.vlaanderen.be/data/boring/2005-003015
    boornummer,1,string,GEO-04/024-B6
    datum,1,date,nan
    x,1,float,123280
    y,1,float,188129
    gemeente,1,string,Wichelen
    diepte_van_m,1,float,5.9
    diepte_tot_m,1,float,6.05
    peil_van_mtaw,1,float,0.26
    peil_tot_mtaw,1,float,0.11
    monstertype,10,string,ongeroerd
    astm_naam,10,string,Organic silt
    grondsoort_bggg,10,string,humush. klei
    humusgehalte,10,float,15.6
    kalkgehalte,10,float,4.4
    uitrolgrens,10,float,50.4
    vloeigrens,10,float,86.4
    glauconiet,10,float,NaN
    korrelvolumemassa,10,float,NaN
    volumemassa,10,float,NaN
    watergehalte,10,float,NaN
    diameter,10,float,10
    fractie,10,float,0
    methode,10,string,ZEEFPROEF

