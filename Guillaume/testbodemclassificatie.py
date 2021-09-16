import pandas as pd
from pydov.search.bodemclassificatie import BodemclassificatieSearch
from owslib.fes import PropertyIsEqualTo

from pydov.util.location import Box, Within

bodemclassificatie = BodemclassificatieSearch()
fields = bodemclassificatie.get_fields()
for f in fields.values():
    print(f['name'])


df2 = bodemclassificatie.search(location=Within(Box(124000, 197800, 134500, 204000)))

pd.set_option('display.max_columns', None, 'display.max_rows',None,'max_colwidth', None, 'display.width',None)
df = pd.DataFrame(df2)
print(df)
