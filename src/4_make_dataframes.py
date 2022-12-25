# %% Imports
import numpy as np
import pandas as pd
import geopandas as gpd

import xarray
import rioxarray

from functions.na_seadec import na_seadec

# %% Define the time limits and the data paths
t0 = np.datetime64("2001-01-01")
tf = np.datetime64("2022-01-01")

meteorological_path = "data/raw/{}_raw_data.csv"
discharge_path = "data/raw/magdalena_river_discharge_data.csv"
spectral_path = "data/processed/{}_ndvi_temperature.nc"
forests_path = "data/shapefile/mangrove_forests.shp"
soi_path = "data/processed/simple_soi.csv"

# %% Define the key to iterate raw and processed data
lagoons = ["mallorquin", "totumo", "virgen"]
cities = ["barranquilla", "totumo", "cartagena"]

# %% Read total precipitation and mean discharge
hydro_data = []

# For loop to iterate throught cities and lagoons to load the precipitation data
for city, lagoon in zip(cities, lagoons):
    # Load precipitation data, dates are in the 17 column
    df = pd.read_csv(meteorological_path.format(city), parse_dates=[16], index_col=16)
    df = df[["Valor"]]                          # Subset the column with the data
    df = df.resample("m").mean()                # Resample data to monthly mean

    df.columns = ["Precipitation"]              # Rename column
    df.index.name = "Time"                      # Rename index column
    df["Lagoon"] = lagoon                       # Define a new column with the lagoon

    # If there are NaN values in precipitation, interpolate it with na_seadec
    if df.Precipitation.isna().sum() > 0:
        df.Precipitation = na_seadec(df.Precipitation) 

    # If the city is Barranquilla we have to load the mean river discharge of
    # Magdalena river
    if city == "barranquilla":
        # Load mean discharge data, dates are in the column 17
        df2 = pd.read_csv(discharge_path, parse_dates=[16], index_col=16)
        df2 = df2[["Valor"]]                # Subset the data
        df2 = df2.resample("m").mean()      # Resample to monthly mean
        
        df2.columns = ["Discharge"]         # Rename column
        df2.index.name = "Time"             # Rename index column
        
        # If there are NaN values interpolate it with na_seadec
        if df2.Discharge.isna().sum() > 0:
            df2.Discharge = na_seadec(df2.Discharge)

        # Merge precipitation and discharge data
        df = df.merge(df2, left_index=True, right_index=True)

    # Else, define the discharge as NaN
    else:
        df["Discharge"] = np.nan

    # Append new data to the list
    hydro_data.append(df)

# Convert list in a dataframe, resort the columns and reset the index to
# get the Time column
hydro_data = pd.concat(hydro_data)
hydro_data = hydro_data[["Lagoon", "Precipitation", "Discharge"]]
hydro_data = hydro_data.reset_index()

# %% Read mean NDVI and temperature
spectral_data = []

forests = gpd.read_file(forests_path)       # Load the forest to clip the images

# For loop throught lagoons to get the NDVI and Temperature data
for lagoon in lagoons: 
    # Read the NetCDF data
    data = xarray.open_dataset(spectral_path.format(lagoon), decode_coords="all")
    
    # Define the forest of interest to clip the data
    roi = forests[forests.key == lagoon].geometry

    # Clip the dataset to forest of interest, all touched False implies that only
    # conserve the pixels completely overlaped by the forest
    data = data.rio.clip(roi, all_touched=False)

    # Reduce the DataSet to a DataFrame and resample it to monthly mean data
    # Calculate the mean NDVI, Surface Temperature and the pixel count
    df = pd.DataFrame({
        "NDVI": data["NDVI"].mean(dim=["latitude", "longitude"]).to_series(), 
        "Temperature": data["Surface Temperature"].mean(dim=["latitude", "longitude"]).to_series(),
        "Count": data["NDVI"].count(dim=["latitude", "longitude"]).to_series()
    }).resample("m").mean()

    # Pass the first and second entries because they have NaN
    df = df.iloc[2:,:]

    # Set the NaN values in pixel count to 0 and calculate the pixel percentage
    df.Count[df.Count.isna()] = 0
    df["PixelPercentage"] = df.Count/df.Count.max()*100
    df = df.drop("Count", axis=1)           # Then, drop the Count column

    # Create a mask that hide al values where the pixel percentegae is lower than
    # 10%
    mask = df.PixelPercentage < 10.00

    df["NDVI"][mask] = np.nan
    df["Temperature"][mask] = np.nan

    # Interpolate NaN values in NDVI and Temperature
    df.NDVI = na_seadec(df.NDVI)
    df.Temperature = na_seadec(df.Temperature)

    df["Lagoon"] = lagoon                   # Define the Lagoon column
    df.index.name = "Time"                  # Rename index column
    
    # Append spectral data
    spectral_data.append(df)

# Convert list in a dataframe, resort the columns and reset the index to
# get the Time column
spectral_data = pd.concat(spectral_data)
spectral_data = spectral_data[["Lagoon", "NDVI", "Temperature", "PixelPercentage"]]
spectral_data = spectral_data.reset_index()

# %% Merge hydrological and spectral data
data = hydro_data.merge(spectral_data, how="left", on=["Time", "Lagoon"])

# Remove values outside the timespan and resort the data based on lagoon
# and time
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
