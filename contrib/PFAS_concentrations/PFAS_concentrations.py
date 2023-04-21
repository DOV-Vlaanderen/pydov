import os
import pandas as pd
from pydov.search.generic import WfsSearch
from pydov.search.grondwatermonster import GrondwaterMonsterSearch
from pydov.search.grondwaterfilter import GrondwaterFilterSearch
from pydov.util.location import Within, Box
from pydov.util.query import Join
from loguru import logger
from owslib.fes2 import PropertyIsEqualTo
from tqdm.auto import tqdm
from datetime import datetime
from importlib.metadata import version
import json

class RequestPFASdata:

    def __init__(self):
        """Initialize the class.

        Create a metadata file that contains the date and necessary package versions.
        """

        #todo: in which file type is metadata saved? JSON?

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

        self.lowerleftx = 15000
        self.lowerlefty = 150000
        self.upperrightx = 270000
        self.upperrighty = 250000

    def wfs_request(self, layer, bbox):
        """Download the available PFAS-data through a wfs request.

        Parameters
        ----------
        layer : str
            The name of the layer containing the PFAS-data.
        bbox : Box
            A box location, also known as a bounding box.

        Returns
        -------
        The downloaded PFAS-data.
        """

        wfsSearch = WfsSearch(layer)
        return wfsSearch.search(location=Within(bbox))

    def pydov_request(self, bbox):
        """Function to download the groundwater monster and according filter data for a specific bounding box.

        Parameters
        ----------
        bbox : Box
            A box location, also known as a bounding box.

        Returns
        -------
        The downloaded groundwater monster and filter data for a given bounding box.
        """

        gwmonster = GrondwaterMonsterSearch()
        query = PropertyIsEqualTo(propertyname='chemisch_PFAS', literal='true')
        df = gwmonster.search(location=Within(bbox), query=query)
        df = df[df.parametergroep == "Grondwater_chemisch_PFAS"]
        df = pd.DataFrame(df)  # Create a dataframe.
        data = df

        try:
            # Link a local variable to GrondwaterMonsterSearch()
            gwfilter = GrondwaterFilterSearch()
            filter_elements = gwfilter.search(query=Join(data, "pkey_filter"), return_fields=[
                "pkey_filter",
                "aquifer_code",
                "diepte_onderkant_filter",
                "lengte_filter"])
            # Change the type of date.
            data["datum_monstername"] = pd.to_datetime(
                data["datum_monstername"])
            data = pd.merge(data, filter_elements)  # Combine the dataframes.
        except ValueError as e:
            logger.info(f"Empty dataframe: {e}")
        return data

    def biota(self):
        """
        Download the biota data.
        """
        logger.info(f"Downloading biota data")
        data_wfs_VMM_biota = self.wfs_request(
            'pfas:pfas_biota',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))

        data_wfs_VMM_biota = data_wfs_VMM_biota.drop_duplicates(
            subset=data_wfs_VMM_biota.columns)

        data_wfs_VMM_biota_len = len(data_wfs_VMM_biota)

        nb_datapoints = {"Biota_VMM" : data_wfs_VMM_biota_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_VMM_biota

    def effluent(self):
        """
        Download the effluent data.
        """
        logger.info(f"Downloading effluent data")
        data_wfs_OVAM = self.wfs_request(
            'pfas:pfas_analyseresultaten',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))

        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)

        data_wfs_OVAM = data_wfs_OVAM[data_wfs_OVAM['medium'] == 'Effluent']
        data_wfs_OVAM_len = len(data_wfs_OVAM)

        nb_datapoints = {"Effluent_OVAM" : data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_OVAM

    def groundwater(self):
        """
        Download the groundwater data.
        """
        logger.info(f"Downloading groundwater data")
        data_pydov_VMM_gw = self.pydov_request(
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))
        data_wfs_OVAM = self.wfs_request(
            'pfas:pfas_analyseresultaten',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))
        data_wfs_Lantis_gw = self.wfs_request(
            'pfas:lantis_gw_metingen_publiek',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))

        data_pydov_VMM_gw = data_pydov_VMM_gw.drop_duplicates(
            subset=data_pydov_VMM_gw.columns)
        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)
        data_wfs_OVAM = data_wfs_OVAM[data_wfs_OVAM['medium'] == 'Grondwater']
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

    def migration(self):
        """
        Download the migration data.
        """
        logger.info(f"Downloading migration data")
        data_wfs_OVAM = self.wfs_request(
            'pfas:pfas_analyseresultaten',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))

        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)
        data_wfs_OVAM = data_wfs_OVAM[data_wfs_OVAM['medium'] == 'Migratie']

        data_wfs_OVAM_len = len(data_wfs_OVAM)

        nb_datapoints = {"Migration_OVAM" : data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_OVAM

    def pure_product(self):
        """
        Download the pure product data.
        """
        logger.info(f"Downloading pure product data")
        data_wfs_OVAM = self.wfs_request(
            'pfas:pfas_analyseresultaten',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))

        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)
        data_wfs_OVAM = data_wfs_OVAM[data_wfs_OVAM['medium'] == 'Puur product']

        data_wfs_OVAM_len = len(data_wfs_OVAM)

        nb_datapoints = {"Pure_product_OVAM" : data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_OVAM

    def rainwater(self):
        """
        Download the rainwater data.
        """
        logger.info(f"Downloading rainwater data")
        data_wfs_OVAM = self.wfs_request(
            'pfas:pfas_analyseresultaten',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))

        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)
        data_wfs_OVAM = data_wfs_OVAM[data_wfs_OVAM['medium'] == 'Regenwater']

        data_wfs_OVAM_len = len(data_wfs_OVAM)

        nb_datapoints = {"Rainwater_OVAM" : data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_OVAM

    def soil(self):
        """
        Download the soil data.
        """
        logger.info(f"Downloading soil data")
        data_wfs_OVAM = self.wfs_request(
            'pfas:pfas_analyseresultaten',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))
        data_wfs_Lantis_soil = self.wfs_request(
            'pfas:lantis_bodem_metingen',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))

        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)
        data_wfs_OVAM = data_wfs_OVAM[data_wfs_OVAM['medium'] == 'Vaste deel van de aarde']
        data_wfs_Lantis_soil = data_wfs_Lantis_soil.drop_duplicates(
            subset=data_wfs_Lantis_soil.columns)

        data_wfs_OVAM_len = len(data_wfs_OVAM)
        data_wfs_Lantis_soil_len = len(data_wfs_Lantis_soil)

        nb_datapoints = {"Soil_OVAM" : data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)
        nb_datapoints = {"Soil_Lantis" : data_wfs_Lantis_soil_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_OVAM, data_wfs_Lantis_soil

    def soil_water(self):
        """
        Download the soil water data.
        """
        logger.info(f"Downloading soilwater data")
        data_wfs_VMM_ws = self.wfs_request(
            'waterbodems:pfas_meetpunten_fcs',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))
        data_wfs_OVAM = self.wfs_request(
            'pfas:pfas_analyseresultaten',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))

        data_wfs_VMM_ws = data_wfs_VMM_ws.drop_duplicates(
            subset=data_wfs_VMM_ws.columns)
        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)
        data_wfs_OVAM = data_wfs_OVAM[data_wfs_OVAM['medium'] == 'Waterbodem - sediment']

        data_wfs_VMM_ws_len = len(data_wfs_VMM_ws)
        data_wfs_OVAM_len = len(data_wfs_OVAM)

        nb_datapoints = {"Soil_water_VMM" : data_wfs_VMM_ws_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)
        nb_datapoints = {"Soil_water_OVAM" : data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_VMM_ws, data_wfs_OVAM

    def surface_water(self):
        """
        Download the surface water data.
        """
        logger.info(f"Downloading surface water data")
        data_wfs_VMM_sw = self.wfs_request(
            'pfas:pfas_oppwater',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))
        data_wfs_OVAM = self.wfs_request(
            'pfas:pfas_analyseresultaten',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))

        data_wfs_VMM_sw = data_wfs_VMM_sw.drop_duplicates(
            subset=data_wfs_VMM_sw.columns)
        data_wfs_OVAM = data_wfs_OVAM.drop_duplicates(
            subset=data_wfs_OVAM.columns)
        data_wfs_OVAM = data_wfs_OVAM[data_wfs_OVAM['medium'] == 'Oppervlaktewater']

        data_wfs_VMM_sw_len = len(data_wfs_VMM_sw)
        data_wfs_OVAM_len = len(data_wfs_OVAM)


        nb_datapoints = {"Surface_water_VMM" : data_wfs_VMM_sw_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)
        nb_datapoints = {"Surface_water_OVAM": data_wfs_OVAM_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_VMM_sw, data_wfs_OVAM

    def waste_water(self):
        """
        Download the waste water data.
        """
        logger.info(f"Downloading waste water data")
        data_wfs_VMM_ww = self.wfs_request(
            'pfas:pfas_afvalwater',
            Box(self.lowerleftx, self.lowerlefty, self.upperrightx, self.upperrighty))

        data_wfs_VMM_ww = data_wfs_VMM_ww.drop_duplicates(
            subset=data_wfs_VMM_ww.columns)

        data_wfs_VMM_ww_len = len(data_wfs_VMM_ww)

        nb_datapoints = {"Waste_water_VMM": data_wfs_VMM_ww_len}
        self.dictionary["nb_datapoints"][0].update(nb_datapoints)

        return data_wfs_VMM_ww

    def main(self, medium, save):

        #todo: get pfas analyseresultaten from OVAM in cache, so it doesn't have to download again.
        # Can you query wfs?
        # What with the cache of dov

        start_time = datetime.now()

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

        Returns
        -------
        The requested data in separate dataframe(s).
        """

        return_list = []

        for i in medium:
            if i == 'all':
                data_wfs_VMM_biota = self.biota()
                data_wfs_OVAM_effluent = self.effluent()
                data_pydov_VMM_gw, data_wfs_OVAM_gw, data_wfs_Lantis_gw = self.groundwater()
                data_wfs_OVAM_migration = self.migration()
                data_wfs_OVAM_pp = self.pure_product()
                data_wfs_OVAM_rainwater = self.rainwater()
                data_wfs_OVAM_soil, data_wfs_Lantis_soil = self.soil()
                data_wfs_VMM_ws, data_wfs_OVAM_ws = self.soil_water()
                data_wfs_VMM_sw, data_wfs_OVAM_sw = self.surface_water()
                data_wfs_VMM_ww = self.waste_water()
                return_list.extend([data_wfs_VMM_biota, data_wfs_OVAM_effluent, data_pydov_VMM_gw, data_wfs_OVAM_gw,
                        data_wfs_Lantis_gw, data_wfs_OVAM_migration, data_wfs_OVAM_pp, data_wfs_OVAM_rainwater,
                        data_wfs_OVAM_soil, data_wfs_Lantis_soil, data_wfs_VMM_ws, data_wfs_OVAM_ws, data_wfs_VMM_sw,
                        data_wfs_OVAM_sw, data_wfs_VMM_ww])
            elif i == 'biota':
                data_wfs_VMM_biota = self.biota()
                return_list.extend([data_wfs_VMM_biota])
            elif i == 'effluent':
                data_wfs_OVAM_effluent = self.effluent()
                return_list.extend([data_wfs_OVAM_effluent])
            elif i == 'groundwater':
                data_pydov_VMM_gw, data_wfs_OVAM_gw, data_wfs_Lantis_gw = self.groundwater()
                return_list.extend([data_pydov_VMM_gw, data_wfs_OVAM_gw, data_wfs_Lantis_gw])
            elif i == 'migration':
                data_wfs_OVAM_migration = self.migration()
                return_list.extend([data_wfs_OVAM_migration])
            elif i == 'pure product':
                data_wfs_OVAM_pp = self.pure_product()
                return_list.extend([data_wfs_OVAM_pp])
            elif i == 'rainwater':
                data_wfs_OVAM_rainwater = self.rainwater()
                return_list.extend([data_wfs_OVAM_rainwater])
            elif i == 'soil':
                data_wfs_OVAM_soil, data_wfs_Lantis_soil = self.soil()
                return_list.extend([data_wfs_OVAM_soil, data_wfs_Lantis_soil])
            elif i == 'soil water':
                data_wfs_VMM_ws, data_wfs_OVAM_ws = self.soil_water()
                return_list.extend([data_wfs_VMM_ws, data_wfs_OVAM_ws])
            elif i == 'surface water':
                data_wfs_VMM_sw, data_wfs_OVAM_sw = self.surface_water()
                return_list.extend([data_wfs_VMM_sw, data_wfs_OVAM_sw])
            elif i == 'waste water':
                data_wfs_VMM_ww = self.waste_water()
                return_list.extend([data_wfs_VMM_ww])

        metadata = json.dumps(self.dictionary, indent=3)
        path = os.getcwd()
        with open(f"{path}/results/metadata.json", "w") as outfile:
            outfile.write(metadata)

        if save:
            path = os.getcwd()
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
                        data_wfs_OVAM_ws.to_excel(writer, sheet_name='Soil_water_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Soil_water_OVAM'])
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
                        data_wfs_OVAM_ws.to_excel(writer, sheet_name='Soil_water_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Soil_water_OVAM'])
                    elif i == 'surface water':
                        data_wfs_VMM_sw.to_excel(writer, sheet_name='Surface_water_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Surface_water_VMM'])
                        data_wfs_OVAM_sw.to_excel(writer, sheet_name='Surface_water_OVAM')
                        pbar.update(metadata['nb_datapoints'][0]['Surface_water_OVAM'])
                    elif i == 'waste water':
                        data_wfs_VMM_ww.to_excel(writer, sheet_name='Waste_water_VMM')
                        pbar.update(metadata['nb_datapoints'][0]['Waste_water_VMM'])
            pbar.close()
        else:
            return return_list

        end_time = datetime.now()
        duration = end_time-start_time
        logger.info(f'The program was executed in {duration}.')


df = RequestPFASdata().main(['soil water', 'waste water'], False)
pd.set_option("display.max_columns", None)
print('df1: \n', df[0])
print('df2: \n', df[1])
print('df3: \n', df[2])
