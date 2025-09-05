# CitiBike_NY

**Visualizing CitiBike Usage Patterns in New York City**

---

## Overview

This project explores CitiBike trip data from 2022 through spatial analyses, user-type breakdowns, and interactive visualizations. It incorporates neighborhood population and socio-demographic data as well as subway infrastructure geography to better understand urban mobility dynamics.

To view the analyses and recommendations in summarised format without running the files, you can simply open the [dashboard](https://citibikeny-bds8rujq4bcgrepucgv2oc.streamlit.app/)

---

## Project Structure

```
CitiBike_NY/
├── Data/                              # Processed datasets
├── notebooks/                         # Jupyter notebooks for data preparation, exploration & analyses
├── scripts/                           # Scripts used for extracting data and dashboard creation
├── visualisations/                    # Output images, plots, and maps
├── requirements.txt                   # Python dependencies
├── 2020 Neighborhood Tabulation Areas (NTAs)_20250721.geojson   # Neighborhood boundaries
├── subway_lines.geojson               # Subway route geometries
├── subway_stations.geojson            # Subway station locations
└── README.md                          # This documentation
```


## Setup & Installation

1. **Clone the repository:**

git clone https://github.com/SeanKGitHub/CitiBike_NY.git


cd CitiBike_NY


2. **Install dependencies:**

pip install -r requirements.txt


3. **Data Preparation:**

⚠️ Note: File paths in the notebooks/scripts are currently configured for the author’s local environment. You will need to update these paths to match your own directory structure before running the code.

Download the raw Citi Bike trip data for all months of 2022 and place the files into a local Data/ folder. (https://s3.amazonaws.com/tripdata/index.html).

Adapt paths within this script and run it to extract the tripdata: 
    
    scripts/extract_data.py

To run the notebook that prepares the main dataframe needed for the analyses, you need to first get an API key from the National Centers for Environmental Information (NCEI) to access the necessary weather data.

With this saved in a local .env folder, you can then adapt the paths accordingly and run the following notebook:

    notebooks/loading_merging_wrangling.ipynb

Which will save the main dataframe of processed data needed for the analysis notebooks as a parquet file.

Following this, these notebooks must be run to generate summary and sample datasets for certain visualisations, as well as process the geographic and socio-demographic data needed for map layers:

    notebooks\chart_data_queries.ipynb
    notebooks\making_station_summary.ipynb
    notebooks\NY_pop_inc_prep.ipynb

⚠️ Note: Once the above notebooks were executed and data saved, the analysis notebooks don’t need to be run in a strict order. Some are exploratory and independent of each other. You can open whichever analysis interests you, as long as the required data files exist in Data/.

---

## Running the Analysis

1. **Explore data in Jupyter notebooks:**

Navigate to the `notebooks/` directory and start a notebook such as `weather_EDA.ipynb`:

jupyter notebook notebooks/exploration.ipynb


2. **Generate Visualizations:**

Use notebooks to produce charts and maps. Visual outputs are stored in `visualisations/`.

3. **Create Dashboard**

There are two versions of the final dashboard, one that runs on locally saved (full) dataset, while the other Github version is based off a subsample of 100,000 rows to accommodate Github filesize limitations.
    
    scripts\st_end_dashboard_github.py
    scripts\st_end_dashboard_local.py

---

## Project Goals & Use-Cases

- Understand spatial distribution of trips and station usage across NYC neighborhoods.
- Explore the relationship between CitiBike usage and subway infrastructure or neighborhood boundaries.
- Assist urban planners or mobility analysts in identifying underserved areas and usage hotspots.
- Enable interactive visual storytelling through mapped and charted data.

---

## Data Sources

- **Citi Bike trip data**: [source](https://s3.amazonaws.com/tripdata/index.html)
- **Neighborhood Tabulation Areas**: 2020 NTA GeoJSON (included) https://data.cityofnewyork.us/City-Government/2020-Neighborhood-Tabulation-Areas-NTAs-/9nt8-h7nd/about_data 
- **Subway infrastructure**: Available GeoJSON for lines and stations (included)
- **Income Data** American Community Survey (ACS) 5 year file (2018-2022). Downloaded from https://www.nyc.gov/content/planning/pages/resources/datasets/american-community-survey
- **Population data** U.S. Census Bureau, 2010 and 2020 Census Redistricting Data (Public Law 94-171) Summary Files. https://www.nyc.gov/assets/planning/download/office/planning-level/nyc-population/census2020/nyc_decennialcensusdata_2010_2020_change.xlsx

---

## License

MIT License

---

## Contact & Acknowledgments

- Developed by **SeanKGitHub**
- Inspired by broader efforts in urban data visualisation and mobility analytics.