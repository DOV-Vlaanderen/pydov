"""Module grouping tests for the pydov.util.location module."""
import pytest

from owslib.fes2 import (
    And,
    Or,
    Not,
)
from pydov.util.location import (
    Box,
    Point,
    Equals,
    Disjoint,
    Touches,
    Within,
    Intersects,
    WithinDistance,
    GmlObject
)
from owslib.etree import etree
from pydov.util.owsutil import set_geometry_column
from tests.abstract import clean_xml


class TestLocation(object):
    """Class grouping tests for the AbstractLocation subtypes."""

    def test_gml_id_unique(self):
        """Test whether GML id's for two different locations are unique."""
        box1 = Box(94720, 186910, 112220, 202870)
        id1 = box1.get_element().get('{http://www.opengis.net/gml/3.2}id')

        box2 = Box(94721, 186911, 112221, 202871)
        id2 = box2.get_element().get('{http://www.opengis.net/gml/3.2}id')

        assert id1.startswith('pydov')
        assert id2.startswith('pydov')
        assert id1 != id2

    def test_gml_id_stable(self):
        """Test whether GML id's for two equal locations are the same."""
        box1 = Box(94720, 186910, 112220, 202870)
        id1 = box1.get_element().get('{http://www.opengis.net/gml/3.2}id')

        box2 = Box(94720, 186910, 112220, 202870)
        id2 = box2.get_element().get('{http://www.opengis.net/gml/3.2}id')

        assert id1.startswith('pydov')
        assert id2.startswith('pydov')
        assert id1 == id2

    def test_box(self, mp_gml_id):
        """Test the default Box type.

        Test whether the generated XML is correct.

        """
        box = Box(94720, 186910, 112220, 202870)
        xml = box.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid">'
            '<gml:lowerCorner>94720.000000 186910.000000</gml:lowerCorner>'
            '<gml:upperCorner>112220.000000 202870.000000</gml:upperCorner>'
            '</gml:Envelope>')

    def test_box_wgs84(self, mp_gml_id):
        """Test the Box type with WGS84 coordinates.

        Test whether the generated XML is correct.

        """
        box = Box(3.6214, 50.9850, 3.8071, 51.1270, epsg=4326)
        xml = box.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#4326" gml32:id='
            '"pydov.gmlid">'
            '<gml:lowerCorner>3.621400 50.985000</gml:lowerCorner>'
            '<gml:upperCorner>3.807100 51.127000</gml:upperCorner>'
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

    def test_point(self, mp_gml_id):
        """Test the default Point type.

        Test whether the generated XML is correct.

        """
        point = Point(110680, 202030)
        xml = point.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid">'
            '<gml:pos>110680.000000 202030.000000</gml:pos></gml:Point>')

    def test_point_wgs84(self, mp_gml_id):
        """Test the Point type with WGS84 coordinates.

        Test whether the generated XML is correct.

        """
        point = Point(3.8071, 51.1270, epsg=4326)
        xml = point.get_element()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#4326" gml32:id='
            '"pydov.gmlid">'
            '<gml:pos>3.807100 51.127000</gml:pos></gml:Point>')

    def test_gmlobject_element(self):
        """Test the GmlObject type with an etree.Element.

        Test whether the returned XML is correct.

        """
        with open('tests/data/util/location/polygon_single_31370.gml',
                  'r') as gmlfile:
            gml = gmlfile.read()

            gml_element = etree.fromstring(gml.encode('utf8'))
            gml_element = gml_element.find(
                './/{http://www.opengis.net/gml/3.2}Polygon')

            gml_object = GmlObject(gml_element)

            assert clean_xml(etree.tostring(
                gml_object.get_element()).decode('utf8')) == clean_xml(
                '<gml:Polygon '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id='
                '"polygon_single_31370.geom.0"><gml:exterior><gml'
                ':LinearRing><gml:posList>108636.150020818 194960.844295764 '
                '108911.922161617 194291.111953824 109195.573506438 '
                '195118.42837622 108636.150020818 '
                '194960.844295764</gml:posList></gml:LinearRing></gml'
                ':exterior></gml:Polygon>')

    def test_gmlobject_bytes(self):
        """Test the GmlObject type with a GML string.

        Test whether the returned XML is correct.

        """
        with open('tests/data/util/location/polygon_single_31370.gml',
                  'r') as gmlfile:
            gml = gmlfile.read()

            gml_element = etree.fromstring(gml.encode('utf8'))
            gml_element = gml_element.find(
                './/{http://www.opengis.net/gml/3.2}Polygon')

            gml_object = GmlObject(etree.tostring(gml_element))

            assert clean_xml(etree.tostring(
                gml_object.get_element()).decode('utf8')) == clean_xml(
                '<gml:Polygon '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id='
                '"polygon_single_31370.geom.0"><gml:exterior><gml'
                ':LinearRing><gml:posList>108636.150020818 194960.844295764 '
                '108911.922161617 194291.111953824 109195.573506438 '
                '195118.42837622 108636.150020818 '
                '194960.844295764</gml:posList></gml:LinearRing></gml'
                ':exterior></gml:Polygon>')

    def test_gmlobject_string(self):
        """Test the GmlObject type with a GML string.

        Test whether the returned XML is correct.

        """
        with open('tests/data/util/location/polygon_single_31370.gml',
                  'r') as gmlfile:
            gml = gmlfile.read()

            gml_element = etree.fromstring(gml.encode('utf8'))
            gml_element = gml_element.find(
                './/{http://www.opengis.net/gml/3.2}Polygon')

            gml_object = GmlObject(etree.tostring(gml_element).decode('utf8'))

            assert clean_xml(etree.tostring(
                gml_object.get_element()).decode('utf8')) == clean_xml(
                '<gml:Polygon '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id='
                '"polygon_single_31370.geom.0"><gml:exterior><gml'
                ':LinearRing><gml:posList>108636.150020818 194960.844295764 '
                '108911.922161617 194291.111953824 109195.573506438 '
                '195118.42837622 108636.150020818 '
                '194960.844295764</gml:posList></gml:LinearRing></gml'
                ':exterior></gml:Polygon>')

    def test_gmlobject_no_gml(self):
        """Test the GmlObject type with XML that is not GML.

        Test whether an ValueError is raised.

        """
        with open('tests/data/types/interpretaties/gecodeerde_lithologie/'
                  'gecodeerde_lithologie.xml', 'r') as xmlfile:
            xml = xmlfile.read()

            with pytest.raises(ValueError, match='not to be valid GML3.2'):
                GmlObject(xml)

    def test_gmlobject_old_gml(self):
        """Test the GmlObject type with XML that is GML 3.1.1

        Test whether an ValueError is raised.

        """
        with open('tests/data/util/location/point_single_31370_gml31.gml',
                  'r') as xmlfile:
            xml = xmlfile.read()

            with pytest.raises(ValueError, match='older'):
                GmlObject(xml)


class TestBinarySpatialFilters(object):
    """Class grouping tests for the AbstractBinarySpatialFilter subtypes."""

    def test_equals_point(self, mp_gml_id):
        """Test the Equals spatial filter with a Point location.

        Test whether the generated XML is correct.

        """
        equals = Equals(Point(150000, 150000))
        equals.set_geometry_column('geom')
        xml = equals.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Equals><fes:ValueReference>geom</fes:ValueReference>'
            '<gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid">'
            '<gml:pos>150000.000000 150000.000000</gml:pos></gml:Point>'
            '</fes:Equals>')

    def test_equals_nogeom(self):
        """Test the Equals spatial filter without setting a geometry column.

        Test whether a RuntimeError is raised.

        """
        equals = Equals(Point(150000, 150000))

        with pytest.raises(RuntimeError):
            equals.toXML()

    def test_disjoint_box(self, mp_gml_id):
        """Test the Disjoint spatial filter with a Box location.

        Test whether the generated XML is correct.

        """
        disjoint = Disjoint(Box(94720, 186910, 112220, 202870))
        disjoint.set_geometry_column('geom')
        xml = disjoint.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Disjoint><fes:ValueReference>geom</fes:ValueReference>'
            '<gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid">'
            '<gml:lowerCorner>94720.000000 186910.000000</gml:lowerCorner>'
            '<gml:upperCorner>112220.000000 202870.000000</gml:upperCorner>'
            '</gml:Envelope></fes:Disjoint>')

    def test_disjoint_nogeom(self):
        """Test the Disjoint spatial filter without setting a geometry column.

        Test whether a RuntimeError is raised.

        """
        disjoint = Disjoint(Point(150000, 150000))

        with pytest.raises(RuntimeError):
            disjoint.toXML()

    def test_touches_box(self, mp_gml_id):
        """Test the Touches spatial filter with a Box location.

        Test whether the generated XML is correct.

        """
        touches = Touches(Box(94720, 186910, 112220, 202870))
        touches.set_geometry_column('geom')
        xml = touches.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Touches><fes:ValueReference>geom</fes:ValueReference>'
            '<gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid">'
            '<gml:lowerCorner>94720.000000 186910.000000</gml:lowerCorner>'
            '<gml:upperCorner>112220.000000 202870.000000</gml:upperCorner>'
            '</gml:Envelope></fes:Touches>')

    def test_touches_nogeom(self):
        """Test the Touches spatial filter without setting a geometry column.

        Test whether a RuntimeError is raised.

        """
        touches = Touches(Point(150000, 150000))

        with pytest.raises(RuntimeError):
            touches.toXML()

    def test_within_box(self, mp_gml_id):
        """Test the Within spatial filter with a Box location.

        Test whether the generated XML is correct.

        """
        within = Within(Box(94720, 186910, 112220, 202870))
        within.set_geometry_column('geom')
        xml = within.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Within><fes:ValueReference>geom</fes:ValueReference>'
            '<gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid">'
            '<gml:lowerCorner>94720.000000 186910.000000</gml:lowerCorner>'
            '<gml:upperCorner>112220.000000 202870.000000</gml:upperCorner>'
            '</gml:Envelope></fes:Within>')

    def test_within_nogeom(self):
        """Test the Within spatial filter without setting a geometry column.

        Test whether a RuntimeError is raised.

        """
        within = Within(Box(94720, 186910, 112220, 202870))

        with pytest.raises(RuntimeError):
            within.toXML()

    def test_intersects_box(self, mp_gml_id):
        """Test the Intersects spatial filter with a Box location.

        Test whether the generated XML is correct.

        """
        intersects = Intersects(Box(94720, 186910, 112220, 202870))
        intersects.set_geometry_column('geom')
        xml = intersects.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Intersects><fes:ValueReference>geom</fes:ValueReference>'
            '<gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid">'
            '<gml:lowerCorner>94720.000000 186910.000000</gml:lowerCorner>'
            '<gml:upperCorner>112220.000000 202870.000000</gml:upperCorner>'
            '</gml:Envelope></fes:Intersects>')

    def test_intersects_nogeom(self):
        """Test the Intersects spatial filter without setting a geometry
        column.

        Test whether a RuntimeError is raised.

        """
        intersects = Intersects(Box(94720, 186910, 112220, 202870))

        with pytest.raises(RuntimeError):
            intersects.toXML()


class TestLocationFilters(object):
    """Class grouping tests for the AbstractLocationFilter subtypes."""

    def test_withindistance_point(self, mp_gml_id):
        """Test the WithinDistance spatial filter with a Point location.

        Test whether the generated XML is correct.

        """
        withindistance = WithinDistance(Point(150000, 150000), 100)
        withindistance.set_geometry_column('geom')
        xml = withindistance.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:DWithin><fes:ValueReference>geom</fes:ValueReference>'
            '<gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid">'
            '<gml:pos>150000.000000 150000.000000</gml:pos></gml:Point>'
            '<gml:Distance units="meter">100.000000</gml:Distance>'
            '</fes:DWithin>')

    def test_withindistance_point_named_args(self, mp_gml_id):
        """Test the WithinDistance spatial filter with a Point location.

        Test whether the generated XML is correct.

        """
        withindistance = WithinDistance(location=Point(150000, 150000),
                                        distance=100, distance_unit='meter')
        withindistance.set_geometry_column('geom')
        xml = withindistance.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:DWithin><fes:ValueReference>geom</fes:ValueReference>'
            '<gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid">'
            '<gml:pos>150000.000000 150000.000000</gml:pos></gml:Point>'
            '<gml:Distance units="meter">100.000000</gml:Distance>'
            '</fes:DWithin>')

    def test_withindistance_nogeom(self):
        """Test the WithinDistance spatial filter without setting a geometry
        column.

        Test whether a RuntimeError is raised.

        """
        withindistance = WithinDistance(Point(150000, 150000), 100)

        with pytest.raises(RuntimeError):
            withindistance.toXML()

    def test_withindistance_point_wgs84(self, mp_gml_id):
        """Test the WithinDistance spatial filter with a Point location
        using WGS84 coordinates.

        Test whether the generated XML is correct.

        """
        withindistance = WithinDistance(Point(51.1270, 3.8071, epsg=4326), 100)
        withindistance.set_geometry_column('geom')
        xml = withindistance.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:DWithin><fes:ValueReference>geom</fes:ValueReference>'
            '<gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#4326" gml32:id='
            '"pydov.gmlid">'
            '<gml:pos>51.127000 3.807100</gml:pos></gml:Point>'
            '<gml:Distance units="meter">100.000000</gml:Distance>'
            '</fes:DWithin>')


class TestLocationFilterExpressions(object):
    """Class grouping tests for expressions with spatial filters."""

    def test_point_and_box(self, mp_gml_id):
        """Test a location filter expression using a Within(Box) and a
        WithinDistance(Point) filter.

        Test whether the generated XML is correct.

        """
        point_and_box = And([WithinDistance(Point(150000, 150000), 100),
                             Within(Box(94720, 186910, 112220, 202870))])
        xml = set_geometry_column(point_and_box, 'geom')

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:And><fes:DWithin><fes:ValueReference>geom</fes:ValueReference'
            '><gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid"><gml:pos>150000.000000 '
            '150000.000000</gml:pos></gml:Point><gml:Distance '
            'units="meter">100.000000</gml:Distance></fes:DWithin><fes'
            ':Within><fes:ValueReference>geom</fes:ValueReference><gml'
            ':Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid"><gml:lowerCorner>94720.000000 '
            '186910.000000</gml:lowerCorner><gml:upperCorner>112220.000000 '
            '202870.000000</gml:upperCorner></gml:Envelope></fes:Within'
            '></fes:And>')

    def test_box_or_box(self, mp_gml_id):
        """Test a location filter expression using an Intersects(Box) and a
        Within(Box) filter.

        Test whether the generated XML is correct.

        """
        box_or_box = Or([
            Intersects(Box(50.9850, 3.6214, 51.1270, 3.8071, epsg=4326)),
            Within(Box(94720, 186910, 112220, 202870))])
        xml = set_geometry_column(box_or_box, 'geom')

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Or><fes:Intersects><fes:ValueReference>geom</fes'
            ':ValueReference><gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#4326" gml32:id='
            '"pydov.gmlid"><gml:lowerCorner>50.985000 '
            '3.621400</gml:lowerCorner><gml:upperCorner>51.127000 '
            '3.807100</gml:upperCorner></gml:Envelope></fes:Intersects><fes'
            ':Within><fes:ValueReference>geom</fes:ValueReference><gml:Envelope '
            'srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid"><gml:lowerCorner>94720.000000 '
            '186910.000000</gml:lowerCorner><gml:upperCorner>112220.000000 '
            '202870.000000</gml:upperCorner></gml:Envelope></fes:Within'
            '></fes:Or>')

    def test_recursive(self, mp_gml_id):
        """Test a location filter expression using a recursive expression
        with And(Not(WithinDistance(Point) filter.

        Test whether the generated XML is correct.

        """
        point_and_box = And([Not([WithinDistance(Point(150000, 150000), 100)]),
                             Within(Box(94720, 186910, 112220, 202870))])
        xml = set_geometry_column(point_and_box, 'geom')

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:And><fes:Not><fes:DWithin><fes:ValueReference>geom</fes'
            ':ValueReference><gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid"><gml:pos>150000.000000 '
            '150000.000000</gml:pos></gml:Point><gml:Distance '
            'units="meter">100.000000</gml:Distance></fes:DWithin></fes:Not'
            '><fes:Within><fes:ValueReference>geom</fes:ValueReference><gml'
            ':Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid"><gml:lowerCorner>94720.000000 '
            '186910.000000</gml:lowerCorner><gml:upperCorner>112220.000000 '
            '202870.000000</gml:upperCorner></gml:Envelope></fes:Within'
            '></fes:And>')
