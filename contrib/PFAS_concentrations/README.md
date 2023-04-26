# Download the PFAS data from DOV

Download all the publicly available PFAS data from [DOV](https://www.dov.vlaanderen.be/) through [pydov](https://pydov.readthedocs.io/en/stable/index.html).

The dataset consist of the following PFAS data:

- From [VMM](https://www.vmm.be/)
    - surface water
    - soilwater
    - groundwater
    - waste water
    - biota

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

The different datasets can be saved as separate Excel tabs of one Excel file.

## Installation for contribution

Noticed a bug, want to improve the documentation? Great! Want to dive into the code directly on your local machine? Make sure to
have the development environment setup:

1. Fork the [project repository](https://github.com/DOV-Vlaanderen/pydov) by clicking on the 'Fork' button
  near the top right of the page. This creates a copy of the code under your personal GitHub user account.
2. Clone the [Github repo](https://github.com/DOV-Vlaanderen/pydov):

    ```$ git clone https://github.com/YOUR-GITHUB-USERNAME/pydov```

3. Create a development environment using the environment.yml from the contrib folder, for example using [conda](https://docs.conda.io/projects/conda/en/stable/):

    ```$ conda env create -f environment.yml```

4. Link the environment to the project in your IDE as interpreter.

## Installation for use
1. Download the [project repository](https://github.com/DOV-Vlaanderen/pydov) as a zip-file.
2. Create a development environment using the environment.yml from the contrib folder, for example using [conda](https://docs.conda.io/projects/conda/en/stable/):
    
    ```$ conda env create -f environment.yml```

3. Execute script
 
    3.1 Work with the code directly in your IDE
    
     - Link the environment to the project in your IDE as interpreter.

    3.2 Use the example notebooks
    
     - Activate the environment 

        ```$ conda activate pydov_pfas```
    
     - Open the notebooks with the examples

        ```$ cd 'PATH_TO_CONTRIB_FOLDER'``` 
        
        ```$ jupyter notebook```

## Tutorial

Possible mediums:

<details>
<summary>'all'</summary>

    -> returns 15 dataframes
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

    -> returns 1 dataframes
        - Migration_OVAM
</details>

<details>
<summary>'pure product'</summary>

    -> returns 1 dataframes
        - Pure_product_OVAM
</details>

<details>
<summary>'rainwater'</summary>

    -> returns 1 dataframes
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

    -> returns 1 dataframes
        - Waste_water_VMM
</details>


- Case 1 : You want to save the data

  <br>

  - Example 1 : You want to download and save all the PFAS data

      ```python
      RequestPFASdata().main(['all'], True)
      ```
      This results in one excel-file with 15 tabs. One for each dataset.

  <br>

  <br>

  - Example 2 : You only want to download and save the groundwater data

      ```python
      RequestPFASdata().main(['groundwater'], True)
      ```
      This results in one excel-file with 3 tabs. One tab with the groundwater data from VMM,
      one with the groundwater data from OVAM and one with the groundwater data from Lantis.

  <br>

  - Example 3 : You want to download and save the soil and groundwater data

      ```python
      RequestPFASdata().main(['soil', 'groundwater'], True)
      ```
      This results in one excel-file with 5 tabs. One tab with the soil data from OVAM,
      one with the soil data from Lantis, one with the groundwater data from VMM,
      one with the groundwater data from OVAM and one with the groundwater data from Lantis.

  <br>

- Case 2 : You want the data in a dataframe to integrate it in your python script

  <br>

  - Example 1 : You want to download all the PFAS data

    ```python
    df = RequestPFASdata().main(['all'], False)
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
    ```
  <br>

  <br>

  - Example 2 : You only want to download the groundwater data

    ```python
    df = RequestPFASdata().main(['groundwater'], False)
    df[0] # Groundwater_VMM
    df[1] # Groundwater_OVAM
    df[2] # Groundwater_Lantis
    ```
  <br>

  - Example 3 : You want to download the soil and groundwater data

    ```python
    df = RequestPFASdata().main(['soil', 'groundwater'], False)
    df[0] # Soil_OVAM
    df[1] # Soil_Lantis
    df[2] # Groundwater_VMM
    df[3] # Groundwater_OVAM
    df[4] # Groundwater_Lantis
    ```
