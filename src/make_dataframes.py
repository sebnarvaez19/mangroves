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
path_csv = "data/processed/mean_ndvi_temperature.csv"

forests = gpd.read_file(path_shp)
data = []

for lagoon in lagoons:
    ic = xarray.open_dataset(path_nc.format(lagoon), decode_coords="all")
    roi = forests[forests.key == lagoon].geometry

    ic = ic.rio.clip(roi, all_touched=False)

    df = pd.DataFrame({
        "NDVI": ic["NDVI"].mean(dim=["latitude", "longitude"]).to_series(),
        "Temperature": ic["Surface Temperature"].mean(dim=["latitude", "longitude"]).to_series(),
        "Count": ic["NDVI"].count(dim=["latitude", "longitude"]).to_series()
    }).resample("m").mean()

    df.Count[df.Count.isna()] = 0
    df["PixelPercentage"] = df.Count/df.Count.max()*100
    df["Lagoon"] = lagoon

    mask = df.PixelPercentage < 0.10

    df.NDVI[mask] = np.nan
    df.Temperature[mask] = np.nan

    df.NDVI = na_seadec(df.NDVI)
    df.Temperature = na_seadec(df.Temperature)

    df = df.drop("Count", axis=1)
    df = df.dropna(axis=0, how="all")
    df = df[df.index >= np.datetime64("2001-01-01")]

    data.append(df)

data = pd.concat(data)
data.to_csv(path_csv)