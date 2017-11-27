DovGrondwaterFilter object
==========================

Het DOVGrondwaterFilter object bevat alle data van een zoekactie op de laag meetnetten.

Acherliggend zit de meeste informatie vervat in 3 dataframes:

 * ligging: bevat de ligging (xyz)
 * observaties
 * peilmetingen


Ligging
~~~~~~~
In deze dataframe komen dezelfde velden als bij het zoeken in de site:

 * GW-ID
 * Filternr
 * Filtertype
 * X (mL72)
 * Y (mL72)
 * Z (mTAW)
 * Gemeente
 * Deelgemeente
 * Meetnet
 * Aquifer
 * Grondwaterlichaam
 * Onderkant filter(m)
 * Lengte filter(m)

Observaties
~~~~~~~~~~~

In deze dataframe worden volgende velden gegeven:
 * grondwaterlocatie
 * filternummer
 * diepte
 * methode
 * betrouwbaarheid

Peilmetingen
~~~~~~~~~~~~
* grondwaterlocatie
* filternummer
* monsternummer
* datum (monstername)
* parameter
* detectie (opm: nu niet in xml)
* waarde
* eenheid
* betrouwbaarheid
