# %% Imports
import numpy as np
import pandas as pd

from functions.stat_utils import plot_ts_components, detrend_variables

# %% Imports for plots and define some parameters
import matplotlib.pyplot as plt

# Load custom style
plt.style.use("src/style.mplstyle")

# Define custom titles
titles = {
    "Precipitation": "Total Precipitation [mm]",
    "Discharge": "Mean Discharge [m3 s-1]",
    "NDVI": "Mean NDVI",
    "Temperature": "Mean Temperature [°C]",
}

# Keys for subset the data
lagoons = ["mallorquin", "totumo", "virgen"]

# Variables to study
variables = [t for t in titles.keys()]

# %% Define constants
data_path = "data/processed/hydrological_spectral_mean_data.csv"
save_path = "data/processed/detrended_hydrological_spectral_mean_data.csv"
save_images_path = "images/{}_{}_time_series_components.{}"

# %% Load data
DATA = pd.read_csv(data_path, parse_dates=[1], index_col=0)

# Plot TS Components
figs = []

for lagoon in lagoons:
    subset = DATA[DATA.Lagoon == lagoon].copy().set_index("Time", drop=True)
    enso = subset.ENSO.values

    subset = subset[variables]
    
    if lagoon == "mallorquin":
        fs = (9, 4)
    else:
        fs = (7, 4)

    figs.append(plot_ts_components(subset, fs, enso, titles=titles))

# %% Show plots
# plt.show()

# %% Save plots
for i, (lagoon, fig) in enumerate(zip(lagoons, figs)):
    fig.savefig(save_images_path.format(i+1, lagoon, "svg"))

# %% Detrended data
# List to store the detrended dataframes
DAT2 = []

# Iterate throught lagoons to subset data
for lagoon in lagoons:
    # Subset data by lagoon
    subset = DATA[DATA.Lagoon == lagoon].copy().set_index("Time", drop=True)    
    
    # If the lagoon isn't Mallorquín, we don't need Discharge
    if lagoon == "mallorquin":
        variables = ["Precipitation", "Discharge", "NDVI", "Temperature"]

    else:
        variables = ["Precipitation", "NDVI", "Temperature"]
    
    # Detrend variables of interest from subset dataframe
    subset = detrend_variables(subset, variables)
    
    # Save subset dataframe into the list
    DAT2.append(subset)

# Merge all dataframes by lagoon
DAT2 = pd.concat(DAT2).reset_index()

# Save detrended data
DAT2.to_csv(save_path)