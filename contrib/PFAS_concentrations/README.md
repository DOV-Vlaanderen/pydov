# Download the PFAS data from DOV

Download all the publicly available PFAS data from [DOV](https://www.dov.vlaanderen.be/) through [pydov](https://pydov.readthedocs.io/en/stable/index.html).

The dataset consist of the following PFAS data:

- From [VMM](https://www.vmm.be/)
    - surface water
    - soilwater
    - groundwater
    - waste water
    - biota
    - air dust
    - air gas
    - air deposition

- From [OVAM](https://ovam.vlaanderen.be/)
    - rain water
    - surface water
    - soilwater
    - groundwater
    - soil
    - effluent
    - migration
    - pure product

- From [Lantis](https://www.lantis.be/)
    - groundwater
    - soil

The different datasets from the different sources (VMM, OVAM, Lantis) can be saved as separate Excel tabs of one Excel file.

There is also an option to download the combined datasets per matrix and save them as separate Excel tabs.

- Combined datasets
  - combined groundwater
    - Contains groundwater data from VMM, OVAM and Lantis
  - combined soil
    - Contains soil data from OVAM and Lantis
  - combined soilwater
    - Contains soilwater data from VMM and OVAM
  - combined surface water
    - Contains surface water from VMM and OVAM

## Installation for contribution

Noticed a bug, want to improve the documentation? Great! Want to dive into the code directly on your local machine? Make sure to
have the development environment setup:

1. Fork the [project repository](https://github.com/DOV-Vlaanderen/pydov) by clicking on the 'Fork' button
  near the top right of the page. This creates a copy of the code under your personal GitHub user account.
2. Clone the [Github repo](https://github.com/DOV-Vlaanderen/pydov):


    $ git clone https://github.com/YOUR-GITHUB-USERNAME/pydov

3. Create a development environment, for example using [conda](https://docs.conda.io/projects/conda/en/stable/):


    # using conda:
      $ conda env create -f environment.yml

4. Link the environment to the project in your IDE as interpreter.

## Installation for use

Create a development environment, for example using [conda](https://docs.conda.io/projects/conda/en/stable/):

    # using conda:
      $ conda env create -f environment.yml


## Tutorial

Possible mediums:

<details>
<summary>'all'</summary>

    -> returns 22 dataframes
        - Biota_VMM
        - Effluent_OVAM
        - Groundwater_VMM
        - Groundwater_OVAM
        - Groundwater_Lantis
        - Migration_OVAM
        - Pure_product_OVAM
        - Rainwater_OVAM
        - Soil_OVAM
        - Soil_Lantis
        - Soil_water_VMM
        - Soil_water_OVAM
        - Surface_water_VMM
        - Surface_water_OVAM
        - Waste_water_VMM
        - Air_dust_VMM
        - Air_gas_VMM
        - Air_deposition_VMM
        - Combined_groundwater
        - Combined_soil
        - Combined_soil_water
        - Combined_surface_water

</details>

<details>
<summary>'biota'</summary>

    -> returns 1 dataframe
        - Biota_VMM
</details>

<details>
<summary>'effluent'</summary>

    -> returns 1 dataframe
        - Effluent_OVAM
</details>

<details>
<summary>'groundwater'</summary>

    -> returns 3 dataframes
        - Groundwater_VMM
        - Groundwater_OVAM
        - Groundwater_Lantis
</details>

<details>
<summary>'migration'</summary>

    -> returns 1 dataframe
        - Migration_OVAM
</details>

<details>
<summary>'pure product'</summary>

    -> returns 1 dataframe
        - Pure_product_OVAM
</details>

<details>
<summary>'rainwater'</summary>

    -> returns 1 dataframe
        - Rainwater_OVAM
</details>

<details>
<summary>'soil'</summary>

    -> returns 2 dataframes
        - Soil_OVAM
        - Soil_Lantis
</details>

<details>
<summary>'soil water'</summary>

    -> returns 2 dataframes
        - Soil_water_VMM
        - Soil_water_OVAM
</details>

<details>
<summary>'surface water'</summary>

    -> returns 2 dataframes
        - Surface_water_VMM
        - Surface_water_OVAM
</details>

<details>
<summary>'waste water'</summary>

    -> returns 1 dataframe
        - Waste_water_VMM
</details>

<details>
<summary>'air'</summary>

    -> returns 3 dataframes
        - Air_dust_VMM
        - Air_gas_VMM
        - Air_deposition_VMM
</details>

<details>
<summary>'combined_groundwater'</summary>

    -> returns 1 dataframe
        - Combined groundwater
</details>

<details>
<summary>'combined_soil'</summary>

    -> returns 1 dataframe
        - Combined soil
</details>

<details>
<summary>'combined_soil_water'</summary>

    -> returns 1 dataframe
        - Combined soilwater
</details>

<details>
<summary>'combined_surface_water'</summary>

    -> returns 1 dataframe
        - Combined surface water
</details>

### Basis

```python
from pydov.util.location import Within, Box
from pydov.util.query import Join
from loguru import logger
from owslib.fes2 import PropertyIsEqualTo, And
from tqdm.auto import tqdm
from datetime import datetime
from importlib.metadata import version

medium = ['MEDIUM']
location = Within(Box(LowerLeftX,LowerLeftY,UpperRightX,UpperRightY))  # Bounding box of area of interest

rd = RequestPFASdata()

# If you are only interested in the data
df = rd.main(medium, location=location, max_features=None, save=False)[0]

# If you are only interested in the metadata
metadata = rd.main(medium, location=location, max_features=None, save=False)[1]

# If you are interested in both the data as the metadata
df, metadata = rd.main(medium, location=location, max_features=None, save=False)

```
Check out the query and customization options from pydov.\
You can query on [location](https://pydov.readthedocs.io/en/stable/query_location.html)
and also [restrict the number of WFS features returned](https://pydov.readthedocs.io/en/stable/sort_limit.html).

### Case 1 : You want to save the data

  - Example 1 : You want to download and save all the PFAS data of Flanders

      ```python
      # Change in the basis request:
        medium = ['all']
        location = Within(Box(15000, 150000, 270000, 250000))  # Bounding box Flanders
        save = True
      ```
      This results in one excel-file with 15 tabs. One for each dataset.


  - Example 2 : You only want to download and save the groundwater PFAS data of Flanders

      ```python
    # Change in the basis request:
        medium = ['groundwater']
        location = Within(Box(15000, 150000, 270000, 250000))  # Bounding box Flanders
        save = True
      ```
      This results in one excel-file with 3 tabs. One tab with the groundwater data from VMM,
      one with the groundwater data from OVAM and one with the groundwater data from Lantis.


  - Example 3 : You want to download and save the soil and groundwater PFAS data of Flanders

      ```python
    # Change in the basis request:
        medium = ['soil', 'groundwater']
        location = Within(Box(15000, 150000, 270000, 250000))  # Bounding box Flanders
        save = True
      ```
      This results in one excel-file with 5 tabs. One tab with the soil data from OVAM,
      one with the soil data from Lantis, one with the groundwater data from VMM,
      one with the groundwater data from OVAM and one with the groundwater data from Lantis.


- Example 4 : You want to download and save the combined groundwater PFAS data of Flanders

    ```python
   # Change in the basis request:
      medium = ['combined_groundwater']
      location = Within(Box(15000, 150000, 270000, 250000))  # Bounding box Flanders
      save = True
    ```
    This results in one excel-file with one tab containing the groundwater data from all the sources (VMM, OVAM and Lantis).

### Case 2 : You want the data in a dataframe to integrate it in your python script

  - Example 1 : You want to download all the PFAS data of Flanders

    ```python
    # Change in the basis request:
        medium = ['all']
        location = Within(Box(15000, 150000, 270000, 250000))  # Bounding box Flanders

    # Access data:
        df[0] # Biota_VMM
        df[1] # Effluent_OVAM
        df[2] # Groundwater_VMM
        df[3] # Groundwater_OVAM
        df[4] # Groundwater_Lantis
        df[5] # Migration_OVAM
        df[6] # Pure_product_OVAM
        df[7] # Rainwater_OVAM
        df[8] # Soil_OVAM
        df[9] # Soil_Lantis
        df[10] # Soil_water_VMM
        df[11] # Soil_water_OVAM
        df[12] # Surface_water_VMM
        df[13] # Surface_water_OVAM
        df[14] # Waste_water_VMM
        df[15] # Air_dust_VMM
        df[16] # Air_gas_VMM
        df[17] # Air_deposition_VMM
        df[18] # Combined_groundwater
        df[19] # Combined_soil
        df[20] # Combined_soil_water
        df[21] # Combined_surface_water
    ```

  - Example 2 : You only want to download the groundwater PFAS data of Flanders

    ```python
    # Change in the basis request:
        medium = ['groundwater']
        location = Within(Box(15000, 150000, 270000, 250000))  # Bounding box Flanders

    # Access data:
        df[0] # Groundwater_VMM
        df[1] # Groundwater_OVAM
        df[2] # Groundwater_Lantis
    ```

  - Example 3 : You want to download the soil and groundwater PFAS data of Flanders

    ```python
    # Change in the basis request:
        medium = ['soil', 'groundwater']
        location = Within(Box(15000, 150000, 270000, 250000))  # Bounding box Flanders

    # Access data:
        df[0] # Soil_OVAM
        df[1] # Soil_Lantis
        df[2] # Groundwater_VMM
        df[3] # Groundwater_OVAM
        df[4] # Groundwater_Lantis
    ```

  - Example 4 : You want to download the combined groundwater PFAS data of Flanders

      ```python
    # Change in the basis request:
        medium = ['combined_groundwater']
        location = Within(Box(15000, 150000, 270000, 250000))  # Bounding box Flanders

    # Access data:
        df[0] # combined_groundwater
      ```
