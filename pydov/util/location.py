from owslib.etree import etree


class AbstractLocation(object):
    def get_element(self):
        raise NotImplementedError


class AbstractLocationFilter(object):
    def set_geometry_column(self, geometry_column):
        raise NotImplementedError

    def get_element(self):
        raise NotImplementedError


class Box(AbstractLocation):
    def __init__(self, minx, miny, maxx, maxy, epsg=31370):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

        self.element = etree.Element('{http://www.opengis.net/gml}Envelope')
        self.element.set('srsDimension', '2')
        self.element.set('srsName',
                         'http://www.opengis.net/gml/srs/epsg.xml#%i' % epsg)

        lower_corner = etree.Element('{http://www.opengis.net/gml}lowerCorner')
        lower_corner.text = '%0.3f %0.3f' % (self.minx, self.miny)
        self.element.append(lower_corner)

        upper_corner = etree.Element('{http://www.opengis.net/gml}upperCorner')
        upper_corner.text = '%0.3f %0.3f' % (self.maxx, self.maxy)
        self.element.append(upper_corner)

    def get_element(self):
        return self.element


class Point(AbstractLocation):
    def __init__(self, x, y, epsg=31370):
        self.x = x
        self.y = y

        self.element = etree.Element('{http://www.opengis.net/gml}Point')
        self.element.set('srsName',
                         'http://www.opengis.net/gml/srs/epsg.xml#%i' % epsg)

        coordinates = etree.Element('{http://www.opengis.net/gml}coordinates')
        coordinates.set('decimal', '.')
        coordinates.set('cs', ',')
        coordinates.set('ts', ' ')
        coordinates.text = '%f,%f' % (self.x, self.y)

    def get_element(self):
        return self.element


class Within(AbstractLocationFilter):
    def __init__(self, box):
        self.box = box
        self.geom_column = ''

        self.element = etree.Element('{http://www.opengis.net/ogc}Within')

        geom = etree.Element('{http://www.opengis.net/ogc}PropertyName')
        geom.text = self.geom_column

        self.element.append(geom)
        self.element.append(box.get_element())

    def set_geometry_column(self, geometry_column):
        self.geom_column = geometry_column
        geom = self.element.find('.//{http://www.opengis.net/ogc}PropertyName')
        geom.text = geometry_column

    def get_element(self):
        if self.geom_column == '':
            raise RuntimeError('Geometry column has not been set. Use '
                               '"set_geometry_column" to set it.')
        return self.element


class WithinDistance(AbstractLocationFilter):
    def __init__(self, point, distance, distance_units='meter'):
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
        self.geom_column = geometry_column
        geom = self.element.find('.//{http://www.opengis.net/ogc}PropertyName')
        geom.text = geometry_column

    def get_element(self):
        if self.geom_column == '':
            raise RuntimeError('Geometry column has not been set. Use '
                               '"set_geometry_column" to set it.')
        return self.element
