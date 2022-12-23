import numpy as np
import pandas as pd
import geopandas as gpd
import xarray
import rioxarray

from functions.na_seadec import na_seadec

import matplotlib.pyplot as plt
plt.style.use("src/style.mplstyle")

lagoons = ["mallorquin", "totumo", "virgen"]
path_nc = "data/processed/{}_ndvi_temperature.nc"
path_shp = "data/shapefile/mangrove_forests.shp"
path_csv = "data/processed/{}_mean_ndvi_temperature.csv"

forests = gpd.read_file(path_shp)

for lagoon in lagoons:
    data = xarray.open_dataset(path_nc.format(lagoon), decode_coords="all")
    roi = forests[forests.key == lagoon].geometry

    data = data.rio.clip(roi, all_touched=False)

    df = pd.DataFrame({
        "NDVI": data["NDVI"].mean(dim=["latitude", "longitude"]).to_series(),
        "Temperature": data["Surface Temperature"].mean(dim=["latitude", "longitude"]).to_series(),
        "Count": data["NDVI"].count(dim=["latitude", "longitude"]).to_series()
    }).resample("m").mean()

    mask = df.Count < df.Count.max()*0.1

    df.NDVI[mask] = np.nan
    df.Temperature[mask] = np.nan

    df = df.drop("Count", axis=1)
    
    df["NDVI_interpolated"] = na_seadec(df.NDVI)
    df["Temperature_interpolated"] = na_seadec(df.Temperature)

    df = df.dropna(axis=0, how="all")

    df.to_csv(path_csv.format(lagoon))
