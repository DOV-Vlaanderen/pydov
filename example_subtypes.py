from pydov.search.boring import Boring, BoringSearch

print(
    Boring.find_subtypes(),
    Boring.find_fieldsets()
)

s = BoringSearch()
print(s.search(max_features=1))
