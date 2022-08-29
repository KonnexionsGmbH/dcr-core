# DCR-CORE - Application - Installation

![GitHub (Pre-)Release](https://img.shields.io/github/v/release/KonnexionsGmbH/dcr-core?include_prereleases)
![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/KonnexionsGmbh/dcr-core)

1. Clone or copy the **`DCR-CORE`** repository from [here](https://github.com/KonnexionsGmbH/dcr-core){:target="_blank"}.

2. Switch to the file directory **`DCR-CORE`**:

    **`cd dcr`**

3. Install the necessary Python packages by running the script  **`run_dcr_prod`** with action **`m_p`**.

4. Optionally, adjustments can be made in the following configuration files - details may be found [here](https://konnexionsgmbh.github.io/dcr/running_configuration/){:target="_blank"}:

    - **`data/db_initial_data_file.json`**: to configure the document languages to be used
    - **`logging_cfg.yaml`**: for the logging functionality
    - **`setup.cfg`**: for the **`DCR-CORE`** application in section **`DCR-CORE`**
 
5. Create a PostgreSQL database container by running the script **`scripts/run_setup_postgresql`** with action **`prod`**.

6. Create the **`DCR-CORE`** database by running the script **`run_dcr_prod`** with action **`db_c`**.
