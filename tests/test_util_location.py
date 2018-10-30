"""Module grouping tests for the pydov.util.location module."""
import pytest

from pydov.util.location import (
    Box,
    Point,
    Equals,
    Disjoint,
    Touches,
    Within,
    Intersects,
    WithinDistance,
)
from owslib.etree import etree
from tests.abstract import clean_xml


class TestLocation(object):
    """Class grouping tests for the AbstractLocation subtypes."""

    def test_box(self):
        """Test the default Box type.

        Test whether the generated XML is correct.

        """
        box = Box(94720, 186910, 112220, 202870)
        xml = box.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370">'
            '<gml:lowerCorner>94720.000000 186910.000000</gml:lowerCorner>'
            '<gml:upperCorner>112220.000000 202870.000000</gml:upperCorner>'
            '</gml:Envelope>')

    def test_box_wgs84(self):
        """Test the Box type with WGS84 coordinates.

        Test whether the generated XML is correct.

        """
        box = Box(50.9850, 3.6214, 51.1270, 3.8071, epsg=4326)
        xml = box.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">'
            '<gml:lowerCorner>50.985000 3.621400</gml:lowerCorner>'
            '<gml:upperCorner>51.127000 3.807100</gml:upperCorner>'
            '</gml:Envelope>')

    def test_box_invalid(self):
        """Test the Box type with the wrong ordering of coordinates.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            Box(94720, 202870, 186910, 112220)

    def test_box_invalid_wgs84(self):
        """Test the Box type with the wrong ordering of WGS84 coordinates.

        Test whether a ValueError is raised.

        """
        with pytest.raises(ValueError):
            Box(50.9850, 3.6214, 3.8071, 51.1270, epsg=4326)

    def test_point(self):
        """Test the default Point type.

        Test whether the generated XML is correct.

        """
        point = Point(110680, 202030)
        xml = point.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370">'
            '<gml:pos>110680.000000 202030.000000</gml:pos></gml:Point>')

    def test_point_wgs84(self):
        """Test the Point type with WGS84 coordinates.

        Test whether the generated XML is correct.

        """
        point = Point(51.1270, 3.8071, epsg=4326)
        xml = point.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">'
            '<gml:pos>51.127000 3.807100</gml:pos></gml:Point>')


class TestBinarySpatialFilters(object):
    """Class grouping tests for the AbstractBinarySpatialFilter subtypes."""

    def test_equals_point(self):
        """Test the Equals spatial filter with a Point location.

        Test whether the generated XML is correct.

        """
        equals = Equals(Point(150000, 150000))
        equals.set_geometry_column('geom')
        xml = equals.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<ogc:Equals><ogc:PropertyName>geom</ogc:PropertyName>'
            '<gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370">'
            '<gml:pos>150000.000000 150000.000000</gml:pos></gml:Point>'
            '</ogc:Equals>')

    def test_equals_nogeom(self):
        """Test the Equals spatial filter without setting a geometry column.

        Test whether a RuntimeError is raised.

        """
        equals = Equals(Point(150000, 150000))

        with pytest.raises(RuntimeError):
            equals.get_element()

    def test_disjoint_box(self):
        """Test the Disjoint spatial filter with a Box location.

        Test whether the generated XML is correct.

        """
        disjoint = Disjoint(Box(94720, 186910, 112220, 202870))
        disjoint.set_geometry_column('geom')
        xml = disjoint.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<ogc:Disjoint><ogc:PropertyName>geom</ogc:PropertyName>'
            '<gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370">'
            '<gml:lowerCorner>94720.000000 186910.000000</gml:lowerCorner>'
            '<gml:upperCorner>112220.000000 202870.000000</gml:upperCorner>'
            '</gml:Envelope></ogc:Disjoint>')

    def test_disjoint_nogeom(self):
        """Test the Disjoint spatial filter without setting a geometry column.

        Test whether a RuntimeError is raised.

        """
        disjoint = Disjoint(Point(150000, 150000))

        with pytest.raises(RuntimeError):
            disjoint.get_element()

    def test_touches_box(self):
        """Test the Touches spatial filter with a Box location.

        Test whether the generated XML is correct.

        """
        touches = Touches(Box(94720, 186910, 112220, 202870))
        touches.set_geometry_column('geom')
        xml = touches.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<ogc:Touches><ogc:PropertyName>geom</ogc:PropertyName>'
            '<gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370">'
            '<gml:lowerCorner>94720.000000 186910.000000</gml:lowerCorner>'
            '<gml:upperCorner>112220.000000 202870.000000</gml:upperCorner>'
            '</gml:Envelope></ogc:Touches>')

    def test_touches_nogeom(self):
        """Test the Touches spatial filter without setting a geometry column.

        Test whether a RuntimeError is raised.

        """
        touches = Touches(Point(150000, 150000))

        with pytest.raises(RuntimeError):
            touches.get_element()

    def test_within_box(self):
        """Test the Within spatial filter with a Box location.

        Test whether the generated XML is correct.

        """
        within = Within(Box(94720, 186910, 112220, 202870))
        within.set_geometry_column('geom')
        xml = within.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<ogc:Within><ogc:PropertyName>geom</ogc:PropertyName>'
            '<gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370">'
            '<gml:lowerCorner>94720.000000 186910.000000</gml:lowerCorner>'
            '<gml:upperCorner>112220.000000 202870.000000</gml:upperCorner>'
            '</gml:Envelope></ogc:Within>')

    def test_within_nogeom(self):
        """Test the Within spatial filter without setting a geometry column.

        Test whether a RuntimeError is raised.

        """
        within = Within(Box(94720, 186910, 112220, 202870))

        with pytest.raises(RuntimeError):
            within.get_element()

    def test_intersects_box(self):
        """Test the Intersects spatial filter with a Box location.

        Test whether the generated XML is correct.

        """
        intersects = Intersects(Box(94720, 186910, 112220, 202870))
        intersects.set_geometry_column('geom')
        xml = intersects.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<ogc:Intersects><ogc:PropertyName>geom</ogc:PropertyName>'
            '<gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370">'
            '<gml:lowerCorner>94720.000000 186910.000000</gml:lowerCorner>'
            '<gml:upperCorner>112220.000000 202870.000000</gml:upperCorner>'
            '</gml:Envelope></ogc:Intersects>')

    def test_intersects_nogeom(self):
        """Test the Intersects spatial filter without setting a geometry
        column.

        Test whether a RuntimeError is raised.

        """
        intersects = Intersects(Box(94720, 186910, 112220, 202870))

        with pytest.raises(RuntimeError):
            intersects.get_element()


class TestLocationFilters(object):
    """Class grouping tests for the AbstractLocationFilter subtypes."""

    def test_withindistance_point(self):
        """Test the WithinDistance spatial filter with a Point location.

        Test whether the generated XML is correct.

        """
        withindistance = WithinDistance(Point(150000, 150000), 100)
        withindistance.set_geometry_column('geom')
        xml = withindistance.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<ogc:DWithin><ogc:PropertyName>geom</ogc:PropertyName>'
            '<gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370">'
            '<gml:pos>150000.000000 150000.000000</gml:pos></gml:Point>'
            '<gml:Distance units="meter">100.000000</gml:Distance>'
            '</ogc:DWithin>')

    def test_withindistance_nogeom(self):
        """Test the WithinDistance spatial filter without setting a geometry
        column.

        Test whether a RuntimeError is raised.

        """
        withindistance = WithinDistance(Point(150000, 150000), 100)

        with pytest.raises(RuntimeError):
            withindistance.get_element()

    def test_withindistance_point_wgs84(self):
        """Test the WithinDistance spatial filter with a Point location
        using WGS84 coordinates.

        Test whether the generated XML is correct.

        """
        withindistance = WithinDistance(Point(51.1270, 3.8071, epsg=4326), 100)
        withindistance.set_geometry_column('geom')
        xml = withindistance.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<ogc:DWithin><ogc:PropertyName>geom</ogc:PropertyName>'
            '<gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">'
            '<gml:pos>51.127000 3.807100</gml:pos></gml:Point>'
            '<gml:Distance units="meter">100.000000</gml:Distance>'
            '</ogc:DWithin>')
