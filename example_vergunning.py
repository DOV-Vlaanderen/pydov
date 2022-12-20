from pydov.search.grondwatervergunning import GrondwaterVergunningSearch
from pydov.util.location import Within, Box

from owslib.fes2 import PropertyIsEqualTo

s = GrondwaterVergunningSearch()

df = s.search(query=PropertyIsEqualTo('pkey_installatie',
              'https://www.dov.vlaanderen.be/data/installatie/2021-098492'))
print(df)
