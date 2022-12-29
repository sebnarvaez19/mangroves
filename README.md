# Spatial and temporal trends of NDVI in Mangrove Forests coastal lagoons in the Colombian Caribbean

This is the official repository of Spatial and temporal trends of NDVI in Mangrove Forests coastal lagoons in the Colombian Caribbean where could be found all the processing performed.

In this repository we analyze the relationship of the mean NDVI (taken from Landsat 5, 7 and 8 images) with total monthly precipitation, mean river dicharge (taken from near gauge stations) and surface temperature (also taken from landsat images) in the mangrove forests associated with Mallorquín, Totumo and La Virgen coastal lagoons (Colombian Caribbean Region). To do this we use time series decomposition to explore the data, autocorrelation and cross-correlation of the variables to see how the affect NDVI and a linear regression model to compare the effect of Precipitaiton, Discharge and Temperature on NDVI and try to predict it.

## Folder Structure
```bash
.
├── appendix                    # Folder for appendixes, must be created
│   ├── all_images              # All RGB images from Landsat 5, 7 and 8
│   ├── gaps                    # Plot to how many gaps are in the series (and when)
│   └── gauge_stations          # Shapefile with the stations to consult
├── data                        # Folder with all data used
│   ├── processed               # All processed data
│   ├── raster                  # Folder with the raster images by lagoon, must be created
│   │   ├── mallorquin          
│   │   ├── totumo
│   │   └── virgen
│   ├── raw                     # Raw data taken from gauge stations
│   └── shapefile               # Shapefiles to consult
├── images                      # All final plots
├── models                      # Linear regression models with their summaries
├── src                         # All scripts made
│   └── functions               # Functions made to optimize the process
├── wheels                      # Wheels for Windows to install problematic packages
└── mallorquin_example.ipynb    # Mallorquín Lagoon example
```

## Usage

To run all in this repository you have to install all dependencies in [requeriments.yml](requeriments.yml).

In Windows some of that packages could be installed with errors so you have to unistall da pacakges in the wheels folder manually.  

Finally you have to create the rasters folders for each lagoon in data folder and the appendix folder with the subfolder for all images, gaps and gauge stations