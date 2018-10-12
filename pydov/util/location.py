# -*- coding: utf-8 -*-
"""Module grouping classes for location based filters used for searching."""

from owslib.etree import etree


class AbstractLocation(object):
    """Abstract base class for location types (f.ex. point, box, polygon).

    Locations are GML elements, for inclusion in the WFS GetFeature request.

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

    Location filters are ogc:Filter elements, for inclusion in the WFS
    GetFeature request.

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

    def get_element(self):
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


class Box(AbstractLocation):
    """Class representing a box location, also known as bounding box,
    envelope, extent."""
    def __init__(self, minx, miny, maxx, maxy, epsg=31370):
        """Initialise a Box.

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
            coordinates specified as minx, miny, maxx, maxy. Defaults to
            31370 (Belgian Lambert72).

        """
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

        Parameters
        ----------
        x : float
            X coordinate of the point.
        y : float
            Y coordinate of the point.
        epsg : int, optional
            EPSG code of the coordinate reference system (CRS) of the
            coordinates specified as minx, miny, maxx, maxy. Defaults to
            31370 (Belgian Lambert72).

        """
        self.x = x
        self.y = y

        self.element = etree.Element('{http://www.opengis.net/gml}Point')
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


class Within(AbstractLocationFilter):
    """Class representing a spatial Within filter.

    A spatial Within will return all points that are within a polygon or
    box location.

    """
    def __init__(self, location):
        """Initialise a Within filter.

        Parameters
        ----------
        location : AbstractLocation
            An instance of a location to use as location for the Within
            filter.

        """
        self.location = location
        self.geom_column = ''

        self.element = etree.Element('{http://www.opengis.net/ogc}Within')

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

    def get_element(self):
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


class WithinDistance(AbstractLocationFilter):
    """Class representing a spatial DWithin filter.

    A spatial DWithin will return all points that are within a given
    distance of a certain location.

    """
    def __init__(self, point, distance, distance_units='meter'):
        """Initialise a WithinDistance filter.

        Parameters
        ----------
        point : Point
            Instance of a Point location to use as location for the
            WithinDistance filter.
        distance : float
            Amount of distance units to use for the filter.
        distance_units : string, optional, defaults to 'meter'
            The distance unit of the value of `distance`.

        """
        self.point = point
        self.distance = distance
        self.distance_units = distance_units
        self.geom_column = ''

        self.element = etree.Element('{http://www.opengis.net/ogc}DWithin')

        geom = etree.Element('{http://www.opengis.net/ogc}PropertyName')
        geom.text = self.geom_column

        distance = etree.Element('{http://www.opengis.net/ogc}Distance')
        distance.set('units', self.distance_units)
        distance.text = '%f' % self.distance

        self.element.append(geom)
        self.element.append(point.get_element())
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

    def get_element(self):
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
