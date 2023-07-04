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

        Create a metadata file that contains the date and necessary package versions.
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
                return_list.extend([data_wfs_VMM_biota, data_wfs_OVAM_effluent, data_pydov_VMM_gw, data_wfs_OVAM_gw,
                        data_wfs_Lantis_gw, data_wfs_OVAM_migration, data_wfs_OVAM_pp, data_wfs_OVAM_rainwater,
                        data_wfs_OVAM_soil, data_wfs_Lantis_soil, data_wfs_VMM_ws, data_wfs_OVAM_ws_sediment, data_wfs_OVAM_ws_fixed, data_wfs_VMM_sw,
                        data_wfs_OVAM_sw, data_wfs_VMM_ww])
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
            pbar.close()


        end_time = datetime.now()
        duration = end_time-start_time
        logger.info(f'The program was executed in {duration}.')

        return return_list, metadata


if __name__ == '__main__':
    medium = ['all']
    location = Within(Box(15000, 150000, 270000, 250000))  # Bounding box Flanders
    rd = RequestPFASdata()
    df = rd.main(medium, location=location, save=True)[0]
    #print(df[0])

