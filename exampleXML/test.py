import pandas as pd
import xmltodict
import matplotlib.pyplot as plt


def get_peilmetingen(xml_doc):
    for filter in xml_doc["ns2:dov-schema"]['filtermeting']:
        for meting in filter['peilmeting']:
            yield (filter['grondwaterlocatie'], 
                   filter['filter']['identificatie'], 
                   meting['datum'],
                   meting['peil_mtaw'])


def get_peilmetingen_df(xml_doc):
    doc_df = pd.DataFrame(list(get_peilmetingen(xml_doc)), columns =["grondwaterlocatie",
    "filternummer","datum","diepte"])
    doc_df["datum"] = pd.to_datetime(doc_df["datum"])
    doc_df["diepte"]  = pd.to_numeric(doc_df["diepte"])
    return doc_df
            
with open('1-0709.xml') as fd:
    doc = xmltodict.parse(fd.read())

doc_df = get_peilmetingen_df(doc)
filter1 =doc_df [(doc_df.filternummer == "1")]

fig, ax = plt.subplots(figsize=(16, 10))
fig.show()
filter1[["datum", "diepte"]].set_index("datum").plot(ax=ax, style='-')
