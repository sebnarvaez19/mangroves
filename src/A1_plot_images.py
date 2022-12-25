# %% Imports
import ee
import geemap
import matplotlib.pyplot as plt

from geemap import cartoee
from functions.gee_processing import *

ee.Initialize()

# %% Define constants
path = "./appendix/all_images/{}.png"

lagoons = ["mallorquin", "totumo", "virgen"]

zooms = {
    "mallorquin": [-74.82934525005177, 11.028868816913656, -74.91404810273207, 11.062596879860857],
    "totumo": [-75.21347135428282, 10.690516171754405, -75.25896861605656, 10.760405796055716],
    "virgen": [-75.4639732791029, 10.409937971541012, -75.51173334636263, 10.512366397279758]
}

vis = {"bands": ["RED", "GREEN", "BLUE"], "min": 0.0, "max": 0.3, "gamma": 1.3}

# %% Load mangrove forests feature collection
forests = ee.FeatureCollection("projects/ee-sebnarvaez-mangroves/assets/forests")

# %% Load, scale and rename Landsat 5, 7 and 8 image collections
L5 = (
    ee.ImageCollection("LANDSAT/LT05/C02/T1_L2").map(image_scaler)
                                                .map(renamer7)
                                                .filter(ee.Filter.calendarRange(1996, 1998, "year"))
)

L7 = (
    ee.ImageCollection("LANDSAT/LE07/C02/T1_L2").map(image_scaler)
                                                .map(renamer7)
                                                .filter(ee.Filter.calendarRange(1999, 2013, "year"))
)

L8 = (
    ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").map(image_scaler)
                                                .map(renamer8)
                                                .filter(ee.Filter.calendarRange(2014, 2021, "year"))
)

# %% Merge image collections
IC = L5.merge(L7.merge(L8))

# %% Loop over the image collection to plot all images
for lagoon in lagoons:
    roi = forests.filter(ee.Filter.eq("key", lagoon)).first().geometry()
    ICF = IC.filterBounds(roi)
    
    dates = ICF.reduceColumns(ee.Reducer.toList(), ["DATE_ACQUIRED"]).get("list").getInfo()

    for date in dates:
        img = ICF.filter(ee.Filter.eq("DATE_ACQUIRED", date)).mean()

        fig = plt.figure()

        ax = cartoee.get_map(img, vis_params=vis, region=zooms[lagoon])
        lb = f"{lagoon} {date}"

        ax.set_title(lb, fontsize=12)

        plt.savefig(path.format(lb))
        plt.close()
