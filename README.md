# NYSmesonet-plotting
Scripts to read in New York State (NYS) mesonet data &amp; plot in various visualizations.

| Plotting Script | Description |
|-----------------|-------------|
accum_nys_mask.py | plots the NYS mesonet accumulated precipitation (mm) on a map of only NYS (103018_accum_nysm.png). 
nysm_meteograms.py | plots a meteogram for a specific NYS mesonet station.
read_mesonet_data.py | reads multiple NYS mesonet data files and extracts basic meteorological variables for later analysis & plotting.

**Note:** 
NYS mesonet data were requested from http://nysmesonet.org/weather/requestdata/. Geojson data (gz_2010_us_040_00_500k.json) were downloaded from https://eric.clst.org/tech/usgeojson/.

![Image](https://github.com/lgaudet/NYSmesonet-plotting/blob/master/103018_accum_nysm.png)
![Image](https://github.com/lgaudet/NYSmesonet-plotting/blob/master/nysm_meteogram_VOOR.png)
