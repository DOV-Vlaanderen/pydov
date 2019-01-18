.. _query_location:

=================
Query on location
=================

To find data based on its geographical location, we can use the ``location`` parameter of the search objects. This parameter takes a location filter expression as its argument, based on custom pydov location filters from the pydov.util.location module.

Location filter predicates
**************************
A location query consists of a location filter predicate and a location. pydov uses custom location filter predicates and custom locations, all defined in the pydov.util.location module.

You can use the following location filters:

Within
    Search for points entirely within a given location. This does not include points on the boundary.

    Example: ``Within(Box(200000, 211000, 205000, 214000))``

Intersects
    Search for points within or on the boundary of a given location.

    Example: ``Intersects(Box(200000, 211000, 205000, 214000))``

Touches
    Search for points on the boundary but not inside a given location.

    Example: ``Touches(Box(200000, 211000, 205000, 214000))``

Disjoint
    Search for points that don't share any part with the given location. This means points that are completely outside of a polygon and its boundary.

    Example: ``Disjoint(Box(200000, 211000, 205000, 214000))``

Equals
    Search for points exactly equal to the given location.

    Example: ``Equals(Point(200000, 205000))``


A special location filter exists for spatial buffers, requiring a location and a distance:

WithinDistance
    Search for points within a given distance from a given location. By default, the distance is expressed in meters, but this can optionally by changed with the `distance_unit` parameter.

    Example: ``WithinDistance(Point(200000, 205000), distance=100)``

    Example: ``WithinDistance(location=Point(200000, 205000), distance=1, distance_unit='kilometer')``


Using locations
***************
You can define three different types of locations for use in a spatial filter: a rectangular box, a point and a custom GML object.

Box
    A rectangular twodimensional box defined by its lower left and upper right corners. The coordinate order for creating a Box is: lower left (minimum) x, lower left y, upper right (maximum) x, upper right y.

    By default, boxes use the Belgian Lambert 72 coordinate reference system (EPSG:31370). Should you want to create a Box using GPS coordinates in decimal degrees, use the parameter `epsg` to change the coordinate reference system and enter the longitude range as `minx` and `maxx` and the latitude range as `miny` and `maxy`.

    Example: ``Box(94720, 186910, 112220, 202870)``

    Example: ``Box(3.6214, 50.9850, 3.8071, 51.1270, epsg=4326)``

Point
    A twodimensional point defined by its x and y coordinate.

    By default, points use the Belgian Lambert 72 coordinate reference system (EPSG:31370). Should you want to create a Point using GPS coordinates in decimal degrees, use the parameter `epsg` to change the coordinate reference system and enter the longitude as `x` and the latitude `y`.

    Example: ``Point(110680, 202030)``

    Example: ``Point(3.8071, 51.1270, epsg=4326)``

GmlObject
    A custom GML 3.1.1 object. This can be any point, multipoint, linestring, multicurve (multilinestring), polygon or multisurface (multipolygon). This needs to be valid GML 3.1.1 for inclusion in the WFS 1.1.0 GetFeature request that pydov uses internally to query the datasets.

    See also :ref:`gml_documents` below.

    ::

        with open('polygon.gml', 'r') as gmlfile:
            gml = gmlfile.read()

            gml_element = etree.fromstring(gml)
            gml_element = gml_element.find(
                './/{http://www.opengis.net/gml}Polygon')

            location = GmlObject(gml_element)

Logically combining location filter expressions
***********************************************
The same way you can combine multiple attribute filters in one query, you can also combine different location filter in one location query. With the same logical filters from OWSLib you can build advanced spatial queries by using the `And`, `Or` and `Not` predicates from the owslib.fes package.

Each of `And`, `Or` and `Not` take a list as argument, in the case of `And` and `Or` the list should consist of at least two items. Each item can be a simple location filter expression, another `And`, `Or` or `Not` expression or a GmlFilter, so you can nest different levels of location filters.

And
    Return results that match all listed location filters.

    Example: ``And([Within(Box(94720, 186910, 112220, 202870), WithinDistance(Point(94720, 186910), distance=200)])``

    Example: ``And([Disjoint(Box(94720, 186910, 112220, 202870), Disjoint(Box(194720, 286910, 212220, 302870)])``

Or
    Return results that match one or more listed location filters.

    Example: ``Or([Within(Box(94720, 186910, 112220, 202870), Within(Box(194720, 286910, 212220, 302870)])``

Not
    Return results that do not match any of the listed filters.

    Example: ``Not([Intersects(GmlObject(gml_element))])``


.. _gml_documents:

Using GML documents
*******************
To make it easy to use GML documents for spatial queries, there is a special location filter class for creating location filter expressions from GML documents: GmlFilter.

GmlFilter
    Build a location filter expression using a GML 3.1.1 document.

    Instead of a single location filter, this class builds a location filter expression from a given GML document (`gml`), location filter (`location_filter`, optionally with `location_filter_kwargs`) and a logical `combinator` (by default this is `Or`).

    Example: given a GML document containing polygons, this GmlFilter will return all results that are completely within *any one* of the polygons (using the default `Or` combinator, the equivalent of a spatial union):

    ::

        GmlFilter('polygons.gml', Within)

    Example: given a GML document containing polygons, this GmlFilter will return all results that are completely within *all* of the polygons (using the `And` combinator, the equivalent of a spatial intersection):

    ::

        GmlFilter('polygons.gml', Within, combinator=And)

    Example: given a GML document containing polygons (f.ex. Belgian communities), this GmlFilter will return all results that are completely disjoint from any of the polygons (i.e. are not inside of Belgium):

    ::

        GmlFilter('polygons.gml', Disjoint, combinator=And)


    Example: given a GML document containing linestrings, this GmlFilter will return all results that are within 500 meters of any one of the linestrings (using the default `Or` combinator, this is the equivalent of a spatial buffer followed by a spatial union):

    ::

        GmlFilter('lines.gml', WithinDistance, {'distance': 500})

    Example: given a GML document containing points, this GmlFilter will return all results that are within 5 kilometers of each of the points (using the `And` combinator, this is the equivalent of a spatial buffer followed by a spatial intersection):

    ::

        GmlFilter('points.gml', WithinDistance, {'distance': 5, 'distance_unit': 'kilometer'}, combinator=And)

