# %% Imports
import numpy as np
import pandas as pd
import geopandas as gpd

import xarray
import rioxarray

from functions.na_seadec import na_seadec

# %% Define constants
t0 = np.datetime64("2001-01-01")
tf = np.datetime64("2022-01-01")

meteorological_path = "data/raw/{}_raw_data.csv"
discharge_path = "data/raw/magdalena_river_discharge_data.csv"
spectral_path = "data/processed/{}_ndvi_temperature.nc"
forests_path = "data/shapefile/mangrove_forests.shp"
soi_path = "data/processed/simple_soi.csv"

lagoons = ["mallorquin", "totumo", "virgen"]
cities = ["barranquilla", "totumo", "cartagena"]

# %% Read total precipitation and mean discharge
hydro_data = []

for city, lagoon in zip(cities, lagoons):
    df = pd.read_csv(meteorological_path.format(city), parse_dates=[16], index_col=16)
    df = df[["Valor"]]
    df = df.resample("m").mean()

    df.columns = ["Precipitation"]
    df.index.name = "Time"
    df["Lagoon"] = lagoon

    if df.Precipitation.isna().sum() > 0:
        df.Precipitation = na_seadec(df.Precipitation) 

    if city == "barranquilla":
        df2 = pd.read_csv(discharge_path, parse_dates=[16], index_col=16)
        df2 = df2[["Valor"]]
        df2 = df2.resample("m").mean()
        
        df2.columns = ["Discharge"]
        df2.index.name = "Time"
        
        if df2.Discharge.isna().sum() > 0:
            df2.Discharge = na_seadec(df2.Discharge)

        df = df.merge(df2, left_index=True, right_index=True)

    else:
        df["Discharge"] = np.nan

    hydro_data.append(df)

hydro_data = pd.concat(hydro_data)
hydro_data = hydro_data[["Lagoon", "Precipitation", "Discharge"]]
hydro_data = hydro_data.reset_index()

# %% Read mean NDVI and temperature
forests = gpd.read_file(forests_path)

spectral_data = []

for lagoon in lagoons: 
    data = xarray.open_dataset(spectral_path.format(lagoon), decode_coords="all")
    roi = forests[forests.key == lagoon].geometry

    data = data.rio.clip(roi, all_touched=False)

    df = pd.DataFrame({
        "NDVI": data["NDVI"].mean(dim=["latitude", "longitude"]).to_series(), 
        "Temperature": data["Surface Temperature"].mean(dim=["latitude", "longitude"]).to_series(),
        "Count": data["NDVI"].count(dim=["latitude", "longitude"]).to_series()
    }).resample("m").mean()

    df.Count[df.Count.isna()] = 0
    df["PixelPercentage"] = df.Count/df.Count.max()*100
    df = df.drop("Count", axis=1)

    mask = df.PixelPercentage < 0.10

    df["NDVI"][mask] = np.nan
    df["Temperature"][mask] = np.nan

    df.NDVI = na_seadec(df.NDVI)
    df.Temperature = na_seadec(df.Temperature)

    df["Lagoon"] = lagoon
    df.index.name = "Time"
    
    spectral_data.append(df)

spectral_data = pd.concat(spectral_data)
spectral_data = spectral_data[["Lagoon", "NDVI", "Temperature", "PixelPercentage"]]
spectral_data = spectral_data.reset_index()

# %% Merge hydrological and spectral data
data = hydro_data.merge(spectral_data, how="left", on=["Time", "Lagoon"])

mask = (data.Time > t0) & (data.Time < tf)
data = data[:][mask]
data = data.sort_values(["Lagoon", "Time"])
data = data.reset_index(drop=True)

# %% Load SOI data to final dataframe
soi_data = pd.read_csv(soi_path, parse_dates=[0])
soi_data.columns = ["Time", "SOI", "ENSO"]
data = data.merge(soi_data, how="left", on="Time")

# %% View final dataframe
print(data)

# %% Save final dataframe
data.to_csv("data/processed/hydrological_spectral_mean_data.csv")
