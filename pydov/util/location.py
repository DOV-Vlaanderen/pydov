# -*- coding: utf-8 -*-
"""Module grouping classes for location based filters used for searching.

This module is designed to comply with the WFS 2.0.0 standard, implying
Filter Encoding 2.0 and GML 3.2.

"""
import os
from collections import OrderedDict
from packaging.version import Version
from io import BytesIO
import random
import string

from owslib.etree import etree
from owslib.fes2 import Or


class AbstractLocation(object):
    """Abstract base class for location types (f.ex. point, box, polygon).

    Locations are GML elements, for inclusion in the WFS GetFeature request.
    As described in the Filter Encoding 2.0 standard, locations are expressed
    using GML 3.2.

    The initialisation should require all necessary parameters to construct
    a valid location of this type: i.e. all locations should be valid after
    initialisation.

    """

    def _get_id(self):
        random_id = ''.join(random.choice(
            string.ascii_letters + string.digits) for x in range(8))
        return f'pydov.{random_id}'

    def get_element(self):
        """Return the GML representation of the location.

        Returns
        -------
        etree.Element
            XML element of the GML representation of this location.
        """
        raise NotImplementedError('This should be implemented in a subclass.')


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
        raise NotImplementedError('This should be implemented in a subclass.')

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
        raise NotImplementedError('This should be implemented in a subclass.')


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
            An instance of a location to use as location for the spatial
            filter.

        """
        self.location = location
        self.geom_column = ''

        self.element = etree.Element(
            '{{http://www.opengis.net/fes/2.0}}{}'.format(type))

        geom = etree.Element('{http://www.opengis.net/fes/2.0}ValueReference')
        geom.text = self.geom_column

        self.element.append(geom)
        self.element.append(location.get_element())

    def set_geometry_column(self, geometry_column):
        self.geom_column = geometry_column
        geom = self.element.find(
            './/{http://www.opengis.net/fes/2.0}ValueReference')
        geom.text = geometry_column

    def toXML(self):
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

        self.element = etree.Element(
            '{http://www.opengis.net/gml/3.2}Envelope')
        self.element.set('srsDimension', '2')
        self.element.set(
            'srsName',
            'http://www.opengis.net/gml/srs/epsg.xml#{:d}'.format(epsg))
        self.element.set('{http://www.opengis.net/gml/3.2}id', self._get_id())

        lower_corner = etree.Element(
            '{http://www.opengis.net/gml/3.2}lowerCorner')
        lower_corner.text = '{:.06f} {:.06f}'.format(self.minx, self.miny)
        self.element.append(lower_corner)

        upper_corner = etree.Element(
            '{http://www.opengis.net/gml/3.2}upperCorner')
        upper_corner.text = '{:.06f} {:.06f}'.format(self.maxx, self.maxy)
        self.element.append(upper_corner)

    def get_element(self):
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

        self.element = etree.Element('{http://www.opengis.net/gml/3.2}Point')
        self.element.set('srsDimension', '2')
        self.element.set(
            'srsName',
            'http://www.opengis.net/gml/srs/epsg.xml#{:d}'.format(epsg))
        self.element.set('{http://www.opengis.net/gml/3.2}id', self._get_id())

        coordinates = etree.Element('{http://www.opengis.net/gml/3.2}pos')
        coordinates.text = '{:.06f} {:.06f}'.format(self.x, self.y)
        self.element.append(coordinates)

    def get_element(self):
        return self.element


class GmlObject(AbstractLocation):
    """Class representing a raw GML3.2 location, f.ex. gml32:Surface or
    gml32:MultiSurface."""

    def __init__(self, gml_element):
        """Initialise a GmlObject.

        Initialise a GmlObject from an existing XML element representing a
        GML3.2 location.

        Parameters
        ----------
        gml_element : etree.Element or str or bytes
            XML element of the GML3.2 location, either as etree.Element,
            bytes or string representation.

        """
        if isinstance(gml_element, str):
            self.element = etree.fromstring(gml_element.encode('utf8'))
        elif isinstance(gml_element, bytes):
            self.element = etree.fromstring(gml_element)
        else:
            self.element = gml_element

        if self.element.find('.//{http://www.opengis.net/gml/3.2}*') is None:
            if self.element.find(
                    './/{http://www.opengis.net/gml}*') is not None:
                raise ValueError(
                    'GML element should be GML version 3.2, it appears to be '
                    'older.')

            raise ValueError('GML element appears not to be valid GML3.2')

    def get_element(self):
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

    def __init__(self, location, distance, distance_unit='meter'):
        """Initialise a WithinDistance filter.

        Parameters
        ----------
        location : AbstractLocation
            An instance of a location to use as location for the
            WithinDistance filter.
        distance : float
            Amount of distance units to use for the filter.
        distance_unit : string, optional, defaults to 'meter'
            The distance unit of the value of `distance`.

        """
        self.location = location
        self.distance = distance
        self.distance_unit = distance_unit
        self.geom_column = ''

        self.element = etree.Element('{http://www.opengis.net/fes/2.0}DWithin')

        geom = etree.Element('{http://www.opengis.net/fes/2.0}ValueReference')
        geom.text = self.geom_column

        distance = etree.Element('{http://www.opengis.net/fes/2.0}Distance')
        distance.set('units', self.distance_unit)
        distance.text = '{:.06f}'.format(self.distance)

        self.element.append(geom)
        self.element.append(location.get_element())
        self.element.append(distance)

    def set_geometry_column(self, geometry_column):
        self.geom_column = geometry_column
        geom = self.element.find(
            './/{http://www.opengis.net/fes/2.0}ValueReference')
        geom.text = geometry_column

    def toXML(self):
        if self.geom_column == '':
            raise RuntimeError('Geometry column has not been set. Use '
                               '"set_geometry_column" to set it.')
        return self.element


class GmlFilter(AbstractLocationFilter):
    """Class for construction a spatial filter expression from a GML3.2
    document.
    """

    def __init__(self, gml, location_filter, location_filter_kwargs=None,
                 combinator=Or):
        """Initialise a spatial filter expression from a GML3.2 string.

        Parameters
        ----------
        gml : str
            Either a string representation of the GML document to parse,
            or a path to a GML3.2 file on disk.
        location_filter : class<AbstractLocationFilter>
            Location filter to use for the geometries in the GML document.
        location_filter_kwargs : dict, optional
            Keyword-based arguments to pass to the `location_filter` on
            initialisation (with the exception of the `location` parameter,
            which is automatically parsed from the GML). Can be skipped in
            cases where the location_filter takes no extra arguments besides
            location.
        combinator : class<BinaryLogicOpType>, optional, defaults to Or
            One of (Or, And) used to combine filters for different geometries
            in the GML document.

        Raises
        ------
        ValueError
            When no geometries could be parsed from the given GML record.

        """
        self.gml = gml
        self.subelements = OrderedDict()

        if location_filter_kwargs is None:
            location_filter_kwargs = {}

        self._parse_gml()

        if len(self.subelements) == 1:
            self.element = location_filter(
                GmlObject(list(self.subelements)[0]),
                **location_filter_kwargs)
        else:
            self.element = combinator(
                [location_filter(GmlObject(e), **location_filter_kwargs)
                 for e in self.subelements])

    def _dedup_multi(self, tree, xpath_single, xpath_multi):
        """Parse single and multi* geometries from the same type from the
        GML tree. Deduplicates in the sense that single geometries inside a
        multi* geometry will be discarded in favor of the latter.

        Parameters
        ----------
        tree : etree.ElementTree
            XML tree of the GML to parse.
        xpath_single : str
            XPath of the single geometries to parse.
        xpath_multi : str
            XPath of the multi* geometries to parse.

        Returns
        -------
        single, multi : set of etree.Element, set of etree.Element
            Sets of the parsed single and multi geometry Elements.

        """
        single = OrderedDict.fromkeys(tree.findall(xpath_single))
        multi = OrderedDict.fromkeys(tree.findall(xpath_multi))

        for m in multi:
            s_in_m = OrderedDict.fromkeys(m.findall(xpath_single))
            single = OrderedDict.fromkeys(e for e in single if e not in s_in_m)

        return single, multi

    def _parse_gml(self):
        """Checks the gml parameter and tries parsing the file.

        Raises
        ------
        ValueError
            When the file could not be parsed.

        """
        gml_tree = None
        try:
            if isinstance(self.gml, str):
                gml_tree = etree.fromstring(self.gml.encode('utf8'))
            elif isinstance(self.gml, bytes):
                gml_tree = etree.fromstring(self.gml)
        except etree.ParseError as error:
            if os.path.isfile(self.gml):
                with open(self.gml, 'r') as gml_file:
                    gml_tree = etree.fromstring(gml_file.read().encode('utf8'))
            else:
                raise error
        finally:
            if gml_tree is not None:
                self._parse_gml_tree(gml_tree)
            else:
                raise ValueError('Failed to parse GML3.2 file.')

    def _parse_gml_tree(self, gml_tree):
        """Parse the GML tree and add subelements for geometries.

        Parameters
        ----------
        gml_tree : etree.ElementTree
            XML tree of the GML to parse.

        Raises
        ------
        ValueError
            When no geometries could be parsed from the given GML record.

        """
        points, multipoints = self._dedup_multi(
            gml_tree,
            './/{http://www.opengis.net/gml/3.2}Point',
            './/{http://www.opengis.net/gml/3.2}MultiPoint'
        )

        self.subelements.update(points)
        self.subelements.update(multipoints)

        linestrings, multicurves = self._dedup_multi(
            gml_tree,
            './/{http://www.opengis.net/gml/3.2}LineString',
            './/{http://www.opengis.net/gml/3.2}MultiCurve'
        )

        self.subelements.update(linestrings)
        self.subelements.update(multicurves)

        polygons, multisurfaces = self._dedup_multi(
            gml_tree,
            './/{http://www.opengis.net/gml/3.2}Polygon',
            './/{http://www.opengis.net/gml/3.2}MultiSurface')

        self.subelements.update(polygons)
        self.subelements.update(multisurfaces)

        if len(self.subelements) == 0:
            if gml_tree.find('.//{http://www.opengis.net/gml}*') is not None:
                raise ValueError(
                    'GML document should be GML version 3.2, it appears to be '
                    'older.')

            raise ValueError('Failed to extract geometries from GML3.2 '
                             'document, is this a valid GML3.2 document?')

    def set_geometry_column(self, geometry_column):
        if len(self.subelements) == 1:
            self.element.set_geometry_column(geometry_column)
        else:
            for sub_element in self.element.operations:
                sub_element.set_geometry_column(geometry_column)

    def toXML(self):
        return self.element.toXML()


class GeometryFilter(GmlFilter):
    """Class for construction a spatial filter expression from any Geometry
    Fiona can convert to a GML 3.2 document.

    This class requires the ``fiona`` package to be installed.
    """

    def __init__(self, geometry, location_filter,
                 location_filter_kwargs=None, combinator=Or):
        """Initialise a spatial filter expression from a given Geometry.

        Parameters
        ----------
        geometry : str
            A path to a vector file on disk.
        location_filter : class<AbstractLocationFilter>
            Location filter to use for the geometries in the GML document.
        location_filter_kwargs : dict, optional
            Keyword-based arguments to pass to the `location_filter` on
            initialisation (with the exception of the `location` parameter,
            which is automatically parsed from the geomery). Can be skipped in
            cases where the location_filter takes no extra arguments besides
            location.
        combinator : class<BinaryLogicOpType>, optional, defaults to Or
            One of (Or, And) used to combine filters for different geometries
            in the geometry document.

        Raises
        ------
        ValueError
            When no geometries could be parsed from the given geometry.
        """
        gml = self._parse_geometry(geometry)

        super().__init__(gml, location_filter, location_filter_kwargs,
                         combinator)

    @staticmethod
    def _parse_geometry(geometry):
        """Checks the geometry and parse the file if possible.

        Raises
        ------
        ValueError
            When the file could not be parsed.
        """
        try:
            import fiona

            # Check if the GML driver and write mode are supported and check
            # if version of Fiona supports GML 3.2 output (Fiona >= 1.8.18)
            drivers = fiona.supported_drivers
            if 'w' not in drivers.get('GML', '') or \
                    Version(fiona.__version__) < Version('1.8.18'):
                raise UserWarning('Please use module Fiona version 1.8.18 '
                                  'or higher')
        except ImportError:
            raise ImportError('Failed to import fiona. GeometryFilter '
                              'requires fiona to be installed.')
        else:
            # Open the geometry as a collection containing multiple records
            with fiona.open(geometry, 'r') as c:
                gml_blob = BytesIO()
                # Assume the geometry is loaded from file
                layer = os.path.basename(os.path.splitext(geometry)[0])
                with fiona.open(gml_blob, 'w', layer=layer, driver='GML',
                                schema=c.schema, crs=c.crs,
                                FORMAT='GML3.2') as gml:
                    for r in c:
                        gml.write(r)
                gml_blob.seek(0)
                # Set the gml attribute used by the parent class
                gml = gml_blob.read()
                return gml


class GeopandasFilter(GmlFilter):
    """Class for construction a spatial filter expression from a
    GeoPandas object.

    This class requires the ``geopandas`` package to be installed.
    """

    def __init__(self, geodataframe, location_filter,
                 location_filter_kwargs=None, combinator=Or):
        """Initialise a spatial filter expression from a GeoPandas
        GeoDataFrame.

        Parameters
        ----------
        geodataframe : GeoPandas.GeoDataFrame
            A GeoDataFrame with a valid crs.
        location_filter : class<AbstractLocationFilter>
            Location filter to use for the geometries in the GML document.
        location_filter_kwargs : dict, optional
            Keyword-based arguments to pass to the `location_filter` on
            initialisation (with the exception of the `location` parameter,
            which is automatically parsed from the geomery). Can be skipped in
            cases where the location_filter takes no extra arguments besides
            location.
        combinator : class<BinaryLogicOpType>, optional, defaults to Or
            One of (Or, And) used to combine filters for different geometries
            in the geometry document.

        Raises
        ------
        ValueError
            When no geometries could be parsed from the given geometry.
        """
        gml = self._parse_geometry(geodataframe)

        super().__init__(gml, location_filter, location_filter_kwargs,
                         combinator)

    @staticmethod
    def _parse_geometry(gdf):
        """Checks the geometry and parse the file if possible.

        Raises
        ------
        ValueError
            When the file could not be parsed.
        """
        try:
            import geopandas
        except ImportError:
            raise ImportError('Failed to import geopandas. GeopandasFilter '
                              'requires geopandas to be installed.')
        else:
            if not isinstance(gdf, geopandas.GeoDataFrame):
                raise TypeError("pydov only supports geopandas.GeoDataFrame "
                                "to define a spatial query.")

            if not gdf.crs:
                raise AttributeError("geopandas.GeoDataFrame is missing a "
                                     "CRS definition")

            with BytesIO() as gml_blob:
                gdf.to_file(gml_blob, driver="GML", FORMAT="GML3.2",
                            layer="geodataframe")
                gml_blob.seek(0)
                gml = gml_blob.read()
            return gml
