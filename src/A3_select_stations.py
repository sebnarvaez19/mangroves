# %% Imports
import geopandas as gpd

# %% Define parameters
# CRS to reproject all dataframes
EPSG = 32618

# Varaibles that will be discarded from stations dataframe
unused_vars = [
    "TECNOLOGIA", "AREA_OPERA", "AREA_HIDRO", 
    "ZONA_HIDRO", "observacio", "CORRIENTE", 
    "SUBZONA_HI", "ENTIDAD", "subred"
]

# %% Defien paths
forests_path = "data/shapefile/mangrove_forests.shp"
stations_path = "data/shapefile/CNE_IDEAM.shp"
save_path = "appendix/gauge_stations/stations_of_interest.shp"

# %% Read and reproject forests and stations
forests = gpd.read_file(forests_path).to_crs(epsg=EPSG)
stations = gpd.read_file(stations_path).to_crs(epsg=EPSG)

# %% Subset stations
buffers = forests.copy()                    # Copy the data from the forest
buffers.geometry = buffers.buffer(6000)     # Replace its geometry with a buffer of 6 km
buffers = buffers[["key", "geometry"]]      # Get only the key (Forest) and geomtry

# Spatial join to filter the stations and add thier respective forest
stations = stations.sjoin(buffers, how="inner")

# Get only Climatical, Pluviometrical and Synaptical stations
categories_of_interest = (stations.CATEGORIA == "PM") | \
    (stations.CATEGORIA == "CP") | (stations.CATEGORIA == "SP")

# Get stations from the categories of interest
stations = stations[categories_of_interest]

# Drop unused variables
stations = stations.drop(unused_vars, axis=1)

# %% Show stations of interest
print(stations)

# %% Save stations of interst
stations.to_file(save_path)
