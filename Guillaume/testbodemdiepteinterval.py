import pandas as pd
from pydov.search.bodemdiepteinterval import BodemdiepteintervalSearch
from owslib.fes import PropertyIsEqualTo

from pydov.util.location import Box, Within

bodemdiepteinterval = BodemdiepteintervalSearch()
fields = bodemdiepteinterval.get_fields()
for f in fields.values():
    print(f['name'])


df2 = bodemdiepteinterval.search(location=Within(Box(124000, 197800, 134500, 204000)))

pd.set_option('display.max_columns', None, 'display.max_rows',None,'max_colwidth', None, 'display.width',None)
df = pd.DataFrame(df2)
print(df)
