"""Module grouping tests for the pydov.util.location.GmlFilter class."""
import pytest
import platform
import subprocess
from owslib.etree import etree
from owslib.fes2 import And, Or

from pydov.util.location import (Box, Disjoint, GeometryFilter,
                                 GeopandasFilter, GmlFilter, Within,
                                 WithinDistance)
from pydov.util.owsutil import set_geometry_column
from tests.abstract import clean_xml


class TestPoint(object):
    """Class grouping tests for point locations."""

    def test_point_single_31370(self):
        """Test the WithinDistance filter with a GML containing a single
        point geometry in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/point_single_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, WithinDistance, {'distance': 100})
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:DWithin><fes:ValueReference>geom</fes:ValueReference><gml'
            ':Point srsName="urn:ogc:def:crs:EPSG::31370" gml:id="point_single'
            '_31370.geom.0"><gml:pos>109124'
            '.660670233 194937.206683695</gml:pos></gml:Point><gml:Distance '
            'units="meter">100.000000</gml:Distance></fes:DWithin>')

    def test_point_multiple_31370(self):
        """Test the WithinDistance filter with a GML containing multiple
        point geometries in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/point_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, WithinDistance, {'distance': 100})
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 2

        points = ['109124.660670233 194937.206683695',
                  '109234.969526552 195772.402310114']

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}DWithin'

            point = f.find('./{http://www.opengis.net/gml/3.2}Point')
            assert point.get('srsName') == 'urn:ogc:def:crs:EPSG::31370'

            posList = point.find('./{http://www.opengis.net/gml/3.2}pos').text
            assert posList in points

            points.remove(posList)

        assert len(points) == 0

    def test_point_multiple_31370_stable(self):
        """Test the WithinDistance filter with a GML containing multiple
        point geometries in EPSG:31370.

        Test whether the generated XML is correct and stable.

        """
        with open('tests/data/util/location/point_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        for i in range(10):
            f = GmlFilter(gml, WithinDistance, {'distance': 100})
            f.set_geometry_column('geom')
            xml = f.toXML()

            assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
                '<fes:Or><fes:DWithin><fes:ValueReference>geom</fes'
                ':ValueReference><gml:Point '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="point_multiple'
                '_31370.geom.0"><gml:pos>109124'
                '.660670233 194937.206683695</gml:pos></gml:Point><gml'
                ':Distance units="meter">100.000000</gml:Distance></fes'
                ':DWithin><fes:DWithin><fes:ValueReference>geom</fes'
                ':ValueReference><gml:Point '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="point_multiple'
                '_31370.geom.1"><gml:pos>109234'
                '.969526552 195772.402310114</gml:pos></gml:Point><gml'
                ':Distance units="meter">100.000000</gml:Distance>'
                '</fes:DWithin></fes:Or>')

    def test_point_single_4326(self):
        """Test the WithinDistance filter with a GML containing a single
        point geometry in EPSG:4326.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/point_single_4326.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, WithinDistance, {'distance': 100})
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:DWithin><fes:ValueReference>geom</fes:ValueReference><gml'
            ':Point srsName="urn:ogc:def:crs:EPSG::4326" gml:id="point_single'
            '_4326.geom.0"><gml:pos>51.0631382448644 '
            '3.7856620304411</gml:pos></gml:Point><gml:Distance '
            'units="meter">100.000000</gml:Distance></fes:DWithin>')

    def test_gml_311(self):
        """Test the GmlFilter with GML version 3.1.1.

        Test whether a ValueError is raised.
        """
        with open('tests/data/util/location/point_single_31370_gml31.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        with pytest.raises(ValueError) as error:
            GmlFilter(gml, Within)

            assert 'older' in error


class TestMultipoint(object):
    """Class grouping tests for multipoint locations."""

    def test_multipoint_single_31370(self):
        """Test the WithinDistance filter with a GML containing a single
        multipoint geometry in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/multipoint_single_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, WithinDistance, {'distance': 100})
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:DWithin><fes:ValueReference>geom</fes:ValueReference><gml'
            ':MultiPoint srsName="urn:ogc:def:crs:EPSG::31370" gml:id="multipo'
            'int_single_31370.geom.0"><gml'
            ':pointMember><gml:Point gml:id="multipo'
            'int_single_31370.geom.0.0"><gml:pos>108770.096489206 '
            '194992.361111855</gml:pos></gml:Point></gml:pointMember><gml'
            ':pointMember><gml:Point gml:id="multipo'
            'int_single_31370.geom.0.1"><gml:pos>109045.868630005 '
            '194929.327479672</gml:pos></gml:Point></gml:pointMember></gml'
            ':MultiPoint><gml:Distance '
            'units="meter">100.000000</gml:Distance></fes:DWithin>')

    def test_multipoint_multiple_31370(self):
        """Test the WithinDistance filter with a GML containing multiple
        multipoint geometries in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/multipoint_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, WithinDistance, {'distance': 100})
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 2

        multipoints = [['108770.096489206 194992.361111855',
                        '109045.868630005 194929.327479672'],
                       ['108825.250917366 195433.596537133',
                        '108738.579673115 195614.818229658']]

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}DWithin'

            multipoint = f.find('./{http://www.opengis.net/gml/3.2}MultiPoint')
            assert multipoint.get('srsName') == 'urn:ogc:def:crs:EPSG::31370'

            posList = [p.text for p in multipoint.findall(
                './/{http://www.opengis.net/gml/3.2}pos')]
            multipoints.remove(posList)

        assert len(multipoints) == 0

    def test_multipoint_multiple_31370_stable(self):
        """Test the WithinDistance filter with a GML containing multiple
        multipoint geometries in EPSG:31370.

        Test whether the generated XML is correct and stable.

        """
        with open('tests/data/util/location/multipoint_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        for i in range(10):
            f = GmlFilter(gml, WithinDistance, {'distance': 100})
            f.set_geometry_column('geom')
            xml = f.toXML()

            assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
                '<fes:Or><fes:DWithin><fes:ValueReference>geom</fes'
                ':ValueReference><gml:MultiPoint '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="multipo'
                'int_multiple_31370.geom.0"><gml:pointMember><gml'
                ':Point gml:id="multipo'
                'int_multiple_31370.geom.0.0"><gml:pos>108770.096489206 '
                '194992.361111855</gml:pos></gml:Point></gml:pointMember'
                '><gml:pointMember><gml:Point gml:id="multipo'
                'int_multiple_31370.geom.0.1"><gml:pos>109045.868630005 '
                '194929.327479672</gml:pos></gml:Point></gml:pointMember'
                '></gml:MultiPoint><gml:Distance '
                'units="meter">100.000000</gml:Distance></fes:DWithin><fes'
                ':DWithin><fes:ValueReference>geom</fes:ValueReference><gml'
                ':MultiPoint '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="multipo'
                'int_multiple_31370.geom.1"><gml:pointMember><gml'
                ':Point gml:id="multipo'
                'int_multiple_31370.geom.1.0"><gml:pos>108825.250917366 '
                '195433.596537133</gml:pos></gml:Point></gml:pointMember'
                '><gml:pointMember><gml:Point gml:id="multipo'
                'int_multiple_31370.geom.1.1"><gml:pos>108738.579673115 '
                '195614.818229658</gml:pos></gml:Point></gml:pointMember'
                '></gml:MultiPoint><gml:Distance '
                'units="meter">100.000000</gml:Distance></fes:DWithin>'
                '</fes:Or>')


class TestLine(object):
    """Class grouping tests for line locations."""

    def test_line_single_31370(self):
        """Test the WithinDistance filter with a GML containing a single
        line geometry in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/line_single_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, WithinDistance, {'distance': 100})
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:DWithin><fes:ValueReference>geom</fes:ValueReference><gml'
            ':LineString srsName="urn:ogc:def:crs:EPSG::31370" gml:id="line_'
            'single_31370.geom.0"><gml:posList'
            '>108344.619471974 195008.119519901 108801.613305297 '
            '194842.656235421 109077.385446096 '
            '195094.790764152</gml:posList></gml:LineString><gml:Distance '
            'units="meter">100.000000</gml:Distance></fes:DWithin>')

    def test_line_multiple_31370(self):
        """Test the WithinDistance filter with a GML containing multiple
        line geometries in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/line_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, WithinDistance, {'distance': 100})
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 2

        lines = [
            '108344.619471974 195008.119519901 108801.613305297 '
            '194842.656235421 109077.385446096 195094.790764152',
            '108194.91459554 196032.416042867 108714.942061046 '
            '195528.146985407 108911.922161617 195528.146985407']

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}DWithin'

            point = f.find('./{http://www.opengis.net/gml/3.2}LineString')
            assert point.get('srsName') == 'urn:ogc:def:crs:EPSG::31370'

            posList = point.find(
                './{http://www.opengis.net/gml/3.2}posList').text
            assert posList in lines

            lines.remove(posList)

        assert len(lines) == 0

    def test_line_multiple_31370_stable(self):
        """Test the WithinDistance filter with a GML containing multiple
        line geometries in EPSG:31370.

        Test whether the generated XML is correct and stable.

        """
        with open('tests/data/util/location/line_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        for i in range(10):
            f = GmlFilter(gml, WithinDistance, {'distance': 100})
            f.set_geometry_column('geom')
            xml = f.toXML()

            assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
                '<fes:Or><fes:DWithin><fes:ValueReference>geom</fes'
                ':ValueReference><gml:LineString '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="line_'
                'multiple_31370.geom.0"><gml:posList>108344'
                '.619471974 195008.119519901 108801.613305297 '
                '194842.656235421 109077.385446096 '
                '195094.790764152</gml:posList></gml:LineString><gml'
                ':Distance units="meter">100.000000</gml:Distance></fes'
                ':DWithin><fes:DWithin><fes:ValueReference>geom</fes'
                ':ValueReference><gml:LineString '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="line_'
                'multiple_31370.geom.1"><gml:posList>108194'
                '.91459554 196032.416042867 108714.942061046 '
                '195528.146985407 108911.922161617 '
                '195528.146985407</gml:posList></gml:LineString><gml'
                ':Distance units="meter">100.000000</gml:Distance>'
                '</fes:DWithin></fes:Or>')


class TestMultiline(object):
    """Class grouping tests for multiline locations."""

    def test_multiline_single_31370(self):
        """Test the WithinDistance filter with a GML containing a single
        multiline geometry in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/multiline_single_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, WithinDistance, {'distance': 100})
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:DWithin><fes:ValueReference>geom</fes:ValueReference><gml'
            ':MultiCurve srsName="urn:ogc:def:crs:EPSG::31370" gml:id="multi'
            'line_single_31370.geom.0"><gml'
            ':curveMember><gml:LineString gml:id="multi'
            'line_single_31370.geom.0.0"><gml:posList>108210.673003586 '
            '194850.535439444 108454.928328293 195031.757131969 '
            '108746.458877137 194834.777031398</gml:posList></gml:LineString'
            '></gml:curveMember><gml:curveMember><gml:LineString gml:id="multi'
            'line_single_31370.geom.0.1"><gml'
            ':posList>109164.056690347 195055.394744037 109211.331914484 '
            '194661.434542896 109416.191219077 '
            '194440.816830258</gml:posList></gml:LineString></gml'
            ':curveMember></gml:MultiCurve><gml:Distance '
            'units="meter">100.000000</gml:Distance></fes:DWithin>')

    def test_multiline_multiple_31370(self):
        """Test the WithinDistance filter with a GML containing multiple
        multiline geometries in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/multiline_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, WithinDistance, {'distance': 100})
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 2

        multilines = [
            ['108210.673003586 194850.535439444 108454.928328293 '
             '195031.757131969 108746.458877137 194834.777031398',
             '109164.056690347 195055.394744037 109211.331914484 '
             '194661.434542896 109416.191219077 194440.816830258'],
            ['108226.431411631 196095.44967505 108384.015492088 '
             '196276.671367574 108580.995592658 196048.174450913',
             '108911.922161617 196379.101019871 109030.110221959 '
             '196552.443508373 109282.244750689 196607.597936533']]

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}DWithin'

            multicurve = f.find('./{http://www.opengis.net/gml/3.2}MultiCurve')
            assert multicurve.get('srsName') == 'urn:ogc:def:crs:EPSG::31370'

            posList = [p.text for p in multicurve.findall(
                './/{http://www.opengis.net/gml/3.2}posList')]
            multilines.remove(posList)

        assert len(multilines) == 0

    def test_multiline_multiple_31370_stable(self):
        """Test the WithinDistance filter with a GML containing multiple
        multiline geometries in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/multiline_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        for i in range(10):
            f = GmlFilter(gml, WithinDistance, {'distance': 100})
            f.set_geometry_column('geom')
            xml = f.toXML()

            assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
                '<fes:Or><fes:DWithin><fes:ValueReference>geom</fes'
                ':ValueReference><gml:MultiCurve '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="multi'
                'line_multiple_31370.geom.0"><gml:curveMember><gml'
                ':LineString gml:id="multi'
                'line_multiple_31370.geom.0.0"><gml:posList>108210.673003586'
                ' 194850.535439444 '
                '108454.928328293 195031.757131969 108746.458877137 '
                '194834.777031398</gml:posList></gml:LineString></gml'
                ':curveMember><gml:curveMember><gml:LineString gml:id="multi'
                'line_multiple_31370.geom.0.1"><gml:posList'
                '>109164.056690347 195055.394744037 109211.331914484 '
                '194661.434542896 109416.191219077 '
                '194440.816830258</gml:posList></gml:LineString></gml'
                ':curveMember></gml:MultiCurve><gml:Distance '
                'units="meter">100.000000</gml:Distance></fes:DWithin><fes'
                ':DWithin><fes:ValueReference>geom</fes:ValueReference><gml'
                ':MultiCurve '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="multi'
                'line_multiple_31370.geom.1"><gml:curveMember><gml'
                ':LineString gml:id="multi'
                'line_multiple_31370.geom.1.0"><gml:posList>108226.431411631'
                ' 196095.44967505 '
                '108384.015492088 196276.671367574 108580.995592658 '
                '196048.174450913</gml:posList></gml:LineString></gml'
                ':curveMember><gml:curveMember><gml:LineString gml:id="multi'
                'line_multiple_31370.geom.1.1"><gml:posList'
                '>108911.922161617 196379.101019871 109030.110221959 '
                '196552.443508373 109282.244750689 '
                '196607.597936533</gml:posList></gml:LineString></gml'
                ':curveMember></gml:MultiCurve><gml:Distance '
                'units="meter">100.000000</gml:Distance></fes:DWithin>'
                '</fes:Or>')


class TestPolygon(object):
    """Class grouping tests for polygon locations."""

    def test_polygon_single_31370(self):
        """Test the Within filter with a GML containing a single
        polygon geometry in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/polygon_single_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, Within)
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Within><fes:ValueReference>geom</fes:ValueReference><gml'
            ':Polygon srsName="urn:ogc:def:crs:EPSG::31370" gml:id="polygon_'
            'single_31370.geom.0"><gml:exterior'
            '><gml:LinearRing><gml:posList>108636.150020818 194960.844295764 '
            '108911.922161617 194291.111953824 109195.573506438 '
            '195118.42837622 108636.150020818 '
            '194960.844295764</gml:posList></gml:LinearRing></gml:exterior'
            '></gml:Polygon></fes:Within>')

    def test_polyon_multiple_31370(self):
        """Test the Within filter with a GML containing multiple
        polygon geometries in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/polygon_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, Within)
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 2

        polygons = [
            '108636.150020818 194960.844295764 108911.922161617 '
            '194291.111953824 109195.573506438 195118.42837622 '
            '108636.150020818 194960.844295764',
            '107485.786233486 196741.544404921 107840.350414513 '
            '196339.704999757 108297.344247837 196843.974057217 '
            '107485.786233486 196741.544404921']

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}Within'

            point = f.find('./{http://www.opengis.net/gml/3.2}Polygon')
            assert point.get('srsName') == 'urn:ogc:def:crs:EPSG::31370'

            posList = point.find(
                './/{http://www.opengis.net/gml/3.2}posList').text
            assert posList in polygons

            polygons.remove(posList)

        assert len(polygons) == 0

    def test_polyon_multiple_31370_stable(self):
        """Test the Within filter with a GML containing multiple
        polygon geometries in EPSG:31370.

        Test whether the generated XML is correct and stable.

        """
        with open('tests/data/util/location/polygon_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        for i in range(10):
            f = GmlFilter(gml, Within)
            f.set_geometry_column('geom')
            xml = f.toXML()

            assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
                '<fes:Or><fes:Within><fes:ValueReference>geom</fes'
                ':ValueReference><gml:Polygon '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="polygon_'
                'multiple_31370.geom.0"><gml:exterior'
                '><gml:LinearRing><gml:posList>108636.150020818 '
                '194960.844295764 108911.922161617 194291.111953824 '
                '109195.573506438 195118.42837622 108636.150020818 '
                '194960.844295764</gml:posList></gml:LinearRing></gml'
                ':exterior></gml:Polygon></fes:Within><fes:Within><fes'
                ':ValueReference>geom</fes:ValueReference><gml:Polygon '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="polygon_'
                'multiple_31370.geom.1"><gml:exterior'
                '><gml:LinearRing><gml:posList>107485.786233486 '
                '196741.544404921 107840.350414513 196339.704999757 '
                '108297.344247837 196843.974057217 107485.786233486 '
                '196741.544404921</gml:posList></gml:LinearRing></gml'
                ':exterior></gml:Polygon></fes:Within></fes:Or>')

    def test_polyon_multiple_disjoint_31370(self):
        """Test the Disjoint filter with the And combinator with a GML
        containing multiple polygon geometries in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/polygon_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, Disjoint, combinator=And)
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}And'
        assert len(list(xml)) == 2

        polygons = [
            '108636.150020818 194960.844295764 108911.922161617 '
            '194291.111953824 109195.573506438 195118.42837622 '
            '108636.150020818 194960.844295764',
            '107485.786233486 196741.544404921 107840.350414513 '
            '196339.704999757 108297.344247837 196843.974057217 '
            '107485.786233486 196741.544404921']

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}Disjoint'

            point = f.find('./{http://www.opengis.net/gml/3.2}Polygon')
            assert point.get('srsName') == 'urn:ogc:def:crs:EPSG::31370'

            posList = point.find(
                './/{http://www.opengis.net/gml/3.2}posList').text
            assert posList in polygons

            polygons.remove(posList)

        assert len(polygons) == 0


class TestMultipolygon(object):
    """Class grouping tests for multipolygon locations."""

    def test_multipolygon_single_31370(self):
        """Test the Within filter with a GML containing a single
        multipolygon geometry in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/multipolygon_single_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, Within)
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Within><fes:ValueReference>geom</fes:ValueReference><gml'
            ':MultiSurface srsName="urn:ogc:def:crs:EPSG::31370" gml:id="multi'
            'polygon_single_31370.geom.0"><gml'
            ':surfaceMember><gml:Polygon gml:id="multi'
            'polygon_single_31370.geom.0.0"><gml:exterior><gml:LinearRing><gml'
            ':posList>108588.874796681 195015.998723923 108911.922161617 '
            '194251.71593371 109195.573506438 195134.186784266 '
            '108588.874796681 195015.998723923</gml:posList></gml:LinearRing'
            '></gml:exterior></gml:Polygon></gml:surfaceMember><gml'
            ':surfaceMember><gml:Polygon gml:id="multi'
            'polygon_single_31370.geom.0.1"><gml:exterior><gml:LinearRing><gml'
            ':posList>109140.419078278 195748.764698045 109400.432811031 '
            '195307.529272768 109597.412911602 195772.402310114 '
            '109140.419078278 195748.764698045</gml:posList></gml:LinearRing'
            '></gml:exterior></gml:Polygon></gml:surfaceMember></gml'
            ':MultiSurface></fes:Within>')

    def test_multipolygon_multiple_31370(self):
        """Test the Within filter with a GML containing multiple
        multipolygon geometries in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/multipolygon_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        f = GmlFilter(gml, Within)
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert xml.tag == '{http://www.opengis.net/fes/2.0}Or'
        assert len(list(xml)) == 2

        multipolygons = [
            ['107564.578273715 196646.993956647 107785.195986354 '
             '196386.980223894 107966.417678878 197143.383810084 '
             '107564.578273715 196646.993956647',
             '108384.015492088 197214.29664629 108447.04912427 '
             '196489.40987619 108785.854897252 197269.45107445 '
             '108384.015492088 197214.29664629'],
            ['108588.874796681 195015.998723923 108911.922161617 '
             '194251.71593371 109195.573506438 195134.186784266 '
             '108588.874796681 195015.998723923',
             '109140.419078278 195748.764698045 109400.432811031 '
             '195307.529272768 109597.412911602 195772.402310114 '
             '109140.419078278 195748.764698045']]

        for f in xml:
            assert f.tag == '{http://www.opengis.net/fes/2.0}Within'

            multicurve = f.find(
                './{http://www.opengis.net/gml/3.2}MultiSurface')
            assert multicurve.get('srsName') == 'urn:ogc:def:crs:EPSG::31370'

            posList = [p.text for p in multicurve.findall(
                './/{http://www.opengis.net/gml/3.2}posList')]
            multipolygons.remove(posList)

        assert len(multipolygons) == 0

    def test_multipolygon_multiple_31370_stable(self):
        """Test the Within filter with a GML containing multiple
        multipolygon geometries in EPSG:31370.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/multipolygon_multiple_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        for i in range(10):
            f = GmlFilter(gml, Within)
            f.set_geometry_column('geom')
            xml = f.toXML()

            assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
                '<fes:Or><fes:Within><fes:ValueReference>geom</fes'
                ':ValueReference><gml:MultiSurface '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="multi'
                'polygon_multiple_31370.geom.0"><gml:surfaceMember'
                '><gml:Polygon gml:id="multi'
                'polygon_multiple_31370.geom.0.0"><gml:exterior>'
                '<gml:LinearRing><gml:posList'
                '>107564.578273715 196646.993956647 107785.195986354 '
                '196386.980223894 107966.417678878 197143.383810084 '
                '107564.578273715 '
                '196646.993956647</gml:posList></gml:LinearRing'
                '></gml:exterior></gml:Polygon></gml:surfaceMember><gml'
                ':surfaceMember><gml:Polygon gml:id="multi'
                'polygon_multiple_31370.geom.0.1"><gml:exterior><gml:LinearRing'
                '><gml:posList>108384.015492088 197214.29664629 '
                '108447.04912427 196489.40987619 108785.854897252 '
                '197269.45107445 108384.015492088 '
                '197214.29664629</gml:posList></gml:LinearRing'
                '></gml:exterior></gml:Polygon></gml:surfaceMember></gml'
                ':MultiSurface></fes:Within><fes:Within><fes:ValueReference'
                '>geom</fes:ValueReference><gml:MultiSurface '
                'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="multi'
                'polygon_multiple_31370.geom.1"><gml:surfaceMember'
                '><gml:Polygon gml:id="multi'
                'polygon_multiple_31370.geom.1.0"><gml:exterior>'
                '<gml:LinearRing><gml:posList'
                '>108588.874796681 195015.998723923 108911.922161617 '
                '194251.71593371 109195.573506438 195134.186784266 '
                '108588.874796681 '
                '195015.998723923</gml:posList></gml:LinearRing'
                '></gml:exterior></gml:Polygon></gml:surfaceMember><gml'
                ':surfaceMember><gml:Polygon gml:id="multi'
                'polygon_multiple_31370.geom.1.1"><gml:exterior><gml:LinearRing'
                '><gml:posList>109140.419078278 195748.764698045 '
                '109400.432811031 195307.529272768 109597.412911602 '
                '195772.402310114 109140.419078278 '
                '195748.764698045</gml:posList></gml:LinearRing'
                '></gml:exterior></gml:Polygon></gml:surfaceMember></gml'
                ':MultiSurface></fes:Within></fes:Or>')


class TestCombination(object):
    """Class grouping tests for combinations of locations."""

    def test_polygon_and_box(self, mp_gml_id):
        """Test the combination of a Within filter with a GML containing a
        single polygon geometry in EPSG:31370 and a Box.

        Test whether the generated XML is correct.

        """
        with open('tests/data/util/location/polygon_single_31370.gml',
                  'r') as gml_file:
            gml = gml_file.read()

        polygon = GmlFilter(gml, Within)
        box = Box(94720, 186910, 112220, 202870)

        location_filter = Or([polygon, Within(box)])
        set_geometry_column(location_filter, 'geom')
        xml = location_filter.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Or><fes:Within><fes:ValueReference>geom</fes:ValueReference'
            '><gml:Polygon srsName="urn:ogc:def:crs:EPSG::31370" gml:id="'
            'polygon_single_31370.geom.0"><gml'
            ':exterior><gml:LinearRing><gml:posList>108636.150020818 '
            '194960.844295764 108911.922161617 194291.111953824 '
            '109195.573506438 195118.42837622 108636.150020818 '
            '194960.844295764</gml:posList></gml:LinearRing></gml:exterior'
            '></gml:Polygon></ogc:Within><ogc:Within><fes:ValueReference>geom'
            '</fes:ValueReference><gml:Envelope srsDimension="2" '
            'srsName="http://www.opengis.net/gml/srs/epsg.xml#31370" gml32:id='
            '"pydov.gmlid"><gml:lowerCorner>94720.000000 '
            '186910.000000</gml:lowerCorner><gml:upperCorner>112220.000000 '
            '202870.000000</gml:upperCorner></gml:Envelope></fes'
            ':Within></fes:Or>')


class TestGeometryFilter(object):
    """Class grouping tests for the GeometryFilter."""

    def test_shapefile(self):
        """Test the conversion of a shapefile to GML using fiona,
        Within operator.

        Test whether the generated XML is correct and stable.
        """
        shapefile = 'tests/data/util/location/polygon_multiple_31370.shp'

        f = GeometryFilter(shapefile, Within)
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Or xmlns:gml="http://www.opengis.net/gml/3.2" '
            'xmlns:fes="http://www.opengis.net/fes/2.0"><fes:Within><fes:'
            'ValueReference>geom</fes:ValueReference><gml:Polygon srsName='
            '"urn:ogc:def:crs:EPSG::31370" gml:id="polygon_multiple_31370'
            '.geom.0"><gml:exterior>'
            '<gml:LinearRing><gml:posList>108636.150020818 '
            '194960.844295764 109195.573506438 195118.42837622 '
            '108911.922161617 194291.111953824 108636.150020818 '
            '194960.844295764</gml:posList></gml:LinearRing>'
            '</gml:exterior></gml:Polygon></fes:Within><fes:Within>'
            '<fes:ValueReference>geom</fes:ValueReference><gml:Polygon '
            'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="polygon_multiple'
            '_31370.geom.1"><gml:exterior>'
            '<gml:LinearRing><gml:posList>107485.786233486 '
            '196741.544404921 108297.344247837 196843.974057217 '
            '107840.350414513 196339.704999757 107485.786233486 '
            '196741.544404921</gml:posList></gml:LinearRing>'
            '</gml:exterior></gml:Polygon></fes:Within></fes:Or>')

    def test_geopackage(self):
        """Test the conversion of a geopackage to GML using fiona,
        Within operator.

        Test whether the generated XML is correct and stable.
        """
        gpkg = 'tests/data/util/location/polygon_multiple_31370.gpkg'

        f = GeometryFilter(gpkg, Within)
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Or xmlns:fes="http://www.opengis.net/fes/2.0"><fes:Within>'
            '<fes:ValueReference>geom</fes:ValueReference><gml:Polygon '
            'xmlns:gml="http://www.opengis.net/gml/3.2" '
            'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="polygon_multiple_'
            '31370.geom.0"><gml:exterior>'
            '<gml:LinearRing><gml:posList>108636.150020818 194960.844295764 '
            '108911.922161617 194291.111953824 109195.573506438 '
            '195118.42837622 108636.150020818 194960.844295764</gml:posList>'
            '</gml:LinearRing></gml:exterior></gml:Polygon></fes:Within>'
            '<fes:Within><fes:ValueReference>geom</fes:ValueReference>'
            '<gml:Polygon xmlns:gml="http://www.opengis.net/gml/3.2" '
            'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="polygon_multiple_'
            '31370.geom.1"><gml:exterior>'
            '<gml:LinearRing><gml:posList>107485.786233486 196741.544404921 '
            '107840.350414513 196339.704999757 108297.344247837 '
            '196843.974057217 107485.786233486 196741.544404921</gml:posList>'
            '</gml:LinearRing></gml:exterior></gml:Polygon></fes:Within>'
            '</fes:Or>')


class TestGeopandasFilter:

    def test_geopandas_dataframe(self):
        """Test the conversion of a GeoPandas GeoDataFrame

        Test whether the generated XML is correct and stable.
        """
        shapefile = 'tests/data/util/location/polygon_multiple_31370.shp'
        import geopandas as gpd
        gdf = gpd.read_file(shapefile)

        f = GeopandasFilter(gdf, Within)
        f.set_geometry_column('geom')
        xml = f.toXML()

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Or xmlns:gml="http://www.opengis.net/gml/3.2" '
            'xmlns:fes="http://www.opengis.net/fes/2.0"><fes:Within><fes:'
            'ValueReference>geom</fes:ValueReference><gml:Polygon srsName='
            '"urn:ogc:def:crs:EPSG::31370" gml:id="geodataframe.geom.0"'
            '><gml:exterior>'
            '<gml:LinearRing><gml:posList>108636.150020818 '
            '194960.844295764 109195.573506438 195118.42837622 '
            '108911.922161617 194291.111953824 108636.150020818 '
            '194960.844295764</gml:posList></gml:LinearRing>'
            '</gml:exterior></gml:Polygon></fes:Within><fes:Within>'
            '<fes:ValueReference>geom</fes:ValueReference><gml:Polygon '
            'srsName="urn:ogc:def:crs:EPSG::31370" gml:id="geodataframe.geom.1"'
            '><gml:exterior>'
            '<gml:LinearRing><gml:posList>107485.786233486 '
            '196741.544404921 108297.344247837 196843.974057217 '
            '107840.350414513 196339.704999757 107485.786233486 '
            '196741.544404921</gml:posList></gml:LinearRing>'
            '</gml:exterior></gml:Polygon></fes:Within></fes:Or>')

    def test_geopandas_dataframe_subset(self):
        """Test the conversion of a GeoPandas GeoDataFrame subset.

        Test whether the generated XML is correct and stable.
        """
        shapefile = 'tests/data/util/location/polygon_multiple_31370.shp'
        import geopandas as gpd
        gdf = gpd.read_file(shapefile)

        # geopandas subselection to single feature line geodataframe
        f = GeopandasFilter(gdf.iloc[[0]], Within)
        f.set_geometry_column('geom')
        xml = f.toXML()

        print(clean_xml(etree.tostring(xml).decode('utf8')))

        assert clean_xml(etree.tostring(xml).decode('utf8')) == clean_xml(
            '<fes:Within xmlns:gml="http://www.opengis.net/gml/3.2" '
            'xmlns:fes="http://www.opengis.net/fes/2.0"><fes:ValueReference>'
            'geom</fes:ValueReference><gml:Polygon srsName="urn:ogc:def:crs:'
            'EPSG::31370" gml:id="geodataframe.geom.0"><gml:exterior><gml:'
            'LinearRing><gml:posList>'
            '108636.150020818 194960.844295764 109195.573506438 '
            '195118.42837622 108911.922161617 194291.111953824 '
            '108636.150020818 194960.844295764</gml:posList>'
            '</gml:LinearRing></gml:exterior></gml:Polygon>'
            '</fes:Within>')

    def test_geopandas_series(self):
        """Test GeoPandas GeoSeries not supported by pydov spatial filter
        """
        shapefile = 'tests/data/util/location/polygon_multiple_31370.shp'
        import geopandas as gpd
        gdf = gpd.read_file(shapefile)

        # geopandas geometry not supported Type
        with pytest.raises(TypeError):
            GeopandasFilter(gdf.geometry, Within)

        # geopandas series not supported Type
        with pytest.raises(TypeError):
            GeopandasFilter(gdf.iloc[0, :], Within)

    def test_geopandas_nocrs(self):
        """Test GeoPandas GeoSeries not supported by pydov spatial filter
        """
        shapefile = 'tests/data/util/location/polygon_multiple_31370.shp'
        import geopandas as gpd
        gdf = gpd.read_file(shapefile)
        gdf.crs = None

        # geopandas geometry not supported Type
        with pytest.raises(AttributeError):
            GeopandasFilter(gdf, Within)
