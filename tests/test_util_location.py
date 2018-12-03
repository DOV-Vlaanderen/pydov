"""Module grouping tests for the pydov.util.location module."""
import pytest

from owslib.fes import (
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
    GmlObject,
)
from owslib.etree import etree
from pydov.util.owsutil import set_geometry_column
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

    def test_gmlobject_element(self):
        """Test the GmlObject type with an etree.Element.

        Test whether the returned XML is correct.

        """
        with open('tests/data/util/location/polygon.gml', 'r') as gmlfile:
            gml = gmlfile.read()

            gml_element = etree.fromstring(gml.encode('utf8'))
            gml_element = gml_element.find(
                './/{http://www.opengis.net/gml}MultiSurface')

            gml_object = GmlObject(gml_element)

            assert clean_xml(etree.tostring(
                gml_object.get_element()).decode('utf8')) == clean_xml(
                '<gml:MultiSurface '
                'srsName="urn:ogc:def:crs:EPSG::31370"><gml:surfaceMember'
                '><gml:Polygon><gml:exterior><gml:LinearRing><gml:posList'
                '>223907.66 157292.28 223965.136100002 157441.4956 '
                '223963.657 157442.877 223976.078 157439.609 '
                '224520.891500004 158850.3048 224531.114500001 '
                '158844.409699999 224617.707 158794.385899998 224656.12 '
                '158772.212400001 224656.49 158771.998799998 224654.5 '
                '158764.7788 224647.268399999 158741.4197 224645.753 '
                '158736.524900001 224700.595399998 158717.952199999 '
                '224700.939 158717.8358 224695.568 158695.684799999 '
                '224685.8138 158656.346799999 224685.812399998 '
                '158656.341200002 224676.694 158619.567 224775.526 '
                '158586.979800001 224899.9507 158546.466800001 224900.604 '
                '158540.7918 224987.56 158481.678800002 224988.113 '
                '158481.2995 224989.754600003 158480.173700001 '
                '224945.080600001 158428.7436 224946.8508 158427.279599998 '
                '224977.243199997 158402.071199998 224975.594899997 '
                '158363.630800001 224974.995399997 158349.651 224974.755 '
                '158344.044 224974.602600001 158339.6589 224966.868 '
                '158117.100699998 224966.509099998 158104.9778 224972.3539 '
                '158078.378199998 225006.176399998 157989.3149 225008.46 '
                '157984.298799999 225008.502 157984.186700001 '
                '225065.433200002 157832.254799999 225069.567 157821.223 '
                '225077.962 157771.743900001 225082.314900003 157746.0876 '
                '225082.3156 157746.0832 225083.658 157738.170899998 '
                '225083.926899999 157736.7326 225084.1483 157735.547899999 '
                '225079.266800001 157734.7542 225067.953299999 157732.5825 '
                '225067.790200002 157732.551199999 225069.62 157730.284 '
                '225069.672799997 157730.220699999 225078.292800002 '
                '157719.8763 225126.304499999 157662.260200001 225119.357 '
                '157655.1153 225095.1 157630.169 225117.314 157609.238400001 '
                '225124.592100002 157602.3807 225194.282799996 157536.3607 '
                '225193.219 157535.3528 225192.626 157534.791 '
                '225210.150899999 157518.858800001 225299.6646 157437.4804 '
                '225303.359099999 157488.327199999 225303.403899997 '
                '157488.943399999 225303.480099998 157489.992199998 '
                '225362.386399999 157444.988899998 225362.394199997 '
                '157444.983 225376.959 157433.855700001 225345.644 '
                '157382.3389 225345.205300003 157381.611499999 225335.09 '
                '157390.46 225323.84 157369.01 225302.55 157329.61 225289.0 '
                '157293.15 225306.5 157278.15 225108.26 156935.55 225106.88 '
                '156933.0 225102.61 156942.18 225094.43 156961.49 225083.18 '
                '156997.57 225073.37 157038.0 225061.281499997 157111.9989 '
                '225057.31 157136.31 225053.12 157155.19 225045.94 157174.84 '
                '225037.0 157192.23 225025.43 157209.19 224927.19 157344.3 '
                '224815.8 157473.64 224798.63 157493.6 224777.42 157464.63 '
                '224757.67 157442.47 224594.18 157290.44 224569.42 157265.56 '
                '224552.88 157247.53 224444.46 157124.69 224442.07 157126.63 '
                '224368.49 157186.16 224344.99 157159.16 224371.99 157132.85 '
                '224362.28 157122.08 224273.64 157023.74 224208.99 157075.16 '
                '224203.27 157068.31 224128.65 157115.03 224065.04 157155.4 '
                '224054.41 157161.81 223978.02 157205.54 224002.19 157241.71 '
                '223925.3112 157282.837299999 223907.66 '
                '157292.28</gml:posList></gml:LinearRing></gml:exterior'
                '></gml:Polygon></gml:surfaceMember></gml:MultiSurface>')

    def test_gmlobject_bytes(self):
        """Test the GmlObject type with a GML string.

        Test whether the returned XML is correct.

        """
        with open('tests/data/util/location/polygon.gml', 'r') as gmlfile:
            gml = gmlfile.read()

            gml_element = etree.fromstring(gml.encode('utf8'))
            gml_element = gml_element.find(
                './/{http://www.opengis.net/gml}MultiSurface')

            gml_object = GmlObject(etree.tostring(gml_element))

            assert clean_xml(etree.tostring(
                gml_object.get_element()).decode('utf8')) == clean_xml(
                '<gml:MultiSurface '
                'srsName="urn:ogc:def:crs:EPSG::31370"><gml:surfaceMember'
                '><gml:Polygon><gml:exterior><gml:LinearRing><gml:posList'
                '>223907.66 157292.28 223965.136100002 157441.4956 '
                '223963.657 157442.877 223976.078 157439.609 '
                '224520.891500004 158850.3048 224531.114500001 '
                '158844.409699999 224617.707 158794.385899998 224656.12 '
                '158772.212400001 224656.49 158771.998799998 224654.5 '
                '158764.7788 224647.268399999 158741.4197 224645.753 '
                '158736.524900001 224700.595399998 158717.952199999 '
                '224700.939 158717.8358 224695.568 158695.684799999 '
                '224685.8138 158656.346799999 224685.812399998 '
                '158656.341200002 224676.694 158619.567 224775.526 '
                '158586.979800001 224899.9507 158546.466800001 224900.604 '
                '158540.7918 224987.56 158481.678800002 224988.113 '
                '158481.2995 224989.754600003 158480.173700001 '
                '224945.080600001 158428.7436 224946.8508 158427.279599998 '
                '224977.243199997 158402.071199998 224975.594899997 '
                '158363.630800001 224974.995399997 158349.651 224974.755 '
                '158344.044 224974.602600001 158339.6589 224966.868 '
                '158117.100699998 224966.509099998 158104.9778 224972.3539 '
                '158078.378199998 225006.176399998 157989.3149 225008.46 '
                '157984.298799999 225008.502 157984.186700001 '
                '225065.433200002 157832.254799999 225069.567 157821.223 '
                '225077.962 157771.743900001 225082.314900003 157746.0876 '
                '225082.3156 157746.0832 225083.658 157738.170899998 '
                '225083.926899999 157736.7326 225084.1483 157735.547899999 '
                '225079.266800001 157734.7542 225067.953299999 157732.5825 '
                '225067.790200002 157732.551199999 225069.62 157730.284 '
                '225069.672799997 157730.220699999 225078.292800002 '
                '157719.8763 225126.304499999 157662.260200001 225119.357 '
                '157655.1153 225095.1 157630.169 225117.314 157609.238400001 '
                '225124.592100002 157602.3807 225194.282799996 157536.3607 '
                '225193.219 157535.3528 225192.626 157534.791 '
                '225210.150899999 157518.858800001 225299.6646 157437.4804 '
                '225303.359099999 157488.327199999 225303.403899997 '
                '157488.943399999 225303.480099998 157489.992199998 '
                '225362.386399999 157444.988899998 225362.394199997 '
                '157444.983 225376.959 157433.855700001 225345.644 '
                '157382.3389 225345.205300003 157381.611499999 225335.09 '
                '157390.46 225323.84 157369.01 225302.55 157329.61 225289.0 '
                '157293.15 225306.5 157278.15 225108.26 156935.55 225106.88 '
                '156933.0 225102.61 156942.18 225094.43 156961.49 225083.18 '
                '156997.57 225073.37 157038.0 225061.281499997 157111.9989 '
                '225057.31 157136.31 225053.12 157155.19 225045.94 157174.84 '
                '225037.0 157192.23 225025.43 157209.19 224927.19 157344.3 '
                '224815.8 157473.64 224798.63 157493.6 224777.42 157464.63 '
                '224757.67 157442.47 224594.18 157290.44 224569.42 157265.56 '
                '224552.88 157247.53 224444.46 157124.69 224442.07 157126.63 '
                '224368.49 157186.16 224344.99 157159.16 224371.99 157132.85 '
                '224362.28 157122.08 224273.64 157023.74 224208.99 157075.16 '
                '224203.27 157068.31 224128.65 157115.03 224065.04 157155.4 '
                '224054.41 157161.81 223978.02 157205.54 224002.19 157241.71 '
                '223925.3112 157282.837299999 223907.66 '
                '157292.28</gml:posList></gml:LinearRing></gml:exterior'
                '></gml:Polygon></gml:surfaceMember></gml:MultiSurface>')

    def test_gmlobject_string(self):
        """Test the GmlObject type with a GML string.

        Test whether the returned XML is correct.

        """
        with open('tests/data/util/location/polygon.gml', 'r') as gmlfile:
            gml = gmlfile.read()

            gml_element = etree.fromstring(gml.encode('utf8'))
            gml_element = gml_element.find(
                './/{http://www.opengis.net/gml}MultiSurface')

            gml_object = GmlObject(etree.tostring(gml_element).decode('utf8'))

            assert clean_xml(etree.tostring(
                gml_object.get_element()).decode('utf8')) == clean_xml(
                '<gml:MultiSurface '
                'srsName="urn:ogc:def:crs:EPSG::31370"><gml:surfaceMember'
                '><gml:Polygon><gml:exterior><gml:LinearRing><gml:posList'
                '>223907.66 157292.28 223965.136100002 157441.4956 '
                '223963.657 157442.877 223976.078 157439.609 '
                '224520.891500004 158850.3048 224531.114500001 '
                '158844.409699999 224617.707 158794.385899998 224656.12 '
                '158772.212400001 224656.49 158771.998799998 224654.5 '
                '158764.7788 224647.268399999 158741.4197 224645.753 '
                '158736.524900001 224700.595399998 158717.952199999 '
                '224700.939 158717.8358 224695.568 158695.684799999 '
                '224685.8138 158656.346799999 224685.812399998 '
                '158656.341200002 224676.694 158619.567 224775.526 '
                '158586.979800001 224899.9507 158546.466800001 224900.604 '
                '158540.7918 224987.56 158481.678800002 224988.113 '
                '158481.2995 224989.754600003 158480.173700001 '
                '224945.080600001 158428.7436 224946.8508 158427.279599998 '
                '224977.243199997 158402.071199998 224975.594899997 '
                '158363.630800001 224974.995399997 158349.651 224974.755 '
                '158344.044 224974.602600001 158339.6589 224966.868 '
                '158117.100699998 224966.509099998 158104.9778 224972.3539 '
                '158078.378199998 225006.176399998 157989.3149 225008.46 '
                '157984.298799999 225008.502 157984.186700001 '
                '225065.433200002 157832.254799999 225069.567 157821.223 '
                '225077.962 157771.743900001 225082.314900003 157746.0876 '
                '225082.3156 157746.0832 225083.658 157738.170899998 '
                '225083.926899999 157736.7326 225084.1483 157735.547899999 '
                '225079.266800001 157734.7542 225067.953299999 157732.5825 '
                '225067.790200002 157732.551199999 225069.62 157730.284 '
                '225069.672799997 157730.220699999 225078.292800002 '
                '157719.8763 225126.304499999 157662.260200001 225119.357 '
                '157655.1153 225095.1 157630.169 225117.314 157609.238400001 '
                '225124.592100002 157602.3807 225194.282799996 157536.3607 '
                '225193.219 157535.3528 225192.626 157534.791 '
                '225210.150899999 157518.858800001 225299.6646 157437.4804 '
                '225303.359099999 157488.327199999 225303.403899997 '
                '157488.943399999 225303.480099998 157489.992199998 '
                '225362.386399999 157444.988899998 225362.394199997 '
                '157444.983 225376.959 157433.855700001 225345.644 '
                '157382.3389 225345.205300003 157381.611499999 225335.09 '
                '157390.46 225323.84 157369.01 225302.55 157329.61 225289.0 '
                '157293.15 225306.5 157278.15 225108.26 156935.55 225106.88 '
                '156933.0 225102.61 156942.18 225094.43 156961.49 225083.18 '
                '156997.57 225073.37 157038.0 225061.281499997 157111.9989 '
                '225057.31 157136.31 225053.12 157155.19 225045.94 157174.84 '
                '225037.0 157192.23 225025.43 157209.19 224927.19 157344.3 '
                '224815.8 157473.64 224798.63 157493.6 224777.42 157464.63 '
                '224757.67 157442.47 224594.18 157290.44 224569.42 157265.56 '
                '224552.88 157247.53 224444.46 157124.69 224442.07 157126.63 '
                '224368.49 157186.16 224344.99 157159.16 224371.99 157132.85 '
                '224362.28 157122.08 224273.64 157023.74 224208.99 157075.16 '
                '224203.27 157068.31 224128.65 157115.03 224065.04 157155.4 '
                '224054.41 157161.81 223978.02 157205.54 224002.19 157241.71 '
                '223925.3112 157282.837299999 223907.66 '
                '157292.28</gml:posList></gml:LinearRing></gml:exterior'
                '></gml:Polygon></gml:surfaceMember></gml:MultiSurface>')


class TestBinarySpatialFilters(object):
    """Class grouping tests for the AbstractBinarySpatialFilter subtypes."""

    def test_equals_point(self):
        """Test the Equals spatial filter with a Point location.

        Test whether the generated XML is correct.

        """
        equals = Equals(Point(150000, 150000))
        equals.set_geometry_column('geom')
        xml = equals.toXML()

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
            equals.toXML()

    def test_disjoint_box(self):
        """Test the Disjoint spatial filter with a Box location.

        Test whether the generated XML is correct.

        """
        disjoint = Disjoint(Box(94720, 186910, 112220, 202870))
        disjoint.set_geometry_column('geom')
        xml = disjoint.toXML()

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
            disjoint.toXML()

    def test_touches_box(self):
        """Test the Touches spatial filter with a Box location.

        Test whether the generated XML is correct.

        """
        touches = Touches(Box(94720, 186910, 112220, 202870))
        touches.set_geometry_column('geom')
        xml = touches.toXML()

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
            touches.toXML()

    def test_within_box(self):
        """Test the Within spatial filter with a Box location.

        Test whether the generated XML is correct.

        """
        within = Within(Box(94720, 186910, 112220, 202870))
        within.set_geometry_column('geom')
        xml = within.toXML()

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
            within.toXML()

    def test_intersects_box(self):
        """Test the Intersects spatial filter with a Box location.

        Test whether the generated XML is correct.

        """
        intersects = Intersects(Box(94720, 186910, 112220, 202870))
        intersects.set_geometry_column('geom')
        xml = intersects.toXML()

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
            intersects.toXML()


class TestLocationFilters(object):
    """Class grouping tests for the AbstractLocationFilter subtypes."""

    def test_withindistance_point(self):
        """Test the WithinDistance spatial filter with a Point location.

        Test whether the generated XML is correct.

        """
        withindistance = WithinDistance(Point(150000, 150000), 100)
        withindistance.set_geometry_column('geom')
        xml = withindistance.toXML()

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
            withindistance.toXML()

    def test_withindistance_point_wgs84(self):
        """Test the WithinDistance spatial filter with a Point location
        using WGS84 coordinates.

        Test whether the generated XML is correct.

        """
        withindistance = WithinDistance(Point(51.1270, 3.8071, epsg=4326), 100)
        withindistance.set_geometry_column('geom')
        xml = withindistance.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<ogc:DWithin><ogc:PropertyName>geom</ogc:PropertyName>'
            '<gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#4326">'
            '<gml:pos>51.127000 3.807100</gml:pos></gml:Point>'
            '<gml:Distance units="meter">100.000000</gml:Distance>'
            '</ogc:DWithin>')


class TestLocationFilterExpressions(object):
    """Class grouping tests for expressions with spatial filters."""

    def test_point_and_box(self):
        """Test a location filter expression using a Within(Box) and a
        WithinDistance(Point) filter.

        Test whether the generated XML is correct.

        """
        point_and_box = And([WithinDistance(Point(150000, 150000), 100),
                             Within(Box(94720, 186910, 112220, 202870))])
        xml = set_geometry_column(point_and_box, 'geom')

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<ogc:And><ogc:DWithin><ogc:PropertyName>geom</ogc:PropertyName'
            '><gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370"><gml'
            ':pos>150000.000000 '
            '150000.000000</gml:pos></gml:Point><gml:Distance '
            'units="meter">100.000000</gml:Distance></ogc:DWithin><ogc'
            ':Within><ogc:PropertyName>geom</ogc:PropertyName><gml'
            ':Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370"><gml'
            ':lowerCorner>94720.000000 '
            '186910.000000</gml:lowerCorner><gml:upperCorner>112220.000000 '
            '202870.000000</gml:upperCorner></gml:Envelope></ogc:Within'
            '></ogc:And>')

    def test_box_or_box(self):
        """Test a location filter expression using an Intersects(Box) and a
        Within(Box) filter.

        Test whether the generated XML is correct.

        """
        box_or_box = Or([
            Intersects(Box(50.9850, 3.6214, 51.1270, 3.8071, epsg=4326)),
            Within(Box(94720, 186910, 112220, 202870))])
        xml = set_geometry_column(box_or_box, 'geom')

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<ogc:Or><ogc:Intersects><ogc:PropertyName>geom</ogc'
            ':PropertyName><gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#4326"><gml'
            ':lowerCorner>50.985000 '
            '3.621400</gml:lowerCorner><gml:upperCorner>51.127000 '
            '3.807100</gml:upperCorner></gml:Envelope></ogc:Intersects><ogc'
            ':Within><ogc:PropertyName>geom</ogc:PropertyName><gml:Envelope '
            'srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370"><gml '
            ':lowerCorner>94720.000000 '
            '186910.000000</gml:lowerCorner><gml:upperCorner>112220.000000 '
            '202870.000000</gml:upperCorner></gml:Envelope></ogc:Within'
            '></ogc:Or>')

    def test_recursive(self):
        """Test a location filter expression using a recursive expression
        with And(Not(WithinDistance(Point) filter.

        Test whether the generated XML is correct.

        """
        point_and_box = And([Not([WithinDistance(Point(150000, 150000), 100)]),
                             Within(Box(94720, 186910, 112220, 202870))])
        xml = set_geometry_column(point_and_box, 'geom')

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<ogc:And><ogc:Not><ogc:DWithin><ogc:PropertyName>geom</ogc'
            ':PropertyName><gml:Point srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370"><gml'
            ':pos>150000.000000 '
            '150000.000000</gml:pos></gml:Point><gml:Distance '
            'units="meter">100.000000</gml:Distance></ogc:DWithin></ogc:Not'
            '><ogc:Within><ogc:PropertyName>geom</ogc:PropertyName><gml'
            ':Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370"><gml'
            ':lowerCorner>94720.000000 '
            '186910.000000</gml:lowerCorner><gml:upperCorner>112220.000000 '
            '202870.000000</gml:upperCorner></gml:Envelope></ogc:Within'
            '></ogc:And>')
