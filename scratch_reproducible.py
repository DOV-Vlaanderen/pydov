import pydov
from pydov.util.location import Within, WithinDistance, Box, Point, GmlFilter
from pydov.search.interpretaties import LithologischeBeschrijvingenSearch

from owslib.fes import And, Or, Not
from owslib.fes import PropertyIsEqualTo, PropertyIsLike, PropertyIsNull, PropertyIsLessThan
from owslib.fes import SortBy, SortProperty
from pydov.util.hooks import RepeatableLogRecorder
from pydov.util.hooks import RepeatableLogReplayer

pydov.hooks.append(RepeatableLogReplayer("C:\\Users\\Joris Synaeve\\Documents\\Python Scripts\\pydov tmp\\pydov-archive-20200127T134514-6e9f12.zip"))
pydov.hooks.append(RepeatableLogRecorder("C:\\Users\\Joris Synaeve\\Documents\\Python Scripts\\pydov tmp"))

ip_litho = LithologischeBeschrijvingenSearch()


# Get all lithological descriptions in a bounding box (llx, lly, ulx, uly)
# the pkey_boring link is not available below, but is in the df
df = ip_litho.search(
    query=And([PropertyIsLike(propertyname='pkey_boring', literal='https://www.dov.vlaanderen.be/data/boring/189%'),
               PropertyIsLessThan(propertyname='x', literal='200000')]),
    location=Or([WithinDistance(Point(200000, 205000), 10, 'km'),GmlFilter('tests/data/util/location/multipolygon_multiple_31370.gml', Within)]),
    return_fields=('pkey_interpretatie', 'pkey_boring', 'beschrijving'),
    sort_by=SortBy([SortProperty('pkey_interpretatie', 'DESC')]))
df = df[df.beschrijving.notnull()]
print(df.head())
