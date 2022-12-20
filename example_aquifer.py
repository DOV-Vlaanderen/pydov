from pydov.search.grondwaterfilter import GrondwaterFilterSearch

s = GrondwaterFilterSearch()
print(s.get_fields()['aquifer_code'])
