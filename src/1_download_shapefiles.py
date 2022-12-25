# %% Imports
import ee
import geemap

ee.Initialize()

# %% define save path
save_shp = "data/shapefile/mangrove_forests.shp"

# %% Load mangrove forests as a feature collection
forests = ee.FeatureCollection("projects/ee-sebnarvaez-mangroves/assets/forests")

# %% Export feature collection to shapefile
geemap.ee_export_vector(forests, save_shp, verbose=True)