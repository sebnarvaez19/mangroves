import ee
import geemap

ee.Initialize()

out_shp = "data/shapefile/mangrove_forests.shp"
forests = ee.FeatureCollection("projects/ee-sebnarvaez-mangroves/assets/forests")

geemap.ee_export_vector(forests, out_shp, verbose=True)