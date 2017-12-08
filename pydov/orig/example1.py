import matplotlib.pyplot as plt
from dovseries import DovGroundwater

dov = DovGroundwater("../tests/data/1-0709.xml")
dov.peilmetingen.plot()

dov.peilmetingen_timeseries.resample('A').mean().plot()

print(dov.peilmetingen.head())
print(dov.observaties.head())
print(dov.metadata_locatie)
print(dov.metadata_filters['1'])
print(dov.peilmetingen.shape)

dov.peilmetingen.reset_index().pivot_table(index="datum",
                                           columns=["grondwaterlocatie",
                                                    "filternummer"],
                                           values="diepte").plot()

dov.observaties.pivot_table(index="datum",
                            columns=["parameter"],
                            values="waarde").plot()

dov.get_parameter_series("NO3").plot(kind='barh')
plt.tight_layout()

plt.show()
