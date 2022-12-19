import ee
import geemap

from statgis.landsat_functions import landsat_scaler, landsat_cloud_mask
from functions.gee_processing import renamer7, renamer8, calc_ndvi

ee.Initialize()

L5 = ee.ImageCollection("LANDSAT/LT05/C02/T1_L2").filter(ee.Filter.calendarRange(1996, 1998, "year"))
L7 = ee.ImageCollection("LANDSAT/LE07/C02/T1_L2").filter(ee.Filter.calendarRange(1999, 2013, "year"))
L8 = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").filter(ee.Filter.calendarRange(2014, 2021, "year"))

forests = ee.FeatureCollection("projects/ee-sebnarvaez-mangroves/assets/forests")

keys = ["mallorquin", "totumo", "virgen"]

for key in keys:
    roi = forests.filter(ee.Filter.eq("key", key)).first().geometry()
    
    l5 = L5.filterBounds(roi).map(landsat_scaler).map(landsat_cloud_mask).map(renamer7).map(calc_ndvi)
    l7 = L7.filterBounds(roi).map(landsat_scaler).map(landsat_cloud_mask).map(renamer7).map(calc_ndvi)
    l8 = L8.filterBounds(roi).map(landsat_scaler).map(landsat_cloud_mask).map(renamer8).map(calc_ndvi)

    for i in range(1996, 2022):
        for j in range(1, 13):
            if i < 1999:
                img = (
                    l5.filter(ee.Filter.calendarRange(i, i, "year"))
                      .filter(ee.Filter.calendarRange(j, j, "month"))
                      .mean()
                      .set("date", f"01-{j:02d}-{i:04d}")
                )
            
            elif i < 2014:
                img = (
                    l7.filter(ee.Filter.calendarRange(i, i, "year"))
                      .filter(ee.Filter.calendarRange(j, j, "month"))
                      .mean()
                      .set("date", f"01-{j:02d}-{i:04d}")
                )

            else:
                img = (
                    l8.filter(ee.Filter.calendarRange(i, i, "year"))
                      .filter(ee.Filter.calendarRange(j, j, "month"))
                      .mean()
                      .set("date", f"01-{j:02d}-{i:04d}")
                )

            filename = f"data/raster/{key}/{i:04d}-{j:02d}-01.tif"

            print(f"{key}: image {j:02d}-{i:04d}")
            geemap.ee_export_image(
                img, filename=filename, scale=30, region=roi, unmask_value=-3e5
            )