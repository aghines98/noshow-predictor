# Data sources

Raw data files aren't committed to this repo (kept out via `.gitignore` to keep
the repo lean). To reproduce training locally, download:

- `KaggleV2-May-2016.csv` — [Medical Appointment No Shows](https://www.kaggle.com/datasets/joniarroba/noshowappointments) (Kaggle)
- `2025_Gaz_zcta_national.txt` — [ZCTA Gazetteer file](https://www.census.gov/geographies/reference-files/time-series/geo/gazetteer-files.html) (US Census Bureau)
- `CensusPopulation.json` — derived from US Census Bureau population data

Place downloaded files in this folder, then run `zcta_to_json.py` and
`model_dataprep.py` to regenerate the normalized training set.
