# -*- coding: utf-8 -*-
"""Module grouping classes for location based filters used for searching.

This module is designed to comply with the WFS 1.1.0 standard, implying
Filter Encoding 1.1 and GML 3.1.1.

"""
from numpy.compat import unicode

from owslib.etree import etree
from owslib.fes import (
    Or,
)


class AbstractLocation(object):
    """Abstract base class for location types (f.ex. point, box, polygon).

    Locations are GML elements, for inclusion in the WFS GetFeature request.
    As described in the Filter Encoding 1.1 standard, locations are expressed
    using GML 3.1.1.

    The initialisation should require all necessary parameters to construct
    a valid location of this type: i.e. all locations should be valid after
    initialisation.

    """
    def get_element(self):
        """Return the GML representation of the location.

        Returns
        -------
        etree.Element
            XML element of the GML representation of this location.
        """
        raise NotImplementedError


class AbstractLocationFilter(object):
    """Abstract base class for location filters (f.ex. within, dwithin).

    Location filters are ogc:SpatialOpsType elements, for inclusion in
    the WFS GetFeature request.

    The initialisation should accept at least a (subclass of)
    AbstractLocation and require all additional parameters that are required
    for a valid location filter of this type.

    One exception is the name of the geometry column to query: this is set
    automatically upon building the WFS GetFeature request using the
    `set_geometry_column` method.

    """
    def set_geometry_column(self, geometry_column):
        """Set the name of the geometry column to query.

        Parameters
        ----------
        geometry_column : str
            The name of the geometry column to query.

        """
        raise NotImplementedError

    def toXML(self):
        """Return the XML representation of the location filter.

        Should raise a RuntimeError when called before the geometry column
        is set through `set_geometry_column`: location filters without the
        geometry column name are invalid.

        Returns
        -------
        etree.Element
            XML element of this location filter.

        Raises
        ------
        RuntimeError
            When called before the geometry column name is set: location
            filters without the geometry column name are invalid.

        """
        raise NotImplementedError


class AbstractBinarySpatialFilter(AbstractLocationFilter):
    """Class representing a binary spatial filter.

    Binary spatial filters are ogc:BinarySpatialOpType elements, i.e. one of
    Equals, Disjoint, Touches, Within, Overlaps, Crosses, Intersects or
    Contains.

    """
    def __init__(self, type, location):
        """Initialise a Binary spatial filter.

        Parameters
        ----------
        type : str
            Type of this filter: one of Equals, Disjoint, Touches, Within,
            Overlaps, Crosses, Intersects or Contains.
        location : AbstractLocation
            An instance of a location to use as location for the Within
            filter.

        """
        self.location = location
        self.geom_column = ''

        self.element = etree.Element('{http://www.opengis.net/ogc}%s' % type)

        geom = etree.Element('{http://www.opengis.net/ogc}PropertyName')
        geom.text = self.geom_column

        self.element.append(geom)
        self.element.append(location.get_element())

    def set_geometry_column(self, geometry_column):
        """Set the name of the geometry column to query.

        Parameters
        ----------
        geometry_column : str
            The name of the geometry column to query.

        """
        self.geom_column = geometry_column
        geom = self.element.find('.//{http://www.opengis.net/ogc}PropertyName')
        geom.text = geometry_column

    def toXML(self):
        """Return the XML representation of the Within filter.

        Returns
        -------
        etree.Element
            XML element of this Within filter.

        Raises
        ------
        RuntimeError
            When called before the geometry column name is set: location
            filters without the geometry column name are invalid.

        """
        if self.geom_column == '':
            raise RuntimeError('Geometry column has not been set. Use '
                               '"set_geometry_column" to set it.')
        return self.element


class Box(AbstractLocation):
    """Class representing a box location, also known as bounding box,
    envelope, extent."""
    def __init__(self, minx, miny, maxx, maxy, epsg=31370):
        """Initialise a Box.

        To initialise a Box using GPS coordinates in decimal degrees,
        use epsg=4326 and enter the longitude range as `minx` and `maxx` and
        the latitude range as `miny` and `maxy`.

        Parameters
        ----------
        minx : float
            X coordinate of the lower left corner of the box.
        miny : float
            Y coordinate of the lower left corner of the box.
        maxx : float
            X coordinate of the upper right corner of the box.
        maxy : float
            Y coordinate of the upper right corner of the box.
        epsg : int, optional
            EPSG code of the coordinate reference system (CRS) of the
            coordinates specified in `minx`, `miny`, `maxx`, `maxy`. Defaults
            to 31370 (Belgian Lambert72).

        Raises
        ------
        ValueError
            If `maxx` is lower than or equal to `minx`.
            If `maxy` is lower than or equal to `miny`.

        """
        if maxx <= minx:
            raise ValueError("MaxX should be greater than MinX.")

        if maxy <= miny:
            raise ValueError("MaxY should be greater than MinY.")

        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

        self.element = etree.Element('{http://www.opengis.net/gml}Envelope')
        self.element.set('srsDimension', '2')
        self.element.set('srsName',
                         'http://www.opengis.net/gml/srs/epsg.xml#%i' % epsg)

        lower_corner = etree.Element('{http://www.opengis.net/gml}lowerCorner')
        lower_corner.text = '%0.6f %0.6f' % (self.minx, self.miny)
        self.element.append(lower_corner)

        upper_corner = etree.Element('{http://www.opengis.net/gml}upperCorner')
        upper_corner.text = '%0.6f %0.6f' % (self.maxx, self.maxy)
        self.element.append(upper_corner)

    def get_element(self):
        """Return the GML representation of the box.

        Returns
        -------
        etree.Element
            XML element of the GML representation of this box.

        """
        return self.element


class Point(AbstractLocation):
    """Class representing a point location."""
    def __init__(self, x, y, epsg=31370):
        """Initialise a Point.

        To initialise a Point using GPS coordinates in decimal degrees,
        use epsg=4326 and enter the longitude as `x` and the latitude as `y`.

        Parameters
        ----------
        x : float
            X coordinate (or longitude) of the point.
        y : float
            Y coordinate (or latitude) of the point.
        epsg : int, optional
            EPSG code of the coordinate reference system (CRS) of the
            coordinates specified in `x`, `y`. Defaults to
            31370 (Belgian Lambert72).

        """
        self.x = x
        self.y = y

        self.element = etree.Element('{http://www.opengis.net/gml}Point')
        self.element.set('srsDimension', '2')
        self.element.set('srsName',
                         'http://www.opengis.net/gml/srs/epsg.xml#%i' % epsg)

        coordinates = etree.Element('{http://www.opengis.net/gml}pos')
        coordinates.text = '%0.6f %0.6f' % (self.x, self.y)
        self.element.append(coordinates)

    def get_element(self):
        """Return the GML representation of the point.

        Returns
        -------
        etree.Element
            XML element of the GML representation of this point.
        """
        return self.element


class GmlObject(AbstractLocation):
    """Class representing a raw GML location, f.ex. gml:Surface or
    gml:MultiSurface."""
    def __init__(self, gml_element):
        """Initialise a GmlObject.

        Initialise a GmlObject from an existing XML element representing a
        GML location.

        Parameters
        ----------
        gml_element : etree.Element or str
            XML element of the GML location, either as etree.Element, bytes or
            string representation.
        """
        if type(gml_element) in (str, unicode):
            self.element = etree.fromstring(gml_element.encode('utf8'))
        elif type(gml_element) is bytes:
            self.element = etree.fromstring(gml_element)
        else:
            self.element = gml_element

    def get_element(self):
        """Return the GML representation of this location.

        Returns
        -------
        etree.Element
            XML element of the GML representation of this location.
        """
        return self.element


class Equals(AbstractBinarySpatialFilter):
    """Class representing a spatial Equals filter.

    A spatial Equals will return all points that are equal to another point.

    """
    def __init__(self, location):
        """Initialise an Equals filter.

        Parameters
        ----------
        location : AbstractLocation
            An instance of a location to use as location for the Equals
            filter.

        """
        super(Equals, self).__init__('Equals', location)


class Disjoint(AbstractBinarySpatialFilter):
    """Class representing a spatial Disjoint filter.

    A spatial Disjoint will return all points that are disjoint from a
    polygon or box location: i.e. that are not inside nor on the boundary.

    A spatial Disjoint is the inverse of a spatial Intersects.

    """
    def __init__(self, location):
        """Initialise a Disjoint filter.

        Parameters
        ----------
        location : AbstractLocation
            An instance of a location to use as location for the Disjoint
            filter.

        """
        super(Disjoint, self).__init__('Disjoint', location)


class Touches(AbstractBinarySpatialFilter):
    """Class representing a spatial Touches filter.

    A spatial Touches will return all points that touch a polygon or box
    location: i.e. that are on the boundary but not inside.

    """
    def __init__(self, location):
        """Initialise a Touches filter.

        Parameters
        ----------
        location : AbstractLocation
            An instance of a location to use as location for the Touches
            filter.

        """
        super(Touches, self).__init__('Touches', location)


class Within(AbstractBinarySpatialFilter):
    """Class representing a spatial Within filter.

    A spatial Within will return all points that are entirely within a
    polygon or box location (i.e. are not on the boundary).

    """
    def __init__(self, location):
        """Initialise a Within filter.

        Parameters
        ----------
        location : AbstractLocation
            An instance of a location to use as location for the Within
            filter.

        """
        super(Within, self).__init__('Within', location)


class Intersects(AbstractBinarySpatialFilter):
    """Class representing a spatial Intersects filter.

    A spatial Intersects will return all points that are within or on the
    boundary of a polygon or box location.

    A spatial Intersects is the inverse of a spatial Disjoint.

    """
    def __init__(self, location):
        """Initialise an Intersects filter.

        Parameters
        ----------
        location : AbstractLocation
            An instance of a location to use as location for the Intersects
            filter.

        """
        super(Intersects, self).__init__('Intersects', location)


class WithinDistance(AbstractLocationFilter):
    """Class representing a spatial DWithin filter.

    A spatial DWithin will return all points that are within a given
    distance of a certain location.

    """
    def __init__(self, location, distance, distance_units='meter'):
        """Initialise a WithinDistance filter.

        Parameters
        ----------
        location : AbstractLocation
            An instance of a location to use as location for the
            WithinDistance filter.
        distance : float
            Amount of distance units to use for the filter.
        distance_units : string, optional, defaults to 'meter'
            The distance unit of the value of `distance`.

        """
        self.location = location
        self.distance = distance
        self.distance_units = distance_units
        self.geom_column = ''

        self.element = etree.Element('{http://www.opengis.net/ogc}DWithin')

        geom = etree.Element('{http://www.opengis.net/ogc}PropertyName')
        geom.text = self.geom_column

        distance = etree.Element('{http://www.opengis.net/ogc}Distance')
        distance.set('units', self.distance_units)
        distance.text = '%0.6f' % self.distance

        self.element.append(geom)
        self.element.append(location.get_element())
        self.element.append(distance)

    def set_geometry_column(self, geometry_column):
        """Set the name of the geometry column to query.

        Parameters
        ----------
        geometry_column : str
            The name of the geometry column to query.

        """
        self.geom_column = geometry_column
        geom = self.element.find('.//{http://www.opengis.net/ogc}PropertyName')
        geom.text = geometry_column

    def toXML(self):
        """Return the XML representation of the WithinDistance filter.

        Returns
        -------
        etree.Element
            XML element of this WithinDistance filter.

        Raises
        ------
        RuntimeError
            When called before the geometry column name is set: location
            filters without the geometry column name are invalid.

        """
        if self.geom_column == '':
            raise RuntimeError('Geometry column has not been set. Use '
                               '"set_geometry_column" to set it.')
        return self.element


class GmlFilter(Or):
    """Class for construction a spatial filter expression from a GML
    3.1.1 document.
    """

    def __init__(self, gml, location_filter, location_filter_kwargs=None):
        """Initialise a spatial filter expression from a GML 3.1.1 string.

        Parameters
        ----------
        gml : str
            String representation of the GML document to parse.
        location_filter : AbstractLocationFilter
            Location filter to use for the geometries in the GML document.
        location_filter_kwargs : dict, optional
            Keyword-based arguments to pass to the `location_filter` on
            initialisation (with the exception of the `location` parameter,
            which is automatically parsed from the GML). Can be skipped in
            cases where the location_filter takes no extra arguments besides
            location.

        """
        self.gml = gml
        self.subelements = set()

        if location_filter_kwargs is None:
            location_filter_kwargs = {}

        self._parse_gml()

        if len(self.subelements) == 1:
            # WithinDistance(Point(0, 0), 0) is a hack to have a second
            # operation for the Or expression (that never returns a result).
            ops = [location_filter(GmlObject(self.subelements.pop()),
                                   **location_filter_kwargs),
                   WithinDistance(Point(0, 0), 0)]
        else:
            ops = [location_filter(GmlObject(e), **location_filter_kwargs)
                   for e in self.subelements]

        super(GmlFilter, self).__init__(ops)

    def _parse_gml(self):
        """Parse the GML string and add subelements for geometries."""
        gml_tree = etree.fromstring(self.gml.encode('utf8'))

        for e in gml_tree.findall(
                './/{http://www.opengis.net/gml}Surface'):
            self.subelements.add(e)

        for e in gml_tree.findall(
                './/{http://www.opengis.net/gml}MultiSurface'):
            self.subelements.add(e)

        for e in gml_tree.findall(
                './/{http://www.opengis.net/gml}LineString'):
            self.subelements.add(e)

        for e in gml_tree.findall(
                './/{http://www.opengis.net/gml}MultiLineString'):
            self.subelements.add(e)

        for e in gml_tree.findall(
                './/{http://www.opengis.net/gml}Point'):
            self.subelements.add(e)

        for e in gml_tree.findall(
                './/{http://www.opengis.net/gml}MultiPoint'):
            self.subelements.add(e)

        if len(self.subelements) == 0:
            raise ValueError('Failed to extract geometries from GML file.')
