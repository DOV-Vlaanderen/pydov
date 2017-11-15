import xmltodict
import pandas as pd


class DOVVariableError(Exception):
    pass


namespaces = {"http://kern.schemas.dov.vlaanderen.be": 'kern'}


class DovGroundwater(object):
    def __init__(self, xml_doc):
        with open(xml_doc) as fd:
            doc = xmltodict.parse(fd.read(), process_namespaces=True,
                                  namespaces=namespaces)
            self.peilmetingen = self._get_peilmetingen_df(doc)
            self.observaties = self._get_observaties_df(doc)
            self.metadata_locatie = doc["kern:dov-schema"]["grondwaterlocatie"]
            self.metadata_filters = self._get_filter_metadata(doc)

    @staticmethod
    def _get_filter_metadata(doc):
        """"""
        filter_info = {}
        for filterd in doc["kern:dov-schema"]['filter']:
            filter_info[filterd["identificatie"]] = filterd
        return filter_info

    @staticmethod
    def get_peilmetingen(doc):
        """Generator to extract the individual measurements from the XML
        export"""
        for filterm in doc["kern:dov-schema"]['filtermeting']:
            for meting in filterm['peilmeting']:
                yield (filterm['grondwaterlocatie'],
                       filterm['filter']['identificatie'],
                       meting['datum'],
                       meting['peil_mtaw'],
                       meting['methode'],
                       meting['betrouwbaarheid'])

    def _get_peilmetingen_df(self, doc):
        """"""
        doc_df = pd.DataFrame(list(self.get_peilmetingen(doc)),
                              columns=["grondwaterlocatie",
                                       "filternummer",
                                       "datum",
                                       "diepte",
                                       "methode",
                                       "betrouwbaarheid"])
        doc_df["datum"] = pd.to_datetime(doc_df["datum"])
        doc_df["diepte"] = pd.to_numeric(doc_df["diepte"])
        doc_df = doc_df.set_index("datum")
        return doc_df

    @staticmethod
    def get_observaties(doc):
        """Generator to extract the individual observations from the XML
        export"""
        for filterm in doc["kern:dov-schema"]['filtermeting']:
            for watermonster in filterm['watermonster']:
                for observatie in watermonster['observatie']:
                    yield (filterm['grondwaterlocatie'],
                           filterm['filter']['identificatie'],
                           watermonster['identificatie'],
                           ' '.join([watermonster['monstername']['datum'],
                                     watermonster['monstername']['tijd']]),
                           observatie['parameter'],
                           observatie['waarde_numeriek'],
                           observatie['eenheid'],
                           observatie['betrouwbaarheid'])

    def _get_observaties_df(self, doc):
        """"""
        doc_df = pd.DataFrame(list(self.get_observaties(doc)),
                              columns=["grondwaterlocatie",
                                       "filternummer",
                                       "monsternummer",
                                       "datum",
                                       "parameter",
                                       "waarde",
                                       "eenheid",
                                       "betrouwbaarheid"])
        doc_df["datum"] = pd.to_datetime(doc_df["datum"])
        doc_df["waarde"] = pd.to_numeric(doc_df["waarde"])
        return doc_df

    @property
    def variables(self):
        """return list of variables currently stored"""
        return self.observaties["parameter"].unique()

    def get_parameter_series(self, variable):
        """select specific parameter"""
        if variable not in self.observaties["parameter"].unique():
            raise DOVVariableError("Variable name {} not represented in "
                                   "observations".format(variable))

        vardata = self.observaties[self.observaties["parameter"] == variable]
        return vardata.pivot_table(
            index="datum",
            columns=["filternummer"],
            values="waarde")

    @property
    def peilmetingen_timeseries(self):
        return self.peilmetingen.reset_index().pivot_table(
            index="datum",
            columns=["grondwaterlocatie", "filternummer"],
            values="diepte")
