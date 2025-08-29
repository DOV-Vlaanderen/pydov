import os
import pandas as pd
from pydov.search.generic import WfsSearch
from pydov.search.grondwatermonster import GrondwaterMonsterSearch
from pydov.search.grondwaterfilter import GrondwaterFilterSearch
from pydov.util.location import Within, Box
from pydov.util.query import Join
from loguru import logger
from owslib.fes2 import PropertyIsEqualTo, And, Or
from tqdm.auto import tqdm
from datetime import datetime
from importlib.metadata import version
import json


class RequestPFASdata:

    def __init__(self):
        """Initialize the class.

        Create a metadata file that contains the date, necessary package versions and the datapoints count.
        """

        def json_serial(obj):
            """JSON serializer for objects not serializable by default json code

            Parameters
            ----------
            obj : datetime
                The date and time.

            Returns
            -------
            The date as a string.
            """

            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError("Type %s not serializable" % type(obj))

        date = datetime.now()
        date = json_serial(date)

        package_versions = (f'pandas: {version("pandas")}', f'pydov: {version("pydov")}')

        self.dictionary = {"date": date, "versions": package_versions, "nb_datapoints": [{}]}
        self.combined_datasets = {}

    def wfs_request(self, layer, location, max_features, query=None, sort_by=None):
        """Download the available PFAS-data through a wfs request.

        Parameters
        ----------
        layer : str
            The name of the layer containing the PFAS-data.
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)
        query:
            Find data based on one or more of its attribute values.
            (https://pydov.readthedocs.io/en/stable/query_attribute.html)
        sort_by:
            Sort on one or multiple attributes.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded PFAS-data.
        """

        wfsSearch = WfsSearch(layer)
        return wfsSearch.search(
            location=location,
            query=query,
            sort_by=sort_by,
            max_features=max_features)

    def pydov_request(self, location, max_features, query=None, sort_by=None):
        """Function to download the groundwater monster and according filter data for a specific bounding box.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)
        query:
            Find data based on one or more of its attribute values.
            (https://pydov.readthedocs.io/en/stable/query_attribute.html)
        sort_by:
            Sort on one or multiple attributes.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded groundwater monster and filter data for a given bounding box.
        """

        gwmonster = GrondwaterMonsterSearch()
        if query is not None:
            query = And([PropertyIsEqualTo(propertyname='chemisch_PFAS', literal='true'), query])
        else:
            query = PropertyIsEqualTo(propertyname='chemisch_PFAS', literal='true')
        df = gwmonster.search(location=location, query=query, sort_by=sort_by, max_features=max_features)
        df = df[df.parametergroep == "Grondwater_chemisch_PFAS"]
        df = pd.DataFrame(df)
        data = df

        try:
            gwfilter = GrondwaterFilterSearch()
            filter_elements = gwfilter.search(query=Join(data, "pkey_filter"), return_fields=[
                "pkey_filter",
                "aquifer_code",
                "diepte_onderkant_filter",
                "lengte_filter"])

            data["datum_monstername"] = pd.to_datetime(
                data["datum_monstername"])
            data = pd.merge(data, filter_elements)
        except ValueError as e:
            logger.info(f"Empty dataframe: {e}")
        return data

    def biota(self, location, max_features, query=None, sort_by=None):
        """
        Download the biota data.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)
        query:
            Find data based on one or more of its attribute values.
            (https://pydov.readthedocs.io/en/stable/query_attribute.html)
        sort_by:
            Sort on one or multiple attributes.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded biota data.
        """
        logger.info(f"Downloading biota data")
        data_wfs_VMM_biota = self.wfs_request(
            'pfas:pfas_biota',
            location, max_features, query, sort_by)

        data_wfs_VMM_biota = data_wfs_VMM_biota.drop_duplicates(
            subset=data_wfs_VMM_biota.columns)

        data_wfs_VMM_biota_len = len(data_wfs_VMM_biota)

        nb_datapoints = {"Biota_VMM" : data_wfs_VMM_biota_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_VMM_biota

    def effluent(self, location, max_features, query=None, sort_by=None):
        """
        Download the effluent data.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)
        query:
            Find data based on one or more of its attribute values.
            (https://pydov.readthedocs.io/en/stable/query_attribute.html)
        sort_by:
            Sort on one or multiple attributes.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded effluent data.
        """
        logger.info(f"Downloading effluent data")

        if query is not None:
            query = And([query, PropertyIsEqualTo(propertyname='medium', literal='Effluent')])
        else:
            query = PropertyIsEqualTo(propertyname='medium', literal='Effluent')

        data_wfs_OVAM = self.wfs_request(
            layer='pfas:pfas_analyseresultaten',
            location=location,
            max_features=max_features,
            query=query,
            sort_by=sort_by)

        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)

        data_wfs_OVAM_len = len(data_wfs_OVAM)

        nb_datapoints = {"Effluent_OVAM" : data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_OVAM

    def groundwater(self, location, max_features):
        """
        Download the groundwater data.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded groundwater data.
        """
        logger.info(f"Downloading groundwater data")

        data_pydov_VMM_gw = self.pydov_request(
            location=location,
            max_features=max_features)
        data_wfs_OVAM = self.wfs_request(
            layer='pfas:pfas_analyseresultaten',
            location=location,
            max_features=max_features,
            query=PropertyIsEqualTo(propertyname='medium', literal='Grondwater'))
        data_wfs_Lantis_gw = self.wfs_request(
            layer='pfas:lantis_gw_metingen_publiek',
            location=location,
            max_features=max_features)

        data_pydov_VMM_gw = data_pydov_VMM_gw.drop_duplicates(
            subset=data_pydov_VMM_gw.columns)
        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)
        data_wfs_Lantis_gw = data_wfs_Lantis_gw.drop_duplicates(
            subset=data_wfs_Lantis_gw.columns)

        combined_groundwater = {'Groundwater': [data_pydov_VMM_gw, data_wfs_OVAM, data_wfs_Lantis_gw]}
        self.combined_datasets.update(combined_groundwater)

        data_pydov_VMM_gw_len = len(data_pydov_VMM_gw)
        data_wfs_OVAM_len = len(data_wfs_OVAM)
        data_wfs_Lantis_gw_len = len(data_wfs_Lantis_gw)

        nb_datapoints = {"Groundwater_VMM" : data_pydov_VMM_gw_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)
        nb_datapoints = {"Groundwater_OVAM" : data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)
        nb_datapoints = {"Groundwater_Lantis" : data_wfs_Lantis_gw_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_pydov_VMM_gw, data_wfs_OVAM, data_wfs_Lantis_gw

    def migration(self, location, max_features, query=None, sort_by=None):
        """
        Download the migration data.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)
        query:
            Find data based on one or more of its attribute values.
            (https://pydov.readthedocs.io/en/stable/query_attribute.html)
        sort_by:
            Sort on one or multiple attributes.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded migration data.
        """
        logger.info(f"Downloading migration data")

        if query is not None:
            query = And([query, PropertyIsEqualTo(propertyname='medium', literal='Migratie')])
        else:
            query = PropertyIsEqualTo(propertyname='medium', literal='Migratie')

        data_wfs_OVAM = self.wfs_request(
            layer='pfas:pfas_analyseresultaten',
            location=location,
            max_features=max_features,
            query=query,
            sort_by=sort_by)

        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)

        data_wfs_OVAM_len = len(data_wfs_OVAM)

        nb_datapoints = {"Migration_OVAM" : data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_OVAM

    def pure_product(self, location, max_features, query=None, sort_by=None):
        """
        Download the pure product data.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)
        query:
            Find data based on one or more of its attribute values.
            (https://pydov.readthedocs.io/en/stable/query_attribute.html)
        sort_by:
            Sort on one or multiple attributes.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded pure product data.
        """
        logger.info(f"Downloading pure product data")

        if query is not None:
            query = And([query, PropertyIsEqualTo(propertyname='medium', literal='Puur product')])
        else:
            query = PropertyIsEqualTo(propertyname='medium', literal='Puur product')

        data_wfs_OVAM = self.wfs_request(
            layer='pfas:pfas_analyseresultaten',
            location=location,
            max_features=max_features,
            query=query,
            sort_by=sort_by)

        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)

        data_wfs_OVAM_len = len(data_wfs_OVAM)

        nb_datapoints = {"Pure_product_OVAM" : data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_OVAM

    def rainwater(self, location, max_features, query=None, sort_by=None):
        """
        Download the rainwater data.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)
        query:
            Find data based on one or more of its attribute values.
            (https://pydov.readthedocs.io/en/stable/query_attribute.html)
        sort_by:
            Sort on one or multiple attributes.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded rainwater data.
        """
        logger.info(f"Downloading rainwater data")

        if query is not None:
            query = And([query, PropertyIsEqualTo(propertyname='medium', literal='Regenwater')])
        else:
            query = PropertyIsEqualTo(propertyname='medium', literal='Regenwater')

        data_wfs_OVAM = self.wfs_request(
            layer='pfas:pfas_analyseresultaten',
            location=location,
            max_features=max_features,
            query=query,
            sort_by=sort_by)

        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)

        data_wfs_OVAM_len = len(data_wfs_OVAM)

        nb_datapoints = {"Rainwater_OVAM" : data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_OVAM

    def soil(self, location, max_features):
        """
        Download the soil data.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded soil data.
        """
        logger.info(f"Downloading soil data")
        data_wfs_OVAM = self.wfs_request(
            layer='pfas:pfas_analyseresultaten',
            location=location,
            max_features=max_features,
            query=PropertyIsEqualTo('medium', 'Vaste deel van de aarde'))
        data_wfs_Lantis_soil = self.wfs_request(
            layer='pfas:lantis_bodem_metingen',
            location=location,
            max_features=max_features)

        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)
        data_wfs_Lantis_soil = data_wfs_Lantis_soil.drop_duplicates(
            subset=data_wfs_Lantis_soil.columns)

        combined_soil = {'Soil': [data_wfs_OVAM, data_wfs_Lantis_soil]}
        self.combined_datasets.update(combined_soil)

        data_wfs_OVAM_len = len(data_wfs_OVAM)
        data_wfs_Lantis_soil_len = len(data_wfs_Lantis_soil)

        nb_datapoints = {"Soil_OVAM" : data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)
        nb_datapoints = {"Soil_Lantis" : data_wfs_Lantis_soil_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_OVAM, data_wfs_Lantis_soil

    def soil_water(self, location, max_features):
        """
        Download the soil water data.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)
        query:
            Find data based on one or more of its attribute values.
            (https://pydov.readthedocs.io/en/stable/query_attribute.html)
        sort_by:
            Sort on one or multiple attributes.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded soil water data.
        """
        logger.info(f"Downloading soilwater data")
        data_wfs_VMM_ws = self.wfs_request(
            layer='waterbodems:pfas_meetpunten_fcs',
            location=location,
            max_features=max_features)
        data_wfs_OVAM = self.wfs_request(
            layer='pfas:pfas_analyseresultaten',
            location=location,
            max_features=max_features,
            query=Or([
                PropertyIsEqualTo('medium', 'Waterbodem - sediment'),
                PropertyIsEqualTo('medium', 'Waterbodem - vaste deel van waterbodem')]))

        data_wfs_VMM_ws = data_wfs_VMM_ws.drop_duplicates(
            subset=data_wfs_VMM_ws.columns)
        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)
        data_wfs_OVAM_sediment = data_wfs_OVAM[data_wfs_OVAM['medium'] == 'Waterbodem - sediment']
        data_wfs_OVAM_fixed = data_wfs_OVAM[data_wfs_OVAM['medium'] == 'Waterbodem - vaste deel van waterbodem']

        combined_soil_water = {'Soil_water': [data_wfs_VMM_ws, data_wfs_OVAM_sediment, data_wfs_OVAM_fixed]}
        self.combined_datasets.update(combined_soil_water)

        data_wfs_VMM_ws_len = len(data_wfs_VMM_ws)
        data_wfs_OVAM_sediment_len = len(data_wfs_OVAM_sediment)
        data_wfs_OVAM_fixed_len = len(data_wfs_OVAM_fixed)

        nb_datapoints = {"Soil_water_VMM" : data_wfs_VMM_ws_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)
        nb_datapoints = {"Soil_water_sediment_OVAM" : data_wfs_OVAM_sediment_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)
        nb_datapoints = {"Soil_water_fixed_OVAM": data_wfs_OVAM_fixed_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_VMM_ws, data_wfs_OVAM_sediment, data_wfs_OVAM_fixed

    def surface_water(self, location, max_features):
        """
        Download the surface water data.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)
        query:
            Find data based on one or more of its attribute values.
            (https://pydov.readthedocs.io/en/stable/query_attribute.html)
        sort_by:
            Sort on one or multiple attributes.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded surface water data.
        """
        logger.info(f"Downloading surface water data")
        data_wfs_VMM_sw = self.wfs_request(
            layer='pfas:pfas_oppwater',
            location=location,
            max_features=max_features)
        data_wfs_OVAM = self.wfs_request(
            layer='pfas:pfas_analyseresultaten',
            location=location,
            max_features=max_features,
            query=PropertyIsEqualTo('medium', 'Oppervlaktewater'))

        data_wfs_VMM_sw = data_wfs_VMM_sw.drop_duplicates(
            subset=data_wfs_VMM_sw.columns)
        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)

        combined_surface_water = {'Surface_water': [data_wfs_VMM_sw, data_wfs_OVAM]}
        self.combined_datasets.update(combined_surface_water)

        data_wfs_VMM_sw_len = len(data_wfs_VMM_sw)
        data_wfs_OVAM_len = len(data_wfs_OVAM)

        nb_datapoints = {"Surface_water_VMM" : data_wfs_VMM_sw_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)
        nb_datapoints = {"Surface_water_OVAM": data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_VMM_sw, data_wfs_OVAM

    def waste_water(self, location, max_features, query=None, sort_by=None):
        """
        Download the waste water data.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)
        query:
            Find data based on one or more of its attribute values.
            (https://pydov.readthedocs.io/en/stable/query_attribute.html)
        sort_by:
            Sort on one or multiple attributes.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded waste water data.
        """
        logger.info(f"Downloading waste water data")
        data_wfs_VMM_ww = self.wfs_request(
            layer='pfas:pfas_afvalwater',
            location=location,
            max_features=max_features,
            query=query,
            sort_by=sort_by)

        data_wfs_VMM_ww = data_wfs_VMM_ww.drop_duplicates(
            subset=data_wfs_VMM_ww.columns)

        data_wfs_VMM_ww_len = len(data_wfs_VMM_ww)

        nb_datapoints = {"Waste_water_VMM": data_wfs_VMM_ww_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_VMM_ww

    def air(self, location, max_features):
        """
        Download the air data.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded air data.
        """
        logger.info(f"Downloading air data")

        data_wfs_zwevend_stof_VMM = self.wfs_request(
            layer='pfas:lucht_zwevendstof_metingen',
            location=location,
            max_features=max_features)
        data_wfs_gas_VMM = self.wfs_request(
            layer='pfas:lucht_gas_metingen',
            location=location,
            max_features=max_features)
        data_wfs_depositie_VMM = self.wfs_request(
            layer='pfas:lucht_depositie_metingen',
            location=location,
            max_features=max_features)

        data_wfs_zwevend_stof_VMM = data_wfs_zwevend_stof_VMM.drop_duplicates(
            subset=data_wfs_zwevend_stof_VMM.columns)
        data_wfs_gas_VMM = data_wfs_gas_VMM.drop_duplicates(
            subset=data_wfs_gas_VMM.columns)
        data_wfs_depositie_VMM = data_wfs_depositie_VMM.drop_duplicates(
            subset=data_wfs_depositie_VMM.columns)

        data_wfs_zwevend_stof_VMM_len = len(data_wfs_zwevend_stof_VMM)
        data_wfs_gas_VMM_len = len(data_wfs_gas_VMM)
        data_wfs_depositie_VMM_len = len(data_wfs_depositie_VMM)

        nb_datapoints = {"Air_dust_VMM" : data_wfs_zwevend_stof_VMM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)
        nb_datapoints = {"Air_gas_VMM" : data_wfs_gas_VMM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)
        nb_datapoints = {"Air_deposition_VMM" : data_wfs_depositie_VMM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_zwevend_stof_VMM, data_wfs_gas_VMM, data_wfs_depositie_VMM

    def combined_groundwater(self, location, max_features):
        """
        Download the groundwater data and combine it in one dataframe.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded and combined groundwater data.
        """
        if 'Groundwater' in self.combined_datasets:
            gw_datasets = self.combined_datasets['Groundwater']
            gw_VMM = gw_datasets[0]
            gw_OVAM = gw_datasets[1]
            gw_Lantis = gw_datasets[2]
        else:
            gw_VMM, gw_OVAM, gw_Lantis = RequestPFASdata().groundwater(location, max_features)

        gw_VMM['top_m_mv'] = gw_VMM['diepte_onderkant_filter']-gw_VMM['lengte_filter']

        gw_VMM = gw_VMM.rename(columns={'grondwatermonsternummer': 'id', 'datum_monstername': 'datum', 'x': 'x_m_L72', 'y': 'y_m_L72', 'detectie': 'detectieconditie', 'waarde': 'meetwaarde', 'eenheid': 'meeteenheid', 'diepte_onderkant_filter': 'basis_m_mv'})
        gw_OVAM = gw_OVAM.rename(columns={'top_in_m': 'top_m_mv', 'basis_in_m': 'basis_m_mv', 'x_ml72': 'x_m_L72', 'y_ml72': 'y_m_L72'})
        gw_Lantis = gw_Lantis.rename(columns={'filter_van_m': 'top_m_mv', 'filter_tot_m': 'basis_m_mv', 'analysemonster': 'id', 'datum_bemonstering': 'datum', 'waarde': 'meetwaarde', 'eenheid': 'meeteenheid', 'x_ml72': 'x_m_L72', 'y_ml72': 'y_m_L72'})

        gw_VMM['bron'] = 'VMM'
        gw_OVAM['bron'] = 'OVAM'
        gw_Lantis['bron'] = 'Lantis'

        gw_VMM = gw_VMM[['id', 'datum', 'x_m_L72', 'y_m_L72', 'top_m_mv', 'basis_m_mv', 'parameter', 'detectieconditie', 'meetwaarde', 'meeteenheid', 'bron']]
        gw_OVAM = gw_OVAM[['id', 'datum', 'x_m_L72', 'y_m_L72', 'top_m_mv', 'basis_m_mv', 'parameter', 'detectieconditie', 'meetwaarde', 'meeteenheid', 'bron']]
        gw_Lantis = gw_Lantis[['id', 'datum', 'x_m_L72', 'y_m_L72', 'top_m_mv', 'basis_m_mv', 'parameter', 'detectieconditie', 'meetwaarde', 'meeteenheid', 'bron']]

        groundwater = pd.concat([gw_VMM, gw_OVAM, gw_Lantis])

        data_groundwater_len = len(groundwater)
        nb_datapoints = {"Combined_groundwater": data_groundwater_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return groundwater

    def combined_soil(self, location, max_features):
        """
        Download the soil data and combine it in one dataframe.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded and combined soil data.
        """
        if 'Soil' in self.combined_datasets:
            soil_datasets = self.combined_datasets['Soil']
            soil_OVAM = soil_datasets[0]
            soil_Lantis = soil_datasets[1]
        else:
            soil_OVAM, soil_Lantis = RequestPFASdata().soil(location, max_features)

        soil_OVAM = soil_OVAM.rename(columns={'id': 'id_original','top_in_m': 'top_m_mv', 'basis_in_m': 'basis_m_mv', 'x_ml72': 'x_m_L72', 'y_ml72': 'y_m_L72'})
        soil_Lantis = soil_Lantis.rename(columns={'diepte_van_m': 'top_m_mv', 'diepte_tot_m': 'basis_m_mv', 'datum_bemonstering': 'datum', 'waarde': 'meetwaarde', 'eenheid': 'meeteenheid', 'x_ml72': 'x_m_L72', 'y_ml72': 'y_m_L72'})

        soil_OVAM['bron'] = 'OVAM'
        soil_Lantis['bron'] = 'Lantis'
        id_OVAM_list = []
        for i in range(len(soil_OVAM)):
            id_OVAM = f"{int(soil_OVAM['opdracht'][i])}/{int(soil_OVAM['pfasdossiernr'][i])}/{soil_OVAM['profielnaam'][i]}"
            id_OVAM_list.append(id_OVAM)
        soil_OVAM['id'] = id_OVAM_list
        id_lantis_list = []
        for i in range(len(soil_Lantis)):
            id_lantis = f"{soil_Lantis['boring'][i]}/{int(soil_Lantis['nummer'][i])}/{soil_Lantis['analysemonster'][i]}"
            id_lantis_list.append(id_lantis)
        soil_Lantis['id'] = id_lantis_list

        soil_OVAM = soil_OVAM[['id', 'datum', 'x_m_L72', 'y_m_L72', 'top_m_mv', 'basis_m_mv', 'parameter', 'detectieconditie', 'meetwaarde', 'meeteenheid', 'bron']]
        soil_Lantis = soil_Lantis[['id', 'datum', 'x_m_L72', 'y_m_L72', 'top_m_mv', 'basis_m_mv', 'parameter', 'detectieconditie', 'meetwaarde', 'meeteenheid', 'bron']]

        soil = pd.concat([soil_OVAM, soil_Lantis])
        soil = soil.replace(['som PFOA', 'som PFOS'],['PFOAtotaal', 'PFOStotaal'])

        data_soil_len = len(soil)
        nb_datapoints = {"Combined_soil": data_soil_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return soil

    def combined_soil_water(self, location, max_features):
        """
        Download the soilwater data and combine it in one dataframe.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded and combined soilwater data.
        """
        if 'Soil_water' in self.combined_datasets:
            soilwater_datasets = self.combined_datasets['Soil_water']
            soilwater_VMM = soilwater_datasets[0]
            soilwater_OVAM_sediment = soilwater_datasets[1]
            soilwater_OVAM_fixed = soilwater_datasets[2]
        else:
            soilwater_VMM, soilwater_OVAM_sediment, soilwater_OVAM_fixed = RequestPFASdata().soil_water(location, max_features)

        soilwater_VMM = soilwater_VMM.rename(columns={'VHA_code': 'id', 'X': 'x_m_L72', 'Y': 'y_m_L72'})
        soilwater_OVAM_sediment = soilwater_OVAM_sediment.rename(columns={'x_ml72': 'x_m_L72', 'y_ml72': 'y_m_L72'})
        soilwater_OVAM_fixed = soilwater_OVAM_fixed.rename(columns={'x_ml72': 'x_m_L72', 'y_ml72': 'y_m_L72'})

        soilwater_VMM['bron'] = 'VMM'
        soilwater_OVAM_sediment['bron'] = 'OVAM_sediment'
        soilwater_OVAM_fixed['bron'] = 'OVAM_fixed'

        soilwater_VMM = soilwater_VMM[['id', 'datum', 'x_m_L72', 'y_m_L72', 'parameter', 'detectieconditie', 'meetwaarde', 'meeteenheid', 'bron']]
        soilwater_OVAM_sediment = soilwater_OVAM_sediment[['id', 'datum', 'x_m_L72', 'y_m_L72', 'parameter', 'detectieconditie', 'meetwaarde', 'meeteenheid', 'bron']]
        soilwater_OVAM_fixed = soilwater_OVAM_fixed[['id', 'datum', 'x_m_L72', 'y_m_L72', 'parameter', 'detectieconditie', 'meetwaarde', 'meeteenheid', 'bron']]

        soilwater = pd.concat([soilwater_VMM, soilwater_OVAM_sediment, soilwater_OVAM_fixed])

        data_soilwater_len = len(soilwater)
        nb_datapoints = {"Combined_soil_water": data_soilwater_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return soilwater

    def combined_surface_water(self, location, max_features):
        """
        Download the surface water data and combine it in one dataframe.

        Parameters
        ----------
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)

        Returns
        -------
        The downloaded and combined surface water data.
        """
        if 'Surface_water' in self.combined_datasets:
            surfacewater_datasets = self.combined_datasets['Surface_water']
            surfacewater_VMM = surfacewater_datasets[0]
            surfacewater_OVAM = surfacewater_datasets[1]
        else:
            surfacewater_VMM, surfacewater_OVAM = RequestPFASdata().surface_water(location, max_features)

        surfacewater_VMM = surfacewater_VMM.rename(columns={'ogc_fid': 'id', 'x_mL72': 'x_m_L72', 'y_mL72': 'y_m_L72'})
        surfacewater_OVAM = surfacewater_OVAM.rename(columns={'x_ml72': 'x_m_L72', 'y_ml72': 'y_m_L72'})

        surfacewater_VMM['bron'] = 'VMM'
        surfacewater_OVAM['bron'] = 'OVAM'

        surfacewater_VMM = surfacewater_VMM[['id', 'datum', 'x_m_L72', 'y_m_L72', 'parameter', 'detectieconditie', 'meetwaarde', 'meeteenheid', 'bron']]
        surfacewater_OVAM = surfacewater_OVAM[['id', 'datum', 'x_m_L72', 'y_m_L72', 'parameter', 'detectieconditie', 'meetwaarde', 'meeteenheid', 'bron']]

        surfacewater = pd.concat([surfacewater_VMM, surfacewater_OVAM])

        data_surfacewater_len = len(surfacewater)
        nb_datapoints = {"Combined_surface_water": data_surfacewater_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return surfacewater

    def main(self, medium, location=None, max_features=None, save=False):

        """
        Call the functions to download the requested data and save the result in an Excel-file, with the different mediums as seperate tabs.

        Parameters
        ----------
        medium: list of str
            The requested medium(s).

            Possibilities:
                    - 'all'
                    - 'biota'
                    - 'effluent'
                    - 'groundwater'
                    - 'migration'
                    - 'pure product'
                    - 'rainwater'
                    - 'soil'
                    - 'soil water'
                    - 'surface water'
                    - 'waste water'
                    - 'air'
                    - 'combined_groundwater'
                    - 'combined_soil'
                    - 'combined_soil_water'
                    - 'combined_surface_water'
        location:
            Query on location.
            (https://pydov.readthedocs.io/en/stable/query_location.html)
        max_features: int
            Limit the number of WFS features you want to be returned.
            (https://pydov.readthedocs.io/en/stable/sort_limit.html)
        save: boolean
            Option to save the downloaded data if True.

        Returns
        -------
        The requested data in separate dataframe(s) and the metadata.
        """
        start_time = datetime.now()

        return_list = []

        for i in medium:
            if i == 'all':
                data_wfs_VMM_biota = self.biota(location, max_features)
                data_wfs_OVAM_effluent = self.effluent(location, max_features)
                data_pydov_VMM_gw, data_wfs_OVAM_gw, data_wfs_Lantis_gw = self.groundwater(location, max_features)
                data_wfs_OVAM_migration = self.migration(location, max_features)
                data_wfs_OVAM_pp = self.pure_product(location, max_features)
                data_wfs_OVAM_rainwater = self.rainwater(location, max_features)
                data_wfs_OVAM_soil, data_wfs_Lantis_soil = self.soil(location, max_features)
                data_wfs_VMM_ws, data_wfs_OVAM_ws_sediment, data_wfs_OVAM_ws_fixed = self.soil_water(location, max_features)
                data_wfs_VMM_sw, data_wfs_OVAM_sw = self.surface_water(location, max_features)
                data_wfs_VMM_ww = self.waste_water(location, max_features)
                data_wfs_zwevend_stof_VMM, data_wfs_gas_VMM, data_wfs_depositie_VMM = self.air(location, max_features)
                data_groundwater = self.combined_groundwater(location, max_features)
                data_soil = self.combined_soil(location, max_features)
                data_soil_water = self.combined_soil_water(location, max_features)
                data_surface_water = self.combined_surface_water(location, max_features)
                return_list.extend([data_wfs_VMM_biota, data_wfs_OVAM_effluent, data_pydov_VMM_gw, data_wfs_OVAM_gw,
                        data_wfs_Lantis_gw, data_wfs_OVAM_migration, data_wfs_OVAM_pp, data_wfs_OVAM_rainwater,
                        data_wfs_OVAM_soil, data_wfs_Lantis_soil, data_wfs_VMM_ws, data_wfs_OVAM_ws_sediment, data_wfs_OVAM_ws_fixed, data_wfs_VMM_sw,
                        data_wfs_OVAM_sw, data_wfs_VMM_ww, data_wfs_zwevend_stof_VMM, data_wfs_gas_VMM, data_wfs_depositie_VMM, data_groundwater, data_soil, data_soil_water, data_surface_water])
            elif i == 'biota':
                data_wfs_VMM_biota = self.biota(location, max_features)
                return_list.extend([data_wfs_VMM_biota])
            elif i == 'effluent':
                data_wfs_OVAM_effluent = self.effluent(location,max_features)
                return_list.extend([data_wfs_OVAM_effluent])
            elif i == 'groundwater':
                data_pydov_VMM_gw, data_wfs_OVAM_gw, data_wfs_Lantis_gw = self.groundwater(location, max_features)
                return_list.extend([data_pydov_VMM_gw, data_wfs_OVAM_gw, data_wfs_Lantis_gw])
            elif i == 'migration':
                data_wfs_OVAM_migration = self.migration(location, max_features)
                return_list.extend([data_wfs_OVAM_migration])
            elif i == 'pure product':
                data_wfs_OVAM_pp = self.pure_product(location, max_features)
                return_list.extend([data_wfs_OVAM_pp])
            elif i == 'rainwater':
                data_wfs_OVAM_rainwater = self.rainwater(location, max_features)
                return_list.extend([data_wfs_OVAM_rainwater])
            elif i == 'soil':
                data_wfs_OVAM_soil, data_wfs_Lantis_soil = self.soil(location, max_features)
                return_list.extend([data_wfs_OVAM_soil, data_wfs_Lantis_soil])
            elif i == 'soil water':
                data_wfs_VMM_ws, data_wfs_OVAM_ws_sediment, data_wfs_OVAM_ws_fixed = self.soil_water(location, max_features)
                return_list.extend([data_wfs_VMM_ws, data_wfs_OVAM_ws_sediment, data_wfs_OVAM_ws_fixed])
            elif i == 'surface water':
                data_wfs_VMM_sw, data_wfs_OVAM_sw = self.surface_water(location, max_features)
                return_list.extend([data_wfs_VMM_sw, data_wfs_OVAM_sw])
            elif i == 'waste water':
                data_wfs_VMM_ww = self.waste_water(location, max_features)
                return_list.extend([data_wfs_VMM_ww])
            elif i == 'air':
                data_wfs_zwevend_stof_VMM, data_wfs_gas_VMM, data_wfs_depositie_VMM = self.air(location, max_features)
                return_list.extend([data_wfs_zwevend_stof_VMM, data_wfs_gas_VMM, data_wfs_depositie_VMM])
            elif i == 'combined_groundwater':
                data_groundwater = self.combined_groundwater(location, max_features)
                return_list.extend([data_groundwater])
            elif i == 'combined_soil':
                data_soil = self.combined_soil(location, max_features)
                return_list.extend([data_soil])
            elif i == 'combined_soil_water':
                data_soil_water = self.combined_soil_water(location, max_features)
                return_list.extend([data_soil_water])
            elif i == 'combined_surface_water':
                data_surface_water = self.combined_surface_water(location, max_features)
                return_list.extend([data_surface_water])

        metadata = json.dumps(self.dictionary, indent=3)

        if save:
            path = os.getcwd()
            path1 = f"{path}/results"
            if not os.path.exists(path1):
                os.mkdir(f"{path}/results")
            path2 = f"{path}/results/metadata.json"
            with open(path2, "w") as outfile:
                outfile.write(metadata)

            with open(f"{path}/results/metadata.json") as metadata_file:
                metadata = json.load(metadata_file)

            pbar = tqdm(total=sum(metadata['nb_datapoints'][0].values()))
            with pd.ExcelWriter(f'{path}/results/data.xlsx') as writer:
                for i in medium:
                    if i == 'all':
                        data_wfs_VMM_biota.to_excel(writer, sheet_name='Biota_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Biota_VMM'])
                        data_wfs_OVAM_effluent.to_excel(writer, sheet_name='Effluent_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Effluent_OVAM'])
                        data_pydov_VMM_gw.to_excel(writer, sheet_name='Groundwater_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Groundwater_VMM'])
                        data_wfs_OVAM_gw.to_excel(writer, sheet_name='Groundwater_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Groundwater_OVAM'])
                        data_wfs_Lantis_gw.to_excel(writer, sheet_name='Groundwater_Lantis')
                        pbar.update(metadata['nb_datapoints'][0]['Groundwater_Lantis'])
                        data_wfs_OVAM_migration.to_excel(writer, sheet_name='Migration_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Migration_OVAM'])
                        data_wfs_OVAM_pp.to_excel(writer, sheet_name='Pure_product_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Pure_product_OVAM'])
                        data_wfs_OVAM_rainwater.to_excel(writer, sheet_name='Rainwater_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Rainwater_OVAM'])
                        data_wfs_OVAM_soil.to_excel(writer, sheet_name='Soil_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Soil_OVAM'])
                        data_wfs_Lantis_soil.to_excel(writer, sheet_name='Soil_Lantis')
                        pbar.update(metadata['nb_datapoints'][0]['Soil_Lantis'])
                        data_wfs_VMM_ws.to_excel(writer, sheet_name='Soil_water_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Soil_water_VMM'])
                        data_wfs_OVAM_ws_sediment.to_excel(writer, sheet_name='Soil_water_sediment_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Soil_water_sediment_OVAM'])
                        data_wfs_OVAM_ws_fixed.to_excel(writer, sheet_name='Soil_water_fixed_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Soil_water_fixed_OVAM'])
                        data_wfs_VMM_sw.to_excel(writer, sheet_name='Surface_water_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Surface_water_VMM'])
                        data_wfs_OVAM_sw.to_excel(writer, sheet_name='Surface_water_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Surface_water_OVAM'])
                        data_wfs_VMM_ww.to_excel(writer, sheet_name='Waste_water_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Waste_water_VMM'])
                        data_wfs_zwevend_stof_VMM.to_excel(writer, sheet_name='Air_dust_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Air_dust_VMM'])
                        data_wfs_gas_VMM.to_excel(writer, sheet_name='Air_gas_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Air_gas_VMM'])
                        data_wfs_depositie_VMM.to_excel(writer, sheet_name='Air_deposition_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Air_deposition_VMM'])
                        data_groundwater.to_excel(writer, sheet_name='Combined_groundwater')
                        pbar.update(metadata['nb_datapoints'][0]['Combined_groundwater'])
                        data_soil.to_excel(writer, sheet_name='Combined_soil')
                        pbar.update(metadata['nb_datapoints'][0]['Combined_soil'])
                        data_soil_water.to_excel(writer, sheet_name='Combined_soil_water')
                        pbar.update(metadata['nb_datapoints'][0]['Combined_soil_water'])
                        data_surface_water.to_excel(writer, sheet_name='Combined_surface_water')
                        pbar.update(metadata['nb_datapoints'][0]['Combined_surface_water'])
                    elif i == 'biota':
                        data_wfs_VMM_biota.to_excel(writer, sheet_name='Biota_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Biota_VMM'])
                    elif i == 'effluent':
                        data_wfs_OVAM_effluent.to_excel(writer, sheet_name='Effluent_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Effluent_OVAM'])
                    elif i == 'groundwater':
                        data_pydov_VMM_gw.to_excel(writer, sheet_name='Groundwater_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Groundwater_VMM'])
                        data_wfs_OVAM_gw.to_excel(writer, sheet_name='Groundwater_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Groundwater_OVAM'])
                        data_wfs_Lantis_gw.to_excel(writer, sheet_name='Groundwater_Lantis')
                        pbar.update(metadata['nb_datapoints'][0]['Groundwater_Lantis'])
                    elif i == 'migration':
                        data_wfs_OVAM_migration.to_excel(writer, sheet_name='Migration_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Migration_OVAM'])
                    elif i == 'pure product':
                        data_wfs_OVAM_pp.to_excel(writer, sheet_name='Pure_product_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Pure_product_OVAM'])
                    elif i == 'rainwater':
                        data_wfs_OVAM_rainwater.to_excel(writer, sheet_name='Rainwater_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Rainwater_OVAM'])
                    elif i == 'soil':
                        data_wfs_OVAM_soil.to_excel(writer, sheet_name='Soil_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Soil_OVAM'])
                        data_wfs_Lantis_soil.to_excel(writer, sheet_name='Soil_Lantis')
                        pbar.update(metadata['nb_datapoints'][0]['Soil_Lantis'])
                    elif i == 'soil water':
                        data_wfs_VMM_ws.to_excel(writer, sheet_name='Soil_water_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Soil_water_VMM'])
                        data_wfs_OVAM_ws_sediment.to_excel(writer, sheet_name='Soil_water_sediment_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Soil_water_sediment_OVAM'])
                        data_wfs_OVAM_ws_fixed.to_excel(writer, sheet_name='Soil_water_fixed_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Soil_water_fixed_OVAM'])
                    elif i == 'surface water':
                        data_wfs_VMM_sw.to_excel(writer, sheet_name='Surface_water_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Surface_water_VMM'])
                        data_wfs_OVAM_sw.to_excel(writer, sheet_name='Surface_water_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Surface_water_OVAM'])
                    elif i == 'waste water':
                        data_wfs_VMM_ww.to_excel(writer, sheet_name='Waste_water_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Waste_water_VMM'])
                    elif i == 'air':
                        data_wfs_zwevend_stof_VMM.to_excel(writer, sheet_name='Air_dust_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Air_dust_VMM'])
                        data_wfs_gas_VMM.to_excel(writer, sheet_name='Air_gas_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Air_gas_VMM'])
                        data_wfs_depositie_VMM.to_excel(writer, sheet_name='Air_deposition_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Air_deposition_VMM'])
                    elif i == 'combined_groundwater':
                        data_groundwater.to_excel(writer, sheet_name='Combined_groundwater')
                        pbar.update(metadata['nb_datapoints'][0]['Combined_groundwater'])
                    elif i == 'combined_soil':
                        data_soil.to_excel(writer, sheet_name='Combined_soil')
                        pbar.update(metadata['nb_datapoints'][0]['Combined_soil'])
                    elif i == 'combined_soil_water':
                        data_soil_water.to_excel(writer, sheet_name='Combined_soil_water')
                        pbar.update(metadata['nb_datapoints'][0]['Combined_soil_water'])
                    elif i == 'combined_surface_water':
                        data_surface_water.to_excel(writer, sheet_name='Combined_surface_water')
                        pbar.update(metadata['nb_datapoints'][0]['Combined_surface_water'])
            pbar.close()


        end_time = datetime.now()
        duration = end_time-start_time
        logger.info(f'The program was executed in {duration}.')

        return return_list, metadata


if __name__ == '__main__':
    medium = ['combined_soil']
    location = Within(Box(15000, 150000, 270000, 250000, epsg=31370))  # Bounding box Flanders
    rd = RequestPFASdata()
    df = rd.main(medium, location=location, save=True)[0]
    #print(df[0])

