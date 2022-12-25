# %% Imports
import ee
import geemap

from statgis.landsat_functions import landsat_scaler, landsat_cloud_mask
from functions.gee_processing import renamer7, renamer8, calc_ndvi

ee.Initialize()

# %% Load Landsat 5, 7 and 8 SR images colloection
L5 = ee.ImageCollection("LANDSAT/LT05/C02/T1_L2").filter(ee.Filter.calendarRange(1996, 1998, "year"))
L7 = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2").filter(ee.Filter.calendarRange(1999, 2013, "year"))
L8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").filter(ee.Filter.calendarRange(2014, 2021, "year"))

# %% Load mangrove forests feature collection
forests = ee.FeatureCollection("projects/ee-sebnarvaez-mangroves/assets/forests")

# %% Define the keys to iterate the forests
keys = ["mallorquin", "totumo", "virgen"]

# %% Iterate the forests to download image by forests and date
for key in keys:
    # Extract the forest of interest
    roi = forests.filter(ee.Filter.eq("key", key)).first().geometry()
    
    # Filter images that intersect with the forest and interest and
    # scale them, mask their clouds, rename their bands and calculate their NDVI
    l5 = L5.filterBounds(roi).map(landsat_scaler).map(landsat_cloud_mask).map(renamer7).map(calc_ndvi)
    l7 = L7.filterBounds(roi).map(landsat_scaler).map(landsat_cloud_mask).map(renamer7).map(calc_ndvi)
    l8 = L8.filterBounds(roi).map(landsat_scaler).map(landsat_cloud_mask).map(renamer8).map(calc_ndvi)

    # For loop to iterate throught years
    for i in range(1996, 2022):
        # For loop to iterate throught months
        for j in range(1, 13):
            # If the image is from before 1999 use Landsat 5, filter them by the
            # year and the month, calculate the mean and set the date
            if i < 1999:
                img = (
                    l5.filter(ee.Filter.calendarRange(i, i, "year"))
                      .filter(ee.Filter.calendarRange(j, j, "month"))
                      .mean()
                      .set("date", f"01-{j:02d}-{i:04d}")
                )
            
            # If the images are from 1999 to 2014 use Landsat 7 and perform the
            # same process
            elif i < 2014:
                img = (
                    l7.filter(ee.Filter.calendarRange(i, i, "year"))
                      .filter(ee.Filter.calendarRange(j, j, "month"))
                      .mean()
                      .set("date", f"01-{j:02d}-{i:04d}")
                )

            # If the images are from after 2014 use Landsat 8 and perform the
            # same process
            else:
                img = (
                    l8.filter(ee.Filter.calendarRange(i, i, "year"))
                      .filter(ee.Filter.calendarRange(j, j, "month"))
                      .mean()
                      .set("date", f"01-{j:02d}-{i:04d}")
                )

            # Define the save path of the image
            filename = f"data/raster/{key}/{i:04d}-{j:02d}-01.tif"

            # Report and save the image
            print(f"{key}: image {j:02d}-{i:04d}")
            geemap.ee_export_image(
                img, filename=filename, scale=30, region=roi, unmask_value=-3e5
            )