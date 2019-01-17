.. _endpoints:

==================
Accessing DOV data
==================

DOV manages and publishes a lot of data about the soil, subsoil and groundwater of Flanders. Next to our userfriendly and easy-to-use `web applications <https://www.dov.vlaanderen.be/portaal>`_ like the 'DOV Verkenner', all of our data is also available in various publicly available services providing standards-based access to our content.

This document describes the standards and endpoints we use so you'll be able to find the data you need and use it in your projects.

A quick overview of the endpoints and standards that are described in more detail below:


* Discovering data: `DOV metadata catalogue <https://www.dov.vlaanderen.be/geonetwork>`_\ , using `INSPIRE <https://inspire.ec.europa.eu/documents/inspire-metadata-implementing-rules-technical-guidelines-based-en-iso-19115-and-en-iso-1>`_ guidelines based on ISO 19115, ISO 19119 and the `OGC CSW <http://www.opengeospatial.org/standards/cat>`_ standard.
* Viewing data: `DOV WMS service <https://www.dov.vlaanderen.be/geoserver/wms?request=GetCapabilities>`_\ , using the `OGC WMS <http://www.opengeospatial.org/standards/wms>`_ standard.
* Accessing data:

  * Accessing vector maps: `DOV WFS service <https://www.dov.vlaanderen.be/geoserver/wfs?request=GetCapabilities>`_\ , using the `OGC WFS <http://www.opengeospatial.org/standards/wfs>`_ standard.
  * Accessing raster grids: `DOV WCS service <https://www.dov.vlaanderen.be/geoserver/wcs?request=GetCapabilities>`_\ , using the `OGC WCS <http://www.opengeospatial.org/standards/wcs>`_ standard.
  * Accessing raw data: services providing raw XML data in the `DOV schema <https://www.dov.vlaanderen.be/xdov/schema/latest/xsd/kern/dov.xsd>`_

Discovering data
----------------

To get an overview of the datasets we publish, you can use our `metadata catalogue <https://www.dov.vlaanderen.be/geonetwork>`_. We maintain a metadata record for all datasets we manage and publish, according to the `INSPIRE implementing rules <https://inspire.ec.europa.eu/documents/inspire-metadata-implementing-rules-technical-guidelines-based-en-iso-19115-and-en-iso-1>`_ regarding metadata records, based in turn on the ISO 19115, ISO 19119 and `OGC CSW <http://www.opengeospatial.org/standards/cat>`_ standards.

To find the dataset of your interest you can either use the web interface at https://www.dov.vlaanderen.be/geonetwork, or use the CSW endpoint located at ``https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw``. We support version 2.0.2 of the CSW standard.

Each metadata record has a section describing where the dataset can be obtained. All layers we publish should have a WMS service associated with them, next to a WFS service for vector and an WCS service for raster data.

For increased usability and discoverability we group some of our metadata records into records of the type 'datasetseries'. This way we organise our dataset records into hierarchical trees, for example grouping projects like G3Dv2 or H3O which include a lot of datasets.

Some of our metadata records have a feature catalogue associated with them, describing each attribute of the feature type in more detail. We plan on adding more of these feature catalogues to our metadata records in the future.

Examples
~~~~~~~~

Metadata record describing the dataset 'Grondwatermeetnetten', in HTML:

..

   https://www.dov.vlaanderen.be/geonetwork/?uuid=6c39d716-aecc-4fbc-bac8-4f05a49a78d5


----

Metadata record describing the dataset 'Grondwatermeetnetten', in ISO 19115 XML:

..

   https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw?Service=CSW&Request=GetRecordById&Version=2.0.2&outputSchema=http://www.isotc211.org/2005/gmd&elementSetName=full&id=6c39d716-aecc-4fbc-bac8-4f05a49a78d5


Endpoints
~~~~~~~~~


* `CSW GetCapabilities, version 2.0.2 <https://www.dov.vlaanderen.be/geonetwork/srv/dut/csw?Service=CSW&Request=GetCapabilities&version=2.0.2>`_

More information
~~~~~~~~~~~~~~~~


* `OGC CSW standard <http://www.opengeospatial.org/standards/cat>`_
* `INSPIRE implementing rules on metadata <https://inspire.ec.europa.eu/documents/inspire-metadata-implementing-rules-technical-guidelines-based-en-iso-19115-and-en-iso-1>`_

Viewing data
------------

To display the layers we publish on a map, you can use our `WMS service <https://www.dov.vlaanderen.be/geoserver/wms?request=GetCapabilities>`_. We support versions 1.1.1 and 1.3.0 of the WMS protocol.

Note that the result of a WMS request is an image, which makes it ideal for use in a web viewer or as a background layer in your local GIS application. If you need access to the data itself, you can use the WFS (for vector data) or WCS services (for raster data) which are described below.

We support a limited number of coordinate systems in our WMS service, all of them except EPSG:31370 (Lambert72, which is the native coordinate system of our data) are transformed on the fly.

Examples
~~~~~~~~

PNG image of a detail of the soil map (bodemtypes) in the Lambert72 coordinate system.

..

   https://www.dov.vlaanderen.be/geoserver/bodemkaart/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&FORMAT=image%2Fpng8&TRANSPARENT=true&LAYERS=bodemkaart%3Abodemtypes&STYLES&SRS=EPSG%3A31370&WIDTH=768&HEIGHT=330&BBOX=141884.87421969333%2C198790.57243614786%2C145549.7443438222%2C200365.3213176095


Endpoints
~~~~~~~~~


* `WMS GetCapabilities, version 1.1.1 <https://www.dov.vlaanderen.be/geoserver/wms?request=getcapabilities&service=wms&version=1.1.1>`_
* `WMS GetCapabilities, version 1.3.0 <https://www.dov.vlaanderen.be/geoserver/wms?request=getcapabilities&service=wms&version=1.3.0>`_

More information
~~~~~~~~~~~~~~~~


* `OGC WMS standard <http://www.opengeospatial.org/standards/wms>`_
* `Geoserver WMS implementation <http://docs.geoserver.org/stable/en/user/services/wms/index.html>`_

Accessing data
--------------

There are three ways of accessing data published by DOV. To get the data behind the layers we publish in our WMS service, you can use either the `WFS service <https://www.dov.vlaanderen.be/geoserver/wfs?request=GetCapabilities>`_ (for vector data) or the `WCS service <https://www.dov.vlaanderen.be/geoserver/wcs?request=GetCapabilities>`_ (for raster data).

Some of the data we publish is also available in an interactive web application as well as in an XML representation.

.. _vector_wfs:

Using vector data
~~~~~~~~~~~~~~~~~

We offer a vector version of our map layers through the `OGC WFS <http://www.opengeospatial.org/standards/wfs>`_ standard. We support versions 1.0.0, 1.1.0 and 2.0.0 of the WFS protocol.

WFS supports advanced spatial and non-spatial querying and the resulting data can be obtained in various formats including GML, KML, JSON and CSV.

We support a limited number of coordinate systems in our WFS service, all of them except EPSG:31370 (Lambert72, which is the native coordinate system of our data) are transformed on the fly. The maximum number of features returned by any WFS request is 10000, if you reach this many features in your query you should split the problem in multiple requests.

Examples
""""""""

All CPT's (sonderingen) linked to project 'GEO-02/126' in GML format:

..

   https://www.dov.vlaanderen.be/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=dov-pub:Sonderingen&CQL_FILTER=opdrachten=%27GEO-02/126%27


----

All boreholes (boringen) deeper than 2000 m in JSON format:

..

   https://www.dov.vlaanderen.be/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=dov-pub:Boringen&CQL_FILTER=diepte_tot_m%3E2000&outputFormat=json


----

All hydrogeologic interpretations of boreholes created last year in KML format:

..

   https://www.dov.vlaanderen.be/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=interpretaties:hydrogeologische_stratigrafie&CQL_FILTER=Type_proef=%27Boring%27%20and%20Datum%3E=2016-01-01%20and%20Datum%3C2017-01-01&outputFormat=KML


----

Permanent URLs of all groundwater screens in Wuustwezel that have water level measurements later than January 1st 2017 in CSV format:

..

   https://www.dov.vlaanderen.be/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=gw_meetnetten:meetnetten&propertyname=filterfiche&CQL_Filter=peilmetingen_tot%3E2017-01-01%20and%20gemeente=%27Wuustwezel%27&outputFormat=csv


Endpoints
"""""""""


* `WFS GetCapabilities, version 1.0.0 <https://www.dov.vlaanderen.be/geoserver/wfs?request=getcapabilities&service=wfs&version=1.0.0>`_
* `WFS GetCapabilities, version 1.1.0 <https://www.dov.vlaanderen.be/geoserver/wfs?request=getcapabilities&service=wfs&version=1.1.0>`_
* `WFS GetCapabilities, version 2.0.0 <https://www.dov.vlaanderen.be/geoserver/wfs?request=getcapabilities&service=wfs&version=2.0.0>`_

More information
""""""""""""""""

* `OGC WFS standard <http://www.opengeospatial.org/standards/wfs>`_
* `Geoserver WFS implementation <http://docs.geoserver.org/stable/en/user/services/wfs/index.html>`_

Using raster data
~~~~~~~~~~~~~~~~~

The raw raster data of the grids published in our WMS service can be obtained using our `OGC WCS <http://www.opengeospatial.org/standards/wcs>`_ service. We support versions 1.0.0, 1.1.1 and 2.0.1 of the WCS protocol.

We support a limited number of coordinate systems in our WCS service, all of them except EPSG:31370 (Lambert72, which is the native coordinate system of our data) are transformed on the fly.

Examples
""""""""

Excerpt of the base of the geological Formation of Tienen in the GeoTiff format (MIME encoded):

..

   https://www.dov.vlaanderen.be/geoserver/wcs?version=1.1.0&request=GetCoverage&service=WCS&format=geotiff&identifier=g3dv2_0314_PA_Ti&BoundingBox=188200,163000,200000,171000,urn:ogc:def:crs:EPSG::31370


Endpoints
"""""""""


* `WCS GetCapabilities, version 1.0.0 <https://www.dov.vlaanderen.be/geoserver/wcs?request=getcapabilities&service=wcs&version=1.0.0>`_
* `WCS GetCapabilities, version 1.1.1 <https://www.dov.vlaanderen.be/geoserver/wcs?request=getcapabilities&service=wcs&version=1.1.1>`_
* `WCS GetCapabilities, version 2.0.1 <https://www.dov.vlaanderen.be/geoserver/wcs?request=getcapabilities&service=WCS&version=2.0.1>`_

More information
""""""""""""""""


* `OGC WCS standard <http://www.opengeospatial.org/standards/wcs>`_
* `Geoserver WCS implementation <http://docs.geoserver.org/stable/en/user/services/wcs/index.html>`_

.. _xml_data:

Using XML data
~~~~~~~~~~~~~~

For some core feature types DOV has custom applications to enter, edit, import and export the data. These are the feature types that are used most often in our daily business, including:


* Boringen (boreholes)
* Sonderingen (cone penetration tests)
* Interpretaties, including: (descriptive and (hydro-) geological interpretations of boreholes and CPT's)

  * Formele stratigrafie
  * Gecodeerde lithologie
  * Geotechnische coderingen
  * Hydrogeologische stratigrafie
  * Informele hydrogeologische stratigrafie
  * Informele stratigrafie
  * Lithologische beschrijvingen
  * Quartaire stratigrafie

* Putten (groundwater locations)
* Filters (groundwater screens)

Each feature of these feature types is uniquely and permanently identifiable by its URL starting with ``https://www.dov.vlaanderen.be/data/``. This URL resolves to an interactive HTML view of the feature. To obtain an XML representation of the same object according to the `DOV schema <https://www.dov.vlaanderen.be/xdov/schema/latest/xsd/kern/dov.xsd>`_\ , you can append ``.xml`` to the URL.

For each of these feature types we also provide a map layer that contains all features and some key attributes, including the permanent URL described above. This allows using the map layer to search and identify features of interest (using the WFS service) and subsequently get their XML representation through the permanent URL.

A short overview of the map layers including permanent URL's can be found below. Please note that a detailed description of each dataset and its attributes can be found in our `metadata catalogue <https://www.dov.vlaanderen.be/geonetwork>`_\ , linked to in the first column:

.. list-table::
   :header-rows: 1

   * - Featuretype
     - Feature catalogue (fc)
     - WFS layer
     - Permanent URL base
   * - `Boringen <https://www.dov.vlaanderen.be/geonetwork/?uuid=4e20bf9c-3a5c-42be-b5b6-bef6214d1fa7>`_
     - `Boringen fc <https://www.dov.vlaanderen.be/geonetwork/?uuid=c0cbd397-520f-4ee1-aca7-d70e271eeed6>`_
     - dov-pub:Boringen
     - ``https://www.dov.vlaanderen.be/data/boring/``
   * - `Sonderingen <https://www.dov.vlaanderen.be/geonetwork/?uuid=b397faec-1b64-4854-8000-2375edb3b1a8>`_
     - `Sonderingen fc <https://www.dov.vlaanderen.be/geonetwork/?uuid=bd539ba5-5f4d-4c43-9662-51c16caea351>`_
     - dov-pub:Sonderingen
     - ``https://www.dov.vlaanderen.be/data/sondering/``
   * - `Formele stratigrafie <https://www.dov.vlaanderen.be/geonetwork/?uuid=212af8cd-bffd-423c-9d2b-69c544ab3b04>`_
     - `Formele stratigrafie fc <https://www.dov.vlaanderen.be/geonetwork/?uuid=68405b5d-51e6-44d0-b634-b580bc2f9eb6>`_
     - interpretaties:formele_stratigrafie
     - ``https://www.dov.vlaanderen.be/data/interpretatie/``
   * - `Gecodeerde lithologie <https://www.dov.vlaanderen.be/geonetwork/?uuid=35d630e4-9145-46f9-b7dc-da290a0adc55>`_
     - `Gecodeerde lithologie fc <https://www.dov.vlaanderen.be/geonetwork/?uuid=0032241d-8920-415e-b1d8-fa0a48154904>`_
     - interpretaties:gecodeerde_lithologie
     - ``https://www.dov.vlaanderen.be/data/interpretatie/``
   * - `Geotechnische coderingen <https://www.dov.vlaanderen.be/geonetwork/?uuid=6a3dc5d4-0744-4d9c-85ce-da50913851cc>`_
     - `Geotechnische coderingen fc <https://www.dov.vlaanderen.be/geonetwork/?uuid=85404aa6-2d88-46f6-ae5a-575aece71efd>`_
     - interpretaties:geotechnische_coderingen
     - ``https://www.dov.vlaanderen.be/data/interpretatie/``
   * - `Hydrogeologische stratigrafie <https://www.dov.vlaanderen.be/geonetwork/?uuid=25c5d9fa-c2ba-4184-b796-fde790e73d39>`_
     - `Hydrogeologische stratigrafie fc <https://www.dov.vlaanderen.be/geonetwork/?uuid=b89e72de-35a9-4bca-8d0b-712d1e881ea6>`_
     - interpretaties:hydrogeologische_stratigrafie
     - ``https://www.dov.vlaanderen.be/data/interpretatie/``
   * - `Informele hydrogeologische stratigrafie <https://www.dov.vlaanderen.be/geonetwork/?uuid=ca1d704a-cdee-4968-aa65-9c353863e4b1>`_
     - `Informele hydrogeologische stratigrafie fc <https://www.dov.vlaanderen.be/geonetwork/?uuid=69f71840-bd29-4b59-9b02-4e36aafaa041>`_
     - interpretaties:informele_hydrogeologische_stratigrafie
     - ``https://www.dov.vlaanderen.be/data/interpretatie/``
   * - `Informele stratigrafie <https://www.dov.vlaanderen.be/geonetwork/?uuid=bd171ea4-2509-478d-a21c-c2728d3a9051>`_
     - `Informele stratigrafie fc <https://www.dov.vlaanderen.be/geonetwork/?uuid=b6c651f9-5972-4252-ae10-ad69ad08e78d>`_
     - interpretaties:informele_stratigrafie
     - ``https://www.dov.vlaanderen.be/data/interpretatie/``
   * - `Lithologische beschrijvingen <https://www.dov.vlaanderen.be/geonetwork/?uuid=45b5610e-9a66-42bd-b920-af099e399f3b>`_
     - `Lithologische beschrijvingen fc <https://www.dov.vlaanderen.be/geonetwork/?uuid=2450d592-29bc-4970-a89f-a7b14bd38dc2>`_
     - interpretaties:lithologische_beschrijvingen
     - ``https://www.dov.vlaanderen.be/data/interpretatie/``
   * - `Quartaire stratigrafie <https://www.dov.vlaanderen.be/geonetwork/?uuid=8b204ed6-e44c-4567-bbe8-bd427eba082c>`_
     - `Quartaire stratigrafie fc <https://www.dov.vlaanderen.be/geonetwork/?uuid=d40ef884-3278-45db-ad69-2c2a8c3981c3>`_
     - interpretaties:quartaire_stratigrafie
     - ``https://www.dov.vlaanderen.be/data/interpretatie/``
   * - `Grondwatermeetnetten <https://www.dov.vlaanderen.be/geonetwork/?uuid=6c39d716-aecc-4fbc-bac8-4f05a49a78d5>`_
     - `Grondwatermeetnetten fc <https://www.dov.vlaanderen.be/geonetwork/?uuid=b142965f-b2aa-429e-86ff-a7cb0e065d48>`_
     - gw_meetnetten:meetnetten
     - ``https://www.dov.vlaanderen.be/data/put``\ , ``https://www.dov.vlaanderen.be/data/filter``


Examples
""""""""

The HTML representation of borehole '1407-B4':

..

   https://www.dov.vlaanderen.be/data/boring/2017-148917


----

The XML representation of borehole '1407-B4':

..

   https://www.dov.vlaanderen.be/data/boring/2017-148917.xml


Endpoints
"""""""""


* We do not provide an endpoint to get all features of a feature type as XML. You should use the WFS endpoint of the corresponding map layer to get the permanent URL of the features of interest to you and get their XML representation in a second step.

More information
""""""""""""""""


* `DOV XML documentation <https://www.dov.vlaanderen.be/page/dov-uitwisselingsformaat>`_
* `DOV XSD schema <https://www.dov.vlaanderen.be/xdov/schema/latest/xsd/kern/dov.xsd>`_
