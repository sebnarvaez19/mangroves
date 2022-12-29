# Spatial and temporal trends of NDVI in Mangrove Forests coastal lagoons in the Colombian Caribbean

This is the official repository of Spatial and temporal trends of NDVI in Mangrove Forests coastal lagoons in the Colombian Caribbean where could be found all the processing performed.

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