from pydov.search.sondering import SonderingSearch
from pydov.util.location import Within, GeometryFilter

path = r"tests/data/util/location/polygon_multiple_31370.shp"
sonderingsearch = SonderingSearch()
df_sondering = sonderingsearch.search(location=GeometryFilter(path, Within))
